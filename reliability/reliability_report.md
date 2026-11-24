# Second-coder reliability report — n = 30 abstracts (first pass, raw scores)

Coder 2: 30 rows from `reliability/sample_frozen.csv`, scored blind on the abstract text
only, against `reliability/codebook_v1.md`, committed (`5d7bff4`) before any join.
Sampler frozen in `819fa95`. No score in `dataset_papers.csv` has been changed.

Reproduce: `python3 reliability/join_and_stats.py`

## 1. Agreement (raw scores, pre-adjudication)

| Item | Scale | n | Exact | ±1 | κ | 95% CI | PABAK | vs 0.60 target |
|---|---|---|---|---|---|---|---|---|
| R1 attacker-capability | 0–2 | 30 | 0.433 | 1.000 | **0.394** | 0.181–0.539 | −0.133 | fail |
| R2 evaluation realism | 0–2 | 30 | 0.633 | 1.000 | **0.292** | 0.030–0.587 | 0.267 | fail |
| R3 cost | 0–2 | 30 | 0.633 | 0.967 | **0.114** | −0.200–0.438 | 0.267 | fail |
| R4 artifacts | 0–2 | 30 | 1.000 | 1.000 | n/a | — | 1.000 | degenerate (no variance: 60/60 cells = 0) |
| R5 standards | 0–2 | 30 | 0.933 | 1.000 | **0.762** | 0.294–1.000 | 0.867 | pass |
| track | nominal | 30 | 0.800 | — | **0.717** | 0.504–0.903 | 0.600 | pass |
| function | nominal | 30 | 0.900 | — | **0.843** | 0.688–1.000 | 0.800 | pass |
| method_family | nominal | 30 | 0.767 | — | **0.681** | 0.463–0.860 | 0.533 | pass |
| data_source | nominal | 30 | 0.533 | — | **0.379** | 0.156–0.592 | 0.067 | fail |
| validation | nominal | 30 | 0.400 | — | **0.207** | −0.006–0.411 | −0.200 | fail |
| venue_channel | nominal | 30 | 0.900 | — | **0.826** | 0.605–1.000 | 0.800 | pass |

Six of eleven items pass the protocol's κ ≥ 0.60; four fail; R4 cannot be tested.

## 2. The failures are a calibration drift, not noise

Signed difference (coder 2 − coder 1), all 30 rows:

| Item | Mean | Distribution |
|---|---|---|
| R1 | −0.43 | −1 ×15, 0 ×13, +1 ×2 |
| R2 | −0.30 | −1 ×10, 0 ×19, +1 ×1 |
| R3 | −0.27 | −2 ×1, −1 ×8, 0 ×19, +1 ×2 |
| R4 | 0.00 | 0 ×30 |
| R5 | −0.07 | −1 ×2, 0 ×28 |

15 of 17 R1 disagreements are coder 2 scoring exactly one level lower. That is a
floor-definition difference, not random error, and the codebook explains it:

- **`R1 = 0` is unused in all 130 corpus rows.** The published item has a non-operative
  floor: coder 1's effective scale is {1, 2}, where 1 is a floor for any security paper
  and 2 means an explicit attacker model. Any coder who applies the written anchor
  literally ("0 absent") scores 0 for papers that never name an adversary, and registers
  as disagreeing on every such row. Coder 2 did exactly that (R1 = 2 share: 0.467 coder 1
  vs 0.267 coder 2).
- `validation` and `data_source` overlap by construction (testbed vs simulation vs
  third-party data vs standard split), and the v1 codebook gives no tie-break rule —
  hence κ = 0.21 and 0.38 with substantively identical definitions.
- R3's κ collapses on a handful of cells (−2 once, +1 twice) because the item has almost
  no variance in the frame (101 of 130 corpus rows are 0).

## 3. Derived-claim check (same 30 rows)

| Claim | Coder 1 | Coder 2 |
|---|---|---|
| mean R2, threat (n=12) | 1.58 | 1.42 |
| mean R2, defense (n=9) | 1.67 | 1.11 |
| mean R2, dual (n=5) | 1.00 | 1.20 |
| mean R2, PQC (n=4) | 1.75 | 1.00 |
| **R2 threat − defense gap** | **−0.08** | **+0.31** |
| RFFI share | 0.567 | 0.567 |
| artifact rate (R4 ≥ 1) | 0.000 | 0.000 |
| standards signal (R5 ≥ 1) | 0.200 | 0.133 |
| explicit threat model (R1 = 2) | 0.467 | 0.267 |

Two things follow, and the first matters more than the κ table:

