# Final V2 Finalization Protocol

This protocol is the canonical operating procedure for finishing the DocGuard Final V2 thesis experiment. The repository is the implementation source of truth. Later gates may not silently revise a completed gate; any superseding decision must create a new explicit manifest and explain why the previous artifact is being replaced.

## Global invariants

- Final classifier inputs are limited to `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`.
- Audit-only, gold-only, outcome or post-change fields must not enter model-facing text. This includes `gold_*`, `human_label_notes`, `suggested_*`, `docs_after_excerpt`, `docs_diff_excerpt`, `docs_changed_files`, source URLs and PR titles.
- Development model selection uses only `development_train` and `development_validation`.
- Confirmation is sealed until Gate 5 and must be used only once for the final frozen configuration.
- Historical experiments may remain as evidence, but the canonical artifact map controls which paths are allowed in the final experiment.
- Later gates must fail closed rather than silently repairing labels, partitions, manifests or model choices.

## Gate 0 — Canonical pipeline and integrity baseline

Purpose: establish repository truth, canonical artifacts and contamination protection.

Required inputs:

- repository working tree;
- Final V2 scripts, configs, manifests, tests and reports;
- current canonical artifact map;
- current finalization state file.

Required outputs:

- `reports/final_v2/FINALIZATION_PROTOCOL.md`;
- `reports/final_v2/CANONICAL_ARTIFACT_MAP.md`;
- `reports/final_v2/finalization_state.json`;
- passing pre-experiment audit;
- passing relevant non-confirmation tests.

PASS conditions:

- canonical Final V2 paths are identified;
- historical/deprecated paths are classified;
- confirmation remains sealed;
- this gate does not access confirmation results for model selection;
- pre-experiment audit status is `PASS`;
- relevant non-confirmation tests pass;
- no ambiguous competing artifact is allowed to feed the current final experiment.

Immutable after PASS:

- the gate ordering;
- the canonical artifact map unless superseded by a later explicit gate decision;
- the rule that later gates may not silently revise completed gates.

Current Gate 0 status: `PASS`.

## Gate 1 — Human-gold dataset freeze

Purpose: finalize Natural Diversity / human-reviewed gold and permanently freeze the exact dataset used for model research.

Required inputs:

- canonical consolidated reviewed corpus;
- canonical split files;
- canonical repository partition manifest;
- human-review completion/audit evidence;
- source-provenance manifest.

Required outputs:

- immutable human-gold manifest;
- immutable train/validation/confirmation split hashes;
- explicit confirmation-sealed statement;
- repository-disjointness proof;
- review-completion proof.

PASS conditions:

- review complete;
- taxonomy valid;
- all rows approved or explicitly excluded before freeze;
- no duplicate `case_id`;
- no duplicate repository/PR key;
- no repository overlap across train/validation/confirmation;
- controlled augmentation rows are development-train-only;
- confirmation case IDs and repositories remain sealed;
- hashes match the frozen manifest.

Immutable after PASS:

- gold labels;
- dataset membership;
- train/validation/confirmation assignment;
- row ordering and hashes;
- canonical dataset paths.

Do not execute Gate 1 inside Gate 0.

## Gate 2 — Development-only ML model study

Purpose: conduct or document development-only classifier experimentation using only train and validation data.

Required inputs:

- Gate 1 frozen dataset;
- predeclared model/config search space;
- safe feature contract.

Required outputs:

- development-only training summaries;
- development-only model comparisons;
- development-only figures;
- leakage audit evidence.

PASS conditions:

- no confirmation data or metrics are read;
- model selection uses only development validation;
- safe feature contract is enforced;
- selected model and threshold criteria are documented.

Immutable after PASS:

- development model-selection evidence;
- selected candidate family for final freeze unless Gate 3 explicitly rejects it before confirmation.

Do not execute Gate 2 inside Gate 0.

## Gate 3 — Final classifier selection and freeze

Purpose: select Binary and Category models using only predeclared development criteria, train/finalize development models, calibrate/select threshold where applicable, freeze artifacts and forbid post-confirmation tuning.

Required inputs:

- Gate 1 frozen dataset;
- Gate 2 development-only results;
- binary/category configs;
- selected development model artifacts.

Required outputs:

- binary model freeze manifest;
- category model freeze manifest;
- hashes for model files, configs, training summaries and splits;
- explicit `confirmation_accessed=false` in freeze manifests.

PASS conditions:

