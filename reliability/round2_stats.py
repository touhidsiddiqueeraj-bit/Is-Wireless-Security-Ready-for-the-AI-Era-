#!/usr/bin/env python3
"""Round-2 agreement: five clarified items + R5 control. Same estimators as round 1.

Self-check: reproduces round 1's R1 kappa from coder2_scores.csv before computing round 2.
"""
import csv, collections, random, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reliability"
ORD = ["R1", "R2", "R3", "R5"]
NOM = ["validation", "data_source"]
B = 2000
random.seed(7)

ds = {r["id"]: r for r in csv.DictReader(open(ROOT / "dataset_papers.csv"))}
r1 = {r["id"]: r for r in csv.DictReader(open(OUT / "coder2_scores.csv"))}
r2 = list(csv.DictReader(open(OUT / "coder2_round2.csv")))
assert len(r2) == 30


def agree(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n**2
    return po, ((po - pe) / (1 - pe) if pe < 1 else None)


def qwk(a, b, k=3):
    n = len(a)
    o = collections.Counter(zip(a, b))
    ca, cb = collections.Counter(a), collections.Counter(b)
    d = lambda i, j: (i - j) ** 2 / (k - 1) ** 2
    do = sum(d(i, j) * v for (i, j), v in o.items())
    de = sum(d(i, j) * ca[i] * cb[j] / n for i in range(k) for j in range(k))
    return 1 - do / de if de else None


def ci(pairs, fn):
    vals = []
    for _ in range(B):
        s = [pairs[random.randrange(len(pairs))] for _ in pairs]
        v = fn([x for x, _ in s], [y for _, y in s])
        if v is not None:
            vals.append(v)
    vals.sort()
    return (round(vals[int(.025 * len(vals))], 3), round(vals[int(.975 * len(vals)) - 1], 3)) if vals else (None, None)


# self-check against round 1 (published value is rounded to 3 dp)
_r1p = [(int(ds[i]["R1"]), int(r1[i]["R1"])) for i in r1]
assert abs(qwk([x for x, _ in _r1p], [y for _, y in _r1p]) - 0.394) < 5e-4, "estimator drift"


def pairs_for(rowmap, item):
    if item in ORD:
        return [(int(ds[i][item]), int(rowmap[i][item])) for i in rowmap]
    return [(ds[i][item], rowmap[i][item]) for i in rowmap]


def kappa_of(p, item):
    a, b = [x for x, _ in p], [y for _, y in p]
    return qwk(a, b) if item in ORD else agree(a, b)[1]


rows = []
print(f"{'item':13s} {'r1':>6s} {'r2':>6s} {'95% CI':>14s} {'exact':>6s} {'PABAK':>6s} {'delta':>6s}")
for item in ORD + NOM:
    p = pairs_for({r["id"]: r for r in r2}, item)
    a, b = [x for x, _ in p], [y for _, y in p]
    po, _ = agree(a, b)
    k1, k2 = kappa_of(pairs_for(r1, item), item), kappa_of(p, item)
    kci = ci(p, lambda x, y: qwk(x, y) if item in ORD else agree(x, y)[1])
    pabak = 2 * po - 1
    f = lambda v: "  n/a" if v is None else f"{v:6.3f}"
    d = "   n/a" if (k1 is None or k2 is None) else f"{k2 - k1:+.3f}"
    print(f"{item:13s} {f(k1)} {f(k2)} {str(kci):>14s} {po:6.3f} {pabak:6.3f} {d:>6s}")
    rows.append([item, "ordinal 0-2" if item in ORD else "nominal", 30, round(po, 3),
                 "" if k2 is None else round(k2, 3), kci[0], kci[1], round(pabak, 3),
                 "" if k1 is None else round(k1, 3)])

with open(OUT / "tableS11b_round2.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["item", "scale", "n", "exact_agreement", "kappa_round2",
                "kappa_ci_low", "kappa_ci_high", "pabak", "kappa_round1"])
    w.writerows(rows)

print("\nderived claims under round-2 coding (coder1 | coder2-r2):")
b2 = {r["id"]: r for r in r2}
for t in ["threat", "defense", "both", "pqc-context"]:
    ids = [i for i in b2 if ds[i]["track"] == t]
    print(f"  mean R2 {t:12s} (n={len(ids):2d}): "
          f"{sum(int(ds[i]['R2']) for i in ids) / len(ids):.2f} | "
          f"{sum(int(b2[i]['R2']) for i in ids) / len(ids):.2f}")
ids = list(b2)
th = [i for i in ids if ds[i]["track"] == "threat"]
de = [i for i in ids if ds[i]["track"] == "defense"]
for tag, src in [("coder1", lambda i: int(ds[i]["R2"])), ("coder2-r2", lambda i: int(b2[i]["R2"]))]:
    print(f"  {tag:10s} gap threat-defense = "
          f"{sum(src(i) for i in th) / len(th) - sum(src(i) for i in de) / len(de):+.2f}")
print("wrote tableS11b_round2.csv")
