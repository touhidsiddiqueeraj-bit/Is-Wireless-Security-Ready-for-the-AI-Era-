# Exact search strings — copy-paste per database
Principle: crypto-primitive terms are MANDATORY (kills IDS/anomaly flood). `anomaly detection / federated learning / intrusion detection` only retrieve when crypto + wireless also match. Single core run (W AND C AND AI); tag threat/defense at screening — avoids duplicate runs.

## Concept blocks (shared vocabulary)
- **W (wireless, required):** wireless, radio, "physical layer", RF, "radio frequency", 5G, 6G, Wi-Fi, WiFi, BLE, Bluetooth, Zigbee, LoRa, NB-IoT, V2X, VANET, UAV, drone, swarm, IoT, "edge", "constrained radio"
- **C (crypto primitive, required):** encrypt*, "authenticated encryption", authentication, "key exchange", "key management", "key generation", "physical-layer security", "physical layer security"
- **AI (required):** "machine learning", "deep learning", neural, adversarial, "RF fingerprint*", "side-channel", "side channel", "reverse engineer*", fuzz*, "traffic analysis", "signal analysis", "large language model", LLM, "foundation model", "anomaly detection", "federated learning"

## 1. Scopus (primary broad index)
```
TITLE-ABS-KEY((wireless OR radio OR "physical layer" OR RF OR "radio frequency" OR 5G OR 6G OR Wi-Fi OR WiFi OR BLE OR Bluetooth OR Zigbee OR LoRa OR NB-IoT OR V2X OR VANET OR UAV OR drone OR swarm OR IoT OR edge OR "constrained radio") AND (encrypt* OR "authenticated encryption" OR authentication OR "key exchange" OR "key management" OR "key generation" OR "physical-layer security" OR "physical layer security") AND ("machine learning" OR "deep learning" OR neural OR adversarial OR "RF fingerprint*" OR "side-channel" OR "side channel" OR "reverse engineer*" OR fuzz* OR "traffic analysis" OR "signal analysis" OR "large language model" OR LLM OR "foundation model" OR "anomaly detection" OR "federated learning")) AND PUBYEAR > 2019 AND PUBYEAR < 2027 AND (DOCTYPE(ar) OR DOCTYPE(cp)) AND LANGUAGE(english)
```
Run: Advanced search → paste → filter years 2020–2026 → record hits.

## 2. IEEE Xplore (command search)
```
(("Abstract":wireless OR "Abstract":radio OR "Abstract":"physical layer" OR "Abstract":RF OR "Abstract":5G OR "Abstract":6G OR "Abstract":Wi-Fi OR "Abstract":UAV OR "Abstract":drone OR "Abstract":swarm OR "Abstract":IoT OR "Abstract":V2X OR "Abstract":LoRa OR "Abstract":Zigbee) AND ("Abstract":encrypt* OR "Abstract":authentication OR "Abstract":"key exchange" OR "Abstract":"key management" OR "Abstract":"key generation" OR "Abstract":"physical-layer security") AND ("Abstract":"machine learning" OR "Abstract":"deep learning" OR "Abstract":neural OR "Abstract":adversarial OR "Abstract":fingerprint OR "Abstract":side-channel OR "Abstract":fuzz* OR "Abstract":"traffic analysis" OR "Abstract":LLM))
```
Filters: Year 2020–2026, Conferences + Journals. Note: IEEE truncates long queries — if rejected, split AI block into two runs (A-threat terms / B-defense terms) and merge.

## 3. ACM Digital Library
```
[Abstract: (wireless OR radio OR "physical layer" OR RF OR 5G OR 6G OR UAV OR drone OR IoT OR V2X)] AND [Abstract: (encrypt* OR authentication OR "key exchange" OR "key management" OR "key generation" OR "physical-layer security")] AND [Abstract: ("machine learning" OR "deep learning" OR neural OR adversarial OR fingerprint OR side-channel OR fuzz* OR "traffic analysis" OR LLM OR "anomaly detection" OR "federated learning")] AND [E-Publication Date: (01/01/2020 TO 10/11/2026)]
```
Use Advanced search → edit query. Record refinements (ACM stemming varies).

## 4. Web of Science (use only if no Scopus; else skip to avoid double-index bloat)
```
TS=((wireless OR radio OR "physical layer" OR RF OR 5G OR 6G OR UAV OR drone OR swarm OR IoT OR V2X OR LoRa OR Zigbee) AND (encrypt* OR "authenticated encryption" OR authentication OR "key exchange" OR "key management" OR "key generation" OR "physical-layer security") AND ("machine learning" OR "deep learning" OR neural OR adversarial OR fingerprint OR side-channel OR fuzz* OR "traffic analysis" OR LLM)) AND PY=(2020-2026) AND LA=(English) AND DT=(Article OR Proceedings Paper)
```

## 5. Supplemental (USENIX Security / NDSS / CCS / MobiCom — manual, same week)
No formal string; run site search with stem `wireless encrypt (ML OR neural OR fingerprint OR side-channel)` on usenix.org + ndss-symposium.org, plus check ACM CCS/MobiCom proceedings already indexed. Purpose: catch PHY/RF work missed by indexers. Log proceedings volume + papers screened + added count. Everything found still passes §2 eligibility.

## 5b. arXiv (countable source since 2026-10-11 amendment)
Query: same W AND C AND AI blocks via arXiv advanced search (cs.CR + cs.LG + eess.SP), 2020–2026. Record ID + version + access date per included preprint; deduplicate against published versions (published wins). Cap: preprints ≤40% of final set; report peer-reviewed vs preprint split + sensitivity check per protocol §2.

## 6. PQC contextual mini-search (OUTSIDE core count, own table)
Scopus:
```
TITLE-ABS-KEY((wireless OR radio OR UAV OR drone OR IoT OR V2X OR "constrained radio" OR edge) AND ("harvest now decrypt later" OR "post-quantum" OR PQC OR Kyber OR Dilithium OR "migration") AND (encrypt* OR authentication OR "key exchange" OR "key management")) AND PUBYEAR > 2019 AND PUBYEAR < 2027 AND LANGUAGE(english)
```
Target ~15–25 for background section. Link sentence: HNDL amplified by AI (AI-assisted target selection via traffic/signal analysis; ML-accelerated cryptanalysis pressure on harvested flows); PQC cost on constrained radios bounds AI-defense budgets. Core set admits a PQC paper only if it explicitly discusses AI per protocol §2.

## Run log (fill both dates — initial + pre-submission rerun)
| database | date_run | string_version | filters | hits | after_dedup_to_screen | notes |
|---|---|---|---|---|---|---|
| Scopus core |  | v1 above | 2020–2026, ar/cp, EN |  |  |  |
| IEEE core |  | v1 above | 2020–2026 |  |  | split runs? Y/N |
| ACM core |  | v1 above | date filter |  |  |  |
| USENIX/NDSS suppl. |  | manual | — |  |  | vols screened |
| PQC mini (Scopus) |  | §6 | 2020–2026 |  | separate table | contextual only |
| RERUN all above |  | same | same |  | delta: n | pre-submission |
