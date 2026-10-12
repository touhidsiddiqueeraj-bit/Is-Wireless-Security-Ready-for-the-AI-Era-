"""Resolve the remaining 17 weak-bib rows.

For each arXiv ID: fetch journal-ref + DOI + latest version date.
Then Crossref title-search each full title; print top hit for review.
Writes nothing (human applies after review).
"""
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROWS = [
    ("D25", "2102.10639", "Privacy-Preserving Wireless Federated Learning Exploiting Inherent Hardware Impairments"),
    ("D33", "2411.10287", "Random Adversarial Data Obfuscation Model"),
    ("D35", "2403.10342", "Cooperative Jamming for Physical Layer Security Enhancement Using Deep Reinforcement Learning"),
    ("D38", "2210.02337", "When Physical Layer Key Generation Meets RIS Opportunities Challenges and Road Ahead"),
    ("D39", "2409.15303", "Disruptive RIS for Enhancing Key Generation and Secret Transmission in Low-Entropy Environments"),
    ("D42", "2507.00714", "RIS-Assisted Physical Layer Group Key Generation"),
    ("D45", "2605.15593", "Dynamic and Open-Set RF Fingerprinting and Localization in Crowded Indoor Environments"),
    ("D46", "2608.04881", "HoRFFI High-Openness RF Fingerprint Identification"),
    ("D49", "2308.07925", "Domain-Adaptive Device Fingerprints for Network Access Authentication"),
    ("D50", "2305.09594", "HiNoVa A Novel Open-set Detection Method for Automating RF Device Authentication"),
    ("D53", "2408.02095", "Secure Semantic Communications From Perspective of Physical Layer Security"),
    ("D63", "2306.13895", "Open-Set RF Fingerprinting via Improved Prototype Learning"),
    ("T09", "2007.08363", "Generative Adversarial Network in the Air Deep Adversarial Learning for Wireless Signal Spoofing"),
    ("T14", "2107.12173", "Membership Inference Attack and Defense for Wireless Signal Classifiers with Deep Learning"),
    ("T19", "2110.11188", "Classification of Encrypted IoT Traffic Despite Padding and Shaping"),
    ("T35", "2505.00487", "Analysis of the vulnerability of machine learning regression models to adversarial attacks using data from 5G wireless networks"),
    ("T36", "2607.20280", "Chained Attacks on Drone-Based Federated Learning From Network Disruption to Device Impersonation"),
]


def get(url, js=False):
    req = urllib.request.Request(url, headers={"User-Agent": "corpus-verify/1.0 (mailto:anon@example.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r) if js else r.read()


NS = {"a": "http://www.w3.org/2005/Atom", "arx": "http://arxiv.org/schemas/atom"}
print("=== arXiv journal-ref / DOI / version ===")
vers = {}
for pid, aid, _ in ROWS:
    try:
        e = ET.fromstring(get(f"http://export.arxiv.org/api/query?id_list={aid}")).find("a:entry", NS)
        if e is None:
            print(f"{pid} {aid} | ARXIV-NOT-FOUND")
            continue
        jr = (e.findtext("arx:journal_ref", default="", namespaces=NS) or "").strip()
        doi = (e.findtext("arx:doi", default="", namespaces=NS) or "").strip()
        upd = (e.findtext("a:updated", default="", namespaces=NS) or "")[:10]
        vers[pid] = upd
        print(f"{pid} {aid} | jref={jr[:90] or '-'} | doi={doi or '-'} | updated={upd}")
    except Exception as ex:  # noqa: BLE001
        print(f"{pid} {aid} | ERROR {ex}")
    time.sleep(1)

print("=== Crossref top hit by title ===")
for pid, _, title in ROWS:
    try:
        d = get("https://api.crossref.org/works?query.title=" + urllib.parse.quote(title)
                + "&rows=1&select=title,author,container-title,DOI,score,published", True)
        items = d["message"]["items"]
        if not items:
            print(f"{pid} | NO-HIT")
            continue
        m = items[0]
        au = "; ".join(f"{a.get('given', '')} {a.get('family', '')}".strip() for a in m.get("author", [])[:3])
        print(f"{pid} | {m.get('title', ['?'])[0][:80]} | {au[:50]} | "
              f"{'; '.join(m.get('container-title', [])[:1])[:50]} | {m.get('DOI', '')} | s={m.get('score', 0):.0f}")
        time.sleep(1)
    except Exception as ex:  # noqa: BLE001
        print(f"{pid} | ERROR {ex}")
