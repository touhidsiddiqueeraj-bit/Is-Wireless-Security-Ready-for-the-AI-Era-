#!/usr/bin/env python3
"""Final reliability sync: CRediT attribution, abstract/body hardware count, §3 reader note,
§2.6 closed-loop caveat, and the back-matter duplicate that v9 kept in sync by hand."""
import copy, pathlib, docx
from docx.text.paragraph import Paragraph

SUB = pathlib.Path(__file__).resolve().parent
MS = SUB / "01_Manuscript_IET_Communications_v2.docx"
DEC = SUB / "03_Declarations_IET_Communications.docx"


def patch(path, subs):
    d = docx.Document(path)
    for old, new in subs:
        hits = [p for p in d.paragraphs if old in p.text]
        assert len(hits) == 1, (path.name, old[:55], len(hits))
        assert len(hits[0].runs) == 1, (path.name, old[:40])
        hits[0].runs[0].text = hits[0].text.replace(old, new)
    d.save(path)


patch(MS, [
    # abstract: the count rests on the weakest item -> upper bound
    ("Attacks are demonstrated on real hardware (16 of 30)",
     "Attacks are demonstrated on real hardware in up to 16 of 30"),
    # body: state the bracket from the two codings
    ("among threat papers (n=30), 16 are testbed/field demonstrations, 9 standard splits",
     "among threat papers (n=30), 16 are testbed/field demonstrations (16 under the primary "
     "coding; the two codings found 6 and 4 such rows among the 12 sampled attack rows, so the "
     "corpus-wide figure is an upper bound of roughly 10–16 — Table S11), 9 standard splits"),
    # conclusions: stop calling the weakest field the most robust contrast
    ("attacks are cheap, largely demonstrated on captures/testbeds (threat plurality 16/30 "
     "testbed, not norm), and OTA-demonstrated in the strongest cases; this is the corpus’s most "
     "robust contrast because it rests on categorical validation counts.",
     "attacks are cheap, largely demonstrated on captures/testbeds (threat plurality up to 16 of "
     "30, not norm), and OTA-demonstrated in the strongest cases. That contrast is descriptively "
     "striking but rests on the least reliable field in the corpus (validation, κ = 0.21), so it "
     "is reported as an upper bound rather than as a precise count."),
    # §2.6: closed-loop has no measured reliability
    ("It reaches at least 14 of 121 core (11.6%, a lower bound\u00a0— abstract wording may hide "
     "further cases; a full-text audit is future work)",
     "It reaches at least 14 of 121 core (11.6%, a lower bound — abstract wording may hide "
     "further cases, a full-text audit is future work, and it is a hand-judged construct with no "
     "separate reliability estimate)"),
    # back-matter duplicate (v9 kept this in sync by hand)
    ("Md. Abul Malek Fahim performed corrective checks on the coding decisions and revision",
     "Md. Abul Malek Fahim performed corrective checks on the coding decisions, the blinded "
     "second coding of 30 abstract-coded records, and revision"),
    ("Data availability. The classified corpus (dataset_papers.csv), screening log, retrieval "
     "records, and analysis scripts are openly available",
     "Data availability. The classified corpus (dataset_papers.csv), both second-coder score "
     "sheets, the agreement script, screening log, retrieval records, and analysis scripts are "
     "openly available"),
    ("AI use. AI assistance was limited to candidate pooling and copy-editing;",
     "AI use. AI assistance was limited to candidate pooling, rubric drafting and copy-editing;"),
])

patch(DEC, [
    ("Md. Abul Malek Fahim performed corrective checks on the coding decisions and revision",
     "Md. Abul Malek Fahim performed corrective checks on the coding decisions, the blinded "
     "second coding of 30 abstract-coded records, and revision"),
    ("The validation role reflects corrective review of coding decisions and derived outputs; the "
     "blinded second coding of 30 abstract-coded rows produced the per-item agreement reported in "
     "§2.4 and Table S11.",
     "The validation role reflects corrective review of coding decisions, the blinded second "
     "coding of 30 abstract-coded rows (agreement in §2.4 and Table S11), and derived outputs."),
])

# §3 reader note, inserted directly under the section heading
d = docx.Document(MS)
head = [p for p in d.paragraphs if p.text.strip().startswith("3  Corpus Overview")][0]
new = copy.deepcopy(head._p)
head._p.addnext(new)
np = Paragraph(new, head._parent)
for r in np.runs[1:]:
    r._r.getparent().remove(r._r)
np.runs[0].text = (
    "Two kinds of number appear in this section. Composition numbers — how many papers do what, "
    "in which venue, with which method family — carry measured inter-coder agreement of 0.68–0.84 "
    "(§2.4, Table S11) and can be read as counts. Readiness numbers — attacker-model explicitness, "
    "evaluation realism, cost, standards — carry agreement of 0.11–0.76, and the four weakest "
    "items bound rather than certify any level comparison. Where a quantity depends on a weak "
    "item it is given as an upper bound or a range, and the underlying codings are released.")
d.save(MS)
print("ok")
