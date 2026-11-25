#!/usr/bin/env python3
"""Stage 2: reliability section, figure pruning, hedges, conclusion, limitations."""
import pathlib, re

SRC = pathlib.Path(__file__).with_name("_body2.tex")
OUT = pathlib.Path(__file__).with_name("_body3.tex")
s = SRC.read_text(encoding="utf-8")
E = []


def rep(old, new):
    E.append((old, new))


def drop_block(label):
    """Remove a figure environment carrying the given label."""
    global s
    pat = re.compile(r"\\begin\{figure\}\[tbp\]\n(?:(?!\\begin\{figure\}).*\n)*?\\label\{%s\}\n\\end\{figure\}\n" % re.escape(label))
    m = pat.search(s)
    assert m, label
    s = s[:m.start()] + s[m.end():]


# --------------------------------------------------- reliability subsection
RELIABILITY = r"""\subsection{Coding reliability}
\label{sec:reliability}
A second coder, blind to the first coding, re-coded 30 of the 110 abstract-coded records from the
same abstract strings against the rubric above. The sample was drawn deterministically (12 threat,
5 dual-track, 4 post-quantum, 9 defense; all seven years; all three venue channels; two records
with an exercised attacker-cost value), and the frozen sample and a blank score sheet were
committed to the released repository before scoring, so the sample could not be tuned to the
result. Agreement is Cohen's $\kappa$ with 2,000-sample bootstrap intervals: quadratic weights for
the ordinal items, no weights for the nominal ones, and raw agreement only for artifact release,
which has no variance in this stratum.

Agreement is good for security function (0.84), venue channel (0.83), track (0.72), standards
signal (0.76) and method family (0.68), and poor for attacker-model explicitness (0.39), data
source (0.38), evaluation realism (0.29), validation approach (0.21) and cost signal (0.11)
(Table~\ref{tab:reliability}). The low values are not an artifact of chance correction:
unweighted $\kappa$, Krippendorff's $\alpha$ and Gwet's AC1 agree for four of the five, none
lifting them above 0.43; cost signal is a separate case, since 19 of 30 records sit at the floor
for both coders, which makes the item uninformative rather than contested. A clarification round
that rewrote only the five weak items, keeping the standards item unchanged as a control, did not
improve them (control unchanged at 0.76), so the residual disagreement lies in what abstracts
report rather than in rubric wording.

Two consequences follow for the rest of this article. Composition counts---function, track, method
family, venue---rest on agreement of 0.68--0.84 and are read as counts. Readiness comparisons rest
on agreement of 0.11--0.39; they are reported as directions and their quantities as bounds, and no
finding in this review turns on a fine-grained readiness contrast. Both score sheets, the frozen
sample, the codebook for the clarification round and the agreement script are released with the
corpus.

\begin{table}[tbp]
\centering
\footnotesize
\caption{Inter-coder agreement over 30 blindly re-coded abstract-depth records, before
adjudication. Values are Cohen's $\kappa$; the nominal items carry no weights and are measured
once, while the five weak items and one control item were re-scored under a clarified codebook.}
\label{tab:reliability}
\begin{tabular}{@{}lcc l@{}}
\toprule
Item & $\kappa$ (round 1) & $\kappa$ (round 2) & Reading \\
\midrule
Security function      & 0.84 & ---  & good \\
Venue channel          & 0.83 & ---  & good \\
Standards signal (R5)  & 0.76 & 0.76 & good; control, unchanged \\
Track                  & 0.72 & ---  & good \\
Method family          & 0.68 & ---  & acceptable \\
Attacker model (R1)    & 0.39 & 0.38 & poor \\
Data source            & 0.38 & 0.38 & poor \\
Evaluation realism (R2)& 0.29 & 0.29 & poor \\
Validation approach    & 0.21 & 0.20 & poor \\
Cost signal (R3)       & 0.11 & 0.11 & uninformative, floor-coded \\
Artifact release (R4)  & ---  & ---  & no variance; raw agreement only \\
\bottomrule
\end{tabular}
\end{table}

"""
anchor = r"\subsection{Comparative synthesis approach}"
rep(anchor, RELIABILITY + anchor)

# ----------------------------------------------------------- limitations
rep(r"""Third, coding reliability: inter-rater reliability was not formally assessed, so all counts should be read as one documented coding---the released dataset (\S\ref{sec:methods}) allows independent re-coding.""",
    r"""Third, coding reliability: agreement was measured on 30 of the 110 abstract-coded records and is poor for five readiness items (\S\ref{sec:reliability}), so the remaining 80 abstract-coded rows and the 20 body-read rows rest on a single coding, and readiness comparisons are reported as directions rather than magnitudes.""")

rep(r"""(frozen by identifier, version, and access date; 18 preprints, 13.8\%, sensitivity-checked)""",
    r"""(frozen by identifier, version, and access date; 19 preprints, 14.6\%, sensitivity-checked)""")

