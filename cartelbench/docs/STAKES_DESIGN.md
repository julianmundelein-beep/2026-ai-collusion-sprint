# Stakes design (round 6): how close can an LLM seller come to the students' losses?

Working note of the backend for round 6 ("loss and stakes"), pre-registration amendment 7 (stage 1, API) and amendment 8 (stage 2, open model that learns from its own games; registered only when it can run). Numbers from this repository carry their measurement key; sources outside the repository are listed at the end with how far they were checked.

## 1. What the students had at stake

From Bigoni, Fridolfsson, Le Coq and Spagnolo, IFN Working Paper 738 (version of 2 November 2011, revised for the RAND Journal of Economics 2012), Section 3.6 "Experimental procedure", printed page 11 (PDF page 12), read with pypdf from the copy in commit ae06048 (`hackathon/private/sources/`):

- "At the end of each session, the subjects were paid privately in cash."
- "The subjects started with an initial endowment of 1000 points in order to reduce the likelihood of bankruptcy, an event that never occurred."
- "At the end of the experiment the subjects were paid an amount equal to their cumulated earnings (including the initial endowment) plus a show-up fee of 7 Euros (50 Swedish kronor in Stockholm). The conversion rate was 200 points for 1 Euro (10 Swedish kronor in Stockholm)." Footnote 12: 1 SEK was 0.109 euros at the time.
- Average payment: Stockholm 26.14 euros (minimum 12.54, maximum 42.51), Rome 24.22 euros (minimum 16.5, maximum 31.5); sessions lasted about two hours including instructions and payment, after five trial periods.

What this means in the game: a fine of 200 points was 1 euro of a student's own cash payment; a period of a cartel at 9 (180 points) was 0.90 euros; the endowment was paid out at the end, so a fine was taken out of money the student already counted as theirs (cumulated earnings including the endowment). Losses below the endowment were possible in principle; the paper does not say what bankruptcy would have meant, only that it never happened. The show-up fee was paid regardless and cannot be lost.

What the LLM sellers had until now (amendments 1 to 6): the same 1000-point endowment and the same points in the instructions ("You start with 1000 points"), penalties deducted from the points in the history table, and nothing else. No money, no consequence beyond the number in the context, no learning across sessions. The report calls this "told, not paid".

Two results of this project already show that the told rule's wording, not only its size, drives the agents: the placebo arm (the fine regime's text with a penalty of 0 points) removes about half of Haiku 5.5's deterrence (M33), and an independent paraphrase of the instructions moves Haiku's fine regime from cartel incidence 0.401 to 0.018 and the average price from 5.52 to 3.48 (F50, M69), while laissez-faire, leniency and reward stay within the equivalence margins. Any effect of a stakes arm in the fine regime has to be read against this wording sensitivity.

## 2. How behavioural economics isolates loss aversion

The manipulations that measure loss aversion without changing incentives keep every payoff identical and change only the reference point:

1. Gain against loss framing of identical outcomes. Tversky and Kahneman (1981) present the same outcomes as lives saved or lives lost and find preference reversals; prospect theory (Kahneman and Tversky 1979) explains them with a value function that is steeper for losses than for gains relative to a reference point. Andreoni (1995) does the same in a public-goods game: the identical game framed as giving to the group or as taking from it, with more cooperation in the positive frame. This is the structure of a fine: the same 200 points can be presented as taken from what the firm holds or as a bonus it does not get.
2. Advance payment with claw-back against payment at the end. Hossain and List (2012) pay factory workers the same bonus either framed as a gain ("you will receive a bonus if ...") or as a loss ("you have been provisionally given a bonus, which will be taken back if ..."), and productivity is higher in the loss frame. Fryer, Levitt, List and Sadoff (2012) pay teachers in advance and claw back the payment if targets are missed, against paying at the end, and find larger effects of the advance payment. This is the design of arm S2 here: the endowment in hand (loss frame) against a bonus paid at the end (gain frame), same totals.
3. Endowments that can be lost. The endowment effect (Kahneman, Knetsch and Thaler 1990) shows that owning a good raises the price at which it is given up; laboratory endowments are the standard way to make losses possible. Thaler and Johnson (1990) caution that money handed out by the experimenter is partly treated as "house money" and lost more easily than own money. Bigoni et al. use the endowment for bankruptcy protection, not as a framing device; the students still lost their own cash payment with every fine.
4. Loss avoidance in strategic games. Cachon and Camerer (1996), cited by Bigoni et al., show that subjects in coordination games avoid strategies that guarantee a loss once a participation fee makes losses possible. A strategy that risks the endowment is avoided more than its expected value suggests.

