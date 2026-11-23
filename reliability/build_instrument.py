#!/usr/bin/env python3
"""Build the frozen second-coder sample and the blank score sheet.

Coder-1 scores are never written to either output; the sheet is generated from
id/title/venue/year/abstract only. Run order:
  1. python3 build_instrument.py            -> sample_frozen.csv + coder2_scores.csv
  2. fill any evidence_source=MISSING rows into fetched_abstracts.json, rerun.
"""
import csv, json, random, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reliability"
SEED = 20261123                      # draw date, fixed literal
N = 30
QUOTA = {"threat": 12, "both": 5, "pqc-context": 4, "defense": 9}
FORCE_R3_2 = 2                       # rare-cell guard (over-inclusion of R3=2)
MIN_PREPRINT = 3
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]

rows = [r for r in csv.DictReader(open(ROOT / "dataset_papers.csv"))
        if r["coding_depth"] == "abstract"]
assert len(rows) == 110, len(rows)
by_id = {r["id"]: r for r in rows}
found = {r["id"]: r for r in csv.DictReader(open(ROOT / "found_papers.csv"))}
abstracts = json.load(open(ROOT / "abstracts.json"))
fetched_path = OUT / "fetched_abstracts.json"
fetched = json.load(open(fetched_path)) if fetched_path.exists() else {}

rng = random.Random(SEED)
order = [r["id"] for r in rows]
rng.shuffle(order)
has_abs = lambda pid: pid in abstracts or pid in fetched
rank = {pid: i for i, pid in enumerate(order)}

picked, counts, years_left = [], {t: 0 for t in QUOTA}, set(YEARS)

def take(pid, why):
    assert pid not in picked
    if counts[by_id[pid]["track"]] >= QUOTA[by_id[pid]["track"]]:
        return False
    counts[by_id[pid]["track"]] += 1
    picked.append((pid, why))
    years_left.discard(by_id[pid]["year"])
    return True

# 1. rare-cell guard: R3=2 exists only among PQC rows in this frame
rare = sorted([r["id"] for r in rows if r["R3"] == "2"], key=lambda i: rank[i])
for pid in rare[:FORCE_R3_2]:
    take(pid, "rare-cell:R3=2")
assert counts["pqc-context"] == FORCE_R3_2

# 2. coverage: every year once, then preprints
while True:
    need_preprint = sum(1 for p, _ in picked
                        if by_id[p]["venue_channel"] == "preprint") < MIN_PREPRINT
    cands = sorted((r["id"] for r in rows if r["id"] not in dict(picked)),
                   key=lambda i: (not has_abs(i), rank[i]))
    best, best_score = None, 0
    for pid in cands:
        r = by_id[pid]
        if counts[r["track"]] >= QUOTA[r["track"]]:
            continue
        score = (r["year"] in years_left) + (need_preprint and r["venue_channel"] == "preprint")
        if score > best_score:
            best, best_score = pid, score
    if not best:
        break
    take(best, "coverage")
    if not years_left and sum(1 for p, _ in picked
                              if by_id[p]["venue_channel"] == "preprint") >= MIN_PREPRINT:
        break

# 3. fill each stratum to quota
for track, target in QUOTA.items():
    for pid in sorted((r["id"] for r in rows if r["track"] == track
                       and r["id"] not in dict(picked)),
                      key=lambda i: (not has_abs(i), rank[i])):
        if counts[track] >= target:
            break
        take(pid, "stratum-fill")

picked.sort(key=lambda p: p[0])
assert len(picked) == N, len(picked)
assert counts == QUOTA, counts
assert not years_left, years_left
preprints = sum(1 for p, _ in picked if by_id[p]["venue_channel"] == "preprint")
assert preprints >= MIN_PREPRINT, preprints
assert len({p for p, _ in picked}) == N

now = datetime.date.today().isoformat()
sample_path = OUT / "sample_frozen.csv"
with open(sample_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["seq", "id", "stratum", "year", "venue_channel", "why", "evidence_source", "seed", "draw_date"])
    for i, (pid, why) in enumerate(picked, 1):
        ev = ("fetched_abstracts.json" if pid in fetched
              else "abstracts.json" if pid in abstracts else "MISSING")
        w.writerow([i, pid, by_id[pid]["track"], by_id[pid]["year"],
                    by_id[pid]["venue_channel"], why, ev, SEED, now])

FIELDS = ["track", "function", "method_family", "data_source", "validation",
          "venue_channel", "R1", "R2", "R3", "R4", "R5"]
sheet_path = OUT / "coder2_scores.csv"
with open(sheet_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["seq", "id", "title_short", "venue", "year", "abstract"] + FIELDS + ["coder2_note"])
    for i, (pid, _) in enumerate(sorted(picked), 1):
        r = by_id[pid]
        text = (fetched.get(pid) or abstracts.get(pid) or "")
        w.writerow([i, pid, r["title_short"], found.get(pid, {}).get("venue", ""),
                    r["year"], text] + [""] * len(FIELDS) + [""])

missing = [p for p, _ in picked
           if p not in abstracts and p not in fetched]
print(f"ok: {N} rows -> {sample_path.name}, {sheet_path.name}")
print("coverage: years", sorted({by_id[p]['year'] for p, _ in picked}),
      "| channels", {c: sum(1 for p, _ in picked if by_id[p]['venue_channel'] == c)
                     for c in ('journal', 'conference', 'preprint')},
      "| R3=2 rows", sum(1 for p, _ in picked if by_id[p]['R3'] == '2'))
if missing:
    print("need abstract fetch:", missing)
    sys.exit(1)

# self-check: the sheet must carry evidence for every row and no coder-1 values
sheet = list(csv.DictReader(open(sheet_path)))
assert len(sheet) == N
assert all(len(r["abstract"]) > 200 for r in sheet), [r["id"] for r in sheet if len(r["abstract"]) <= 200]
assert all(r[f] == "" for r in sheet for f in FIELDS), "score cell pre-filled"
print("self-check ok: abstracts present, score cells blank")
