"""Fetch OpenAlex abstracts for database-run shortlist screening.

Reconstructs abstracts from abstract_inverted_index, prints title + abstract
for human V1-V3 eligibility screening. Writes shortlist_abstracts.json.
"""
import json
import urllib.parse
import urllib.request

DOIS = [
    "10.1109/tifs.2025.3577013", "10.48550/arxiv.2301.03760",
    "10.1145/3643833.3656138", "10.1109/ucom59132.2023.10257584",
    "10.1109/tifs.2024.3352423", "10.48550/arxiv.2201.06093",
    "10.48550/arxiv.2609.16341", "10.48550/arxiv.2603.08402",
    "10.48550/arxiv.2604.24022", "10.13052/jcsm2245-1439.1547",
    "10.31838/njap/07.01.24", "10.12928/telkomnika.v24i4.27791",
    "10.1109/tifs.2022.3219287", "10.1109/tgcn.2024.3373886",
    "10.1109/tifs.2022.3149396", "10.1109/tmlcn.2024.3446743",
    "10.1109/pimrc62392.2025.11275484",
]
MAIL = "mailto=corpus-verify@example.com"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "corpus-triangulation/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def recon(inv):
    if not inv:
        return ""
    pos = {}
    for w, ps in inv.items():
        for p in ps:
            pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))


out = {}
for doi in DOIS:
    try:
        d = get("https://api.openalex.org/works/https://doi.org/" + doi + f"?{MAIL}&select=id,doi,title,publication_year,primary_location,authorships,abstract_inverted_index")
        au = "; ".join(f"{a.get('author', {}).get('display_name', '')}" for a in d.get("authorships", [])[:4])
        ven = ((d.get("primary_location") or {}).get("source") or {}).get("display_name")
        out[doi] = {"title": d.get("title"), "year": d.get("publication_year"),
                    "venue": ven, "authors": au, "abstract": recon(d.get("abstract_inverted_index"))[:1500]}
        print(f"## {doi}\n{out[doi]['title']} ({out[doi]['year']}) [{ven}]\n{au}\n{out[doi]['abstract'][:900]}\n")
    except Exception as ex:  # noqa: BLE001
        print(f"## {doi} ERROR {ex}\n")
        out[doi] = {"error": str(ex)}
    __import__("time").sleep(1)

json.dump(out, open("shortlist_abstracts.json", "w"), indent=1)
print("saved", len(out))
