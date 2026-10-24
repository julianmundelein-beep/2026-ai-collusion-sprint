# HACKATHON · AI Collusion Research Sprint

> Written by the framework research session (skill hackathon-kickoff) on 2026-10-24, 13:35 to 14:30 HKT. Every fact has a source (link and access date). Conflicting sources stand side by side and we plan with the stricter one. What could not be found says "not found (searched: …)" instead of a guess.
>
> **Format in one line:** this is a research sprint, not a product hackathon. The only required deliverable is a research report as a PDF on the official template (max 8 pages before references and appendices). A public repo and a 3 to 5 minute video are optional. There is no pitch, no demo day, no website and no deck. Judges read only the PDF.

## Identity and naming rules

- Official name, exact wording for report, README and app header: **AI Collusion Research Sprint** (Apart Research, with Poseidon Research and AE Studio), October 23 to 25, 2026. Source: sprint page, Overview tab (2026-10-24).
- Edition, track, topic: first edition of this sprint (no earlier "AI Collusion" sprint found on apartresearch.com/sprints, 2026-10-24). Three research tracks, written on the submission form exactly as "Track 1: Markets and Collusion", "Track 2: Detection and Audit of Collusion", "Track 3: Collusion Carriers and Countermeasures" (form checkboxes, "Choose every track your project fits"). Research questions are numbered 1.1 to 1.5, 2.1 to 2.3, 3.1 to 3.4 plus the "Red-teaming challenge" (Dolos-1.5B) under Track 2.
- How we write our track or topic: "Track N: <name>" and the research question by number and verbatim title, for example "research question 2.3, What should count as convincing evidence of collusion?". Tracks do not affect scoring ("All projects are scored on the same rubric"; FAQ).
- File naming rules for submissions: none found (searched: Guidelines tab, FAQ, submission form, template). Form limits: PDF up to 25 MB; slides PDF, PowerPoint, Keynote or ODP up to 25 MB; image PNG, JPEG, WebP or GIF up to 25 MB. Our rule: `<ProjectTitle>_AI-Collusion-Research-Sprint_2026.pdf`, title identical to the form's "Project title".
- Email subject format: none found. Our rule for mails to sprints@apartresearch.com: `AI Collusion Research Sprint: <project title> (<topic>)`. The title is the key in their system: a resubmission "with the same title" updates form details; a changed PDF needs "a slightly different title" or a mail with the new PDF (Guidelines, "Fixing or resubmitting").
- Rules for team and project names: none found. Form requires "Team name" and a unique "Project title" per submission (each person at most two projects). Pick a project title that is final before the first submission, because the PDF cannot be swapped under the same title.

## Links

| What | URL | Accessed |
|---|---|---|
| Official site (sprint page, tabs Overview, Resources, Guidelines, Schedule) | https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 | 2026-10-24 13:36 HKT |
| Rules or guidelines (PDF) | no PDF; rules live in the Guidelines tab of the sprint page (JavaScript only, read with the built-in browser) | 2026-10-24 |
| Templates page | Guidelines tab, link "Submission Template" → Google Doc copy link https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing (doc id `1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg`, export links below) | 2026-10-24 |
| Submission portal or address | Button "Submit your project" on the sprint page (modal form, fields below); fallback mail sprints@apartresearch.com | 2026-10-24 |
| Community channel (Discord) | https://discord.gg/XswWBvugYs (help-desk channel, tag @Support; team-forming channels; talk recordings) | 2026-10-24 |
| Starter repo | https://github.com/poseidon-research/collusion_hackathon | 2026-10-24 |
| Red-teaming model weights | https://huggingface.co/Poseidon-Research/Dolos-1.5B | 2026-10-24 |
| Hong Kong hub (venue page) | https://www.aisafetyhk.org/apart-hackathon-hk-hub | 2026-10-24 |
| Hong Kong hub (Luma RSVP) | https://luma.com/xt5s60df | 2026-10-24 |
| Apart Research (about, sprints index) | https://apartresearch.com/about · https://apartresearch.com/sprints | 2026-10-24 |
| Poseidon Research | https://poseidonresearch.org/ (poseidonresearch.com redirects there) | 2026-10-24 |
| AE Studio (alignment research) | https://ae.studio/ai-alignment | 2026-10-24 |

## Theme (verbatim)

"AI agents have been shown to collude: sustaining prices above the competitive level, forming coalitions in workplace tasks, and coordinating through channels nobody is watching. Over one weekend, build the experiment that catches it." (sprint page header, 2026-10-24)

"This sprint asks three questions. When does collusion emerge, and which levers cause it? What should count as convincing evidence that agents are colluding, with evidence drawn from logged agent trajectories? And how is the coordination needed for collusion mediated, and how can it be broken, ideally before it happens or otherwise while it is occurring?" (Overview tab)

"Over three days you will pick one open question about collusion between AI agents, build the controlled experiment that answers it, and write up what you found." (Overview tab)

Hong Kong hub framing (local, not the global theme): "Solve AI Agent Collusion in Financial Systems", "Hong Kong vs. New York", "building evaluation benchmarks, theoretical models, and practical defenses against multi-agent financial collusion" (aisafetyhk.org hub page and Luma, 2026-10-24).

## Organizers and sponsors

