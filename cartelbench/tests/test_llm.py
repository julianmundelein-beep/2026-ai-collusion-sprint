"""Model layer: the schema sent to the API drops the bounds the API rejects; the local parser keeps them."""
from cartelbench.llm import api_schema, parse_json


PRICE_SCHEMA = {"type": "object", "properties": {"price": {"type": "integer", "minimum": 0, "maximum": 12},
                                                 "reason": {"type": "string", "maxLength": 200}},
                "required": ["price", "reason"], "additionalProperties": False}


def test_api_schema_drops_bounds_but_keeps_structure():
    sent = api_schema(PRICE_SCHEMA)
    assert sent["properties"]["price"] == {"type": "integer"}
    assert sent["properties"]["reason"] == {"type": "string"}
    assert sent["required"] == ["price", "reason"]
    assert sent["additionalProperties"] is False
    assert "minimum" in PRICE_SCHEMA["properties"]["price"]  # the original is untouched


def test_parse_json_still_enforces_bounds():
    assert parse_json('{"price": 9, "reason": "ok"}', PRICE_SCHEMA) == {"price": 9, "reason": "ok"}
    assert parse_json('{"price": 13, "reason": "too high"}', PRICE_SCHEMA) is None
    assert parse_json('{"price": -1, "reason": "too low"}', PRICE_SCHEMA) is None


def test_dotenv_fallback(tmp_path, monkeypatch):
    from cartelbench import llm
    for name in llm.ANTHROPIC_KEY_ENVS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.chdir(tmp_path)
    assert llm.anthropic_api_key() == ""
    (tmp_path / ".env").write_text("# local\nexport ANTHROPIC_API_KEY='sk-test-123'\n")
    assert llm.anthropic_api_key() == "sk-test-123"
