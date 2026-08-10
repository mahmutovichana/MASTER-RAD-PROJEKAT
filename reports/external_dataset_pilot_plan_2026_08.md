# External Dataset Pilot Plan 2026-08

## Pilot Goal

Map 100-500 records from CoDocBench, or another selected external dataset, into the normalized DocGuard external schema.

## Pilot Outputs

- `data/external/codocbench_sample.jsonl`
- `reports/external_codocbench_sample_audit.md`
- `reports/external_codocbench_label_quality_notes.md`

## Pilot Questions

- Can the dataset provide `code_diff`?
- Can it provide documentation/comment before and after?
- Can we create positive examples reliably?
- Can we create negative examples safely?
- Does the task map to binary `docs_update_required`?
- Does the task map to project-level `doc_category`, or only to comment/docstring update?
- Are patches available, or must they be reconstructed from `doc_before`/`doc_after`?
- Which labels are strong and which are weak?

## Proposed Pilot Process

1. Inspect CoDocBench release file structure and license.
2. Select 100-500 records without downloading the full dataset if possible.
3. Convert records into `ExternalDocGuardRecord`.
4. Validate schema and label provenance.
5. Produce sample audit and label-quality notes.
6. Run only binary update detection first.