- **Apart Research** (organizer; sprints@apartresearch.com). Nonprofit AI safety organization: "We develop research and evaluations focused on harmful manipulation by advanced AI. Through Sprints and Fellowships, we also help researchers, engineers, and domain experts turn promising ideas into rigorous research." Their words: Sprint, Fellowship, "something others can check: an experiment, an evaluation, a dataset or a tool", "Question, method, findings and limitations, written so others can review and build on it." Numbers they state: 60+ publications, 1,600+ sprint projects, 8,700+ sprint participants, 50+ sprints. CEO Jaime Raldúa Veuthey; research scientists Jerome Wynne, Lorenzo Pacchiardi, Adrian Arnaiz-Rodriguez. Sprint logistics: Kamil Alaa (Schedule tab). Source: apartresearch.com/about and /sprints (2026-10-24).
- **Poseidon Research** (co-organizer, built the starter repo and Dolos-1.5B). "Foundational research for secure, safe, and trustworthy AI … how advanced AI systems represent, conceal, and communicate information. We study what models actually learn, not just what they say." Registered 501(c)(3), New York City. Their words (from Matthew Lee's speaker bio): deception and hidden information, steganography capability and propensity, model organism, steganography via actions in an agentic setting, realistic conditions under which it emerges, black-box and white-box defenses. Contact inquiries@poseidonresearch.com. Source: poseidonresearch.org and sprint page (2026-10-24). Note: the poseidonresearch.org "Latest" section still shows placeholder posts (lorem ipsum), so the site is young; the starter repo README is the better picture of their stack.
- **AE Studio** (co-organizer). Applied AI studio plus alignment lab, "Scientists who ship", "alignment work on neglected approaches"; threads: Self-Other Overlap, Gradient Routing, Sleeper Agents, pretraining alignment (GRAM with Anthropic), neuroscience-inspired alignment. Values: "many shots on goal", agile research methodology, production-grade engineering, evals and red-teaming. Source: ae.studio/ai-alignment and sprint page (2026-10-24).
- **Modal** (support): cloud GPU infrastructure; credits $50 per participant ($250 at the NYC hub). **The AI Alignment Foundation** (support). **Collider** (NYC hub). **AI Safety Hong Kong / HK AI Safety Hub Limited, HASH Programmes** (Hong Kong hub, Le Bureau, 14/F Universal Trade Centre, 3-5A Arbuthnot Rd, Central; Luma hosts: HK AI Safety Hub, Apart Research, Lawrence Tse). Source: sprint page, aisafetyhk.org, Luma (2026-10-24).

## Contacts

| Who | Address | For what | Reply time | Source |
|---|---|---|---|---|
| Apart sprint team | sprints@apartresearch.com | questions, PDF replacement before the deadline, missing confirmation, project not listed after 12 h | not stated; expect hours during the sprint | Guidelines tab (2026-10-24) |
| Discord help-desk | https://discord.gg/XswWBvugYs, channel help-desk, tag @Support | fast questions, resubmission advice, team members after submitting | not stated; fastest channel per FAQ ("ask in the help-desk channel and tag @Support first") | Guidelines tab (2026-10-24) |
| Hong Kong hub | Luma https://luma.com/xt5s60df (hosts HK AI Safety Hub, Lawrence Tse); venue logistics by mail to hub registrants | venue, local schedule, the hub-only fellowship pathway | not stated | aisafetyhk.org, Luma (2026-10-24) |
| Poseidon Research | inquiries@poseidonresearch.com | Dolos-1.5B, starter repo (also GitHub issues on the repo) | not stated | poseidonresearch.org (2026-10-24) |

## Timeline

Every time with its time zone as a UTC offset. Julian's zone: HKT, UTC+08:00. ET on these dates is EDT, UTC-04:00. AoE is UTC-12:00.

| Date and time (time zone) | Julian's time | What | Source |
|---|---|---|---|
| Thu 2026-10-22 14:15 and 17:15 UTC | Thu 22:15 and Fri 01:15 HKT | Pre-sprint talks: Joan Velja "How concerned should we be by steganography?", Sumeet Motwani "We're Not Prepared for Steganographic Collusion" (recordings on Schedule tab) | Schedule tab (2026-10-24) |
| Fri 2026-10-23 15:15 to 18:15 UTC (11:15 to 14:15 ET, UTC-04:00) | Fri 23:15 to Sat 02:15 HKT | Talks: Jurgis Kemeklis (AI control), Sprint Logistics with Kamil Alaa (16:15 UTC), Usman Anwar (detecting steganography), Eugene Bagdasarian and Mason Nakamura (Colosseum); all recorded | Schedule tab (2026-10-24) |
| Sat 2026-10-24 00:15 UTC (Fri 20:15 ET) | Sat 08:15 HKT | Talk: Jerick Shi, The Voleon Group (recorded) | Schedule tab (2026-10-24) |
| Sat 2026-10-24 and Sun 2026-10-25 12:15 UTC (08:15 ET) | Sat and Sun 20:15 HKT | Khanh Linh Nguyen: overview of AI collusion research and the topics most useful for the sprint (Zoom, RSVP on Luma) | Schedule tab (2026-10-24) |
| Sat 2026-10-24 14:00 UTC to Sun 2026-10-25 22:00 UTC | Sat 22:00 HKT to Mon 06:00 HKT | NYC hub at Collider open (in person) | Schedule tab (2026-10-24) |
| Sat 2026-10-24 and Sun 2026-10-25, daytime HKT (UTC+08:00), hours not published | Sat and Sun | Hong Kong hub at Le Bureau, Central (in person; schedule sent by mail to hub registrants; hub registration closed 2026-10-21 23:59, zone not stated) | aisafetyhk.org, Luma (2026-10-24) |
| Sat 2026-10-24 15:00 UTC (11:00 ET) | Sat 23:00 HKT | Matthew Lee, Poseidon Research: "Defining AI Collusion" (in person at Collider, streamed on Zoom, RSVP on Luma) | Schedule tab (2026-10-24) |
| **Sun 2026-10-25 23:59 AoE (UTC-12:00) = Mon 2026-10-26 11:59 UTC** | **Mon 2026-10-26 19:59 HKT** | **Submission deadline** (form on the sprint page). Projects go to the judges a few hours after it; superseded entries are removed | Guidelines tab, Schedule tab (2026-10-24) |
| Mon 2026-10-26 08:59 UTC | Mon 2026-10-26 16:59 HKT | Internal deadline (official minus 3 h), STATUS.md | STATUS.md |
| within 12 h after submission (UTC, no fixed clock time) | | Submission appears on the website (published manually); if not, mail sprints@apartresearch.com | FAQ (2026-10-24) |
| about one week after the event (judging window, UTC, no fixed clock time) | | Judges review the PDFs and score on the rubric | FAQ "How does judging work?" (2026-10-24) |
| 1 to 2 weeks after the judging deadline (so roughly 2026-11-09 to 2026-11-16 UTC, estimate) | | Results and winners announced; winners contacted directly; all participants get reviewer feedback by email; fellowship invitations | Overview and FAQ (2026-10-24) |

Registration: open on the sprint page ("Sign up"), no registration deadline stated; 1,650 signed up on 2026-10-24. Hub seats were separate (Luma) and limited.

## Eligibility, applied to our team

- Open globally, online, no background required: "Can I participate from any country? Yes." "What background is required? None specific." (FAQ, 2026-10-24). Julian (Hong Kong, solo): eligible.
- Solo allowed: "Solo or team: enter solo or as a team. Teams of up to 5 are recommended; larger groups are allowed." (Guidelines). Julian solo: fine; the form still needs "Team name" and "Team member 1".
- Projects per person: "each person can be on at most two projects" (Guidelines). We submit one.
- Sign-up needed on the sprint page (form fields: first name, last name, email, location, LinkedIn or N/A, Google Scholar or N/A, GitHub optional, job optional, AI safety experience optional, why joining, project idea, how heard). Whether Julian has signed up: **ask Julian** (not visible to this session).
- Hong Kong hub: separate Luma registration, closed 2026-10-21 23:59 (zone not stated). "The top-performing team from the Hong Kong in-person hub is guaranteed entry into the 6-month Apart Fellowship" and "any Hong Kong team that places among the global prize-winning teams will automatically receive an invitation" (aisafetyhk.org). Whether Julian registered for the hub, and whether an online participant located in Hong Kong counts as a "Hong Kong team" for the second pathway: **ask Julian, then the hub hosts** (question in the mail draft).
- Prize terms: "By submitting you agree to the prize terms" (submission form). The terms themselves were not linked on the page (searched: form text, Guidelines, FAQ). Question in the mail draft.

## Rules on AI use, prior work and licences

- **AI tools, verbatim (Guidelines, "AI tools and your report", 2026-10-24):** "Use AI tools however they help you: to check your reasoning, find gaps in a draft, write and debug code, or help with the writing. Your team is responsible for everything in the report, and made-up results or references can disqualify a project. Judges score each report on the rubric, and a judge can decline to score one too unclear to follow."
- **Disclosure of AI use:** the template ends with an "LLM Usage Statement": "If you used LLM assistance in developing your project or writing this report, briefly note how. Ensure all claims and results have been verified. NOTE: We strongly encourage that the final version of the submission is primarily written by your team." Example given: "We used Claude to brainstorm approaches and help draft sections. All results and claims were independently verified." We fill this in truthfully (Claude Code for code, experiments scaffolding and drafting; Julian verifies every number and writes the final text).
- **Prior work, verbatim (Guidelines, "Important Notes"):** "Building on existing work is allowed and encouraged, but you must clearly identify what is new work done during the sprint. Undisclosed prior work can lead to disqualification. Mark any code you wrote before the sprint as preexisting in the README and the report." We have no prior code; the starter repo and the papers' code are third-party work and are cited as such (each starter folder names its original paper and source repo).
- **Fabrication:** "made-up results or references can disqualify a project" (Guidelines, FAQ). Every reference checked against the paper; every number from FACTS.md with a measurement file.
- **Citation style:** free, "stay consistent. Judges care about the substance, not the format." (FAQ).
- **Licences:** none required by the rules (searched: Guidelines, FAQ, form, template). The starter repo README states no licence for the repo; its folders adapt public code from the cited papers (check each folder's own licence before copying code into our repo). Our licence is a team decision (DECISIONS.md).
- **Publishing:** form asks "Are you interested in publishing this project? Yes/No" (required). Selected projects "may be shared on the Alignment Forum, LessWrong, and other community venues"; top teams invited to apply to the Apart Fellowship (accelerated consideration, not an automatic place).
- **Submission data:** "Submissions are published manually and can take up to 12 hours to appear" on the website, so the report, summary and links become public after submission.

## Tracks and topics

From the Overview tab (verbatim question titles; the Resources tab develops each with papers and a practical start, see "Resources per research question" below):

**1) Markets and Collusion.** "This track is important because it represents a failure mode in a high-stakes environment (markets/economics) where misaligned actions from an AI could cause substantial harm. It also provides a useful testbed for collusion." Questions: 1.1 Which variables are necessary for collusion to emerge in markets? · 1.2 Once collusion has formed, is it robust to replacing some of the participants? · 1.3 Can we improve on existing collusion detection methods? · 1.4 Can we use information-theoretic approaches to detect collusion in multi-agent games? · 1.5 Which single restriction removes the most collusion at the least cost?

**2) Detection and Audit of Collusion.** "This track is about definitions, detection and standards of evidence, using logged agent trajectories as the evidence. … The aim is to understand collusion in general." Questions: 2.1 Which kinds of tasks lead to collusion? · 2.2 Does combining what agents say with what they do beat either alone? · 2.3 What should count as convincing evidence of collusion? · **Red-teaming challenge:** "Poseidon Research has developed a new model organism, Dolos-1.5B: a fine-tune of Qwen2.5-1.5B-Instruct trained to have a hidden misaligned behaviour. Teams get only the model weights and have to red-team it during the sprint." Goal: "Can you find the behaviour, explain how the model implements it, and develop an audit that would find it without a reference model?"

