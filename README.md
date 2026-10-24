# CartelBench: the Bigoni cartel experiment replayed with LLM sellers

Working name; the final project name follows Julian's pick (CORE_IDEA.md, "Message"). Submission to the AI Collusion Research Sprint (Apart Research, October 2026), Track 1: Markets and Collusion, research question 1.5 (Which single restriction removes the most collusion at the least cost?) with 1.1 (Which variables are necessary for collusion to emerge in markets?) as the second question.

Links: [Repository](https://github.com/julianmundelein-beep/2026-ai-collusion-sprint) · [The paper (RAND 2012, publisher page)](https://onlinelibrary.wiley.com/doi/10.1111/j.1756-2171.2012.00170.x) · [Pre-registration](cartelbench/PREREGISTRATION.md) · [Build plan](cartelbench/BUILD_PLAN.md) · [Measurements](cartelbench/evidence/MEASUREMENTS.md) · [Judges' guide](docs/JUDGES_GUIDE.md) · [Design notes: what comes from the paper, what is new](docs/DESIGN_NOTES.md) · Research report: to follow (PDF on the official template)

Cartel policy (fines, leniency programmes, whistleblower rewards) rests on assumptions about human players, and nobody has tested these instruments on LLM pricing agents. This repository replays the cartel laboratory experiment of Bigoni, Fridolfsson, Le Coq and Spagnolo (RAND Journal of Economics, 2012) with LLM sellers under the same rules, payoffs, regimes and matching, so that every number sits next to the published human result. The output is a scorecard "x of 8 Bigoni results replicated" per model, a regime ranking with cluster-bootstrap intervals, and a cost per regime (fines, reports as investigation load, rewards). Status on 2026-10-24: harness checked against the paper and tests done (46 tests green, M01), pre-registration committed with the jury-round R01 amendment, pilot with real models pending the API key.

## What it does

One command runs one regime for one model. A pool of 20 agents plays the repeated duopoly: prices 0 to 12, payoff table of the paper, seven steps per period (communication wish, two-round price discussion, price plus secret report, prices revealed plus public report, detection with probability 0.10, points, feedback), same partner with probability 0.85 per period, session end after period 20 at the first rematching event. Regimes are configuration: laissez-faire (positive control), fine, leniency, reward, plus the arms NoReport, ReMatch and clone. Every model call is one JSON line with run id, seed, model, commit, pool, period, agent, step, prompt, answer and token usage. Refusals and invalid answers are counted and reported, never retried to success.

## Run it

```bash
cd cartelbench
pip install -e .                      # anthropic, numpy, pandas, matplotlib
sh scripts/run_tests.sh               # 36 tests, no API
python3 scripts/scripted_baseline.py  # naive baseline with scripted players, no API
export ANTHROPIC_API_KEY=...          # or put it in .env (see .env.example)
python3 -m cartelbench.smoke --model claude-haiku-5-5                                   # one real call
python3 -m cartelbench.contamination --model claude-haiku-5-5                           # does the model know the paper?
python3 -m cartelbench.pilot --models claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5  # positive control, 3 duopoles each
```

One command per regime and model (the main runs; 20 duopoles as 4 independent pool sessions of 10 agents, the bootstrap unit):

```bash
python3 -m cartelbench.run --regime laissez_faire --model claude-haiku-5-5 --duopoles 20 --seed 1
python3 -m cartelbench.run --regime fine          --model claude-haiku-5-5 --duopoles 20 --seed 2
python3 -m cartelbench.run --regime leniency      --model claude-haiku-5-5 --duopoles 20 --seed 3
python3 -m cartelbench.run --regime reward        --model claude-haiku-5-5 --duopoles 20 --seed 4
python3 -m cartelbench.run --regime noreport      --model claude-haiku-5-5 --duopoles 20 --seed 5
python3 -m cartelbench.run --regime rematch       --model claude-haiku-5-5 --duopoles 20 --seed 6
python3 -m cartelbench.run --regime clone         --model claude-haiku-5-5 --duopoles 20 --seed 7
python3 -m cartelbench.run --regime instructed_cartel --model claude-haiku-5-5 --duopoles 10 --pools 2 --seed 11  # validation: must form cartels
python3 -m cartelbench.run --regime fine_certain      --model claude-haiku-5-5 --duopoles 10 --pools 2 --seed 12  # validation: must kill cartels
python3 -m cartelbench.run --regime nocomm            --model claude-haiku-5-5 --duopoles 10 --pools 2 --seed 13  # validation: no discussion
python3 -m cartelbench.run --regime laissez_faire --price-offset 5 --model claude-haiku-5-5 --duopoles 10 --pools 2 --seed 14  # contamination: shifted grid
python3 -m cartelbench.run --regime leniency --detection 0.05 --model claude-haiku-5-5 --duopoles 20 --seed 8   # dose
python3 -m cartelbench.run --regime laissez_faire --payoff-scale 2 --model claude-haiku-5-5 --duopoles 10 --seed 9  # robustness
python3 -m cartelbench.analyze --bootstrap evidence/runs/<run_id> ...     # measures with 95 percent intervals over pool sessions
python3 -m cartelbench.scorecard --model claude-haiku-5-5                 # scorecard.md, scorecard.json, figure1_dotplot.png, figure1b_scorecard_table.png
python3 -m cartelbench.prompts --regime fine                              # verbatim instructions for the appendix
```

Other providers: `--provider openai --base-url https://<endpoint>/v1 --api-key-env OPENROUTER_API_KEY --model <id>` works with any OpenAI-compatible chat endpoint (Modal, OpenRouter, Nebius). Scripted players instead of a model: `--player collude|deviate|nash|random|tit`.

## Example: one period of one pair (scripted players, no API)

Input: regime `leniency`, agents Firm Alder and Firm Birch, period 4, both agreed on price 9 in the discussion. Alder plays "collude" (price 9, no report), Birch plays "deviate" (best reply to 9, secret report). Output line in `periods.jsonl` (abridged): `talked: true, agreed_price: 9, prices: [9, 7], secret_report: [false, true], reporters: ["birch"], detected: false, convicted: true, fines: [-200, 0], market_points: [20, 296], points: [-180, 296]`. Alder's feedback row for period 4 reads "agreement reported (1 firm reported); you paid 200; agreement ended". The measures in `summary.json` then show deviation rate 0.5 and report rate 1.0 for this pair.

## What is real, what is simulated

- Real: every model decision in `evidence/runs/` and `evidence/pilot/` comes from a live API call, logged with token usage and the model id the API returned. The payoff points are computed by the harness from the table, not by the model. Every `summary.json` carries an n-table: pool sessions, duopoles, periods, calls, refusals, invalid answers, errors, defaulted decisions, tokens and cost.
- Simulated: the market is the laboratory game of the paper, not a real market; fines and rewards are points told to the agents, not money. Scripted players (`--player ...`) are simulations by construction and are labelled `provider: scripted` in every file.
- From the paper: `cartelbench/data/payoff_table.csv` is the transcription of Table 1 (169 cells, checked against the paper's demand model); the rules of Sections 3.2 to 3.5 are implemented and tested. The instructions in `cartelbench/cartelbench/prompts.py` render the design in neutral words; the verbatim subject instructions (2009 version) are still to be aligned. See `docs/DESIGN_NOTES.md`.

## How to verify

- `sh cartelbench/scripts/run_tests.sh` reruns the acceptance tests and rewrites `cartelbench/evidence/tests/pytest_latest.txt`.
- Every result file starts with `Generated by <command> at <time> from commit <sha>`; `cartelbench/evidence/MEASUREMENTS.md` maps each claimed number to its command and file.
- `python3 -m cartelbench.analyze <run dir>` recomputes every measure from `periods.jsonl`; `calls.jsonl` holds every prompt and answer so a run can be audited line by line.

## Prior work and new work

- Prior work (cited, not ours): the experimental design, payoff structure, regimes, matching and termination rules, and the human results are from Bigoni, Fridolfsson, Le Coq and Spagnolo, "Fines, Leniency and Rewards in Antitrust", RAND Journal of Economics 43(2), 2012 (working paper CEPR DP 7417, 2009). The sprint's starter repository (poseidon-research/collusion_hackathon) was read as reference only; no code from it is used.
- New work during the sprint (all code in this repository): the harness, regimes, scripted players, model clients, tests, measures, bootstrap, scorecard, figures and all runs. No preexisting code.
- LLM use: Claude Code wrote the code and drafts under Julian's direction; the models under test are named with their ids in every result file.

## Repository map

| Path | What |
|---|---|
| `cartelbench/cartelbench/` | the package: `game.py` (payoffs), `regimes.py` (Table 2 rules), `prompts.py`, `players.py`, `llm.py` (Anthropic, OpenAI-compatible, fake), `engine.py` (pools, periods, matching, logs), `run.py`, `pilot.py`, `smoke.py`, `contamination.py`, `analyze.py`, `scorecard.py` |
| `cartelbench/tests/` | acceptance tests A1 to A8 of the build plan |
| `cartelbench/data/` | payoff table, human baseline candidates |
| `cartelbench/evidence/` | measurements, test logs, scripted baseline, pilot and main runs, scorecard |
| `cartelbench/PREREGISTRATION.md` | hypotheses, measures, decision rules, scorecard rules (committed before the first model call) |
| `docs/` | judges' guide, design notes |
| `hackathon/` | working notes of the sprint (leave the tree at submission) |
