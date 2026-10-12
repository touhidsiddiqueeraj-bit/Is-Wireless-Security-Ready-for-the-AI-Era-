# AGENTS.md — Major-Revision Repair Log (N=123 corpus)

Scope decision (user, plan-mode): **retitle to broader wireless-ML security** to retain T42/T44/T45/T46.
Live truth source: `dataset_papers.csv` (N=123) + `found_papers.csv`. All counts regenerated from dataset.

## Progress
- [x] 2026-10-12 — Plan audit; scope=retitle; AGENTS.md created
- [x] Phase 0 — check_consistency.py passes (N=123, 8 cited-in, 2 dup-DOIs disclosed)
- [x] Phase 1 — retitle to Wireless Security + criterion-(ii) adjudication (T42/T44/T45/T46 kept with caveats)
- [x] Phase 2 — §2 methods (funnel disposition, coder identity, OpenAlex recall, 13%→4.1% dual defined)
- [x] Phase 3 — fragility/overclaim fixes (tie artifact, 18 thru 2023, 29/42 RFFI, domain-shift surface, plurality-not-norm, P05 exception, T01/T28 corrected)
- [x] Phase 4 — references disclosed (8 cited-in, D55/T15 + D20/T20, D31/D40 flagged, preprint 12+2=14)
- [x] Phase 5 — stale-number sweep (track/year/method/venue/data/valid/R-means/captions) + regen tables/figs
- [x] 2026-10-12 — Table rows shortened; last Overfull on line 130 cleared; zero-warning compile 29 pages
- [x] 2026-10-12 — check_consistency.py OK; build_tables_refs.py OK (Table2/3/45/6/R + refs N=123)
- [x] 2026-10-12 — USER REQUESTED STOP: no further work after this AGENTS.md update
- [x] 2026-10-12 — Journal hardening resumed (user: go): 8 cited-in → 0 (Crossref DOIs), D31 2024→2025 + T38 2021→2022 year fixes, OA pass 33→30 Unclear (T05/D76/P11; D33 kept per prior full-text read), single-coder disclosure hardened (no κ invented), OpenAlex rerun 994 hits → round-4 backlog (12 eligible held, 8 excluded, N frozen at 123); gate OK, 29pp clean compile
- [x] v4 reviewer-v3 repair (user: go ×2): merged round-4 12 (D78–D88/T47) + scope cuts (T02 subsumed; T07 no-AI; T35 no-crypto; T45 non-radio; T34→background) + moves (T05/T14→both; T28→protocol-func, proceedings-verified; D20/D55 re-keyed, 0 shared IDs; D48→preprint); N refrozen at 130 (84/30/7/9; years 4/17/10/21/30/35/13; ch 66/46/18); closed-loop 14/130 reported; anonymized + de-changelogged; Table3 gate assertion; Fig.8 numeric w/ n-a; PRISMA checklist + BG cites + RESPONSE_v4.md; gate OK, 31pp clean compile
- [x] v5 reviewer-v4 repair (user: go): zero v-history in paper (gate-asserted; abstract 718→256w); R2 audit (rule-as-applied published; sim-only→1 incl. D11/D19/D40 reversal; T01/T08→2; T06/T27→Testbed data; means threat 1.30/defense 1.06); channels flipped (conf 1.13 vs journ 1.06; Fisher p .24/.25 reproduced; no prestige gradient either way); T15/D55 distinct proven (arXiv cites TCCN); D41/D52 verified, D46 label fixed, BG7 corrected, uniform venue rule; FL-privacy justified + with/without sensitivity; FigD/Fig8+dual/FigC fixed; gaps table + checklist + stratification corrected; gate OK, 31pp clean compile
- [x] v6 reviewer-v5 repair (user: go): full R2:=f(validation) uniformity (86 flips; dual 0.57→1.14 still lowest; threat 1.53/def 1.27; journals lead R2 1.41 — no gradient claimed); N=121+9 framing; shares-reverse evidence grade; T15/D55 + BG7 + D46 + T28 + uniform venue rule closed; FL with/without recomputed (1.32 vs 1.27); glossary + survey table + FigD/Fig8/FigC fixes; gate OK (mapping + sensitivity assertions), 31pp clean compile
- [x] v7 reviewer-v6 repair (user: go): earliest-date audit (15 mismatches scripted; T06→2025 + T25→2021 true errors fixed; year_first col, P05 only diff; lags stand); mapping fallout (dual 1.14 margin-hedged; threat 1.53/def 1.27; journ 1.40/conf 1.26, no gradient); depth splits (20/110 coded, Unclear=32 subset); N=121 headlines (57.0/3.3/14.9/11.6); P09→preprint; stale sweep incl. FL 1.32 fix + 16/30 abstract; gate OK (mapping/depth/sensitivity/ban-list), 31pp clean compile, abstract ~270w
- [x] v8 reviewer-v7 repair (user: go): mapping audit closed (T01 sole override named; range ~0.6; verifier-vs-reconciliation split; dual demoted to remark; T18 RL-impersonation clarified); month table + lag out of abstract/conclusion; R3-R5 distributions + by-year flat table; depth supplement + 30/20/110-vs-32 exact; N=121 base everywhere (57.0/11.6/3.3); stale sweep (AdvML 2025 peak, Fig.12 37/31/28, 47/35, P09 19 preprints); gate OK, 32pp clean compile, abstract ~260w

## Act-mode constraints (honest limits — do not fabricate)
- No institutional access: cannot run Scopus/IEEE/WoS. OpenAlex = executed substitute; report recall limit.
- No second human coder: cannot invent kappa. Document single-coder + corrective verifier; add explicit rubric; require future kappa step.
- 33 Unclear (abstract) rows stay unclear without full-text reads. Flag as limitation; fix conditional-on-data-source wording.
- Offline-safe: verify DOIs/years only against local CSVs; do NOT invent DOIs or OpenAlex IDs.

## Verification commands (run before presenting)
- `python3 submission/code/check_consistency.py`
- `cd submission/code && python3 build_tables_refs.py && python3 regen_figures.py`
- `cd submission && pdflatex manuscript.tex (twice, zero warnings)`

## Final status (journal-hardened 2026-10-12; v4 N=130 — supercedes prior 123 lines)
- Manuscript: 29 pages, compiles clean (0 errors/undefined/overfull; only benign first-pass label notice).
- Consistency: `check_consistency.py` → CONSISTENCY OK (N=130; tracks 84/30/7/9; years 4/18/9/21/29/36/13; channels 65/46/19; 0 cited-in, 0 shared IDs; R2-mapping + depth + Table3 assertions).
- Data/validation: Unclear 32, Collected 26, Simulation 20, Analysis 6, Testbed/OTA 46; Std 35, Sim-only 18, Benchmark 4, Testbed-demo 47, Cross-domain 26. R2 means threat 1.53 / defense 1.27 / dual 1.14 / pqc 1.44.
- Headlines on N=121 core: RFFI 57.0%, artifacts 3.3%, preprints 14.9%, closed-loop 11.6%.
- Tables regenerated from dataset (Table6 CSV matches manuscript sensitivity table incl. new Benchmark row); figures regenerated.
- Round-4 backlog: 12 eligible (4 RFFI + 7 FL-privacy defense, 1 FL-jamming threat) held pending full-text reads; 8 excluded with reasons; all in `run_log.md` + `code/round4_*.json`. N frozen at 123.
- Pending/unresolved (honest limits, unchanged): no Scopus/IEEE/WoS access; no second coder (no κ, required pre-journal); 30 paywalled Unclear rows; round-4 merge + full R3–R5 body reads are pre-submission work.