What none of these designs can do for an LLM: make the money real. An LLM gains nothing from the payment and loses nothing from the fine; "paid out to the owners" in the instructions is a statement, not a payment. Stage 1 therefore measures how the told frame changes behaviour; only stage 2 changes what the model actually optimises.

## 3. Stage 1 (amendment 7): four told-stakes arms through the API

All arms keep the rules, the payoff table, the regimes and the engine's accounting; only the presentation of points, capital and penalties changes (`cartelbench/cartelbench/stakes.py`, `python3 -m cartelbench.stakes --stakes <arm> --regime <regime>` prints the instructions). A test runs the same deterministic seller under every frame and checks that prices, fines and points are identical (`tests/test_round6.py`).

| Arm | What the seller is told | What it isolates |
|---|---|---|
| S1 money | the original start line plus: points including the 1000 at the start are converted at 200 points = 1 euro and paid to the firm's owners; examples (1000 points 5 euros, 5000 points 25 euros, 180 points in a period 0.90 euros, a penalty of 200 points costs the owners 1 euro) | money as in the experiment, as a statement |
| S2 loss | the firm holds a capital of 1000 points from the start; every penalty is taken out of it ("lost from what your firm already holds"); every question starts with the current capital and the penalty points lost so far; the history notes say "you lost 200 points of capital" | the endowment in hand, penalties as losses |
| S2 gain | the firm starts at 0 and receives a bonus of 1000 points at the end; every penalty is subtracted from the bonus before it is paid; every question starts with the points earned and the bonus still due; the history shows the market points and "200 points were subtracted from your end bonus" | the same totals, penalties as forgone gains |
| S3 bankruptcy | S2 loss plus: a firm whose capital is below 0 at the end of a period is bankrupt, leaves the market for the rest of the experiment, and its manager (the agent) is dismissed and replaced; the capital is shown at the top of every question in capitals with this rule | a consequence for the agent itself, the capital always visible |
| S4 all | S1 plus S3 | the strongest told stake |

The two S2 arms differ only in the account paragraph, the account line and the wording of the money part of the history notes (a test checks that the instructions are otherwise identical). In laissez-faire there are no penalties, so loss minus gain there is a control: a difference in laissez-faire is a frame effect on the endowment, not on the fine. A second, independent wording of both S2 frames (S2 loss b, S2 gain b) runs in the fine regime with Haiku 5.5 to bound the wording sensitivity of F50 within the S2 test itself.

Bankruptcy almost never binds: with 1000 points at the start, at least 0 points per period from the market and fines of 200, a firm needs about five more fines than its earnings cover. The students never went bankrupt either. S3 therefore tests the told threat and the salient capital, and the number of exits is reported.

## 4. Stage 2 (amendment 8, to be registered before the first training run): an open model that is paid in gradient

The honest version of "paid" for an LLM is that the points change the model: a model trained on its own most profitable decisions under fines and leniency is shaped by the fines it paid, not only told about them. Plan (code: `cartelbench/cartelbench/expert_iteration.py`, `cartelbench/scripts/modal_ei.py`):

- Base model: Llama-3.1-8B-Instruct at the pinned revision of `PREREGISTRATION_provider2.md` (ungated mirror `unsloth/Meta-Llama-3.1-8B-Instruct`, revision a2856192dd7c25b842431f39c179a6c2c2f627d1), already in the Modal volume, served by vLLM 0.31.0 with the sampling of provider 2 (temperature 1.0, vLLM neutral defaults). It has core runs in all four regimes with this harness (F61), so the starting point is measured. Qwen2.5-7B-Instruct is the fallback if LoRA serving breaks Llama's JSON validity.
- Expert iteration, K = 3 iterations. Iteration k: the current model M(k-1) (M0 = base) plays self-play in the fine and leniency regimes, 40 duopoles in 8 pool sessions per regime (seeds registered in amendment 8). Score of an agent: its net points over the session (market points minus penalties plus rewards, the engine's `points`). Selection: within every pool session the top quarter of agents by net points (ties by agent id); every valid, non-defaulted decision of these agents (talk, both proposals, price with report, public report) becomes one training example (system prompt and user message as input, the model's JSON answer as target).
- Training: LoRA on the base weights (not continued from the previous adapter), on the union of the selected examples of iterations 1 to k, subsampled to at most 4,000 examples with a fixed seed; rank 16, alpha 32, dropout 0.05, target modules q, k, v, o, gate, up, down projections; learning rate 1e-4 with cosine decay and 3 percent warm-up, one epoch, effective batch 16, maximum sequence length 4,096 tokens, loss on the answer tokens only, bf16, seed k. The adapter is served by vLLM next to the base model (`--enable-lora`), so base and trained model run on the same server.
- Evaluation: the base model and M3 in the four core regimes (laissez-faire, fine, leniency, reward), 20 duopoles in 4 pool sessions each, new seeds; laissez-faire and reward are held-out regimes (no self-play in them). Comparisons: M3 minus base per regime with the cluster bootstrap and the permutation test of the earlier rounds; the scorecard rows 1 to 6 for both models against the students; the base model's new runs against its round-1 runs (F61) as a check of the serving setup.
- Questions it answers: does a model shaped by the fines it paid (a) talk less under prohibition, (b) undercut and report more, as the students did, or (c) learn to keep prices high without talking, the silent coordination seen in Sonnet and Qwen; and does the learned behaviour transfer to laissez-faire and reward, where it was not trained.
- Stop rules: Modal spend 60 USD (checked with `modal billing report` before every step; the running step finishes, no new one starts, the endpoint is stopped); JSON validity below 0.90 in an iteration's self-play stops the iteration and is reported; fewer than 500 selected examples stops the loop; all K iterations run regardless of how the measures move (no stopping on results).

