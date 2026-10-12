"""Apply round-2 resolution (9 confirmed publications, 8 rejected hits).

D33/D39/D42/D45/D46/D63/T35/T36 hits REJECTED (wrong/different papers or no
authors); those rows keep confirmed-arXiv-author bib where fetched, venues stay
'unconfirmed' preprint. Run from repo root:
  python3 submission/code/apply_round2.py
"""
import csv
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

# id: (authors, venue, doi_url, venue_type, year)
UPD = {
    "D25": ("Aghdam SR; Amid E; Furdek M; Graell i Amat A", "IEEE CAMAD Workshops",
            "https://doi.org/10.1109/camad52502.2021.9617764", "peer-reviewed", None),
    "D35": ("Hoseini SA; Bouhafs F; Aboutorab N", "IEEE GLOBECOM Workshops",
            "https://doi.org/10.1109/gcwkshps58843.2023.10465104", "peer-reviewed", "2023"),
    "D38": ("Gao N; Han Y; Li N; Jin S; Matthaiou M", "IEEE Wireless Communications",
            "https://doi.org/10.1109/mwc.013.2200538", "peer-reviewed", "2024"),
    "D49": ("Johnson B; Albousayri H; Hamdaoui B", "IEEE Network",
            "https://doi.org/10.1109/mnet.2025.3587300", "peer-reviewed", "2025"),
    "D50": ("Puppo L; Wong W-K; Hamdaoui B", "IEEE ISCC",
            "https://doi.org/10.1109/iscc58397.2023.10217841", "peer-reviewed", None),
    "D53": ("Li Y; Shi Z; Hu H; Fu Y; Wang H; Lei H", "IEEE Communications Letters",
            "https://doi.org/10.1109/lcomm.2024.3452715", "peer-reviewed", None),
    "T09": ("Shi Y; Davaslioglu K; Sagduyu YE", "IEEE Trans Cogn Commun Netw",
            "https://doi.org/10.1109/tccn.2020.3010330", "peer-reviewed", "2021"),
    "T14": ("Shi Y; Sagduyu YE", "IEEE Trans Mobile Computing",
            "https://doi.org/10.1109/tmc.2022.3148690", "peer-reviewed", "2023"),
    "T19": ("Engelberg A; Wool A", "ACM WPES",
            "https://doi.org/10.1145/3559613.3563191", "peer-reviewed", "2022"),
}

CONF_KEYS = ["conf", "workshop", "symposium", "milcom", "globecom", "infocom",
             "mobicom", "wisec", "wiseml", "ndss", "ccs", "icccn", "isncc",
             "ncic", "wcnc", "wcsp", "ismvl", "icassp", "vtc", "icc", "gass",
             "cps-iot", "aiiot", "lnns", "lecture notes", "chapter", "wpes",
             "camad", "iscc"]


def channel(venue_type, venue):
    return "preprint" if venue_type == "preprint" else (
        "conference" if any(k in venue.lower() for k in CONF_KEYS) else "journal")


fp_path = f"{ROOT}/found_papers.csv"
fp = list(csv.DictReader(open(fp_path)))
for r in fp:
    if r["id"] in UPD:
        au, ve, doi, _, _ = UPD[r["id"]]
        r["authors"], r["venue"] = au, ve
        if doi:
            r["doi_url"] = doi
        r["note"] = (r.get("note", "") + " | round2-resolved 2026-10-11").strip(" |")
with open(fp_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fp[0].keys())
    w.writeheader()
    w.writerows(fp)

ds_path = f"{ROOT}/dataset_papers.csv"
ds = list(csv.DictReader(open(ds_path)))
fpf = {r["id"]: r for r in fp}
for r in ds:
    if r["id"] in UPD:
        _, _, _, vt, yr = UPD[r["id"]]
        if vt:
            r["venue_type"] = vt
        if yr:
            r["year"] = yr
    r["venue_channel"] = channel(r["venue_type"], fpf[r["id"]]["venue"])
with open(ds_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ds[0].keys())
    w.writeheader()
    w.writerows(ds)

from collections import Counter
print(Counter(r["venue_type"] for r in ds), Counter(r["venue_channel"] for r in ds))
print("years:", sorted(Counter(r["year"] for r in ds).items()))
weak = [r["id"] for r in ds if fpf[r["id"]]["authors"].strip().startswith("?")
        or "unconfirmed" in fpf[r["id"]]["venue"]]
print(len(weak), "weak remain:", weak)
