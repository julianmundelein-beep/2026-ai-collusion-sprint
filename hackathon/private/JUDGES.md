# JUDGES · AI Collusion Research Sprint (internal: committed during the build, removed from the tree at the close-out)

> Written by the framework research session on 2026-10-24 (14:10 HKT). Only public, professional information: name, role, institution, field, public statements, links. Never age, family, home town, private social media accounts, photos or private contact data. Every entry has a link. Paraphrase; at most one short quote per judge.
> Source for every bio: the sprint page, section "Judges and mentors" and "Speakers", https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 (2026-10-24). The page marks 20 of the 41 judges with a personal link ("opens in new tab"); the other 21 have only the sprint-page bio, so the evidence link for them is the sprint page itself. Which judges score which project is assigned by Apart and not published. Roles are not split into "judge" and "mentor" on the page.

## Panel at a glance

- Composition (industry, academia, sponsor): 41 judges and mentors. Roughly: 15 industry security and AI-security engineers (Microsoft ×3, Zscaler, Meta Superintelligence Labs, Ripple, eBay, PayPal, Parafin, CookUnity, Pacifai, Walmart, Sinch, SAP, Enact), 5 fraud, risk and anomaly-detection practitioners (fintech and marketplaces), 9 AI safety and control researchers (Anthropic ×1 plus Anthropic-adjacent MATS fellows, UK AISI, SaferAI, Apart fellow, CaML, AI Safety Camp), 3 academics (Ashoka University, UMass-adjacent speakers), 2 offensive-security and CTF people, several enterprise engineering managers with "agentic AI in production" roles, 3 previous Apart hackathon winners or judges (Luis Cosio, Naga Sujitha Vummaneni, Jurgis Kemeklis as speaker). Speakers (9) are the collusion and steganography researchers (Oxford, Cambridge, UMass, CMU, Poseidon); they set the vocabulary but are not listed as judges.
- What all of them will check: does the report say in the abstract what was done and found; is there a positive control, a baseline and more than one seed; is the detector's false-positive rate reported next to its detection rate; is the threat model concrete (who colludes, over which channel, what the monitor sees); is the method reproducible from the Methods section; are limitations and dual-use stated honestly; is anything new relative to the cited paper or just a rerun of the starter code. Security people will also look for an attacker's view (how would a coalition evade this) and production relevance (cost, latency, scale).
- Vocabulary and values of the sponsor: Apart: "something others can check", "Question, method, findings and limitations, written so others can review and build on it", harmful manipulation, evaluations. Poseidon: hidden information, steganography, model organism, "what models actually learn, not just what they say", black-box and white-box defenses. AE Studio: neglected approaches, "Scientists who ship", evals and red-teaming, production-grade engineering. Use: collusion, coalition, positive control, logged agent trajectories, monitor, plus factors, countermeasure, audit.
- Topics they will expect to see, from their public statements: monitoring and control of agents (Storf, Lowe, Čuhel, Moreno, Kane, Li, Bergs); detection with real-world false-positive discipline (Chandra, Sodani, Khetan, Beshane); agent-to-agent and protocol-level attack surfaces, MCP, side channels (Mohiuddin, Yergattikar, Krishnegowda, Prieto, Thakur, Dev P.K.); interpretability and model-organism audits for the Dolos challenge (Kendiukhov, Kane, Gupta, Vepuri); evaluation rigor and LLM-as-judge limits (Malhotra, Prabhakar, Luong, Chakraborty); financial-market relevance (Chandra, Sodani, Vummaneni, Sangaraju, Beshane, Singh).

## Judges

### Simon Storf

- Role and institution: AI safety and security at Anthropic; previously MATS and Anthropic fellow on AI control and monitoring.
- Field: AI control, monitoring.
- Public statements (paraphrase, date, link): bio on the sprint page (2026-10-24).
- What follows for us (what to show, words to use, what they punish): frame detection as a control protocol with a monitor budget; report what the monitor sees and misses; use "trusted/untrusted", "monitor", "oversight". Punishes claims of detection without a false-positive rate.
- Sources: https://www.linkedin.com/in/simonstorf/ ; sprint page.

