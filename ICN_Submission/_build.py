#!/usr/bin/env python3
"""Assemble the ICN manuscript from the ported body, appendix, and references.

Layout work only: two-column float placement, figure widths from the native
raster size so no figure is upsampled, and the journal's title/abstract block.
No number in the text is touched.
"""
import pathlib
import re

SUB = pathlib.Path(__file__).resolve().parent
FIG = SUB / "figures"

body = (SUB / "_body4.tex").read_text(encoding="utf-8")
appendix = (SUB / "_appendix.tex").read_text(encoding="utf-8")
refs = (SUB / "_refs.tex").read_text(encoding="utf-8")

# ------------------------------------------------------------------ figures
FIG_ENV = re.compile(
    r"\\begin\{figure\}\[tbp\]\n((?:.*\n)*?)\\end\{figure\}\n", re.M)

from PIL import Image


def widen(m):
    """Full-width float at the figure's native size (300 dpi, never upsampled)."""
    block = m.group(1)
    g = re.search(r"\\includegraphics\[width=[^\]]*\]\{figures/([^}]+)\}", block)
    if not g:
        return m.group(0)
    px = Image.open(FIG / g.group(1)).size[0]
    cm = min(round(px / 300 * 2.54, 1), 17.0)
    block = block.replace(g.group(0),
                          r"\includegraphics[width=%scm]{figures/%s}" % (cm, g.group(1)))
    return "\\begin{figure*}[tbp]\n" + block + "\\end{figure*}\n"


body = FIG_ENV.sub(widen, body)

# ------------------------------------------------------------------- tables
TAB_ENV = re.compile(
    r"\\begin\{table\}\[[^\]]*\]\n((?:.*\n)*?)\\end\{table\}\n", re.M)


def wide_table(m):
    """Promote to a full-width float when the natural width exceeds one column."""
    block = m.group(1)
    spec = re.search(r"\\begin\{tabular\}\{(.*)\}\s*$", block, re.M)
    if not spec:
        return m.group(0)
    pcm = sum(float(x) for x in re.findall(r"p\{([\d.]+)cm\}", spec.group(1)))
    rows = [ln for ln in block.splitlines() if "&" in ln]
    ncol = max((ln.count("&") + 1 for ln in rows), default=1)
    longest = max((len(ln) for ln in rows), default=0)
    if pcm < 7.0 and ncol <= 4 and longest <= 55:
        return m.group(0)
    if "\\footnotesize" not in block and "\\scriptsize" not in block:
        block = "\\footnotesize\n" + block
    return "\\begin{table*}[tbp]\n" + block + "\\end{table*}\n"


body = TAB_ENV.sub(wide_table, body)

TABLE = r"""
\title{Is Wireless Security Ready for the AI Era? A Scoping Review of 130 Studies, 2020--2026}

\firstheadname{Is Wireless Security Ready for the AI Era?}
\firstfootname{}
\headevenname{Is Wireless Security Ready for the AI Era?}
\headoddname{H.~T.~Siddiquee and M.~A.~M.~Fahim}

\author{\begin{tabular}{c}
Hussain Touhid Siddiquee$^{1*}$ and Md. Abul Malek Fahim$^{1}$\\
{\small $^{1}$Department of Computer Science and Engineering, \emph{[University]}, \emph{[City]}, \emph{[Postcode]}, Bangladesh}\\
{\small $^{*}$E-mail: touhidsiddiqueeraj@gmail.com}
\end{tabular}}

\abstract{Wireless links broadcast by physics, so the radio link is where AI-enabled
interception, spoofing and jamming land. This scoping review charts 130 studies published
2020--2026 that apply machine learning to wireless-link security or attack it, drawn from a
seeded search and two Crossref/arXiv runs and screened for radio population, security link, AI
involvement and evaluable evidence. Defenses dominate (84) over threats (30) and dual-track work
(7), while deep supervised learning (45) only narrowly leads adversarial machine learning (40).
Radio-frequency fingerprinting is the dominant function (69 of 121 core studies, 57.0\%),
artifact release remains rare (4, 3.3\%), and closed-loop attack--defense evaluation reaches at
least 14 studies (11.6\%). A blinded re-coding of 30 records gives good agreement for composition
items ($\kappa$ 0.68--0.84) but poor agreement for readiness items ($\kappa$ 0.11--0.39), so
readiness findings are directions, not magnitudes. On current evidence the literature does not
demonstrate wireless security ready for the AI era.}

\doi{}\par
\keyword{Wireless security; physical-layer security; radio-frequency fingerprinting; adversarial
machine learning; jamming; federated learning privacy; post-quantum migration; scoping review}

"""

ACK = r"""
\begin{acknowledgement}
The authors thank the maintainers of the Crossref, arXiv and OpenAlex APIs, on whose records the
retrieval described in \S\ref{sec:methods} depends.
\end{acknowledgement}

"""

BIO = r"""
\begin{biographynophoto}
\textbf{Hussain Touhid Siddiquee} is with the Department of Computer Science and Engineering,
\emph{[University]}, Bangladesh. His research covers wireless and physical-layer security,
machine learning for radio-frequency fingerprinting, and the empirical evaluation of
learning-based defenses.
\end{biographynophoto}

\begin{biographynophoto}
\textbf{Md. Abul Malek Fahim} is with the Department of Computer Science and Engineering,
\emph{[University]}, Bangladesh. His work concerns security analytics, coding validation, and
the reproducibility of empirical security research.
\end{biographynophoto}
"""

doc = r"""%% ICN submission manuscript --- compiled with XeLaTeX.
%% Author affiliations marked \emph{[...]} are placeholders to be completed.
\documentclass[10.5pt,compsoc,winfonts]{ICN}
\usepackage{fontspec}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{array}
\usepackage{longtable}
\usepackage[noadjust]{cite}
\usepackage{amsmath,amssymb}
\usepackage{float}
\usepackage{url}
\linespread{1.2}

\setmainfont{Carlito}[Ligatures=TeX]
\defaultfontfeatures{Ligatures=TeX}
\newcommand{\bta}{\fontspec{InriaSans-Bold.ttf}}
\newcommand{\bbb}{\fontspec{InriaSans-Light.ttf}}
\renewcommand\figurename{Fig.~}
\makeatletter
\renewcommand{\doi}[1]{\gdef\icn@doi{}}
\makeatother
\newcommand{\upcite}[1]{\cite{#1}}

\begin{document}
""" + TABLE + r"""\maketitle\pagestyle{icnheadings}

""" + body + r"""
\appendix
\section{Included studies}
""" + appendix + ACK + r"""
\begin{thebibliography}{999}
\small
""" + refs + r"""\end{thebibliography}

""" + BIO + r"""
\end{document}
"""

# XeTeX+fontspec leaves TeX ligatures unapplied with this font; substitute the
# Unicode characters directly (verified: no "--" occurs inside math mode).
doc = doc.replace("---", "\u2014").replace("--", "\u2013")
doc = doc.replace("``", "\u201c").replace("''", "\u201d")

(SUB / "manuscript.tex").write_text(doc, encoding="utf-8")
print("manuscript.tex:", doc.count("\n"), "lines")
print("figure*:", doc.count(r"\begin{figure*}"), "| table*:", doc.count(r"\begin{table*}"))
print("single-col figures:", doc.count(r"\begin{figure}["),
      "| single-col tables:", doc.count(r"\begin{table}["))
