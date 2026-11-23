#!/usr/bin/env python3
"""Round-2 sheet: the five clarified items plus the R5 control, same 30 rows, blind."""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reliability"
ITEMS = ["R1", "R2", "R3", "validation", "data_source", "R5"]

ds = {r["id"]: r for r in csv.DictReader(open(ROOT / "dataset_papers.csv"))}
found = {r["id"]: r for r in csv.DictReader(open(ROOT / "found_papers.csv"))}
frozen = list(csv.DictReader(open(OUT / "sample_frozen.csv")))
abstracts = json.load(open(ROOT / "abstracts.json"))
fetched = json.load(open(OUT / "fetched_abstracts.json"))

path = OUT / "coder2_round2.csv"
with open(path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["seq", "id", "title_short", "venue", "year", "abstract"] + ITEMS + ["coder2_note"])
    for row in frozen:
        pid = row["id"]
        text = (fetched.get(pid) or {}).get("text") if isinstance(fetched.get(pid), dict) else None
        if not text:
            v = abstracts.get(pid, "")
            text = v["abstract"] if isinstance(v, dict) else v   # abstracts.json stores {title, abstract}
        w.writerow([row["seq"], pid, ds[pid]["title_short"], found.get(pid, {}).get("venue", ""),
                    ds[pid]["year"], text] + [""] * len(ITEMS) + [""])

sheet = list(csv.DictReader(open(path)))
assert len(sheet) == 30
assert all(len(r["abstract"]) > 200 for r in sheet)
assert all(r[i] == "" for r in sheet for i in ITEMS), "round-2 cells must start blank"
print(f"ok: {path.name} — 30 rows x {len(ITEMS)} items "
      f"({', '.join(ITEMS)}); cells blank; R5 present as control")