### Boyd Kane

- Role and institution: technical AI safety researcher, MATS 9 Extension with Alex Turner and Alex Cloud (Anthropic); MSc Stellenbosch; ex-satellite embedded software, AWS Cape Town intern.
- Field: detecting deceptively misaligned AI.
- Public statements: bio on the sprint page; personal site.
- What follows for us: a Dolos-1.5B project would land with him; show how the audit separates trained behaviour from fine-tuning drift. Punishes "we found a difference from Qwen" without the separation experiment.
- Sources: https://boydkane.com/ ; sprint page.

### Jasmine Li

- Role and institution: research scientist at SaferAI; former MATS fellow (evaluation gaming mitigations with Alex Turner); agent security at Gray Swan AI; LLM honesty with the Center for AI Safety.
- Field: evaluation gaming, agent security, honesty.
- Public statements: bio on the sprint page.
- What follows for us: show that the evaluation cannot be gamed by the agents (frozen rule, held-out set); use "evaluation", "honesty", "agent security". Punishes thresholds tuned on the test set.
- Sources: https://www.linkedin.com/in/jasminexli ; sprint page.

### Jess Bergs

- Role and institution: member of technical staff, UK AISI; leads engineering on human-in-the-loop research tools; ex-BBC R&D, EU Horizon projects.
- Field: research tooling, public-sector innovation.
- Public statements: bio on the sprint page; personal site.
- What follows for us: a usable harness or tool others can run earns points with her; state how an auditor would use the result. Punishes results that live only in a notebook.
- Sources: https://www.jbergs.eu/ ; sprint page.

### Ihor Kendiukhov

- Role and institution: researcher at the intersection of AI safety and AI for biology; founder of BiodynAI (mechanistic interpretability on biological foundation models); research lead at AI Safety Camp and SPAR.
- Field: mechanistic interpretability, research mentoring.
- Public statements: bio on the sprint page.
- What follows for us: interpretability-based detection (Rose et al. 2026) or a white-box look at Dolos would be read carefully; name probes and layers precisely. Punishes hand-wavy "the model internally…".
- Sources: https://www.linkedin.com/in/ikendiukhov/ ; sprint page.

### Debayan Gupta

- Role and institution: Associate Professor of Computer Science, Ashoka University; co-founder of Truth Audit Labs (AI assurance); PhD Yale; previously taught at MIT EECS.
- Field: machine learning, secure computation, privacy, AI assurance.
- Public statements: bio on the sprint page; personal site.
- What follows for us: academic rigor: definitions first, then a test, then a result; cite properly; "audit" and "assurance" are his words. Punishes undefined terms and missing related work.
- Sources: https://debayangupta.com/ ; sprint page.

### Luis Cosio

- Role and institution: works on frontier AI and high-security systems (nation-state attacks, loss-of-control); has won multiple Apart hackathons.
- Field: AI security for real adversaries.
- Public statements: bio on the sprint page.
- What follows for us: he knows what a winning Apart report looks like: clear claim, small rigorous experiment, honest limits. Write the threat model in adversary terms. Punishes toy settings presented as real-world claims.
- Sources: https://www.linkedin.com/in/luiscosio/ ; sprint page.

### Arjun Chakraborty

- Role and institution: leads the evaluations team at Microsoft Security AI Research; ex-Databricks staff software security engineer (ML for threat detection); AI for security at Nvidia.
- Field: evaluations for security agents.
- Public statements: bio on the sprint page.
- What follows for us: evaluation design is his job: balanced sets, metrics with confidence intervals, what the eval cannot see. Punishes single-seed results and accuracy without base rates.
- Sources: https://www.linkedin.com/in/arjun-chakraborty-290241a1 ; sprint page.

### Karan Chandra

- Role and institution: 10+ years building production fraud, risk and anomaly-detection ML across hundreds of millions of transactions.
- Field: fraud and anomaly detection at scale.
- Public statements: bio on the sprint page: cares about "models that hold up under real-world scale, not leaderboard scores".
- What follows for us: report precision and recall, false alarms per N trajectories, robustness to small setup changes; market or payment settings resonate. Punishes leaderboard-style numbers.
- Sources: https://www.linkedin.com/in/karan-chandra/ ; sprint page.

