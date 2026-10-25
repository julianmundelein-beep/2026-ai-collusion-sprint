# Narration and shot list for the CartelBench video

Thirteen scenes, one voice file each. Record or generate each block as `video/voice/01.mp3` to `13.mp3` (see README.md). `build.py` reads the Voice column of this file, measures the pauses in each voice file and places every on-screen element at the moment its anchor phrase is spoken (the phrases are quoted in the "On screen" column; `python3 video/build.py --cues` prints the resulting seconds). Each scene lasts its voice file plus 0.8 s. Without voice files the elements follow the same phrases at an assumed 150 words per minute. Times below are the build with the committed voice files (`python3 video/build.py --timeline`). Every number is in `facts_used.md`.

| Scene | Start | Length |
|---|---|---|
| 01 Intro | 0:00 | 11.0 s |
| 02 Title | 0:10 | 21.5 s |
| 03 The game | 0:31 | 20.0 s |
| 04 The human experiment | 0:50 | 23.0 s |
| 05 The testbed | 1:12 | 26.0 s |
| 06 Findings 1 and 2 | 1:37 | 31.0 s |
| 07 The central finding | 2:08 | 36.0 s |
| 08 An honest negative | 2:43 | 19.0 s |
| 09 Told or paid | 3:01 | 22.5 s |
| 10 Application | 3:23 | 23.0 s |
| 11 Scorecard | 3:45 | 25.5 s |
| 12 Limits | 4:10 | 20.0 s |
| 13 Close | 4:29 | 24.0 s |

Pronunciation for a voice tool: "Bigoni" as bee-GO-nee, "Qwen" as kwen, "Llama" as lah-ma, "Haiku" as HY-koo, "Nash" as in cash.

## 01 Intro

| Voice | On screen |
|---|---|
| When two companies quietly agree on a price instead of competing, customers pay more. That is a cartel, and it is illegal almost everywhere. | Two firm boxes appear with "When two companies" and slide together at "agree on a price", joined by a line "one price"; the second sentence appears at "That is a cartel". |

## 02 Title

| Voice | On screen |
|---|---|
| Competition authorities fight cartels with three tools: fines, leniency for the member who confesses, and rewards for whistleblowers. All three were designed for people. Today, more and more prices are set by software, and language-model agents are starting to set them too. Do the three tools work on them? | Title card from the start. The chips Fines, Leniency, Rewards appear at those words; "designed for people" with "All three were designed"; the sentence on software with "Today, more and more"; the question with "Do the three tools". |

## 03 The game

| Voice | On screen |
|---|---|
| The game comes from a published laboratory experiment. Two firms each set a price from zero to twelve in every period. Three is the competitive price. Nine is the cartel price. Before pricing, the firms may agree to talk, and that talk forms a cartel. | Firm boxes at "Two firms"; the price line 0 to 12 at "zero to twelve"; the marker at 3 with a pulse at "Three is"; the marker at 9 at "Nine is"; the note on talking at "Before pricing"; the payoff sentence at "forms a cartel". |

## 04 The human experiment

| Voice | On screen |
|---|---|
| Bigoni and colleagues ran this game with students under four rules: no authority; a fine of two hundred points per firm; leniency, where the firm that reports pays nothing; and a reward, where the reporter also collects the other firm's fine. Only the reward pushed the students' prices toward the competitive level. | The four cards appear at "no authority", "a fine of two hundred", "leniency, where" and "and a reward"; the students' average prices appear under the cards at "Only the reward" (reward value in the accent colour); the closing line at "pushed the students". |

## 05 The testbed

| Voice | On screen |
|---|---|
| CartelBench replays that experiment with language-model sellers: the same rules, payoffs and instructions, checked cell by cell. The published student data are the baseline for every measure. Decision rules were committed before the first model call. Four models from three families played, forty-five thousand calls, not a single refusal. | Bullets appear at "the same rules", "The published student data", "Decision rules", "Four models" and "forty-five thousand"; the call count counts up with the last one. |

## 06 Findings 1 and 2

