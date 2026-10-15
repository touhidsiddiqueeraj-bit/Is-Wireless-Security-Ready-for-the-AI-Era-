"""Verify manuscript headline numbers against the released dataset_papers.csv."""
import csv
from collections import Counter, defaultdict

import pathlib as _pl
with open(_pl.Path(__file__).resolve().parent.parent / 'data' / 'dataset_papers.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

N = len(rows)
print(f"N = {N}")
print()

# 1. Track split
tc = Counter(r['track'] for r in rows)
print("TRACK SPLIT:", dict(tc))

# 2. Function counts
fc = Counter(r['function'] for r in rows)
print("\nFUNCTION COUNTS:")
for k, v in fc.most_common():
    print(f"  {k}: {v}")

# 3. Method family counts
mc = Counter(r['method_family'] for r in rows)
print("\nMETHOD FAMILIES:", dict(mc.most_common()))

# 4. Validation counts (Table 8)
vc = Counter(r['validation'] for r in rows)
print("\nVALIDATION COUNTS (Table 8 claims: Testbed 47, Cross 26, Sim 18, Std 35, Bench 4):")
for k, v in vc.most_common():
    print(f"  {k}: {v}")

# 5. Validation x function cross-tab (Table 9) - THE DISPUTED TABLE
print("\nVALIDATION x FUNCTION CROSS-TAB (Table 9):")
funcs = sorted(set(r['function'] for r in rows))
vals = sorted(set(r['validation'] for r in rows))
xtab = defaultdict(Counter)
for r in rows:
    xtab[r['function']][r['validation']] += 1
col_sums = Counter()
for fn in funcs:
    line = f"  {fn} ({sum(xtab[fn].values()):3d}): "
    parts = []
    for v in vals:
        c = xtab[fn][v]
        col_sums[v] += c
        parts.append(f"{v}={c}")
    print(line + ", ".join(parts))
print("  COLUMN SUMS:", dict(col_sums))

# 6. Venue channel
cc = Counter(r['venue_channel'] for r in rows)
print("\nVENUE CHANNEL (claims: 65 journal, 46 conference, 19 preprint):", dict(cc))

# 7. Validation x venue channel (Table 11)
print("\nVALIDATION x VENUE CHANNEL (Table 11):")
xtab2 = defaultdict(Counter)
for r in rows:
    xtab2[r['validation']][r['venue_channel']] += 1
for v in vals:
    print(f"  {v}: {dict(xtab2[v])}")

# 8. R-means per track (Fig 10 / claims)
def mean(vals):
    vals = [float(v) for v in vals if v not in ('', None, 'NA')]
    return sum(vals) / len(vals) if vals else float('nan')

print("\nR-MEANS PER TRACK (claims: threat R1 1.70 R2 1.53; defense R1 1.14 R2 1.27 R3 0.19 R4 0.02 R5 0.07; dual R1 1.86 R2 1.14 R3 0.14 R5 0.14; PQC R1 1.00 R2 1.44 R3 1.11 R5 0.56):")
for tr in sorted(set(r['track'] for r in rows)):
    sub = [r for r in rows if r['track'] == tr]
    line = f"  {tr} (n={len(sub)}): "
    for rx in ['R1', 'R2', 'R3', 'R4', 'R5']:
        vals_ = [r[rx] for r in sub if r[rx] != 'NA']
        if vals_:
            line += f"{rx}={mean(vals_):.2f} "
        else:
            line += f"{rx}=NA "
    print(line)

# R5 mean over defense only
d5 = [float(r['R5']) for r in rows if r['track'] == 'defense' and r['R5'] != 'NA']
print(f"\n  Defense R5 over {len(d5)} scored rows: mean={sum(d5)/len(d5):.3f}")

# 9. R-score distributions (Table 5)
print("\nR-SCORE DISTRIBUTIONS over 130 rows (Table 5: R3 0/101 1/25 2/4; R4 0/126 1/4; R5 0/113 1/17):")
for rx in ['R1', 'R2', 'R3', 'R4', 'R5']:
    c = Counter(r[rx] for r in rows)
    print(f"  {rx}: {dict(sorted(c.items()))}")

# 10. R4 artifacts: which rows have R4>=1
print("\nR4 >= 1 rows (claims 4 verified releases):")
for r in rows:
    if r['R4'] in ('1', '2'):
        print(f"  {r['id']} [{r['track']}] {r['title_short'][:60]} R4={r['R4']}")

# 11. R5 >= 1 rows (claims 12 core + 5 attack = 17)
print("\nR5 >= 1 rows (claims 17 total: 6 defense + 1 dual + 5 attack-named + 5 PQC):")
for r in rows:
    if r['R5'] in ('1', '2'):
        print(f"  {r['id']} [{r['track']}] {r['title_short'][:50]} R5={r['R5']}")

# 12. Year distribution
yc = Counter(r['year'] for r in rows)
print("\nYEAR DISTRIBUTION (claims: 4, 17, 10, 21, 29, 36, 13):", dict(sorted(yc.items())))

# 13. R1=2 count (claims 39 of 130)
r1_2 = sum(1 for r in rows if r['R1'] == '2')
print(f"\nR1=2 count (claims 39): {r1_2}")

# 14. Adversarial ML by track (claims 20 threat / 7 dual / 13 defense)
adv = Counter(r['track'] for r in rows if 'adv' in r['method_family'].lower())
print("\nADVERSARIAL ML by track (claims 20/7/13):", dict(adv))

# 15. Deep supervised by track (claims 42 defense / 3 threat)
ds = Counter(r['track'] for r in rows if 'deep' in r['method_family'].lower())
print("DEEP SUPERVISED by track (claims 42 defense, 3 threat):", dict(ds))

# 16. Coding depth
cd = Counter(r['coding_depth'] for r in rows)
print("\nCODING DEPTH (claims 110 abstract-only, 20 body-read):", dict(cd))

# 17. Closed-loop: dual-track IDs (claims D08, D36, D37, T05, T11, T14, T46)
duals = [r['id'] for r in rows if r['track'] in ('both', 'dual')]
print("\nDUAL-TRACK IDs (claims D08, D36, D37, T05, T11, T14, T46):", sorted(duals))
