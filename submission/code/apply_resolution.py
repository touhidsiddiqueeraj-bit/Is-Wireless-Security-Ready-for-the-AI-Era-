"""Apply venue/author resolution to found_papers.csv + dataset_papers.csv.

- Fills confirmed authors/venue/DOI for the 24 weak rows (D42/D45/D46/T35
  hits REJECTED after title/author verification -- see comments).
- Flips venue_type preprint->peer-reviewed where publication confirmed.
- Corrects year to published-version year (D34, T23, T27, P10).
- Adds venue_channel column (journal/conference/preprint) for all 109.
Run from repo root: python3 submission/code/apply_resolution.py
"""
import csv

import os
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

# id: (authors, venue, doi_url, venue_type, year) -- None = leave unchanged
UPD = {
    "D07": ("Shen G; Zhang J; Marshall A; Woods R", "IEEE Trans Mobile Computing",
            "https://doi.org/10.1109/tmc.2023.3340039", None, None),
    "D11": ("Zhang X; Li G; Zhang J; Hu A; Xiao B", "IEEE Internet of Things Journal",
            "https://doi.org/10.1109/jiot.2021.3109272", "peer-reviewed", None),
    "D13": ("Shi Y; Tang J; Wang R; Wen H", "IEEE NCIC",
            "https://doi.org/10.1109/ncic61838.2023.00027", None, None),
    "D15": ("Lv Z; Xiao L; Du Y; Niu G", "IEEE Trans Wireless Commun vol 22(12)",
            "https://doi.org/10.1109/twc.2023.3268082", None, None),
    "D19": ("Amin H; Kaldari J; Mohamed N; Aman W; Al-Kuwari S", "IEEE ISNCC",
            "https://doi.org/10.1109/isncc58260.2023.10323824", "peer-reviewed", None),
    # D25: submitted CAMAD only -- stays preprint, authors filled from arXiv
    "D25": ("Aghdam SR; Amid E; Furdek M; Graell i Amat A",
            "venue unconfirmed (arXiv 2102.10639; submitted IEEE CAMAD)", None, None),
    "D31": ("Ma Z; Fang S; Fan Y", "Sensors",
            "https://doi.org/10.3390/s25175415", None, None),
    "D32": ("Huang Y; Li R; Chen M; Zhao F; Zhang D; Tu W", "IEEE Internet of Things Journal",
            "https://doi.org/10.1109/jiot.2025.3631020", "peer-reviewed", None),
    # D33: arXiv only -- authors filled, stays preprint
    "D33": ("Tyler JH; Fadul MKM; Reising DR", "venue unconfirmed (arXiv 2411.10287)", None, None),
    "D34": ("Abdalla AS; Behfarnia A; Marojevic V", "IEEE WCNC",
            "https://doi.org/10.1109/wcnc51071.2022.9771893", "peer-reviewed", "2022"),
    "D40": ("Guo J; Gao N; Zuo Y; Xu H; Jin S; Wong KK", "IEEE WCSP",
            "https://doi.org/10.1109/wcsp68525.2025.1010537", "peer-reviewed", None),
    # D42: Crossref hit is a DIFFERENT paper (Jia et al.) -- rejected, stays preprint
    "D42": ("Shahiri V; Li G; Behroozi H", "venue unconfirmed (arXiv 2507.00714; under review)", None, None),
    # D45: hit was a 2013 SIU paper -- rejected. D46: hit was WMCS 2021 -- rejected.
    "D45": ("Razak FA; Yilmaz Y", "venue unconfirmed (arXiv 2605.15593)", None, None),
    "D46": ("Zeng S; Shen Y; Zhang Y; Shen Y; Tan Z; Song HH",
            "venue unconfirmed submitted INFOCOM 2026 (arXiv 2608.04881)", None, None),
    "D54": ("Huang S; Zhou Y; Wang T; Shi Y", "IEEE ICC Workshops",
            "https://doi.org/10.1109/iccworkshops50388.2021.9473694", None, None),
    "P04": ("Kim Y; Yoon S; Seo SC", "IEEE Access",
            "https://doi.org/10.1109/access.2024.3435451", None, None),
    "P08": ("Gonzalez de la Torre MA; Morales Sandoval IA; Freitas de Abreu GT",
            "IEEE Access", "https://doi.org/10.1109/access.2025.3560023", "peer-reviewed", None),
    "P10": ("Blanco-Romero J; Garcia-Nino YM; Almenares Mendoza F; Diaz-Sanchez D",
            "Lecture Notes in Networks and Systems (book chapter)",
            "https://doi.org/10.1007/978-3-032-16995-2_30", "peer-reviewed", "2025"),
    "T08": ("Ji Y; Dubrova E; Wang R", "IEEE ISMVL",
            "https://doi.org/10.1109/ismvl64713.2025.00035", None, None),
    "T23": ("Eleftherakis S; Giustiniano D; Kourtellis N", "ACM WiSec",
            "https://doi.org/10.1145/3734477.3734716", "peer-reviewed", "2025"),
    "T27": ("Shuvo MNH; Hossain M; Mallik A; Twigg J; Dagefu F", "IEEE INFOCOM",
            "https://doi.org/10.1109/infocom59046.2026.11571658", "peer-reviewed", "2026"),
    "T34": ("Li C; Xu M; Du Y; Liu L", "ACM MobiCom",
            "https://doi.org/10.1145/3636534.3649367", None, None),
    # T35: hit lacks authors, cannot confirm same paper -- rejected, stays preprint
    "T35": ("Legashev L; Zhigalov A; Parfenov D", "venue unconfirmed (arXiv 2505.00487)", None, None),
    "T40": ("Cao X; Adhikari B; Zhao S; Wu J", "IEEE MILCOM",
            "https://doi.org/10.1109/milcom64451.2025.11309917", None, None),
}

