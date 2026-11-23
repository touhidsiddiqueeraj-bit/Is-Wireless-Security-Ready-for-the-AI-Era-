# Coder 2 codebook — v1 (2026-11-23), frozen before scoring

You are coding **`reliability/coder2_scores.csv`**: 30 rows, each with title, venue, year
and the abstract text the first coder worked from. Fill the 11 empty columns.

## Ground rules

1. **Evidence = the abstract in the sheet, nothing else.** Do not consult the paper, the
   web, or `dataset_papers.csv`. If the abstract does not state something, that is data:
   score it as absent, not as "probably there".
2. **Do not open `dataset_papers.csv` until the sheet is filled and committed.** It holds
   coder 1's scores; looking first destroys the blind. `sample_frozen.csv` also records
   the sampling strata — open it after scoring if you want a clean blind on `track`.
3. **Conservative rule** (inherited from the manuscript): when the abstract sits between
   two levels of an R item, take the lower level and say why in `coder2_note`.
4. **Disagreement is the product.** Code what the codebook says, not what the corpus
   probably says. If an anchor is ambiguous, score your best reading and log the
   ambiguity in `coder2_note` — that sentence becomes part of the reliability report.
5. Roughly 2–3 min per row; ~60–90 min total.

## Fields (11)

### `track`
- `threat` — the contribution is an attack or attack analysis against a wireless
  security function.
- `defense` — the contribution protects, hardens, or authenticates (includes learned
  models used as a defense).
- `both` — develops **and** evaluates both sides under one evaluation.
- `pqc-context` — post-quantum cryptography implementation/migration paper (contextual
  set, not an AI-security paper).

### `function` (one of 8)
`Authentication/RFFI` · `Key generation/distribution` · `Anti-jamming/secure comms` ·
`Protocol/traffic/cryptanalysis` · `PQC migration (contextual)` ·
`Federated/privacy-preserving FL` · `Learned primitives/crypto` ·
`Side-channel attack analysis`

Pick the function the paper's *security mechanism* serves. RFFI, PUF-free device
identification and PHY-layer authentication all map to `Authentication/RFFI`.
Encryption/key-establishment schemes built from learned components map to
`Learned primitives/crypto`; cryptanalysis of an existing protocol maps to
`Protocol/traffic/cryptanalysis`.

### `method_family` (one of 12)
`Deep supervised (CNN/RNN/Transformer)` · `Adversarial ML` · `Federated/private learning` ·
`Reinforcement/DRL` · `PQC implementation` · `Survey/systematization` ·
`Dataset/benchmark contribution` · `Defensive/robust ML` · `Traffic-analysis ML` ·
`Optimization-based (SCA/SDR)` · `Classical/Bayesian ML` · `LLM/foundation-assisted`

Code the *dominant* AI method. Attack papers that generate adversarial examples or use a
GAN are `Adversarial ML`. A paper whose main artifact is data or a benchmark is
`Dataset/benchmark contribution` even if it trains models on it.

### `data_source`
- `Testbed/OTA measurement` — the authors captured signals themselves on hardware.
- `Collected dataset/traces` — a pre-existing or third-party dataset is used.
- `Simulation` — synthetic channel/data generation.
- `Analysis/benchmark` — no learning data; proofs, measurements of implementations,
  benchmark runs.
- `Unclear (abstract)` — the abstract does not say. Use this rather than guessing.

### `validation`
- `Testbed/field demonstration` — author-run hardware/Ota evaluation.
- `Simulation-only` — the evaluation is explicitly simulation.
- `Cross-domain/generalization test` — evaluated on conditions/receivers/datasets outside
  the training distribution.
- `Standard split/unclear` — same-distribution train/test, or the abstract does not say.
- `Benchmark/analysis` — evaluation by proof, complexity/area measurement, benchmark suite.

### `venue_channel`
`journal` · `conference` (workshop counts here) · `preprint` (arXiv/eprint, no confirmed
venue). Derive it from the `venue` string; "unconfirmed"/arXiv means `preprint`.

## Readiness items R1–R5 (0–2)

Anchors are the manuscript's, verbatim:

- **R1 attacker-capability explicitness** — 0 absent / 1 implicit / 2 explicit capability
  + assumptions.
- **R2 evaluation realism** — 0 theory/proof without data evaluation / 1 controlled
  evaluation (simulation, reused data, or cross-domain protocols on collected data) /
  2 author-conducted OTA/testbed demonstration or demonstrated real key recovery.
- **R3 cost** — defense/learned-crypto: 0 none / 1 latency **or** energy + hardware
  target / 2 both + target.
- **R4 artifact release** — 0 neither / 1 code **or** data / 2 both or artifact-evaluated.
- **R5 standards alignment** — 0 none / 1 mentions 3GPP/IETF/NIST/ETSI / 2 evaluated
  against a profile.

As applied in this corpus (also from the manuscript):

- Simulation-only rows score **R2 = 1**.
- A standard-split row whose evaluation demonstrates real over-the-air key recovery may
  score **R2 = 2**; the corpus contains exactly one such documented override (T01). Code
  the anchors as written; if your reading differs from the corpus, that is a finding.
- **R3 and R5 apply to attack rows too**, with an observable attacker-cost or
  standards signal; rows without such a signal score 0 (not N/A).
- Totals sum applicable items only.

### Clarifications added for this pass (v1, fixed before scoring)

- **C1 — threat-side R3.** For an attack paper, R3 = 1 means the abstract reports an
  attacker cost (compute, RF/query budget, attack or key-recovery time, required
  equipment); R3 = 2 additionally names the hardware/implementation target the cost was
  measured on. Defender anchors ("latency or energy + hardware target") are the defense
  reading of the same item.
- **C2 — no N/A in this sheet.** Every row gets a 0–2 on R1–R5. 0 means "criterion
  applies, abstract shows no signal".
- **C3 — R4 has almost no variance in this corpus.** That is a known result, not a cue to
  inflate it: score 1 or 2 only if the abstract explicitly points to released
  code/data/artifact.

## When you are done

1. `git add reliability/coder2_scores.csv && git commit -m "coder 2 scored (n=30, blind)"`
   — the commit hash is the blindness proof.
2. Tell me. I then join against `dataset_papers.csv`, compute agreement, and write the
   reliability report. Nothing gets tuned before that join.
