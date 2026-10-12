# Is Wireless Encryption Ready for the AI Era? A Structured Scoping Review and Classification of 109 Studies, 2020–2026

> SUPERSEDED 2026-10-11: working draft only. The submission build is `submission/manuscript.tex` (anonymized, 14 figures, 3-way venue-velocity analysis, corrected years 4/13/7/18/28/31/8 and 90/19 peer/preprint split). Do not quote numbers from this file.

Hussain Touhid Siddiquee
Leading University, Sylhet, Bangladesh
Syeda Salsabil Islam Ariya
Leading University, Sylhet, Bangladesh
Jasimul Islam Chowdhury
Leading University, Sylhet, Bangladesh

## Abstract
Machine learning (ML) has moved from a promising addition to wireless security to a load-bearing component of radio-link authentication — and simultaneously to the adversary's standard toolkit. This paper presents a structured scoping review of 109 studies published between 2020 and 2026 that apply machine learning to wireless-link security or attack it, assembled from Crossref- and arXiv-verified records plus a fully logged expert-seeded set, and classified uniformly by security function, AI method family, wireless technology, data source, validation practice, and deployment readiness. The corpus comprises 65 defense, 31 threat, and 4 dual studies (100 core) plus 9 post-quantum contextual studies kept in a separate stratum (79 peer-reviewed, 30 preprints).
The bibliometric analysis reveals a sharp evolution. Deep supervised fingerprinting dominated through 2023 (35 papers), while adversarial ML — 37 of 109, with 12 papers in 2024 alone — is now the largest family, alongside rising reinforcement-learning anti-jamming (8 papers) and the first LLM-assisted protocol fuzzers (2024–2026). Authentication/RFFI absorbs 59 of 109 studies (54%); key generation (11), anti-jamming/secure communications (12), protocol/traffic analysis (9), federated privacy (4), learned primitives (3), and side-channel analysis (2) split the remainder.
Three structural weaknesses persist across the six-year window. First, validation is split by kind, not just rigor: threat studies demonstrate exploits on real captures (testbed/field demonstration the norm; mean R2 1.19), while defense studies show a fat-tailed split — testbed mass in RFFI but the corpus's highest simulation-only concentration in key generation and DRL anti-jamming (defense mean R2 0.94) — and closed-loop attack-plus-defense evaluation appears in only ~13%. Second, reproducibility is near-absent (mean R4 0.03–0.06; release signals in ~3%) and standards alignment is weakest (mean R5 0.09–0.16; ~7% overall): the RFF literature is nearly standards-free. Third, the autonomous-systems gap is concrete: real-time, over-the-air-update, and multi-agent-trust needs are essentially unaddressed (1–2 papers), while harvest-now evidence for short-range radio (BLE/AKA) already exists. The review's sharpest finding is that defenses optimize benign-conditions accuracy while threats exploit domain shift itself — RFF accuracy is not authentication; domain-shift misclassification is itself exploitable. A peer-reviewed-only sensitivity rerun (n=79) preserves every headline pattern. The review closes with a gap-driven research agenda and a twelve-item reporting checklist (WIRELESS-AI-RC).
Keywords: wireless security; physical-layer authentication; RF fingerprinting; adversarial machine learning; physical-layer key generation; anti-jamming; post-quantum migration; scoping review

## 1. Introduction
### 1.1 The radio link under AI pressure
Wireless links broadcast by physics: every transmission is receivable by anyone in range, which makes the radio link the natural attack surface for interception, impersonation, and jamming. The classical answer — encryption, authentication and key agreement (AKA), and physical-layer techniques — now faces three simultaneous strains. First, software-defined radios put laboratory-grade interception and transmission in every adversary's hands. Second, machine learning turns raw captures into fingerprints, keys, and exploits automatically, without hand-built demodulators. Third, autonomous systems (drones, vehicles, swarms, IoT/edge fleets) need authentication under real-time deadlines, over-the-air updates, and multi-agent trust — requirements the literature rarely addresses together. The question this review asks is whether the radio-link security literature has kept pace with the adversary it has itself equipped.

