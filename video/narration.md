# Narration and shot list for the CartelBench video

Twelve scenes, one voice file each. Record or generate each block as `video/voice/01.mp3` to `12.mp3` (see README.md); `build.py` then lengthens a scene to its file plus 1.2 s and lays the files under the video at the scene starts. The "On screen" column says what appears while the sentence is spoken; the seconds in brackets are the moments inside the scene at which elements appear, so that the voice can follow them. Times below are the silent build (`python3 video/build.py --timeline`); with voice files the starts shift by the extra seconds. Pace: about 150 words per minute; each block fits its scene with 2 to 4 s to spare. Every number is in `facts_used.md`.

| Scene | Start (silent build) | Length | Words |
|---|---|---|---|
| 01 Title | 0:00 | 15.0 s | 31 |
| 02 The game | 0:14 | 18.0 s | 45 |
| 03 The human experiment | 0:31 | 22.5 s | 52 |
| 04 The testbed | 0:53 | 23.5 s | 49 |
| 05 Findings 1 and 2 | 1:16 | 30.5 s | 73 |
| 06 The central finding | 1:46 | 35.5 s | 86 |
| 07 An honest negative | 2:20 | 21.0 s | 47 |
| 08 Told or paid | 2:40 | 26.0 s | 65 |
| 09 Application | 3:06 | 22.5 s | 53 |
| 10 Scorecard | 3:27 | 24.0 s | 53 |
| 11 Limits | 3:51 | 24.5 s | 47 |
| 12 Close | 4:14 | 22.5 s | 50 |

Pronunciation for a voice tool: "Bigoni" as bee-GO-nee, "Qwen" as kwen, "Llama" as lah-ma, "Haiku" as HY-koo, "Nash" as in cash.

## 01 Title (0:00, 15.0 s)

| Voice | On screen |
|---|---|
| Competition authorities fight cartels with three tools: fines, leniency for the member who confesses, and rewards for whistleblowers. All three were designed for people. Do they work on AI pricing agents? | Title card. The three words appear one by one (3.0 s, 3.7 s, 4.4 s), then "designed for people" (5.6 s), then the question (8.0 s). |

## 02 The game (0:14, 18.0 s)

| Voice | On screen |
|---|---|
| The game comes from a published laboratory experiment. Two firms each set a price from zero to twelve in every period. Three is the competitive price. Nine is the cartel price. Before pricing, the firms may agree to talk, and that talk forms a cartel. | Two firm boxes (0.8 s), the note on talking (2.0 s), the price line 0 to 12 (3.2 s), the marker at 3 with a pulse (4.6 s), the marker at 9 (6.2 s), the payoff sentence (8.0 s). |

## 03 The human experiment (0:31, 22.5 s)

| Voice | On screen |
|---|---|
| Bigoni and colleagues ran this game with students under four rules: no authority; a fine of two hundred points per firm; leniency, where the firm that reports pays nothing; and a reward, where the reporter also collects the other firm's fine. Only the reward pushed the students' prices toward the competitive level. | Four cards appear left to right (1.4 s, 2.7 s, 4.0 s, 5.3 s); the students' average prices appear under the cards (7.6 s to 9.1 s), the reward value in the accent colour; the closing sentence (10.5 s). |

## 04 The testbed (0:53, 23.5 s)

| Voice | On screen |
|---|---|
| CartelBench replays that experiment with language-model sellers: the same rules, payoffs and instructions, checked cell by cell. The published student data are the baseline for every measure. Decision rules were committed before the first model call. Four models from three families played, forty-five thousand calls, not a single refusal. | Five bullets appear one after another (1.2 s, 2.9 s, 4.6 s, 6.3 s, 8.0 s); the call count counts up to 45,286 with the last bullet. |

## 05 Findings 1 and 2 (1:16, 30.5 s)

| Voice | On screen |
|---|---|
| Without an authority, the agents form cartels about as often as the students did. But the students undercut their partners more than half the time, and the agents almost never do, so their price stays near nine. Once a fine, leniency or reward is told, explicit cartels nearly vanish. Yet three of the four models keep prices well above the competitive level, almost without a word. Only Haiku falls near the competitive price. | Table header (1.0 s), human row (1.6 s), Haiku row (3.0 s); the no-authority column is highlighted with the first caption (5.0 s). Sonnet, Qwen and Llama rows appear (11.0 s, 13.0 s, 15.0 s); the shaded prices under the three told rules light up with the second caption (17.5 s). |

