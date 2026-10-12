"""Consistency gate for the N=130 corpus (v4 refreeze). Fails on any stale n / split / caption.
Run: python3 check_consistency.py (from submission/code/). Reads ../data/*.csv.
"""
import csv, collections, re, sys, pathlib

CODE = pathlib.Path(__file__).parent
DATA = CODE.parent / "data"
ROOT_SUB = CODE.parent
TEX = ROOT_SUB / "manuscript.tex"

ds = list(csv.DictReader(open(DATA / "dataset_papers.csv")))
fp = {r["id"]: r for r in csv.DictReader(open(DATA / "found_papers.csv"))}
tex = TEX.read_text()

errs = []
def check(cond, msg):
    if not cond:
        errs.append(msg)

N = len(ds)
check(N == 130, f"N={N} expected 130")
check(len(set(r["id"] for r in ds)) == N, "duplicate ids in dataset")
check(set(r["id"] for r in ds) <= set(fp), "dataset id missing in found_papers")

trk = collections.Counter(r["track"] for r in ds)
check(trk["defense"] == 84 and trk["threat"] == 30 and trk["both"] == 7 and trk["pqc-context"] == 9,
      f"track split {dict(trk)} expected 84/30/7/9")

yrs = collections.Counter(r["year"] for r in ds)
check(dict(sorted(yrs.items())) == {"2020":4,"2021":17,"2022":10,"2023":21,"2024":29,"2025":36,"2026":13},
      f"years {dict(sorted(yrs.items()))}")

ch = collections.Counter(r["venue_channel"] for r in ds)
check(ch["journal"]==65 and ch["conference"]==46 and ch["preprint"]==19, f"channels {dict(ch)}")

meth = collections.Counter(r["method_family"] for r in ds)
check(meth["Adversarial ML"]==40 and meth["Deep supervised (CNN/RNN/Transformer)"]==45,
      f"methods {meth['Adversarial ML']}/{meth['Deep supervised (CNN/RNN/Transformer)']} expected 40/45")
check("Protocol fuzzing/analysis" not in meth, "Protocol fuzzing/analysis family should be gone (T07 excluded)")
# Table2 tail must equal dataset tail (no double count)
tail = N - (meth["Adversarial ML"]+meth["Deep supervised (CNN/RNN/Transformer)"]+meth["Reinforcement/DRL"]+meth["PQC implementation"]+meth["Federated/private learning"])
check(tail == sum(meth[k] for k in meth if k not in ("Adversarial ML","Deep supervised (CNN/RNN/Transformer)","Reinforcement/DRL","PQC implementation","Federated/private learning")),
      "method tail mismatch")

# deep-sup cumulative and RFFI share
deep=[r for r in ds if r["method_family"].startswith("Deep supervised")]
check(sum(1 for r in deep if int(r["year"])<=2023)==21, "deep cum<=2023 must be 21")
check(sum(1 for r in deep if r["function"]=="Authentication/RFFI")==33, "deep RFFI must be 33/45")

# data / validation
check(collections.Counter(r["data_source"] for r in ds)==collections.Counter({"Testbed/OTA measurement":46,"Collected dataset/traces":26,"Simulation":20,"Analysis/benchmark":6,"Unclear (abstract)":32}), "data_source mismatch")
check(collections.Counter(r["validation"] for r in ds)==collections.Counter({"Testbed/field demonstration":47,"Standard split/unclear":35,"Cross-domain/generalization test":26,"Simulation-only":18,"Benchmark/analysis":4}), "validation mismatch")

