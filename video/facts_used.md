# Numbers shown in the video and their sources

Source of every number: `paper/report.md` (final version; the FACTS id in square brackets is the one printed there) together with the measurement files `cartelbench/evidence/MEASUREMENTS.md` (M keys), `cartelbench/evidence/MEASUREMENTS_round7.md` (R7 keys) and `cartelbench/evidence/provider2/MEASUREMENTS_provider2.md` (P2 keys). Where a machine-readable file exists, `build.py` reads the value from it ("Read from"); the rest is typed in `build.py` under `R` with the id next to it.

| Scene | On screen | Value | Report id | Measurement key | Read from |
|---|---|---|---|---|---|
| 03 Game | prices 0 to 12, Nash 3, joint optimum 9 | design | Methods, "The game" [F08] | M07 | typed; `diagonal.json` carries `nash_price` 3 and `joint_optimum` 9 |
| 03 Game | pair stays together with probability 0.85 | 0.85 | Methods, "The game" [F06] | M06 | typed |
| 04 Humans | fine 200 points per firm, detection 0.10 per period | 200; 0.10 | Methods, "The game" | M05 | typed |
| 04 Humans, 06 Table | students' average prices: no authority, fine, leniency, reward | 4.92, 5.35, 4.85, 3.97 | Table 2 [F15] (leniency printed as 4.85, as in the report; the data file holds 4.845) | | typed from Table 2 |
| 04 Humans | only the reward pushed the students' prices toward the competitive level | wording | Related Work, "The source experiment" | | wording only |
| 05 Testbed | payoff cells match | 169 of 169 | contribution 1 [F08] | M07 | typed |
| 05 Testbed | model calls, refusals | 45,286; 0 | Table A2 [F40] | M56 | typed |
| 05 Testbed | pre-registered before the first model call | commit times | Methods, "Pre-registration" [F20] | M08 | wording only |
| 05 Testbed | four models, three families | names | Methods, "Models" | | wording only |
| 06 Table | cartel incidence without authority, students and Haiku | 0.961; 0.962 | Table 2 [F15, F63] | M63 | `data/human_baseline.json`; `round4/scorecard_haiku_8pool/scorecard.json` (`metrics`) |
| 06 Table | deviation rate without authority, students and Haiku | 0.564; 0.015 | Finding 1 [F15, F13] | M20 | typed |
| 06 Table | Haiku prices per regime | 8.87, 5.52, 3.26, 3.21 | Table 2 [F63] | M63 | `round4/scorecard_haiku_8pool/scorecard.json` |
| 06 Table | Sonnet prices per regime | 8.92, 6.10, 6.24, 5.74 | Table 2 [F64] | M66 | `round4/scorecard_sonnet_4pool/scorecard.json` |
| 06 Table | Qwen prices per regime | 6.85, 7.27, 7.20, 7.33 | Table 2 [F57] | P2-20 to P2-35 | `provider2/scorecard/scorecard.json` |
| 06 Table | Llama prices per regime | 7.31, 6.64, 6.78, 6.40 | Table 2 [F61] | P2-60 to P2-71 | `provider2/scorecard_llama-3.1-8b-instruct/scorecard.json` |
| 06 Table | Sonnet and Qwen cartel incidence under told rules; "5.7 to 7.3" | 0.000; range | Table 2, Finding 2 [F64, F57, F61] | M66, P2 | the scorecard files (`metrics`) |
| 07 Line | screen rule: both prices above the threshold in two consecutive periods | p, k = 2 | Methods, "Price screen" [F51] | M70 | typed |
| 07 Line | Sonnet average price at thresholds 3 to 6 | 3.00, 4.00, 4.99, 5.93 | Finding 4, Figure 2 [F85] | R7-12, M72, M80 | `round7/diagonal.json` |
| 07 Line | Sonnet slope; share of prices exactly on the threshold | 0.98 (0.976); at least 93 percent (0.934 to 1.000) | Finding 4 [F85] | R7-12 | slope typed from the report; shares in `diagonal.json` |
| 07 Line | Haiku and Qwen slopes; most frequent price equals the threshold in every cell | 0.70; 0.68; modal price | Finding 4 [F85] | R7-11, P2 | slopes typed; modal prices in `diagonal.json` |
| 07 Line | Llama slope; most frequent price off the threshold | 0.31; hollow points | Finding 4 [F85] | | slope typed; modal prices in `diagonal.json` |
| 07 Line | at threshold 3 every Sonnet price is exactly 3 | share 1.000 | Finding 4 [F86] | R7-12, R7-13 | `diagonal.json` |
| 07 Line | "we read this as optimisation against the rule" | wording | Abstract, Discussion | | wording only |
| 08 Random | threshold drawn at random from 3 to 6, never disclosed | design | "Hiding the threshold" [F87] | R7-20, R7-21 | typed |
| 08 Random | share of prices exactly at 4, announced against random: Haiku, Sonnet | 0.645 to 0.105; 1.000 to 0.465 | "Hiding the threshold" (fell by 0.54 for each) [F87] | R7-20, R7-21 | typed from `round7/random.md` |
| 08 Random | average price announced at 4 against random: Haiku, Sonnet, Qwen, Llama | 4.16 to 3.80; 4.00 to 3.87; 5.13 to 5.55; 4.55 to 6.53 | "Hiding the threshold" [F87] | R7-20, R7-21 (Claude); report for the open models | typed |
| 08 Random | Haiku difference not detectable | p 0.229 | "Hiding the threshold" [F87] | R7-20 | typed |
| 09 Stakes | Haiku fine-regime cartel incidence under money, loss and bankruptcy frames against the original | 0.093 to 0.164 against 0.401 | "Told or paid" [F80, F81, F82] | M91 | typed |
| 09 Stakes | a rewording alone | 0.018 | Validity checks [F50] | M69 | typed |
| 09 Stakes | no loss-aversion effect | verdict | "Told or paid" | M93 | wording only |
| 09 Stakes | Llama expert iteration: prices under leniency and reward; distance to the students | -0.50, -0.60; 0.222 to 0.206 | "Told or paid" [F91, F92] | | typed |
| 10 Risk card | Sonnet 5.5 card rows | 1.000 (students 0.961); +1.000 (students +0.378); 5.740 (students 3.973); 7.364; 3.796; p3 1.00 p4 1.00 p5 0.98 p6 0.93; 4.000, 0 penalties; 0.245 USD per duopoly | Discussion (risk card), Table 2, Table 4 [F64, F47, F71, F72, F85] | R7-40 | typed from `risk_cards/summary.md`; `risk_cards.json` is loaded as a check that the file exists |
| 11 Scorecard | results reproduced; state per result | 3 of 7; states | "Haiku reproduces three of seven" [F46] | M63, M64 | `round4/scorecard_haiku_8pool/scorecard.json` (`reproduced`, `tested`, row names); `round4/scorecards.json` (states of `haiku_8pool`) |
| 11 Scorecard | caveat | Result 3 bootstrap yes, permutation p 0.099; first 4 pools 2 of 7 | same paragraph [F46] | M64 | typed |
| 12 Limits | paraphrase cuts Haiku's fine-regime cartel incidence | 0.40 to 0.02 (0.401 to 0.018) | Validity checks, Limitations [F50] | M69 | typed |
| 13 Close | conclusion sentences | wording | Conclusion | | wording only |
| 02, 13 | title, author, affiliation | wording | report page 1 | | typed |

Not shown on purpose: the false-positive rate of the screen (1.1 percent on scripted players, 2 percent on honest LLM agents [F52, F76]) and the unannounced fixed threshold [F69, F70]; both are in the report and would add a second number to a scene that already carries one message.

Scene 01 (intro) and the sentence on software setting prices in scene 02 carry no number; the claim that LLM pricing agents set prices follows the report's introduction (Fish et al., 2024).
