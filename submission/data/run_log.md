# Retrieval run log — open-web sourcing (Round 1, 2026-10-11)
Method: web-search sourcing, NOT the database runs in searches.md. Scopus/IEEE/ACM strings still need running with institutional access. These candidates seed screening; they do not replace per-database hit counts.

| round | query focus | results returned | kept |
|---|---|---|---|
| 1 | DL RF fingerprinting authentication | 10 | T02-link, D05, D06, B03, B04-lead |
| 2 | ML side-channel wireless AES key | 10 | T01, T08-lead |
| 3 | neural crypto / PHY security ML era | 10 | D07, B02, D01-lead |
| 4 | ML PHY authentication / key generation | 10 | D02-lead, D03, D04 |
| 5 | adversarial neural crypto (Abadi line) | 10 | D01, B01 |
| 6 | LTE/5G fuzzing + RL RRC fuzzer | 10 | T07 |
| 7 | HNDL + PQC constrained IoT | 10 | P01, P02-lead |
| 8 | adversarial RFFI LoRa ICC 2023/2024 | 10 | T02, T03, T04, D07, D08-lead, T05 |
| 9 | verify Guo-TIFS DOI + Ma-ICC venue | 5+10 | D02 venue confirmed, T03 journal confirmed |
| 10 | GAN/signal spoofing (WiseML line, Wi-Spoof, impersonation) | 10 | T09-lead, T10, T11-lead |
| 11 | 5G AKA formal analysis / fuzzing (Basin, 5GReasoner, SoK, EAP-AKA) | 10 | B05, B06 (pre-range); T23-lead, T24-lead |
| 12 | encrypted traffic analysis (Engelberg, WCNC19, WiSec23, TIFS-ATVITSC) | 10 | T19-lead, T20-lead, T21-lead, T22-lead |
| 13 | AMC adversarial attack+defense (ADE, TIFS-EH-AT, LI-waveform) | 10 | D36, D37, T25-lead, T26-lead |
| 14 | PHY keygen ML (VTC22, IRS-ICC23, KGNet, WiseML21, NCIC23) | 10 | D09, D10, D11-lead, D12, D13 |
| 15 | DRL anti-jamming + UAV secrecy (WCNC24, TWC-swarm, TMC24, ICOIN24) | 10 | D14, D15, D16, D17, D21-lead, D22-lead |
| 16 | V2X/UAV auth (V2I-hybrid, TWC-UAV-PLA, TVT25, SecureLink) | 10 | D18, D19-lead, D20-lead, D32-lead |
| 17 | ANC follow-ups (RANDOM, CPA-ANC chain) | 10 | D33-lead |
| 18 | backdoor/Trojan/MIA wireless (ICCCN23, INFOCOMW24, TMLCN24) | 10 | T12, T13-bg, T14-lead, T15-lead, T16, T17 |
| 19 | wireless FL privacy (PFELS-TDSC, LDP, HW-impairments, CJ) | 10 | D23, D24-lead, D25-lead, D26-lead, T27-grey |
| 20 | PQC embedded (ACNS22, Access24, TCHES21, Kyber-HW) | 10 | P03, P04, P05, P06-lead, P07-lead |
| 21 | open-set RFFI (MTPL, JRFFP-SC, few-shot, SRP-CBL) | 10 | D27-lead, D28-lead, D29-lead, D30-lead, D31-lead |
| 22 | LLM fuzzing 5G baseband (ConSeT, model-based) | 10 | T28, T29-lead |
| 23 | recent PHY-keygen (RIS, fluid antenna, FDD multi-env, group) | 10 | D38-lead, D39-lead, D40-lead, D41-lead, D42-lead, D43-lead |
| 24 | OTA adversarial (Magmaw, O-RAN, MobiCom-WiFi, 5G regression) | 10 | T30, T31, T34, T35-lead, T33-lead |
| 25 | PQC-wireless (WKyber, QS-6G, PQ-entropy, LAKE) | 10 | P08-lead, P09-lead, P10-lead, P11-lead |
| 26 | RFF transformers/contrastive (ICC24, MILCOM24, ContraCSI, HoRFFI) | 10 | D44, D45-lead, D46-lead, D47, D48-lead, D49-lead, D50-lead |
| 27 | UAV/drone-ML (SecureLink, ZAPS-skip-no-AI, swarms, ZTA, chained-FL) | 10 | T36, D51-lead (ZAPS excluded: no AI link) |
| 28 | semantic/ISAC security (TCCN25, DeepSSC, ISAC-SoK-bg) | 10 | D52, D53-lead, B08 |
| 29 | FL poisoning (WFL-SoK-bg, AirComp-Byzantine) | 10 | B09, D54-lead |

