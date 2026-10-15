#!/usr/bin/env python3
"""Regenerate all DATA-DRIVEN manuscript figures (figs 3-12) at FINAL physical size.

Each figure is rendered with figsize width (inches) equal to its docx display
width / 96, so matplotlib point sizes land 1:1 on the A4 page -- no squeeze,
on-page text is exactly the size set here (ticks ~8pt, labels ~9pt, titles ~10pt).
All counts are recomputed from dataset_papers.csv and hard-asserted against the
published values printed in the manuscript before any plotting. DPI 300 for crispness.
"""
import csv
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
fm.fontManager.addfont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "axes.unicode_minus": False,
    "axes.linewidth": 0.8,
})

import pathlib as _pl
ROWS = list(csv.DictReader(open(_pl.Path(__file__).resolve().parent.parent / 'data' /
                                          'dataset_papers.csv', newline='', encoding='utf-8')))
YEARS = [str(y) for y in range(2020, 2027)]
OUT = "/home/z/my-project/scripts/manuscript/figs"
DPI = 300

BLUE, ORANGE, GREEN, RED = "#1f77b4", "#e8a020", "#199e77", "#d62728"

# ---------------- shared corpus aggregates (asserted) ----------------
years_c = Counter(r["year"] for r in ROWS)
YCOUNTS = [years_c[y] for y in YEARS]
assert YCOUNTS == [4, 17, 10, 21, 29, 36, 13], YCOUNTS

track_c = Counter(r["track"] for r in ROWS)
assert (track_c["defense"], track_c["threat"], track_c["both"], track_c["pqc-context"]) == (84, 30, 7, 9)

chan_c = Counter(r["venue_channel"] for r in ROWS)
assert (chan_c["journal"], chan_c["conference"], chan_c["preprint"]) == (65, 46, 19)

MAJOR = [
    "Adversarial ML",
    "Deep supervised (CNN/RNN/Transformer)",
    "Reinforcement/DRL",
    "PQC implementation",
    "Federated/private learning",
    "Survey/systematization",
]
GROUPS = MAJOR + ["Other"]

def grp(fam):
    return fam if fam in MAJOR else "Other"

def tcol(t):
    return "Threat(+both)" if t in ("threat", "both") else ("Defense" if t == "defense" else "PQC-context")

VALS = [
    "Testbed/field demonstration",
    "Cross-domain/generalization test",
    "Simulation-only",
    "Standard split/unclear",
    "Benchmark/analysis",
]

# family x year
fy = defaultdict(Counter)
for r in ROWS:
    fy[grp(r["method_family"])][r["year"]] += 1
# family x track
ft = defaultdict(Counter)
for r in ROWS:
    ft[grp(r["method_family"])][tcol(r["track"])] += 1
# function x family (raw)
ff = defaultdict(Counter)
for r in ROWS:
    ff[r["function"]][r["method_family"]] += 1
FAMS = sorted({r["method_family"] for r in ROWS})
assert [sum(ff[f].get(x, 0) for f in ff) for x in FAMS] == [40, 1, 2, 45, 2, 12, 1, 1, 9, 9, 6, 2]
# validation x track / x year
vt = defaultdict(Counter)
vy = defaultdict(Counter)
for r in ROWS:
    vt[tcol(r["track"])][r["validation"]] += 1
    vy[r["year"]][r["validation"]] += 1
assert [vt["Threat(+both)"][v] for v in VALS] == [17, 4, 2, 13, 1]
assert [vt["Defense"][v] for v in VALS] == [25, 22, 16, 19, 2]
# data source / validation totals
ds_c = Counter(r["data_source"] for r in ROWS)
val_c = Counter(r["validation"] for r in ROWS)
assert [val_c[v] for v in VALS] == [47, 26, 18, 35, 4]
assert [ds_c["Testbed/OTA measurement"], ds_c["Collected dataset/traces"], ds_c["Simulation"],
        ds_c["Unclear (abstract)"], ds_c["Analysis/benchmark"]] == [46, 26, 20, 32, 6]

