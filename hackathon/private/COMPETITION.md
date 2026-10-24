# COMPETITION · AI Collusion Research Sprint (internal: committed during the build, removed from the tree at the close-out)

> Written by the framework research session. Public submissions only. A snapshot with date and time, because repos change until the deadline. No rubric scores here: scoring is the jury simulation's job (`private/reviews/`).

Snapshot (date, time, time zone): 2026-10-24 14:05 HKT (06:05 UTC), about 30 hours before the deadline. Nothing is officially published yet: submissions appear on the sprint page only after the deadline (manual publication, up to 12 h). What is visible are early public GitHub repos, most of them empty scaffolds. 1,650 people signed up (sprint page counter); the number of final submissions will be far lower (Apart's Global South hackathon 2026 had 216 to 217 submissions from a larger sign-up pool, per hub retrospectives on the EA Forum).

Where searched (GitHub queries with date filter, Devpost or the official gallery, social posts, last edition's winners): `gh search repos` with `created:>2026-10-22` and the terms collusion; apart sprint; dolos; collusion_hackathon; steganography agents; and `created:>2026-10-20` collusion llm agents (2026-10-24 14:05 HKT). Sprint page gallery: empty until after the deadline. Devpost: not used by Apart. Social posts: not searched (time). Last editions: Apart publishes sprint projects on apartresearch.com after judging; no winners list for 2026 sprints was found by web search (searched "Apart Research hackathon winners 2026", "AI Control Hackathon winners", "Global South AI Safety Hackathon winners").

## Entries per track

| Track | Entries | Notes |
|---|---|---|
| 1 Markets and Collusion | 9 public repos | replacement/succession (1.2) ×2, pricing levers and undercuts (1.1) ×2, net influence (1.4) ×2, detection calibration (1.3) ×1, energy-trade market (own setting) ×1, coalition-vs-coalition market study ×1 |
| 2 Detection and Audit | 8 public repos | plus factors on a payment ledger (2.3), talk-without-action detector test (2.2/2.3), simulated collusion ground-truth artifact (2.3), leaderboard and bid-rigging testbeds (2.1), two Dolos red-teaming repos, collusion-audit scaffold, poker fraud demo (off-theme) |
| 3 Carriers and Countermeasures | 2 public repos | learned vector channels between frozen LLMs with countermeasures (3.1), peer-swap (3.3) |
| unclear / empty scaffolds | 8 | names only (collusion_hackathon forks, "ai-collusion-sprint", "Collusion_Sprint", satellite collusion avoidance) |

Total: 27 repos created 2026-10-23 or 2026-10-24 that name the sprint or its terms, 1 of them ours (private). Counted by description; many have no README yet.

## Strongest entries

| # | Entry (link) | Track | What it is, in one sentence | Why it is strong |
|---|---|---|---|---|
| 1 | https://github.com/groothaha/vector-channel-countermeasures | 3.1 | Countermeasures and monitor probes for learned vector channels between frozen LLMs | goes beyond the starter repo (a learned carrier, not text); countermeasure plus probe in one |
| 2 | https://github.com/saltxd/plus-factors-on-the-ledger | 2.3 | "Plus factors" from antitrust applied to coordinated demand in live AI-agent payment markets | picks up the exact antitrust framing the Resources tab asks for, on a real ledger |
| 3 | https://github.com/horigyns/cartel-rivalry-study | 1 | Pre-registered LLM coalition-vs-coalition market study (clearing rules, model refusals, scarcity contests) | pre-registration signals rigor; coalition-vs-coalition is a new axis |
| 4 | https://github.com/belln1/simcol_eval | 2.3 | "Simulating Collusion and Enforcement: A Ground-Truth Artifact for Evaluating Empirical Methods" | a ground-truth artifact is exactly the "convincing evidence" question; reusable by others |
| 5 | https://github.com/saihariG/talk-without-action | 2.2/2.3 | Do collusion detectors catch real coordination or just collusive talk that cannot affect prices? | tests the words-vs-actions gap with a clean falsifiable question |
| 6 | https://github.com/SupratikB23/LLM-Cartel-Succession | 1.2 | Does price collusion survive agent replacement via inherited price history | direct answer to 1.2 with the LLMCartel harness; already has a star and a description |
| 7 | https://github.com/777sun77/dolos-compromised-overseer | Red-teaming | "Dolos-1.5B is a compromised overseer" (Sihu Park) | claims a specific hypothesis on the hidden behaviour already on day 1 |
| 8 | https://github.com/franciseliang99-dot/calibrated-net-influence | 1.4 | Calibrated net-influence tests for colluding pairs from action logs | calibration is the step the Resources tab says is missing |
| 9 | https://github.com/soumya-nayak-commits/collusion-detetction | 1.4 | Pairwise net influence vs a Cramér's V baseline | has a named baseline, the thing most entries forget |
| 10 | https://github.com/ArnolFokam/collusion-harness and https://github.com/ArnolFokam/collusion-leaderboard | 2.1 | Bid-rigging and leaderboard testbeds with hidden-truth scoring and episode logs | new environments outside markets (2.1 asks for exactly that); same author, three repos |
| 11 | https://github.com/Stasfer02/research_sprint-colluding-agents-energy-trade | 1 | Collusion between intracompany balancing actors in energy trading | a domain nobody else has; market intuition transfers |
| 12 | https://github.com/Noah19823/AI-Collusion---Response-to-Forced-Undercuts-under-a-Forced-Deviation-test-on-LLM-Agents. | 1.1 | How LLM agents respond to forced undercuts (forced-deviation test) | a single clean lever, matches the "one variable at a time" advice |
| 13 | https://github.com/yiping-miao/AI-collusion-redteaming and https://github.com/bubskee/dolos-lenses | Red-teaming | Dolos red-teaming; "dolos-lenses", tools for sprint participants | signals that several teams attack Dolos; a shared tool could raise the floor for all of them |

## Minimum standard

What every good entry already has, so it earns no points on its own: running the starter repo's weekend project with the supplied positive control; one lever varied; an LLM judge as the detector; 3 to 5 seeds; a README with setup. Among the early repos, the ones with descriptions already name a baseline (Cramér's V), a pre-registration, or a falsifiable question; a report that only replicates Fish et al. or Agrawal et al. with one new prompt will sit at Impact 2 to 3.

## Gaps

Tracks or angles nobody covers well (as of the snapshot): 3.2 trusted agents (no public repo); 3.4 coalition behaviour under partial monitoring (none); 1.5 cost of a single restriction against legitimate performance (none); 2.2 as a structured claims-vs-outcomes monitor with reported false-positive rate (one adjacent entry); the finance framing the HK hub asks for (only the energy-trade and ledger entries); cross-provider "Schelling salience" detection without a channel (1.3, one scaffold). Dolos red-teaming is crowded (at least 4 repos) and shared tools circulate, so a Dolos-only project competes on explanation and audit method, not on finding the behaviour.

## Last edition's winners

| Year | Winner | What won | Source |
|---|---|---|---|
| 2026 | Jurgis Kemeklis and Nikhil Vemuri, Apart AI Control Hackathon | "Omission Attacks: When Doing Nothing Is the Attack": agents cause harm by leaving out necessary actions; follow-up found omissions caught much less often than commissions, even by strong monitors | sprint page speaker bio (2026-10-24); https://www.lesswrong.com/posts/5W38vuwbJmTYfY6t3/omission-attacks-project-proposal |
| 2026 | Global South AI Safety Hackathon (Apart): 6 winners from 216 to 217 submissions, for example ColDron (open dataset of drone attacks in Colombia) | a dataset others can check; honourable mentions for hubs | EA Forum hub retrospectives (Bogotá, Mexico), https://forum.effectivealtruism.org/posts/Kxd58zbWMJwtDmXQ9/running-the-bogota-hub-of-apart-s-global-south-ai-safety |
| earlier | TraceGuard (Khanh Linh Nguyen), built at an Apart x Redwood hackathon, now a speaker's paper and a starter folder | a monitoring protocol that became a paper (2604.03968) | starter repo README, sprint page |

What a 4 or 5 report has, from these: one new attack or evidence class with a name ("omission attacks", "plus factors"), a small experiment that others could rerun, a surprising quantitative finding stated in the abstract, and a path to a follow-up (fellowship, paper). First-edition note: this is the first AI Collusion sprint, so there is no direct previous edition.

## Rescans

(none yet; the main session sends "Rescan COMPETITION.md" and the result goes here as a new dated section)
