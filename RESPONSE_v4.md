# Response to v3 review (major revision) — v4 resubmission, N=130

All changes refer to `submission/manuscript.tex` unless noted. Gate: `check_consistency.py` → CONSISTENCY OK (N=130, 84/30/7/9, 0 cited-in, 0 shared IDs); `pdflatex` ×2 zero warnings; 31 pages.

## Blocking issues

**1. The 12 eligible papers — MERGED.** The 12 round-4 records are now coded (6 fields + R1–R5, conservative abstract-level) and merged as D78–D88/T47; corpus refrozen at N=130 with cutoff stated (§2.3). Federated privacy 4→11 is reported as a coverage correction from the previously rate-limited FL query, not field growth (abstract, §3.2). The 241 Path A records stay an unscreened extension pool; the abstract now says so verbatim.

**2. Anonymity/audit trail — FIXED.** Initials removed everywhere (roles: Screener 1, Verifiers A/B). All changelog language deleted from the paper ("prior draft", "withdrawn", "former placeholders", "required before journal submission"); review-history narrative lives here, not in the manuscript.

**3. Identifiers — RE-KEYED, claim corrected.** D20→10.1109/tvt.2025.3532982 (Qi Cheng et al., TVT Jun 2025; the shared DOI resolves to T20's paper, verified via Crossref); D55→10.1109/tccn.2020.3043332 (exact vol/pages match; the shared arXiv ID is T15's). Zero shared identifiers remain (gate-asserted). "All 123 carry DOI/arXiv" replaced with the verified per-record identifier claim (DOI, arXiv/ePrint, USENIX URL, or publisher landing page).

