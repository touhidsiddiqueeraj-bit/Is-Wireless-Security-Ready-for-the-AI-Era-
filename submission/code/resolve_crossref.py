"""Second pass: Crossref title search for rows missing authors/venue/DOI.

Prints top-hit authors + venue + DOI + score for human review; writes nothing.
"""
import json
import time
import urllib.parse
import urllib.request

TITLES = {
    "D07": "Towards Receiver-Agnostic and Collaborative Radio Frequency Fingerprint Identification",
    "D11": "Deep Learning-based Physical-Layer Secret Key Generation for FDD Systems",
    "D13": "Physical Layer Key Distribution Technology on Deep Learning",
    "D15": "Multi-Agent Reinforcement Learning Based UAV Swarm Communications Against Jamming",
    "D19": "Hybrid PLS-ML Authentication Scheme for V2I",
    "D31": "Open-Set Radio Frequency Fingerprint Identification Based on Multi-Task Prototype",
    "D32": "Securing UAV Communications by Fusing Cross-Layer Fingerprints",
    "D34": "Aerial Base Station Positioning and Power Control for Securing Communications",
    "D40": "Fluid Antenna Enabled Physical Layer Key Generation",
    "D42": "RIS-Assisted Physical Layer Group Key Generation",
    "D45": "Dynamic and Open-Set RF Fingerprinting and Localization in Crowded Indoor Environments",
    "D46": "HoRFFI High-Openness RF Fingerprint Identification",
    "P04": "Vectorized Implementation of Kyber and Dilithium on 32-bit ARM Cortex-A",
    "P08": "Post-Quantum Wireless-based Key Encapsulation Mechanism via CRYSTALS-Kyber",
    "P10": "Post-Quantum Entropy as a Service for Embedded Systems",
    "T08": "Is Your Bluetooth Chip Leaking Secrets via RF Signals",
    "T23": "SoK Evaluating 5G Protocols Against Legacy and Emerging Privacy and Security Attacks",
    "T27": "FLARE A Wireless Side-Channel Fingerprinting Attack on Federated Learning",
    "T34": "Practical Adversarial Attack on WiFi Sensing Through Unnoticeable Communication",
    "T35": "Analysis of the vulnerability of machine learning regression models to adversarial attacks using data from 5G wireless networks",
    "T40": "An Adversarial-Driven Experimental Study on Deep Learning for RF Fingerprinting",
    "D54": "Byzantine-Resilient Federated Machine Learning via Over-the-Air Computation",
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "corpus-verify/1.0 (mailto:anon@example.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


for pid, title in TITLES.items():
    try:
        q = urllib.parse.quote(title)
        d = get(f"https://api.crossref.org/works?query.title={q}&rows=2&select=title,author,container-title,DOI,score,published,type")
        items = d["message"]["items"]
        if not items:
            print(f"{pid} | NO-HIT")
            continue
        m = items[0]
        au = "; ".join(f"{a.get('given', '')} {a.get('family', '')}".strip() for a in m.get("author", [])[:4])
        ven = "; ".join(m.get("container-title", [])[:1])
        print(f"{pid} | {au[:80]} | {ven[:60]} | {m.get('DOI', '')} | score={m.get('score', 0):.1f}")
        time.sleep(1)
    except Exception as ex:  # noqa: BLE001
        print(f"{pid} | ERROR {ex}")
