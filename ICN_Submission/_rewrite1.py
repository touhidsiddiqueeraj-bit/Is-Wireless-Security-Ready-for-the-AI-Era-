#!/usr/bin/env python3
"""Journal rewrite of the v9 body -> ICN submission structure.

Applies prose edits only. No number in the corpus is changed; every edit that
touches a count keeps the v9 value. Structure is remapped onto the journal's
required Introduction / Method / Results / Discussion / Conclusion skeleton.
"""
import pathlib

SRC = pathlib.Path(__file__).with_name("_body.tex")
OUT = pathlib.Path(__file__).with_name("_body2.tex")
s = SRC.read_text(encoding="utf-8")

EDITS = []


def rep(old, new):
    EDITS.append((old, new))


# ---------------------------------------------------------------- structure
rep(r"\section{Review Methodology}",
    r"\section{Method}")
rep(r"\section{Corpus Overview and Six-Year Evolution}",
    "\\section{Results}\n"
    "\\subsection{Corpus overview and six-year evolution}")
rep(r"\section{AI-Enabled Threats: What the Corpus Demonstrates}",
    r"\subsection{AI-enabled threats}")
rep(r"\section{AI-Assisted Defenses: What the Corpus Demonstrates}",
    r"\subsection{AI-assisted defenses}")
rep(r"\section{Quantum-Era Context (Separate Stratum)}",
    r"\subsection{Quantum-era context}")
rep(r"\section{Cross-Cutting Directions}",
    "\\section{Discussion}\n" r"\subsection{Cross-cutting directions}")
rep(r"\section{Research Gaps and Future Directions}",
    r"\subsection{Research gaps and future directions}")

# subsections of the corpus overview become the third level
for h in ["Publication trend", "Method-family evolution",
          "Application-area distribution",
          "Data landscape and validation practice"]:
    rep("\\subsection{%s}" % h, "\\subsubsection{%s}" % h)
rep(r"\subsection{Sensitivity analysis: is peer review too slow for AI security?}",
    r"\subsubsection{Sensitivity analysis: is peer review too slow for AI security?}")

# ------------------------------------------------- reader guide at Results
rep(r"""\subsection{Corpus overview and six-year evolution}
\label{sec:corpus}""",
    r"""\subsection{Corpus overview and six-year evolution}
\label{sec:corpus}
Two kinds of number appear in this section. Composition numbers---how many papers do
what, in which venue, with which method family---carry measured inter-coder agreement of
0.68--0.84 (\S\ref{sec:reliability}) and can be read as counts. Readiness numbers---attacker-model
explicitness, evaluation realism, cost, standards---carry agreement of 0.11--0.76, and the
weakest items bound rather than certify any level comparison. Where a quantity depends on a weak
item it is given as an upper bound or a range, and the underlying codings are released.""")

# ------------------------------------------------------------- method: search
rep(r"""The seeded path went from 126 unique candidates, screened against a validity floor (V1 peer-reviewed, in range, and retrievable; V2 evaluable evidence; V3 traceable claims), to 109 included records, 12 background survey-only landmarks, 4 backup needs-check rows (D51/T26/T29/P07, held), and 1 title-gate exclusion (T24, EAP-AKA with no AI link). The first OpenAlex path went from 894 hits to 662 unseen records, title-gated to 130 candidates, and abstract-level V1--V3 screening produced 14 included (D70--D77, T41--T46), 2 background (BG10, a systematic O-RAN analysis; BG11, a conceptual QML plan---both without primary mechanism), and 1 exclusion (EX01, no crypto link); the remainder were out-of-scope surveys, non-radio, or IDS-only work. A rerun on 2026-10-12 went from 994 hits to 743 post-deduplication, title-gated to 136, and produced 12 included (D78--D88, T47) plus 8 exclusions with logged reasons.""",
    r"""The seeded path went from 126 unique candidates, screened against a validity floor (V1 peer-reviewed, in range, and retrievable; V2 evaluable evidence; V3 traceable claims), to 109 included records, 12 background survey-only landmarks, 4 backup needs-check rows held for later screening, and 1 title-gate exclusion (an EAP-AKA scheme with no AI link). The first database run went from 894 hits to 662 unseen records, title-gated to 130 candidates; abstract-level screening produced 14 included records, 2 background entries (a systematic O-RAN analysis and a conceptual quantum-ML plan, neither with a primary mechanism) and 1 exclusion (no cryptographic link), the remainder being out-of-scope surveys, non-radio, or intrusion-detection-only work. A second database run went from 994 hits to 743 post-deduplication, title-gated to 136, and produced 12 included records plus 8 exclusions with logged reasons.""")

rep(r"""An adjudication pass then applied scope and deduplication cuts to the merged 135 (T02 subsumed by T03; T07 without AI content; T35 without a crypto link; T45 without a radio link; T34 moved to background under the sensing rule) and moved T05/T14 to dual-track under one stated rule. The final corpus is 130 included studies (121 core: 84 defense, 30 threat, 7 both, plus 9 PQC-context), 15 background (13 seeded-origin including T34, plus BG10/BG11), 4 backup, and 14 excluded (T24, EX01, T02, T07, T35, T45, and 8 rerun-screened records).""",
    r"""An adjudication pass then applied scope and deduplication cuts to the merged pool: one record was subsumed by a later version of the same work, one carried no machine-learning content, one no cryptographic link, and one no radio link, while one moved to background under the sensing rule; two further records were reclassified as dual-track under a single stated rule. The final corpus is 130 included studies (121 core: 84 defense, 30 threat, 7 both, plus 9 post-quantum context), 15 background, 4 backup, and 14 excluded.""")

