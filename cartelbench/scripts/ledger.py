"""Run ledger (pre-registration amendment 4 (d)): every run ever started, hashed and bound to the pre-registration.

    python3 cartelbench/scripts/ledger.py

Lists every run folder under evidence/runs/ and evidence/pilot/ (complete or aborted), the launches in
evidence/ledger/launches.jsonl, the contamination and smoke probes and the scripted false-positive runs of the price
screen, with SHA-256 of the evidence files, the harness commit, start time, status, cost, the commit that first
added the run to git, and the pre-registration section the run belongs to: its commit must be an ancestor of the
run's harness commit and older than the run's start. Writes evidence/ledger/ledger.json and ledger.md.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cartelbench.pricing import cost_usd  # noqa: E402
from cartelbench.util import CODE_DIR, EVIDENCE_DIR, ROOT, evidence_header, write_json  # noqa: E402

FILES = ["calls.jsonl", "periods.jsonl", "config.json", "summary.json", "prompts.json"]

# pre-registration sections (PREREGISTRATION.md) and their commits
SECTIONS = {
    "base": ("aeb16a0", "hypotheses, measures, decision rules, scorecard; extra arms NoReport, ReMatch, clone; dose; robustness"),
    "R01": ("4f90714", "R01 amendment: pool sessions, validation arms, pilot threshold, shifted grid"),
    "A2": ("b688f97", "amendment 2: design check against the paper"),
    "A3": ("3930456", "amendment 3: pools of 10, validation arms at 20 duopoles, placebo, second model"),
    "A4": ("7b727bb", "amendment 4: K1 8 pools, K2 Sonnet 4 pools and nocomm, paraphrase, ledger"),
    "A5": ("61c83a9", "amendment 5: price screen"),
    "A6": ("83a3179", "amendment 6: screen threshold and announcement (N2), scripted-partner control (K), instructed adversary (N5), open models (N1)"),
}


def section_for(kind: str, model: str, regime: str, seed: int | None, offset: int) -> str:
    """The latest section that registered this run (by model, regime and seed)."""
    if kind == "pilot":
        return "A2"
    if seed is not None and 91 <= seed <= 136:
        return "A6"
    if seed in (71, 72, 73):
        return "A5"
    if seed is not None and 41 <= seed <= 64:
        return "A4"
    if regime == "placebo" or model == "claude-sonnet-5-5":
        return "A3"
    if regime in ("instructed_cartel", "fine_certain", "nocomm") or offset:
        return "R01"   # registered in R01 with 10 duopoles in 2 pools; amendment 3 changed the validation arms to 20 duopoles
    return "A2"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def sha256(path: pathlib.Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def commit_time(sha: str) -> str:
    return git("show", "-s", "--format=%cI", sha)


def is_ancestor(a: str, b: str) -> bool | None:
    if not b or b == "unknown":
        return None
    r = subprocess.run(["git", "merge-base", "--is-ancestor", a, b], cwd=ROOT, capture_output=True)
    return r.returncode == 0


def first_added(path: pathlib.Path) -> str | None:
    out = git("log", "--diff-filter=A", "--format=%h %cI", "--", str(path.relative_to(ROOT)))
    return out.splitlines()[-1] if out else None


def parse_t(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def run_entry(d: pathlib.Path, kind: str) -> dict:
    calls = d / "calls.jsonl"
    header, n_calls, tokens, first_call, last_call, model = {}, 0, [0, 0, 0, 0], None, None, None
    if calls.exists():
        with calls.open() as fh:
            for i, line in enumerate(fh):
                r = json.loads(line)
                if i == 0 and r.get("header"):
                    header = r
                    continue
                n_calls += 1
                model = r.get("model", model)
                for j, k in enumerate(("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens")):
                    tokens[j] += r.get(k) or 0
                first_call = first_call or r.get("time")
                last_call = r.get("time")
    cfg = json.loads((d / "config.json").read_text()) if (d / "config.json").exists() else {}
    summ = json.loads((d / "summary.json").read_text()) if (d / "summary.json").exists() else None
    c = cfg.get("config") or {}
    model = model or c.get("model")
    harness = (header.get("commit") or cfg.get("commit") or "").replace("-dirty", "")
    started = cfg.get("started") or first_call
    cost = (summ or {}).get("n_table", {}).get("cost_usd") if summ else None
    if cost is None and model and model.startswith("claude"):
        cost = cost_usd(model, *tokens)
    sec = section_for(kind, model or "", c.get("regime", ""), c.get("seed"), c.get("price_offset") or 0)
    sec_sha, _ = SECTIONS[sec]
    sec_time = commit_time(sec_sha)
    return {
        "run_id": d.name, "kind": kind, "folder": str(d.relative_to(CODE_DIR)), "status": "complete" if summ else "aborted",
        "model": model, "regime": c.get("regime"), "seed": c.get("seed"), "duopoles": c.get("duopoles"), "pools": c.get("pools"),
        "prompt_variant": c.get("prompt_variant") or "original", "price_offset": c.get("price_offset") or 0,
        "partner": c.get("partner") or "", "screen_p": c.get("screen_p"),
        "detection_override": c.get("detection_prob"), "label": c.get("label") or "",
        "harness_commit": header.get("commit") or cfg.get("commit"), "started": started, "first_call": first_call, "last_call": last_call,
        "finished": (summ or {}).get("finished"), "calls": n_calls, "cost_usd": cost,
        "sha256": {f: sha256(d / f) for f in FILES}, "first_added_to_git": first_added(d / "config.json"),
        "registered_in": sec, "section_commit": sec_sha, "section_time": sec_time,
        "section_is_ancestor": is_ancestor(sec_sha, harness),
        "section_before_start": (parse_t(sec_time) < parse_t(started)) if started else None,
    }


def main() -> int:
    runs = []
    for d in sorted((EVIDENCE_DIR / "runs").iterdir()):
        if d.is_dir():
            runs.append(run_entry(d, "run"))
    for d in sorted((EVIDENCE_DIR / "pilot").iterdir()):
        if d.is_dir():
            runs.append(run_entry(d, "pilot"))
    probes = []
    for p in sorted(list((EVIDENCE_DIR / "contamination").glob("*.json")) + list((EVIDENCE_DIR / "smoke").glob("*.json"))):
        j = json.loads(p.read_text())
        probes.append({"file": str(p.relative_to(CODE_DIR)), "sha256": sha256(p), "commit": j.get("commit"), "time": j.get("time")})
    launches_path = EVIDENCE_DIR / "ledger" / "launches.jsonl"
    launches = [json.loads(x) for x in launches_path.read_text().splitlines()] if launches_path.exists() else []
    started_ids = [x["run_id"] for x in launches if x["event"] == "start"]
    ended = {x["run_id"]: x for x in launches if x["event"] == "end"}
    folders = {r["run_id"] for r in runs}
    launch_rows = [{"run_id": i, "folder": i in folders, "end": (ended.get(i) or {}).get("status", "no end line (running or killed)")}
                   for i in started_ids]
    fp = json.loads((EVIDENCE_DIR / "round4" / "screen_fp.json").read_text()) if (EVIDENCE_DIR / "round4" / "screen_fp.json").exists() else {}
    scripted = [{"player": k, "runs": v["runs"], "periods_sha256_without_header": v["periods_sha256_without_header"],
                 "note": "not committed (52 MB, deterministic); rebuilt by python3 cartelbench/scripts/screen_fp.py"}
                for k, v in (fp.get("players") or {}).items()]
    deleted = git("log", "--all", "--diff-filter=D", "--name-only", "--format=", "--", "cartelbench/evidence/runs", "cartelbench/evidence/pilot")
    violations = [r["run_id"] for r in runs if r["section_before_start"] is False or r["section_is_ancestor"] is False]
    total = sum(r["cost_usd"] or 0 for r in runs)
    aborted_cost = sum(r["cost_usd"] or 0 for r in runs if r["status"] == "aborted")
    out = {**evidence_header("python3 cartelbench/scripts/ledger.py"),
           "sections": {k: {"commit": v[0], "time": commit_time(v[0]), "what": v[1]} for k, v in SECTIONS.items()},
           "n_runs": len(runs), "n_complete": sum(r["status"] == "complete" for r in runs),
           "n_aborted": sum(r["status"] == "aborted" for r in runs), "cost_usd_runs_and_pilot": round(total, 4),
           "cost_usd_aborted": round(aborted_cost, 4),
           "registration_violations": violations, "deleted_run_files_in_git_history": deleted.splitlines(),
           "coverage_note": ("Runs since amendment 4 are also listed in launches.jsonl at start, so a run killed before it wrote "
                             "a folder still appears. Runs before amendment 4 are listed from their folders and git history; "
                             "no run file was ever deleted in git, but a run that crashed before writing a folder before "
                             "amendment 4 could not be listed."),
           "runs": runs, "launches": launch_rows, "probes": probes, "scripted_screen_runs": scripted}
    ledger_dir = EVIDENCE_DIR / "ledger"
    write_json(ledger_dir / "ledger.json", out)
    lines = [f"<!-- Generated by {out['generated_by']} at {out['time']} from commit {out['commit']}. Do not edit by hand. -->",
             "# Run ledger", "",
             f"{out['n_runs']} run folders ({out['n_complete']} complete, {out['n_aborted']} aborted), cost {total:.2f} USD "
             f"(aborted {aborted_cost:.2f} USD). Registration check (section commit an ancestor of the harness commit and "
             f"older than the run's start): {len(violations)} exceptions" + (": " + ", ".join(violations) if violations else "") + ".", "",
             out["coverage_note"], "", "## Pre-registration sections", "", "| section | commit | time (UTC) | what |", "|---|---|---|---|"]
    for k, v in out["sections"].items():
        lines.append(f"| {k} | {v['commit']} | {v['time']} | {v['what']} |")
    lines += ["", "## Runs", "", "| run | status | model | regime | seed | variant | started | calls | cost USD | section | before start | ancestor | sha256 calls.jsonl |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in runs:
        lines.append(f"| {r['run_id']} | {r['status']} | {r['model']} | {r['regime']} | {r['seed']} | {r['prompt_variant']} | {r['started']} | "
                     f"{r['calls']} | {0 if r['cost_usd'] is None else r['cost_usd']:.3f} | {r['registered_in']} | {r['section_before_start']} | "
                     f"{r['section_is_ancestor']} | {(r['sha256']['calls.jsonl'] or '')[:16]} |")
    lines += ["", "## Launch log (since amendment 4)", "", "| run | folder | end |", "|---|---|---|"]
    for x in launch_rows:
        lines.append(f"| {x['run_id']} | {x['folder']} | {x['end']} |")
    lines += ["", "## Probes", "", "| file | commit | time | sha256 |", "|---|---|---|---|"]
    for p in probes:
        lines.append(f"| {p['file']} | {(p['commit'] or '')[:12]} | {p['time']} | {p['sha256'][:16]} |")
    if scripted:
        lines += ["", "## Scripted price-screen runs (not committed, deterministic)", "", "| player | runs | content sha256 |", "|---|---|---|"]
        for s in scripted:
            lines.append(f"| {s['player']} | {', '.join(s['runs'])} | {', '.join(h[:16] for h in s['periods_sha256_without_header'])} |")
    (ledger_dir / "ledger.md").write_text("\n".join(lines) + "\n")
    print(f"{out['n_runs']} runs ({out['n_complete']} complete, {out['n_aborted']} aborted), {total:.2f} USD; exceptions: {violations}")
    print(f"ledger sha256 {sha256(ledger_dir / 'ledger.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
