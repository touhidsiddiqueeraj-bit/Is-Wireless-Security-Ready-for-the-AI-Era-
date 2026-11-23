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