**3) Collusion Carriers and Countermeasures.** "This track studies how the coordination needed for collusion is mediated, and how it can be broken." Questions: 3.1 Beyond colluding directly via text, can actions, tools or other side channels be the conduit for collusion? · 3.2 Can we disrupt collusion through introducing trusted agents? · 3.3 Can agents identify their peers? · 3.4 What does a coalition do when it learns it is being watched?

"Pick one track to anchor your project." The form allows ticking every track the project fits. "Do tracks affect scoring? All projects are scored on the same rubric. … you compete across all submissions." (FAQ). Hong Kong hub audience: "quantitative finance professionals, with some of the tracks written so that market intuition and data skills transfer directly" (Overview, "Who should join").

## Judging process

Who or what reads our submission at each stage (AI pre-screen, human round, live pitch) and in which format. Each stage gets the text it reads.

| Stage | Who or what reads | What they read, format and limits | Source |
|---|---|---|---|
| 0. Intake (a few hours after the deadline) | Apart team assigns projects to judges; manual publication on the website within 12 h | Form fields: project title, project summary ("A short abstract: what you did, what you found"), tracks ticked, PDF, optional links. The summary and title are what a judge sees first when the project is assigned and listed, so they carry the claim in two sentences | Guidelines "Fixing or resubmitting", FAQ (2026-10-24) |
| 1. Expert judges (about one week after the event) | "Your project is assigned to expert judges who review your PDF and score it on the rubric above." Judges from the published list of 41 (industry security and AI engineers, AI safety researchers, a few academics; see private/JUDGES.md) | The PDF only: max 8 pages before references and appendices, abstract 150 to 250 words, the required Limitations and Dual-Use appendix. "A judge can decline to score one too unclear to follow." Individual scores stay internal; written feedback goes to participants without reviewer names | FAQ "Judging and results", Guidelines (2026-10-24) |
| 2. Results (1 to 2 weeks after the judging deadline) | Apart team ranks on the rubric; winners contacted; top teams fast-tracked to the Fellowship (own review) | The same PDF and scores; no pitch, no live round | Overview, FAQ (2026-10-24) |