# R2 mapping uniformity: R2 must equal f(validation) except logged key-recovery exceptions
RMAP={"Testbed/field demonstration":"2","Cross-domain/generalization test":"1","Standard split/unclear":"1","Simulation-only":"1","Benchmark/analysis":"0"}
bad=[(r["id"],r["validation"],r["R2"]) for r in ds if r["id"] not in ("T01","T08") and r["R2"]!=RMAP[r["validation"]]]
check(len(bad)==0, f"R2 mapping violations: {bad}")
# coding depth: 20 body-read rows (fulltext log + T28/T30 proceedings) vs 110 abstract-coded
check(sum(1 for r in ds if r.get("coding_depth")=="full-text")==20, "depth full-text count drift")
check(sum(1 for r in ds if r.get("coding_depth")=="abstract")==110, "depth abstract count drift")
# FL-7 sensitivity numbers cited in §3.1 (recompute, never hand-copy)
FL7 = {"D82","D83","D84","D85","D86","D87","D88"}
sub = [r for r in ds if r["id"] not in FL7]
subd = [r for r in sub if r["track"] == "defense"]
subt = [r for r in sub if r["track"] == "threat"]
check(round(sum(int(r["R2"]) for r in subd)/len(subd),2)==1.32, "FL-sensitivity defense R2 drift")
check(round(sum(int(r["R2"]) for r in subt)/len(subt),2)==1.53, "FL-sensitivity threat R2 drift")
check(sum(1 for r in sub if r["year"]=="2021")==12, "FL-sensitivity 2021 count drift")
check("1.32 instead of 1.27" in tex and "unchanged at 1.53" in tex, "FL-sensitivity sentence drift")

# readiness means
def mean(track, col):
    rows=[r for r in ds if r["track"]==track]
    return round(sum(int(r[col]) for r in rows)/len(rows),2)
check(mean("threat","R2")==1.53 and mean("defense","R2")==1.27 and mean("both","R2")==1.14, "R2 means drift")
check(mean("threat","R1")==1.7 and mean("threat","R5")==0.17 and mean("threat","R4")==0.07 and mean("defense","R5")==0.07 and mean("defense","R3")==0.19, "R-means drift")

# year-table (Table 3) totals must match the year distribution
yrsum = {"2020":4,"2021":17,"2022":10,"2023":21,"2024":29,"2025":36,"2026":13}
for s in [f"{v} ({k})" for k,v in yrsum.items()]:
    pass  # totals live in CSV; tex table checked below via column sums
check("3 (2020), 12 (2021)" not in tex and "12 (2021), 8 (2022)" not in tex, "stale year profile in tex")

# year_first audit column (earliest evidenced public date; issue-year stays primary)
check("year_first" in ds[0], "year_first column missing")
check({r["id"]:r["year_first"] for r in ds if r["year_first"]!=r["year"]}=={"P05":"2020","D36":"2021"}, "year_first diffs")
# year-table (Table 3) column sums must match the year distribution (catches unregenerated tables)
yrsum = {"2020":4,"2021":17,"2022":10,"2023":21,"2024":29,"2025":36,"2026":13}
import os
t3p = ROOT_SUB / "tables" / "Table3_function_by_year.csv"
if os.path.exists(t3p):
    t3 = list(csv.DictReader(open(t3p)))
    cols = {y: sum(int(r[y]) for r in t3) for y in yrsum}
    check(cols == yrsum, f"Table3 columns {cols} != year distribution {yrsum}")
    check(sum(int(r["total"]) for r in t3) == N, "Table3 total != N")

