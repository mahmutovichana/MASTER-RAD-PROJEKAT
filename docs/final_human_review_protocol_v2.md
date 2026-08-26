# Final V2 Human Review Protocol

Final V2 gold labels require manual review for every included primary-label row. Automated prefill is only a reviewer aid and never becomes ground truth unless a human explicitly fills the human fields.

## Batch Workflow

`scripts/build_human_review_batches_v2.py` converts a prefilled review JSONL into deterministic review batches. Each batch is written as JSONL and CSV for practical review in Excel or similar tools. Default batch size is 500.

Reviewer-facing files include:

- `case_id`
- `repository`
- `pr_number`
- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`
- `suggested_docs_update_required`
- `suggested_doc_category`
- `suggested_notes`
- blank `human_docs_update_required`
- blank `human_doc_category`
- blank `human_label_notes`
- `review_status`

Suggested fields are prefixed with `suggested_`. Human fields start empty and must be filled manually.

## Taxonomy

Allowed final categories are:

- `api_reference`
- `configuration`
- `developer_setup`
- `model_contract`
- `other_documentation`
- `no_update`

If `human_docs_update_required` is false, `human_doc_category` must be `no_update`. If true, the category must be one of the positive categories. No aliases or forced conversions are allowed.

## Integrity Hashes

Every review row contains `review_row_hash`, computed from immutable evidence only:

- `case_id`
- `repository`
- `pr_number`
- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

Human fields and suggested fields are excluded from the hash. If immutable evidence changes during review/import, the row is rejected as an integrity conflict.

## Partition Blinding

If a repository partition manifest is supplied during batch construction, it is recorded only for audit provenance. Reviewer-facing CSV/JSONL files do not expose `development_train`, `development_validation`, or `confirmation`.

Partitions are restored later by the finalizer from the frozen partition manifest.

## Merge And Progress

`scripts/merge_human_review_batches_v2.py` imports reviewed CSV/JSONL batches and detects duplicate cases, conflicting labels, invalid taxonomy, pending rows, missing human fields, and modified immutable evidence. It never chooses a winner silently.

`scripts/report_human_review_progress_v2.py` reports review completion counts only. It is not model evaluation and does not report training or confirmation performance.

## Second Reviewer And Adjudication

`scripts/build_second_reviewer_subset_v2.py` creates a deterministic blind subset for inter-annotator reliability. It does not sample based on human labels, suggested labels, model predictions, difficulty, or model errors.

`scripts/compare_human_gold_reviewers_v2.py` reports agreement and kappa for overlapping approved rows. Disagreements are not automatically applied to final labels.

`scripts/build_human_review_adjudication_v2.py` creates a human-only adjudication sheet with empty adjudicated fields. No automated adjudication is performed.

## Completion Audit

`scripts/audit_human_review_complete_v2.py` must pass before final gold finalization. It asserts that every included row is approved, human fields are explicitly populated, review hashes are valid, duplicate cases are absent, conflicts are resolved, and taxonomy is valid.

Only after this audit can `scripts/finalize_human_gold_v2.py` set:

```json
{
  "label_source": "human_reviewed_final_v2",
  "human_review_complete": true
}
```
