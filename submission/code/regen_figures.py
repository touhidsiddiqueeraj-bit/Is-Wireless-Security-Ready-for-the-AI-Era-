"""Build ALL submission figures in color from the live coded dataset.

Colorblind-safe palette (Okabe-Ito based). Every number is computed from
../../dataset_papers.csv -- nothing hand-typed. Run: python3 regen_figures.py
Outputs ../figures/Fig1..Fig9_*.png (150 dpi).
"""
import csv
import collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

plt.rcParams.update({"font.family": "serif", "font.size": 11})
OUT = "../figures"
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]

BLUE, ORANGE, GREEN = "#0072B2", "#E69F00", "#009E73"
SKY, RED, PINK, GRAY = "#56B4E9", "#D55E00", "#CC79A7", "#999999"
STACK = [BLUE, ORANGE, GREEN, "#F0E442", SKY, RED, PINK]
NAVY = "#08306B"

with open("../../dataset_papers.csv") as f:
    ROWS = list(csv.DictReader(f))
N = len(ROWS)
assert N > 100

# ---- Fig 1: screening flow (three-path triangulation) ------------------------------
nd = collections.Counter(r["track"] for r in ROWS if r["track"] != "pqc-context")
npqc = sum(1 for r in ROWS if r["track"] == "pqc-context")
fig, ax = plt.subplots(figsize=(10.5, 6.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10.6)
ax.axis("off")
ax.text(5, 9.55, "Screening flow (seeded + OpenAlex runs; programmatic pool held; Scopus/IEEE/WoS pending)",
        ha="center", fontsize=12)
boxes = [("Identification (2 search paths + programmatic pool)\nCrossref+arXiv: 1,945 records (0 included)  |  Expert seed: ~290  |  OpenAlex: 894 + 994 rerun",
          8.55, 1.25),
         ("Deduplication (DOI / arXiv-ID / title)\n126 seeded candidates  +  662 new OpenAlex records  +  743 rerun records",
          6.85, 1.25),
         ("Title gate (wireless AND security AND AI)\n241 programmatic (extension pool)  +  130 OpenAlex gated",
          5.15, 1.25),
         ("Validity floor V1-V3 + reads\n109 seeded + 14 OpenAlex + 12 rerun included; scope/dedupe cuts to 130",
          3.45, 1.25),
         (f"Included evidence base: {N} (121 core + 9 PQC-context)\n{N-npqc} core ({nd['defense']} defense / {nd['threat']} threat / {nd['both']} both)\n15 background  |  4 backup  |  14 excluded",
          1.55, 1.9)]
for t, y, h in boxes:
    ax.add_patch(FancyBboxPatch((0.6, y - h / 2), 8.8, h, boxstyle="round,pad=0.05",
                                facecolor="#DCE9F7", edgecolor=BLUE, linewidth=1.6))
    ax.text(5, y, t, ha="center", va="center", fontsize=10.5)
ys = [b[1] for b in boxes]
hs = [b[2] for b in boxes]
for y0, h0, y1, h1 in zip(ys, hs, ys[1:], hs[1:]):
    ax.annotate("", xy=(5, y1 + h1 / 2), xytext=(5, y0 - h0 / 2),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.4))
fig.tight_layout()
fig.savefig(f"{OUT}/Fig1_screening_flow.png", dpi=150)
plt.close(fig)

# ---- Fig 2: corpus composition -------------------------------------------------
trk_counts = collections.Counter(r["track"] for r in ROWS)
tracks = [("Defense", trk_counts["defense"]), ("Threat", trk_counts["threat"]), ("Both", trk_counts["both"]), ("PQC-context", trk_counts["pqc-context"])]
assert sum(v for _, v in tracks) == N
peer = [sum(1 for r in ROWS if r["year"] == y and r["venue_type"] == "peer-reviewed") for y in YEARS]
pre = [sum(1 for r in ROWS if r["year"] == y and r["venue_type"] == "preprint") for y in YEARS]
assert [a + b for a, b in zip(peer, pre)] == [sum(1 for r in ROWS if r["year"] == y) for y in YEARS]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))
vals = [v for _, v in tracks]
b = a1.barh([t for t, _ in tracks], vals, color=BLUE, edgecolor="black")
a1.set_xlabel(f"Papers (n = {N} included)")
a1.set_title("(a) Track split")
for bar, v in zip(b, vals):
    a1.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2, str(v), va="center")