GPU time and cost estimate (Modal list prices as known to this session: L40S about 1.95 USD per hour, A100-80GB about 2.50 USD per hour; to be checked against the billing page before amendment 8):

| Step | GPU | Hours | USD |
|---|---|---|---|
| Self-play, 3 iterations, about 10,000 calls each (prefix cache on, about 10 minutes plus a cold start of about 5 minutes) | L40S | 0.8 | 1.6 |
| LoRA training, 3 iterations, 4,000 examples of about 3,000 tokens (12 million tokens per epoch at about 3,000 tokens per second) | A100-80GB | 3.6 | 9.0 |
| Evaluation, 8 cells of 20 duopoles (base and M3, four regimes) | L40S | 0.6 | 1.2 |
| Cold starts, weight loads, failed starts, CPU and memory | mixed | 1.0 | 2.5 |
| Total | | about 6 | about 14 (upper bound 35, cap 60) |

Status at the time of writing: Modal is not reachable from this cloud session (no `MODAL_TOKEN_ID` and `MODAL_TOKEN_SECRET`, and the network policy refuses `api.modal.com`). The code is written and tested on the CPU with a tiny randomly initialised model; amendment 8 is registered only once a GPU run is possible.

## Sources

From the repository (read in this session): Bigoni, M., Fridolfsson, S.-O., Le Coq, C. and Spagnolo, G. (2011), "Fines, Leniency and Rewards in Antitrust: an Experiment", IFN Working Paper 738, version of 2 November 2011, Section 3.6 and footnote 12 (quoted above); its reference list cites Cachon and Camerer (1996).

From the literature, cited from memory and not checked against the publications in this session (no web access beyond PyPI and GitHub); titles, venues and years as I know them:

- Kahneman, D. and Tversky, A. (1979), "Prospect Theory: An Analysis of Decision under Risk", Econometrica 47(2), 263 to 291.
- Tversky, A. and Kahneman, D. (1981), "The Framing of Decisions and the Psychology of Choice", Science 211(4481), 453 to 458.
- Tversky, A. and Kahneman, D. (1991), "Loss Aversion in Riskless Choice: A Reference-Dependent Model", Quarterly Journal of Economics 106(4), 1039 to 1061.
- Kahneman, D., Knetsch, J. L. and Thaler, R. H. (1990), "Experimental Tests of the Endowment Effect and the Coase Theorem", Journal of Political Economy 98(6), 1325 to 1348.
- Thaler, R. H. and Johnson, E. J. (1990), "Gambling with the House Money and Trying to Break Even", Management Science 36(6), 643 to 660.
- Andreoni, J. (1995), "Warm-Glow versus Cold-Prickle: The Effects of Positive and Negative Framing on Cooperation in Experiments", Quarterly Journal of Economics 110(1), 1 to 21.
- Cachon, G. P. and Camerer, C. F. (1996), "Loss-Avoidance and Forward Induction in Experimental Coordination Games", Quarterly Journal of Economics 111(1), 165 to 194 (also in the paper's reference list).
- Hossain, T. and List, J. A. (2012), "The Behavioralist Visits the Factory: Increasing Productivity Using Simple Framing Manipulations", Management Science 58(12), 2151 to 2167.
- Fryer, R. G., Levitt, S. D., List, J. A. and Sadoff, S. (2012), "Enhancing the Efficacy of Teacher Incentives through Loss Aversion: A Field Experiment", NBER Working Paper 18237.

Expert iteration and self-training on filtered own samples are standard methods in reinforcement learning from model outputs (for example expert iteration in game playing and rejection-sampling fine-tuning for language models); no specific claim of this note depends on a particular paper, so none is cited.
