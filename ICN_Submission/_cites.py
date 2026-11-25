#!/usr/bin/env python3
"""Convert corpus IDs to numbered citations and emit the reference list.

Corpus IDs (D01, T03, ...) are the dataset keys used in the working notes. A
journal needs numbered references in order of first citation, so this script
assigns numbers by first appearance and builds \bibitem entries from
found_papers.csv. The ID is kept in the released dataset only.
"""
import csv, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUB = pathlib.Path(__file__).resolve().parent
BODY = SUB / "_body3.tex"

ID = re.compile(r"\[?(?<![A-Za-z])(BG\d{1,2}|[DTPQ]\d{2})(?![0-9])\]?")

papers = {r["id"]: r for r in csv.DictReader(open(ROOT / "found_papers.csv"))}

# the working notes label background surveys BG2/BG3/BG7; the dataset uses B02/B03/B07
ALIAS = {"BG%d" % i: "B%02d" % i for i in range(1, 10)}


def resolve(pid):
    return ALIAS.get(pid, pid)


INI = re.compile(r"^[A-Z][A-Z.\-]*$")


def _ini(tok):
    """'C-H' -> 'C.-H.';  'Y-WP' -> 'Y.-W. P.';  'Kwok-Yan' -> 'K.-Y.'"""
    groups = []
    for part in tok.split("-"):
        letters = [c.upper() for c in part if c.isalpha()]
        if letters:
            groups.append(". ".join(letters) + ".")
    return "-".join(groups)


def _first(tok):
    """Given names contribute one initial per hyphenated part: 'Kwok-Yan' -> 'K.-Y.'"""
    groups = [p for p in tok.split("-") if p and p[0].isalpha()]
    return "-".join(p[0].upper() + "." for p in groups)


def fmt_name(tok):
    tok = tok.strip().rstrip(",")
    parts = tok.split()
    if len(parts) == 1:
        return tok                      # surname only, as recorded
    last = parts[-1]
    if INI.match(last) and len(last.replace("-", "").replace(".", "")) <= 4:
        return _ini(last) + " " + " ".join(parts[:-1])   # 'Ma J' -> 'J. Ma'
    ini = "-".join(_first(p) for p in parts[:-1])
    return ini + " " + last                              # 'Helin Yang' -> 'H. Yang'


def fmt_authors(raw):
    raw = (raw or "").strip()
    if not raw:
        return ""
    names = [n.strip() for n in raw.split(";") if n.strip()]
    out = []
    for n in names:
        if "et al" in n.lower():
            out.append("et al.")
        else:
            out.append(fmt_name(n))
    if len(out) == 1:
        return out[0]
    if out[-1] == "et al.":
        return ", ".join(out)
    if len(out) == 2:
        return "%s and %s" % (out[0], out[1])
    return "%s, and %s" % (", ".join(out[:-1]), out[-1])


def esc(t):
    t = (t or "").strip()
    for a, b in [("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"),
                 ("$", r"\$")]:
        t = t.replace(a, b)
    t = t.replace(r"\&amp;", r"\&")
    return t


VOL = re.compile(r"\bvol\.?\s*([0-9]+)\s*(?:\(([0-9A-Za-z]+)\))?")
PP = re.compile(r"\bpp\.?\s*([0-9]+)\s*[-\u2013]\s*([0-9]+)")


def split_venue(v):
    """'Journal vol 26(3), pp 1-10' -> ('Journal', ', vol. 26, no. 3, pp. 1-10')"""
    tail = []
    m = VOL.search(v)
    if m:
        tail.append("vol. %s" % m.group(1))
        if m.group(2):
            tail.append("no. %s" % m.group(2))
        v = v[:m.start()] + v[m.end():]
    m = PP.search(v)
    if m:
        tail.append("pp. %s--%s" % (m.group(1), m.group(2)))
        v = v[:m.start()] + v[m.end():]
    v = re.sub(r"[,\s]+$", "", v.strip())
    return v, "".join(", " + t for t in tail)


def bibitem(n, pid):
    r = papers[pid]
    au = fmt_authors(r["authors"])
    ti = esc(r["title"]).rstrip(".")
    ve, extra = split_venue(esc(r["venue"]))
    yr = r["year"]
    doi = (r["doi_url"] or "").strip()
    tail = ""
    if "doi.org/" in doi:
        tail = ", doi: %s" % esc(doi.split("doi.org/")[-1].rstrip("."))
    elif doi:
        tail = r", \url{%s}" % doi
    entry = "%s, %s, \\emph{%s}%s, %s%s." % (au, ti, ve, extra, yr, tail)
    return "\\bibitem[%d]{%s}\n%s\n" % (n, pid, entry)


