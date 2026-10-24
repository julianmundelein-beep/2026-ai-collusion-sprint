"""Second provider: an open model served by vLLM on Modal as an OpenAI-compatible endpoint.

    P2_DOWNLOAD_ONLY=1 P2_MODEL=qwen2.5-32b-instruct modal run cartelbench/scripts/modal_vllm.py::download  # weights (CPU)
    P2_MODEL=qwen2.5-32b-instruct modal deploy cartelbench/scripts/modal_vllm.py          # endpoint up (scales to zero)
    curl -H "Authorization: Bearer $P2_KEY" https://<workspace>--cartelbench-vllm-serve.modal.run/v1/models
    modal app stop cartelbench-vllm                                                        # endpoint down after the runs

The harness talks to it with
    python3 -m cartelbench.run --provider openai --base-url https://<...>.modal.run/v1 --api-key-env P2_KEY --model <served name> ...

The bearer token lives in the Modal secret `cartelbench-vllm` (key VLLM_API_KEY) and locally in the environment
variable P2_KEY; it is never written to the repository. Model, revision, dtype and sampling defaults are fixed in
PREREGISTRATION_provider2.md; the GPU is an operational choice (P2_GPU overrides the candidate's default).
Cost guards: one container at most, scale to zero after 5 idle minutes, `modal app stop` after the last run.
"""
from __future__ import annotations

import os
import subprocess

import modal

# served name -> Hugging Face repo, pinned revision, default GPU, extra vLLM arguments
CANDIDATES = {
    "qwen2.5-32b-instruct": {
        "repo": "Qwen/Qwen2.5-32B-Instruct",
        "revision": "5ede1c97bbab6ce5cda5812749b4c0bdf79b18dd",
        "gpu": "A100-80GB",
        "args": [],
    },
    "qwen3-32b": {
        "repo": "Qwen/Qwen3-32B",
        "revision": "9216db5781bf21249d130ec9da846c4624c16137",
        "gpu": "A100-80GB",
        # non-thinking mode for every request (Qwen3 chat template switch)
        "args": ["--default-chat-template-kwargs", '{"enable_thinking": false}'],
    },
    "llama-3.1-8b-instruct": {
        # ungated mirror of meta-llama/Llama-3.1-8B-Instruct (same weights, no Hugging Face token needed)
        "repo": "unsloth/Meta-Llama-3.1-8B-Instruct",
        "revision": "a2856192dd7c25b842431f39c179a6c2c2f627d1",
        "gpu": "L40S",
        "args": [],
    },
}

MODEL = os.environ.get("P2_MODEL", "qwen2.5-32b-instruct")
SPEC = CANDIDATES[MODEL]
GPU = os.environ.get("P2_GPU", SPEC["gpu"])
# P2_DOWNLOAD_ONLY=1 defines the CPU download alone (Modal refuses an app with a GPU function until the workspace
# has a payment method on file, so the weights can be fetched before that)
DOWNLOAD_ONLY = os.environ.get("P2_DOWNLOAD_ONLY", "") == "1"
VLLM_VERSION = "0.31.0"
MAX_MODEL_LEN = 8192  # prompts stay under about 4,000 tokens (Haiku max 2,180 plus the appended schema), answers under 2,048
PORT = 8000

hf_cache = modal.Volume.from_name("cartelbench-hf-cache", create_if_missing=True)
vllm_cache = modal.Volume.from_name("cartelbench-vllm-cache", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install(f"vllm=={VLLM_VERSION}", "huggingface_hub[hf_transfer]")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "HF_HOME": "/root/.cache/huggingface", "P2_MODEL": MODEL, "P2_GPU": GPU,
          "P2_DOWNLOAD_ONLY": "1" if DOWNLOAD_ONLY else ""})
)

app = modal.App("cartelbench-vllm", image=image)
VOLUMES = {"/root/.cache/huggingface": hf_cache, "/root/.cache/vllm": vllm_cache}


@app.function(volumes=VOLUMES, timeout=60 * 60)
def download() -> str:
    """Fetch the pinned weights into the volume on a CPU container, so no GPU time is spent downloading."""
    from huggingface_hub import snapshot_download

    path = snapshot_download(SPEC["repo"], revision=SPEC["revision"],
                             ignore_patterns=["*.pt", "*.bin", "original/*"])
    hf_cache.commit()
    return path


@app.function(timeout=15 * 60)
def check_flags() -> str:
    """CPU check that this vLLM build defines every option `serve` passes (the CLI itself needs a GPU to start)."""
    import importlib.util
    import pathlib

    root = pathlib.Path(importlib.util.find_spec("vllm").submodule_search_locations[0])
    src = "\n".join(p.read_text(errors="ignore") for p in (root / "engine").rglob("*.py"))
    src += "\n".join(p.read_text(errors="ignore") for p in (root / "entrypoints").rglob("*.py"))
    src += "\n".join(p.read_text(errors="ignore") for p in (root / "config").rglob("*.py"))
    fields = ["revision", "served_model_name", "api_key", "dtype", "max_model_len", "enable_prefix_caching",
              "gpu_memory_utilization", "generation_config", "default_chat_template_kwargs"]
    report = "\n".join(f"--{f.replace('_', '-')}: {'ok' if (f + ':') in src else 'MISSING'}" for f in fields)
    print(report)
    return report


def serve() -> None:
    cmd = [
        "vllm", "serve", SPEC["repo"],
        "--revision", SPEC["revision"],
        "--served-model-name", MODEL,
        "--host", "0.0.0.0", "--port", str(PORT),
        "--api-key", os.environ["VLLM_API_KEY"],
        "--dtype", "bfloat16",
        "--max-model-len", str(MAX_MODEL_LEN),
        "--enable-prefix-caching",
        "--gpu-memory-utilization", "0.92",
        # vLLM's neutral sampling defaults instead of the model's generation_config.json: the harness sends
        # temperature 1.0 and nothing else, as with the Anthropic API (no top_p, top_k or repetition penalty)
        "--generation-config", "vllm",
        *SPEC["args"],
    ]
    subprocess.Popen(cmd)


if not DOWNLOAD_ONLY:
    serve = app.function(
        gpu=GPU,
        volumes=VOLUMES,
        secrets=[modal.Secret.from_name("cartelbench-vllm")],
        max_containers=1,
        scaledown_window=5 * 60,
        timeout=24 * 60 * 60,
    )(modal.concurrent(max_inputs=128)(modal.web_server(port=PORT, startup_timeout=30 * 60)(serve)))
