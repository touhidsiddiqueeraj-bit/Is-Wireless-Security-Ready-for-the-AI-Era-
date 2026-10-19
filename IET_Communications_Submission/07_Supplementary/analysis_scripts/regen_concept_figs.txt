#!/usr/bin/env python3
"""Regenerate CONCEPT manuscript figures (figs 1, 2, 13, 14) at FINAL physical size.

Same principle as regen_data_figs.py: figsize width = docx display width / 96,
so point sizes land 1:1 on the page. Content matches the published figures
exactly (Fig 1 milestones anchored to the dataset years; the 2025/2026 cluster
matches dataset_papers.csv exactly).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
fm.fontManager.addfont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "axes.unicode_minus": False,
})

OUT = "/home/z/my-project/scripts/manuscript/figs"
DPI = 300
BLUE, RED, PURPLE = "#1f77b4", "#d62728", "#9467bd"
BOXFILL, BOXEDGE = "#d6e6f5", "#2b6cb0"

# ---------------- fig01: milestone timeline ----------------
def fig01():
    # (year, level, color, label, ha, dx_label)
    milestones = [
        (2020, 0.46, RED,    "[T01] Far-field SCA (15 m)", "center", 0.0),
        (2021, 0.88, RED,    "[T18] RL impersonation", "center", 0.0),
        (2022, 0.52, PURPLE, "[D36] Ensemble Rx (A+D)", "center", 0.0),
        (2023, 0.88, RED,    "[T12] Stealthy backdoor", "center", 0.0),
        (2024, 0.55, RED,    "[T16] Agnostic backdoor", "center", 0.0),
        (2025, 0.72, RED,    "[T30] Magmaw UAP", "center", 0.0),
        (2025, 0.30, BLUE,   "[D67] Proactive auth", "right", -0.08),
        (2026, 0.95, RED,    "[T27] FLARE\nFL side-channel", "center", 0.0),
        (2026, 0.50, RED,    "[T03] Black-box\nUAP 81.7%", "center", 0.0),
        (2026, 0.22, RED,    "[T28] LLM baseband\nfuzzing", "center", 0.0),
    ]
    fig, ax = plt.subplots(figsize=(5.78, 1.90), constrained_layout=True)
    ax.set_xlim(2019.55, 2026.55)
    ax.set_ylim(0, 1.34)
    ax.axhline(0, color="black", linewidth=1.1)
    for yr, lev, c, lab, ha, dx in milestones:
        ax.plot([yr, yr], [0, lev], color=c, linewidth=1.3, zorder=2)
        ax.scatter([yr], [lev], s=26, color=c, edgecolor="black", linewidth=0.4, zorder=3)
        ax.text(yr + dx, lev + 0.045, lab, ha=ha, va="bottom", fontsize=7, color="black", zorder=4,
                linespacing=1.05)
    for yr in range(2020, 2027):
        ax.plot([yr, yr], [-0.045, 0], color="black", linewidth=1.1)
        ax.text(yr, -0.10, str(yr), ha="center", va="top", fontsize=8.5)
    ax.axis("off")
    handles = [
        plt.Line2D([], [], marker="o", linestyle="", color=RED, markersize=5, label="threat"),
        plt.Line2D([], [], marker="o", linestyle="", color=BLUE, markersize=5, label="defense"),
        plt.Line2D([], [], marker="o", linestyle="", color=PURPLE, markersize=5, label="both"),
    ]
    ax.legend(handles=handles, loc="lower left", fontsize=6.5, frameon=True, framealpha=0.95,
              handletextpad=0.3, borderpad=0.3, bbox_to_anchor=(0.0, -0.02))
    ax.set_title("Milestones of AI in wireless-link security, 2020\u20132026", fontsize=9.5, pad=4)
    fig.savefig(f"{OUT}/fig01.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig02: screening flow ----------------
def _box(ax, x, y, w, h, lines, sizes):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
                                facecolor=BOXFILL, edgecolor=BOXEDGE, linewidth=1.1))
    n = len(lines)
    for i, (txt, bold) in enumerate(lines):
        dy = (i + 1) / (n + 1)
        ax.text(x + w / 2, y + h * (1 - dy), txt, ha="center", va="center",
                fontsize=sizes[i], fontweight="bold" if bold else "normal")

def fig02():
    fig, ax = plt.subplots(figsize=(4.48, 2.82))
    ax.set_position([0.002, 0.002, 0.996, 0.90])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Screening flow (seeded + OpenAlex runs; programmatic pool held;\nScopus/IEEE/WoS pending)",
                 fontsize=7.8, pad=2)
    bw, bx = 0.90, 0.05
    bh = 0.154
    boxes = [
        (0.97,  [("Identification (2 search paths + programmatic pool)", True),
                 ("Crossref+arXiv 1,945 (0 incl.) \u00b7 seed ~290 \u00b7 OpenAlex 894 + 994 rerun", False)]),
        (0.784, [("Deduplication (DOI / arXiv-ID / title)", True),
                 ("126 seeded candidates + 662 new OpenAlex records + 743 rerun records", False)]),
        (0.598, [("Title gate (wireless AND security AND AI)", True),
                 ("241 programmatic (extension pool)  +  130 OpenAlex gated", False)]),
        (0.412, [("Validity floor V1\u2013V3 + reads", True),
                 ("109 seeded + 14 OpenAlex + 12 rerun included; scope/dedupe cuts to 130", False)]),
        (0.226, [("Included evidence base: 130 (121 core + 9 PQC-context)", True),
                 ("121 core (84 def, 30 thr, 7 both); 15 bg | 4 backup | 14 excluded", False)]),
    ]
    for ytop, lines in boxes:
        y = ytop - bh
        sizes = [8.2 if b else 7.4 for _, b in lines]
        _box(ax, bx, y, bw, bh, lines, sizes)
    for i in range(len(boxes) - 1):
        y_from = boxes[i][0] - bh
        y_to = boxes[i + 1][0]
        ax.add_patch(FancyArrowPatch((0.5, y_from - 0.004), (0.5, y_to + 0.004),
                                     arrowstyle="-|>", mutation_scale=9,
                                     color="black", linewidth=1.0))
    fig.savefig(f"{OUT}/fig02.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig13: layered attack surface ----------------
def fig13():
    fig, ax = plt.subplots(figsize=(5.21, 2.26))
    ax.set_position([0.002, 0.002, 0.996, 0.94])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Layered attack surface vs demonstrated defense coverage (conceptual, from corpus)",
                 fontsize=8.6, pad=2)
    # column ranges
    lx, lw = 0.015, 0.265     # layer
    tx, tw = 0.315, 0.34      # threats
    cx, cw = 0.690, 0.305     # coverage
    # headers
    for x, w, t in [(lx, lw, "Layer"), (tx, tw, "Demonstrated threats"), (cx, cw, "Defense coverage")]:
        ax.text(x + w / 2, 0.945, t, ha="center", va="center", fontsize=8.4, fontweight="bold")
    rows = [
        dict(y=0.79, layer=("1  Signal / waveform\n(RF fingerprint,\nI/Q, EM leakage)"),
             threats=("[T09] GAN-spoof [T18] RL impersonation\n[T01] far-field SCA [T30] Magmaw UAP"),
             status="PARTIAL", fill="#7fb8dd", tcol="black",
             detail="Open-set / receiver-agnostic RFFI;\nno deployed counter to UAP spoofing"),
        dict(y=0.585, layer=("2  Link / PHY security\n(auth, keygen,\nanti-jam)"),
             threats=("[T06] fingerprint erasure DRL jammers\n[K] keygen only simulated"),
             status="PARTIAL", fill="#7fb8dd", tcol="black",
             detail="Contrastive + few-shot RFFI;\nkeygen/DRL defenses sim-only"),
        dict(y=0.38, layer=("3  Protocol / traffic\n(AKA, RRC, padding,\nbaseband)"),
             threats=("[T28] LLM fuzzing (7 vulns)\n[T19] padding defeat [T23] 5G SoK"),
             status="THIN", fill="#f0e442", tcol="black",
             detail="Fuzzing finds bugs; no learned\nin-line protocol defense in corpus"),
        dict(y=0.175, layer=("4  System / fleet\n(swarm, FL, V2X,\nOTA update)"),
             threats=("[T27] FLARE FL side-channel\n[T36] chained drone-FL attack"),
             status="ABSENT", fill="white", tcol="black",
             detail="1\u20132 papers; no OTA-update or\nswarm-trust mechanism evaluated"),
    ]
    bh = 0.19
    for r in rows:
        y = r["y"]
        ax.add_patch(FancyBboxPatch((lx, y - bh / 2), lw, bh, boxstyle="round,pad=0.008,rounding_size=0.015",
                                    facecolor=BOXFILL, edgecolor=BOXEDGE, linewidth=1.0))
        ax.text(lx + lw / 2, y, r["layer"], ha="center", va="center", fontsize=7.0, linespacing=1.25)
        ax.add_patch(FancyBboxPatch((tx, y - bh / 2), tw, bh, boxstyle="round,pad=0.008,rounding_size=0.015",
                                    facecolor="#fdeeee", edgecolor="#c0504d", linewidth=1.0))
        ax.text(tx + tw / 2, y, r["threats"], ha="center", va="center", fontsize=6.2, linespacing=1.35)
        ax.add_patch(FancyBboxPatch((cx, y - bh / 2), cw, bh, boxstyle="round,pad=0.008,rounding_size=0.015",
                                    facecolor=r["fill"], edgecolor="black", linewidth=1.0))
        ax.text(cx + cw / 2, y + 0.048, r["status"], ha="center", va="center",
                fontsize=7.4, fontweight="bold", color=r["tcol"])
        ax.text(cx + cw / 2, y - 0.035, r["detail"], ha="center", va="center", fontsize=6.0, linespacing=1.3)
    fig.savefig(f"{OUT}/fig13.png", dpi=DPI)
    plt.close(fig)

# ---------------- fig14: autonomous-systems gap matrix ----------------
def fig14():
    fig, ax = plt.subplots(figsize=(5.21, 1.71))
    ax.set_position([0.002, 0.002, 0.996, 0.94])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Autonomous-systems gap matrix (Partial = 1\u20132 papers; HNDL proper unaddressed)",
                 fontsize=8.4, pad=2)
    ax.text(0.012, 0.52, "Coverage", ha="left", va="center", fontsize=8.5, rotation=90)
    cells = [
        ("Partial", "#74a9cf", "black", "Real-time\ndeadlines"),
        ("Absent", "white", "black", "OTA update /\ncrypto-agility"),
        ("Partial", "#74a9cf", "black", "Multi-agent\ntrust"),
        ("Evidenced", "#08306b", "white", "Long-lived\nsecrets (HNDL)"),
    ]
    x0, x1 = 0.075, 0.985
    w = (x1 - x0) / 4
    y0, y1 = 0.30, 0.86
    for i, (lab, fill, tcol, xlab) in enumerate(cells):
        x = x0 + i * w
        ax.add_patch(plt.Rectangle((x, y0), w, y1 - y0, facecolor=fill, edgecolor="black", linewidth=1.0))
        ax.text(x + w / 2, (y0 + y1) / 2, lab, ha="center", va="center", fontsize=9.5, color=tcol)
        ax.text(x + w / 2, y0 - 0.05, xlab, ha="center", va="top", fontsize=8.5, linespacing=1.15)
    fig.savefig(f"{OUT}/fig14.png", dpi=DPI)
    plt.close(fig)

if __name__ == "__main__":
    fig01()
    print("fig01 ok")
    fig02()
    print("fig02 ok")
    fig13()
    print("fig13 ok")
    fig14()
    print("fig14 ok")
    print("ALL CONCEPT FIGURES REGENERATED")
