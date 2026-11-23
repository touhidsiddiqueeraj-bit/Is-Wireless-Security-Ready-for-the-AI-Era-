# Second-coder reliability pass (record 1 of the reply to reviewer: "no IRR, 110/130 abstract-only")

Coder 2 sizes the reliability of the abstract-only charting that carries 110 of 130 rows.
Nothing here alters `dataset_papers.csv` unless adjudication explicitly changes a score.

## Files

| File | Role |
|---|---|
| `build_instrument.py` | Deterministic sampler (seed 20261123) + blank sheet builder, with asserts |
| `sample_frozen.csv` | The 30 drawn rows, stratum, draw reason, evidence source, seed, date |
| `fetch_abstracts.py` | Fetches the 5 abstracts missing from `abstracts.json`, with URL + date |
| `fetched_abstracts.json` | Cached fetched text (5 rows: D08, T11, T20, T39, T46) |
| `codebook_v1.md` | The anchors coder 2 applies, frozen before scoring, incl. three clarifications |
| `coder2_scores.csv` | **Coder 2's sheet — blank until scored.** No coder-1 column is in this file |
| `join_and_stats.py` | Created only after the sheet is committed (see below) |

## Design fixed before scoring

- Frame: the 110 abstract-depth rows (the criticised stratum). Body-read rows excluded — no
  local PDFs for most, stated as a limitation rather than silently skipped.
- n = 30 (27% of frame; the protocol already promises 20%): 12 threat, 5 dual, 4 PQC,
  9 defense; all 7 years; 14 journal / 13 conference / 3 preprint; 2 forced `R3=2` rows.
- `R4 = 1` appears **zero** times in this frame — the only four such rows in the corpus are
  body-read. R4 agreement is therefore expected degenerate; the report will say so and use
  PABAK instead of κ there.
- Evidence: the identical abstract string coder 1 read, except the 5 fetched ones
  (provenance in `fetched_abstracts.json`).
- Blindness proof: `coder2_scores.csv` is committed empty; coder 2's filled version is
  committed before any join with `dataset_papers.csv`.

## Analysis plan (fixed before scoring — do not edit after the join)

1. κ is computed on coder 2's **raw** scores; adjudicated scores are reported separately.
2. Ordinal items R1, R2, R3, R5: quadratic-weighted κ + exact and ±1 agreement + 2000-sample
   bootstrap 95% CI. R4: exact agreement + PABAK, with an explicit note that κ is
   uninformative at a 126:4 marginal.
3. Nominal items (track, function, method_family, data_source, validation, venue_channel):
   unweighted κ + PABAK + bootstrap CI.
4. Derived-claim check: on the same 30 rows, recompute the threat-vs-defense R2 gap sign,
   RFFI share, artifact rate and closed-loop count for coder 1 and coder 2 side by side.
5. Target is κ ≥ 0.60 (protocol §5). If an item misses it, report the miss and run at most
   one documented codebook-clarification round for that item only, both values disclosed.
6. Report `n`, frame, blinding, and the limitation that agreement here measures codebook
   reproducibility on abstracts — not label truth, and not a second independent human.

## Reproduce

```sh
python3 reliability/build_instrument.py     # asserts: 30 rows, quotas, coverage, blanks
python3 reliability/fetch_abstracts.py      # only needed if fetched_abstracts.json is absent
```