| Voice | On screen |
|---|---|
| Without an authority, the agents form cartels about as often as the students did. But the students undercut their partners more than half the time, and the agents almost never do, so their price stays near nine. Once a fine, leniency or reward is told, explicit cartels nearly vanish. Yet three of the four models keep prices well above the competitive level, almost without a word. Only Haiku falls near the competitive price. | Table header from the start; the human and Haiku rows at "Without an authority"; the no-authority column highlighted with the first caption at "But the students undercut"; Sonnet, Qwen and Llama rows at "Once a fine"; the shaded prices under the told rules and the second caption at "Yet three of the four". |

## 07 The central finding

| Voice | On screen |
|---|---|
| So I tested an announced price screen: a fine whenever both prices exceed a threshold in two consecutive periods. My central finding: Sonnet's average price follows the threshold almost one to one, slope zero point nine eight, with at least ninety-three percent of prices exactly on the line. Haiku and Qwen follow more loosely, their most frequent price always the threshold. Llama does not. And at a threshold of three, the competitive price, every single Sonnet price is three. I read this as optimisation against the rule. | Rule sentence at "So I tested"; axes and the dashed line at "a fine whenever". Sonnet points with a pulse at "Sonnet's average price", "follows the threshold", "almost one to one" and "slope zero point"; the Sonnet note at "with at least ninety-three". Haiku line at "Haiku and Qwen", Qwen line 0.8 s later, their note at "their most frequent"; Llama line and note at "Llama does not". The notes fade, the point at 3 pulses and the pointe appears at "And at a threshold of three"; the reading at "I read this". |

## 08 An honest negative

| Voice | On screen |
|---|---|
| Does hiding the threshold help? I drew it at random from three to six each period and never disclosed it. The bunching on four dissolves. But the prices do not fall by a detectable amount: Haiku, Sonnet and Qwen stay within noise, and Llama's price even rose. | Intro line at "I drew it at random"; the bars of the share of prices at 4 at "The bunching" (announced, then random; Haiku, then Sonnet); the price table at "But the prices"; the conclusion at "stay within noise". |

## 09 Told or paid

| Voice | On screen |
|---|---|
| The instruments are told, not paid. So I framed the points as money, as a loss from own capital, and as a risk of bankruptcy. Haiku's cartel incidence under the fine fell, but only within the range that a mere rewording produces, with no loss-aversion effect. A Llama retrained on its own best moves after fines moved only slightly. | Chips at "as money", "as a loss" and "risk of bankruptcy"; the Haiku incidence row at "Haiku's cartel incidence"; no loss aversion at "with no loss-aversion"; the Llama row at "A Llama retrained". |

## 10 Application

| Voice | On screen |
|---|---|
| For an authority, all of this condenses into a Cartel Risk Card per model, recomputed from the recorded runs. Here is Sonnet's: cartels whenever it can talk, none once a rule is told, a silent price of seven point four, every price exactly on an announced threshold, a quarter dollar per duopoly. | Intro line at "Cartel Risk Card"; the card frame and title at "Here is Sonnet's"; rows at "cartels whenever" (laissez-faire), "none once a rule" (fine, reward), "a silent price" (no channel, Nash partner), "every price exactly" (threshold shares, instructed) and "a quarter dollar" (cost). |

## 11 Scorecard

| Voice | On screen |
|---|---|
| Against the eight numbered results of the human experiment, Haiku reproduces three of the seven testable ones under the pre-registered rule: deterrence, detection through reports, and lower recidivism under leniency. The results that rest on human undercutting do not reproduce. One caveat: result three passes the bootstrap rule but not the permutation test. | Rule line at "Against the eight"; the green tiles at "deterrence", "detection through reports" and "lower recidivism"; the red and grey tiles at "The results that rest"; the caveat at "One caveat". |

## 12 Limits

| Voice | On screen |
|---|---|
| Four limits. This is a laboratory game, not a market. The agents play for points, not money. Haiku's response to the fine is not robust to a rewording of the instructions. And the price screen has no human baseline: the threshold curve was never run with people. | Bullets at "This is a laboratory", "The agents play for points", "Haiku's response" and "And the price screen". |

## 13 Close

| Voice | On screen |
|---|---|
| A price screen reaches the silent coordination, but the agents price on its published line, and hiding the line alone does not lower prices. An authority has to choose where the line lies, not only whether to publish it. My code, every model call, the whole documentation and the report are on GitHub. Thank you for watching. | The conclusion in the accent colour at "An authority has to choose"; title, author, sprint and the repository address at "My code"; "Thank you for watching." at "Thank you". |
