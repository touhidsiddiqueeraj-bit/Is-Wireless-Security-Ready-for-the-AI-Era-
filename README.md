# Is Wireless Security Ready for the AI Era?

**A Structured Scoping Review and Classification of 130 Studies, 2020–2026**

Repository for the systematic/scoping review manuscript, its coded dataset, evidence trail, and the code that regenerates every table and figure from the data. The submission package is anonymized for double-blind review.

> **Headline answer (research literature):** *no* — defenses optimize accuracy while threats demonstrate exploits, and readiness evidence trails accuracy claims.

## Corpus at a glance

| | |
|---|---|
| Total classified | **130 studies** (2020–2026) |
| Core | **121** — 84 defense · 30 threat · 7 dual attack+defense |
| Context stratum | 9 post-quantum (PQC) studies, kept separate |
| Peer-reviewed vs preprint | 111 peer-reviewed (65 journal + 46 conference) · 19 preprints (14.6%) |
| Key findings (on the 121 core) | Authentication/RFFI absorbs **57.0%** · verified artifacts **3.3%** · preprints **14.9%** · closed-loop evaluation **11.6%** |
| Validation mix | Unclear 32 · Collected 26 · Simulation 20 · Analysis 6 · Testbed/OTA 46 |
| Manuscript | `submission/manuscript.pdf` — 32 pages, compiles clean (0 errors / undefined / overfull) |

All counts are machine-derived from `dataset_papers.csv` (duplicated at `submission/data/dataset_papers.csv`); nothing in the paper is hand-typed.

## Repository layout

```
.
├── manuscript.pdf            # working draft PDF (root copy)
├── draft_paper.md            # markdown draft of the paper
├── figures/                  # draft-stage figures (SVG + PNG)
├── retrieval/                # raw API records: arXiv XML, Crossref JSON, logs
├── submission/               # ← the actual submission package (anonymized)
│   ├── manuscript.tex/pdf    #    32-page LaTeX manuscript
│   ├── README.md             #    submission-package notes + revision history
│   ├── figures/              #    Fig1–Fig9 + FigA–FigE (14 figures, 150 dpi)
│   ├── tables/               #    machine-generated count tables (CSV) + refs_fragment.tex
│   ├── data/                 #    full evidence trail (see below)
│   └── code/                 #    generation + verification scripts
├── dataset_papers.csv        # coded dataset (root copy; same as submission/data/)
├── screening_log.csv         # PRISMA screening decisions
├── found_papers.csv          # bibliography records (drives the reference list)
├── protocol.md, searches.md, selection_criteria.md   # a priori protocol
├── run_log.md                # chronological audit log of every decision
├── RESPONSE_v4.md            # reviewer response letter
├── AGENTS.md                 # phase-by-phase repair log (v1→v8)
└── .gitignore                # LaTeX artifacts, __pycache__, 3rd-party publisher PDFs
```

### Evidence trail (`submission/data/`)

`dataset_papers.csv` (per-study coding: function, method family, data source, validation, readiness, venue channel, first-publication year…), `screening_log.csv` (include/exclude at every screening stage), `found_papers.csv` (bibliography with DOI/arXiv IDs — **0 fabricated records**), `protocol.md` / `searches.md` / `selection_criteria.md`, `PRISMA_ScR_checklist.md`, `fulltext_reads.md`, `verifier_pack.csv` / `verifier_rescore.csv` (verification pass), `glossary.md`, and `run_log.md` (complete decision history incl. the OpenAlex runs and round-4 backlog).

## Reproducing the results

Requirements: `python3` (standard library only for the checks below) and `pdflatex`.

```bash
# 1. Consistency gate — every headline count vs. the dataset
python3 submission/code/check_consistency.py
#    → "CONSISTENCY OK: N=130 tracks {defense:84, threat:30, both:7, pqc-context:9} ..."

# 2. Regenerate all tables + the reference fragment, then all figures
cd submission/code
python3 build_tables_refs.py     # tables/Table*.csv + tables/refs_fragment.tex
python3 regen_figures.py         # figures/Fig*.png
cd ../..

# 3. Build the manuscript (twice for cross-references; expect zero warnings)
cd submission && pdflatex manuscript.tex && pdflatex manuscript.tex
```

`check_consistency.py` asserts corpus size, track/year/channel distributions, zero cited-in placeholders, zero shared IDs between the dual-keyed records, the R2-mapping rule, depth splits, and the Table 3 counts. Run all three before any edit is presented.

## What the review codes

Each included study is coded along explicit axes:

- **Function** — authentication/RFFI, key generation, anti-jamming, protocol/traffic analysis, federated privacy, classifier-as-boundary
- **Method family** — deep supervised ML, adversarial ML, reinforcement learning, classical ML, LLM-assisted, non-learned baseline
- **Data source** — Unclear / Collected / Simulation / Analysis / Testbed-OTA
- **Validation depth** — Standard, Sim-only, Benchmark, Testbed-demo, Cross-domain
- **Readiness (R1–R5)** — threat-model statement, real-adversary evaluation, cost on constrained radios, reproducibility, standards alignment
- **Venue channel & dates** — journal vs conference; first-publication year (earliest-date audited)

Scope: radio-link security under AI-capable adversaries — authentication/RFFI, PHY key generation, anti-jamming, classifier-as-boundary analysis, federated-learning privacy — plus a separate PQC-migration stratum.

## Known limitations (stated in the paper, not hidden)

1. **Single coder, no inter-rater statistic.** No second human coder was available; no κ is invented. §2.5 discloses this and a corrective verifier pass is documented in `submission/data/verifier_pack.csv`. A second-coder κ step is required before journal submission.
2. **No subscription-database access.** Scopus / IEEE Xplore / Web of Science runs are pending institutional access. OpenAlex was the executed substitute (10 queries, fully logged); its recall limit is reported in the methods.
3. **Round-4 backlog not merged.** 12 eligible candidates from the 2026-10-12 OpenAlex rerun are held pending full-text reads (8 further excluded with reasons); N is frozen as reported.
4. **Some rows remain "Unclear."** 30 paywalled rows stay unclear without full-text reads — flagged as a limitation rather than guessed.
5. **Inline citations use corpus IDs** (`[T30]`, `[D07]`); renumber to venue style on acceptance.

## Excluded from this repository

Third-party publisher PDFs used as background reading (`1-s2.0-*.pdf`, `ML-BMS-Review.pdf`) are git-ignored — they are copyrighted elsewhere and are not ours to redistribute. LaTeX build artifacts (`*.aux`, `*.log`, `*.out`) and `__pycache__/` are ignored as well.

## Provenance

- Every included record carries a DOI or arXiv ID; **0 cited-in placeholders, 0 fabricated IDs**.
- Bibliography resolution (Crossref + arXiv + OpenAlex passes) and every inclusion/exclusion decision are logged in `run_log.md`.
- Revision history v1→v8 (reviewer-response repairs) is tracked in `AGENTS.md`; the reviewer response letter is `RESPONSE_v4.md`.