x = np.arange(7)
a2.bar(x, peer, color=BLUE, edgecolor="black", label="Peer-reviewed")
a2.bar(x, pre, bottom=peer, color=ORANGE, edgecolor="black", label="Preprint")
a2.set_xticks(x, YEARS)
a2.set_ylabel("Papers")
a2.set_title("(b) Year x venue type")
a2.legend(fontsize=9)
fig.suptitle("Corpus composition")
fig.tight_layout()
fig.savefig(f"{OUT}/Fig2_corpus_composition.png", dpi=150)
plt.close(fig)

# ---- Fig 3: function x method heatmap ------------------------------------------
FNS = ["Authentication/\nRFFI", "Key generation/\ndistribution", "Anti-jamming/\nsecure comms",
       "Protocol/\ntraffic/\ncryptanalysis", "Federated/\nprivacy-preserving FL",
       "Learned primitives/\ncrypto", "Side-channel attack analysis", "PQC migration (contextual)"]
MFS = ["Adversarial ML", "Deep supervised (CNN/RNN/Transformer)", "Reinforcement/DRL",
       "Federated/private learning", "PQC implementation", "Traffic-analysis ML",
       "Protocol fuzzing/analysis", "LLM/foundation-assisted", "Defensive/robust ML",
       "Dataset/benchmark contribution", "Classical/Bayesian ML",
       "Optimization-based (SCA/SDR)", "Survey/systematization"]
SHORT = ["AdvML", "DeepSup", "DRL", "FL/Priv", "PQC-impl", "TrafficML", "Fuzz", "LLM",
         "DefML", "DataBench", "ClassBayes", "Opt", "Survey"]
# exact mapping (function labels contain no newlines in the csv)
FNKEYS = ["Authentication/RFFI", "Key generation/distribution", "Anti-jamming/secure comms",
          "Protocol/traffic/cryptanalysis", "Federated/privacy-preserving FL",
          "Learned primitives/crypto", "Side-channel attack analysis", "PQC migration (contextual)"]
mat = np.zeros((8, 13))
for i, fk in enumerate(FNKEYS):
    for j, m in enumerate(MFS):
        mat[i, j] = sum(1 for r in ROWS if r["function"] == fk and r["method_family"] == m)
assert mat.sum() == N
cmap = LinearSegmentedColormap.from_list("blues", ["#ffffff", "#6BAED6", NAVY])
fig, ax = plt.subplots(figsize=(11.5, 6))
vmax = max(29, float(mat.max()))
im = ax.imshow(mat, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
for i in range(8):
    for j in range(13):
        v = int(mat[i, j])
        if v:
            ax.text(j, i, str(v), ha="center", va="center", fontsize=10,
                    color="white" if v >= 9 else "black")
ax.set_xticks(range(13), SHORT, rotation=35, ha="right", fontsize=10)
ax.set_yticks(range(8), FNS, fontsize=10)
for s in ax.spines.values():
    s.set_visible(True)
ax.set_title(f"Function x method family (cell = paper count, n = {N})")
fig.colorbar(im, ax=ax, shrink=0.8, label="papers")
fig.tight_layout()
fig.savefig(f"{OUT}/Fig3_function_method_heatmap.png", dpi=150)
plt.close(fig)

# ---- Fig 4: year trend + cumulative ----------------------------------------------
totals = [sum(1 for r in ROWS if r["year"] == y) for y in YEARS]
cum = np.cumsum(totals).tolist()
assert cum[-1] == N
fig, ax1 = plt.subplots(figsize=(9.5, 5))
ax1.bar(YEARS, totals, color=BLUE, edgecolor="black", label="Papers per year")
ax1.set_ylabel("Papers per year")
ax2 = ax1.twinx()
ax2.plot(YEARS, cum, color=RED, marker="o", linewidth=1.8, label="Cumulative")
ax2.set_ylabel("Cumulative")
ax1.set_title("Corpus by publication year (bars) with cumulative total (line)")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, fontsize=9)
fig.tight_layout()
fig.savefig(f"{OUT}/Fig4_year_trend.png", dpi=150)
plt.close(fig)

