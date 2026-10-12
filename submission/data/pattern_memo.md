# Pattern memo — 108 verified papers (abstract-level evidence, 75 abstracts + 33 excerpt-coded)
Coverage: abstracts.json holds 75/108; remainder coded from verification excerpts. Code/data-release rates are floors (release statements usually live in body text, not abstracts). Provisional — full-text reads pending for R-scores.

## 1. Topic distribution (abstract-coded, n=75)
- RFF/authentication (incl. spoofing, PLA, open-set): 32 (+3 classifier misses ≈ 35, ~47%)
- PHY key generation/distribution: 11 (~15%)
- Protocol fuzzing / RE / traffic analysis: 7 (~9%)
- UAV / anti-jamming / V2X: 6 (+O-RAN/sensing ≈ 9, ~12%)
- EM/RF side-channel key recovery: 5 (~7%)
- PQC-on-constrained-wireless: 5–9 (contextual stratum)
- Wireless FL privacy/robustness: 3 (~4%)
- Learned primitives (ANC, AMC ensembles, semantic PLS): 2–6
- Year skew: 2024 (29) + 2025 (30) dominate; 2026 already 8 — the field is accelerating, which supports the preprint-inclusion call.

## 2. Evaluation realism (headline finding, still provisional)
- Testbed/measured/OTA/prototype: 31/75 (41%)
- Experimental-data (datasets, captures): 13/75 (17%)
- Simulation/numerical only: 12/75 (16%)
- Unclassifiable from abstract: 19/75 (25%)
- Direction: the literature is roughly half measured, half simulated — NOT overwhelmingly simulation-only. The honest thesis line is weaker and more interesting: *attacks* skew measured (SDR testbeds: T01 15m BLE, T02 LoRa, T18 SDR, T30 SDR, T08 1m), while *defenses* (esp. keygen D09–D13, DRL anti-jamming, IRS/PLS optimization) skew simulated. Adversarial-robustness claims with OTA validation are the exception (T31 O-RAN, D36 ADE black-box transfer).

## 3. The threat–defense asymmetry (core pattern)
- Threat papers name concrete artifacts: <400 traces at 15 m (T01), >90% impersonation with binary feedback only (T18), 76% GAN-spoof success (T09), 81.7% black-box UAP (T03), 90k-trace full-key RF-SCA (T08), 3 baseband CVEs via LLM fuzzing (T28), padding/shaping defeated by packet-size distributions (T19).
- Defense papers cluster on RFF *accuracy under domain shift* (contrastive D44, receiver-agnostic D07/D47, open-set D27–D31/D55/D60–D63) — i.e., defenses optimize benign-conditions accuracy while threats exploit deployment-shift and adaptivity. T40 makes this explicit: domain-shift misclassification itself is the backdoor.
- Only ~13% of abstracts evaluate attack AND defense together (T05, D36, D37, T31, D67-proactive). The field throws attacks over the wall; closed-loop evaluation is rare.

## 4. Readiness signals (provisional, abstract-level)
- Explicit threat-model language: ~23% (floor — modeled attackers often appear only in Section 3).
- Latency/energy/complexity numbers: ~32% (best in PQC stratum: ESP32 DTLS 313 ms P10, <12 kB Dilithium P05, Cortex-M4 cycles P03; worst in DRL anti-jamming — almost no onboard-cost reporting).
- Standards alignment: ~9% (AKA analyses, SUCI, 1609.2-V2X, FIPS 203–205). The RFF literature is nearly standards-free — a gap, since authentication without a profile can't deploy.
- Code/data release: ~4% in abstracts (floor; WiSig-style datasets exist but are cited, not released, in most rows).
- Autonomous-systems presence: ~13% mention UAV/drone/swarm/V2X — yet the thesis gap (real-time deadlines, OTA-update crypto-agility, multi-agent trust) is addressed by almost none: D15 (swarm MARL) optimizes relay/power, not trust; T36 shows FL-for-drones falls to deauth+impersonation chaining; swarm authentication (SecureLink D32) is one of very few.

## 5. PQC stratum (contextual, kept separate)
Coherent story, distinct from AI: ML-KEM/ML-DSA run on ESP32/Raspberry Pi with acceptable compute, but handshake size/latency—not cycles—is the deployment blocker (P09, P10); WKyber (P08) and LAKE (P11) attack exactly the bandwidth problem. No paper in the set yet joins AI-threat × PQC-migration (e.g., ML side-channels on PQC implementations over the air) — a stated gap, not a finding.

## 6. What would overturn this memo
Full-text reads could (a) raise code-release and threat-model rates substantially (both live in body text), (b) flip the sim/measured split either way — the 25% abstract-silent slice is the uncertainty, (c) surface cost numbers in DRL/UAV papers that abstracts omit. The threat–defense asymmetry and RFF-dominance patterns are robust to this; the readiness percentages are not.
