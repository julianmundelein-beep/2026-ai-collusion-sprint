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
    # config.json as the engine writes it: "config" is RunConfig (overrides None = default), "regime" the effective regime
    base_s = {"regime": "leniency", "model": "m", "player": "llm", "price_offset": 0}
    def conf(**over):
        cfg = {"price_offset": 0, "payoff_scale": 1.0, "detection_prob": None, "fine": None, **over}
        reg = {"key": "leniency", "detection_prob": cfg["detection_prob"] or 0.10, "fine": cfg["fine"] or 200}
        return {"config": cfg, "regime": reg}
    assert is_core_run(_run(tmp_path, "a", base_s, conf()), base_s)
    s = {**base_s, "price_offset": 5}
    assert not is_core_run(_run(tmp_path, "b", s, conf(price_offset=5)), s)
    assert not is_core_run(_run(tmp_path, "c", base_s, conf(payoff_scale=2.0)), base_s)
    assert not is_core_run(_run(tmp_path, "d", base_s, conf(detection_prob=0.05)), base_s)
    assert not is_core_run(_run(tmp_path, "e", base_s, conf(fine=300)), base_s)
    # an older config.json without the nested block but with an effective regime that differs from the registered one
    assert not is_core_run(_run(tmp_path, "g", base_s, {"regime": {"key": "leniency", "detection_prob": 0.2, "fine": 200}}), base_s)
    assert is_core_run(_run(tmp_path, "h", base_s, {"regime": {"key": "leniency", "detection_prob": 0.1, "fine": 200}}), base_s)