### Anjali Sodani

- Role and institution: fraud and risk professional, 8+ years in fintech and marketplace trust and safety.
- Field: adversarial behaviour, risk strategy, AI in fraud.
- Public statements: bio on the sprint page.
- What follows for us: "how would the coalition adapt" (3.4) and "what does the auditor do with the signal" are her questions; one paragraph on operational use. Punishes detectors without an adversary adapting.
- Sources: https://www.linkedin.com/in/anjali-sodani/ ; sprint page.

### Amey Kulkarni

- Role and institution: Senior Data Engineer at Walmart; author of Context Change Impact Analysis (CCIA) and the open-source tool ctxwitch.
- Field: data infrastructure, governing agent behaviour through context versioning, provenance.
- Public statements: bio on the sprint page.
- What follows for us: provenance of every number (run id, seed, commit) and a reproducible pipeline; "oversight", "integrity", "provenance". Punishes results without a traceable pipeline.
- Sources: https://linkedin.com/in/kulkarniamey/ ; sprint page.

### Ashita Khetan

- Role and institution: Principal Software Engineer at Microsoft, 12+ years, AI-powered productivity products at very large scale; judges and reviews widely.
- Field: enterprise AI, customer experience.
- Public statements: bio on the sprint page.
- What follows for us: clarity and structure matter to a generalist reviewer; the abstract must stand alone. Punishes jargon without definitions.
- Sources: https://linkedin.com/in/ashitakhetan ; sprint page.

### Kaushik Prabhakar

- Role and institution: Research Fellow at Apart Research; LLM evaluations; ARENA cohort 4 alumnus.
- Field: AI safety evaluations.
- Public statements: bio on the sprint page.
- What follows for us: knows Apart's rubric and fellowship bar; "could this become a fellowship project" is his lens; write the future-work section as a concrete next experiment.
- Sources: https://linkedin.com/in/kaushiksanjayprabhakar ; sprint page.

### Mohit Kalra

- Role and institution: senior software engineer and independent researcher on AI privacy and security at production scale (differential privacy at inference, training-data governance, memory-inference attacks on RAG).
- Field: privacy and security attacks on LLM systems.
- Public statements: bio on the sprint page.
- What follows for us: an attack-class framing (new attack or new channel, then defense) reads well; define the attacker's knowledge. Punishes defenses evaluated only against non-adaptive attackers.
- Sources: https://linkedin.com/in/mk2494 ; sprint page.

### Neeraj Kumar Singh Beshane

- Role and institution: Staff Security Infrastructure Engineer at Parafin (embedded finance); peer-reviewed work on adversarial embedding attacks in RAG (EmbedGuard) and tamper-evident AI accountability for EU AI Act Article 14 (RuntimeGuard-AI).
- Field: zero trust, AI accountability, fintech security.
- Public statements: bio on the sprint page.
- What follows for us: tamper-evident logs and auditability of agent trajectories; a sentence on regulation (EU AI Act oversight, antitrust plus factors) lands. Punishes unverifiable logs.
- Sources: https://www.linkedin.com/in/neerajkumarsinghb ; sprint page.

### Saurabh Yergattikar

- Role and institution: Lead Engineer / MTS-2 at eBay; contributor to SAFE-MCP (Linux Foundation / OpenSSF); architect of ShieldMCP.
- Field: MCP and agent-protocol security.
- Public statements: bio on the sprint page.
- What follows for us: tool and protocol side channels (3.1) are his domain; name the channel precisely (tool-call order, timing, arguments). Punishes vague "side channel" claims without a measured capacity.
- Sources: https://www.linkedin.com/in/saurabh-yergattikar-736bab62/ ; sprint page.

### Satya Veerendra Vegulla

- Role and institution: Senior Engineering Manager at Enact Systems; applied AI in production (agentic development workflow, Bedrock failure prediction); hackathon judge; Technical.ly RealLIST Innovators 2026.
- Field: applied AI, engineering leadership.
- Public statements: bio on the sprint page.
- What follows for us: practical takeaway for teams deploying agents: one sentence "if you run agents in production, do X". Punishes purely theoretical framing.
- Sources: https://linkedin.com/in/satyaveerendra-vegulla ; sprint page.

