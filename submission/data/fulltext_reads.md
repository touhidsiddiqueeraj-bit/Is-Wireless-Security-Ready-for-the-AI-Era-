# Full-text adjudication log — 30 preprints (2026-10-11)
All 30 arXiv HTML fetched (T35 via PDF, pypdf). Evidence extracted: threat-model sections, eval setup, code links, cost numbers, standards refs. Machine extraction + human read of snippets.

## Upgrades applied to dataset_papers.csv
- R1→2 (explicit threat/attack-model section in body): D11 (III-B Attack Model, passive Eve), D25 (III-C), D32 (II-A), D33 (III), T27 (III-A), T36 (III-A/B/C).
- R2→2 (testbed confirmed): T06 (3×USRP B210 + 3×LimeSDR), D32 (real-world testbed + GitHub datasets), T27 (heterogeneous Wi-Fi testbed), T36 (Pi + Jetson Flower testbeds).
- R2→0 + Simulation-only (body confirms sims): D11 (VII Simulation Results), D19 (IV Simulation), D40 (IV Simulations).
- R3→1 (cost numbers): D32 (15 ms/auth + per-stage table), D33 (130→164 kB net sizes), D46 (0.1015 ms/sample), T09 (0.088 ms processing), T19 (10 ms fast check).
- R4→1 (artifacts released): D30 (repo + 45-LoRa dataset), D32 (repo + datasets). T23 links are third-party tools, not own artifacts — no upgrade.
- R5→1: D32 (802.11), T09 (802.11), T14 (O-RAN), T23 (3GPP/O-RAN), D34 (3GPP), P08 (FIPS 203/186, NIST).
- T35 (DeepMIMO emulator, 105k records, FGSM + LightGBM-98%): verified, emulator-grade evidence, no threat model/code/cost — unchanged scores stand.

## Effect on means
Threat R2 0.97→1.09, R5 0.09→0.14; defense R2 0.88→0.94, R3 0.22→0.25, R4 0.01→0.03. No headline overturned: full-text reads confirmed the abstract-level picture rather than inflating it. Reproducibility (R4) and standards (R5) remain the weakest criteria corpus-wide — now as full-text-backed findings, not abstract artifacts.

## OA-adjudication pass, Unclear rows (2026-10-12)
Attempted OA abstract/full-text verification for all 33 Unclear (abstract) rows. 30 are paywalled journal/conference papers (no institutional access) and stay Unclear as a stated limitation. 3 OA rows resolved (abstract-level evidence, no R-score changes — bodies not fully read):
- T05 (arXiv 2412.21164, authors verified): "trained ... using actual LoRa signal data" → data_source Unclear→Collected dataset/traces. Validation stays Standard split/unclear (author OTA collection not established); R-scores unchanged pending body read.
- D76 (arXiv 2604.24022, authors verified): "simulation results demonstrate" → data_source Unclear→Simulation, validation Standard split/unclear→Simulation-only (consistent with existing R2=1).
- P11 (eprint 2025/2293, title verified): construction + reduction + quantitative analysis (ciphertext −15–25%, DFR, overhead) → data_source Unclear→Analysis/benchmark, validation Standard split/unclear→Benchmark/analysis.
- D33 deliberately unchanged: prior full-text read (R3 upgrade logged above) left data_source Unclear — learned-primitive taxonomy gap, not missing evidence.
Effect: Unclear 33→30; Collected 25→26; Simulation 16→17; Analysis 3→4; Std/unclear validation 36→34; Sim-only 14→15; Benchmark 1→2. No R-means move.
