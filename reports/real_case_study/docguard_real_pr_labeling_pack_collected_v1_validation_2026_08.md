# DocGuard Real Dataset Validation Report

- Input: `data\external\project_case_study\real_pr_labeling_pack_collected_v1.jsonl`
- Status: `ok`
- Records: `30`
- Error count: `0`
- Warning count: `0`

## Leakage Boundary

Allowed model input fields:

- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`
- `language`

Audit-only fields:

- `allowed_model_input_fields`
- `audit_labeling_context`
- `audit_only_fields`
- `base_sha`
- `candidate_evidence`
- `changed_files`
- `docs_after_excerpt`
- `docs_changed_files`
- `docs_diff_excerpt`
- `gold_doc_category`
- `gold_docs_update_required`
- `gold_label_to_fill`
- `gold_patch_summary`
- `gold_target_doc_file`
- `gold_target_section`
- `head_sha`
- `label_confidence`
- `labeling_guidance`
- `manual_label_notes`
- `merged_at`
- `pr_number`
- `pr_state`
- `pr_title`
- `repository`
- `source_url`

## Distribution Summary

- Language counts: `{'typescript': 26, 'python': 4}`
- Label confidence counts: `{'needs_manual_review': 30}`
- Gold label counts: `{'None': 30}`
- Gold category counts: `{'None': 30}`
- Repository counts: `{'ragpark/controltower': 6, 'd-hinders/Haven-AI': 10, 'eclipsefdn-ai-registry/ai-registry-core': 10, 'torbido-hq/cicerone': 4}`

## Errors

- None

## Warnings

- None

## Interpretation Boundary

- This validator does not assign labels.
- It checks dataset structure, leakage safety, basic label consistency, and reporting readiness.
- `docs_after_excerpt`, gold fields, source URL, docs-changed files, and manual notes must remain outside model input.