**4. Years/venues — VERIFIED.** T02 cut (below); D48 recoded preprint (ICASSP per author comment only, no proceedings record); D46 stays submitted (partitioned, not double-counted); T28 confirmed published (USENIX Security '26, pp. 457–476) with authors/venue/artifact updated from the proceedings page.

**5. Accounting reconciled.** Seeded path restated as 126 (109 includes + 12 background + 4 backup + T24 exclusion; v3's 125 omitted T24 whose row was deleted — owned in text). v4 cuts bridge 135→130 explicitly. Background 15 (13 seeded-origin + 2 OpenAlex, all rowed in `found_papers.csv`). Preprint partition rebuilt programmatically: 14 unconfirmed + D26 presented + T05 preliminary + D46 submitted + D48 author-claimed = 18.

## Stale/contradictory numbers — all regenerated

Table 3 repasted from `Table3_function_by_year.csv` (gate now asserts column sums == year distribution). Fig.5 text fixed (2020 2–1, 2023 9–7 — the alleged ties were a v3-census artifact). Abstract 10→8 unclear-threat. §8 rewritten (70 testbed-or-collected, 34 unclear; scored-vs-prospective split). Fig.10 now prints numeric means with defined bands; R3/R5 shown n/a for attack-only rows. Medians + N/A rates in §2.5/§3.4. Fig.13 cites T36. Fig.14 legend reconciled (Partial = 1–2 papers, nascent). Fig.1 text says two exceptions. LLM fuzzer singular (2026), T28 refolded to Protocol/traffic (Fig.7 follows data). Fig.9 retitled to validation categories.

## Evidence discipline

Title answer narrowed to literature maturity (abstract + conclusion). Closed-loop broader measure now REPORTED: 14/130 with rule + named papers (§6). T05/T14→both under the develops-and-evaluates-both rule. Checklist scored only on coded items; items 7–9/11 marked prospective. "Uncalibrated uncertainty" dropped. AKA-linkability dropped; HNDL-proper recorded unaddressed. New function×validation table (tab:funcval). WiSig-reuse claim dropped. R4 re-verified (T30 code + D32 data releases confirmed; 4/130 = 3.1%). Rigor wording bidirectional per Table 6 (journals 39/28 testbed, 9/17 sim-only). Venue-community stratification added (runs against the confound).

## Scope

T45 excluded (non-radio), T34→background (sensing rule enforced), T35 excluded (no security boundary), T07 excluded (no AI content — T24-consistent; Fuzz column leaves Fig.7 with it). T42 kept on corrected geofence-bypass grounds. D55/T15 and D20/T20 kept as distinct same-team works with corrected keys.

## Round-2 carryovers

§1.3 cites BG2/BG3/BG5/BG7 (listed, not counted); protocol + PRISMA-ScR checklist in archive. "100% full-text" replaced with screening-vs-coding distinction. AI-use enumerates (pooling/drafting/editing only). §3.5 owns the T02 dedupe + D81 tie. Verifier raw disagreement 1/22 reported (R-rescores never entered — stated, no κ).

---

# Response to v4 review (second major revision) — v5 resubmission, N=130

## Version history removed
`grep -c "v4\|v3\|v2"` on the manuscript returns 0 (gate-asserted ban list). Abstract cut 718 → 256 words; run dates stay in methods as PRISMA freshness reporting, everything else lives here and in `run_log.md`.

## R2
Published the rule as applied (2 = author OTA/testbed or demonstrated key recovery; 1 = controlled sim/reused-data evaluation; 0 = theory/proof/analysis without data evaluation). Restored the protocol rubric for simulation rows, reversing the 10-11 downgrades of D11/D19/D40 with disclosure. Recoded on in-hand evidence only: T01/T08 → 2 (OTA/key-recovery), D42/D52 → 1, T06/T27 data → Testbed, 11 sim-only 0 → 1. Means: threat 1.30, defense 1.06. Residual abstract-level zeros owned as a conservative floor with full regrade as pre-journal work.

## Abstract/Table 6
Abstract now says key generation only; representative-table anti-jamming row rewritten as mixed (8 testbed / 4 sim-only — the 5 DRL-UAV testbed papers plus O-RAN/IRS rows explain the surprise).

## Identifiers/venues
T15/D55 proven distinct: the arXiv v1 full text cites the TCCN paper as prior published work. D46 label corrected (stated INFOCOM 2026 inconsistent with Aug-2026 posting). D41 (TVT Jul 2024) and D52 (TCCN Oct 2025) Crossref-verified, so the author-claim rule is uniform: publisher record = confirmed (D41/D52/T28), author comment alone = preprint (D26/D48/D46-submitted). BG7 corrected to Adesina/Hsieh/Sagduyu/Qian, COMST vol 25 (2023). T28 published proceedings cited with artifact.

## §3.5
Rewritten to the flipped numbers (journals 1.06 vs conferences 1.13, gap 0.07); Fisher p ≈ 0.24/0.25 independently reproduced; no prestige gradient claimed either way; frontier lag claimed only for adversarial ML and DRL (deep tied 2020, PQC reversed). Conclusion matches.

## Scope/selection
FL-privacy justified (channel-produced guarantees: OTA superposition, channel-noise DP; D24 precedent) with with/without-7 sensitivity (defense R2 1.16 vs 1.06; 2021 reads 12; patterns hold). 2021 spike owned as coverage effect; "accelerating" → "rising but non-monotonic". First-run incompleteness, no stopping rule, Path-A-zero (two paths + pool), screening-depth correction, and verifier CI (0.1–23%, inclusion-only) all stated.

## Evidence claims
Closed-loop fenced as lower bound (14/130). Adversarial split three-way everywhere (20/7/13) with the figure-pooling rule stated; "attack arm" language removed. Checklist prospective beyond coded items; "uncalibrated uncertainty" dropped. T40 pointer gives the demonstrated trigger. Standards rate split (9.9% non-PQC). Security-venue 7 listed with scores. Table 5 admits proofs ("no empirical validation").

## Stale numbers/figures
11.4%→13.8%, 63/14→66/18, Fig.3/7 captions n=130, classical/Bayesian corrected to RFFI, Table 2 vs Fig.6 rule stated. FigD: T07 removed, T27/T36 corrected. Fig.10: dual row added, title shortened. Fig.1: wider canvas, smaller staggered labels.

---

# Response to v5 review (fourth major revision) — v7 resubmission, N=121+9

## Venue lag vs year coding (concern 1)
Scripted Crossref online/print-date audit over all 15 DOI-year mismatches: 13 are DOI-numbering vs issue-year (D22 printed Apr 2023 despite tvt.2022; T09 Mar 2021 as coded); only T06 (→2025) and T25 (→2021) were true errors, fixed. New `year_first` column (differs on P05 only). Lags stand under both codings; preprint-dot artifact captioned. D36's own arXiv (Apr 2021) confirms the adv journal cell.

## R2 lookup-table (concern 2)
Mapping now gate-asserted over all rows (T01/T08 exceptions logged). Dual margin hedged everywhere (0.13 at n=7). Deltas published as computed; sign-flip owned. Verifier-vs-reconciliation wording split. Testbed-ownership caveat attached to the threat lead.

## Standards rate (concern 3)
Denominator rule published in §2.5 and abstract: 12 = 6 defense + 1 dual R5>0 plus 5 attack rows naming an affected standard, over 121. Threat R3/R5 are n/a in the TableR generator (no longer means).

## Depth confound (concern 4)
`coding_depth` column (20/110, gate-asserted); Unclear=32 shown as subset; Fig.11/Table 8 carry the splits (full-text rows skew sim-heavy 5/20 vs 13/110).

## Outstanding items (concern 5)
Blind second coder still unavailable — R3–R5 fenced as lower bounds. "Trails" language de-temporalized to measured volume/maturity. Autonomous gaps labeled purposive lower-bound scan. R3–R5-by-year added (flat) to reconcile conclusion vs §3.4. Headlines on N=121 base.

## PQC (concern 7)
121+9 framing throughout; non-meeting note; join emptiness caveated as scoping result.

## R2 ownership (concern 8)
Owned as limitation next to the reworded deployment-facing-demonstration lead.

## Stale sweep
All listed items fixed and gate-pinned, including the FL-sensitivity recompute (1.32 vs 1.27), 16/84 coincidence verified distinct, T18 dataset-year correct, and the survey table without B05.

## Smaller questions
P09 recoded preprint (no proceedings record — uniform rule). 110 abstract-only vs 32 Unclear-source rows derived exactly from read logs and stated as different quantities.

---

# Response to v6 review (fifth major revision) — v8 resubmission, N=121+9

## Venue lag (concern 1)
Crossref online/print audit over all 15 mismatches: 13 are DOI-numbering; T06/T25 fixed; D36 journal issue Mar 2022 (year fixed). D22's earliest evidenced date is Apr-2023 print (no online-first record exists) — stated, not assumed. T09 print = coded year. Month table added; lag dropped from abstract/conclusion, hedged in §3.5 with single-cell caveats.

## R2 (concern 2)
T01 named as the sole override (46 with, 45 without). Range corrected to ~0.6. Verifier-vs-reconciliation wording split. Dual demoted to descriptive remark. Testbed-ownership caveat attached.

## Standards (concern 3)
Denominator rule published (12 = 6+1+5 over 121); threat R3/R5 n/a in generator; abstract uses defined figures.

## Depth (concern 4)
coding_depth 20/110 gate-asserted; Unclear=32 subset; splits carried; R3–R5-by-year flat table added.

## Outstanding (concern 5)
No second coder — lower bounds kept. "Trails" de-temporalized to measured volume/maturity. Autonomous scan labeled purposive. R3–R5-by-year reconciles conclusion vs §3.4. Headlines on N=121.

## PQC/R2-ownership (concerns 7–8)
121+9 throughout with non-meeting note; join caveat carried to §6/Table 10. Ownership caveat attached.

## Stale sweep
All fixed and pinned: abstract 16/30, 47/35, 2025 peak + ties, Fig.12 37/31/28, Table 3 rows, §8, T18 positional (dataset 2021 correct), FL recompute. 16/84 coincidence verified distinct. T18 confirmed RL-driven impersonation (adversarial-ML, not DRL family) across all four spots.

## Smaller points
P09 preprint (uniform rule). 110-vs-32 derived from logs and stated as different quantities.
