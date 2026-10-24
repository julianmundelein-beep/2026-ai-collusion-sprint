"""Model clients. One interface, three implementations:

* AnthropicClient: the official `anthropic` SDK (Claude models).
* OpenAICompatibleClient: any /v1/chat/completions endpoint (Modal, OpenRouter, Nebius).
* FakeClient: scripted answers for tests, no network.

Every call returns a ModelResponse with the raw text, token usage, latency and
flags for refusal, transport error and invalid JSON. Nothing here retries a
refusal or an invalid answer: the engine counts them and plays a default action.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


@dataclass
class ModelResponse:
    text: str = ""
    parsed: dict | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    latency_s: float = 0.0
    stop_reason: str = ""
    refusal: bool = False
    error: str = ""
    invalid_json: bool = False
    prompt_user: str = ""
    raw: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.parsed is not None and not self.refusal and not self.error


def parse_json(text: str, schema: dict) -> dict | None:
    """Parse the model's JSON; accept a JSON object embedded in prose; validate required keys and types."""
    candidates = [text]
    m = JSON_RE.search(text or "")
    if m:
        candidates.append(m.group(0))
    for cand in candidates:
        try:
            obj = json.loads(cand)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(obj, dict):
            continue
        ok = True
        for key in schema.get("required", []):
            if key not in obj:
                ok = False
                break
            spec = schema["properties"][key]
            val = obj[key]
            if spec["type"] == "boolean" and not isinstance(val, bool):
                ok = False
            elif spec["type"] == "integer":
                if isinstance(val, bool) or not isinstance(val, int):
                    ok = False
                elif not (spec.get("minimum", val) <= val <= spec.get("maximum", val)):
                    ok = False
            elif spec["type"] == "string" and not isinstance(val, str):
                ok = False
        if ok:
            return obj
    return None


class ModelClient(Protocol):
    model: str
    provider: str

    async def complete(self, system: str, user: str, schema: dict) -> ModelResponse: ...


class AnthropicClient:
    provider = "anthropic"

    def __init__(self, model: str, effort: str = "low", max_tokens: int = 2048, concurrency: int = 8,
                 timeout_s: float = 120.0):
        import anthropic  # imported here so tests without the SDK still run the engine

        self.model = model
        self.effort = effort
        self.max_tokens = max_tokens
        self._client = anthropic.AsyncAnthropic(timeout=timeout_s, max_retries=2)
        self._sem = asyncio.Semaphore(concurrency)
        self._anthropic = anthropic

    async def complete(self, system: str, user: str, schema: dict) -> ModelResponse:
        resp = ModelResponse()
        t0 = time.monotonic()
        async with self._sem:
            try:
                msg = await self._client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                    messages=[{"role": "user", "content": user}],
                    output_config={"effort": self.effort,
                                   "format": {"type": "json_schema", "schema": schema}},
                )
            except self._anthropic.APIStatusError as exc:  # 4xx/5xx after SDK retries
                resp.error = f"api_status_{exc.status_code}: {str(exc)[:300]}"
                resp.latency_s = time.monotonic() - t0
                return resp
            except self._anthropic.APIConnectionError as exc:
                resp.error = f"connection: {str(exc)[:300]}"
                resp.latency_s = time.monotonic() - t0
                return resp
            except Exception as exc:  # noqa: BLE001  anything else is logged, never raised into a run
                resp.error = f"{type(exc).__name__}: {str(exc)[:300]}"
                resp.latency_s = time.monotonic() - t0
                return resp
        resp.latency_s = time.monotonic() - t0
        resp.stop_reason = msg.stop_reason or ""
        usage = msg.usage
        resp.input_tokens = usage.input_tokens or 0
        resp.output_tokens = usage.output_tokens or 0
        resp.cache_read_tokens = getattr(usage, "cache_read_input_tokens", 0) or 0
        resp.cache_write_tokens = getattr(usage, "cache_creation_input_tokens", 0) or 0
        resp.text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        resp.raw = {"id": msg.id, "model": msg.model}
        if msg.stop_reason == "refusal":
            resp.refusal = True
            details = getattr(msg, "stop_details", None)
            if details is not None:
                resp.raw["stop_details"] = {"category": getattr(details, "category", None),
                                            "explanation": getattr(details, "explanation", None)}
            return resp
        resp.parsed = parse_json(resp.text, schema)
        resp.invalid_json = resp.parsed is None
        return resp


