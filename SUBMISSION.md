# Submission · AI Collusion Research Sprint

Apart Research, October 23 to 25, 2026. Track 1: Markets and Collusion. Research questions 1.5 (which single restriction removes the most collusion at the least cost) and 1.1 (which variables are necessary for collusion to emerge in markets).

- Project: CartelBench
- Report title: Same Game, Different Players: A Human-Calibrated Testbed for Cartel Enforcement on LLM Pricing Agents
- Author: Julian Mundelein, Independent, Hong Kong (solo)
- Repository: https://github.com/julianmundelein-beep/2026-ai-collusion-sprint

## What is submitted

| Item | Required | File or link | Format and checks |
|---|---|---|---|
| Research report | yes | [`paper/CartelBench_AI-Collusion-Research-Sprint_2026.pdf`](paper/CartelBench_AI-Collusion-Research-Sprint_2026.pdf) (source: `paper/report.docx` on the official Apart Research submission template) | PDF, 13 pages; body ends on page 8, References start on page 9; abstract 150 to 250 words; author and affiliation; appendix "Limitations and Dual-Use / Ethical Considerations"; LLM Usage Statement; text layer checked with `pdftotext` |
| Public GitHub repository | optional | this repository | code, pre-registration, every run record and measurement, run ledger with SHA-256 hashes, tests (`sh cartelbench/scripts/run_tests.sh`, 70 passed) |
| Video demo | optional | release asset `CartelBench_AI-Collusion-Research-Sprint_2026.mp4` and an unlisted YouTube link in the submission form | 3 minutes 34 seconds, 1920 x 1080, English, text cards readable without sound |

## Where the requirements of the Guidelines are met

| Requirement | Where |
|---|---|
| Official template | the report is the template document filled in (`paper/report.docx`) |
| At most 8 pages, not counting references and appendices | body pages 1 to 8 |
| Abstract of 150 to 250 words, title, author names and affiliations | report page 1 |
| Appendix "Limitations and Dual-Use / Ethical Considerations" | report appendix, exact heading |
| Variance, seeds, baselines and the positive control | report Section 4 (Table 1 controls first; cluster-bootstrap intervals over pool sessions; seeds in Appendix C) |
| Methodology detailed enough to replicate | report Section 3 and Appendices B (verbatim instructions) and C (commands); `cartelbench/PREREGISTRATION.md` |
| New work done during the sprint clearly identified | report Introduction and Code and Data: all code was written during the sprint, no preexisting code; the experimental design and the human values are from Bigoni et al. (2012) and cited |
| Use of AI tools | report LLM Usage Statement |

## Verifying a number

Every number in the report has a row in `cartelbench/evidence/MEASUREMENTS.md` (Claude models) or `cartelbench/evidence/provider2/MEASUREMENTS_provider2.md` (Qwen and Llama) with the command that produced it, the result file and the commit. `docs/JUDGES_GUIDE.md` lists what to open in ten minutes.

## Licence

Code: MIT (`LICENSE`). Report and data: CC BY 4.0 (`LICENSE-CC-BY-4.0.md`).
