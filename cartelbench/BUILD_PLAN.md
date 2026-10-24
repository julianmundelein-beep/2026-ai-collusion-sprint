# Build plan · backend (CartelBench, Bigoni twin)

Written by the backend session (skill hackathon-backend) on 2026-10-24 16:40 HKT; updated at every checkpoint. Decisions Julian takes go to `hackathon/DECISIONS.md` as well.

- Code folder: `cartelbench/` (name follows Julian's pick in CORE_IDEA.md "Message"; recommended option (a) CartelBench)
- Build window: start Sat 2026-10-24 16:30 HKT → internal deadline Mon 2026-10-26 16:59 HKT (HKT, UTC+8). The card's own clock is tighter and binds: harness, tests, pilot and pre-registration by Sat 23:00 HKT; core runs Sun 08:00 to 13:00 HKT (Julian, local); dose, robustness, analysis, scorecard, Figure 1 Sun 13:00 to 17:00 HKT.
- Stack (KEEP in DECISIONS.md once Julian confirms): Python 3.13, standard library for the game engine, `anthropic` SDK 2.x for Claude models, an OpenAI-compatible adapter (stdlib `urllib`) for Modal, OpenRouter and Nebius, `pytest` for tests, `numpy`, `pandas`, `matplotlib` for analysis and Figure 1. No framework, no database, no server. Alternative considered: the starter repo's `poseidon_compute` runner (knows only Nebius and OpenRouter, needs `uv`); rejected because the Anthropic credit is the main budget and the harness must be new sprint code anyway.

## Checkpoints

Share of window is measured on the card's clock (Sat 16:30 to Mon 16:59 HKT = 48.5 h), but the card's fixed times win where they are earlier.

| Stage | Done when | Due (share of window) | Due (clock, HKT) | State |
|---|---|---|---|---|
| 1 Toolchain | pytest runs; the Anthropic SDK answers one real call with Julian's key; scripted players play a full session without API | 10 % | Sat 21:20 | done 2026-10-24 17:50 UTC+8 (cloud): 49 tests, smoke call M10; the cloud environment provides the key as `CARTELBENCH_ANTHROPIC_KEY` |
| 2 Happy path | pilot 3 models × 3 duopoles laissez-faire runs with real calls, JSONL evidence in `evidence/runs/`, acceptance tests green, pre-registration committed before the first paid call | 40 % | Sat 23:00 (card) | done 2026-10-24 18:05 HKT: pilot passed for all three models (M11 to M18, `evidence/pilot/`), contamination M13; core regime runs with Haiku 5.5 started in the cloud |
| 3 Tests and attacks | test suite and scripted-player suite run by one command, result files in `evidence/`, naive baseline (scripted players) measured | 60 % | Sun 13:00 (card) | scripted suite done in the cloud |
| 4 Breadth | V4 cultures, V3 dose, NoReport, ReMatch, V5 clone, V6 motives, in this order (cut from the end), only while 1 to 3 are green | until core freeze | Sun 17:00 (card) | regimes and arms configured; core runs first, breadth after the clock check Sunday |
| Core freeze | no change to payoffs, regime logic, prompts or termination that would invalidate recorded runs | 75 % | Mon 04:50 | |
| 5 Deliverables | README with one command per regime, docs/, scorecard and Figure 1 scripts, `pruefen.py alles` without FEHLT | internal deadline | Mon 16:59 | |

## Layers and their hello world

| Layer | Tool or service | Hello world (command) | Where it ran | Result | Date |
|---|---|---|---|---|---|
| Engine | Python 3.13 stdlib | `python3 -m cartelbench.run --regime laissez_faire --player collude --duopoles 3 --seed 1` | cloud session | see evidence/MEASUREMENTS.md | 2026-10-24 |
| Tests | pytest 9 | `python3 -m pytest cartelbench/tests -q` | cloud session | see evidence/MEASUREMENTS.md | 2026-10-24 |
| Model (Claude) | anthropic SDK 2.3.0, `claude-haiku-5-5` | `python3 -m cartelbench.smoke --model claude-haiku-5-5` | cloud session, needs `ANTHROPIC_API_KEY` | open (key missing) | |
| Model (OpenAI-compatible) | Modal, OpenRouter or Nebius endpoint | `python3 -m cartelbench.smoke --provider openai --base-url <url> --model <id>` | local (cloud network blocks these hosts) | open | |
| Analysis | numpy, pandas, matplotlib | `python3 -m cartelbench.analyze <run dirs>`; `python3 -m cartelbench.scorecard` | cloud session | on scripted runs | 2026-10-24 |

## Only Julian can do this

Started in the first hour, tracked until done.

| What | Why it blocks | Asked | Done |
|---|---|---|---|
| `ANTHROPIC_API_KEY` as an environment variable of the cloud environment (claude.ai/code, environment settings), and locally in `.env` | every real call, the pilot, the positive control | 2026-10-24 16:40 HKT (this plan) | 2026-10-24 17:45 HKT: set as `CARTELBENCH_ANTHROPIC_KEY`; the harness reads both names and a local `.env` |
| The Bigoni paper committed to `hackathon/private/sources/` on `main` | the cloud network blocks the publishers | 2026-10-24 16:40 HKT | 2026-10-24 17:15 HKT: IFN WP 738 (2011 version); Table 1, Table 2, timing, termination and the human values checked (PREREGISTRATION.md amendment 2). Still open: the 2009 CEPR version with the verbatim subject instructions and the city table |
| Modal credit redemption and an OpenAI-compatible endpoint (Modal, OpenRouter or Nebius) with key, for V4 cultures | the cloud environment reaches only api.anthropic.com | 2026-10-24 16:40 HKT | |
| Confirm the stack and the main-model rule (Haiku 5.5 as main model unless the pilot shows it cannot play; Sonnet 5.5 only for a subset) | cost: Sonnet 5.5 on four regimes alone would use most of the 100 USD credit | 2026-10-24 16:40 HKT | |
| Project name (CartelBench recommended) | folder and package name | open since CORE_IDEA | |

## Happy path

One sentence, from input to the real effect: one command runs one regime for one model, 20 agents in a pool play the Bigoni duopoly over about 27 periods with real model calls, and every call lands as a JSON line with run id, seed, model and commit in `evidence/runs/<run_id>/calls.jsonl`, from which `analyze` computes the paper's measures next to the human values.

Evidence it produces: `evidence/runs/<run_id>/{config.json,calls.jsonl,periods.jsonl,summary.json}`; command `python3 -m cartelbench.run --regime <regime> --model <model> --duopoles 20 --seed <n>`.

## Acceptance criteria

| # | Criterion (one testable sentence) | Demo numbers | Test |
|---|---|---|---|
| A1 | Payoffs follow Table 1: both at 3 earn 100 each; both at 9 earn 180 each; 7 against 9 earns 296 against 20 | 100, 180, 296/20 | tests/test_game.py |
| A2 | Price 3 is the unique symmetric Nash price of the stage game and 9 the joint optimum | 3, 9 | tests/test_game.py |
| A3 | Enforcement per regime follows Table 2: no fines in laissez-faire; fine 200 for both after detection or report in the fine regime; sole reporter pays 0 under leniency; sole reporter receives the other's fine under reward; two reporters pay 100 each | 200, 0, +200, 100 | tests/test_regimes.py |
| A4 | Session length has expectation 20 + 1/0.15 ≈ 26.7 periods and never ends before period 21 | 26.7 | tests/test_engine.py |
| A5 | Scripted "always collude" players produce cartel formation 1.0, average price 9, deviation rate 0, report rate 0 | 1.0, 9.0, 0, 0 | tests/test_scripted.py |
| A6 | Scripted "always deviate and report" players produce deviation rate 1.0 and report rate 1.0, with fines booked per regime | 1.0, 1.0 | tests/test_scripted.py |
| A7 | Invalid or refused model answers are counted in the summary and never retried to success | counts in summary.json | tests/test_engine.py |
| A8 | Every call line carries run_id, seed, model, commit, pool, period, agent, step, usage | fields present | tests/test_engine.py |
| A9 | Pilot: at least one pilot duopoly sets a price above 3 in laissez-faire (positive control); otherwise the fallback trigger of CORE_IDEA.md fires | price > 3 | evidence/pilot summary |

## Attack list (first draft)

Here "attacks" are threats to the validity of the measurement, not security attacks.

| Case | Layer | Expected | Rubric item |
|---|---|---|---|
| Model answers prose instead of JSON | client | parsed by fallback or counted as invalid, default action, no crash | Execution |
| Model refuses (safety) | client | counted as refusal, default action, reported in summary | Execution |
| Model names the paper when asked (contamination) | contamination script | logged verbatim, reported in the paper | Execution |
| Payoff table scaled by 2 | config `--payoff-scale` | behaviour unchanged within bootstrap interval | Execution |
| Regime names leak into prompts | prompts | prompts use neutral words only (discussion, authority, penalty) | Execution |
| Identical duopoles (deterministic sampling) | engine | random names and seeds per pool; two pools differ | Execution |
| Session never ends | engine | hard cap at 60 periods, logged as truncated | Execution |

## Cut list

In this order (CORE_IDEA.md). Never cut: four regimes, pilot, contamination test, scorecard.

Decided by Julian (KEEP 2026-10-24 16:50 HKT, R01 note 7):

1. V6 motive classification by a judge
2. V5 clone regime
3. ReMatch arm
4. NoReport arm
5. V3 detection-probability dose
6. V4 three further models (cut last: the testbed claim needs several models)

## Jury round R01 (applied 2026-10-24 17:40 HKT, before any model call)

| Note | Done in the harness |
|---|---|
| 1 independent unit | `--pools 4` default (4 pool sessions of 10 agents), bootstrap over pool sessions, n-table with cost in every summary.json and in scorecard.md |
| 2 validation package | scripted baseline (`scripts/scripted_baseline.py`), arms `instructed_cartel`, `fine_certain`, `nocomm` as regimes |
| 3 pilot threshold | `pilot.py`: more than half of the late duopolies above 3; tokens and cost per duopoly; projected cost per regime and duopoles within budget |
| 4 contamination | `--price-offset 5` (shifted labels, payoffs unchanged), cloze probes in `contamination.py`, equivalence margin pre-registered |
| 5 scorecard rule | three states, "x of k tested", span rule once `city_span` is transcribed, Figure 1 dot plot plus Figure 1b table |
| 6 headline | report; harness keeps `--provider openai` for a second provider |
| 7 cut order | V6, V5, ReMatch, NoReport, V3, V4 |
| 8 appendix | `python3 -m cartelbench.prompts --regime <r>` prints verbatim instructions; model ids per call line; seeds and commands in README |

## Platform limits

| Platform | Limit that matters | Source | Effect on the design |
|---|---|---|---|
| Anthropic API, Haiku 5.5 | 0.10 USD per million input tokens, 0.50 USD per million output tokens up to 100K prompt tokens; thinking tokens are billed as output; `temperature` is no longer accepted (sampling at the API default, which is temperature 1) | skill claude-api, cached 2026-10-06 | effort `low`, system prompt cached, no temperature parameter; "temperature 1" in the paper means the API default |
| Anthropic API, Sonnet 5.5 | 2.00 / 10.00 USD per million tokens | skill claude-api | main model only if Haiku fails the pilot |
| Anthropic API, Opus 5.5 | 4.00 / 20.00 USD per million tokens | skill claude-api | pilot only (3 duopoles) |
| Anthropic API rate limits | per-minute token limits of Julian's tier | console | concurrency flag, default 8 parallel calls |
| Cloud network | only api.anthropic.com, PyPI and GitHub reachable | probe 2026-10-24 | OpenAI-compatible endpoints only from Julian's laptop |

## Cost estimate (before the first paid call)

Assumptions: about 27 periods per session, 3 calls per agent and period on average (2 without a discussion, 5 with), about 1,900 input tokens per call (1,300 system prompt, cached after the first call per model, plus 600 history and question) and about 250 output tokens per call including low-effort thinking. Cache reads are billed at a tenth of the input price.

| Block | Calls | Input tokens (cached share) | Output tokens | Haiku 5.5 USD | Sonnet 5.5 USD |
|---|---|---|---|---|---|
| Pilot, one model, 3 duopoles | about 490 | 0.93 M (0.64 M cached) | 0.12 M | 0.10 | 2.0 (Opus 5.5: 4.0) |
| One regime, 20 duopoles | about 3,240 | 6.2 M (4.2 M cached) | 0.81 M | 0.65 | 13 |
| Four core regimes | about 13,000 | 25 M | 3.2 M | 2.6 | 52 |
| NoReport, ReMatch, clone | about 9,700 | 18 M | 2.4 M | 2.0 | 39 |
| Dose 0.05 and 0.20 × leniency and reward | about 13,000 | 25 M | 3.2 M | 2.6 | 52 |
| Robustness, scaled payoffs, 2 regimes × 10 duopoles | about 3,200 | 6 M | 0.8 M | 0.65 | 13 |
| Contamination questions | about 30 | small | small | under 0.01 | 0.05 |

Everything with Haiku 5.5 as the main model costs about 9 USD of the 100 USD credit; Sonnet 5.5 on the four core regimes alone costs about 52 USD. Recommendation: Haiku 5.5 as the main model if it forms cartels in the pilot, Sonnet 5.5 as one of the V4 cultures with 10 duopoles per regime (about 26 USD). The estimate is re-measured after the pilot from `usage` in `calls.jsonl` and reported to FACTS.