# tex must not contain stale v3 strings
for s in ["threat 31 / defense 65 / both 4", "(n=109)", "core set, n=100", "1 of 35", "14 of 65",
          "35 of its 42", "overtakes deep supervised", "never first", "n=10) and the conference",
          "journal article [T28]", "R5 $\\\\le$0.16", "defense R3 0.25",
          "Other & 10", "Survey $+$ benchmarks & 8",
          "73 defense, 36 threat, and 5 dual", "73 defense/36 threat/5 both",
          "3 (2020), 11 (2021), 9 (2022), 21 (2023), 31 (2024), 35 (2025)",
          "63 journal, 46 conference, 14 preprint", "63 journal/46 conf + 14 preprint",
          "42 papers each", "tied at 42", "Adversarial ML=DeepSup=42",
          "115 records carry", "8 cited-in placeholders", "8 former placeholders",
          "29 of its 42 address RFFI", "18 papers through end-2023",
          "10 threat data-sources unclear", "(72/123 non-unclear sources)", "(71/123 non-unclear sources)",
          "13 of 73 defense", "13/73 defense", "14 of 73 defense",
          "dual attack-plus-defense studies are 5 of 123", "5 of 123 (4.1\\%",
          "Unclear from abstract 30", "Standard split/unclear 34", "Simulation-only 15 (12\\%)",
          "Benchmark/analysis 2 (right panel)",
          "mean R2 0.40", "(mean R2 0.40", "R2 0.40 (lowest realism)",
          "Federated/private learning (5)", "federated privacy (4)", "Federated/privacy FL (4)",
          "Side-channel analysis (3)", "68 papers (55\\%)", "68 of 123 studies",
          "68 of 123 studies", "threat R1 1.67 / R2 1.19", "defense R1 1.15 / R2 1.00",
          "both (n=5) R1 1.80 / R2 0.40", "4.1\\%; 5 of 114 core, 4.4\\%",
          "12 eligible are held", "round-4 backlog", "frozen N=123",
          "companion-paper adjustment", "D20/T20 companions share DOI",
          "D55/T15 share arXiv", "share arXiv ID 2108.13099",
          "no blind $\\\\kappa$ is claimed---single-coder",
          "with 12 papers in 2024 alone", "2024 is adversarial's peak year (12 papers)",
          "overtake in 2024'' is withdrawn", "the tie is an artifact of the 14-paper",
          "after the v4 merge", "corrected in v4", "reported 125 by omitting", "v4 adjudication", "v4 dedupe",
          "v3 mis-keyings", "v3 reported", "v3 tie", "a v2 deletion", "required before journal submission",
          "observed 11.4", "the field's attack arm", "tenth of a point", "to appear", "Ulukus et al.",
          "(D46, INFOCOM 2026)", "round-4 merge", "round-4 coverage", "round-4 backlog", "8 former placeholders",
          "attack arm", "stagnates", "load-bearing", "years behind", "104 seeded", "Ulukus",
          "14 of 30 threat studies", "15 testbed, 15 standard", "37 standard/unclear validations",
          "(45 testbed, 18 sim-only)", "R2 0.57", "1.06 for journals", "1.30; defense", "0.96 / R3",
          "half the family sits", "Sim-heavy; cost-silent", "survives only in traffic", "to appear", "42--42",
          "tenth of a point", "0.07 R2", "cuts both ways",
          "42--42", "125 unique", "R2 0.57", "1.06 for journals", "not improving as output grows",
          "14 OpenAlex included", "63 journal papers", "preprint arm is small (n=14)"]:
    check(s not in tex, f"stale string still in tex: {s!r}")

# no shared identifiers may remain silently double-counted
doi_count = collections.Counter(r["doi_url"].strip() for r in fp.values() if r["id"] in set(x["id"] for x in ds))
dups = {k:v for k,v in doi_count.items() if v>1 and k.startswith("http")}
check(len(dups) == 0, f"shared identifiers remain: {dups}")

# no cited-in placeholders may remain
n_cited = sum(1 for k,v in fp.items() if k in set(x["id"] for x in ds) and v["doi_url"].startswith("cited-in"))
check(n_cited == 0, f"{n_cited} cited-in rows remain")

# every doi_url must be an http(s) identifier (no bare publisher paths without scheme is fine if http)
nonhttp = [(k,v["doi_url"]) for k,v in fp.items() if k in set(x["id"] for x in ds) and not v["doi_url"].startswith("http")]
check(len(nonhttp) == 0, f"non-http identifiers: {nonhttp}")

if errs:
    print("CONSISTENCY FAIL:")
    for e in errs:
        print(" -", e)
    sys.exit(1)
print(f"CONSISTENCY OK: N={N} tracks {dict(trk)} years {dict(sorted(yrs.items()))} cited-in={n_cited} dup-dois={len(dups)}")
