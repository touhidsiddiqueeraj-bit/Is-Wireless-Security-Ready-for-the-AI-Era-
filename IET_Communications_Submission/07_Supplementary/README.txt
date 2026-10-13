SUPPLEMENTARY MATERIAL — CONTENTS
=================================
This folder contains the classified corpus and the scripts that verify and
regenerate every number and figure from it, as described in the manuscript's
Data Availability statement.

data/
    dataset_papers.csv
        The classified corpus: 130 curated studies (2020–2026) — a
        121-study core (84 defense, 30 threat, 7 dual attack-plus-defense)
        plus a separate 9-study post-quantum-cryptography stratum. One row
        per study; every record carries a resolvable identifier (Crossref,
        arXiv, ACM, or USENIX) plus the six coding fields: security
        function, AI method family, track, primary data source, validation
        practice, and readiness (R1–R5).
    found_papers.csv
        The bibliography underlying the corpus: DOI/arXiv identifiers for
        every record, with no fabricated entries. Provenance notes in this
        file are lightly normalized for release; the complete decision
        history lives in the full research archive's run log.

analysis_scripts/
    check_consistency.py   Consistency gate for the N=130 corpus (asserts
        corpus size, track/year/channel distributions, depth splits, and
        related invariants). It is written for the released research
        archive's layout — it additionally reads manuscript.tex, data/*.csv,
        and the archive's tables/ exports relative to that archive — so run
        it from a checkout of the full archive; the dataset-level checks can
        be reproduced here with verify_dataset.py.
    verify_dataset.py      Verifies headline counts against
        data/dataset_papers.csv.
    claim_checks.py        Consolidated claim checks: computes the numbers
        reported in the manuscript directly from the released dataset and
        writes claim_checks.json.
    regen_data_figs.py     Regenerates the data-driven figures from the CSV.
    regen_concept_figs.py  Regenerates the conceptual figures.

The screening log, retrieval records, and the complete runnable archive
layout ship with the submission as described in the Data Availability
statement. Coding was performed by the first author and independently
validated by the second author; no blind inter-coder agreement statistic
(e.g., kappa) is claimed.