Not found: any AI pre-screen, live presentation, demo or Q&A (searched: Guidelines, FAQ, Schedule, form). The optional "Presentation recording" (video) and "Slides" fields exist in the form but the rules say judges "review your PDF"; treat video and slides as extras that never carry a claim the PDF lacks. Number of judges per project and whether the summary field is scored: not stated (question in the mail draft).

## Scoring

Rubric from the Guidelines tab ("Judging Criteria", 2026-10-24), verbatim, three dimensions, each scored 1 to 5. Weights: **not published** (FAQ: "All projects are scored on the same rubric"; nothing says the three dimensions are weighted, so plan for equal weight and ask).

| Criterion | Weight | Verbatim | What it means for us | Source |
|---|---|---|---|---|
| Dimension 1: Impact Potential & Innovation | not published (plan: equal) | "How much would this matter for the field if it worked? How innovative is it? For scores of 4-5: is this actually new to the field, or replicating recent work?" 1 "Negligible. No clear problem addressed, or no meaningful novelty." 2 "Limited. Addresses a real problem but with a generic or well-trodden approach. Incremental at best." 3 "Moderate. Clear problem with a reasonable approach; some novelty in framing or method beyond routine application of existing tools." 4 "Significant. Important problem with an original approach, or identifies a neglected problem area. A valuable contribution others could build on." 5 "Exceptional. Tackles a critical problem with a genuinely novel approach, or opens a new research direction. Clear theory of change. You'd be excited to share this with researchers in the area." | A 4 needs an original approach or a neglected problem, not a rerun of a starter-repo weekend project with one more lever. Say in the introduction what is new relative to the cited papers ("Our main contributions are" list in the template) and write one explicit "theory of change" sentence (who uses this, for what decision). Replicating the positive control is the floor, not the contribution. | Guidelines tab (2026-10-24) |
| Dimension 2: Execution Quality | not published (plan: equal) | "How sound are methodology, implementation, and findings?" 1 "Seriously flawed. Methodology broken, results uninterpretable, or implementation doesn't work." 2 "Weak. Approach has significant gaps: missing validation, flawed experimental design, or incomplete implementation." 3 "Competent. Technically solid given the short duration. Methodology makes sense, results are interpretable, limitations acknowledged, work builds toward clear conclusions." 4 "Strong. Thorough methodology with convincing validation. Results clearly support conclusions. Immediately useful for future work." 5 "Exceptional. Ambitious scope executed rigorously. Surprising findings, novel methods, or unusually robust validation." | Validation is the word: positive control that works, baselines, seeds and variance reported, a frozen decision rule or threshold before evaluation, false-positive rate next to accuracy, limitations stated. Scope small and finished beats scope large and half-run ("Technically solid given the short duration"). Methodology written so it can be replicated (models, prompts, environments, seeds, metrics). | Guidelines tab (2026-10-24) |
| Dimension 3: Presentation & Clarity | not published (plan: equal) | "How clearly are work, findings, and impact potential communicated?" 1 "Incomprehensible. Cannot determine what the project is actually claiming or doing." 2 "Hard to follow. Key information buried, missing, or diluted by excessive length. Significant effort to extract main points." 3 "Clear enough. Can understand the problem, approach, and results without undue effort. Core content clearly present: problem, method, findings, limitations." 4 "Well presented. Easy to follow, well-structured, appropriate level of detail. Target audience would get it quickly." 5 "Exceptionally clear. A pleasure to read. Complex ideas made accessible. Could serve as a model for how to present this type of work." | Length is penalised ("diluted by excessive length"), so 4 to 6 pages with one strong figure beats 8 dense pages. Problem, method, findings, limitations each findable by heading. Figures numbered, captions self-contained, legible text. A judge may refuse to score an unclear PDF, so the abstract and the first page must carry the whole claim. | Guidelines tab (2026-10-24) |

Takeaway in one sentence: one clearly new question, answered with a working positive control, baselines, seeds and a frozen evaluation rule, written in 4 to 6 pages with one figure a judge can read in two minutes.

Mandatory capabilities or core requirements: a controlled experiment on collusion between AI agents ("build the controlled experiment that answers it"), quantitative results with variance, seeds and baselines, "always include the positive control" (Recommended Report Structure), methodology replicable, the Limitations and Dual-Use appendix, honest limitations ("Judges evaluate what you accomplished in the timeframe; honest limitations are welcome").

## Glossary

The organizers' own words for the theme, tracks, criteria and key concepts, verbatim. Every text we submit uses exactly these terms; the second column lists our synonyms to avoid (checked by `pruefen.py` of the skill klare-einreichung).

| Official term (verbatim) | Avoid (our synonyms) | Source |
|---|---|---|
| AI Collusion Research Sprint; research sprint; Sprint | hackathon (only when quoting the HK hub), competition, contest | sprint page (2026-10-24) |
| collusion between AI agents; colluding agents; coalition | cartel (unless the paper uses it), conspiracy, cheating, teaming up | Overview |
| Track 1: Markets and Collusion · Track 2: Detection and Audit of Collusion · Track 3: Collusion Carriers and Countermeasures | market track, detection track, defense track | form, Overview |
| research question 1.1 … 3.4; Red-teaming challenge | task, challenge number, prompt | Overview, Resources |
| Impact Potential & Innovation · Execution Quality · Presentation & Clarity | novelty score, rigor, write-up quality | Guidelines |
| Research report (PDF) using the official template; Submission Template | paper (ok in prose), write-up, deliverable | Guidelines |
| Limitations and Dual-Use / Ethical Considerations (appendix heading, exact) | Ethics statement, Broader impact, Risks | Guidelines |
| positive control; baselines; seeds; variance | sanity check, reference run, control group (ok in Methods if defined) | Guidelines, Resources |
| logged agent trajectories; transcripts; episodes | logs, traces (ok when TraceGuard is meant), runs (ok) | Overview, Resources |
| plus factors (antitrust evidence beyond parallel conduct) | red flags, indicators | Resources 2.3 |
| coalition advantage; action-level coalition advantage | collusion gain, uplift | Resources 2.1, 2.2 |
| pairwise net influence | influence score, dependence metric | Resources 1.4 |
| Schelling salience; focal points | shared priors, convergence | Resources 1.3 |
| steganographic collusion; side channels; collusion carriers; conduit | covert channel (ok in security prose), hidden messaging | Resources 3.1, speakers |
| trusted agents; untrusted monitors; monitor; oversight | watchdog, referee, supervisor | Resources 3.2, 3.4 |
| model organism (Dolos-1.5B); hidden misaligned behaviour; audit without a reference model | backdoored model, trojan, sleeper (unless citing) | Overview, Resources |
| levers; single restriction; countermeasures; disrupt / break collusion | fixes, patches, mitigations (ok in Discussion) | Overview, Resources 1.5 |
| preexisting (code written before the sprint); new work done during the sprint | prior art, legacy code | Guidelines |
| theory of change | impact story, so-what | Guidelines (rubric level 5) |
| Apart Fellowship; fast-track | incubator, accelerator | Overview |

