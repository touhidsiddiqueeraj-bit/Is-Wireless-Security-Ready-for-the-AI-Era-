"""Stage 2: retry failed OpenAlex queries, then title-gate all hits.

Gate mirrors the Crossref title gate (wireless AND crypto/auth AND AI terms).
Writes: openalex_gated.json. Prints gate statistics + gated titles for review.
"""
import json
import re
import time
import urllib.parse
import urllib.request

MAIL = "mailto=corpus-verify@example.com"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "corpus-triangulation/1.0 (mailto:corpus-verify@example.com)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


QUERIES = [
    "RF fingerprinting deep learning authentication",
    "physical layer key generation machine learning wireless",
    "adversarial attacks radio frequency fingerprint identification",
    "LoRa device identification deep learning security",
    "electromagnetic side channel deep learning AES wireless",
    "5G AKA protocol fuzzing security",
    "anti-jamming deep reinforcement learning UAV",
    "federated learning wireless privacy security over-the-air",
    "post-quantum cryptography wireless constrained devices Kyber",
    "encrypted traffic classification machine learning wireless IoT",
]
WIRELESS = ["wireless", "radio", "rf ", "rff", "fingerprint", "lora", "zigbee",
            "bluetooth", "ble ", "wi-fi", "wifi", "802.11", "5g", "6g", "lte",
            "iot", "v2x", "uav", "drone", "swarm", "phy", "physical-layer",
            "physical layer", "antenna", "ofdm", "csi", "mimo", "nfc", "satellite"]
CRYPTO = ["encrypt", "crypt", "auth", "fingerprint", "fuzz", "spoof", "impersonat",
          "adversar", "backdoor", "side-channel", "side channel", "key", "privacy",
          "secure", "security", "attack", "defense", "defence", "jamm", "trojan",
          "anonym", "padding", "aka "]
AI = ["learn", "neural", "deep ", "cnn", "rnn", "lstm", "transformer", "gan ",
      "gan-", "reinforcement", "federat", "contrastive", "autoencoder",
      "graph neural", "meta-learn", "few-shot", "open-set", "ai-", "ai ",
      "artificial intelligence", "machine intelligence"]


def gate(title):
    t = f" {(title or '').lower()} "
    return (any(k in t for k in WIRELESS) and any(k in t for k in CRYPTO)
            and any(k in t for k in AI))


recs = {json.dumps(h, sort_keys=True) for h in json.load(open("openalex_records.json"))}
hits = [json.loads(r) for r in recs]
have_q = set(h["q"] for h in hits)
for qi in range(len(QUERIES)):
    if qi in have_q:
        continue
    for attempt in range(4):
        try:
            url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(QUERIES[qi])
                   + "&filter=from_publication_date:2020-01-01,to_publication_date:2026-10-11"
                   + "&per-page=100&select=id,doi,title,publication_year,primary_location,authorships,cited_by_count"
                   + f"&{MAIL}")
            d = get(url)
            print(f"Q{qi} retry-ok count={d.get('meta', {}).get('count')} took={len(d.get('results', []))}")
            for w in d.get("results", []):
                dk = (w.get("doi") or "").lower().replace("https://doi.org/", "").strip() or None
                hits.append({"doi": dk, "title": w.get("title"), "year": w.get("publication_year"),
                             "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                             "cites": w.get("cited_by_count"), "q": qi})
            break
        except Exception as ex:  # noqa: BLE001
            print(f"Q{qi} attempt {attempt}: {ex}")
            time.sleep(5 * (attempt + 1))
    time.sleep(2)

json.dump(hits, open("openalex_records.json", "w"), indent=1)
cands = json.load(open("openalex_new_candidates.json"))
gated = [c for c in cands if gate(c.get("title"))]
json.dump(gated, open("openalex_gated.json", "w"), indent=1)
print(f"\nhits={len(hits)} new={len(cands)} gated={len(gated)}")
for g in gated:
    print(f"  [{g['year']}] {str(g['title'])[:85]} | {g['venue']} | {g['doi']}")