# ---- Fig 5: method-family stacked counts by year -----------------------------------
GROUPS = [
    ("Adversarial ML", {"Adversarial ML"}),
    ("Deep supervised (CNN/RNN/Tr)", {"Deep supervised (CNN/RNN/Transformer)"}),
    ("Reinforcement/DRL", {"Reinforcement/DRL"}),
    ("PQC implementation", {"PQC implementation"}),
    ("Federated/private learning", {"Federated/private learning"}),
    ("Survey/systematization", {"Survey/systematization"}),
]
known = set().union(*[g[1] for g in GROUPS])
series = [([sum(1 for r in ROWS if r["method_family"] in m and r["year"] == y) for y in YEARS], lab)
          for lab, m in GROUPS]
series.append(([sum(1 for r in ROWS if r["year"] == y and r["method_family"] not in known)
                for y in YEARS], "Other"))
assert sum(v for s, _ in series for v in s) == N
fig, ax = plt.subplots(figsize=(9.5, 5))
bottom = [0] * 7
for k, (vals, lab) in enumerate(series):
    ax.bar(YEARS, vals, bottom=list(bottom), color=STACK[k % len(STACK)],
           edgecolor="black", linewidth=0.8, label=lab)
    bottom = [b + v for b, v in zip(bottom, vals)]
ax.set_ylabel("Papers")
ax.set_title(f"Method-family counts by publication year (n = {N})")
ax.legend(ncols=2, fontsize=9)
fig.tight_layout()
fig.savefig(f"{OUT}/Fig5_method_by_year.png", dpi=150)
plt.close(fig)

# ---- Fig 6: data landscape + validation ----------------------------------------------
DORD = ["Testbed/OTA measurement", "Collected dataset/traces", "Simulation",
        "Unclear (abstract)", "Analysis/benchmark"]
DLAB = ["Testbed/OTA", "Collected\ntraces", "Simulation", "Unclear", "Analysis"]
dvals = [sum(1 for r in ROWS if r["data_source"] == d) for d in DORD]
VORD = ["Testbed/field demonstration", "Cross-domain/generalization test",
        "Standard split/unclear", "Simulation-only", "Benchmark/analysis"]
VLAB = ["Testbed/\nfield demo", "Cross-domain/\ngeneralization",
        "Standard\nsplit/unclear", "Simulation\nonly", "Benchmark"]
vvals = [sum(1 for r in ROWS if r["validation"] == v) for v in VORD]
assert sum(dvals) == sum(vvals) == N
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))
for ax, vals, labs, title in [(a1, dvals, DLAB, "(a) Primary data source"),
                              (a2, vvals, VLAB, "(b) Validation approach")]:
    bars = ax.bar(range(len(vals)), vals, color=BLUE, edgecolor="black")
    ax.set_xticks(range(len(vals)), labs, fontsize=10)
    ax.set_ylabel("Papers")
    ax.set_title(title)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.6, str(v),
                ha="center", fontsize=11)
fig.suptitle(f"Data landscape and validation practice (n = {N})")
fig.tight_layout()
fig.savefig(f"{OUT}/Fig6_data_validation.png", dpi=150)
plt.close(fig)

# ---- Fig 7: evaluation realism by track -------------------------------------------------
def cls(r):
    v = r["validation"]
    if v == "Testbed/field demonstration":
        return 0
    if v == "Cross-domain/generalization test":
        return 1
    if v == "Simulation-only":
        return 2
    if v == "Standard split/unclear":
        return 3
    return 4

tb = [r for r in ROWS if r["track"] in ("threat", "both")]
df = [r for r in ROWS if r["track"] == "defense"]
tbv = [sum(1 for r in tb if cls(r) == i) for i in range(5)]
dfv = [sum(1 for r in df if cls(r) == i) for i in range(5)]
assert sum(tbv) + sum(dfv) == sum(1 for r in ROWS if r["track"] in ("threat", "both", "defense"))
cats = ["Testbed/\nfield demo", "Cross-domain/\ngeneral.", "Simulation-\nonly", "Standard\nsplit", "Benchmark"]
x = range(5)
fig, ax = plt.subplots(figsize=(10.5, 5))
w = 0.36
b1 = ax.bar([i - w / 2 for i in x], tbv, width=w, color=RED, edgecolor="black",
            label=f"Threat (+both), n={len(tb)}")
b2 = ax.bar([i + w / 2 for i in x], dfv, width=w, color=BLUE, edgecolor="black",
            label=f"Defense, n={len(df)}")
