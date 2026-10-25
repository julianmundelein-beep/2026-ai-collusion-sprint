# Numbers shown in the video and their FACTS ids

Every number on screen comes from `hackathon/FACTS.md`. Where a machine-readable file exists in `cartelbench/evidence/`, `build.py` reads the value from it; the remaining values are typed in `build.py` with their id. Human values come from `cartelbench/data/human_baseline.json` (F15).

| Scene | On screen | Value | FACTS id | Read from |
|---|---|---|---|---|
| 2 Game | prices 0 to 12, Nash 3, joint optimum 9 | design of the paper | F08 (payoff table, Nash 3, optimum 9) | typed |
| 2 Game | pair stays together with probability 0.85 | 0.85 | F06 (continuation 0.85 per period) | typed |
| 3 Regimes | detection probability 0.10, fine 200 points per firm | 0.10; 200 per firm (400 per detection for the pair) | F05 | typed |
| 4 Testbed | payoff cells match | 169 of 169 | F08 | typed |
| 4 Testbed | model calls, refusals | 45,286 calls, 0 refusals | F40 | typed |
| 4 Testbed | pre-registration before the first model call | commit times | F20 | wording only |
| 4 Testbed | four models, three families | Haiku 5.5, Sonnet 5.5, Qwen2.5-32B, Llama-3.1-8B | F63, F64, F57, F61 | wording only |
| 5 Finding 1 | average price without authority, humans | 4.92 | F15 | human_baseline.json |
| 5 Finding 1 | average price without authority, Haiku | 8.87 | F63 | round4/scorecard_haiku_8pool/scorecard.json |
| 5 Finding 1 | cartel incidence, humans and Haiku | 0.961; 0.962 | F15; F63 | human_baseline.json; scorecard_haiku_8pool |
| 5 Finding 1 | deviation rate, humans and Haiku | 0.564; 0.015 | F15; F13 | typed |
| 6 Finding 2 | human prices per regime | 4.92, 5.35, 4.84, 3.97 | F15 (report Table 2 prints leniency as 4.85 from 4.845; the video prints 4.84 from the data file) | human_baseline.json |
| 6 Finding 2 | Haiku prices per regime | 8.87, 5.52, 3.26, 3.21 | F63 | scorecard_haiku_8pool |
| 6 Finding 2 | Sonnet prices per regime | 8.92, 6.10, 6.24, 5.74 | F64 | round4/scorecard_sonnet_4pool/scorecard.json |
| 6 Finding 2 | Qwen prices per regime | 6.85, 7.27, 7.20, 7.33 | F57 | provider2/scorecard/scorecard.json |
| 6 Finding 2 | Llama prices per regime | 7.31, 6.64, 6.78, 6.40 | F61 | provider2/scorecard_llama-3.1-8b-instruct/scorecard.json |
| 6 Finding 2 | cartel incidence under fine, leniency, reward | Sonnet 0.000, Qwen 0.000, Llama at most 0.086, Haiku 0.401 to 0.007 | F64, F57, F61, F63 | the four scorecard files |
| 6 Finding 2 | Sonnet wishes to talk | 1 to 2 of 460 to 510 decisions | F44 | typed |
| 7 Finding 3 | screen rule: both prices above 4 in two consecutive periods | p = 4, k = 2 | F51 | typed |
| 7 Finding 3 | false-positive rate | at most 1.1 percent (0.0114) | F52 | round4/screen.json |
| 7 Finding 3 | Sonnet no channel, price without and with screen | 7.36 to 4.00 | F53 | round4/screen.json |
| 7 Finding 3 | Haiku no channel | 5.26 to 4.16 (4.155) | F53 | round4/screen.json |
| 7 Finding 3 | Haiku fine regime | 5.52 to 3.23 | F53 | round4/screen.json |
| 7 Finding 3 | zero screen penalties; every Sonnet price exactly at 4 | 0; share at 4 = 1.000 | F53 | round4/screen.md |
| 8 Scorecard | results reproduced | 3 of 7 tested, 8 pool sessions | F46 | scorecard_haiku_8pool (`reproduced`, `tested`); figure paper/figures/figure1_landscape.png |
| 9 Limits | placebo removes about half of Haiku's fine effect | placebo incidence 0.714 between laissez-faire 0.956 and fine 0.439 | F26 | typed |
| 9 Limits | paraphrase cuts Haiku's fine incidence | 0.401 to 0.018 (shown as 0.40 to 0.02) | F50 | typed |
| 10 Credits | title, author, affiliation | KEEP 2026-10-25 02:40 | DECISIONS.md | typed |

Statements without a number (cartels "as often as students", "three of four models keep the price", "almost without a word") follow the abstract and Finding 2 of `paper/report.md`.
