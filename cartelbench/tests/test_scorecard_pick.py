"""The scorecard picks, per regime and model, the latest run at the registered settings and skips shifted-grid,
scaled-payoff, dose and fine-override runs that share the folder."""
import json

from cartelbench.scorecard import is_core_run


def _run(tmp_path, name, summary, config):
    d = tmp_path / name
    d.mkdir()
    (d / "summary.json").write_text(json.dumps(summary))
    (d / "config.json").write_text(json.dumps(config))
    return d


def test_is_core_run_skips_overrides(tmp_path):
    base_s = {"regime": "laissez_faire", "model": "m", "player": "llm", "price_offset": 0}
    base_c = {"price_offset": None, "payoff_scale": None, "detection_prob": None, "fine": None}
    assert is_core_run(_run(tmp_path, "a", base_s, base_c), base_s)
    s = {**base_s, "price_offset": 5}
    assert not is_core_run(_run(tmp_path, "b", s, {**base_c, "price_offset": 5}), s)
    assert not is_core_run(_run(tmp_path, "c", base_s, {**base_c, "payoff_scale": 2.0}), base_s)
    assert not is_core_run(_run(tmp_path, "d", base_s, {**base_c, "detection_prob": 0.05}), base_s)
    assert not is_core_run(_run(tmp_path, "e", base_s, {**base_c, "fine": 300}), base_s)
    assert is_core_run(_run(tmp_path, "f", base_s, {**base_c, "payoff_scale": 1.0}), base_s)