class OpenAICompatibleClient:
    """Minimal chat-completions client over the standard library (no extra dependency)."""

    provider = "openai_compatible"

    def __init__(self, model: str, base_url: str, api_key_env: str = "OPENAI_API_KEY",
                 temperature: float = 1.0, max_tokens: int = 2048, concurrency: int = 8, timeout_s: float = 120.0):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = os.environ.get(api_key_env, "")
        if not self.api_key:
            raise RuntimeError(f"environment variable {api_key_env} is not set")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_s = timeout_s
        self._sem = asyncio.Semaphore(concurrency)

    def _post(self, payload: dict) -> dict:
        import urllib.request

        req = urllib.request.Request(
            self.base_url + "/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout_s) as fh:
            return json.loads(fh.read().decode())

    async def complete(self, system: str, user: str, schema: dict) -> ModelResponse:
        resp = ModelResponse()
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user + "\n\nJSON schema:\n" + json.dumps(schema)}],
            "response_format": {"type": "json_object"},
        }
        t0 = time.monotonic()
        async with self._sem:
            for attempt in range(3):
                try:
                    data = await asyncio.to_thread(self._post, payload)
                    break
                except Exception as exc:  # noqa: BLE001
                    resp.error = f"{type(exc).__name__}: {str(exc)[:300]}"
                    await asyncio.sleep(2 ** attempt)
            else:
                resp.latency_s = time.monotonic() - t0
                return resp
        resp.error = ""
        resp.latency_s = time.monotonic() - t0
        choice = (data.get("choices") or [{}])[0]
        resp.text = (choice.get("message") or {}).get("content") or ""
        resp.stop_reason = choice.get("finish_reason") or ""
        usage = data.get("usage") or {}
        resp.input_tokens = usage.get("prompt_tokens", 0) or 0
        resp.output_tokens = usage.get("completion_tokens", 0) or 0
        resp.raw = {"id": data.get("id"), "model": data.get("model")}
        if resp.stop_reason == "content_filter":
            resp.refusal = True
            return resp
        resp.parsed = parse_json(resp.text, schema)
        resp.invalid_json = resp.parsed is None
        return resp


class FakeClient:
    """Scripted client for tests: `script(step_hint, user, schema) -> str | dict`."""

    provider = "fake"

    def __init__(self, script: Callable[[str, dict], Any], model: str = "fake-model", latency_s: float = 0.0):
        self.model = model
        self.script = script
        self.latency_s = latency_s
        self.calls = 0

    async def complete(self, system: str, user: str, schema: dict) -> ModelResponse:
        self.calls += 1
        out = self.script(user, schema)
        resp = ModelResponse(input_tokens=len(system) // 4 + len(user) // 4, output_tokens=20,
                             latency_s=self.latency_s, stop_reason="end_turn")
        if out is None:
            resp.refusal = True
            resp.stop_reason = "refusal"
            return resp
        resp.text = out if isinstance(out, str) else json.dumps(out)
        resp.parsed = parse_json(resp.text, schema)
        resp.invalid_json = resp.parsed is None
        return resp


def make_client(provider: str, model: str, **kw) -> ModelClient:
    if provider == "anthropic":
        return AnthropicClient(model, **{k: v for k, v in kw.items() if k in {"effort", "max_tokens", "concurrency", "timeout_s"}})
    if provider == "openai":
        return OpenAICompatibleClient(model, **{k: v for k, v in kw.items()
                                                if k in {"base_url", "api_key_env", "temperature", "max_tokens", "concurrency", "timeout_s"}})
    raise ValueError(f"unknown provider {provider}")
