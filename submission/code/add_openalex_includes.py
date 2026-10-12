"""Add 14 OpenAlex database-run includes (abstract-screened, V1-V3 pass).

Excluded at title/abstract level (logged, not added): O-RAN AML analysis
(systematic review w/o primary mechanism -> background), QML keygen NJAP
(conceptual plan, no evaluable evidence -> background), Safe Exploration
TIFS (no crypto-primitive link -> excluded).
"""
import csv
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

# found_papers rows: id,title,authors,year,venue,doi_url,track,status,note
FP_NEW = [
    ("D70", "No Blind Spots: On the Resiliency of Device Fingerprints to Hardware Warm-Up Through Sequential Transfer Learning",
     "Elmaghbub A; Hamdaoui B", "2024", "ACM WiSec", "https://doi.org/10.1145/3643833.3656138", "defense", "verified", "OpenAlex run; abstract-screened"),
    ("D71", "PAST-AI: Physical-Layer Authentication of Satellite Transmitters via Deep Learning",
     "Oligeri G; Sciancalepore S; Raponi S; Di Pietro R", "2022", "IEEE Trans Inf Forensics Secur", "https://doi.org/10.1109/tifs.2022.3219287", "defense", "verified", "OpenAlex run; abstract-screened"),
    ("D72", "Distinguishable IQ Feature Representation for Domain-Adaptation Learning of WiFi Device Fingerprints",
     "Elmaghbub A; Hamdaoui B", "2024", "IEEE Trans Mach Learn Commun Netw", "https://doi.org/10.1109/tmlcn.2024.3446743", "defense", "verified", "OpenAlex run; abstract-screened"),
    ("D73", "On the Generalization of Deep Learning Based Radio Frequency Fingerprint Identification System in a Multi-Distance Scenario",
     "Ahmed A; Quoitin B; Fontaine J; Shahid A", "2025", "IEEE PIMRC", "https://doi.org/10.1109/pimrc62392.2025.11275484", "defense", "verified", "OpenAlex run; abstract-screened"),
    ("D74", "Channel-Informed Neural Network for Physical Layer Key Generation",
     "Sanchez Viloria JA; Sklivanitis G; Pados D; Bentley ES", "2026", "venue unconfirmed (arXiv 2609.16341)", "https://arxiv.org/abs/2609.16341", "defense", "verified", "OpenAlex run; abstract-screened"),
    ("D75", "Deep Learning based Cross-Receiver Radio Frequency Fingerprint Identification Under Varying Channels",
     "He J; Wang Y; He F; Huang S", "2026", "venue unconfirmed (arXiv 2603.08402)", "https://arxiv.org/abs/2603.08402", "defense", "verified", "OpenAlex run; abstract-screened"),
    ("D76", "IPRU: Input-Perturbation-based Radio Frequency Fingerprinting Unlearning for LAWNs",
     "Liu C; Meng R; Liu Y; Xu X", "2026", "venue unconfirmed (arXiv 2604.24022)", "https://arxiv.org/abs/2604.24022", "defense", "verified", "OpenAlex run; abstract-screened"),
    ("D77", "UAV Communication Against Intelligent Jamming: A Stackelberg Game Approach With Federated Reinforcement Learning",
     "Yin Z; Li J; Wang Z; Qian Y", "2024", "IEEE Trans Green Commun Netw", "https://doi.org/10.1109/tgcn.2024.3373886", "defense", "verified", "OpenAlex run; abstract-screened"),
    ("T41", "Backdoor Attack on Self-Supervised Learning-Based RFF Identification Using Spectrum Enhanced Insensitive Perturbation Trigger",
     "Yao Z; Gui G", "2025", "IEEE Trans Inf Forensics Secur", "https://doi.org/10.1109/tifs.2025.3577013", "threat", "verified", "OpenAlex run; abstract-screened"),
    ("T42", "Over-The-Air Adversarial Attacks on Deep Learning Wi-Fi Fingerprinting (FooLoc)",
     "Xiao F; Huang Y; Zuo Y; Kuang W", "2023", "venue unconfirmed (arXiv 2301.03760)", "https://arxiv.org/abs/2301.03760", "threat", "verified", "OpenAlex run; abstract-screened"),
    ("T43", "Hidden Backdoor Attack: A New Threat to Learning-Aided Physical Layer Authentication",
     "Huang Y; Liu W; Wang H-M", "2023", "IEEE Ucom", "https://doi.org/10.1109/ucom59132.2023.10257584", "threat", "verified", "OpenAlex run; abstract-screened"),
    ("T44", "Frequency-Selective Adversarial Attack Against Deep Learning-Based Wireless Signal Classifiers",
     "Ke D; Wang X; Huang Z", "2024", "IEEE Trans Inf Forensics Secur", "https://doi.org/10.1109/tifs.2024.3352423", "threat", "verified", "OpenAlex run; abstract-screened"),
    ("T45", "Acoustic and vibration side channel analysis on post-quantum cryptography using image-based deep learning",
     "Muhammad AH; Mandar G; Ibrahim A", "2026", "TELKOMNIKA", "https://doi.org/10.12928/telkomnika.v24i4.27791", "threat", "verified", "OpenAlex run; first AIxPQC join; device-implementation SCA like T01/T08"),
    ("T46", "Security Analysis of IoT Traffic Classification Systems Under Adversarial Machine Learning Attacks",
     "Li C; Zhang X", "2026", "J Cyber Secur Mobility", "https://doi.org/10.13052/jcsm2245-1439.1547", "both", "verified", "OpenAlex run; abstract-screened; attack+defense evaluated"),
]