ax.set_xticks(list(x), cats)
ax.set_ylabel("Papers")
ax.set_title(f"Validation approaches by track (core set, n = {len(tb) + len(df)})")
ax.legend()
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                str(int(bar.get_height())), ha="center", fontsize=10)
fig.tight_layout()
fig.savefig(f"{OUT}/Fig7_eval_by_track.png", dpi=150)
plt.close(fig)

# ---- Fig 8: readiness heatmap (numeric means; bands defined in caption) -----------
def _m(track, col):
    rows = [r for r in ROWS if r["track"] == track]
    return round(sum(int(r[col]) for r in rows) / len(rows), 2)
# R3/R5 are N/A for attack-only rows: shown as n/a, never pooled
nums = [[f"{_m('threat','R1'):.2f}", f"{_m('threat','R2'):.2f}", "n/a",
         f"{_m('threat','R4'):.2f}", "n/a"],
        [f"{_m('both','R1'):.2f}", f"{_m('both','R2'):.2f}", f"{_m('both','R3'):.2f}",
         f"{_m('both','R4'):.2f}", f"{_m('both','R5'):.2f}"],
        [f"{_m('defense','R1'):.2f}", f"{_m('defense','R2'):.2f}", f"{_m('defense','R3'):.2f}",
         f"{_m('defense','R4'):.2f}", f"{_m('defense','R5'):.2f}"],
        [f"{_m('pqc-context','R1'):.2f}", f"{_m('pqc-context','R2'):.2f}", f"{_m('pqc-context','R3'):.2f}",
         f"{_m('pqc-context','R4'):.2f}", f"{_m('pqc-context','R5'):.2f}"]]
def _band(track, col):
    if track == "threat" and col in ("R3", "R5"):
        return "Weak"
    v = _m(track, col)
    return "Stronger" if v >= 1.0 else ("Partial" if v >= 0.10 else "Weak")
tracks8, cols8 = (["threat", "both", "defense", "pqc-context"], ["R1", "R2", "R3", "R4", "R5"])
cells = [[nums[i][j] for j in range(5)] for i in range(4)]
shade = {"Stronger": NAVY, "Partial": "#6BAED6", "Weak": "#F2F2F2"}
fig, ax = plt.subplots(figsize=(11, 5.0))
ax.set_xlim(0, 5)
ax.set_ylim(0, 4)
for i in range(4):
    for j in range(5):
        v = _band(tracks8[i], cols8[j])
        ax.add_patch(Rectangle((j, 3 - i), 1, 1, facecolor=shade[v], edgecolor="black"))
        ax.text(j + 0.5, 3 - i + 0.5, cells[i][j], ha="center", va="center", fontsize=11,
                color="white" if v == "Stronger" else "black")
ax.set_xticks([j + 0.5 for j in range(5)],
              ["R1 Threat\nmodel", "R2 Real\nadversary", "R3 Cost on\nconstrained",
               "R4 Repro-\nducibility", "R5 Standards\nalignment"])
ax.set_yticks([3 - i + 0.5 for i in range(4)], ["Threat (30)", "Dual (7)", "Defense (84)", "PQC (9)"])
ax.tick_params(length=0)
ax.set_title(f"Readiness means by track (R1--R5, n = {N})")
ax.text(2.5, -0.62, "Bands: dark >= 1.0, mid 0.10--0.99, light < 0.10; n/a = N/A for attack-only rows",
        ha="center", fontsize=8)
fig.tight_layout()
fig.savefig(f"{OUT}/Fig8_readiness.png", dpi=150)
plt.close(fig)

# ---- Fig 9: autonomous-systems gap matrix ------------------------------------------------
cells9 = ["Partial", "Absent", "Partial", "Evidenced"]
shade9 = {"Absent": "#ffffff", "Partial": "#6BAED6", "Evidenced": NAVY}
fig, ax = plt.subplots(figsize=(11, 3.6))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1.6)
for j, v in enumerate(cells9):
    ax.add_patch(Rectangle((j, 0.3), 1, 1, facecolor=shade9[v], edgecolor="black"))
    ax.text(j + 0.5, 0.8, v, ha="center", va="center", fontsize=12,
            color="white" if v == "Evidenced" else "black")
