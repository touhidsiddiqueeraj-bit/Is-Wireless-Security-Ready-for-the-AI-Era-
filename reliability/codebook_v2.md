# Coder 2 codebook — v2 (2026-11-23), clarification round for five failing items

Round 1 (`codebook_v1.md`) produced κ 0.39 / 0.29 / 0.11 / 0.38 / 0.21 on R1, R2, R3,
data_source, validation. The agreement matrix showed those misses are **definitional, not
random**: 15 of 17 R1 disagreements were exactly one level down, 6 of 11 validation
disagreements were "Testbed → Standard split/unclear", 8 of 30 data_source disagreements
were "Testbed/OTA → something weaker", and 7 of 9 R3 disagreements were `1 → 0`.

v2 fixes those five items. **R5 is carried over unchanged as a control**: if its κ moves
much, the sheet is being taught rather than clarified.

*Post hoc notice:* v2 was written after seeing round-1 disagreements, which is why round 1
is reported as primary and round 2 as secondary. That is disclosed in the paper.

## The single biggest defect in v1

`R1 = 0` and `R3 = 0` were never used by coder 1 anywhere in 130 rows, and `validation`
had no rule for what an abstract must *say* to license a hardware claim. Coder 2 applied
the anchors literally; coder 1 did not. v2 therefore states the floors and the evidence
thresholds instead of leaving them to inference.

Score **only** the six columns in `coder2_round2.csv`, again from the abstract in the sheet.

---

## R1 — attacker-capability explicitness

| Score | Condition |
|---|---|
| 0 | No adversary appears in the abstract. The paper only builds or evaluates a model, and the threat is verbal ("security is at risk") without anyone doing anything. |
| 1 | An adversary is named (attacker, eavesdropper, impersonator, adversary, malicious node) but the abstract states no capability: no access type, no knowledge assumption, no range, no budget. |
| 2 | A capability or assumption is stated: access type (passive/active, over-the-air, chosen-plaintext), knowledge assumption (known-plaintext, known-position, priori CSI), physical condition (distance, SNR, mobility), or a quantified budget. One such statement is enough. |

**Use 0.** A defense paper that never mentions an attacker is a 0, not a 1. A paper that
says "adversarial examples threaten DNNs" and then defends without naming an attacker is
a 0 as well; naming the *phenomenon* is not naming an *adversary*.

## R2 — evaluation realism

Two-part test. First ask "who produced the evaluation data?" then "was a real attack or
key recovery actually carried out?"

| Score | Condition |
|---|---|
| 0 | No evaluation on data: proof, analysis, complexity, formal security argument only. |
| 1 | Any of: simulation; a third-party or public dataset; cross-domain/generalization protocols on collected data; the abstract never says who collected the data. |
| 2 | The abstract attributes the hardware/over-the-air evaluation to the authors (testbed, SDR/USRP, field trial, measurements we captured) **or** reports an actual key/credential recovery or a successful over-the-air attack. |

**Third-party data caps at 1.** "Evaluated on real-world captures from the literature" is 1.
"Collected 10 000 frames on two USRP B210s" is 2. If the abstract is silent on provenance, 1.

## R3 — cost / attacker-cost signal

| Score | Condition |
|---|---|
| 0 | No cost information, or purely qualitative claims ("lightweight", "efficient", "low overhead") with no number and no target. |
| 1 | A **number** plus a **named hardware/implementation target**: e.g. "15 ms per authentication on a Cortex-M4", "0.088 ms processing on a Jetson Nano". For attack papers: a quantified attacker cost (compute, query count, RF budget, attack time) plus the equipment it was measured on. |
| 2 | Both cost classes (latency **and** energy, or attacker cost **and** success rate) with a named target. |

**The "and" is load-bearing.** A number with no target is 1 *only if* the abstract names a
target elsewhere; otherwise 0. A target with no number is 0.

## validation — what counts as evidence in an abstract

Forced choice, first matching row wins:

| Score | Condition |
|---|---|
| Benchmark/analysis | Evaluation is proof, complexity/area measurement, or a benchmark suite — no learning experiment. |
| Simulation-only | The abstract says the evaluation is simulated / synthetic / generated channels. |
| Cross-domain/generalization test | Training and test conditions deliberately differ (receivers, days, channels, datasets) **and** the abstract presents that transfer as the evaluation. |
| Testbed/field demonstration | The abstract attributes hardware/over-the-air/field evaluation to the authors. Requires an author-attributed artefact word: "we collected", "our testbed", "measured on", "field trial". |
| Standard split/unclear | Everything else, including any abstract that does not say who collected the data. |

Tie-break for "testbed data, standard split": if the author-attributed hardware statement
is present → Testbed/field demonstration (this row describes *realism*, not split design).
If only a dataset is named, with no author-attribution → Cross-domain if transfer is the
point, else Standard split/unclear.

## data_source — who produced the data

| Score | Condition |
|---|---|
| Testbed/OTA measurement | Author-attributed capture on hardware (same attribution test as validation). |
| Collected dataset/traces | A named third-party or public dataset, or data collected by someone else. |
| Simulation | Synthetic generation, or simulation of channels/signals, even with realistic parameters. |
| Analysis/benchmark | No learning data: measurements of an implementation, proofs, benchmarks, complexity. |
| Unclear (abstract) | The abstract gives no signal at all. Prefer this over guessing. |

**Consistency rule:** data_source and validation must tell the same story. Author-attributed
hardware ⇒ `Testbed/OTA measurement` + `Testbed/field demonstration`. If you find yourself
about to write "Testbed/OTA measurement" with validation "Standard split/unclear", stop:
either the author attribution is there (then both move) or it is not (then both stay down).

## R5 — unchanged (control)

0 none / 1 mentions 3GPP, IETF, NIST, ETSI, or a named standard/profile / 2 evaluated
against a profile. Identical wording to v1; this item is here to check that v2 does not
simply raise every κ.

## When you are done

`git commit -m "coder 2 round-2 scored (5 clarified items + R5 control, n=30)"` and tell me.
κ is then recomputed for these six items only; the eleven v1 items stay as published in
round 1.