1. **The §3.4 R2 gap does not reproduce at n = 30 — for either coder.** Coder 1's own
   30-row subset gives −0.08 while the full corpus gives +0.26; coder 2 gives +0.31 on
   the same rows. The direction of a 0.2–0.3 gap is not stable on 21 track-labelled rows.
   The paper already hedges this gap (mixed coding depth, reconciliation drift ≈ 0.6), but
   the reliability pass shows the gap is finer than the sampling noise supports. The
   defensible statement is directional-and-uncertain, not "0.26".
2. Function-level and channel-level shares are stable (RFFI 0.567 exactly, artifact rate 0
   both, venue channel κ 0.83). The paper's largest and most-cited counts do not depend on
   the disputed items.

## 4. Disagreements

92 cells across 29 of 30 rows, listed in `disagreements.csv` with empty
`adjudicated`/`evidence`/`resolution` columns for adjudication. Coder 2's raw scores
remain the ones used above; adjudication will be reported separately and κ will not be
recomputed on adjudicated values.

## 5. What this means for the manuscript

Option **A — report as measured.** Replace "Inter-rater reliability was not formally
assessed" with: n = 30 abstract-only rows, blind, codebook released, κ per item, and list
R1/R2/R3/validation/data_source as fair-to-poor with the diagnosis above. Every claim that
leans on those five items gets an explicit uncertainty statement; the R2 gap loses its
point estimate.

Option **B — one clarification round (pre-registered as allowed).** Fix only the five
failing items in `codebook_v2.md` (R1 floor rule, R2 testbed-vs-third-party rule,
validation/data_source tie-break, R3 cost-signal floor), rescore those items only on the
same 30 rows, and report **both** rounds. This is the standard, defensible move: it
attributes the miss to the instrument where the instrument is demonstrably ambiguous,
and it is disclosed, not hidden.

Either way the following are already true and go in the paper regardless:
`R1 = 0` is non-operative corpus-wide; `R4` has no variance and cannot be reliability-tested
on abstract-coded rows; the R2 threat–defense gap is under-resolved at n ≈ 21.

## 6. Caveats

- n = 30, 21 track-labelled rows: CIs are wide (±0.15–0.25) and the R3 CI spans 0.
- Coder 2 is not an independent human reader of the literature; agreement here measures
  codebook reproducibility on abstracts, not construct validity, and not label truth.
- Coder 1 had read many of these papers during synthesis; the severity asymmetry is
  consistent with coder 1 coding from a richer mental model than the abstract alone.
- Instrument defect, cosmetic only: the round-1 sheet rendered `abstracts.json` entries as
  `{'title': …, 'abstract': …}` dict reprs. The abstract text was complete and unaltered —
  only the wrapper and escaped quotes were noise — so round 1 stands as scored and its file
  is left untouched. Round 2 renders clean text.

## 7. Round 2 — clarification round, result (post hoc, disclosed)

`round2_stats.py` → `tableS11b_round2.csv`. Coder 2 re-read the same 30 abstracts under
`codebook_v2.md` and changed 9 of 180 cells (7 of them `R1 1→2`, one `1→0`, one validation
cell), with reasoning in `coder2_note` for 24 rows — a genuine re-read, not a copy.

| Item | κ round 1 | κ round 2 | Δ |
|---|---|---|---|
| R1 attacker-capability | 0.394 | 0.376 | −0.018 |
| R2 evaluation realism | 0.292 | 0.292 | 0.000 |
| R3 cost signal | 0.114 | 0.114 | 0.000 |
| data_source | 0.379 | 0.379 | 0.000 |
| validation | 0.207 | 0.195 | −0.012 |
| R5 (control, unchanged) | 0.762 | 0.762 | 0.000 |

**The clarification round did not help.** That is the finding, and it is a stronger one than
an improved κ would have been: the control item did not move (no teaching effect), the
rewritten items did not move either, so the disagreement is not in the rubric wording but in
what abstracts permit a coder to conclude. R1 is the clearest case — v2 defined the unused
floor explicitly, coder 2 used it (one row), and the 1↔2 boundary shifted seven rows the
other way, leaving κ where it started.

Practical consequence: the four-to-five weak items cannot be rescued by rewriting anchors.
They are reported as measured, the readiness comparisons are downgraded to directional, and
the paper no longer claims or implies anything stronger than κ ≈ 0.2–0.4 for them.

## 8. What was changed in the submission package

