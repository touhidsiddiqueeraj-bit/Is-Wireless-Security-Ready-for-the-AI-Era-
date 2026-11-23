#!/usr/bin/env python3
"""Join coder 2 to coder 1, compute agreement, test the derived claims.

Pre-registered plan: reliability/README.md, "Analysis plan". Nothing here modifies
dataset_papers.csv; adjudication is logged, not applied.
Run after coder2_scores.csv is committed.
"""
import csv, json, random, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reliability"
ORD = ["R1", "R2", "R3", "R4", "R5"]
NOM = ["track", "function", "method_family", "data_source", "validation", "venue_channel"]
B = 2000
random.seed(7)

ds = {r["id"]: r for r in csv.DictReader(open(ROOT / "dataset_papers.csv"))}
c2 = list(csv.DictReader(open(OUT / "coder2_scores.csv")))
by2 = {r["id"]: r for r in c2}
assert len(c2) == 30, len(c2)


def agree(c1, c2v):
    n = len(c1)
    po = sum(a == b for a, b in zip(c1, c2v)) / n
    ca, cb = collections.Counter(c1), collections.Counter(c2v)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n**2
    kappa = (po - pe) / (1 - pe) if pe < 1 else None
    return po, kappa


def qwk(c1, c2v, k=3):
    n = len(c1)
    o = [[0] * k for _ in range(k)]
    e = [[0] * k for _ in range(k)]
    a = collections.Counter(c1)
    b = collections.Counter(c2v)
    for x, y in zip(c1, c2v):
        o[x][y] += 1
    for i in range(k):
        for j in range(k):
            e[i][j] = a[i] * b[j] / n
    d = [[((i - j) ** 2) / (k - 1) ** 2 for j in range(k)] for i in range(k)]
    do = sum(d[i][j] * o[i][j] for i in range(k) for j in range(k))
    de = sum(d[i][j] * e[i][j] for i in range(k) for j in range(k))
    return 1 - do / de if de else None


def ci(pairs, fn):
    vals = []
    for _ in range(B):
        s = [pairs[random.randrange(len(pairs))] for _ in pairs]
        v = fn([a for a, _ in s], [b for _, b in s])
        if v is not None:
            vals.append(v)
    vals.sort()
    return (round(vals[int(0.025 * len(vals))], 3), round(vals[int(0.975 * len(vals)) - 1], 3)) if vals else (None, None)


rows, tabs, lines = [], [], []
print(f"{'item':14s} {'n':>3s} {'exact':>6s} {'+-1':>5s} {'kappa':>6s} {'95% CI':>14s} {'PABAK':>6s}  note")
for item in ORD:
    keep = [r["id"] for r in c2 if ds[r["id"]][item].isdigit()]
    c1 = [int(ds[i][item]) for i in keep]
    c2v = [int(by2[i][item]) for i in keep]
    assert len(c1) == len(c2v)
    pairs = list(zip(c1, c2v))
    po, _ = agree(c1, c2v)
    kap = qwk(c1, c2v)
    kci = ci(pairs, lambda a, b: qwk(a, b))
    pabak = 2 * po - 1
    within = sum(abs(a - b) <= 1 for a, b in pairs) / len(pairs)
    dom = collections.Counter(c1 + c2v).most_common(1)[0]
    note = ""
    if kap is None or (1 - sum(collections.Counter(c1)[k] ** 2 for k in set(c1)) / len(c1) ** 2) < 0.15:
        note = f"degenerate marginals ({dom[0]}={dom[1]}/{2*len(c1)}); PABAK only"
    print(f"{item:14s} {len(c1):3d} {po:6.3f} {within:5.3f} "
          f"{('  n/a' if kap is None else f'{kap:6.3f}')} {str(kci):>14s} {pabak:6.3f}  {note}")
    rows.append([item, "ordinal 0-2", len(c1), round(po, 3), round(within, 3),
                 "" if kap is None else round(kap, 3), kci[0], kci[1], round(pabak, 3), note])

for item in NOM:
    c1 = [ds[r["id"]][item] for r in c2]
    c2v = [r[item] for r in c2]
    pairs = list(zip(c1, c2v))
    po, kap = agree(c1, c2v)
    kci = ci(pairs, lambda a, b: agree(a, b)[1])
    pabak = 2 * po - 1
    note = "" if kap is not None else "undefined (single level in sample)"
    print(f"{item:14s} {len(c1):3d} {po:6.3f} {'  —':>5s} "
          f"{('  n/a' if kap is None else f'{kap:6.3f}')} {str(kci):>14s} {pabak:6.3f}  {note}")
    rows.append([item, "nominal", len(c1), round(po, 3), "", "" if kap is None else round(kap, 3),
                 kci[0], kci[1], round(pabak, 3), note])

with open(OUT / "tableS11_reliability.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item", "scale", "n", "exact_agreement", "within_one", "kappa",
                  "kappa_ci_low", "kappa_ci_high", "pabak", "note"])
    w.writerows(rows)

# derived-claim check on the same 30 rows
gap = {}
print("\nderived claims (same 30 rows): coder1 | coder2")
for track in ["threat", "defense", "both", "pqc-context"]:
    ids = [i for i in by2 if ds[i]["track"] == track]
    m1 = sum(int(ds[i]["R2"]) for i in ids) / len(ids)
    m2 = sum(int(by2[i]["R2"]) for i in ids) / len(ids)
    print(f"  mean R2 {track:12s} (n={len(ids):2d}): {m1:.2f} | {m2:.2f}")
    if track in ("threat", "defense"):
        gap[track] = (m1, m2)
ids = list(by2)
print(f"  mean R2 all          (n={len(ids):2d}): "
      f"{sum(int(ds[i]['R2']) for i in ids) / len(ids):.2f} | "
      f"{sum(int(by2[i]['R2']) for i in ids) / len(ids):.2f}")
print(f"  R2 gap threat-defense: {gap['threat'][0] - gap['defense'][0]:+.2f} | "
      f"{gap['threat'][1] - gap['defense'][1]:+.2f}")
for label, f1, f2 in [
    ("RFFI share", lambda i: ds[i]["function"] == "Authentication/RFFI",
     lambda i: by2[i]["function"] == "Authentication/RFFI"),
    ("artifact rate (R4>=1)", lambda i: int(ds[i]["R4"]) >= 1, lambda i: int(by2[i]["R4"]) >= 1),
    ("standards signal (R5>=1)", lambda i: int(ds[i]["R5"]) >= 1, lambda i: int(by2[i]["R5"]) >= 1),
    ("explicit threat model (R1=2)", lambda i: int(ds[i]["R1"]) == 2, lambda i: int(by2[i]["R1"]) == 2),
]:
    print(f"  {label:26s}       : {sum(f1(i) for i in ids) / len(ids):.3f} | "
          f"{sum(f2(i) for i in ids) / len(ids):.3f}")

# disagreements, for adjudication
dis = []
for r in c2:
    d = ds[r["id"]]
    for item in ORD + NOM:
        if str(d[item]) != r[item]:
            dis.append((r["id"], item, d[item], r[item]))
print(f"\ndisagreements: {len(dis)} cells across {len({d[0] for d in dis})} rows")
with open(OUT / "disagreements.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "item", "coder1", "coder2", "adjudicated", "evidence", "resolution"])
    for row in sorted(dis):
        w.writerow(list(row) + ["", "", ""])
print("wrote tableS11_reliability.csv, disagreements.csv")
