# DocGuard Project Case Study Template Validation 2026-08

- Input: `data\external\project_case_study\manual_cases_template.jsonl`
- Status: `ok`
- Records checked: `4`
- Change type distribution: `{'api_endpoint_change': 1, 'validation_change': 1, 'testing_command_change': 1, 'internal_refactor_no_docs_needed': 1}`
- Label distribution: `{'True': 3, 'False': 1}`

## Leakage Policy

- Allowed model input fields: `['code_changed_files', 'code_diff_excerpt', 'docs_before_excerpt', 'language']`
- Audit-only fields: `['change_type', 'changed_files', 'docs_after_excerpt', 'docs_changed_files', 'gold_doc_category', 'gold_docs_update_required', 'gold_patch_summary', 'gold_target_doc_file', 'gold_target_section', 'label_confidence', 'manual_label_notes']`
- Documentation file policy: docs_changed_files and changed_files are audit-only; code_changed_files is the only file-list input allowed for future runners.

## Errors

No validation errors found.