| File | Change |
|---|---|
| `01_Manuscript...docx` §2.4 | New paragraph: n=30, blinding, per-item κ, clarification round, weak items bounded at 0.1–0.4. Removed both "not formally assessed" sentences; AI-use sentence now names rubric drafting |
| §2.5 | Discloses the two instrument defects: `R1 = 0` unexercised corpus-wide; data_source/validation overlap and are read as one descriptive axis |
| §3.4 | R2 gap stated as a direction, not a magnitude, with the −0.08…+0.31 coder range |
| Limitations | Replaces "not formally assessed" with the measured bound and its scope |
| `08_Supplementary...docx` | New §S5 and **Table S11** (both rounds); future-work sentence now says the pass is done at n=30 and names the 80+20 rows still single-coded |
| `03_Declarations...docx` | CRediT note points to §2.4/Table S11 and names the second coding under the validation role (Md. Abul Malek Fahim); author contributions add it explicitly; data availability adds both score sheets and the agreement script; AI-use adds "rubric drafting" |
| `02_Cover_Letter...docx` | Replaces "inter-rater reliability was not formally assessed" with the measured n=30 statement; "16 of 30" → "up to 16 of 30" |
| §3 opening | New two-paragraph reading guide: which numbers carry κ 0.68–0.84 (composition) and which carry 0.11–0.76 (readiness), with weak-item quantities given as upper bounds |
| Abstract, §3.3, conclusions | "16 of 30 hardware" → "up to 16 of 30"; body gives the 10–16 bracket from the two codings; the conclusion stops calling the weakest field the "most robust contrast" |
| §2.6 | Closed-loop count now flagged as a hand-judged construct with no separate reliability estimate |
| PDFs | 01 (39 pp), 03, 08 regenerated with soffice |

**Not changed:** every corpus count, every table number, every figure, `dataset_papers.csv`.
No score was revised on the basis of the reliability pass, and adjudication of the 92
disagreement cells remains open work (logged in `disagreements.csv`).

## 9. Residual risk after this pass

- A referee can still say the five weak items are unreliable. The answer is now measured and
  published rather than absent, and the strongest counts (function 0.84, venue 0.83) do not
  depend on them.
- n = 30 of 110 abstract rows, author-as-coder, abstracts only. Stated in the paper.
- Coder 1 was not blinded to their own earlier reading; their severity offset (−0.43 on R1)
  is consistent with coding from a richer model than the abstract alone. Reported.

## 10. "Isn't κ too low to take seriously?" — checked, with five coefficients

`prevalence_checks.py` → `tableS12_coefficients.csv`. κ is prevalence-sensitive, so a low value
can in principle be an artefact of a skewed marginal rather than real disagreement. It is not,
here:

| Item | κ unweighted | κ weighted | Krippendorff α | Gwet AC1 | κ binary (0–1 vs 2) |
|---|---|---|---|---|---|
| R1 attacker-capability | 0.07 | 0.39 | 0.36 | 0.20 | 0.31 |
| R2 evaluation realism | 0.29 | 0.29 | 0.24 | 0.52 | 0.29 |
| R3 cost signal | −0.06 | 0.11 | 0.00 | 0.56 | — |
| R5 standards signal | 0.76 | 0.76 | 0.76 | 0.92 | — |
| validation approach | 0.21 | — | 0.08 | 0.27 | — |
| data_source | 0.38 | — | 0.05 | 0.43 | — |

Readings:

- **R1, R2, validation, data_source: genuinely weak.** No coefficient puts R1 above 0.39 or
  validation above 0.27. This is real disagreement, and it is reported as such.
- **R3 is a different animal.** Both coders agree on 23 of 30 rows; 19 of those are a shared
  `0`. κ and α collapse under that prevalence while AC1 (0.56) and raw agreement (0.63) do
  not. The item's problem is **discrimination, not disagreement** — it is reported
  descriptively, not used as an ordering device.
- **R5 is fine** under every coefficient.

Consequence for the paper: the claims that survive are the ones built on function (0.84),
venue channel (0.83), track (0.72), method family (0.68), R5 (0.76) and R4 (no variance,
hence no false-positive risk) — i.e. the corpus composition and the artifact/standards gaps.
The claims that do not survive at fine grain are the readiness *level* comparisons
(R1/R2/R3), which are now stated as directional.

## 11. Where the paper now stands (author decision log)

- Coder 2 = Md. Abul Malek Fahim (second author), named in the CRediT note and author
  contributions; the AI-use statements still hold because no coding decision was
  delegated to AI (the agent drafted the codebook text and computed the statistics).
- The hardware headline is reported as **up to 16 of 30**, with 10–16 given in the body,
  because the two codings gave 6 and 4 testbed rows among the 12 sampled attack rows.
- Page count 01: 38 (pre-reliability) → 41. The delta is inline-figure pagination
  (two figures now sit on their own pages), not content; image count is unchanged at 46.