### 1.2 How AI entered wireless security
AI entered through authentication. Deep networks learned RF fingerprints from raw I/Q, outperforming hand-crafted features, and physical-layer key generation promised lightweight secrets from channel reciprocity without public-key infrastructure. The adversarial turn followed quickly: white-box perturbations break RFFI classifiers on real LoRa captures; black-box universal perturbations reach 81.7% success with almost no victim knowledge; reinforcement-learned impersonation needs only binary accept/reject feedback for >90% penetration; GAN-spoofed signals pass PHY authentication at 76%. Two results reset expectations the way early-life prediction and closed-loop fast charging did for batteries: far-field deep-learning side-channel recovery of BLE AES-128 at 15 m from fewer than 400 traces, and Magmaw (NDSS'25) — protocol- and modality-agnostic universal perturbations, SDR-demonstrated at noise-level power, surviving adversarial training, subtraction, detection, and oracle defenses, including against an encrypted image channel. Authentication learned from waveforms, it turned out, could be unlearned by waveforms.

### 1.3 Existing reviews and the literature gap
The review literature has grown alongside the applications, but it is fragmented along the same axes as the primary studies. Function-specific surveys cover RF fingerprinting, physical-layer key generation, and post-quantum migration; method-specific ones follow adversarial ML or federated privacy. What is largely missing is a cross-functional, quantitative account of the field's trajectory: which AI method families are actually being used for which security functions, on which data, validated how, and how that picture has shifted over 2020–2026. This gap matters because the field's self-image drives its research allocation. If most published authenticators are validated on closed-set, single-receiver, static-channel benchmarks, the community's sense of progress is calibrated to a regime that differs sharply from deployment under adaptive adversaries. Answering such questions requires a corpus-level, cross-functional account rather than another narrative synthesis of one function.

### 1.4 Contribution of this paper
This paper makes four contributions. First, it assembles a verified corpus of 109 studies (2020–2026) on AI in wireless-link security, in which every reference's bibliographic metadata was confirmed by direct DOI or arXiv-ID resolution. Second, it develops a two-axis classification framework — security function × AI method family — extended with track, data-source, validation-practice, and readiness fields, and applies it uniformly to all 109 papers. Third, it quantifies the field's six-year evolution across functions, methods, data, and validation (§3), identifying the shift from deep supervised fingerprinting through adversarial ML to DRL anti-jamming, federated privacy, and early LLM-assisted analysis. Fourth, it provides a critical, function-by-function review of what the corpus actually demonstrates (§§4–6), a cross-cutting analysis of the threat–defense asymmetry (§7), and distills a gap-driven research agenda plus a reporting checklist (§8).
Fig. d_fig1_heatmap previews the analysis, mapping the corpus across security functions and method families: the field's center of gravity sits squarely in the RFFI × (adversarial + deep-supervised) complex, key generation is a simulation-heavy DRL-adjacent island, and LLM-assisted work is only now appearing. The remainder of the paper is organized as follows. §2 details the review methodology. §3 presents the corpus overview and bibliometric analysis. §§4–6 review threats, defenses, and the quantum-era context. §7 examines cross-cutting directions. §8 formulates gaps and the checklist. §9 concludes.

## 2. Review Methodology
### 2.1 Scope and objective
The objective is to characterize the state and evolution of AI applied to radio-link security: encryption, authentication/RFFI, key generation/distribution/exchange/management, anti-jamming/secure communications, protocol/traffic analysis, side-channel analysis, and learned primitives — crossed with AI as attacker tool, defender tool, or learned primitive — over 2020-01-01–2026-10-11, plus readiness gaps for autonomous systems (drones, vehicles, swarms, IoT/edge). Post-quantum migration forms a separate contextual stratum (9 studies), never pooled with AI claims.

### 2.2 Literature search strategy
Two-path triangulation was used. Path A (programmatic, mirrors the BMS design): Crossref REST API, 16 topical queries (rows=100, date/type filtered) plus arXiv API, 10 queries (max 50) → 1,945 unique records after DOI/arXiv-ID deduplication (1,555 Crossref + 390 arXiv; records.json). Path B (expert-seeded): 29 structured open-web search rounds (~290 records, fully logged in run_log.md) → 125 candidates by paper ID. Two properties of this design should be stated plainly. First, Crossref is a metadata registry, not a discovery engine like Scopus or Web of Science; topical recall for this IEEE/ACM-heavy, terminology-variant literature is ~50% by token overlap, which is why triangulation — not single-source retrieval — is the design, and database runs (Scopus/IEEE/ACM) are recorded as pending for lack of institutional access. Second, the seeded path inherits expert-search bias toward notable and recent work; all trend statements are statements about trends within this verified, English-language sample rather than about the field in the aggregate.

### 2.3 Screening and selection procedure
The funnel is shown in Fig. 1 (fig1_flow). From 1,945 deduplicated programmatic records, a title-level relevance gate requiring wireless AND crypto/auth AND AI terminology retained 241 records (gated.json). The seeded path went 125 candidates → validity floor (V1 peer/in-range/retrievable, V2 evaluable evidence, V3 claims traceable) → 109 included (100 core + 9 PQC-context) + 12 background (surveys, pre-2020 foundations) + 4 backup (thin provenance, held for swaps) + 1 excluded (EAP-AKA formalization, no AI link). Full-text curation of 30 preprints upgraded readiness scores where body text confirmed testbeds, threat models, costs, or artifacts (fulltext_reads.md) — means moved ≤0.12, confirming rather than overturning the abstract-level picture.

### 2.4 Inclusion and exclusion criteria
Table 1 summarizes the criteria. Inclusion required: (i) radio-link/wireless population; (ii) crypto-primitive link; (iii) AI involvement; (iv) dated 2020–2026, English, retrievable; (v) evaluable evidence (experiment, testbed, simulation, proof, cryptanalysis); (vi) peer-reviewed venue or reputable arXiv preprint (ID+version+access date; published supersedes; preprints ≤40% — observed 27.5%). Exclusion: not wireless; no crypto link; no AI link; survey/opinion without primary mechanism (background only); pre-2020; non-English; retracted; unretrievable; duplicate; no evaluable evidence; preprint without evaluation. Adjudications logged: cellular AKA/RRC fuzzing counts as authentication-link (included); Wi-Fi sensing without crypto-link moved to background; Xplore-hosted rows counted as peer-reviewed (Xplore hosts only peer-reviewed content), venue reverify at full-text read.

Table 1. Inclusion and exclusion criteria.
| Dimension | Included | Excluded |
|---|---|---|
| Population | Radio-link/wireless systems | Wired-only, pure sensing without crypto link |
| Concept | Crypto primitive + AI involvement | Missing either link |
| Document | Peer-reviewed + reputable arXiv (≤40%) | Surveys w/o mechanism, evidence-free preprints |
| Period | 2020–2026 | Pre-2020 |
| Verification | DOI/arXiv-ID resolved | Unresolvable, retracted, duplicate |
| Language | English | Non-English |

### 2.5 Classification framework
Each paper was classified along six fields: (1) security function (8 values: Authentication/RFFI, Key generation/distribution, Anti-jamming/secure comms, Protocol/traffic/cryptanalysis, PQC migration contextual, Federated/privacy-preserving FL, Learned primitives/crypto, Side-channel attack analysis); (2) AI method family (adversarial ML, deep supervised, PQC implementation, reinforcement/DRL, federated/private, traffic-analysis ML, LLM-assisted, defensive/robust ML, classical/Bayesian, optimization-based, dataset/benchmark, survey); (3) track (threat 31 / defense 65 / both 4 / pqc-context 9); (4) primary data source; (5) validation approach; (6) readiness R1–R5 (R1 adversary explicitness, R2 evaluation realism, R3 cost — attacker-cost charted for attacks, R4 reproducibility, R5 standards — affected-standard charted for attacks), each 0–2 with N/A handling. Papers take a single dominant value per field; conservative coding throughout. A verifier checking pass reviewed the labels but was corrective rather than blind double-coding — no agreement statistic is claimed, and counts should be read as one documented coding (the same honesty formula as the BMS blueprint). The complete dataset is released as dataset_papers.csv precisely so independent coders can check, correct, or extend it.

### 2.6 Comparative synthesis approach
Quantitatively, classification fields are aggregated into cross-tabulations — function by year, method by year, data, validation, readiness per track — that characterize the corpus as a sample (§3); every figure and count was generated programmatically from the released dataset. Qualitatively, the review synthesizes each function critically: what each cluster assumes, demonstrates, and where its support is thin (§§4–7). The methodology has limitations readers should weigh: open-web seeding favors notable work; title-gate screening can miss nonstandard terminology; preprint inclusion adds recency at the cost of version instability (frozen by ID+version+date); single-coder classification carries no reliability statistic; database triangulation is pending access. §3 should therefore be read as a structured sample, not a census — which is why this paper describes itself as a scoping review with bibliometric classification rather than a meta-analysis. No pooled effect sizes are reported: metric heterogeneity (accuracy vs KGR vs secrecy rate vs attack-success rate) forbids it — a deliberate choice.

## 3. Corpus Overview and Six-Year Evolution
### 3.1 Publication trend
The corpus spans 2020–2026 with an accelerating profile: 4 (2020), 14 (2021), 6 (2022), 18 (2023), 29 (2024), 30 (2025), 8 (2026 partial) (Fig. d_fig2_years). Two caveats: the corpus is curated, so the curve partly reflects curation as well as field growth; and preprint share rises with recency, which is the velocity justification for their inclusion (§3.5). With those caveats, the profile matches the field's post-2020 SDR-democratization and the 2024–2025 adversarial-ML surge.

### 3.2 Method-family evolution
The defining meta-finding is the compositional shift (Fig. d_fig3_methods, Table 2). Deep supervised learning (CNN/RNN/Transformer fingerprinting) leads through 2023 (35 total). Adversarial ML (37) overtakes from 2024 — 12 papers that year — spanning white-box, black-box UAP, GAN-spoofing, backdoors, and universal PHY perturbations. Reinforcement/DRL climbs to 8 (anti-jamming, UAV relay, secrecy-rate optimization). PQC implementation (9) concentrates 2024–2026. Federated/private learning (5), traffic-analysis ML (2), LLM-assisted fuzzing (1+), and defensive/robust ML (1) fill the long tail. Classical ML survives only in traffic analysis. The families are not mutually exclusive in practice; dominant-family coding understates mixing.

Table 2. Method families: representative techniques, strengths, limitations.
| Method family | Papers | Techniques | Strengths | Limitations |
|---|---|---|---|---|
| Adversarial ML | 37 | FGSM/PGD/UAP, GAN-spoof, backdoor, RL-impersonation | Realistic threat evidence; OTA-demonstrated | Rarely tests adaptive defenses |
| Deep supervised | 35 | CNN/RNN/Transformer RFFI, contrastive, open-set | Strong closed-set accuracy; shift-robust variants | Accuracy ≠ authentication; weak adversary eval |
| PQC implementation | 9 | ML-KEM/ML-DSA on ESP32/Pi, WKyber, LAKE | Real onboard costs | Bandwidth, not cycles, blocks |
| Reinforcement/DRL | 8 | Anti-jam power/relay, secrecy-rate control | Adaptive control under jamming | Sim-heavy; cost-silent |
| Federated/private | 5 | DP-OTA-FL, robust aggregation | Privacy + wireless-aware | Small scale; attack-chaining shown |
| Other (traffic/LLM/defensive/classical) | 9 | KNN/SVM/RF, LLM fuzzing, robust training | Niche depth | Thin, scattered |
| Survey/systematization + benchmarks | 8 | Reviews, datasets | Maps field | No primary validation |

### 3.3 Application-area distribution
Functionally the corpus is dominated by Authentication/RFFI: 59 papers (54%), followed by Anti-jamming/secure comms (12), Key generation/distribution (11), Protocol/traffic/cryptanalysis (9), PQC-context (9), Federated/privacy FL (4), Learned primitives (3), Side-channel analysis (2) (Fig. d_fig1_heatmap). The center of gravity sits in RFFI × (adversarial 26 + deep-supervised 24). By contrast, side-channel key recovery (2 coded; more in threat narrative) and learned primitives (3) are thin — telling, since these are where cryptographic consequences are most direct.

Table 3. Corpus composition: function by year (109 papers).
| Function | '20 | '21 | '22 | '23 | '24 | '25 | '26 | Total |
|---|---|---|---|---|---|---|---|---|
| Authentication/RFFI | 3 | 9 | 3 | 10 | 15 | 15 | 4 | 59 |
| Anti-jamming/secure comms | 0 | 1 | 1 | 2 | 4 | 3 | 1 | 12 |
| Key generation/distribution | 0 | 1 | 1 | 2 | 3 | 3 | 1 | 11 |
| Protocol/traffic/cryptanalysis | 1 | 1 | 0 | 1 | 3 | 2 | 1 | 9 |
| PQC migration (contextual) | 0 | 0 | 0 | 1 | 2 | 5 | 1 | 9 |
| Federated/privacy FL | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 4 |
| Learned primitives | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 3 |
| Side-channel analysis | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 2 |
| Total | 4 | 14 | 6 | 18 | 29 | 30 | 8 | 109 |

### 3.4 Data landscape and validation practice
Data sources: Testbed/OTA measurement 43, Collected datasets/traces 19, Simulation 15, Analysis/benchmark 3, Unclear from abstract 29 (Fig. d_fig4_dataval left). Validation: Testbed/field demonstration 45 (41%), Cross-domain/generalization 22 (20%), Simulation-only 13 (12%), Standard split/unclear 28, Benchmark/analysis 1 (right panel). Crossing validation with function substantiates the headline: threat papers skew measured (far-field BLE at 15 m, LoRa captures, SDR impersonation, O-RAN OTA), while key generation and DRL anti-jamming carry the simulation-only mass. Readiness means per track: threat R1 1.65 / R2 1.19 / R3 0.26 / R4 0.06 / R5 0.16; defense R1 1.17 / R2 0.94 / R3 0.25 / R4 0.03 / R5 0.09; both (n=4) R2 0.25; PQC-context R3 1.11 / R5 0.56 — the only stratum with real cost and standards numbers (ESP32 DTLS 313 ms, sub-12 kB Dilithium, Cortex-M4 cycles; FIPS 203/186, 3GPP, 802.11, O-RAN references).

Table 4. Data sources recurring across the corpus.
| Data source | Papers | Typical use |
|---|---|---|
| Testbed/OTA measurement | 43 | SDR captures, LoRa/Wi-Fi/UAV field demos |
| Collected datasets/traces | 19 | WiSig-style RFFI, RF-SCA trace sets |
| Simulation | 15 | Keygen channels, DRL jamming games, PLS optimization |
| Analysis/benchmark | 3 | Proofs, systematizations |
| Unclear from abstract | 29 | Body-text resolution pending |

Table 5. Validation practices.
| Validation | Papers | Interpretation |
|---|---|---|
| Testbed/field demonstration | 45 | Deployment-relevant; threat-cluster norm |
| Cross-domain/generalization | 22 | Strongest lab protocol; defense-cluster best |
| Simulation-only | 13 | Model-fidelity dependent; keygen/DRL-heavy |
| Standard split/unclear | 28 | Optimistic without isolation argument |
| Benchmark/analysis | 1 | No primary validation |

Reading the panels together: the field's empirical base is bifurcated, not uniformly weak. Attacks are demonstrated; defenses are benchmarked. The studies that escape the trap treat evaluation design as the contribution: cross-receiver, cross-day, open-set, and OTA-adversarial protocols.

### 3.5 Sensitivity analysis: does preprint inclusion distort the picture?
Because the corpus includes 30 reputable arXiv preprints (27.5%), headline findings could in principle be a preprint artifact: if preprints systematically report weaker validation, the corpus would understate the peer-reviewed field. A peer-reviewed-only rerun (n=79) rejects this: validation mix nearly identical (testbed 42% vs 41%; sim-only 9% vs 11%; cross-domain 23% vs 24%), method ranking preserved (adversarial 27 = deep-supervised 27). Preprints contribute recency (2025–2026 adversarial + open-set work), not a different evidentiary standard. Two caveats: preprints are version-frozen by ID+version+date and any later published version supersedes; and the sensitivity set is a stratification, not an independent sample. Within those bounds, preprint inclusion buys velocity without buying bias — and the observation that neither stratum reports reproducibility systematically strengthens the case for the checklist in §8.

## 4. AI-Enabled Threats: What the Corpus Demonstrates
RFF/authentication attacks form the densest cluster: white-box FGSM/PGD on real LoRa captures, black-box UAP at 81.7% with ~no victim knowledge, RL impersonation at >90% from binary feedback, GAN-spoofing at 76% PHY-auth pass, backdoors surviving Neural Cleanse/STRIP and working model-agnostically, fingerprint erasure as privacy attack. EM/RF side-channels move key recovery over the air at meters: BLE AES-128 at 15 m from <400 traces, nRF AES-CCM at 1 m, BLE re-keying LTK leakage in ~30 traces. Protocol/traffic attacks show the stack above PHY is equally exposed: LTE/5G AKA+RRC fuzzing (119 vulns/93 CVEs), padding/shaping defeated by packet-size distributions, LLM-assisted baseband fuzzing (7 vulns, 3 CVEs, 542 phone models). Critical assessment: attacks are evaluated against real systems with stated — often weak but honest — threat models (strong R2, narrow R1). The missing attack science is adaptive-defense evaluation: most stop at undefended classifiers, which is why Magmaw matters — it survives adversarial training, subtraction, detection, and oracle defenses.

Table 8 (excerpt). Representative studies by function and family: study summary (data basis; headline contribution).
| Function | Family | Representative studies |
|---|---|---|
| RFF/auth attack | Adversarial | White-box LoRa break (captures; FGSM/PGD vs CNN/LSTM/GRU); black-box UAP 81.7% (captures; no victim knowledge); RL impersonation >90% (SDR; binary feedback); GAN-spoof 76% (OTA; PHY-auth pass) |
| Side-channel | Deep supervised | Far-field BLE AES-128 at 15 m <400 traces (OTA; far-field DL-SCA); nRF AES-CCM at 1 m (RF-SCA); BLE LTK in ~30 traces (re-keying leak) |
| Protocol/traffic | Fuzzing/ML | AKA+RRC fuzzing 119 vulns (testbed; cellular auth-link); LLM baseband fuzzing 3 CVEs (phones; foundation-assisted); padding defeat (traces; traffic-shape exploit) |
| Universal PHY | Adversarial | Magmaw NDSS'25 (SDR; protocol-agnostic UAP vs encrypted link) |
| Defense RFFI | Robust/open-set | Contrastive, receiver-agnostic, open-set/few-shot, proactive authentication (captures; accuracy under shift) |
| Keygen | Deep/DRL | KDR/KGR improvements (mostly simulation; reciprocity + IRS/relay) |
| Anti-jamming | DRL | Relay/power/secrecy-rate control (simulation-leaning; online-acting) |
| PQC-context | Implementation | ML-KEM DTLS 313 ms on ESP32 (hardware; compute fine, bandwidth blocks); WKyber/LAKE (bandwidth attacks) |

## 5. AI-Assisted Defenses: What the Corpus Demonstrates
RFF/PLA defenses chase domain shift: contrastive embeddings, receiver-agnostic training, open-set/few-shot enrollment, proactive authentication — accuracy under shift, rarely under attack. Key generation defenses improve KDR/KGR mostly in simulation. DRL anti-jamming optimizes relay/power/secrecy-rate without onboard-cost reporting. Federated privacy proves differentially private OTA aggregation at small scale. Critical assessment: the wall between §4 and §5 is the finding — only ~13% evaluate attack and defense together. RFF accuracy ≠ authentication; domain-shift misclassification is itself exploitable. The defense literature's strongest protocols (cross-receiver, cross-day, open-set) are exactly the threat literature's attack surface.

## 6. Quantum-Era Context (Separate Stratum)
Compute is feasible on ESP32/Pi-class hardware (ML-KEM DTLS 313 ms, beating classical baselines; sub-12 kB Dilithium; Cortex-M4 cycle counts); bandwidth expansion is the blocker; WKyber and LAKE attack exactly that. AKA-linkability analyses make harvest-now concrete for short-range radio. No in-set paper joins AI-threat × PQC — recorded as a gap (§8), kept separate as thesis hygiene requires.

## 7. Cross-Cutting Directions
Closed-loop evaluation (§§4–5 wall), autonomous trust (real-time deadlines unbenchmarked; OTA crypto-agility essentially unaddressed; multi-agent trust in 1–2 papers while FL-for-drones falls to deauth→impersonation chaining), and reproducibility (code/data signals ~3%; WiSig-style datasets reused far more than released) are the three cross-cutting threads. The field optimizes estimators while adversaries optimize exploitability — a mismatch no single-function advance can fix.

## 8. Research Gaps and Future Directions
Table 10. Structural gaps and directions.
| Gap | Evidence | Direction |
|---|---|---|
| Closed-loop evaluation | ~13% attack+defense jointly | Adversarial-benchmark suites with OTA mandates |
| Reproducibility | ~3% release signals; R4 ≤0.06 | Artifact-evaluated security tracks; dataset DOIs |
| Standards alignment | ~7%; RFF nearly zero; R5 ≤0.16 | Authentication profiles (3GPP/IETF) for learned PHY-auth |
| Onboard cost | DRL/semantic cost-silent; defense R3 0.25 | Latency/energy/memory as required reporting |
| Autonomous trust | 1–2 papers | Real-time auth, OTA agility, swarm insider models |
| AI×PQC join | 0 papers | ML-SCA of PQC over the air; migration prioritization |

Table 11. WIRELESS-AI-RC reporting checklist.
| # | Item | Must report |
|---|---|---|
| 1 | Dataset/testbed identity | Name, version, download or testbed description |
| 2 | Device/link population | Radios, channels, distances, day/receiver splits |
| 3 | Adversary model | Knowledge, capability, RF/compute budget |
| 4 | Split protocol | Within/cross-receiver/day/domain + isolation argument |
| 5 | OTA vs simulation | Declaration; sim-only flagged as such |
| 6 | Closed-loop evaluation | Attack paper: defenses tested; defense paper: attacks tested |
| 7 | Baselines | ≥1 classical alongside proposed method, identical data |
| 8 | Randomness | Seeds or repeated-run statistics |
| 9 | Uncertainty | Error bars, not point estimates alone |
| 10 | Onboard cost | Latency/energy/memory on stated platform |
| 11 | Failure analysis | ≥1 documented failure mode + distribution |
| 12 | Artifacts | Code/data DOI or explicit exemption |

## 9. Conclusion
Three conclusions stand out. First, the method center moved from fingerprint classifiers to adversarial science — attacks are cheap, realistic, and OTA-demonstrated. Second, the application center stayed in RFFI accuracy, which is not authentication — defenses are rarely adversarially evaluated. Third, readiness does not follow publication volume: reproducibility, standards, onboard cost, and autonomous-trust evidence lag years behind accuracy claims. If the last five years were about discovering what learning can extract from radio signals, the next five will be decided by what it can be trusted to protect — under adaptive adversaries, on constrained radios, at fleet scale.

## Declarations
Funding. No specific funding for this work. Conflicts. None declared. Author contributions. H.T.S. conceived the study, designed and executed the search, screening, and verification pipeline, performed classification and analysis, and drafted the manuscript. S.S.I.A. and J.I.C. contributed to corpus curation, verification, and revision. Data availability. dataset_papers.csv, abstracts.json, screening_log.csv, retrieval/ released with the paper. Code availability. Coding + figure scripts rerunnable from the released dataset. Ethics. Not applicable. AI use. AI-assisted pooling, drafting, and editing; all references DOI/arXiv-ID verified; counts regenerated programmatically; authors take full responsibility.
