"""OpenAlex database run for triangulation (no subscription needed).

Runs topical queries against api.openalex.org (polite pool, mailto, 1 req/s),
normalizes DOI/title keys, dedupes against retrieval/records.json (Crossref +
arXiv, n=1945) and found_papers.csv, and reports genuinely new candidates.
Writes: openalex_records.json (all hits), openalex_new_candidates.json.
Does NOT auto-include anything -- candidates need manual V1-V3 screening.
"""
import json
import re
import time
import urllib.parse
import urllib.request

QUERIES = [
    "RF fingerprinting deep learning authentication",
    "physical layer key generation machine learning wireless",
    "adversarial attacks radio frequency fingerprint identification",
    "LoRa device identification deep learning security",
    "electromagnetic side channel deep learning AES wireless",
    "5G AKA protocol fuzzing security",
    "anti-jamming deep reinforcement learning UAV",
    "federated learning wireless privacy security over-the-air",
    "post-quantum cryptography wireless constrained devices Kyber",
    "encrypted traffic classification machine learning wireless IoT",
]
ROOT = "/mnt/drive2/communicationspaper"
MAIL = "mailto=corpus-verify@example.com"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "corpus-triangulation/1.0 (mailto:corpus-verify@example.com)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def dockey(w):
    doi = (w.get("doi") or "").lower().replace("https://doi.org/", "").strip()
    return doi or None


seen_doi, seen_title = set(), set()
recs = json.load(open(f"{ROOT}/retrieval/records.json"))
for r in recs:
    if r.get("doi"):
        seen_doi.add(r["doi"].lower().strip())
    if r.get("title"):
        seen_title.add(norm_title(r["title"]))
import csv
for r in csv.DictReader(open(f"{ROOT}/found_papers.csv")):
    if r.get("doi_url"):
        m = re.search(r"(10\.\S+|arxiv\.org/\S+|eprint\.iacr\.org/\S+)", r["doi_url"])
        if m:
            seen_doi.add(m.group(1).lower())
    seen_title.add(norm_title(r.get("title", "")))

all_hits, new = [], []
for qi, q in enumerate(QUERIES):
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(q)
           + "&filter=from_publication_date:2020-01-01,to_publication_date:2026-10-11"
           + "&per-page=100&select=id,doi,title,publication_year,primary_location,authorships,cited_by_count"
           + f"&{MAIL}")
    try:
        d = get(url)
    except Exception as ex:  # noqa: BLE001
        print(f"Q{qi} ERROR {ex}")
        continue
    print(f"Q{qi} [{q[:45]}] count={d.get('meta', {}).get('count')} took={len(d.get('results', []))}")
    for w in d.get("results", []):
        dk = dockey(w)
        tk = norm_title(w.get("title"))
        all_hits.append({"doi": dk, "title": w.get("title"), "year": w.get("publication_year"),
                         "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                         "cites": w.get("cited_by_count"), "q": qi})
        if (dk and dk not in seen_doi) and tk not in seen_title:
            if not any(n["title"] == w.get("title") for n in new):
                new.append(all_hits[-1])
    time.sleep(1.1)

json.dump(all_hits, open("openalex_records.json", "w"), indent=1)
json.dump(new, open("openalex_new_candidates.json", "w"), indent=1)
print(f"\ntotal hits={len(all_hits)} new candidates={len(new)}")
for n in new[:40]:
    print(f"  [{n['year']}] {str(n['title'])[:80]} | {n['venue']} | {n['doi']}")
