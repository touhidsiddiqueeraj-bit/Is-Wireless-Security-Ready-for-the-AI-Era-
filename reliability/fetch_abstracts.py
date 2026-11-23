#!/usr/bin/env python3
"""Fetch the abstracts missing from abstracts.json for the frozen sample.

Writes reliability/fetched_abstracts.json as {id: {text, url, retrieved}} so the
evidence source of every fetched string stays auditable.
"""
import csv, json, pathlib, re, urllib.parse, urllib.request, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reliability"
MAIL = "mailto=review@example.org"

found = {r["id"]: r for r in csv.DictReader(open(ROOT / "found_papers.csv"))}
need = [r["id"] for r in csv.DictReader(open(OUT / "sample_frozen.csv"))
        if r["evidence_source"] == "MISSING"]


def get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"User-Agent": f"reliability-check ({MAIL})",
                                               "Accept": accept})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def invert(idx):
    words = []
    for w, pos in idx.items():
        for p in pos:
            words.append((p, w))
    return " ".join(w for _, w in sorted(words)) or None


def from_openalex(url):
    j = json.loads(get(url))
    idx = j.get("abstract_inverted_index")
    return (invert(idx) if idx else None), j.get("doi") or url


def doi_of(rid):
    u = found[rid]["doi_url"]
    m = re.search(r"doi\.org/(10\.[^?#]+)", u)
    return m.group(1) if m else None


out = json.load(open(OUT / "fetched_abstracts.json")) if (OUT / "fetched_abstracts.json").exists() else {}
for rid in need:
    if rid in out:
        continue
    doi = doi_of(rid)
    text = src = None
    if doi:
        try:
            text, src = from_openalex(f"https://api.openalex.org/works/doi:{doi}?{MAIL}")
        except Exception as e:
            print(rid, "openalex failed:", e)
    if not text:
        try:
            j = json.loads(get(f"https://api.crossref.org/works/{doi}"))
            text = re.sub(r"<[^>]+>", " ", j["message"].get("abstract") or "") or None
            text = re.sub(r"\s+", " ", text).strip() if text else None
            src = f"https://api.crossref.org/works/{doi}"
        except Exception as e:
            print(rid, "crossref failed:", e)
    if not text:  # last resort: OpenAlex title search
        try:
            t = re.split(r"[:(]", found[rid]["title"])[0]  # colon breaks filter syntax
            q = urllib.parse.quote(t, safe="")
            j = json.loads(get(f"https://api.openalex.org/works?filter=title.search:{q}&per_page=1&{MAIL}"))
            hit = (j.get("results") or [None])[0]
            if hit and hit.get("abstract_inverted_index"):
                text, src = invert(hit["abstract_inverted_index"]), hit["id"]
        except Exception as e:
            print(rid, "title search failed:", e)
    if not text:
        print(rid, "NO ABSTRACT FOUND")
        continue
    out[rid] = {"text": re.sub(r"\s+", " ", text).strip(),
                "url": src, "retrieved": datetime.date.today().isoformat()}
    print(rid, "ok", len(out[rid]["text"]), "chars from", src)

json.dump(out, open(OUT / "fetched_abstracts.json", "w"), indent=1, ensure_ascii=False)
print("cached:", len(out), "of", len(need))
