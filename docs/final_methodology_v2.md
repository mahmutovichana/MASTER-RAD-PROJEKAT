# DocGuard Final Dataset Methodology V2

Final V2 defines the thesis-safe data protocol for DocGuard real-project evaluation and training data preparation.

## Canonical Sequence

Final V2 must be built in this order:

real PR collection -> leak-free candidate builder V2 -> repository partition freeze -> prefilled human review -> full manual approval -> gold finalization -> merge with existing fully-human-reviewed data -> development model training -> model freeze -> one-time confirmation evaluation.

Training and model selection may use only `development_train` and `development_validation`. The `confirmation` repository partition is fixed before training, sealed, and evaluated once after final model freeze.

## Label Provenance

Final gold labels are produced only by full human review:

Candidate collection -> automated suggestion/prefill -> full human review -> approved human label -> final gold dataset.

Automated prefill is workflow assistance only. It may suggest likely documentation-update decisions and likely categories, but it is never ground truth and is never copied into gold fields unless a human reviewer explicitly approves the decision through the reviewed human fields.

Every finalized row must contain:

```json
{
  "label_source": "human_reviewed_final_v2",
  "human_review_complete": true
}
```

## Human Review Fields

Prefill files keep human fields empty until review:

- `review_status`: one of `pending`, `approved`, `exclude`
- `human_docs_update_required`: boolean, filled by the reviewer
- `human_doc_category`: one of the allowed final categories
- `human_label_notes`: reviewer rationale or notes

Rows are finalized only when `review_status` is `approved`.

## Audit Metadata

The following fields are audit metadata only and must never be used as model input:

- `source_url`
- `pr_title`
- `docs_changed_files`
- `docs_diff_excerpt`
- `docs_after_excerpt`
- any `suggested_*` field
- human review notes
- gold labels
- `docs_before_retrieval_policy`
- `docs_before_retrieved_files`

Safe model fields are:

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

## Final Category Policy

No post-hoc category aliases are permitted in Final V2.

Allowed primary Stage-2 classes:

- `api_reference`
- `configuration`
- `developer_setup`
- `model_contract`

Additional categories:

- `other_documentation`: positive binary row, excluded from primary four-class Stage-2 training, counted as Stage-2 coverage outside the primary classes
- `no_update`: binary negative row, never category-training input

Target classes are never resampled or balanced. Binary and category classifiers inherit one canonical repository partition.

## Repository Partitioning

Final V2 uses one canonical repository partition manifest. The same repository can never appear in more than one partition. Confirmation repositories must be completely repository-disjoint from training, validation, and any previously seen datasets supplied to the partition builder.

The manifest must include:

```json
{
  "confirmation_sealed": true
}
```

The confirmation set is not exposed to training or model-selection scripts. Model development sees only `development_train` and `development_validation`. Confirmation is evaluated once after final freeze. Confirmation repositories must be absent from all historical DocGuard datasets used in prior experiments.

Development repositories are split into `development_train` and `development_validation` by repository identity. Binary and category datasets inherit the same repository partition and must not create their own split logic.

All random or stable decisions record the seed. JSON and JSONL outputs are UTF-8 without BOM.

## Final V2.1 Acquisition Policy

Final acquisition is repository-diversity oriented. If the current repository universe cannot satisfy the requested total size or language coverage, the correct response is to expand the repository universe, not to deepen a small number of repositories indefinitely.

Language coverage constraints are permitted because language is a pre-existing input/domain property, not a target label. Repository discovery, shard collection, seed merging, repository partitioning, and optional repository-level caps all occur before human labels are created.

No target-label balancing is used at acquisition time or dataset construction time:

NO CLASS BALANCING / OVERSAMPLING / UNDERSAMPLING / SMOTE.

Raw acquisition shards are immutable and retained for audit. Additional collection is performed as separate shards. Shards are merged with deterministic de-duplication by repository plus PR number and source URL before candidate building.

The existing first large acquisition shard is documented as `acquisition_shard_A_existing_universe`: it collected 5619 seeds from the initial 191-repository universe but did not satisfy the requested 18000 total / 6000 Python coverage target. It must remain unchanged and reusable as shard A.

Final V2 GitHub acquisition uses authenticated, serial GitHub API access. Final collection commands should include:

- `--require-authenticated`
- `--min-request-interval-seconds 0.25`

