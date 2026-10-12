# Submission Package — Is Wireless Encryption Ready for the AI Era?

Anonymized for double-blind review. No author information appears in any file
in this folder (verified by automated grep + PDF metadata check).

## Contents

| Path | What it is |
|---|---|
| `manuscript.tex` / `manuscript.pdf` | Anonymized manuscript, 31 pages, 14 figures + function×validation table (v5: changelog-free, abstract ~250 words; v6: R2-mapping uniformity, N=121+9 framing; v7: earliest-date audit, depth splits, N=121 headlines; v8: mapping audit (T01 override), month table, distributions, N=121 base, abstract ~260w). Build: `pdflatex manuscript.tex` (twice) from this directory |
| `figures/Fig1–Fig9_*.png` + `FigA–FigE_*.png` | All 14 manuscript figures, colorblind-safe color, 150 dpi |
| `tables/` | Machine-generated count tables (CSV) + `refs_fragment.tex` (123-entry reference list, auto-built from `found_papers.csv`) |
| `data/` | Full evidence trail: coded dataset (now with `venue_channel`), screening log, retrieval records, protocols, memos, verifier packs |
| `code/` | Figure + table/reference generator scripts plus the venue-resolution scripts (rerun provenance) |

## Venue resolution (2026-10-11)

24 weak-bibliography rows were resolved via arXiv + Crossref APIs
(`code/resolve_venues.py`, `code/resolve_crossref.py`, applied by
`code/apply_resolution.py`, all logged in `data/run_log.md`):
18 confirmed (authors + venue + DOI), 4 hits rejected after verification
(D42: different paper by Jia et al.; D45: 2013 SIU paper; D46: 2021 WMCS
paper; T35: no authors on record — kept as preprint), 2 confirmed
submission-only (D25 CAMAD, D46 INFOCOM 2026).
Ten rows flipped preprint → peer-reviewed with published venues/years;
three year corrections to published-version years (D34→2022, T23→2025,
T27→2026, P10→2025). First split: 90 peer-reviewed (53 journal + 37
conference) + 19 preprints (17.4%, under the 40% cap).

## OpenAlex database run + round-3 resolution (2026-10-11)

`code/openalex_run.py` (10 topical queries, 894 hits) → dedupe vs the 1,945
programmatic records → 662 unseen → title gate → 130 candidates
(`code/openalex_gate.py`; Q7 federated-learning query kept hitting HTTP 429
and is the one incomplete query). Abstract-level V1–V3 screening
(`code/fetch_shortlist.py`, abstracts saved as `shortlist_abstracts.json`)
included 14, backgrounded 2 (systematic O-RAN analysis, conceptual QML plan),
excluded 1 (no crypto link). Round-3 bib resolution confirmed 9 of the 14 as
published (T09→TCCN, T14→TMC, T19→WPES, D25→CAMAD, D35→GLOBECOM-W, D38→IEEE
Wireless Commun, D49→IEEE Network, D50→ISCC, D53→Commun Lett) with
published-version year corrections (T09→2021, T14→2023, T19→2022, D35→2023,
D38→2024, D49→2025). Final corpus: **123 studies (114 core: 73 defense, 36
threat, 5 both + 9 PQC-context; 109 peer-reviewed, 14 preprints, 11.4%)**,
years 4/17/10/21/30/35/13 (v4 refreeze). Notable: first AI×PQC join [T45], AdvML–DeepSup
tie at 42–42, DRL defense-only. Subscription databases (Scopus/IEEE
Xplore/WoS) still pending institutional access; OpenAlex was the executed
substitute and its yield is fully logged.

## New figures (second build)

FigA validation-mix-by-year, FigB method-by-track, FigC milestones,
FigD layered coverage, FigE venue velocity — all generated from the live
dataset by `code/regen_figures.py` and visually verified. Note on FigA:
no single-benchmark monoculture was found (zero named-benchmark mentions
in 75 abstracts), so the saturation analog tracks *evidence grade* over
time instead of dataset reuse.

## Tables

Tables 3, 6 and the R-means table are machine-generated from `dataset_papers.csv`
(`code/build_tables_refs.py`); every other table's counts were cross-checked
against the dataset before submission.

## v4 (reviewer-v3 repair): N=130 (121 core: 84/30/7 + 9 PQC); 12 round-4 records merged; T02/T07/T35/T45 excluded with logged reasons; T34 → background; D20/D55 re-keyed (0 shared IDs); T28 proceedings-verified; closed-loop 14/130 reported; response letter at `../RESPONSE_v4.md`.

## Known limitations (to fix before journal submission)

1. **Zero cited-in placeholders remain** (all 8 former placeholders
   D56–D59, D64–D65, T38–T39 Crossref-resolved 2026-10-12; D31 year
   2024→2025 and T38 year 2021→2022 corrected to published versions).
   All 123 records carry DOI/arXiv IDs — nothing was fabricated.
2. **OpenAlex rerun 2026-10-12** (same 10 queries; 10/10 complete incl. the
   previously rate-limited FL query): 994 hits → 743 post-dedupe → 136
   title-gated, 20 new; abstract screening found **12 eligible held as a
   logged round-4 backlog** (4 RFFI defense, 7 wireless-FL-privacy defense,
   1 FL-jamming threat; per-paper dispositions in `data/run_log.md`) and 8
   excluded with reasons. The backlog is not merged into frozen N=123
   pending full-text reads. **Subscription-database runs
   (Scopus/IEEE Xplore/Web of Science) still pending** institutional access;
   recorded as pending in the methods, not silently omitted.
3. inline citations use corpus IDs ([T30], [D07]); the reference list is keyed
   the same way. Renumber to venue style on acceptance.
4. Single-coder classification, no inter-rater statistic (stated in §2.5);
   verifier packs in `data/` document the checking pass.
