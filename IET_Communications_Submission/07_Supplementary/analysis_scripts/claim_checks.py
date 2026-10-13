"""Compute every number reported in the manuscript, directly from dataset_papers.csv.

Outputs a JSON + readable summary of the consolidated claim checks.
Integrity rule: only numbers computable from the released CSV are produced here;
process facts (funnel, reconciliation drift, verifier sample) stay as disclosed text.
"""
import csv, json
from collections import Counter, defaultdict

import pathlib as _pl
CSV = str(_pl.Path(__file__).resolve().parent.parent / 'data' / 'dataset_papers.csv')
rows = []
with open(CSV, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append(r)
N = len(rows)
print(f"Corpus rows: {N}")

def rscore(r, k):
    v = r[k].strip()
    try: return int(v)
    except: return 0

# ---------- 1. Corpus split ----------
track = Counter(r["track"] for r in rows)
print("Track split:", dict(track))

# ---------- 2. Preprint count ----------
pre = [r for r in rows if r["venue_channel"] == "preprint"]
print(f"Preprints: {len(pre)} ({len(pre)/N*100:.1f}%)")

# ---------- 3. R-means per track ----------
def rmeans(subset):
    out = {}
    for k in ["R1","R2","R3","R4","R5"]:
        out[k] = round(sum(rscore(r,k) for r in subset)/len(subset), 2) if subset else None
    return out
for t in ["threat","defense","both","pqc-context"]:
    sub = [r for r in rows if r["track"]==t]
    print(f"  {t} (n={len(sub)}): {rmeans(sub)}")

# ---------- 4. Table 9 regen: function x validation ----------
funcs = ["Authentication/RFFI","Anti-jamming/secure comms","Key generation/distribution",
         "Federated/privacy-preserving FL","Protocol/traffic/cryptanalysis","PQC migration (contextual)",
         "Learned primitives/crypto","Side-channel attack analysis"]
vals = ["Testbed/field demonstration","Cross-domain/generalization test","Simulation-only",
        "Standard split/unclear","Benchmark/analysis"]
print("\nTable 9 regen (function x validation):")
t9 = {}
for fu in funcs:
    sub = [r for r in rows if r["function"]==fu]
    counts = [sum(1 for r in sub if r["validation"]==v) for v in vals]
    t9[fu] = {"total": len(sub), "counts": counts}
    print(f"  {fu} ({len(sub)}): {counts}  sum={sum(counts)}")

# ---------- 5. Table 8 regen: validation totals ----------
print("\nValidation totals:", {v: sum(1 for r in rows if r["validation"]==v) for v in vals})
print("Data-source totals:", dict(Counter(r["data_source"] for r in rows)))

# ---------- 6. Coding-depth splits (M2 remediation) ----------
depth = Counter(r["coding_depth"] for r in rows)
print(f"\nCoding depth: {dict(depth)}")
body = [r for r in rows if r["coding_depth"]=="full-text"]
abstract = [r for r in rows if r["coding_depth"]=="abstract"]
print(f"Body-read n={len(body)}, abstract n={len(abstract)}")
print("Body-read validation mix:", dict(Counter(r["validation"] for r in body)))
print("Body-read track mix:", dict(Counter(r["track"] for r in body)))
print("Abstract rows sim-only:", sum(1 for r in abstract if r["validation"]=="Simulation-only"))
print("Body-read R2 mean:", round(sum(rscore(r,'R2') for r in body)/len(body),2),
      "| abstract R2 mean:", round(sum(rscore(r,'R2') for r in abstract)/len(abstract),2))
# threat testbed rows by depth
tt = [r for r in rows if r["track"]=="threat" and r["validation"]=="Testbed/field demonstration"]
print(f"Threat testbed rows: {len(tt)}; of which body-read: {sum(1 for r in tt if r['coding_depth']=='body-read')}, "
      f"abstract: {sum(1 for r in tt if r['coding_depth']=='abstract')}")
# R2 by track within abstract-coded rows only (robustness of the asymmetry)
print("\nR2 means within abstract-coded rows only:")
for t in ["threat","defense","both"]:
    sub = [r for r in abstract if r["track"]==t]
    if sub: print(f"  {t} (n={len(sub)}): {rmeans(sub)}")
print("R2 means within body-read rows only:")
for t in ["threat","defense","both"]:
    sub = [r for r in body if r["track"]==t]
    if sub: print(f"  {t} (n={len(sub)}): {rmeans(sub)}")

# ---------- 7. R5 sensitivity (M4): strict reading ----------
# R5=1 = "mentions a standards body"; R5=2 = "evaluated against a profile".
# Strict test: score R5'=0 when R5==1 (mentions-only counts as no standards signal).
print("\nR5 sensitivity: mentions-only rows scored 0 (strict):")
for t in ["defense","both","pqc-context"]:
    sub = [r for r in rows if r["track"]==t]
    base = sum(rscore(r,'R5') for r in sub)/len(sub)
    strict = sum(rscore(r,'R5') if rscore(r,'R5')==2 else 0 for r in sub)/len(sub)
    print(f"  {t}: base mean {base:.2f} -> strict {strict:.2f}")
r5_one = [r["id"] for r in rows if rscore(r,'R5')==1]
print(f"  Rows with R5=1 (mention-level): {len(r5_one)} -> {r5_one}")
r5_two = [r["id"] for r in rows if rscore(r,'R5')==2]
print(f"  Rows with R5=2 (profile-evaluated): {len(r5_two)} -> {r5_two}")

# ---------- 8. R2 collapse sensitivity (M4): what R2=1 contains ----------
print("\nR2=1 composition by validation (all rows):")
comp = Counter(r["validation"] for r in rows if rscore(r,'R2')==1)
print("  ", dict(comp))
for t in ["threat","defense","both"]:
    comp_t = Counter(r["validation"] for r in rows if rscore(r,'R2')==1 and r["track"]==t)
    print(f"  {t}: {dict(comp_t)}")

# ---------- 9. Table 11 regen: venue channel x validation ----------
print("\nVenue channel x validation:")
chans = ["journal","conference","preprint"]
t11 = {}
for c in chans:
    sub = [r for r in rows if r["venue_channel"]==c]
    t11[c] = {v: sum(1 for r in sub if r["validation"]==v) for v in vals}
    print(f"  {c} (n={len(sub)}):", t11[c])
    print(f"    R2 mean: {rmeans(sub)['R2']}, testbed share: {t11[c]['Testbed/field demonstration']/len(sub)*100:.0f}%")

# ---------- 10. Checklist-adherence regen ----------
r1_2 = sum(1 for r in rows if rscore(r,'R1')==2)
r4_1 = [r["id"] for r in rows if rscore(r,'R4')>=1]
tb_col = sum(1 for r in rows if r["data_source"] in ("Testbed/OTA measurement","Collected datasets/traces"))
unc = sum(1 for r in rows if r["data_source"].startswith("Unclear"))
core = [r for r in rows if r["track"] in ("threat","defense","both")]
r3d = sum(rscore(r,'R3') for r in rows if r["track"]=="defense")
print("\nChecklist adherence:")
print(f"  R1=2 (explicit adversary): {r1_2}/{N}")
print(f"  R4>=1 artifacts: {len(r4_1)}/{len(core)} core -> {r4_1}")
print(f"  testbed-or-collected with named source: {tb_col}; unclear: {unc}")
print(f"  defense R3 sum/mean: {r3d}/{round(r3d/84,2)}")

# ---------- 11. Year x function (Table 4) ----------
years = ["2020","2021","2022","2023","2024","2025","2026"]
print("\nTable 4 regen (function x year):")
for fu in funcs:
    sub = [r for r in rows if r["function"]==fu]
    yc = [sum(1 for r in sub if r["year"]==y) for y in years]
    print(f"  {fu}: {yc} total {len(sub)}")
print("Year totals:", [sum(1 for r in rows if r["year"]==y) for y in years])

# ---------- 12. Margins quoted in abstract/conclusion ----------
th = [r for r in rows if r["track"]=="threat"]; de = [r for r in rows if r["track"]=="defense"]; bo = [r for r in rows if r["track"]=="both"]
print("\nMargins:")
print(f"  threat R2 {rmeans(th)['R2']} vs defense R2 {rmeans(de)['R2']} -> gap {rmeans(th)['R2']-rmeans(de)['R2']:.2f}")
print(f"  both R2 {rmeans(bo)['R2']} vs defense -> margin {rmeans(bo)['R2']-rmeans(de)['R2']:.2f} (n=7)")
print(f"  threat R1 {rmeans(th)['R1']}, defense R1 {rmeans(de)['R1']}, both R1 {rmeans(bo)['R1']}")

# ---------- 13. Anchor examples for rubric (M4 remediation) ----------
print("\nAnchor candidates:")
print("  R1=2 (explicit adversary):", [r["id"] for r in rows if rscore(r,'R1')==2][:12])
print("  R2=2 (OTA/testbed demo):", [r["id"] for r in rows if rscore(r,'R2')==2])
print("  R3=2:", [r["id"] for r in rows if rscore(r,'R3')==2])
print("  R4=1:", r4_1)
print("  R5=1:", r5_one)
print("  R5=2:", r5_two)

# ---------- 14. Venue channel counts + R2 by channel ----------
print("\nVenue channels:", dict(Counter(r["venue_channel"] for r in rows)))

# ---------- 15. Method family x track (Fig 6) ----------
print("\nMethod family totals:", dict(Counter(r["method_family"] for r in rows)))

out = {
    "N": N, "track": dict(track), "preprints": len(pre),
    "preprint_pct": round(len(pre)/N*100, 1),
    "table9": t9, "validation_totals": {v: sum(1 for r in rows if r["validation"]==v) for v in vals},
    "channel_validation": t11,
    "depth": dict(depth),
}
with open("claim_checks.json","w") as f:
    json.dump(out, f, indent=1)
print("\nSaved claim_checks.json")
