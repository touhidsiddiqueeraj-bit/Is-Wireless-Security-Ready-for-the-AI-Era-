"""One-off venue/author resolution for weak-bib corpus rows.

For each arXiv ID: fetch arXiv metadata (authors, journal-ref, comments,
published version) and, where a DOI/journal-ref exists, Crossref metadata.
Prints a resolution table for human review; writes nothing.
"""
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

IDS = ["2105.08364", "2308.14693", "2102.10639", "2511.05796", "2411.10287",
       "2112.11090", "2509.00018", "2507.00714", "2605.15593", "2608.04881",
       "2105.10883", "2504.04511", "2603.10274", "2409.06360", "2512.10296",
       "2505.00487"]


def get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "corpus-verify/1.0 (mailto:anon@example.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


NS = {"a": "http://www.w3.org/2005/Atom", "arx": "http://arxiv.org/schemas/atom"}
out = []
for aid in IDS:
    try:
        raw = get(f"http://export.arxiv.org/api/query?id_list={aid}")
        e = ET.fromstring(raw).find("a:entry", NS)
        if e is None:
            out.append((aid, "ARXIV-NOT-FOUND", "", ""))
            continue
        title = (e.findtext("a:title", default="", namespaces=NS) or "").strip().replace("\n", " ")
        authors = [a.findtext("a:name", default="", namespaces=NS) for a in e.findall("a:author", NS)]
        jref = (e.findtext("arx:journal_ref", default="", namespaces=NS) or "").strip()
        doi = (e.findtext("arx:doi", default="", namespaces=NS) or "").strip()
        comment = (e.findtext("arx:comment", default="", namespaces=NS) or "").strip()[:120]
        out.append((aid, "; ".join(authors[:6]), jref or "(no journal-ref)", doi or comment))
    except Exception as ex:  # noqa: BLE001
        out.append((aid, f"ERROR {ex}", "", ""))

for aid, au, jr, doi in out:
    print(f"{aid} | {au[:90]} | {jr[:100]} | {doi[:100]}")