# dataset rows: id,title_short,track,year,venue_type,function,method_family,
#   data_source,validation,R1,R2,R3,R4,R5 (+venue_channel computed)
DS_NEW = [
    ("D70", "No Blind Spots: warm-up-resilient RFFI (HEEDFUL)", "defense", "2024", "peer-reviewed", "Authentication/RFFI", "Deep supervised (CNN/RNN/Transformer)", "Collected dataset/traces", "Standard split/unclear", 1, 1, 0, 0, 0),
    ("D71", "PAST-AI: satellite PLA", "defense", "2022", "peer-reviewed", "Authentication/RFFI", "Deep supervised (CNN/RNN/Transformer)", "Collected dataset/traces", "Standard split/unclear", 1, 1, 0, 0, 0),
    ("D72", "EPS IQ features for domain-adaptive WiFi RFFI", "defense", "2024", "peer-reviewed", "Authentication/RFFI", "Deep supervised (CNN/RNN/Transformer)", "Collected dataset/traces", "Cross-domain/generalization test", 1, 2, 0, 0, 0),
    ("D73", "Multi-distance LoRa RFFI generalization", "defense", "2025", "peer-reviewed", "Authentication/RFFI", "Deep supervised (CNN/RNN/Transformer)", "Testbed/OTA measurement", "Cross-domain/generalization test", 1, 2, 0, 0, 0),
    ("D74", "Channel-informed NN key generation", "defense", "2026", "preprint", "Key generation/distribution", "Deep supervised (CNN/RNN/Transformer)", "Testbed/OTA measurement", "Testbed/field demonstration", 1, 2, 0, 0, 0),
    ("D75", "Cross-receiver RFFI (DSQ-TCNN)", "defense", "2026", "preprint", "Authentication/RFFI", "Deep supervised (CNN/RNN/Transformer)", "Collected dataset/traces", "Cross-domain/generalization test", 1, 2, 0, 0, 0),
    ("D76", "IPRU: RFF unlearning for LAWNs", "defense", "2026", "preprint", "Authentication/RFFI", "Defensive/robust ML", "Unclear (abstract)", "Standard split/unclear", 1, 1, 0, 0, 0),
    ("D77", "Stackelberg federated-RL UAV anti-jamming", "defense", "2024", "peer-reviewed", "Anti-jamming/secure comms", "Reinforcement/DRL", "Simulation", "Simulation-only", 1, 1, 0, 0, 0),
    ("T41", "SEIP backdoor on SSL-RFFI", "threat", "2025", "peer-reviewed", "Authentication/RFFI", "Adversarial ML", "Unclear (abstract)", "Standard split/unclear", 2, 1, 0, 0, 0),
    ("T42", "FooLoc OTA attack on WiFi fingerprinting", "threat", "2023", "preprint", "Authentication/RFFI", "Adversarial ML", "Testbed/OTA measurement", "Testbed/field demonstration", 2, 2, 0, 0, 0),
    ("T43", "Hidden backdoor on PLA (IQ triggers)", "threat", "2023", "peer-reviewed", "Authentication/RFFI", "Adversarial ML", "Unclear (abstract)", "Standard split/unclear", 2, 1, 0, 0, 0),
    ("T44", "Frequency-selective attack on signal classifiers", "threat", "2024", "peer-reviewed", "Protocol/traffic/cryptanalysis", "Adversarial ML", "Unclear (abstract)", "Standard split/unclear", 2, 1, 0, 0, 0),
    ("T45", "Acoustic/vibration CNN-ViT SCA on PQC", "threat", "2026", "peer-reviewed", "Side-channel attack analysis", "Deep supervised (CNN/RNN/Transformer)", "Collected dataset/traces", "Standard split/unclear", 1, 1, 0, 0, 0),
    ("T46", "Constraint-aware robust IoT traffic classification", "both", "2026", "peer-reviewed", "Protocol/traffic/cryptanalysis", "Adversarial ML", "Collected dataset/traces", "Standard split/unclear", 2, 1, 0, 0, 0),
]


