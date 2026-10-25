# Narration for the CartelBench video (optional voice-over)

The video is understandable without sound. This text is for an optional voice track: read it at a calm pace (about 140 words per minute), one block per scene, and start each block at the scene's start time. Times come from `python3 video/build.py --timeline` (scenes overlap by 0.8 s of cross-fade). Every number is in `facts_used.md`.

| Scene | Start | End | Words |
|---|---|---|---|
| 1 Title | 0:00 | 0:15 | 34 |
| 2 The game | 0:14 | 0:34 | 48 |
| 3 Four regimes | 0:33 | 0:57 | 56 |
| 4 The testbed | 0:56 | 1:21 | 57 |
| 5 Finding 1 | 1:20 | 1:43 | 55 |
| 6 Finding 2 | 1:42 | 2:13 | 72 |
| 7 Finding 3 | 2:13 | 2:39 | 60 |
| 8 Scorecard | 2:38 | 2:58 | 46 |
| 9 Limits | 2:57 | 3:19 | 52 |
| 10 Credits | 3:18 | 3:34 | 32 |

## 1 Title (0:00 to 0:15)

Fines, leniency programmes and whistleblower rewards are how competition authorities fight cartels. They were designed for people. This is CartelBench, a testbed that asks one question: do antitrust tools that work on people work on AI pricing agents?

## 2 The game (0:14 to 0:34)

The game comes from a published laboratory experiment. Two firms each set a price between zero and twelve in every period. Three is the competitive price, nine is the cartel price. Before pricing, the two firms may agree to talk about prices. That talk forms a cartel, and a cartel can be fined.

## 3 Four regimes (0:33 to 0:57)

The students in the original experiment played under four rules. No authority at all. A fine of two hundred points per firm when a cartel is detected or reported, with a detection chance of ten percent per period. Leniency, where the firm that reports pays nothing. And reward, where the reporter also collects the other firm's fine.

## 4 The testbed (0:56 to 1:21)

CartelBench replays that experiment with language-model sellers: the same rules, payoffs and instructions, checked cell by cell against the paper. The published student data serve as the baseline for every measure. Hypotheses and decision rules were committed before the first model call. Four models from three families played, over forty-five thousand calls, without a single refusal.

## 5 Finding 1 (1:20 to 1:43)

First finding. Without an authority, the agents form cartels about as often as the students did; cartel incidence is almost identical. But the students undercut their partners more than half the time, so their average price was below five. The agents almost never undercut, and their price stays near nine, the cartel optimum.

## 6 Finding 2 (1:42 to 2:13)

Second finding. Once a fine, leniency or reward rule is told, explicit cartels nearly vanish: Sonnet and Qwen never form one. Yet three of the four models keep prices well above the competitive level, between five and a half and seven, and they do so almost without a word. Sonnet asked to talk in one or two decisions out of five hundred. Only Haiku falls near the competitive price under leniency and reward.

## 7 Finding 3 (2:13 to 2:39)

Third finding. A pre-registered price screen fines both firms when both prices exceed four in two consecutive periods; its false-positive rate is at most one point one percent. The screen lowers prices in every arm without triggering a single penalty. Sonnet moves every price to exactly four. A known threshold becomes the new focal price.

## 8 Scorecard (2:38 to 2:58)

Against the eight numbered results of the human experiment, Claude Haiku reproduces three of seven testable ones under the pre-registered rule: deterrence, detection through reports and lower recidivism under leniency. The results that rest on human undercutting do not reproduce, because the agents do not undercut.

## 9 Limits (2:57 to 3:19)

Three limits. This is a laboratory game, not a market. Punishments are told, not paid; a placebo text without any penalty already removes about half of Haiku's fine effect. And the fine regime is sensitive to wording: with paraphrased instructions, Haiku's cartel incidence under the fine drops from forty percent to two.

## 10 Credits (3:18 to 3:34)

CartelBench: Same Game, Different Players. Code, pre-registration, every model call and the report are on GitHub. Julian Mundelein, Independent, Hong Kong, for the AI Collusion Research Sprint by Apart Research, October 2026.