rep(r"""Ten rerun rows were subsequently confirmed as published (venue and DOI resolved 2026-10-11), a second resolution round confirmed nine more, and a third confirmed nine of the remainder (D25 CAMAD21, D35 GC Wkshps23, D38 Wireless Commun24, D49 Network25, D50 ISCC23, D53 Commun Lett24, T09 TCCN21, T14 TMC23, T19 WPES22).""",
    r"""Three venue-resolution rounds subsequently confirmed 28 of the newly merged rows as published, each with a resolved DOI (\texttt{found\_papers.csv}).""")

rep(r"""The final corpus carries 19 preprints (14.6\%): 14 venue-unconfirmed arXiv-only entries (D33, D39, D42, D45, D63, D74--D76, T36, T42, D82, D84, D85, T47), 2 presented-or-preliminary rows (D26 presented at ICC per the authors; T05 MILCOM23 preliminary with a 2024 full version), 1 submitted row (D46; stated INFOCOM target inconsistent with its August-2026 posting, held as submitted/unconfirmed), and 2 author-claimed rows (D48, ICASSP per arXiv comment; P09, accepted per Standards Magazine---neither with a proceedings record found). No entry changed status without a logged resolution.""",
    r"""The final corpus carries 19 preprints (14.6\%): 14 venue-unconfirmed arXiv-only entries, 2 presented-or-preliminary rows, 1 submitted row (a stated target conference inconsistent with its posting date, held unconfirmed), and 2 author-claimed rows without a proceedings record. No entry changed status without a logged resolution; the individual dispositions are listed in Table~\ref{tab:corpus} and in the released dataset.""")

# --------------------------------------------------- method: criteria / ad judication
rep(r"""and duplicate (one same-team conference-to-journal extension deduped, T02 subsumed by T03, while two same-team companion pairs were counted as distinct records with disclosure---D55/T15 and D20/T20---each with a drop-one-pair sensitivity check).""",
    r"""and duplicate (one same-team conference-to-journal extension deduplicated, while two same-team companion pairs were counted as distinct records with disclosure, each under a drop-one-pair sensitivity check).""")

rep(r"""Adjudication rulings, all logged: domain-informed cellular fuzzing without ML content is excluded for failing AI involvement (T07, consistent with the T24 exclusion); Wi-Fi localization-fingerprint attacks count where a geofence bypass breaks an authorization boundary (T42, included on that ground rather than on a forgery-breaks-authentication claim); signal-classifier attacks count where the classifier is the security boundary (T44, under the D36/D37 precedent); IoT traffic-classifier attack-plus-defense counts as dual-track protocol work (T46); wireless-FL-privacy work counts where the privacy guarantee is produced by channel properties (over-the-air superposition, channel-noise differential privacy)---a physical-layer mechanism under the D24 precedent---while generic FL-application papers without a channel-produced guarantee are excluded; acoustic/vibration side-channel analysis of PQC fails the radio-link population (T45, moved to related work); Wi-Fi sensing without a security link moved to background (including T34); 5G regression-robustness work without a security boundary excluded (T35); and Xplore-hosted rows counted as peer-reviewed because Xplore hosts only peer-reviewed content, subject to venue reverification at full-text read. The same rule was applied to venue claims in both directions: author-claimed venues without a proceedings record were coded preprint (D26, T05 preliminary, D46 submitted, D48, P09 accepted), while author claims confirmed by a publisher record stayed peer-reviewed (D41 TVT, D52 TCCN, T28 USENIX proceedings).""",
    r"""The boundary rulings were applied consistently and are logged in full in the released screening log. Cellular fuzzing without machine-learning content is excluded for failing AI involvement; Wi-Fi localization-fingerprint attacks are included where a geofence bypass breaks an authorization boundary, rather than on a forgery-breaks-authentication claim; signal-classifier attacks are included where the classifier is the security boundary; IoT traffic-classifier attack-plus-defense work counts as dual-track protocol work. Wireless federated-learning privacy counts where the privacy guarantee is produced by channel properties (over-the-air superposition, channel-noise differential privacy)---a physical-layer mechanism---while generic federated-learning applications without a channel-produced guarantee are excluded. Acoustic and vibration side-channel analysis of post-quantum schemes fails the radio-link population; Wi-Fi sensing without a security link moved to background; 5G regression-robustness work without a security boundary is excluded. The venue rule was applied in both directions: author-claimed venues without a proceedings record were coded preprint, while author claims confirmed by a publisher record stayed peer-reviewed.""")

rep(r"""All screening, eligibility coding, and charting were performed by the review team against the stated rubric. Inter-rater reliability was not formally assessed; the complete coded dataset is released as \texttt{dataset\_papers.csv} so independent researchers can check, correct, or extend any record. Every record also carries a resolvable identifier checked against Crossref, arXiv, ACM, or USENIX; record-level corrections re-keyed D20 (true TVT paper) and D55 (true TCCN paper), corrected D31 year 2024$\rightarrow$2025 and T38 year 2021$\rightarrow$2022 to published versions, confirmed T03 (TMC 2026) and T28 (USENIX Security 2026 proceedings) as published, and recoded D48 to preprint (ICASSP per author comment only).""",
    r"""All screening, eligibility coding, and charting were performed by the review team against the stated rubric, and the complete coded dataset is released as \texttt{dataset\_papers.csv} so independent researchers can check, correct, or extend any record. Every record carries a resolvable identifier checked against Crossref, arXiv, ACM, or USENIX; record-level corrections applied during verification (re-keyed venue attributions, two year corrections to published versions, two preprint recodings) are logged in the released run log.""")

for old, new in EDITS:
    n = s.count(old)
    assert n == 1, (n, old[:70])
    s = s.replace(old, new)

pathlib.Path(OUT).write_text(s, encoding="utf-8")
print("applied", len(EDITS), "edits ->", OUT.name, len(s), "chars")