Yield round 3: 108 rows = 37 verified + 2 verified-borderline + 59 needs-check + 10 background.

## Evidence-read pass (2026-10-11): 118 rows
- T15/T18/T25 venue-confirmed via lab pages + publisher DOIs (GLOBECOM21, ICC21 DOI 10.1109/ICC42927.2021.9500893, URSI-GASS21 DOI 10.23919/URSIGASS51995.2021.9560360) → verified.
- 10 spin-offs from reference lists (TCCN21 authorization, IoT-J21 threat, JSAC21 LoRa, TIFS22 impairment, TCCN23 Bluetooth, TWC24 low-SNR, WiseML20 generalized attack, TIFS-adversarial-study, DeepCRF, WCL25 open-set).
- 16 arXiv-conditionals promoted on abstract-level V2 (flagged PREPRINT full-text-read-pending).
- Count: 63 verified + 2 borderline + 43 needs-check + 10 background. Preprint share of countable set ≈ 25/65 ≈ 38% — inside the 40% cap, no headroom: further preprint adds require peer-reviewed conversions first.

## Conversion blitz (2026-10-11): READY — 125 rows
- arXiv API batch (20 IDs): D41→TVT, D48→ICASSP, D54→ICC-Workshop, P09→Comm-Standards-Mag, T40→MILCOM25+DOI, D28→IoT-J+DOI; authors fixed D38/D49/D50/P10/D41.
- Adjudications: T07 INCLUDED (AKA/RRC fuzzing = auth link); T10→background (sensing, no crypto); T24 DELETED (EAP-AKA, no AI link); P02→background (survey).
- Xplore-hosted = peer-reviewed rule: promoted D21/D22/D27/D29/T11/T21/P06 (venue detail pending full-text read).
- Crossref: D20→CPS-IoT Week 2023; CSDL listings: D61/D68/D69, D66 (TCCN24), D67 (TrustCom25+DOI).
- Final: 109 include (100 core: 65 defense / 31 threat / 4 both; 9 PQC-context) + 12 background + 4 backup (D51/T26/T29/P07 need-check) + T24 excluded. Preprints 30/109 = 27.5%.
- screening_log.csv pre-filled (agent-screened; verifier blind-checks 20%).
- Still yours: verifier 20% re-screen + κ, full-text reads (esp. 30 preprints), database runs (searches.md) for PRISMA flow counts, pre-submission rerun.

## Reverify sweep (2026-10-11, post-restart): all 17 flags cleared by DOI/metadata curl
- Crossref works API: D18→TWC vol 24 pp 2722-2733; D37→TIFS vol 20 pp 3731-3744; D21→TCE Nov 2025; D22→TVT Apr 2023; D27→WCL Mar 2025; D29→Commun Lett Sep 2025; D60→TIFS 2025; D69→TMC Feb 2026; P06→TCAS-I Feb 2025; T11/T17→TMLCN 2024; T20→ACM CPS-IoT Week 2023; T21→AIIoT May 2025; D30→ICC 2025; D61→TMC Nov 2025 (OpenRFI).
- S2 search API: D68→ISCC 2025; T06→journal version TNSE 2025 (DOI 10.1109/TNSE.2025.3568824).
- P11: venue as stated on eprint (proceedings verification pending at full-text read) — sole surviving caveat.
- Year corrections propagated to dataset, draft §3.1, pattern memo, Fig. 2b (now 2024:29/2025:30).

Yield round 2: 77 rows total = 30 verified + 2 verified-borderline + 38 needs-venue-check + 7 background (of which PQC-context: 4 verified + 3 needs-check).

## 2026-10-11 amendment: preprints now countable
Policy change (protocol §2, searches §5b): reputable arXiv preprints count, split-reported vs peer-reviewed, ≤40% cap + sensitivity check. Immediate effect: 19 arXiv-sourced needs-check rows become countable pending V2/V3 evidence read (all above except P02-survey). Projected countable after evidence reads: ~30 verified + ~19 arXiv + ~14 venue-confirmations ≈ 60+. Remainder to ~100 via database runs + reference snowballing.
Rerun due: week before submission (log date + delta here).

