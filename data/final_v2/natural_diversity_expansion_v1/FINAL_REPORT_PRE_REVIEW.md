# Natural Diversity Expansion V1 — final pre-review report

## Outcome

- Accepted natural candidates: **779**
- Scientific rejects: **1** (`missing_textual_code_patch`)
- Operational pending: **0**
- Completely unseen repositories: **20**
- Language distribution: **400 Python / 379 TypeScript**
- Human labels populated: **0**
- Review status: **779 pending**
- Models trained or evaluated: **none**
- Historical confirmation examples accessed: **no**

## Pre-label acquisition strata

These are targeting strata inferred only from repository documentation path metadata. They are not labels.

- `developer_setup`: **320** (41.08%)
- `model_contract`: **199** (25.55%)
- `configuration`: **140** (17.97%)
- `api_reference`: **120** (15.40%)

## Frozen repository split

The split was assigned deterministically by repository before any human label exists.

- Development train: **16 repositories / 619 rows**
- Refresh validation: **4 repositories / 160 rows**
- Repository overlap between partitions: **0**
- Overlap with the 838-repository previously-seen universe: **0**
- Refresh validation is explicitly excluded from future training.

## Leakage and integrity audit

- Duplicate `case_id`: **0**
- Duplicate repository/PR key: **0**
- Missing BASE-SHA/docs-before evidence: **0**
- More than 12 documentation contexts: **0**
- Forbidden classifier-model input fields: **0**
- Pre-labeled rows: **0**
- Raw audit-only rows containing docs-after evidence: **233**
- Docs-after/docs-diff used for targeting, splitting, model input, or review input: **no**
- Review batches expose only pre-change evidence and omit audit-only outcome fields.

## Human review package

- Prefilled review rows: **779**
- Batches: **8** (7 × 100, final batch 79)
- Editable fields: `human_docs_update_required`, `human_doc_category`, `human_label_notes`, `review_status`
- All editable fields remain unset/pending.
- Each row has a deterministic evidence hash.

## Execution quality

- Seed acquisition: **1,100 diverse seeds** from all shortlisted repositories before capping.
- Round-robin pilot plan: **780 seeds** across 20 repositories.
- Final builder: **779 accepted / 1 scientific reject / 0 operational pending**.
- Builder retrieval: BASE-SHA git tree/blob retrieval, 0 REST documentation fallbacks in the final run.
- Tests: **281 passed**, 30 existing scikit-learn single-label warnings.

## Disk footprint

Approximate local footprint under this expansion root:

- GitHub/git caches: **750.9 MB**
- Candidate artifacts (including excluded sequential diagnostic run): **222.0 MB**
- Human-review package: **157.2 MB**
- Final stratified checkpoints: **112.2 MB**
- Excluded sequential diagnostic checkpoints: **109.8 MB**
- Partition materializations: **52.5 MB**
- Discovery cache: **16.8 MB**
- Acquisition artifacts: **6.0 MB**
- Free space after completion: **28.9 GB**

The earlier sequential 800-row build is retained only as a diagnostic artifact and is excluded from the split/review package. The authoritative pilot candidate file is `candidates/pilot_candidates.jsonl`.
