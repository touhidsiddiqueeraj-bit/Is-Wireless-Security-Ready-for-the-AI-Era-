#!/usr/bin/env python3
"""Apply the second-coder reliability result to the submission docx files.

Only text is added/replaced; no number elsewhere changes, and no corpus score is revised.
Run from the repo root, then regenerate PDFs with soffice.
"""
import copy, pathlib, docx
from docx.text.paragraph import Paragraph

SUB = pathlib.Path(__file__).resolve().parent
MS = SUB / "01_Manuscript_IET_Communications_v2.docx"
SUP = SUB / "08_Supplementary_Methods_Figures_v2.docx"
DEC = SUB / "03_Declarations_IET_Communications.docx"


def one_run(p):
    assert len(p.runs) == 1, f"{len(p.runs)} runs: {p.text[:60]}"
    return p.runs[0]


def replace(paras, needle, new):
    hits = [p for p in paras if needle in p.text]
    assert len(hits) == 1, (needle[:60], len(hits))
    p = hits[0]
    one_run(p).text = p.text.replace(needle, new)


def append(paras, needle, extra):
    hits = [p for p in paras if needle in p.text]
    assert len(hits) == 1, (needle[:60], len(hits))
    p = hits[0]
    one_run(p).text = p.text.rstrip() + " " + extra


def insert_after(p, text):
    new = copy.deepcopy(p._p)
    p._p.addnext(new)
    np = Paragraph(new, p._parent)
    for r in np.runs[1:]:
        r._r.getparent().remove(r._r)
    np.runs[0].text = text
    return np


# ---------------------------------------------------------------- manuscript
d = docx.Document(MS)
ps = d.paragraphs

IRR_OLD = ("Inter-rater reliability was not formally assessed; the complete coded dataset is "
           "released so independent researchers can check, correct, or extend any record.")
replace(ps, IRR_OLD, "")

AI_OLD = ("AI assistance was limited to candidate pooling and copy-editing under human control.")
AI_NEW = ("AI assistance was limited to candidate pooling, rubric drafting and copy-editing; no "
          "screening or coding decision was delegated to AI.")
replace(ps, AI_OLD, AI_NEW)

ps = d.paragraphs
anchor = [p for p in ps if p.text.startswith("Screening, retrievability checks")][0]
insert_after(anchor, (
    "Reliability was measured rather than assumed. A second coder, blind to the first coding, "
    "re-coded 30 of the 110 abstract-coded rows against the published rubric and the same abstract "
    "strings: 12 threat, 5 dual-track, 4 post-quantum and 9 defense rows, spanning all seven years "
    "and all three venue channels. The sample and the blank score sheet were committed before "
    "scoring, so the blind is auditable in the released repository. Agreement (Cohen's κ, 95% "
    "bootstrap intervals in Table S11) is substantial for security function (0.84), venue channel "
    "(0.83), standards signal (0.76), track (0.72) and method family (0.68), and poor for "
    "attacker-model explicitness (0.38), data source (0.38), evaluation realism (0.29) and "
    "validation approach (0.20); artifact release has no variance among abstract-coded rows and "
    "cannot be tested. A clarification round that rewrote only the four weak items, keeping one "
    "item unchanged as a control, did not improve them (0.38, 0.38, 0.29, 0.20; control unchanged "
    "at 0.76), so the residual disagreement lies in what abstracts report rather than in rubric "
    "wording. Each row therefore carries one coding, and the four weak items have measured "
    "reproducibility of 0.2–0.4, which is why readiness comparisons are reported as directional "
    "(§3.4). The coded dataset, both score sheets and the agreement script are released."))

ps = d.paragraphs
replace(ps, "Inter-rater reliability was not formally assessed; the coded dataset",
        "The coded dataset")
replace(ps, "together with the screening log, retrieval records, analysis scripts, glossary",
        "together with the second-coder score sheets, the screening log, retrieval records, "
        "analysis scripts, glossary")
replace(ps, ("inter-rater reliability was not formally assessed (the released dataset allows "
             "independent re-coding); "),
        ("agreement is measured only on 30 abstract-coded rows and is poor for attacker-model "
         "explicitness, evaluation realism, data source and validation approach (§2.4), so those "
         "four items bound rather than certify the findings that rest on them; "))
append(ps, "Totals sum applicable items only; dominant value per field; conservative coding",
       ("Two properties of the rubric as applied are disclosed with the reliability pass (§2.4). "
        "R1 = 0 is unexercised across all 130 rows, so the operative scale is {1, 2}: the item "
        "measures explicitness above a floor that every included paper meets. Data source and "
        "validation approach overlap by construction and are the two items with the lowest measured "
        "agreement (0.38 and 0.20); they are therefore read as one descriptive axis rather than "
        "two independent measurements."))
