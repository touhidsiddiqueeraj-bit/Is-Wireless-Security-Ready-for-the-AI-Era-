# PRISMA-ScR Protocol — Is Wireless Encryption Ready for the AI Era?
Assumptions (you said "go" without picking): **scoping review (PRISMA-ScR), floating N (criteria decide count), PQC as contextual section OUTSIDE the counted set.** Change any line and the rest still holds.

## 1. Objective
Map AI-enabled threats to and AI/learned defenses for radio-link security (2020–2026), and chart readiness gaps for autonomous systems (drones, vehicles, swarms, IoT/edge).

## 2. Eligibility (report verbatim in paper)
- **Population:** radio-link/wireless systems (RF, PHY-layer, 5G/6G, Wi-Fi, BLE/Zigbee/LoRa/NB-IoT, V2X/VANET, UAV/drone, swarm, IoT/edge radio).
- **Concept (core set):** security of encryption / authentication / key exchange-management-generation / physical-layer security **AND** AI involvement (AI as attacker tool, defender tool, or learned primitive).
- **Include:** peer-reviewed journal / conference / workshop papers **plus reputable arXiv preprints (2020-01-01–2026-10-11, English, full-text retrievable, with evaluable evidence)**. Rationale (2026-10-11 amendment): AI-security moves faster than review cycles; excluding preprints would miss months of SOTA. Every included preprint records arXiv ID + version + date accessed; if later published, the published version replaces it.
- **Stratification (anti-bias guardrail):** primary synthesis always reported split — peer-reviewed vs preprint — plus a sensitivity check (do headline readiness findings hold on peer-reviewed only?). Preprints never exceed ~40% of the final set; if they do, cap by most-cited/most-evaluated and report the rule.
- **Exclude with reason:** not wireless; no crypto-primitive link (pure IDS/anomaly with no encryption-auth-key link); no AI link; survey/opinion with no primary mechanism (keep ~5 landmarks as background, not counted); pre-2020; non-English; retracted; full-text unavailable; duplicate; methods insufficient to chart. Preprint-specific excludes: no version history / single-day dump with no evaluation artifacts; superseded by published version (dedupe to published).
- **PQC/HNDL:** NOT in core count. Separate contextual mini-search (§6 in searches.md), ~15–25 papers, own count table. Core PQC papers only enter main set if they explicitly discuss AI (AI-assisted cryptanalysis, ML side-channels on PQC implementations, ML for migration prioritisation).
- **Pre-2020 + grey lit:** ~8–12 foundational cites as background. Former peer-review-only limitation (AI-security latency) now resolved by preprint inclusion above; record version-freeze dates instead.

## 3. Validity floor vs readiness outcome
**Floor (include/exclude, 3 checks):** (V1) peer-reviewed + in-range + retrievable? (V2) evaluable evidence present? (V3) claims traceable to reported method/results? Fail V2/V3 → exclude as "no evaluable evidence" / "methods insufficient to chart."
**Readiness (charted, never excludes):** R1 adversary-model explicitness / R2 evaluation realism / R4 reproducibility, all 0–2; R3 + R5 track-dependent with N/A (see §4). Low scores stay — they are the simulation-only finding.

## 4. Track-specific rubric (report per-track, never pooled)
- R1 (all): 0 absent / 1 implicit / 2 explicit attacker capability + assumptions.
- R2 (all): 0 theory/toy only / 1 controlled simulation / 2 OTA testbed, real RF capture, or real cryptanalysis.
- R4 (all): 0 neither / 1 code OR data / 2 both or artifact-evaluated.
- R3 Defense/learned-crypto/auth: 0 no cost / 1 latency OR energy + HW target / 2 both + HW target. **Attack papers: N/A + chart `attacker_cost` (attacker compute/RF budget if reported, else N/A).**
- R5 Defense/PQC-context: 0 none / 1 mentions 3GPP/IETF/NIST/ETSI / 2 evaluated against profile. **Attack papers: N/A + chart `affected_standard` (target profile if stated, else N/A).**
- Report medians/ranges per track with N/A rates. Total = sum of applicable items only (defense /8–10, attack /6 + 2 charted fields).
- Charting extras per paper: `track` (threat/defense), `sim_only_flag`, `quantum_tag` (AI-threat/AI-defense/PQC-context/hybrid — keep PQC analysis in own subsection), autonomous gaps (real-time deadline met? OTA-update discussed? multi-agent trust?).

## 5. Screening (1 + verifier)
Screener 1: 100% title/abstract, 100% full-text, 100% charting. Verifier: blind 20% at each stage + 20% readiness re-score. Binary decisions → Cohen's κ; 0–2 scores → quadratic-weighted κ or ICC(2,1). Target ≥0.60; conflicts by discussion, logged. State single-screener coverage as limitation.

## 6. Search freshness + records
Initial run + rerun week before submission. Log both dates + delta ("new records from update: n") in flow diagram. Record real per-DB hits before/after dedup — no projections. OSF-register this file before screening.

## 7. Codebook for extraction_schema.csv
- `paper_id`: P001…; `track`: threat | defense | both
- `wireless_tech`: 5G/6G/wifi/ble/zigbee/lora/nbiot/v2x/uav/swarm/iot-edge/other
- `crypto_primitive`: encryption/auth/key-exchange/key-management/key-generation/pls/pqc-ref
- `evaluation_type`: testbed/ota-capture/simulation/proof/cryptanalysis/hybrid
- `R1,R2,R4`: 0/1/2; `R3_score`: 0/1/2 or NA; `R5_score`: 0/1/2 or NA
- `attacker_cost` / `affected_standard`: free text or NA
- `sim_only_flag`: y/n; `quantum_tag`: ai-threat/ai-defense/pqc-context/hybrid
- `gap_realtime,gap_ota,gap_multiagent`: met/discussed/absent + note
- `repro_code,repro_data`: y/n + URL
