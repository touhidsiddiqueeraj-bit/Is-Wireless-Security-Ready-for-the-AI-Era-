#!/usr/bin/env python3
"""Is the low kappa a chance-correction artefact? Report the coefficient family.

Unweighted kappa, quadratic-weighted kappa, Krippendorff's alpha (ordinal),
Gwet's AC1, and binary-collapsed kappa (0-1 -> 0, 2 -> 1) on the same 30 rows.
"""
import csv, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reliability"
ORD = ["R1", "R2", "R3", "R5"]
LV = {"validation": ["Testbed/field demonstration", "Simulation-only",
                     "Cross-domain/generalization test", "Standard split/unclear",
                     "Benchmark/analysis"],
      "data_source": ["Testbed/OTA measurement", "Collected dataset/traces", "Simulation",
                      "Analysis/benchmark", "Unclear (abstract)"]}

ds = {r["id"]: r for r in csv.DictReader(open(ROOT / "dataset_papers.csv"))}
c2 = {r["id"]: r for r in csv.DictReader(open(OUT / "coder2_scores.csv"))}


def cohen(p):
    n = len(p)
    po = sum(a == b for a, b in p) / n
    ca, cb = collections.Counter(a for a, _ in p), collections.Counter(b for _, b in p)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n**2
    return (po - pe) / (1 - pe)


def weighted(p, k=3):
    n = len(p)
    d = lambda i, j: (i - j) ** 2 / (k - 1) ** 2
    o = collections.Counter(p)
    ca, cb = collections.Counter(a for a, _ in p), collections.Counter(b for _, b in p)
    do = sum(d(i, j) * v for (i, j), v in o.items()) / n
    de = sum(d(i, j) * ca[i] * cb[j] / n**2 for i in range(k) for j in range(k))
    return 1 - do / de


def alpha(p, q):
    o, n = collections.Counter(), 2 * len(p)
    for a, b in p:
        o[(a, b)] += 1
        o[(b, a)] += 1
    m = collections.Counter()
    for (x, y), c in o.items():
        m[x] += c

    def dlt(c, k):
        lo, hi = min(c, k), max(c, k)
        inner = sum(m[g] for g in range(lo, hi + 1)) - (m[lo] + m[hi]) / 2
        return inner**2

    do = sum(c * dlt(x, y) for (x, y), c in o.items()) / n
    de = sum(m[x] * m[y] * dlt(x, y) for x in range(q) for y in range(q)) / (n * (n - 1))
    return 1 - do / de if de else None


def ac1(p, q):
    po = sum(a == b for a, b in p) / len(p)
    m = collections.Counter()
    for a, b in p:
        m[a] += 1
        m[b] += 1
    pi = [m[k] / (2 * len(p)) for k in range(q)]
    pe = sum(x * (1 - x) for x in pi) / (q - 1)
    return (po - pe) / (1 - pe) if pe < 1 else None


rows = []
for item in ORD:
    p = [(int(ds[i][item]), int(c2[i][item])) for i in c2]
    b = [(x >= 2, y >= 2) for x, y in p]
    kb = cohen(b) if len({x for x, _ in b}) > 1 and len({y for _, y in b}) > 1 else None
    rows.append([item, round(cohen(p), 3), round(weighted(p), 3), round(alpha(p, 3), 3),
                 round(ac1(p, 3), 3), "" if kb is None else round(kb, 3),
                 str(dict(sorted(collections.Counter(x for x, _ in p).items())))])
for item, levels in LV.items():
    p = [(levels.index(ds[i][item]), levels.index(c2[i][item])) for i in c2]
    # no weighting for nominal items: the level order is arbitrary
    rows.append([item, round(cohen(p), 3), "", round(alpha(p, len(levels)), 3),
                 round(ac1(p, len(levels)), 3), "",
                 str(dict(sorted(collections.Counter(x for x, _ in p).items())))])

# self-check: weighted kappa must reproduce the published Table S11 values
pub = {r["item"]: r["kappa"] for r in csv.DictReader(open(OUT / "tableS11_reliability.csv"))}
for r in rows:
    if not pub.get(r[0]):
        continue
    got = r[2] if r[0] in ORD else r[1]      # weighted for ordinal, unweighted for nominal
    assert abs(float(got) - float(pub[r[0]])) < 5e-4, (r[0], got, pub[r[0]])

with open(OUT / "tableS12_coefficients.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item", "kappa_unweighted", "kappa_weighted", "krippendorff_alpha",
                "gwet_ac1", "kappa_binary_collapsed", "coder1_level_counts"])
    w.writerows(rows)
for r in rows:
    wv = "   n/a" if r[2] == "" else f"{r[2]:6.3f}"
    print(f"{r[0]:12s} uw={r[1]:6.3f} w={wv} alpha={r[3]:6.3f} AC1={r[4]:6.3f} "
          f"collapsed={'   n/a' if r[5] == '' else f'{r[5]:6.3f}'}  {r[6]}")
print("wrote tableS12_coefficients.csv")