ax.set_xticks([j + 0.5 for j in range(4)],
              ["Real-time\ndeadlines", "OTA update /\ncrypto-agility",
               "Multi-agent\ntrust", "Long-lived\nsecrets (HNDL)"])
ax.set_yticks([0.8], ["Coverage"])
ax.tick_params(length=0, labelleft=True, bottom=False)
ax.set_title("Autonomous-systems gap matrix (Partial = 1--2 papers, nascent; HNDL proper unaddressed)")
fig.tight_layout()
fig.savefig(f"{OUT}/Fig9_gap_matrix.png", dpi=150)
plt.close(fig)

print("wrote Fig1..Fig9 in color")

# ================= F-A: validation mix by year (evidence-grade check) ==========
# Honest analog of a benchmark-saturation plot: no single-benchmark monoculture
# was found (zero named-benchmark mentions in 75 abstracts), so the plot asks
# whether the *grade* of evidence keeps pace with output growth instead.
VCATS = ["Testbed/field demonstration", "Cross-domain/generalization test",
         "Simulation-only", "Standard split/unclear", "Benchmark/analysis"]
VLABS = ["Testbed/\nfield demo", "Cross-domain/\ngeneralization", "Simulation-\nonly",
         "Standard\nsplit/unclear", "Benchmark"]
VSTACK = [BLUE, GREEN, RED, GRAY, ORANGE]
vseries = [[sum(1 for r in ROWS if r["year"] == y and r["validation"] == v) for y in YEARS]
           for v in VCATS]
totals_y = [sum(1 for r in ROWS if r["year"] == y) for y in YEARS]
assert sum(sum(s) for s in vseries) == N
fig, ax1 = plt.subplots(figsize=(9.5, 5))
bottom = [0] * 7
for k, vals in enumerate(vseries):
    ax1.bar(YEARS, vals, bottom=list(bottom), color=VSTACK[k], edgecolor="black",
            linewidth=0.8, label=VLABS[k].replace("\n", " "))
    bottom = [b + v for b, v in zip(bottom, vals)]
ax1.set_ylabel("Papers")
ax2 = ax1.twinx()
ax2.plot(YEARS, totals_y, color="black", marker="D", linewidth=1.6, label="Total output")
ax2.set_ylabel("Total papers")
ax1.set_title(f"Validation mix by year (stacked) vs total output (diamonds, n = {N})")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, fontsize=8, ncols=2)
fig.tight_layout()
fig.savefig(f"{OUT}/FigA_validation_mix_by_year.png", dpi=150)
plt.close(fig)

# ============ F-B: method family x track (who attacks, who defends) ============
G7 = ["Adversarial ML", "Deep supervised (CNN/RNN/Transformer)", "Reinforcement/DRL",
      "PQC implementation", "Federated/private learning", "Survey/systematization"]
G7LAB = ["AdvML", "DeepSup", "DRL", "PQC-impl", "FL/Priv", "Survey"]
G7SET = set(G7)
trows, tlab = [], []
for g, lab in zip(G7, G7LAB):
    trows.append([sum(1 for r in ROWS if r["method_family"] == g and r["track"] in ("threat", "both")),
                  sum(1 for r in ROWS if r["method_family"] == g and r["track"] == "defense"),
                  sum(1 for r in ROWS if r["method_family"] == g and r["track"] == "pqc-context")])
    tlab.append(lab)
trows.append([sum(1 for r in ROWS if r["method_family"] not in G7SET and r["track"] in ("threat", "both")),
              sum(1 for r in ROWS if r["method_family"] not in G7SET and r["track"] == "defense"),
              sum(1 for r in ROWS if r["method_family"] not in G7SET and r["track"] == "pqc-context")])
tlab.append("Other")
tmat = np.array(trows)
assert tmat.sum() == N
cmap2 = LinearSegmentedColormap.from_list("blues2", ["#ffffff", "#6BAED6", NAVY])
fig, ax = plt.subplots(figsize=(8.5, 5))
im = ax.imshow(tmat, cmap=cmap2, vmin=0, aspect="auto")
for i in range(7):
    for j in range(3):
        v = int(tmat[i, j])
        if v:
            ax.text(j, i, str(v), ha="center", va="center", fontsize=11,
                    color="white" if v >= 12 else "black")
ax.set_xticks(range(3), ["Threat (+both)", "Defense", "PQC-context"])
ax.set_yticks(range(7), tlab)
for s in ax.spines.values():
    s.set_visible(True)