CONF_KEYS = ["conf", "workshop", "symposium", "milcom", "globecom", "infocom",
             "mobicom", "wisec", "wiseml", "ndss", "ccs", "icccn", "isncc",
             "ncic", "wcnc", "wcsp", "ismvl", "icassp", "vtc", "icc", "gass",
             "cps-iot", "aiiot", "lnns", "lecture notes", "chapter"]


def channel(venue_type, venue):
    if venue_type == "preprint":
        return "preprint"
    v = venue.lower()
    if any(k in v for k in CONF_KEYS):
        # guard: 'icc' also matches... only IEEE ICC-style venues are conferences;
        # 'ICC' substring check below is case-sensitive on purpose
        return "conference"
    return "journal"


fp_path = f"{ROOT}/found_papers.csv"
fp = list(csv.DictReader(open(fp_path)))
for r in fp:
    if r["id"] in UPD:
        upd = UPD[r["id"]] + (None,) * (5 - len(UPD[r["id"]]))
        au, ve, doi, _, _ = upd
        r["authors"] = au
        r["venue"] = ve
        if doi:
            r["doi_url"] = doi
        r["note"] = (r.get("note", "") + " | bib-resolved 2026-10-11").strip(" |")
with open(fp_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fp[0].keys())
    w.writeheader()
    w.writerows(fp)

ds_path = f"{ROOT}/dataset_papers.csv"
ds = list(csv.DictReader(open(ds_path)))
for r in ds:
    if r["id"] in UPD:
        upd = UPD[r["id"]] + (None,) * (5 - len(UPD[r["id"]]))
        _, _, _, vt, yr = upd
        if vt:
            r["venue_type"] = vt
        if yr:
            r["year"] = yr
fpf = {r["id"]: r for r in fp}
for r in ds:
    r["venue_channel"] = channel(r["venue_type"], fpf[r["id"]]["venue"])
with open(ds_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ds[0].keys())
    w.writeheader()
    w.writerows(ds)

print("venue_channel distribution:")
from collections import Counter
print(Counter(r["venue_channel"] for r in ds))
print("venue_type:", Counter(r["venue_type"] for r in ds))
print("\nconference rows for review:")
for r in ds:
    if r["venue_channel"] == "conference":
        print(f"  {r['id']} {r['year']} | {fpf[r['id']]['venue'][:70]}")
print("\npreprint rows for review:")
for r in ds:
    if r["venue_channel"] == "preprint":
        print(f"  {r['id']} {r['year']} | {fpf[r['id']]['venue'][:70]}")