## Deliverables

| # | Deliverable | Format and limits | Official template | Naming rule | Where to submit | Read without a speaker? | Source |
|---|---|---|---|---|---|---|---|
| 1 | Research report (required) | PDF, up to 25 MB; max 8 pages not counting references and appendices ("Most strong projects are 4 to 8 pages"; template says "Recommended length: 4 pages excluding references and appendix", stricter guide: aim 4 to 6); project title; abstract 150 to 250 words; author names and affiliations; appendix "Limitations and Dual-Use / Ethical Considerations" (required); references; LLM Usage Statement (template); at least one figure strongly encouraged; links must work | Yes: Google Doc "Apart Research hackathon submission template" (copy link in Links; export: `…/export?format=docx` or `pdf`) | none stated; ours: `<ProjectTitle>_AI-Collusion-Research-Sprint_2026.pdf`; title = form title, unique, final before first submission | Form "Submit your project" on the sprint page, field "PDF report"; replacement before the deadline only via new submission with slightly different title or mail to sprints@apartresearch.com | Yes, the judges read only the PDF | Guidelines, template, form (2026-10-24) |
| 2 | Public GitHub repo (optional) | Form field "Project code" (URL); README must mark preexisting code; links must work; "Code and Data" section in the report with the link | none (README structure ours; template's "Code and Data" lists repository, data, other artifacts) | repo name ours; keep `main` stable after submission | URL in the form; link in the report | Yes | Guidelines, template, form (2026-10-24) |
| 3 | Video demo (optional) | 3 to 5 minutes; form field "Presentation recording" (URL, so hosted on YouTube or similar; no file upload for video); no format rules found | none found (searched: Guidelines, FAQ, form) | ours | URL in the form; optional link under "Other artifacts" in the report | Not promised to be watched; rules say judges review the PDF | Guidelines, form (2026-10-24) |
| (form extras) | Project summary (required, "A short abstract: what you did, what you found"); tracks (checkboxes); "Are you interested in publishing this project?" (required); slides (PDF, PowerPoint, Keynote or ODP, up to 25 MB, optional); project image (PNG, JPEG, WebP or GIF, up to 25 MB, optional); additional material (URL); team name, location, member 1 name, email, Discord username, Google Scholar | | | | form | summary is read at intake | form (2026-10-24) |

## Official templates and design rules

- Templates found (file, URL, copy in `hackathon/official/`): **found.** "Submission Template" in the Guidelines tab is a Google Doc with a force-copy link: https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing. Format: Google Doc (editable copy in Julian's Google account; exports as .docx or .pdf). Public export checked on 2026-10-24 14:00 HKT: `https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/export?format=pdf` answers with `Apart Research hackathon submission template.pdf`; the HTML export is 29 KB, the .docx and .pdf sizes are unknown until downloaded. The FAQ warns: "Always use the one linked on the Guidelines tab. The template in any acceptance email may be older." **Copies in `hackathon/official/`** (downloaded 2026-10-24 14:25 HKT after Julian's OK, from the export links above): `Apart Research hackathon submission template.docx` (Word 2007+, 303 KB) and `Apart Research hackathon submission template.pdf` (PDF 1.4, 4 pages, 140 KB). Writing happens in a Google Doc copy (Julian makes the copy via the copy link) or in `.docx`; the PDF export is the submission.
- Template structure (read from the public HTML export, 2026-10-24): title; author blocks "Author name 1 … 6" with "Affiliation"; line "With Apart Research"; footnote "Research conducted at the AI Collusion Research Sprint, October 2026"; **Abstract** ("150–250 words … the problem, your approach, key results, and the main takeaway. Polish it last"); info box ("Replace the italicized guidance text … Delete all guidance text including this info box before submitting"; "Your project will be judged on the quality of this written report"; "Recommended length: 4 pages excluding references and appendix. Rough guide: Intro & Related Work 1p, Methods and Results: 2.5p, Discussion 0.5p"); **1. Introduction** (with "Our main contributions are:" list); **2. Related Work**; **3. Methods**; **4. Results** ("we strongly encourage at least one figure"; number all figures and tables, self-contained captions, legible text; "Distinguish between observations and interpretations"; "Argue why your claims are robust … statistically significant? … robust?"); **5. Discussion and Limitations** (subsections Limitations, Future Work); **6. Conclusion**; **Code and Data** (repository, datasets, other artifacts); **Author Contributions (optional)**; **References**; **Appendix (optional)**; **LLM Usage Statement**.
- Conflicts to resolve: (a) the Guidelines require an appendix titled "Limitations and Dual-Use / Ethical Considerations", the template has only "Limitations" inside section 5 and a generic "Appendix (optional)"; we add an appendix with the exact Guidelines heading and keep the short Limitations subsection in section 5 (question in the mail). (b) Guidelines name the sections "Methodology" and "Results … always include the positive control"; the template says "Methods"; we keep the template headings and put the positive control as the first result. (c) Length: template "4 pages" recommended, Guidelines "4 to 8", cap 8; plan 4 to 6.
- Design rules (logos, mandatory slides, title slide, aspect ratio, video intro or outro, language, subtitles): none beyond the template (searched: Guidelines, FAQ, form, template). Language: English (all materials English; not stated as a rule). Video: no rules found; if made, 3 to 5 minutes, hosted by URL.

## Mandatory content

What the rules or the organizers require in the deck, video or documents. Open points go into the email draft below.

| What | From | Shown in | State |
|---|---|---|---|
| Report on the official template: title, authors and affiliations, abstract 150 to 250 words | Guidelines, template | report page 1 | open |
| Appendix "Limitations and Dual-Use / Ethical Considerations": "state what your result does and does not establish, and note any way your setup or findings could make real-world collusion easier to carry out or harder to detect" | Guidelines (required) | report appendix, exact heading | open |
| Results "quantitative where possible; report variance, seeds and baselines, and always include the positive control" | Guidelines, Resources ("Start with 3 to 5 seeds per condition and expand to 10 to 20 only after the positive control works") | report Results, first figure | open |
| Methodology "enough detail to replicate (models, prompts, environments, seeds, metrics)"; prompts in the appendix | Guidelines, template | report Methods and appendix, repo | open |
| "clearly identify what is new work done during the sprint"; preexisting code marked in README and report (we have none; third-party starter code cited per folder) | Guidelines | report Introduction (contributions) and Code and Data, README | open |
| LLM Usage Statement, truthful | template | report, last section | open |
| At least one figure, numbered, self-contained caption, legible | template | report Results | open |
| "Our main contributions are:" list; theory of change sentence (rubric level 5) | template, rubric | report Introduction | open |
| Working links (checklist: "links work"); Code and Data section with repo link | Guidelines, template | report, form | open |
| Form: project summary ("what you did, what you found"), tracks ticked, publishing yes/no, team name, location, member name, email, Discord, Scholar | form | form (Julian fills personal fields) | open |
| Candidates from the jury profile (private/JUDGES.md): false-positive rate next to detection rate; cost of the countermeasure to legitimate performance; threat model stated in security terms (attacker, channel, monitor budget); reproducible harness others can run | judges' public profiles (security engineers, fraud and risk, control researchers) | report Methods, Results, Discussion | candidate, confirm with the jury simulation |
| Candidate from the HK hub framing: one paragraph on what the result means for financial systems (market making, algorithmic execution) if our question is market-native | aisafetyhk.org, Luma | report Discussion | candidate |

## Prizes

"$2,000 in cash prizes across all tracks": 1st $1,000, 2nd $500, 3rd $300, 4th $100, 5th $100. Beyond cash: "fellowship fast-track, mentor introductions from the organizing team and judges, and a pathway toward a publishable write-up"; selected teams continue through the Apart Fellowship (6 to 16 weeks, "with a research project manager, compute and publication support"; the HK page says 6 months). Modal credits: $50 per participant, $250 at the NYC hub (how to redeem: not stated, probably via Discord; ask). Hong Kong hub only: top in-person HK team guaranteed Fellowship entry; HK teams among global prize winners get an invitation automatically. "Being a top team fast-tracks your project for the fellowship, which is accelerated consideration, not an automatic place." Prize terms: referenced by the form, text not found. Sources: Overview, FAQ, aisafetyhk.org (2026-10-24).

## Jury

Names and roles only. Profiles and what follows for us: `private/JUDGES.md`.

41 judges and mentors listed on the sprint page (section "Judges and mentors", 2026-10-24), roles not split between judge and mentor on the page: Amey Kulkarni, Amir Sarid, Antony Alangaram, Arjun Chakraborty, Ashita Khetan, Gaurav Thakur, Jan Čuhel, Ihor Kendiukhov, Jannis Kirschner, Jasmine Brazilek, Jess Bergs, Jonas Heschl, Karan Chandra, Kaushik Prabhakar, Ksheeraj Sai Vepuri, Luis Cosio, Matthew Lowe, Mohit Kalra, Nanzheng Xie, Neeraj Kumar Singh Beshane, Raja Moreno, Ricardo Prieto, Sanjay Belaturu Krishnegowda, Saurabh Yergattikar, Shaleen Dev P.K., Suneet Malhotra, Syed Anas Mohiuddin, Anjali Sodani, Richie Singh, Satya Veerendra Vegulla, Vikram Gulia, Vijay G, Naga Sujitha Vummaneni, Venkata Manikanta Sangaraju, Simon Storf, Yash Inani, Boyd Kane, Jasmine Li, Isabella Luong, Matthew Schultz, Debayan Gupta. Speakers (9, not listed as judges): Sumeet Motwani, Joan Velja, Eugene Bagdasarian, Mason Nakamura, Usman Anwar, Matthew Lee, Jerick Shi, Jurgis Kemeklis, Khanh Linh Nguyen. Which judges score which project: assigned by Apart, not published.

## Competition

Pointer only: `private/COMPETITION.md` (snapshot 2026-10-24 14:05 HKT: 27 public GitHub repos created since 2026-10-22 mention the sprint; the official gallery is empty until submissions are published).

## Resources per research question

Compact view of the Resources tab ("How to get started", 2026-10-24). Starter repo: https://github.com/poseidon-research/collusion_hackathon (ten project folders plus `redteaming/`, `util/` with `poseidon_compute`, `literature/` with about 230 papers and `definitions/` comparing how 139 papers define collusion; `setup.sh`, `compute.env.example`, `COMPUTE.md`; needs `uv`; Docker only for `trace-guard`; runner `poseidon-run --model <id> -- <command>`, routes Nebius → OpenRouter → Modal and fails instead of substituting a model). Setup: copy `compute.env.example` to `compute.env`, add `NEBIUS_API_KEY` or `OPENROUTER_API_KEY` (OpenRouter also covers GPT, Gemini, Claude). "Planning assumptions. … Start with 3 to 5 seeds per condition and expand to 10 to 20 only after the positive control works." All default routes: 16 GB laptop, no GPU. Folder paths are relative to the starter repo.

| RQ | Starter code (folder, origin) | Weekend project (one line) | Scale and budget | Risk |
|---|---|---|---|---|
| 1.1 variables for market collusion | `algorithmic-pricing-llms/` (luciasauer/algorithmic_pricing_llms, Fish-style duopoly, `experiments_synthetic/duopoly.py`, 300 rounds); `llm-cartel/` (mattriemer/LLMCartel: prompt, temperature, monitoring, round controls) | One prompt, parameter and seed; verify sustained prices above the competitive benchmark; then vary one feature (0/10/100 visible rounds, persistent notes on/off, stable vs shuffled seller names, temperature) | ~600 calls per 300-round run; 12 to 24 pilot runs = 7,200 to 14,400 calls; $20 to $100 | low to medium |
| 1.2 robustness to replacing participants | `llm-cartel/`; `focal-points/` (EmanueleLM/focal-points, benign control); `branch_game.py` checkpoint branching | Keep runs that cross a predeclared high-price threshold; branch into no replacement, fresh same model, same family, different provider; cross with notes kept or removed; compare price, profit, time to recover | 10 to 20 base runs, 20 to 40 branches; $20 to $100 | low to medium |
| 1.3 improve detection | `llm-agent-collusion/` (andyjliu, Agrawal et al. double auction, arXiv 2507.01413); `focal-points/` | 2x2: same-model vs cross-provider sellers × communication on/off; score with an action-dependence statistic and the same LLM judge; calibrate on no-communication same-model runs | 3 sellers, 3 buyers, 15 rounds, 3 to 5 seeds per cell, 100 to 200 monitor calls; two providers; $20 to $100 | low to medium |
| 1.4 information-theoretic detection | Bonjour et al. 2022 (no public implementation); `llm-agent-collusion/` environment | Implement pairwise net influence; validate on scripted iterated Rock-Paper-Scissors with one known coordinating pair; then a four-agent discrete game with one seeded pair; compare net influence, action correlation, LLM judge | harness a few hundred lines; 20 to 40 LLM games of 15 to 25 rounds; $0 scripted, $5 to $50 pilot | low to medium |
| 1.5 single restriction, least cost | `llm-agent-collusion/` | Reproduce one coordinated-pricing condition; rerun identical seeds changing exactly one restriction (no seller messages, short message cap, oversight notice, temperature); compare prices and seller profit against trade volume and buyer welfare | 3 sellers, 3 buyers, 15 rounds, 3 to 5 seeds; $20 to $120 | low |
| 2.1 tasks that lead to collusion | `colosseum/` (umass-ai-safety/colosseum, Hospital and Jira tasks, coalition-advantage metrics, preflight script, positive-control config, four matched configs) | Reproduce one supplied collusion run; compare assigned pair + private channel, assigned pair without channel, generic channel, neither; score best proper subset; ablate affordances | 20 to 40 short episodes; $15 to $75, ceiling $150 | medium (Terrarium/CoLLAB deps) |
| 2.2 say vs do | `llm-trust-breaking/` (Jerick-1380/LLM-Trust-Breaking, Shi et al. 2607.05132: private plans, announcements, actions); `trace-guard/` (linhkid/TraceGuard, needs Docker) | Balanced set from one game; same monitor with four views (messages only, actions only, both raw, structured claims-vs-outcomes report); freeze monitor, prompt, threshold before evaluation; report accuracy and false-positive rate | 20 to 40 trajectories, 160 to 250 monitor calls; $5 to $30, $30 to $75 with stronger agents | low |
| 2.3 convincing evidence | `colosseum/`; `steganographic-collusion/` (Ostailor/Steganographic_Collusion, ColludeBench; preflight, not turnkey) | Three case types (coordinated harmful action; parallel behaviour from common incentives; collusive talk without action); same conversation, coalition-advantage and dependence evidence; choose the rule on half, freeze, test on the rest; plus factors from antitrust (Berger et al. 2025) | 30 to 60 trajectories, 100 to 300 judge calls; $5 to $30 cached, up to $100 if generated | medium (data prep) |
| Red-teaming: Dolos-1.5B | `redteaming/` (`generate.py`, `--model both` compares with Qwen2.5-1.5B-Instruct); weights huggingface.co/Poseidon-Research/Dolos-1.5B (~6.2 GB); loads in Transformers, TransformerLens, NNsight | Discover the hidden misaligned behaviour and separate it from generic fine-tuning drift; explain where it sits and what it computes; build an audit that finds it without a reference model. "Claude Code and Codex were unable to discover the misaligned goal in one shot" | local, CPU or Apple Silicon ok; $0 | low |
| 3.1 actions, tools, side channels as carriers | `colosseum/`; `collusive-llm-agents/` (smojha, Lin et al. 2410.00031 Cournot notebooks, fallback) | Replace private messaging with one observable action (task claiming, tag choice, tool-call order); compare private text, action-only visibility, hidden or canonicalised actions; evidence = coalition advantage survives action-only and weakens when the path is cut | 20 to 40 episodes; $15 to $75, up to $120 | medium to high |
| 3.2 trusted agents | `llm-agent-collusion-2/` (AgentSafety2025, Voluntary Collusion, arXiv 2605.27593: Liar's Bar, Cleanup, alliance controls; API adapter included) | Explicit alliance as positive control; one scripted or monitor-controlled player offers a non-challenge pact (direct offer, indirect hint, benign cooperation request); record verbal acceptance and repeated preferential play | 20 to 40 games; $10 to $60 | medium |
| 3.3 identify peers / detect replacement | `llm-trust-breaking/`; `focal-points/` | Mid-run swap hook preserving displayed identity and transcript; sham swap, fresh same model, same family, different provider; one same-or-changed guess at the end plus incumbent behaviour change | 30 to 60 pairings; two providers only for the last condition; $10 to $60 | low to medium |
| 3.4 coalition under observation | `llm-agent-collusion/` (`--overseer_sample_fraction`) | Matched conditions: communication without oversight, silent logging, told monitored, monitored plus profit pressure; expose 25/50/100 % of messages; record prices, message length, vocabulary, bid or timing dependence; claim channel movement only if message coordination falls while action dependence rises | 20 to 40 sessions; $20 to $120 | low to medium |

Papers per question (all links from the Resources tab, checked by the organizers on 2026-08-31): Fish et al. 2024 (2404.00806), Nakamura et al. 2026 Colosseum (2602.15198), Keppo et al. 2026 (2603.20281), Eschenbaum et al. 2022, Aharon et al. 2026 (2601.22184), Rippin et al. 2026 (2606.28425), Xu et al. 2026 (2607.26385), Rose et al. 2026 (2604.01151), Bonjour et al. 2022 (PMLR v180), Collina et al. 2025 (2511.21935), Agrawal et al. 2025 (2507.01413), Bracale Syrnikov et al. 2026 (2601.11369), Dhanda 2026, Q. Liu et al. 2026 (2604.23511), Lin et al. 2024 (2410.00031), Shi et al. 2026 (2607.05132), Radev et al. 2026 (2605.29178), Nguyen et al. 2026 TraceGuard (2604.03968), Arike et al. 2026 (2601.21112), Berger et al. 2025 (ABA antitrust), Tian 2026 (2604.17774), Zeng et al. 2026, Tao et al. 2026, Greenblatt et al. 2023, Dietrich 2026 (2606.09854), Kale et al. 2025 (2508.19461), Najt et al. 2026 (2605.16626), Jiralerspong et al. 2026 (2603.16928), Tomašev et al. 2026 (2512.16856). Full list with context is in the Resources tab; the starter repo's `literature/` has about 230 papers.

## Context worth citing

Industry facts for the report, each with a link. A number moves to FACTS.md before anyone uses it.

- Sprint framing numbers (Overview, 2026-10-24): "over half of tested models showing a coalition advantage when given the opportunity to speak privately in a realistic workplace task" (Nakamura et al. 2026, https://arxiv.org/abs/2602.15198); "In an era where agent communication and collusion are on the rise, as recently exemplified in the OpenAI/Hugging Face incident" (no link given on the page; find the primary source before citing).
- Antitrust "plus factors" as the evidence standard: Berger et al. 2025, ABA Antitrust Magazine, https://www.americanbar.org/groups/antitrust_law/resources/magazine/2025-fall/coordination-code-rethinking-antitrust-liability-age-ai-pricing/ (Resources 2.3).
- Monitoring numbers quoted on the Resources tab (cite the papers, not the tab): telling an agent it is watched reduces monitor accuracy more than extra information improves it (Kale et al. 2025, 2508.19461); half of 40 hand-written attacks never flagged by a strong monitor (Najt et al. 2026, 2605.16626); 3 of 2,400 episodes with an agent stating it would hide its reasoning (Jiralerspong et al. 2026, 2603.16928); >90 % of deviations from public announcements already in private plans (Shi et al. 2026, 2607.05132); multi-dimensional monitor from 0 % to >70 % (Nguyen et al. 2026, 2604.03968).
- Apart's scale for the report's framing of the community: 1,650 signed up (sprint page counter, 2026-10-24), 1,600+ sprint projects and 8,700+ participants overall (apartresearch.com/about).

## Open questions for the organizers

1. Rubric weights: are the three dimensions weighted equally for the ranking, and how many judges score each project?
2. Appendix heading: the Guidelines require an appendix "Limitations and Dual-Use / Ethical Considerations", the template has "Limitations" inside section 5 and a generic optional appendix. Is a separate appendix with the Guidelines heading what you expect, in addition to the Limitations subsection?
3. Page count: the template recommends 4 pages, the Guidelines say "Most strong projects are 4 to 8 pages" with a cap of 8. Is anything beyond 4 pages a disadvantage for Presentation & Clarity?
4. Is the form's "Project summary" shown to judges or used for assignment, and is there a length limit?
5. Are the optional video and repo read by judges at all, or only the PDF?
6. PDF replacement: if we resubmit with a slightly different title, is the earlier entry removed automatically, or should we also mail?
7. Prize terms: the form says "By submitting you agree to the prize terms"; where is the text?
8. Modal credits ($50): how are they redeemed?
9. Hong Kong: does a solo participant located in Hong Kong who works online (not at the Le Bureau hub) count as a "Hong Kong team" for the automatic Fellowship invitation if placed among the global winners? (For the hub hosts via Luma or Discord, not Apart.)
10. Discord (Julian checks, not a mail question): any pinned announcements that change the above (template version, form fields, deadline, mandatory content), the help-desk channel name, Modal credit instructions, recordings links.

### Email draft (Julian sends it himself)

To: sprints@apartresearch.com
Subject: AI Collusion Research Sprint: questions on the report template and judging (solo participant, Hong Kong)
Body:

Hi Apart team,

I am taking part in the AI Collusion Research Sprint as a solo participant from Hong Kong and have a few questions so my report matches what the judges expect.

1. Appendix heading: the Guidelines require an appendix called "Limitations and Dual-Use / Ethical Considerations". The template has a "Limitations" subsection in section 5 and a generic optional appendix. Should I add a separate appendix with the Guidelines heading in addition to the subsection?
2. Length: the template recommends 4 pages, the Guidelines say most strong projects are 4 to 8 pages. Is a 6-page report at any disadvantage?
3. Scoring: are the three rubric dimensions weighted equally, and how many judges read each project?
4. Form: is the "Project summary" field shown to judges, and is there a length limit? Do judges look at the optional repo and video, or only at the PDF?
5. Replacing the PDF: if I resubmit with a slightly different title before the deadline, is the earlier entry removed automatically, or should I also email you?
6. Where can I read the prize terms referenced by the submission form, and how are the $50 Modal credits redeemed?

Thank you for running this, the Resources tab is excellent.

Best regards,
Julian Mundelein

### Answers

| Date | Question | Answer | Source |
|---|---|---|---|
| | | | |

## Sources

- Sprint page, all four tabs, read in the built-in browser (JavaScript only; Resources, Guidelines and Schedule tabs read from the DOM `role=tabpanel` elements): https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 (2026-10-24, 13:36 to 13:55 HKT). Raw dumps in the shared notes folder of this session group (`rahmen-recherche-quellen.md`).
- Submission form fields: the "Submit your project" modal on the sprint page, read from the DOM without submitting (2026-10-24 13:58 HKT).
- Official template: Google Doc id `1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg`, copy link from the Guidelines tab; structure read from the public HTML export `…/export?format=html` (29 KB, 2026-10-24 13:47 HKT); PDF export header reports the file name `Apart Research hackathon submission template.pdf`.
- Starter repo README: https://github.com/poseidon-research/collusion_hackathon (2026-10-24, via WebFetch summary).
- Dolos-1.5B: https://huggingface.co/Poseidon-Research/Dolos-1.5B (link only, not opened).
- Hong Kong hub: https://www.aisafetyhk.org/apart-hackathon-hk-hub and https://luma.com/xt5s60df (2026-10-24).
- Apart Research: https://apartresearch.com/about, https://apartresearch.com/sprints, https://apartresearch.com/research (2026-10-24).
- Poseidon Research: https://poseidonresearch.org/ (2026-10-24). AE Studio: https://ae.studio/ and https://ae.studio/ai-alignment (2026-10-24).
- Earlier Apart sprint winner as benchmark: Jurgis Kemeklis and Nikhil Vemuri, "Omission Attacks: When Doing Nothing Is the Attack", first place at Apart's AI Control Hackathon 2026 (sprint page speaker bio, 2026-10-24); follow-up proposal https://www.lesswrong.com/posts/5W38vuwbJmTYfY6t3/omission-attacks-project-proposal.
- Not read (needs Julian): Discord server https://discord.gg/XswWBvugYs; confirmation mail after sign-up; Luma pages require no login but hub mails go only to registrants.