# ------------------------------------------------------------- hedging
rep(r"""Among threat papers (n=30), 16 are testbed/field demonstrations, 9 standard splits, 2 cross-domain, 2 simulation-only, and 1 benchmark---a measured plurality, not a norm""",
    r"""Among threat papers (n=30), 16 are testbed/field demonstrations under the primary coding, 9 standard splits, 2 cross-domain, 2 simulation-only, and 1 benchmark---a measured plurality, not a norm. The testbed figure is an upper bound of roughly 10--16: the two codings found 6 and 4 such records among the 12 sampled attack records (\S\ref{sec:reliability})""")

rep(r"""threat plurality 16/30 testbed, not norm""",
    r"""threat plurality up to 16 of 30 testbed, not norm""")

# ------------------------------------------------- corpus-boundary narration
rep(r"""a 5-paper margin that is not robust: the database-rerun merge added 4 deep-supervised RFFI papers while the dedupe cut removed two adversarial papers (T02 subsumed by T03; T35 excluded), and the federated-privacy additions sit in neither family.""",
    r"""a five-paper margin that is not robust to corpus boundaries: a later merge added four deep-supervised RFFI papers while removing two adversarial ones, and the federated-privacy additions sit in neither family.""")

rep(r"""adversarial ML splits 20 threat / 7 dual / 13 defense across tracks (the dedupe moved two attack-plus-defense papers to dual-track), deep supervised learning""",
    r"""adversarial ML splits 20 threat / 7 dual / 13 defense across tracks, deep supervised learning""")

# -------------------------------------------------------- closed-loop passage
rep(r"""Closed-loop evaluation---defined here as dual-track studies (7 of 130) plus any threat paper that evaluates against a stated defense and any defense paper that evaluates against a stated attack---reaches at least 14 of 121 core (11.6\%, a lower bound---abstract wording may hide further cases; a full-text audit is future work): the 7 dual-track papers (D08, D36, D37, T05, T11, T14, T46---5 under a stricter title-only dual rule with T05/T14 reverting to threat; T31 stays threat either way since its mitigation is secondary), 3 threat papers that demonstrate against defenses (T30 against adversarial training, subtraction, detection, and oracle defenses; T12 by bypassing Neural Cleanse and STRIP; T31 assessing a distillation defense on an OTA O-RAN testbed), and 4 defense papers that demonstrate against attacks (D67 against GAN-based impersonation; D54 against Byzantine poisoning; D32 against live impersonating UAVs; D48 flagging evasive queries).""",
    r"""Closed-loop evaluation---defined here as dual-track studies plus any threat paper that
evaluates against a stated defense and any defense paper that evaluates against a stated
attack---reaches at least 14 of 121 core studies (11.6\%). This is a lower bound: abstract
wording may hide further cases, a full-text audit is future work, and the construct is
hand-judged with no separate reliability estimate. The figure decomposes into 7 dual-track
papers (5 under a stricter title-only rule), 3 threat papers that demonstrate against defenses
(including one that survives adversarial training, subtraction, detection and oracle defenses,
one that bypasses two published detection methods, and one that assesses a distillation defense
on an over-the-air testbed), and 4 defense papers that demonstrate against attacks (GAN-based
impersonation, Byzantine poisoning, live impersonating unmanned aerial vehicles, and evasive
queries).""")

# ------------------------------------------------------------- conclusion
rep("(a statement about literature maturity, not a measurement of deployed systems)",
    "(a statement about literature maturity in this curated sample, not a measurement of "
    "deployed systems)")

rep("and OTA-demonstrated in the strongest cases.",
    "and over-the-air demonstrated in the strongest cases. That contrast is descriptively "
    "striking but rests on the least reliable field in the corpus (validation, $\\kappa = 0.21$), "
    "so it is reported as a bound rather than as a precise count.")


for old, new in E:
    n = s.count(old)
    assert n == 1, (n, old[:70])
    s = s.replace(old, new)

# --------------------------------------------------------- prune 5 figures
for lab in ["fig:years", "fig:methods", "fig:validmix", "fig:venue", "fig:eval"]:
    drop_block(lab)

for old, new in [
    (r"(Figs.~\ref{fig:composition}--\ref{fig:years})", r"(Fig.~\ref{fig:composition})"),
    (r"(Fig.~\ref{fig:methods}, Table~\ref{tab:methods})", r"(Table~\ref{tab:methods})"),
    (r"The year-by-year cut (Fig.~\ref{fig:validmix}) shows", r"The year-by-year cut shows"),
    (r"(Fig.~\ref{fig:venue}, panel a; first-appearance map, panel b)", ""),
    (r"substantiates the section's headline (Fig.~\ref{fig:eval}).", r"substantiates the section's headline (Fig.~\ref{fig:data})."),
]:
    n = s.count(old)
    assert n == 1, (n, old[:60])
    s = s.replace(old, new)

OUT.write_text(s, encoding="utf-8")
left = sorted(set(re.findall(r"\\ref\{(fig:[^}]+)\}", s)))
print("figures now referenced:", left)
print("figure blocks:", s.count(r"\begin{figure}"), "| chars:", len(s))
