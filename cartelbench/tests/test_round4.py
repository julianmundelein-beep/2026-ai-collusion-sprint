"""Round 4 (amendment 4): launch log of the run ledger."""
import json

from cartelbench import run as run_mod


def test_launch_log_lists_start_and_end(tmp_path, monkeypatch):
    log = tmp_path / "launches.jsonl"
    monkeypatch.setattr(run_mod, "LAUNCH_LOG", log)
    rc = run_mod.main(["--regime", "fine", "--player", "nash", "--duopoles", "2", "--pools", "1", "--seed", "3",
                       "--out-dir", str(tmp_path / "runs")])
    assert rc == 0
    rows = [json.loads(x) for x in log.read_text().splitlines()]
    assert [r["event"] for r in rows] == ["start", "end"]
    assert rows[0]["run_id"] == rows[1]["run_id"] and rows[1]["status"] == "complete"
    assert (tmp_path / "runs" / rows[0]["run_id"] / "summary.json").exists()
