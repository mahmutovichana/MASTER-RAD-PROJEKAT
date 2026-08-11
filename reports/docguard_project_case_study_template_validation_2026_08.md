# DocGuard Project Case Study Template Validation 2026-08

- Input: `data\external\project_case_study\manual_cases_template.jsonl`
- Status: `ok`
- Records checked: `4`
- Change type distribution: `{'api_endpoint_change': 1, 'validation_change': 1, 'testing_command_change': 1, 'internal_refactor_no_docs_needed': 1}`
- Label distribution: `{'True': 3, 'False': 1}`

## Leakage Policy

- Allowed model input fields: `['change_type', 'changed_files', 'code_diff_excerpt', 'docs_before_excerpt', 'language']`
- Audit-only fields: `['docs_after_excerpt', 'gold_doc_category', 'gold_docs_update_required', 'gold_patch_summary', 'gold_target_doc_file', 'gold_target_section', 'label_confidence', 'manual_label_notes']`

## Errors

No validation errors found.