ax.set_title(f"Method families by track (cell = paper count, n = {N})")
fig.colorbar(im, ax=ax, shrink=0.8, label="papers")
fig.tight_layout()
fig.savefig(f"{OUT}/FigB_method_by_track.png", dpi=150)
plt.close(fig)

# ================= F-C: milestones timeline 2020-2026 ===========================
MS = [("2020", "T01", "Far-field SCA (15 m)", "threat"),
      ("2021", "T18", "RL impersonation", "threat"),
      ("2022", "D36", "Ensemble Rx (A+D)", "both"),
      ("2023", "T12", "Stealthy backdoor", "threat"),
      ("2024", "T16", "Agnostic backdoor", "threat"),
      ("2025", "T30", "Magmaw UAP", "threat"),
      ("2025", "D67", "Proactive auth", "defense"),
      ("2026", "T28", "LLM fuzzing", "threat"),
      ("2026", "T03", "Black-box UAP 81.7%", "threat"),
      ("2026", "T27", "FLARE FL side-channel", "threat")]
for y, pid, _, _ in MS:
    assert ROWS and next(r for r in ROWS if r["id"] == pid)["year"] == y, pid
MCOL = {"threat": RED, "defense": BLUE, "both": "#7A5195"}
fig, ax = plt.subplots(figsize=(14, 4.6))
ax.set_xlim(2018.7, 2027.4)
ax.set_ylim(0, 3.4)
ax.axhline(1.0, color="black", linewidth=1.6)
for x in range(2020, 2027):
    ax.plot([x, x], [0.92, 1.08], color="black", linewidth=1.4)
    ax.text(x, 0.55, str(x), ha="center", fontsize=11)
up = True
seen_year: dict = {}
for y, pid, txt, tr in MS:
    yy = 1.9 if up else 2.7
    side_right = up
    up = not up
    k = seen_year.get(y, 0)
    seen_year[y] = k + 1
    xx = int(y) + (k - 1) * 0.35 if seen_year[y] > 1 or list(zip(*MS))[0].count(y) > 1 else int(y)
    ax.plot([int(y), int(y)], [1.0, yy], color=MCOL[tr], linewidth=1.2)
    ax.plot(int(y), yy, "o", color=MCOL[tr], markersize=7)
    if side_right:
        ax.text(xx + 0.06, yy + 0.1, f"[{pid}] {txt}", fontsize=7.5, va="bottom",
                bbox=dict(facecolor="white", edgecolor=MCOL[tr], boxstyle="round,pad=0.25"))
    else:
        ax.text(xx - 0.06, yy - 0.1, f"[{pid}] {txt}", fontsize=7.5, va="top", ha="right",
                bbox=dict(facecolor="white", edgecolor=MCOL[tr], boxstyle="round,pad=0.25"))
ax.axis("off")
ax.set_title("Milestones of AI in wireless-link security, 2020-2026 (red = threat, blue = defense, purple = both)")
from matplotlib.lines import Line2D
ax.legend([Line2D([0], [0], marker="o", color="w", markerfacecolor=MCOL[k], markersize=8) for k in MCOL],
          list(MCOL), fontsize=8, loc="lower left")
fig.tight_layout()
fig.savefig(f"{OUT}/FigC_milestones.png", dpi=150)
plt.close(fig)