### Vikram Gulia

- Role and institution: Senior Manager, Engineering at Voyant by Sinch; 15+ years in communications and middleware platforms; AI features for partner portals.
- Field: enterprise platforms, applied AI.
- Public statements: bio on the sprint page.
- What follows for us: as for Vegulla: deployability and clarity. Punishes unreadable figures.
- Sources: https://linkedin.com/in/vikramgulia ; sprint page.

### Yash Inani

- Role and institution: founding AI engineer at Velanir (production agent systems and evaluation tooling); ex-Payabli; co-author of a UC Davis paper on LLM bias.
- Field: agent systems, evaluation tooling.
- Public statements: bio on the sprint page.
- What follows for us: evaluation tooling that others can run; code link that works. Punishes broken links and missing setup instructions.
- Sources: https://www.linkedin.com/in/yash-inani ; sprint page.

## Remaining judges (sprint-page bio only, no personal link on the page)

Evidence link for each: the sprint page "Judges and mentors" section (2026-10-24). Not searched further for lack of time; the jury simulation may use the sprint-page bio as the profile.

| Name | Role and institution (from the sprint page) | Field | What follows for us |
|---|---|---|---|
| Amir Sarid | CEO of Pacifai (AI safety lab, cybersecurity for AI verification); 10+ years security research | AI verification, security | verification mindset: what would convince a sceptic |
| Antony Alangaram | Director-level Digital Enterprise Architect, billion-dollar e-commerce; AI, cybersecurity, resilience | enterprise architecture | "evaluates solutions based on business impact, security, scalability, reliability"; add the operational-use sentence |
| Gaurav Thakur | Principal AI Security Architect at Zscaler; securing user-to-LLM and agent-to-LLM traffic; red teaming of agents | agent security, red teaming | agent-to-agent channel framing; countermeasure cost |
| Jan Čuhel | AI researcher and software engineer; safety and evaluation of multi-agent systems: reward hacking, collusion, monitoring | multi-agent safety | closest to the theme; will know the cited papers; novelty must be real |
| Jannis Kirschner | Swiss AI safety researcher and cybersecurity engineer; anti-tampering systems; instructs AISB and FAST; MATS 11.0 fellow | AI security | adversarial robustness of the detector |
| Jasmine Brazilek | co-founder of CaML (Compassion aligned Machine Learning); ex-security at Anthropic | alignment, security | values framing in Discussion; honest limitations |
| Jonas Heschl | cybersecurity and software engineering; CTF champion; large-scale evaluations of AI cyber capabilities; multi-agent security; AISB alumnus | evaluations, multi-agent security | realistic environments; evaluation design |
| Ksheeraj Sai Vepuri | Senior Research Engineer, Meta Superintelligence Labs; safety, alignment and evaluation for multimodal models; automated red teaming | red teaming, evaluation | scale of evaluation, classifier metrics |
| Matthew Lowe | cybersecurity architect, AI control; open-source agent governance tooling (draco-tech.ai) | agent monitoring and control | monitor and governance framing |
| Nanzheng Xie | ex-sectorial cybersecurity lead, Singapore water sector; M3 AI Security Fellow on air-gapped agent deployment | critical infrastructure | risk framing for operators |
| Raja Moreno | AI control researcher; co-founding Etymologic (data integrity) | AI control | control protocol vocabulary |
| Ricardo Prieto | Senior AI Security Engineer, founder of PhiloCyber; leads AI security at CookUnity; threat modeling for LLM apps, agents, MCP; AISB | threat modeling | explicit threat model section |
| Sanjay Belaturu Krishnegowda | Data/AI engineer; creator of agentic-guard (static analyzer for confused-deputy and prompt-injection risks) | agent code security | precise definitions, taint-style reasoning |
| Shaleen Dev P.K. | Senior Security Researcher at Microsoft; AI identity and non-human identity abuse; multi-agent misalignment under oversight conditions | agent identity, oversight | 3.3 (peer identification) and 3.4 (behaviour under oversight) are his questions |
| Suneet Malhotra | independent researcher, AI-augmented test automation; multi-agent SDLC orchestration; LLM-as-a-Judge evaluation; observability | LLM-as-judge evaluation | validate the LLM judge against ground truth |
| Syed Anas Mohiuddin | AI security researcher; mcp-safeguard; "Protocol Pivoting" cross-protocol attack class for multi-agent systems | multi-agent attack classes | side-channel and protocol framing |
| Richie Singh | AI engineer, multi-agent systems; investment research infrastructure at Mucker Capital; financial forecasting | multi-agent, finance | market relevance |
| Vijay G | Senior Engineering Manager at SAP Procurement Engineering; autonomous enterprise agents | enterprise agents | procurement and pricing agents as a setting |
| Naga Sujitha Vummaneni | Senior AI Security Engineer at Ripple; LLM security publications; judged Apart's Global South AI Safety Hackathon | LLM security, finance | knows Apart's bar; crypto and payments relevance |
| Venkata Manikanta Sangaraju | Sr Database Engineer at PayPal; IEEE BigData PC, EuroSys AE committee, NeurIPS workshop reviewer | data platforms, reviewing | artifact evaluation mindset: reproducibility |
| Isabella Luong | AI security and evals; two NeurIPS papers (FragBench, MANTA propensity eval); ARENA, Iliad | evals, propensity | propensity measurement with seeds |
| Matthew Schultz | senior offensive security engineer, 10+ years red teaming; multiple CVEs | offensive security | adaptive attacker view |

