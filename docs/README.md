# Documentation index

Start with JUDGES_GUIDE.md.

| File | Generated | Content |
|---|---|---|
| `JUDGES_GUIDE.md` | no | ten minutes in order: what to open, how to check each claim, real against simulated |
| `DESIGN_NOTES.md` | no | what is taken from Bigoni et al. (2012), what the harness adds, every known deviation |
| `../cartelbench/PREREGISTRATION.md` | no | hypotheses H1 to H4, measures, decision rules, scorecard rules |
| `../cartelbench/evidence/MEASUREMENTS.md` | no (table), yes (result files) | every claimed number with command, result file and commit |
| `../cartelbench/evidence/scorecard/` | yes, `python3 -m cartelbench.scorecard` | scorecard.md, scorecard.json, figure1_scorecard.png |
| `../cartelbench/evidence/round4/`, `round5/` | yes, `python3 -m cartelbench.round4 <block>`, `python3 -m cartelbench.round5 <block>` | round 4 (more pools, Sonnet baseline, paraphrase, price screen) and round 5 (screen threshold and announcement, scripted-partner control, instructed adversary) analyses |
| `../cartelbench/evidence/ledger/` | yes, `python3 cartelbench/scripts/ledger.py` | run ledger: every run hashed and bound to its pre-registration section |
| `../cartelbench/evidence/scripted/` | yes, `python3 cartelbench/scripts/scripted_baseline.py` | naive baseline with scripted players |
| `../cartelbench/evidence/tests/` | yes, `sh cartelbench/scripts/run_tests.sh` | test log |