append(ps, "The threat–defense R2 gap (1.53 vs 1.27, 0.26) is measured over mixed coding depth",
       ("Sampling noise at this n exceeds the effect: on a 30-row subsample the same comparison "
        "ranges from −0.08 to +0.31 depending on coder, and R2 is the readiness item with the "
        "lowest measured reliability (κ = 0.29, §2.4). The gap is reported as a direction, not as "
        "a magnitude."))
d.save(MS)

# ---------------------------------------------------------------- supplement
s = docx.Document(SUP)
ps = s.paragraphs
replace(ps, ("Independent double-coding of the released dataset against these anchors, with "
             "inter-rater agreement reported, remains the highest-priority item of future work "
             "(§2.4, §9)."),
        ("Double-coding against these anchors has since been carried out on 30 abstract-coded rows, "
         "with per-item agreement reported in Table S11 and §2.4; extending it to the remaining 80 "
         "abstract-coded and 20 body-read rows remains the highest-priority item of future work "
         "(§9)."))

s.add_heading("S5  Second-coder reliability of the abstract-coded rows", level=1)
s.add_paragraph(
    "A second coder, blind to the first coding, re-coded 30 of the 110 abstract-coded rows from "
    "the same abstract strings against the rubric in §2.5 and the anchor examples above. The sample "
    "was drawn deterministically over the abstract-coded stratum (12 threat, 5 dual-track, 4 "
    "post-quantum, 9 defense; all seven years and all three venue channels; two rows with an "
    "exercised R3 = 2), and the frozen sample and the blank score sheet were committed to the "
    "released repository before scoring. Agreement is Cohen's κ with 2,000-sample bootstrap "
    "intervals: quadratic weights for the ordinal items, no weights for the nominal ones, and raw "
    "agreement only for R4, which has no variance in this stratum. A clarification round rewrote "
    "only the five weak items (R1, R2, R3, data source, validation approach) and kept R5 unchanged "
    "as a control; it is reported as secondary because the rewording was informed by the first "
    "round, and it is an upper bound on instrument agreement. No score in dataset_papers.csv was "
    "revised on the basis of this pass.")
s.add_paragraph(
    "Table S11: Second-coder agreement on 30 abstract-coded rows. Round 1 is primary; round 2 "
    "applies only to the five clarified items (ordinal items weighted, nominal unweighted). "
    "Intervals are 95% bootstrap; machine-generated from reliability/tableS11_reliability.csv and "
    "reliability/tableS11b_round2.csv.")

ROWS = [
    ("R1 attacker-capability explicitness", "0.39 (0.18–0.54)", "0.43", "0.38", "poor"),
    ("R2 evaluation realism", "0.29 (0.03–0.59)", "0.63", "0.29", "poor"),
    ("R3 cost signal", "0.11 (−0.20–0.44)", "0.63", "0.11", "poor"),
    ("R4 artifact release", "n/a (no variance)", "1.00", "—", "untestable"),
    ("R5 standards signal", "0.76 (0.29–1.00)", "0.93", "0.76", "substantial"),
    ("Track", "0.72 (0.50–0.90)", "0.80", "—", "substantial"),
    ("Security function", "0.84 (0.69–1.00)", "0.90", "—", "substantial"),
    ("AI method family", "0.68 (0.46–0.86)", "0.77", "—", "substantial"),
    ("Data source", "0.38 (0.16–0.59)", "0.53", "0.38", "poor"),
    ("Validation approach", "0.21 (−0.01–0.41)", "0.40", "0.20", "poor"),
    ("Venue channel", "0.83 (0.61–1.00)", "0.90", "—", "substantial"),
]
tb = s.add_table(rows=len(ROWS) + 1, cols=5)
tb.style = s.tables[0].style
hdr = ["Item", "κ round 1 (95% CI)", "Exact agreement", "κ round 2", "Reading"]
for j, h in enumerate(hdr):
    tb.cell(0, j).text = h
    tb.cell(0, j).paragraphs[0].runs[0].bold = True
for i, row in enumerate(ROWS, 1):
    for j, v in enumerate(row):
        tb.cell(i, j).text = v
s.save(SUP)

# ---------------------------------------------------------------- declarations
dc = docx.Document(DEC)
ps = dc.paragraphs
replace(ps, "inter-rater reliability was not formally assessed.",
        "the blinded second coding of 30 abstract-coded rows produced the per-item agreement "
        "reported in §2.4 and Table S11.")
replace(ps, ("The classified corpus (dataset_papers.csv), screening log, retrieval records, and "
             "analysis scripts are openly available"),
        ("The classified corpus (dataset_papers.csv), both second-coder score sheets, the "
         "agreement script, screening log, retrieval records, and analysis scripts are openly "
         "available"))
replace(ps, "AI assistance was limited to candidate pooling, prose drafting, and copy-editing;",
        "AI assistance was limited to candidate pooling, rubric drafting, prose drafting, and "
        "copy-editing;")
dc.save(DEC)
print("patched:", MS.name, SUP.name, DEC.name)
