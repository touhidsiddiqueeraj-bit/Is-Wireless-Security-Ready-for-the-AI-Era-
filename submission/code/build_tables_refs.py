"""Build machine-generated submission artifacts from the released dataset.

Reads ../data/dataset_papers.csv + ../data/found_papers.csv and writes:
  ../tables/Table2_method_families.csv (dataset-counted, no double count)
  ../tables/Table3_function_by_year.csv
  ../tables/Table45_data_validation.csv
  ../tables/Table6_venue_sensitivity.csv
  ../tables/TableR_readiness_means.csv
  ../tables/refs_fragment.tex   (corpus-ID keyed reference list)
Run: python3 build_tables_refs.py
"""
import csv
from collections import Counter

DATA = "../data"
TABLES = "../tables"

with open(f"{DATA}/dataset_papers.csv") as f:
    ds = list(csv.DictReader(f))
fp = {}
with open(f"{DATA}/found_papers.csv") as f:
    for r in csv.DictReader(f):
        fp[r["id"]] = r

ids = [r["id"] for r in ds]
assert all(i in fp for i in ids), "dataset/found_papers mismatch"
N = len(ids)
assert N == len(ds), "duplicate ids"

# ---- Table 2: method families (dataset-counted) ---------------------------------
with open(f"{TABLES}/Table2_method_families.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["method_family", "papers"])
    mc = Counter(r["method_family"] for r in ds)
    for m, c in mc.most_common():
        w.writerow([m, c])
    assert sum(mc.values()) == N, f"Table2 sum {sum(mc.values())} != N {N}"

# ---- Table 3: function x year ------------------------------------------------
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
with open(f"{TABLES}/Table3_function_by_year.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["function"] + YEARS + ["total"])
    for fn in sorted(set(r["function"] for r in ds)):
        cells = [sum(1 for r in ds if r["function"] == fn and r["year"] == y) for y in YEARS]
        w.writerow([fn] + cells + [sum(cells)])

# ---- Table 6: venue-channel sensitivity (journal / conference / preprint) -----
CHS = ["journal", "conference", "preprint"]
VALS = ["Testbed/field demonstration", "Cross-domain/generalization test",
        "Simulation-only", "Standard split/unclear", "Benchmark/analysis"]
with open(f"{TABLES}/Table6_venue_sensitivity.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["validation"] + [f"{c}_n{sum(1 for r in ds if r['venue_channel'] == c)}" for c in CHS])
    for v in VALS:
        w.writerow([v] + [sum(1 for r in ds if r["venue_channel"] == c and r["validation"] == v)
                          for c in CHS])

# ---- Table 45: data_source + validation ----------------------------------------
with open(f"{TABLES}/Table45_data_validation.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["dimension", "value", "papers"])
    for d, c in Counter(r["data_source"] for r in ds).most_common():
        w.writerow(["data_source", d, c])
    for v, c in Counter(r["validation"] for r in ds).most_common():
        w.writerow(["validation", v, c])

# ---- Table R: readiness means per track (threat R3/R5 are N/A: emitted as n/a) ----
def _tmean(rows, col, na=False):
    if na:
        return "n/a"
    return round(sum(int(r[col]) for r in rows) / len(rows), 2)
with open(f"{TABLES}/TableR_readiness_means.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["track", "n", "R1", "R2", "R3", "R4", "R5"])
    for t in ["threat", "defense", "both", "pqc-context"]:
        rows = [r for r in ds if r["track"] == t]
        na = (t == "threat")
        w.writerow([t, len(rows)] + [_tmean(rows, c, na and c in ("R3", "R5")) for c in ["R1", "R2", "R3", "R4", "R5"]])

# ---- Reference list fragment (corpus-ID keyed) --------------------------------
def tex_escape(s):
    return (s.replace("\\", "\\textbackslash{}").replace("&", "\\&")
             .replace("%", "\\%").replace("#", "\\#").replace("_", "\\_"))


def order_key(pid):
    return (pid[0], int(pid[1:]))


lines = ["% Auto-generated from data/found_papers.csv — do not hand-edit.",
         "\\begin{enumerate}"]
for pid in sorted(ids, key=order_key):
    m = fp[pid]
    venue_bit = f", {tex_escape(m['venue'])}" if m["venue"].strip() else ""
    lines.append(f"\\item[{pid}] {tex_escape(m['authors'])}, "
                 f"``{tex_escape(m['title'])},''{venue_bit}, {m['year'].strip()}. "
                 f"\\url{{{m['doi_url'].strip()}}}")
lines.append("\\end{enumerate}")
with open(f"{TABLES}/refs_fragment.tex", "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"wrote Table2, Table3, Table45, Table6, TableR, refs_fragment (N={N})")
