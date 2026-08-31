# Authoritative review output

The authoritative outputs from the from-scratch review are:

- `reviewed_2323.jsonl` — all 2,323 rows in original order
- `positive_reviewed.jsonl` — only rows labeled `human_docs_update_required=true`
- `excluded_reviewed.jsonl` — rows excluded for insufficient evidence
- `reviewed_batches/batch_001.jsonl`–`batch_024.jsonl` — 100 rows per batch, final batch 23 rows
- `review_manifest.json` — counts, hashes, and method
- `review_report.md` — concise report
- `decision_samples.jsonl` — compact audit sample

The older CSV batch files were moved to the sibling folder
`legacy_non_authoritative_csv_batches` and are not part of this review. Do not use
those legacy files for training or merging.
