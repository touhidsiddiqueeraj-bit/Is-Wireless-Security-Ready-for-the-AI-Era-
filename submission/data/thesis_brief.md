# Thesis answers brief — "Is Wireless Encryption Ready for the AI Era?"
Evidence: 75 abstracts + 33 excerpt-coded rows + 1 full text (Magmaw/NDSS25). Provisional — see honesty footer.

## Central question: how well do radio-link mechanisms hold against AI-capable adversaries?
**Poorly — and the gap is widening, not closing.** Three converging lines:
1. **Learned authenticators fall to cheap, realistic attacks.** White-box FGSM/PGD breaks CNN/LSTM/GRU RFFI on real LoRa captures (T02); black-box UAP reaches 81.7% with ~no victim knowledge (T03); RL impersonation needs only binary accept/reject feedback for >90% penetration (T18); backdoors survive Neural Cleanse/STRIP (T12) and work model-agnostically (T16). Magmaw (full-text read) extends this to entire AI-native links: protocol/modality-agnostic UAPs at noise-level power (−20 to −10 dB PSR), SDR-demonstrated, surviving adversarial training, subtraction, detection, and oracle defenses — including against an *encrypted* image channel (−5.88 dB PSNR).
2. **Key extraction goes over the air.** Far-field EM DL-SCA recovers BLE AES-128 at 15 m from <400 traces (T01); RF-SCA takes nRF52832 AES-CCM at 1 m (T08); BLE re-keying leaks LTK in ~30 DL traces (T42-context). Harvest-now applies to short-range radio, not just backbone fiber.
3. **Defenses optimize the wrong metric.** ~47% of the corpus improves RFF/auth *accuracy under domain shift* (contrastive, receiver-agnostic, open-set, few-shot) while threats exploit adaptivity and shift itself (T40: domain-shift misclassification IS the backdoor). Closed-loop attack+defense evaluation appears in only ~13% (T05, D36, D37, T31, D67-proactive).

## Readiness verdicts (provisional scores, abstract-level)
- **Threat model stated:** WEAK — explicit adversary language in only ~23% of abstracts (floor; body text will raise this, but modeling attackers is clearly not the norm outside the attack papers).
- **Real adversary/cryptanalysis:** SPLIT BY KIND, not just realism rate — attacks demonstrate exploits on real captures (SDR/OTA the norm, sim-only just 1/25 coded); defenses show a fat-tailed split (measured 21/45 on collected datasets, but sim-only 10/45 — the highest sim rate in the corpus). Threat R2 ≈ high, defense R2 ≈ mixed: datasets benchmarked, adversaries rarely present.
- **Latency/energy on constrained radios:** WEAK except PQC — cost numbers in ~32% overall, concentrated in the PQC stratum (ESP32 DTLS 313 ms, <12 kB Dilithium, Cortex-M4 cycles) and lightweight-RL (D14). DRL/UAV and semantic-PLS papers almost never report onboard cost.
- **Reproducibility:** WEAK-UNKNOWN — ~4% release signals in abstracts (floor; Magmaw-class GitHub releases exist but are exceptional). WiSig-style public datasets are reused far more than released.
- **Standards alignment:** WEAKEST — ~9%. AKA/5G analyses reference 3GPP; RFF/PLA work is nearly standards-free; no authentication profile to certify against.

## Autonomous-systems gap matrix
| Need | Literature state |
|---|---|
| Real-time deadlines | DRL anti-jamming assumes training offline + acts online, but latency benchmarking vs control loops is absent; Siamese/open-set inference costs unreported (D02/D30/D61) |
| OTA-update / crypto-agility | Essentially unaddressed; PQC migration work targets handshake cost, never update mechanisms for constrained fleets |
| Multi-agent trust | D15 optimizes swarm relay/power under jamming, not insider trust; T36 demonstrates FL-for-drones falls to deauth→impersonation chaining; only SecureLink (D32) fuses cross-layer UAV identity |
| Long-lived secrets (HNDL) | BLE/AKA evidence (T01/T08/T42-context, AKA-linkability analyses) makes HNDL concrete for short-range radio; migration guidance for fleets doesn't exist in-set |

## Quantum vs AI separation (thesis hygiene)
PQC stratum tells a self-contained story: compute is fine on ESP32/Pi-class hardware; **bandwidth (ciphertext/signature expansion) is the blocker**, and the newest work (WKyber P08, LAKE P11) attacks exactly that. Zero in-set papers join AI-threat × PQC (e.g., ML side-channels against PQC over the air) — record as a gap, keep the sections separate.

## Honesty footer
Abstract-level synthesis: percentages are floors for body-text attributes (threat models, code release) but fair for abstract-absent cost numbers (authors advertise costs when they have them). Full-text reads (esp. 30 preprints) and the verifier pass could move readiness grades up one step but are unlikely to overturn the asymmetry pattern or the standards gap.
