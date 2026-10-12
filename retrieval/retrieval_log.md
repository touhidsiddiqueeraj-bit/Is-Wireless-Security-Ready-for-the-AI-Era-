# Programmatic retrieval log (2026-10-11) — for §2.2
Method mirrors ML-BMS-Review §2.2 (Crossref REST API, multi-query, DOI-dedup) + arXiv API (field moves fast).

## Queries
- Crossref ×16 (rows=100, filter 2020-01-01–2026-10-11, type journal/proceedings-article): RFF-adversarial, DL side-channel AES, 5G/LTE fuzzing, encrypted-traffic fingerprinting, GAN spoofing, RF-backdoor, PHY-keygen DL, PHY-auth ML, neural crypto ANC, DRL anti-jamming UAV, wireless FL privacy, open-set RFFI, PQC Kyber/Dilithium IoT, semantic PLS, LLM fuzzing 5G, AMC adversarial defense.
- arXiv ×10 (max 50, sort submittedDate desc): RFF-adversarial, PLKG-DL, neural-crypto, anti-jamming-RL, Kyber-IoT, AMC-adversarial, FL-privacy, open-set-RFF, 5G-fuzzing, LoRa-auth-DL.

## Funnel (real counts)
| Stage | n |
|---|---|
| Retrieved (16×100 Crossref + 10×~40 arXiv) | 1945 unique (1555 Crossref + 390 arXiv) |
| Title gate (wireless AND crypto/auth AND AI terms) | 241 |
| In range 2020–2026 + venue-type ok | 241 |
| Overlap with expert-seeded 108 (title match) | 19 (+~33 by token-Jaccard ≥0.5) |
| Novel gated candidates (extension pool, UNSCREENED) | 222 → retrieval/gated.json |

## Design decision (logged, reviewer-visible)
Final evidence base = the 108 expert-seeded verified papers (fully screened, logged in screening_log.csv). The 222 novel gated records are released as an extension pool, not merged silently — merging unscreened records would corrupt the verification chain. Rationale, stated plainly as in ML-BMS §2.2: Crossref/arXiv topical recall for this IEEE/ACM-heavy, terminology-variant literature is ~50% by token overlap; registry search alone under-recovers (hence the two-path triangulation). The three following passes exist to counter seed bias: (1) programmatic pool overlap reported, (2) preprint stratum with 40% cap, (3) peer-reviewed-only sensitivity rerun.
