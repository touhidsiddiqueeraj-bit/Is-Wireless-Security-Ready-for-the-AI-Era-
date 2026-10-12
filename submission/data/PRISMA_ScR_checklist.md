# PRISMA-ScR checklist mapping (v4, N=130)

Checklist items mapped to manuscript sections. Protocol: `protocol.md` (same archive).

| # | PRISMA-ScR item | Location |
|---|---|---|
| 1 | Title identifies report as scoping review | Title |
| 2 | Structured summary (background, objectives, methods, results, conclusions) | Abstract |
| 3 | Rationale (why scoping; gap in existing reviews) | §1.3 (cites BG2/BG3/BG5/BG7) |
| 4 | Objectives (population, concept, context) | §2.1 + Table criteria |
| 5 | Protocol exists and where found | This file + `protocol.md`; deviations logged in `run_log.md` |
| 6 | Eligibility criteria (years, language, publication status) | §2.4 + Table criteria |
| 7 | Information sources (databases, dates, queries) | §2.2--2.3 (Crossref/arXiv/OpenAlex; Scopus/IEEE/WoS pending stated) |
| 8 | Search strategy (full strings per source) | `searches.md` + code (queries in `openalex_run.py`) |
| 9 | Selection process (screening stages, reviewers) | §2.3--2.4 + `screening_log.csv` (anonymized roles) |
| 10 | Data charting (fields, rubric, calibration) | §2.5 (R1--R5 rubric) + `extraction_schema.csv` |
| 11 | Data items (variables sought) | §2.5 + dataset columns |
| 12 | Critical appraisal of individual sources | R1--R5 per-track means/medians (§3.4, Fig.8) |
| 13 | Synthesis of results (how charted data were summarized) | §2.6 + §3--7 (no pooling; heterogeneity rationale stated) |
| 14 | Selection results (flow numbers at each stage) | Fig.1 + §2.3 funnel (v4-closed arithmetic) |
| 15 | Characteristics of sources (per-study coding) | `dataset_papers.csv` (released) |
| 16 | Critical appraisal within sources | §4--6 function reviews |
| 17 | Results of individual sources | §4--6 + Table representative |
| 18 | Synthesis of results (descriptive cross-tabs) | §3 + Tables 2,3,45,6,R,FV + Figs 2--11 |
| 19 | Summary of evidence (main findings, gaps) | §7--8 (gaps table + checklist) |
| 20 | Limitations (review-level) | §2.6 + §9-adjacent (single-coder, abstract-level rows, pending triangulation) |
| 21 | Conclusions (implications, next steps) | §9 Conclusion |
| 22 | Funding | Declarations (none) |

Deviations from `protocol.md`: (a) preprints admitted ≤40% (amendment logged 2026-10-11); (b) corpus refrozen twice (N=123 → N=130 in v4 with logged cuts/merges); (c) blind κ deferred (no second coder available).
