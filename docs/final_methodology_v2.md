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

## Leak-Free Candidate Builder V2

Candidate construction does not emit any `gold_*` field. Case identity is stable for each GitHub PR and is derived from normalized repository identity plus PR number. Candidate records may include only safe model inputs and audit context.

`docs_before_excerpt` must be retrieved from the base commit only. The retrieval policy may use repository identity, `base_sha`, code changed files, code diff excerpt, and neutral documentation files existing in the base commit. It must not prioritize documentation because it was later changed by the PR. In particular, `docs_changed_files`, `docs_diff_excerpt`, `docs_after_excerpt`, head/outcome documentation text, gold labels, human labels, and suggested labels must not influence `docs_before_excerpt`.

Each candidate row records:

- `docs_before_retrieval_policy`
- `docs_before_retrieved_files`

These fields are audit-only provenance, not model input.