## Venue-resolution + venue-velocity build (2026-10-11)
- Full resolution pass on 24 weak-bib rows (arXiv API + Crossref works/title search): 18 confirmed with authors+venue+DOI (D07→TMC DOI 10.1109/tmc.2023.3340039; D11→IoT-J 2021; D13→NCIC; D15→TWC; D19→ISNCC; D31→Sensors; D32→IoT-J DOI 10.1109/jiot.2025.3631020; D34→WCNC 2022; D40→WCSP 2025; D54→ICC Workshops; P04→IEEE Access; P08→IEEE Access 2025; P10→LNNS chapter; T08→ISMVL; T23→ACM WiSec 2025; T27→INFOCOM 2026; T34→MobiCom; T40→MILCOM; +T06→TNSE journal, D30→ICC 2025 confirmed published).
- 4 Crossref hits REJECTED after title/author verification (D42: Jia et al. different paper; D45: 2013 SIU; D46: 2021 WMCS; T35: no authors — kept preprint). D25/D46 confirmed submission-only.
- 10 rows flipped preprint→peer-reviewed; published-version year corrections D34→2022, T23→2025, T27→2026, P10→2025. New totals: 90 peer (53 journal + 37 conference) + 19 preprint (17.4%); years 4/13/7/18/28/31/8. Backups: /tmp/*.bak.
- Added venue_channel (journal/conference/preprint) to dataset_papers.csv. dataset_used column SKIPPED: zero named-benchmark mentions in 75 abstracts, so F-A tracks evidence grade over time instead.
- 3-way sensitivity result: frontier methods debut in conferences/preprints ~1 yr before journals (AdvML 2020 vs 2021; DRL 2022 vs 2023; DeepSup 2020 vs 2021); adversarial share conf 41% / pre 37% / journal 28%; R2 means journal 0.94 / conf 0.92 / pre 1.32 (rigor counter-argument fails in-corpus; preprint R2 partly selection). Claim framed as bounded finding with 3 caveats (§3.5).
- 5 new figures (FigA validation-mix, FigB method×track, FigC milestones, FigD layered coverage, FigE venue velocity), all generated + visually verified; §3.5 rewritten; abstract/§3.1/Table 3/conclusion updated; 24-page clean compile.

## OpenAlex database run + round-3 resolution (2026-10-11)
- OpenAlex: 10 topical queries → 894 hits (Q7 FL query rate-limited 429, retried 9x; 9/10 complete) → dedupe vs 1,945 records → 662 unseen → title gate → 130 candidates. Scripts: submission/code/openalex_run.py, openalex_gate.py; records: openalex_records.json, openalex_new_candidates.json, openalex_gated.json.
- Abstract screening (shortlist_abstracts.json via OpenAlex abstract index): 14 included (D70-D77, T41-T46), 2 background (O-RAN systematic analysis w/o primary mechanism; QML keygen plan w/o evaluable evidence), 1 excluded (Safe Exploration TIFS, no crypto link). Scripts: fetch_shortlist.py, add_openalex_includes.py.
- Round-3 bib: 9/14 confirmed published (D25→CAMAD21, D35→GC Wkshps23, D38→IEEE Wireless Commun24, D49→IEEE Network25, D50→ISCC23, D53→Commun Lett24, T09→TCCN21, T14→TMC23, T19→WPES22); 8 hits rejected (wrong papers). Year corrections per published version.
- Final: N=123 (114 core: 73 defense/36 threat/5 both + 9 PQC; 109 peer: 63 journal/46 conf + 14 preprint 11.4%); years 3/12/8/21/32/34/13; AdvML=DeepSup=42; DRL defense-only (9); first AIxPQC join [T45] (proximity SCA, OTA still absent). 8 arXiv-only rows remain (confirmed no publication record).
- Manuscript 26 pages/14 figures, zero-warning compile. Remaining: Scopus/IEEE/WoS (no access), 8 bibs, verifier κ.

## OpenAlex rerun + round-4 screening (2026-10-12; corpus stays frozen at N=123)
- Rerun: same 10 queries, to-date 2026-10-12 → 994 hits (+100; 10/10 complete, incl. Q7 FL query that was 429-limited on 10-11) → dedupe vs updated corpus → 743 post-dedupe → title gate (same keyword gate) → 136 gated, of which 116 were already gated 10-11 and 20 are new. Rerun script: /tmp/oa_rerun.py (copy of openalex_run.py, outputs kept out of prod files); records: submission/code/round4_fresh_gated.json (20), round4_abstracts.json (OpenAlex abstract-index reconstructions).
- Abstract-level V1–V3 screening of the 20 (wireless AND crypto/auth/key/PLS AND AI; peer/arXiv; evaluable evidence; D24 federated-privacy precedent applied):
  - 12 ELIGIBLE, held as logged backlog pending full-text reads (NOT merged; N stays 123): 4 RFFI defense (VTC21 RFFResNet 10.1109/vtc2021-fall52928.2021.9625375; WCNC23 wavelet-scattering 10.1109/wcnc55385.2023.10119009; FutureG25 AI-assisted RFF 10.14722/futureg.2025.23009; Access20 deep complex ResNet 10.1109/access.2020.3037206), 7 wireless-FL-privacy defense (MAMAB-DP 10.48550/arxiv.2106.13039; A-FADMM TCOM21 10.1109/tcomm.2021.3078783; xMK-CKKS-HE arXiv 10.48550/arxiv.2605.30123; DWFL arXiv 10.48550/arxiv.2109.09142; ISIT21 privacy amplification 10.1109/isit45174.2021.9518031; IET24 DP-FL multi-BS 10.1049/cmu2.12722; AFL-UAV JSAC21 10.1109/jsac.2021.3088655), 1 FL-jamming threat (arXiv 10.48550/arxiv.2201.05172).
  - 8 EXCLUDED with reason: 2 surveys without primary mechanism (6G-CPS closed-loop survey arXiv 10.48550/arxiv.2606.08173; healthcare FL review 10.3390/healthcare12242587); 2 already-included/duplicates (PFELS arXiv 10.48550/arxiv.2304.07460 = D23; IET-paper arXiv version 10.48550/arxiv.2208.11848); 2 sensing/applied systems without crypto-AI link (LoRa-RFID attendance 10.52700/scir.v7i2.189; perimeter drone-detection 10.3390/drones9010043); 1 pure IDS without crypto link (FL-IDS UAV 10.1016/j.iot.2025.101592); 1 application paper without security mechanism (air-quality FL 10.48084/etasr.7820).
- Net effect on evidence base: none (frozen N=123; all counts/figures unchanged). Pre-submission merge of the 12 requires full-text reads + 6-field coding + consistency-gate update; the delta is dominated by the previously rate-limited Q7 query (coverage artifact, not one-day field growth).

## v4 revision (reviewer v3 major-revision repair; N=123 → N=130)
- Evidence checks (all verified, no fabrication): T03 abstract covers T02's FGSM/PGD + adds UAP → T02 deduped; T07 abstract has no ML content → excluded (T24-consistent); T35 is 5G-regression robustness with no security boundary → excluded; T42 FooLoc explicitly names geofencing malfunction → kept on authorization-boundary grounds; D20 re-keyed to TVT 10.1109/tvt.2025.3532982 (shared DOI resolves to T20); D55 re-keyed to TCCN 10.1109/tccn.2020.3043332 (shared arXiv ID is T15's); T28 confirmed in USENIX Security 26 proceedings (pp 457-476) with artifact (Zenodo AE); T30 code release confirmed (github.com/juc023/Magmaw) → R4=1; D32 dataset release confirmed → R4=1; PfELS-arXiv = D23 (duplicate, excluded round-4).
- Merge: 12 round-4 records coded as D78-D88/T47. Cuts: T02/T07/T35/T45 excluded, T34 → background. Moves: T05/T14 → both (develops+evaluates both), T28 → Protocol/traffic function, D20 conf→journal channel, D48 → preprint channel, T28 R1/R5 upgraded from proceedings. T24 + BG10/BG11 + EX01 rows added for auditability.
- Frozen v4: N=130 (defense 84 / threat 30 / both 7 / pqc 9); years 4/17/10/21/30/35/13; channels 67→66 journal / 46 conf / 18 preprint (after T28/D48 corrections); preprints partitioned 14+2+1+1.
- Manuscript: anonymized (roles), de-changelogged, closed-loop number reported (14/130), function×validation table added, Fig.8 numeric with n/a, PRISMA-ScR checklist + protocol in archive, response letter at RESPONSE_v4.md.
- Gate: check_consistency.py rewritten for N=130 (incl. Table3 column-sum assertion, 0-dup/0-cited-in assertions); 31pp clean compile.

## v5 repair (second major revision: de-changelog + R2 audit + venue/identifier fixes)
- De-changelog: 0 matches for v4/v3/v2 patterns in manuscript (gate-asserted); abstract cut 718 -> 256 words with process detail moved to methods/supplement; initials already roles; response history kept here + RESPONSE_v4.md only.
- R2 audit: cross-tab showed Testbed/OTA all R2=2 but 21/26 Collected rows R2<2. Published rule as applied (2 = author OTA/testbed or demonstrated key recovery; 1 = controlled sim/reused-data evaluation; 0 = theory/proof/analysis without data evaluation); restored protocol rubric for sim-only rows (D11/D19/D40 reversal logged: 10-11 pass had set confirmed-sims to 0); recoded T01/T08 -> 2 (OTA/key-recovery evidence), D42/D52 -> 1, T06/T27 data -> Testbed/OTA (fulltext-logged), 11 sim-only R2=0 -> 1. Means now threat 1.30 / defense 1.06-1.08 (final 1.06); residual abstract-level R2=0s owned as conservative floor.
- Channels flipped on evidence: conferences lead journals on R2 (1.13 vs 1.06, gap 0.07); Fisher exact p~0.24 (testbed) / ~0.25 (sim) independently reproduced - prestige-gradient claims withdrawn in both directions; timing lag (adv/DRL 1yr, deep tied, PQC reversed) retained.
- Identifiers: T15/D55 proven distinct (arXiv v1 cites TCCN paper as prior work); D41/D52 Crossref-verified (stay peer-reviewed); D46 submission label corrected (year inconsistent); BG7 corrected to Adesina et al. 2023; T28 published proceedings + artifact; uniform venue rule published (publisher record = confirmed, author comment alone = preprint; D48 recoded).
- Scope: FL-privacy justified (channel-produced guarantees, D24 precedent) + with/without-7 sensitivity (N=123: defense R2 1.16, 2021 reads 12); saturation/stopping/Path-A-zero/screening-depth/verifier-CI wording corrected; closed-loop fenced as lower bound; adv split three-way (20/7/13) with figure-pooling rule stated; checklist prospective-only beyond coded items; T40 evidence pointer; Table5 proof wording; sec-venue 7 listed; non-PQC standards rate 9.9%.
- Figures: FigD Layer3 (T07 out) + Layer4 (T27/T36 corrected); Fig8 dual row + short title + numeric bands; FigC wider canvas + staggered same-year labels.

## v6 repair (third major revision: R2-mapping uniformity + N=121 framing + evidence reversals)
- R2 audit forced full mapping R2:=f(validation) (Testbed 2 / Cross,Std,Sim 1 / Bench 0; exceptions T01/T08 key recovery; T06/T27 validation->Testbed): 86 cell flips. Means now threat 1.53 / defense 1.27 / both 1.14 / pqc 1.44. Dual-lowest survives narrowed (1.14 < 1.27). Gate asserts mapping over all rows.
- Channels re-flipped: journals lead R2 (1.41 vs 1.26 conf) after reconciliation lifted journal zeros; Fisher p~0.24/0.25 reproduced but dropped from text (no-tests rule); no prestige gradient claimed either way; timing lag kept to adv/DRL.
- Evidence-grade narrative reversed to shares: testbed+cross 40% (21-22) -> ~60% (23-26); sim ~25% -> <10%; year arms n=10-35 stated.
- Framing N=121 core + 9 PQC (title kept, language narrowed); PQC non-meeting note; AIxPQC construction caveat. Seeded 126; Fig.1 counts 15bg/14excl, 105+13+12; T45 clause removed from scope.
- R3-R5 figures fenced as lower bounds with verification method (4 releases named, live-checked); T15/D55 distinct proven via arXiv-v1 citation; D41/D52 verified, D46 label fixed, BG7 corrected, uniform venue rule in-text; T28 published.
- FL-privacy kept with channel-guarantee justification + with/without-7 sensitivity recomputed post-mapping (defense 1.32 vs 1.27, threat unchanged 1.53; corrects a stale 1.16/1.13 computed pre-mapping); 2021 spike owned; saturation/stopping/Path-A-zero/screening/verifier-CI wording fixed.
- Adv split three-way (20/7/13) with figure-pooling rule; closed-loop lower-bounded 14/130 with 5-vs-7 dual sensitivity; checklist prospective-only; T40 pointer; Table5 proof wording; sec-venue-7 listed (threat 1.29: T01/T28/T30=2); standards 9.9% non-PQC.
- Presentation: methods de-run-logged; survey-comparison table (B05 dropped); glossary.md supplement; FigD/Fig8+dual-row/FigC stagger fixes; Fig.7 retitled to validation approaches.
- Verification: gate OK (mapping + Table3 + 0-dup assertions, v-history ban list); 31pp clean compile; abstract 256w.

## v7 repair (fourth major revision: earliest-date sensitivity + mapping fallout + N=121 base)
- Earliest-date audit: scripted Crossref online/print check over all 15 DOI-year mismatches. Only T06 (coded 2024, TNSE Sep 2025) and T25 (coded 2022, URSI GASS Aug 2021) were true errors - fixed. All others are DOI-numbering vs issue-year (D22 printed Apr 2023 despite tvt.2022 DOI; T09 Mar 2021; D36 arXiv Apr 2021). year_first column added (differs on P05 only: Dec-2020 online-first vs 2021 issue). Lags stand under both codings. Years now 4/18/9/21/29/36/13.
- R2 mapping fallout: dual 1.14 vs 1.27 (0.13 margin, hedged everywhere); threat 1.53 / defense 1.27; channels journ 1.40 / conf 1.26 / pre 1.32 with no-gradient stance; rescoring deltas + sign-flip owned; verifier-vs-reconciliation wording split; testbed-ownership caveat attached.
- Standards: denominator rule published (9.9% = 6 def + 1 dual + 5 attack-naming-standard over 121; 13.1% incl PQC); threat R3/R5 n/a in TableR generator; R3-R5 fenced as lower bounds.
- Depth: coding_depth column (20 body-read / 110 abstract-coded, gate-asserted); Unclear=32 subset; Fig.11/Table 8 carry depth splits; R3-R5-by-year flat (reconciles conclusion vs validation-grade improvement).
- N=121 base headlines (57.0/3.3/14.9/11.6); P09 -> preprint (no proceedings record; uniform rule).
- Stale sweep: abstract 16/30, Table 6/7/8 + Fig.9 + sect8 to 47/35/17/13, Fig.11 ~12% (only 2026 <10%), Table 3 AdvML three-way + DRL mixed row, T18 positional (dataset 2021 correct).
- Gate: mapping + FL-sensitivity + depth + Table3 + expanded ban list. 31pp clean compile, abstract ~270w.

## v8 repair (fifth major revision: mapping audit + earliest-date limits + N=121 base)
- Venue-lag audit closed: scripted Crossref online/print check over 15 mismatches (13 DOI-numbering; T06->2025, T25->2021 fixed); D36 journal issue Mar 2022 (year fixed, year_first 2021); D22 earliest evidenced Apr 2023 print (no online-first record); T09 print = coded year; month-granularity first-appearance table added; lag dropped from abstract/conclusion, hedged in sect3.5.
- R2 audit: T01 named sole override (channels imply 46 with it, 45 without); rescoring range corrected to ~0.6; verifier-vs-reconciliation wording split; dual demoted to descriptive remark (abstract/conclusion drop it); T18 confirmed RL-driven impersonation (adversarial-ML attack, not DRL family).
- Standards: denominator rule published (12 = 6+1+5 over 121); threat R3/R5 n/a in TableR; R3-R5 fenced as lower bounds; R3/R4/R5 0/1/2 distribution + by-year tables added.
- Depth: coding_depth 20/110 gate-asserted; depth_splits.csv supplement; Fig.11/Table 8 carry splits; 30-attempts/20-reads + 110-vs-32 exact.
- N=121 headlines (57.0/3.3/14.9/11.6); P09->preprint (19 total, 14.6%); stale sweep (abstract 16/30, 47/35, AdvML 2025 peak + ties, Fig.12 37/31/28, Table 3 AdvML/DRL rows, sect8); glossary + survey table kept; FigD/Fig8/FigC/FigE verified.
- Gate OK (mapping + depth + sensitivity + ban-list incl. new entries); 32pp clean compile; abstract ~260w.