## 06 The central finding (1:46, 35.5 s)

| Voice | On screen |
|---|---|
| So we tested an announced price screen: a fine whenever both prices exceed a threshold in two consecutive periods. Our central finding: Sonnet's average price follows the threshold almost one to one, slope zero point nine eight, with at least ninety-three percent of prices exactly on the line. Haiku and Qwen follow more loosely, their most frequent price always the threshold. Llama does not. And at a threshold of three, the competitive price, every single Sonnet price is three. We read this as optimisation against the rule. | Rule sentence (1.0 s), axes and the dashed line price = threshold (3.0 s). Sonnet points appear one by one with a pulse: 3.00 (4.5 s), 4.00 (5.7 s), 4.99 (6.9 s), 5.93 (8.1 s); the Sonnet note (9.5 s). Haiku line (13.0 s), Qwen line (15.0 s), the note on both (14.0 s). Llama line with hollow points (18.0 s), its note (19.0 s). The three notes fade, the point at 3 pulses and the pointe appears (22.5 s); the reading sentence (26.5 s). |

## 07 An honest negative (2:20, 21.0 s)

| Voice | On screen |
|---|---|
| Does hiding the threshold help? We drew it at random from three to six each period and never disclosed it. The bunching on four dissolves. But the prices do not fall by a detectable amount: Haiku, Sonnet and Qwen stay within noise, and Llama's price even rose. | Intro line (0.8 s). Left: bars of the share of prices at 4, announced then random, Haiku (2.0 s and 3.5 s) and Sonnet (2.6 s and 4.1 s). Right: price table, four rows (8.6 s to 10.7 s); the conclusion line (12.0 s). |

## 08 Told or paid (2:40, 26.0 s)

| Voice | On screen |
|---|---|
| The instruments are told, not paid. So we framed the points as money, as a loss from the firm's own capital, and as a risk of bankruptcy. Haiku's cartel incidence under the fine fell, but only within the range that a mere rewording of the instructions produces, and with no loss-aversion effect. A Llama retrained on its own best moves after fines moved only slightly. | Three frame chips (1.2 s, 1.8 s, 2.4 s); the Haiku incidence row (3.6 s); no loss aversion (7.0 s); the Llama row (10.0 s). |

## 09 Application (3:06, 22.5 s)

| Voice | On screen |
|---|---|
| For an authority, all of this condenses into a Cartel Risk Card per model, recomputed from the recorded runs. Here is Sonnet's: cartels whenever it can talk, none once a rule is told, a silent price of seven point four, every price exactly on an announced threshold, a quarter dollar per duopoly. | Intro line (0.8 s), the card frame and title (1.4 s), eight rows appear one after another (2.4 s to 7.7 s). |

## 10 Scorecard (3:27, 24.0 s)

| Voice | On screen |
|---|---|
| Against the eight numbered results of the human experiment, Haiku reproduces three of the seven testable ones under the pre-registered rule: deterrence, detection through reports, and lower recidivism under leniency. The results that rest on human undercutting do not reproduce. One caveat: result three passes the bootstrap rule but not the permutation test. | Rule line (0.8 s); eight tiles appear in reading order (2.0 s to 6.9 s), green, red, grey; the caveat line (9.0 s). |

## 11 Limits (3:51, 24.5 s)

| Voice | On screen |
|---|---|
| Four limits. This is a laboratory game, not a market. The agents play for points, not money. Haiku's response to the fine is not robust to a rewording of the instructions. And the price screen has no human baseline: the threshold curve was never run with people. | Four bullets appear one after another (1.2 s, 3.6 s, 6.0 s, 8.4 s). |

## 12 Close (4:14, 22.5 s)

| Voice | On screen |
|---|---|
| A price screen reaches the silent coordination, but the agents price on its published line, and hiding the line alone does not lower prices. An authority has to choose where the line lies, not only whether to publish it. Code, pre-registration, every model call and the report are on GitHub. | First sentence (0.3 s), the conclusion in the accent colour (3.0 s), then title, author and sprint (5.4 s to 6.8 s) and the repository address (7.4 s). |