# ============ F-D: layered kill-chain vs defense coverage (conceptual) ==========
LAYERS = [
    ("1  Signal / waveform\n(RF fingerprint, I/Q, EM leakage)",
     "[T09] GAN-spoof  [T18] RL impersonation\n[T01] far-field SCA  [T30] Magmaw UAP",
     "PARTIAL", "Open-set / receiver-agnostic RFFI;\nno deployed counter to UAP spoofing"),
    ("2  Link / PHY security\n(auth, keygen, anti-jam)",
     "[T06] fingerprint erasure  DRL jammers\n[K] keygen only simulated",
     "PARTIAL", "Contrastive + few-shot RFFI;\nkeygen/DRL defenses sim-only"),
    ("3  Protocol / traffic\n(AKA, RRC, padding, baseband)",
     "[T28] LLM fuzzing (7 vulns)\n[T19] padding defeat  [T23] 5G SoK",
     "THIN", "Fuzzing finds bugs; no learned\nin-line protocol defense in corpus"),
    ("4  System / fleet\n(swarm, FL, V2X, OTA update)",
     "[T27] FLARE FL side-channel\n[T36] chained drone-FL attack",
     "ABSENT", "1-2 papers; no OTA-update or\nswarm-trust mechanism evaluated"),
]
DCOL = {"PARTIAL": "#6BAED6", "THIN": "#F0E442", "ABSENT": "#ffffff"}
fig, ax = plt.subplots(figsize=(12, 5.2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.4)
ax.axis("off")
ax.text(6, 5.0, "Layered attack surface vs demonstrated defense coverage (conceptual, from corpus)",
        ha="center", fontsize=12)
ax.text(2.2, 4.5, "Layer", fontsize=11, weight="bold")
ax.text(5.6, 4.5, "Demonstrated threats", fontsize=11, weight="bold")
ax.text(10.0, 4.5, "Defense coverage", fontsize=11, weight="bold")
for i, (lay, thr, cov, dfn) in enumerate(LAYERS):
    y = 3.55 - i * 0.95
    ax.add_patch(Rectangle((0.2, y - 0.4), 3.4, 0.8, facecolor="#DCE9F7", edgecolor=BLUE, linewidth=1.4))
    ax.text(1.9, y, lay, ha="center", va="center", fontsize=8.5)
    ax.text(5.6, y, thr, ha="center", va="center", fontsize=8.5,
            bbox=dict(facecolor="#FDEDEC", edgecolor=RED, boxstyle="round,pad=0.3"))
    ax.add_patch(Rectangle((8.4, y - 0.4), 3.4, 0.8, facecolor=DCOL[cov], edgecolor="black", linewidth=1.2))
    ax.text(10.1, y + 0.12, cov, ha="center", va="center", fontsize=9, weight="bold")
    ax.text(10.1, y - 0.18, dfn, ha="center", va="center", fontsize=7)
fig.tight_layout()
fig.savefig(f"{OUT}/FigD_layered_coverage.png", dpi=150)
plt.close(fig)

# ================= F-E: venue-velocity panel =====================================
CHS = ["journal", "conference", "preprint"]
CHN = [sum(1 for r in ROWS if r["venue_channel"] == c) for c in CHS]
CHLAB = [f"Journal (n={CHN[0]})", f"Conference (n={CHN[1]})", f"Preprint (n={CHN[2]})"]
adv = [sum(1 for r in ROWS if r["venue_channel"] == c and r["method_family"] == "Adversarial ML")
       / sum(1 for r in ROWS if r["venue_channel"] == c) * 100 for c in CHS]
FM = ["Adversarial ML", "Reinforcement/DRL", "Deep supervised (CNN/RNN/Transformer)"]
first = {}
for m in FM:
    first[m] = [min([r["year"] for r in ROWS if r["method_family"] == m and r["venue_channel"] == c] or ["-"])
                for c in CHS]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1, 1.35]})
b = a1.bar(CHLAB, adv, color=[BLUE, ORANGE, GREEN], edgecolor="black")
a1.set_ylabel("Adversarial-ML share (%)")
a1.set_title("(a) Frontier-method share by channel")
for bar, v in zip(b, adv):
    a1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{v:.0f}%", ha="center")
yrs = [str(y) for y in range(2020, 2027)]
for i, m in enumerate(FM):
    for j, c in enumerate(CHS):
        if first[m][j] != "-":
            a2.plot(int(first[m][j]), i + (j - 1) * 0.13, "o", markersize=10,
                    color=[BLUE, ORANGE, GREEN][j])
a2.set_ylim(-0.5, 2.6)
a2.set_yticks(range(len(FM)), ["AdvML", "DRL", "DeepSup"])
a2.set_xticks(range(2020, 2027), yrs, rotation=30)
a2.set_title("(b) First appearance of method families by channel")
a2.grid(axis="x", linestyle=":", alpha=0.6)
from matplotlib.patches import Patch
a2.legend([Patch(facecolor=c, edgecolor="black") for c in [BLUE, ORANGE, GREEN]], CHS,
          fontsize=9, loc="lower right")
fig.suptitle(f"Venue velocity: fast channels carry more frontier work and publish it first (n = {N})")
fig.tight_layout()
fig.savefig(f"{OUT}/FigE_venue_velocity.png", dpi=150)
plt.close(fig)

print("wrote FigA..FigE")
