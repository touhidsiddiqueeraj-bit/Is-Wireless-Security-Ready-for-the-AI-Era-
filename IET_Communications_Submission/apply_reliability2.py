#!/usr/bin/env python3
"""Add Table S12 (coefficient family) + the §2.4 sentence that answers 'is kappa an artefact?'"""
import pathlib, docx

SUB = pathlib.Path(__file__).resolve().parent
MS = SUB / "01_Manuscript_IET_Communications_v2.docx"
SUP = SUB / "08_Supplementary_Methods_Figures_v2.docx"


def one(p):
    assert len(p.runs) == 1, p.text[:60]
    return p.runs[0]


# ---- manuscript: replace the blanket "poor for ..." tail with a coefficient-aware one
d = docx.Document(MS)
old = ("and poor for attacker-model explicitness (0.38), data source (0.38), evaluation realism "
       "(0.29), cost signal (0.11) and validation approach (0.20); artifact release has no "
       "variance among abstract-coded rows and cannot be tested.")
new = ("and poor for attacker-model explicitness (0.38), data source (0.38), evaluation realism "
       "(0.29), cost signal (0.11) and validation approach (0.20); artifact release has no "
       "variance among abstract-coded rows and cannot be tested. Those low values are not an "
       "artifact of chance correction: unweighted κ, Krippendorff's α and Gwet's AC1 agree for "
       "attacker-model explicitness, evaluation realism, validation approach and data source (all "
       "≤ 0.39 under every coefficient). Cost signal is the exception — 21 of 30 rows are coded 0 "
       "by both coders, so κ and α collapse while AC1 (0.56) and raw agreement (0.63) do not — and "
       "it is reported descriptively, as an item with little discriminating power rather than as a "
       "contested one (Table S12).")
hits = [p for p in d.paragraphs if old in p.text]
assert len(hits) == 1, len(hits)
one(hits[0]).text = hits[0].text.replace(old, new)
d.save(MS)

# ---- supplement: Table S12 + interpretation
s = docx.Document(SUP)
s.add_paragraph(
    "Table S12: The same 30-row agreement data under five coefficients, because κ is sensitive to "
    "prevalence and a low value can in principle be an artefact of a skewed marginal. Nominal items "
    "carry no weighted value (their level order is arbitrary); the binary column recodes 0–1 versus "
    "2; machine-generated from reliability/tableS12_coefficients.csv.")
ROWS = [
    ("R1 attacker-capability", "0.07", "0.39", "0.36", "0.20", "0.31"),
    ("R2 evaluation realism", "0.29", "0.29", "0.24", "0.52", "0.29"),
    ("R3 cost signal", "−0.06", "0.11", "0.00", "0.56", "—"),
    ("R5 standards signal", "0.76", "0.76", "0.76", "0.92", "—"),
    ("Validation approach", "0.21", "—", "0.08", "0.27", "—"),
    ("Data source", "0.38", "—", "0.05", "0.43", "—"),
]
tb = s.add_table(rows=len(ROWS) + 1, cols=6)
tb.style = s.tables[0].style
for j, h in enumerate(["Item", "κ unweighted", "κ quadratic-weighted",
                       "Krippendorff α", "Gwet AC1", "κ binary 0–1 vs 2"]):
    tb.cell(0, j).text = h
    tb.cell(0, j).paragraphs[0].runs[0].bold = True
for i, row in enumerate(ROWS, 1):
    for j, v in enumerate(row):
        tb.cell(i, j).text = v
s.add_paragraph(
    "No coefficient rescues the four weak items: attacker-model explicitness stays at or below 0.39 "
    "under all five, evaluation realism at or below 0.52, validation approach at or below 0.27 and "
    "data source at or below 0.43. Only AC1 lifts evaluation realism and cost signal, and in both "
    "cases by crediting a shared floor coding (14 of 30 rows are 0 on evaluation realism's sibling "
    "field, 21 of 30 on cost), which is agreement without discrimination. Cost signal is therefore "
    "reported descriptively rather than as an ordering device; the four other weak items are "
    "reported as measured, with their low agreement bounding every finding that rests on them.")
s.save(SUP)
print("ok")