body = BODY.read_text(encoding="utf-8")

order, seen = [], set()
for m in ID.finditer(body):
    pid = resolve(m.group(1))
    if pid in papers and pid not in seen:
        seen.add(pid)
        order.append(pid)
num = {pid: i for i, pid in enumerate(order, 1)}


def sub(m):
    pid = resolve(m.group(1))
    if pid not in num:
        return m.group(0)
    return r"\upcite{%s}" % pid


new = ID.sub(sub, body)

# collapse adjacent citations produced by ID lists: ...\upcite{a}\upcite{b}
def merge(m):
    keys = re.findall(r"\\upcite\{([^}]+)\}", m.group(0))
    flat = []
    for k in keys:
        flat.extend(x.strip() for x in k.split(","))
    return r"\upcite{%s}" % ",".join(flat)


new = re.sub(r"(?:\\upcite\{[^}]+\})(?:,\s*\\upcite\{[^}]+\})*", merge, new)

left = sorted(set(re.findall(r"\b(?:BG|[DTPQ])\d{2}\b", new)))
print("cited:", len(order), "| unresolved IDs left in body:", left[:10])

(SUB / "_body4.tex").write_text(new, encoding="utf-8")
(SUB / "_refs.tex").write_text(
    "".join(bibitem(num[p], p) for p in order), encoding="utf-8")

# every included study must be listed (PRISMA-ScR), so records not cited in the
# running text are appended in year order and enumerated in the appendix table.
ds = {r["id"]: r for r in csv.DictReader(open(ROOT / "dataset_papers.csv"))}
uncited = [p for p in ds if p not in num]
uncited.sort(key=lambda p: (ds[p]["year"], p))
for pid in uncited:
    order.append(pid)
num = {pid: i for i, pid in enumerate(order, 1)}
(SUB / "_refs.tex").write_text(
    "".join(bibitem(num[p], p) for p in order), encoding="utf-8")

FUNC = {"Authentication/RFFI": "RFFI/auth",
        "Anti-jamming/secure comms": "Anti-jam",
        "Key generation/distribution": "Keygen",
        "Federated/privacy-preserving FL": "FL/privacy",
        "Protocol/traffic/cryptanalysis": "Protocol",
        "PQC migration contextual": "PQC",
        "Learned primitives/crypto": "Primitive",
        "Side-channel attack analysis": "Side-chan."}
TRACK = {"defense": "D", "threat": "T", "both": "B", "pqc-context": "Q"}


def row(p):
    r = ds[p]
    au = (papers[p]["authors"] or "").split(";")[0].strip()
    toks = au.split()
    if len(toks) == 1:
        sur = toks[0]
    elif INI.match(toks[-1]) and len(toks[-1].replace("-", "").replace(".", "")) <= 4:
        sur = " ".join(toks[:-1])          # 'Ma J' -> 'Ma'
    else:
        sur = toks[-1]                      # 'Helin Yang' -> 'Yang'
    sur = sur.replace("et al.", "").strip()
    ve = papers[p]["venue"] or ""
    ve = ve.replace("&", r"\&")
    return "%d & %s & %s & %s & %s & %s & %s \\\\" % (
        num[p], p, sur.replace("&", r"\&"), r["year"], ve,
        TRACK.get(r["track"], "?"), FUNC.get(r["function"], r["function"]))


CORPUS = [p for p in order if p in ds]
half = (len(CORPUS) + 1) // 2
head = (r"\toprule" "\n" r"No. & ID & Author & Year & Venue & Tr. & Function \\"
        "\n" r"\midrule" "\n")
parts = []
for k, chunk in enumerate([CORPUS[:half], CORPUS[half:]], 1):
    parts.append("\\begin{table*}[p]\n\\centering\n\\scriptsize\n"
                 "\\setlength{\\tabcolsep}{2.5pt}\n"
                 "\\caption{%s}\n\\label{tab:corpus%s}\n"
                 "\\begin{tabular}{@{}lllll>{\\raggedright\\arraybackslash}p{3.3cm}>{\\raggedright\\arraybackslash}p{1.9cm}@{}}\n%s%s"
                 "\\bottomrule\n\\end{tabular}\n\\end{table*}\n"
                 % ("Included studies (part %d of 2): reference number, corpus ID, first "
                    "author, year, publication venue, track (D defense, T threat, B dual, "
                    "Q post-quantum context) and security function." % k,
                    "" if k == 1 else "b", head,
                    "\n".join(row(p) for p in chunk)))
(SUB / "_appendix.tex").write_text("".join(parts), encoding="utf-8")
print("references:", len(order), "| corpus rows in appendix:", len(CORPUS))
