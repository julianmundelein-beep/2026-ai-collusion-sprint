# Judges' guide: ten minutes

1. Read the first paragraph of the root README: the question (do fines, leniency and rewards act on LLM sellers as on humans?), the method (the published experiment replayed with the same rules) and the result format (scorecard x of 8).
2. Open `cartelbench/PREREGISTRATION.md`. The commit that added it (`git log --follow cartelbench/PREREGISTRATION.md`) predates every model call in `cartelbench/evidence/`.
3. Open `cartelbench/evidence/scorecard/scorecard.md` (once the main runs exist): one row per published result, human value next to the LLM value, yes or no by the pre-registered rule. `figure1_scorecard.png` is the same table.
4. Pick any run in `cartelbench/evidence/runs/`. `config.json` names the regime, seed, model and payoff table; `calls.jsonl` holds every prompt and answer with token usage; `periods.jsonl` every period; `summary.json` the measures and the counts of refusals, invalid answers and defaulted decisions. `python3 -m cartelbench.analyze <run dir>` recomputes the measures.
5. Check the positive control first: `cartelbench/evidence/pilot/pilot_summary.json` says per model how many agent-periods priced above the Nash price 3 in laissez-faire and how many answers were refusals.
6. Check what is simulated: the market is a laboratory game, fines are told, not paid; `--player` runs are scripted and labelled `provider: scripted`. The payoff table's provenance is in its header line (reconstructed until the paper's Table 1 is transcribed).
7. Rerun the tests: `sh cartelbench/scripts/run_tests.sh` (no API needed).