The collector applies request-level pacing before every uncached outbound GitHub HTTP request. Cache hits do not count as outbound requests and do not trigger pacing. The older `--sleep-seconds` option is retained for backward compatibility only; Final V2 relies on request-level pacing.

Collection stops safely on GitHub primary rate limits, secondary/abuse rate limits, and authentication failures. These API failures are operational acquisition states, not dataset labels. Already collected seeds are preserved in immutable shard outputs, and partial shards are explicitly reported as `status = partial`.

Final V2 does not use concurrency for GitHub acquisition and does not increase `max-prs-per-repository` solely to reach dataset size. Repository diversity should be increased by expanding the repository universe before collecting additional shards.

## Leak-Free Candidate Builder V2

Candidate construction does not emit any `gold_*` field. Case identity is stable for each GitHub PR and is derived from normalized repository identity plus PR number. Candidate records may include only safe model inputs and audit context.

`docs_before_excerpt` must be retrieved from the base commit only. The retrieval policy may use repository identity, `base_sha`, code changed files, code diff excerpt, and neutral documentation files existing in the base commit. It must not prioritize documentation because it was later changed by the PR. In particular, `docs_changed_files`, `docs_diff_excerpt`, `docs_after_excerpt`, head/outcome documentation text, gold labels, human labels, and suggested labels must not influence `docs_before_excerpt`.

Each candidate row records:

- `docs_before_retrieval_policy`
- `docs_before_retrieved_files`

These fields are audit-only provenance, not model input.

## Final Stage 3 V2: Semantic Documentation Generation

Final V2 separates the thesis flow into three stages:

1. Stage 1 predicts whether a documentation update is required.
2. Stage 2 predicts the broad documentation category for positive cases.
3. Stage 3 V2 generates the documentation patch with a semantic LLM pipeline.

Stage 3 V2 does not route a category to a hard-coded documentation file and does not use deterministic documentation prose as a final fallback. It analyzes the code change, validates exact evidence quotes, retrieves candidate documentation from pre-change documentation context, asks the LLM to write developer-facing documentation, checks provenance safety, and allows one LLM repair attempt.

If the LLM patch cannot pass the safety verifier after one repair attempt, the final output is `human_review_required`. The old grounded/hybrid patch-generation work remains historical Stage 3 V1 evidence and must be reported as an earlier prototype, not as the Final V2 generation method.

## Final Classifier Infrastructure

Final Binary V4 and Final Category V8 inherit the canonical Final V2 repository partitions. Their training scripts accept only `development_train` and `development_validation`; confirmation evaluation is isolated in separate scripts that require a freeze manifest.

Both classifiers use the same shared safe-input serializer:

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

Binary V4 preserves natural class imbalance and treats `other_documentation` as binary positive. Category V8 trains only on exact primary Stage-2 labels: `api_reference`, `configuration`, `developer_setup`, and `model_contract`. `other_documentation` remains part of the dataset taxonomy but is excluded from primary four-class Stage-2 training and reported through Stage-2 coverage.

## Final Stage 3 Evaluation

Final Stage 3 V2 evaluation separates safety/provenance validation from documentation quality. The safety verifier is not the final quality metric. Final quality evidence comes from blind human review, with post-hoc reference comparison used only as supporting diagnostics where real documentation changes are available.

The primary Stage 3 confirmation sample is a natural-distribution random predicted-positive sample. A category-stratified stress sample may be reported as supplementary only. One-shot confirmation aggregation requires a Stage 3 freeze manifest and writes a separate evaluation receipt.

Historical Qwen100 results are retained as V1 internal verifier acceptance rates: grounded 76%, Qwen 67%, and hybrid cascade 87%. These are not accuracy, not human quality, and not Final V2 performance.

## Large-Scale Human Review Workflow

Final V2 human labeling is batched, resumable, and integrity-checked. Automated prefill suggestions remain reviewer assistance only; suggested fields are never copied into gold labels automatically. Reviewer-facing batches hide repository partitions and include deterministic `review_row_hash` values over immutable evidence so accidental evidence edits are detected during merge and completion audit.

The final gold finalizer can assign `label_source = human_reviewed_final_v2` only for approved rows with explicit human fields and valid taxonomy. Second-reviewer subsets and adjudication sheets support reliability analysis, but disagreements require explicit human adjudication and never overwrite primary labels automatically.