# ---------------- fig03: corpus composition ----------------
def fig03():
    ych = defaultdict(Counter)
    for r in ROWS:
        ych[r["year"]][r["venue_channel"]] += 1
    peer = [ych[y]["journal"] + ych[y]["conference"] for y in YEARS]
    pre = [ych[y]["preprint"] for y in YEARS]
    assert sum(peer) == 111 and sum(pre) == 19
    assert peer == [4, 15, 9, 18, 26, 34, 5] and pre == [0, 2, 1, 3, 3, 2, 8]

    fig, (axa, axb) = plt.subplots(
        1, 2, figsize=(5.42, 2.27), constrained_layout=True, gridspec_kw={"width_ratios": [1, 1.3]}
    )
    # (a) track split
    labels = ["PQC-context", "Both", "Threat", "Defense"]
    vals = [track_c["pqc-context"], track_c["both"], track_c["threat"], track_c["defense"]]
    bars = axa.barh(labels, vals, color=BLUE, edgecolor="black", linewidth=0.6, height=0.62)
    for b, v in zip(bars, vals):
        axa.text(v + 1.5, b.get_y() + b.get_height() / 2, str(v), va="center", ha="left", fontsize=8)
    axa.set_xlim(0, 97)
    axa.set_xlabel("Papers (n = 130 included)", fontsize=9)
    axa.set_title("(a) Track split", fontsize=10)
    axa.tick_params(labelsize=8.5)
    # (b) year x venue type
    axb.bar(YEARS, peer, color=BLUE, edgecolor="black", linewidth=0.5, width=0.62, label="Peer-reviewed")
    axb.bar(YEARS, pre, bottom=peer, color=ORANGE, edgecolor="black", linewidth=0.5, width=0.62, label="Preprint")
    axb.set_ylabel("Papers", fontsize=9)
    axb.set_title("(b) Year \u00d7 venue type", fontsize=10)
    axb.tick_params(labelsize=7.5)
    axb.legend(loc="upper left", fontsize=7.5, framealpha=0.95)
    axb.grid(True, axis="y", alpha=0.3)
    axb.set_axisbelow(True)
    fig.suptitle("Corpus composition", fontsize=10.5)
    fig.savefig(f"{OUT}/fig03.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig04: per-year bars + cumulative ----------------
def fig04():
    cum, s = [], 0
    for c in YCOUNTS:
        s += c
        cum.append(s)
    assert cum[-1] == 130 and cum == [4, 21, 31, 52, 81, 117, 130]
    fig, ax = plt.subplots(figsize=(4.79, 2.24), constrained_layout=True)
    bars = ax.bar(YEARS, YCOUNTS, color=BLUE, edgecolor="black", linewidth=0.6, width=0.62, label="Papers per year")
    for b, v in zip(bars, YCOUNTS):
        ax.text(b.get_x() + b.get_width() / 2, v + 3, str(v), ha="center", va="bottom", fontsize=7.5,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85), zorder=5)
    ax.plot(YEARS, cum, color=RED, marker="D", markersize=3.8, linewidth=1.5, label="Cumulative total", zorder=4)
    ax.set_ylabel("Papers", fontsize=9)
    ax.set_ylim(0, 148)
    ax.tick_params(labelsize=8.5)
    ax.grid(True, axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.95)
    fig.savefig(f"{OUT}/fig04.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig05: method-family stacks by year ----------------
def fig05():
    # published invariants
    adv = [fy["Adversarial ML"][y] for y in YEARS]
    deep = [fy["Deep supervised (CNN/RNN/Transformer)"][y] for y in YEARS]
    assert adv == [1, 4, 3, 7, 10, 11, 4] and deep == [2, 6, 4, 9, 10, 11, 3]
    assert sum(adv) == 40 and sum(deep) == 45
    for i in range(4):
        assert deep[i] > adv[i], (i, deep[i], adv[i])   # deep leads through 2023
    assert adv[4] == deep[4] == 10 and adv[5] == deep[5] == 11
    assert adv[6] == 4 and deep[6] == 3                  # 2026: 3-4 deep-vs-adv -> adv 4, deep 3
    colors = ["#1f77b4", "#f5a623", "#19a177", "#ede24a", "#64a8dc", "#d95f02", "#e080c8"]
    legend_labels = [
        "Adversarial ML", "Deep supervised", "Reinforcement/DRL",
        "PQC implementation", "Federated/private", "Survey/system.", "Other",
    ]
    fig, ax = plt.subplots(figsize=(4.90, 2.58), constrained_layout=True)
    bottom = [0] * 7
    for g, c, lab in zip(GROUPS, colors, legend_labels):
        vals = [fy[g][y] for y in YEARS]
        ax.bar(YEARS, vals, bottom=bottom, color=c, edgecolor="black", linewidth=0.4, width=0.62, label=lab)
        bottom = [b + v for b, v in zip(bottom, vals)]
    assert bottom == YCOUNTS
    ax.set_ylabel("Papers", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="upper left", fontsize=6.8, ncol=2, framealpha=0.95, handlelength=1.2, columnspacing=0.9)
    ax.set_ylim(0, 40)
    fig.savefig(f"{OUT}/fig05.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig06: family-group x track heatmap ----------------
def fig06():
    M = [[ft[g][c] for c in ("Threat(+both)", "Defense", "PQC-context")] for g in GROUPS]
    assert M == [
        [27, 13, 0], [3, 42, 0], [0, 9, 0], [0, 0, 9],
        [1, 11, 0], [2, 4, 0], [4, 5, 0],
    ], M
    row_labels = ["AdvML", "DeepSup", "DRL", "PQC-impl", "FL/Priv", "Survey", "Other"]
    col_labels = ["Threat (+both)", "Defense", "PQC-context"]
    fig, ax = plt.subplots(figsize=(4.58, 2.69), constrained_layout=True)
    im = ax.imshow(M, cmap="Blues", vmin=0, vmax=45, aspect="auto")
    for i in range(len(M)):
        for j in range(3):
            v = M[i][j]
            if v:
                ax.text(j, i, str(v), ha="center", va="center", fontsize=8.5,
                        color="white" if v >= 25 else "black")
    ax.set_xticks(range(3))
    ax.set_xticklabels(col_labels, fontsize=9)
    ax.set_yticks(range(len(M)))
    ax.set_yticklabels(row_labels, fontsize=8.5)
    ax.set_title("Method families by track (cell = paper count, n = 130)", fontsize=10)
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.ax.tick_params(labelsize=7.5)
    fig.savefig(f"{OUT}/fig06.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig07: function x family heatmap (12 CSV families) ----------------
def fig07():
    M = [[ff[f].get(x, 0) for x in FAMS] for f in sorted(ff)]
    row_labels = [
        "Anti-jamming/\nsecure comms",
        "Authentication/\nRFFI",
        "Federated/privacy-\npreserving FL",
        "Key generation/\ndistribution",
        "Learned primitives/\ncrypto",
        "PQC migration\n(contextual)",
        "Protocol/traffic/\ncryptanalysis",
        "Side-channel\nattack analysis",
    ]
    col_labels = ["AdvML", "DeepSup", "DRL", "FL/\nPriv", "PQC-\nimpl", "TrafficML",
                  "LLM", "DefML", "DataBench", "ClassBayes", "Opt", "Survey"]
    assert sum(sum(r) for r in M) == 130
    assert [sum(r) for r in M] == [14, 69, 11, 12, 3, 9, 10, 2]
    fig, ax = plt.subplots(figsize=(5.21, 2.72), constrained_layout=True)
    im = ax.imshow(M, cmap="Blues", vmin=0, vmax=34, aspect="auto")
    for i in range(len(M)):
        for j in range(len(FAMS)):
            v = M[i][j]
            if v:
                ax.text(j, i, str(v), ha="center", va="center", fontsize=7.5,
                        color="white" if v >= 20 else "black")
    ax.set_xticks(range(len(FAMS)))
    ax.set_xticklabels(col_labels, fontsize=6.8, rotation=50, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(M)))
    ax.set_yticklabels(row_labels, fontsize=7.5)
    ax.set_title("Function \u00d7 method family (cell = paper count, n = 130)", fontsize=10)
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.ax.tick_params(labelsize=7.5)
    cb.set_label("papers", fontsize=8)
    fig.savefig(f"{OUT}/fig07.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig08: data source + validation horizontal bars ----------------
def fig08():
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(5.42, 1.99), constrained_layout=True)
    ds_labels = ["Testbed/OTA\nmeasurement", "Collected\ndatasets/traces", "Simulation",
                 "Unclear\n(abstract)", "Analysis/\nbenchmark"]
    ds_vals = [ds_c["Testbed/OTA measurement"], ds_c["Collected dataset/traces"],
               ds_c["Simulation"], ds_c["Unclear (abstract)"], ds_c["Analysis/benchmark"]]
    bars = axa.barh(ds_labels[::-1], ds_vals[::-1], color=BLUE, edgecolor="black", linewidth=0.6, height=0.62)
    for b, v in zip(bars, ds_vals[::-1]):
        axa.text(v + 1.2, b.get_y() + b.get_height() / 2, str(v), va="center", ha="left", fontsize=8)
    axa.set_xlim(0, 56)
    axa.set_xlabel("Papers", fontsize=9)
    axa.set_title("(a) Primary data source", fontsize=10)
    axa.tick_params(labelsize=8)
    val_labels = ["Testbed/field\ndemonstration", "Cross-domain/\ngeneralization test",
                  "Simulation-only", "Standard split/\nunclear", "Benchmark/\nanalysis"]
    val_vals = [val_c[v] for v in VALS]
    bars = axb.barh(val_labels[::-1], val_vals[::-1], color=BLUE, edgecolor="black", linewidth=0.6, height=0.62)
    for b, v in zip(bars, val_vals[::-1]):
        axb.text(v + 1.2, b.get_y() + b.get_height() / 2, str(v), va="center", ha="left", fontsize=8)
    axb.set_xlim(0, 56)
    axb.set_xlabel("Papers", fontsize=9)
    axb.set_title("(b) Validation approach", fontsize=10)
    axb.tick_params(labelsize=8)
    fig.suptitle("Data landscape and validation practice (n = 130)", fontsize=10.5)
    fig.savefig(f"{OUT}/fig08.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig09: validation by track grouped bars ----------------
def fig09():
    tb = [vt["Threat(+both)"][v] for v in VALS]
    de = [vt["Defense"][v] for v in VALS]
    assert tb == [17, 4, 2, 13, 1] and de == [25, 22, 16, 19, 2]
    cats = ["Testbed/\nfield demo", "Cross-domain/\ngeneral.", "Simulation-\nonly",
            "Standard\nsplit", "Benchmark"]
    xpos = range(len(VALS))
    w = 0.38
    fig, ax = plt.subplots(figsize=(4.90, 2.33), constrained_layout=True)
    b1 = ax.bar([x - w / 2 for x in xpos], tb, width=w, color="#d95f02", edgecolor="black",
                linewidth=0.5, label="Threat (+both), n=37")
    b2 = ax.bar([x + w / 2 for x in xpos], de, width=w, color=BLUE, edgecolor="black",
                linewidth=0.5, label="Defense, n=84")
    for bars in (b1, b2):
        for b in bars:
            v = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, v + 0.5, str(v), ha="center", va="bottom", fontsize=7.5)
    ax.set_xticks(list(xpos))
    ax.set_xticklabels(cats, fontsize=8.5)
    ax.set_ylabel("Papers", fontsize=9)
    ax.set_ylim(0, 28)
    ax.tick_params(labelsize=8.5)
    ax.legend(loc="upper right", fontsize=8, framealpha=0.95)
    ax.grid(True, axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_title("Validation approaches by track (core set, n = 121)", fontsize=10)
    fig.savefig(f"{OUT}/fig09.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig10: readiness means banded heatmap ----------------
def fig10():
    def mean(track, field):
        vals = [float(r[field]) for r in ROWS if r["track"] == track]
        return sum(vals) / len(vals)

    tracks = [("Threat (30)", "threat"), ("Dual (7)", "both"), ("Defense (84)", "defense"), ("PQC (9)", "pqc-context")]
    fields = ["R1", "R2", "R3", "R4", "R5"]
    col_labels = ["R1 Threat\nmodel", "R2 Real\nadversary", "R3 Cost on\nconstrained", "R4 Repro-\nducibility", "R5 Standards\nalignment"]
    M = [[mean(tk, f) for f in fields] for _, tk in tracks]
    assert abs(M[0][0] - 1.70) < 0.005 and abs(M[0][1] - 1.53) < 0.005
    assert abs(M[0][2] - 0.20) < 0.005 and abs(M[0][4] - 0.17) < 0.005
    assert abs(M[1][0] - 1.86) < 0.005 and abs(M[1][1] - 1.14) < 0.005
    assert abs(M[2][0] - 1.14) < 0.005 and abs(M[2][1] - 1.27) < 0.005
    assert abs(M[3][2] - 1.11) < 0.005 and abs(M[3][4] - 0.56) < 0.005

    DARK, MID, LIGHT = "#084594", "#6baed6", "#f0f0f0"
    def band(v):
        return DARK if v >= 1.0 else (MID if v >= 0.10 else LIGHT)

    fig, ax = plt.subplots(figsize=(4.90, 2.34), constrained_layout=True)
    for i, row in enumerate(M):
        for j, v in enumerate(row):
            c = band(v)
            ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=c, edgecolor="black", linewidth=1.0))
            ax.text(j + 0.5, i + 0.5, f"{v:.2f}", ha="center", va="center", fontsize=9,
                    color="white" if c == DARK else "black")
    ax.set_xlim(0, 5)
    ax.set_ylim(4, 0)
    ax.set_xticks([j + 0.5 for j in range(5)])
    ax.set_xticklabels(col_labels, fontsize=8)
    ax.set_yticks([i + 0.5 for i in range(4)])
    ax.set_yticklabels([t for t, _ in tracks], fontsize=8.5)
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Readiness means by track (R1\u2013R5, n = 130)", fontsize=10, pad=40)
    ax.set_xlabel("Bands: dark \u2265 1.0, mid 0.10\u20130.99, light < 0.10.\nValues from the released dataset (attack-row R3/R5 signals included)",
                  fontsize=6.3, labelpad=3)
    fig.savefig(f"{OUT}/fig10.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig11: validation mix by year + total line ----------------
def fig11():
    stacks = [[vy[y][v] for y in YEARS] for v in VALS]
    assert [sum(s) for s in stacks] == [47, 26, 18, 35, 4]
    assert [sum(vy[y].values()) for y in YEARS] == YCOUNTS
    colors = [BLUE, GREEN, "#d95f02", "#8c8c8c", "#e8a020"]
    legend_labels = ["Testbed/field demo", "Cross-domain general.",
                     "Simulation-only", "Standard split/unclear", "Benchmark", "Total output"]
    fig, ax = plt.subplots(figsize=(4.90, 2.58), constrained_layout=True)
    bottom = [0] * 7
    for stack, c, lab in zip(stacks, colors, legend_labels[:5]):
        ax.bar(YEARS, stack, bottom=bottom, color=c, edgecolor="black", linewidth=0.4, width=0.62, label=lab)
        bottom = [b + v for b, v in zip(bottom, stack)]
    assert bottom == YCOUNTS
    ax.plot(YEARS, YCOUNTS, color="black", marker="D", markersize=4, linewidth=1.5, label=legend_labels[5])
    ax.set_ylabel("Papers", fontsize=9)
    ax.tick_params(labelsize=8.5)
    ax.set_ylim(0, 41)
    ax.legend(loc="upper left", fontsize=6.8, ncol=2, framealpha=0.95, handlelength=1.2, columnspacing=0.9)
    fig.savefig(f"{OUT}/fig11.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig12: venue velocity ----------------
def fig12():
    tot = Counter(r["venue_channel"] for r in ROWS)
    adv = Counter(r["venue_channel"] for r in ROWS if r["method_family"] == "Adversarial ML")
    chan_order = [("Journal", "journal"), ("Conference", "conference"), ("Preprint", "preprint")]
    shares = [100 * adv[c] / tot[c] for _, c in chan_order]
    assert shares == [100 * 20 / 65, 100 * 13 / 46, 100 * 7 / 19], shares

    first = defaultdict(dict)
    for r in ROWS:
        fam, ch = r["method_family"], r["venue_channel"]
        try:
            yf = int(r["year_first"])
        except (ValueError, TypeError):
            yf = int(r["year"])
        if ch not in first[fam] or yf < first[fam][ch]:
            first[fam][ch] = yf
    expected = {
        "Deep supervised (CNN/RNN/Transformer)": {"journal": 2020, "conference": 2020, "preprint": 2023},
        "Adversarial ML": {"journal": 2021, "conference": 2020, "preprint": 2022},
        "Reinforcement/DRL": {"journal": 2023, "conference": 2022},
        "PQC implementation": {"journal": 2020, "conference": 2025, "preprint": 2026},
    }
    for fam, exp in expected.items():
        assert dict(first[fam]) == exp, (fam, dict(first[fam]))

    FAMS12 = list(expected.keys())
    FAM_LABELS = ["Deep\nsupervised", "Adversarial\nML", "Reinforcement\n/DRL", "PQC\nimplementation"]
    CHANNELS = [("journal", "journal", BLUE, "o", +0.20), ("conference", "conference", ORANGE, "s", 0.0),
                ("preprint", "preprint", GREEN, "D", -0.20)]

    fig, (axa, axb) = plt.subplots(1, 2, figsize=(5.10, 2.55), constrained_layout=True,
                                   gridspec_kw={"width_ratios": [1, 1.25]})
    bars = axa.bar([l for l, _ in chan_order], shares, color=[BLUE, ORANGE, GREEN],
                   edgecolor="black", linewidth=0.6, width=0.62)
    for b, v, (_, c) in zip(bars, shares, chan_order):
        axa.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.0f}%\n({adv[c]}/{tot[c]})",
                 ha="center", va="bottom", fontsize=7.5)
    axa.set_ylabel("Adversarial-ML share (%)", fontsize=9)
    axa.set_title("(a) Frontier-method share by channel", fontsize=9.5)
    axa.set_ylim(0, 48)
    axa.tick_params(labelsize=7.5)
    axa.grid(True, axis="y", alpha=0.3)
    axa.set_axisbelow(True)

    for i, (fam, label) in enumerate(zip(FAMS12, FAM_LABELS)):
        y = len(FAMS12) - 1 - i
        for key, cname, color, marker, dy in CHANNELS:
            if key in first[fam]:
                axb.scatter(first[fam][key], y + dy, s=46, color=color, marker=marker,
                            edgecolor="black", linewidth=0.5, zorder=3, label=cname if y == 3 else None)
    axb.set_yticks(range(len(FAMS12)))
    axb.set_yticklabels(FAM_LABELS[::-1], fontsize=8)
    axb.set_xticks(range(2020, 2027))
    axb.set_xlim(2019.6, 2026.4)
    axb.set_ylim(-0.6, 3.6)
    axb.set_xlabel("First appearance (year-first coding)", fontsize=8.5)
    axb.set_title("(b) First appearance by channel", fontsize=9.5)
    axb.tick_params(labelsize=7)
    axb.grid(True, axis="x", alpha=0.3)
    axb.set_axisbelow(True)
    axb.legend(loc="lower right", fontsize=7.5, framealpha=0.95, handletextpad=0.3, borderpad=0.5)
    fig.suptitle("Venue velocity: fast channels carry frontier work first (n = 130)", fontsize=9.5)
    fig.savefig(f"{OUT}/fig12.png", dpi=DPI)
    plt.close(fig)

if __name__ == "__main__":
    fig03()
    print("fig03 ok")
    fig04()
    print("fig04 ok")
    fig05()
    print("fig05 ok")
    fig06()
    print("fig06 ok")
    fig07()
    print("fig07 ok")
    fig08()
    print("fig08 ok")
    fig09()
    print("fig09 ok")
    fig10()
    print("fig10 ok")
    fig11()
    print("fig11 ok")
    fig12()
    print("fig12 ok")
    print("ALL DATA FIGURES REGENERATED")