def channel(venue_type, venue):
    keys = ["conf", "workshop", "symposium", "milcom", "globecom", "infocom",
            "mobicom", "wisec", "wiseml", "ndss", "ccs", "icccn", "isncc",
            "ncic", "wcnc", "wcsp", "ismvl", "icassp", "vtc", "icc", "gass",
            "cps-iot", "aiiot", "lnns", "lecture notes", "chapter", "wpes",
            "camad", "iscc", "ucom", "pimrc"]
    return "preprint" if venue_type == "preprint" else (
        "conference" if any(k in venue.lower() for k in keys) else "journal")


fp_path = f"{ROOT}/found_papers.csv"
fp = list(csv.DictReader(open(fp_path)))
assert not any(r["id"] in [x[0] for x in FP_NEW] for r in fp), "ID collision"
for row in FP_NEW:
    fp.append(dict(zip(fp[0].keys(), row)))
with open(fp_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fp[0].keys())
    w.writeheader()
    w.writerows(fp)

ds_path = f"{ROOT}/dataset_papers.csv"
ds = list(csv.DictReader(open(ds_path)))
cols = ds[0].keys()
base = ["id", "title_short", "track", "year", "venue_type", "function",
        "method_family", "data_source", "validation", "R1", "R2", "R3", "R4", "R5"]
fpf = {r["id"]: r for r in fp}
for row in DS_NEW:
    d = dict(zip(base, [str(x) for x in row]))
    d["venue_channel"] = channel(d["venue_type"], fpf[d["id"]]["venue"])
    ds.append(d)
with open(ds_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cols))
    w.writeheader()
    w.writerows(ds)

from collections import Counter
print(len(ds), Counter(r["venue_type"] for r in ds), Counter(r["venue_channel"] for r in ds))
print("years:", sorted(Counter(r["year"] for r in ds).items()))
print("tracks:", Counter(r["track"] for r in ds))
print("functions:", Counter(r["function"] for r in ds).most_common())
print("methods:", Counter(r["method_family"] for r in ds).most_common())
