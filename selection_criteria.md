# Selection criteria (for the paper — mirrors reviewer-paper Table 2 style)

## Screening summary (real counts, open-web seed)
| Stage | Description | Records |
|---|---|---|
| Identification | Structured web-search rounds (29) | ~290 |
| After deduplication | Unique candidates by paper ID | 125 |
| Assessed (agent screen) | Validity floor + link checks | 125 |
| Included evidence base | Countable set | 109 (100 core + 9 PQC-context) |
| Background | Surveys, pre-2020 foundations | 12 |
| Backup | Thin provenance, held for swaps | 4 |
| Excluded | T24 (EAP-AKA formalization, no AI link) | 1 |

## Inclusion criteria (all required)
1. Radio-link/wireless population (RF, PHY-layer, 5G/6G, Wi-Fi, BLE/Zigbee/LoRa, V2X, UAV/drone, swarm, IoT/edge).
2. Crypto-primitive link (encryption, authentication, key exchange/management/generation, physical-layer security).
3. AI involvement (attacker tool, defender tool, or learned primitive).
4. Dated 2020-01-01–2026-10-11, English, full text retrievable.
5. Evaluable evidence (experiment, testbed, simulation, proof, cryptanalysis).
6. Peer-reviewed venues plus reputable arXiv preprints (ID + version + access date recorded; published version supersedes; preprints ≤40% of final set).

## Exclusion criteria (with reason logged)
Not wireless | no crypto link | no AI link | survey/opinion without primary mechanism | pre-2020 | non-English | retracted | unretrievable | duplicate | no evaluable evidence | methods insufficient to chart | preprint without evaluation | superseded by published version.

## Adjudication log (reviewer-visible decisions)
- T07 RANsacked (CCS'24): INCLUDED — LTE/5G AKA+RRC fuzzing counts as authentication-link.
- T10 Wi-Spoof (JISA'25): moved to background — Wi-Fi sensing, no crypto/auth/key link.
- T24 EAP-AKA formalization: EXCLUDED — no AI link.
- IEEE Xplore-hosted rows with unconfirmed venue detail: counted as peer-reviewed (Xplore hosts only peer-reviewed content), venue reverify at full-text read.