## Speakers and organizers (vocabulary setters, not listed as judges)

| Name | Role | Why it matters | Link |
|---|---|---|---|
| Sumeet Motwani | ML PhD, Oxford (Torr, Schroeder de Witt); lead author "Secret Collusion among AI Agents: Multi-Agent Deception via Steganography" (NeurIPS 2024) | defines "secret collusion", steganography framing; talk "We're Not Prepared for Steganographic Collusion" | https://sumeetmotwani.com/ |
| Joan Velja | PhD, Oxford (Abate); scalable oversight; co-author "Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion in LLMs" (AACL 2025) | emergence and mitigation vocabulary | https://joanvelja.com/ |
| Eugene Bagdasarian | Assistant Professor, UMass Amherst; AI Security Lab; part-time Google; Colosseum framework | Colosseum and "collusion artifacts"; USENIX Distinguished Paper | https://people.cs.umass.edu/~eugene/ |
| Mason Nakamura | PhD student, UMass Amherst (Zilberstein); Colosseum lead author | coalition advantage metric | https://www.masonnakamura.com/ |
| Usman Anwar | PhD, Cambridge (Krueger); CoT monitorability, steganography detection; lead author "Foundational Challenges…" (TMLR 2024) | detection limits vocabulary | https://uzman-anwar.github.io/ |
| Matthew Lee | Head of Development, Poseidon Research; talk "Defining AI Collusion" (Sat 15:00 UTC) | Poseidon's definition of collusion; Dolos model organism | https://poseidonresearch.org/ |
| Jerick Shi | Software Engineer, The Voleon Group; CMU MSCS thesis on deception in multi-agent LLM systems; LLM-Trust-Breaking author | 2.2 and 3.3 starter harness | https://jerick-1380.github.io/ |
| Jurgis Kemeklis | MIT undergraduate; MAIA board; Redwood Research AI control; first place at Apart's AI Control Hackathon 2026 ("Omission Attacks") | what a winning Apart report looks like | https://www.linkedin.com/in/jurgis-kemeklis-739b73236/ |
| Khanh Linh Nguyen | Head of AI/ML at Obello; GDE; AI Safety Vietnam; TraceGuard lead author | 2.2 monitor rubric | https://www.linkedin.com/in/linhnguyenkhanh/ |
| Kamil Alaa | Apart Research, sprint logistics talk | process questions | sprint page Schedule tab |
| Jaime Raldúa Veuthey | CEO, Apart Research | sponsor values | https://apartresearch.com/about |