- model file hash matches freeze manifest;
- config hash matches freeze manifest;
- train/validation split hashes match freeze manifest;
- selected model/threshold came from development-only evidence;
- no confirmation data or metrics were used.

Immutable after PASS:

- final binary/category model files;
- final thresholds and labels;
- freeze manifests;
- model-selection summaries used for thesis reporting.

Do not execute Gate 3 inside Gate 0.

## Gate 4 — Stage 3 retrieval/generation study and freeze

Purpose: finalize retrieval and generation configuration using development-only evidence, then freeze Stage 3.

Required inputs:

- frozen classifier artifacts from Gate 3;
- Stage 3 config;
- prompt/template source files;
- development-only Stage 3 validation evidence.

Required outputs:

- Stage 3 freeze manifest;
- config hash;
- prompt/template/source hashes;
- declared generation settings;
- explicit statement that the frozen Stage 3 path has not used confirmation.

PASS conditions:

- Stage 3 config and source hashes are captured;
- no confirmation generation has run;
- no prompt/model choice changes are made using confirmation evidence;
- generation/retrieval behavior is fully reproducible from frozen inputs.

Immutable after PASS:

- Stage 3 config;
- prompt templates;
- retrieval/generation route;
- source hashes used for final confirmation.

Do not execute Gate 4 inside Gate 0.

## Gate 5 — One-shot confirmation

Purpose: run the final frozen binary, category and Stage 3 systems on sealed confirmation exactly once.

Required inputs:

- Gate 1 frozen confirmation split;
- Gate 3 frozen classifiers;
- Gate 4 frozen Stage 3;
- one-shot output directories with receipt enforcement.

Required outputs:

- confirmation predictions;
- confirmation metrics;
- Stage 3 confirmation generation outputs;
- one-shot receipts;
- final confirmation report.

PASS conditions:

- all freeze manifests validate before running;
- confirmation partition manifest has `confirmation_sealed=true`;
- every evaluated row belongs to the confirmation partition;
- one-shot receipts are written;
- no post-confirmation model, threshold, prompt or label change occurs.

Immutable after PASS:

- confirmation metrics;
- confirmation predictions;
- Stage 3 confirmation generations;
- one-shot receipts.

Do not execute Gate 5 inside Gate 0.

## Gate 6 — Post-hoc and human evaluation

Purpose: perform post-hoc reference evaluation and blind human quality evaluation after confirmation outputs exist.

Required inputs:

- Gate 5 immutable confirmation outputs;
- predeclared reference-evaluation scripts;
- blind human-review forms/sheets, where applicable.

Required outputs:

- post-hoc reference metrics;
- human quality review exports;
- aggregation receipts and reports.

PASS conditions:

- evaluation inputs match Gate 5 hashes;
- human review does not feed back into model selection;
- post-hoc findings are reported as evaluation, not tuning.

Immutable after PASS:

- human evaluation exports;
- post-hoc reference metrics;
- aggregation receipts.

Do not execute Gate 6 inside Gate 0.

## Gate 7 — Thesis evidence freeze

Purpose: freeze final tables, figures, metrics, manifests, thesis-facing reports and reproducibility evidence.

Required inputs:

- all previous gate manifests and reports;
- final thesis-facing result tables and figures;
- reproducibility instructions.

Required outputs:

- final evidence manifest;
- final thesis figures/tables;
- final reproducibility report;
- final Git commit SHA.

PASS conditions:

- all upstream gate hashes match;
- no unresolved blocker remains;
- all thesis-facing metrics trace to immutable artifacts;
- repository state is clean except intentionally documented external/local-only paths.

Immutable after PASS:

- thesis-facing final results;
- final figures/tables;
- final evidence manifest.

Do not execute Gate 7 inside Gate 0.

## Current Gate 0 audit summary

- Canonical reviewed corpus: `data/final_v2/human_review/consolidated_enriched_training_v2/consolidated_human_review.jsonl`.
- Canonical gold dataset: `experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl`.
- Canonical partition manifest: `data/final_v2/partitions/canonical_repository_partitions/repository_partition_manifest.json`.
- Confirmation is sealed in the canonical partition manifest.
- This Gate 0 task did not run confirmation evaluation and did not access confirmation result metrics or prediction files.
- Pre-experiment audit: `PASS`, 15 checks.
- Relevant non-confirmation tests: 122 passed, 0 failed, 30 warnings.
- Current blocker for moving directly to confirmation: classifier and Stage 3 freeze manifests are not yet present; Gates 1, 3 and 4 must be formally completed before Gate 5.
