# DocGuard Real GitHub PR Candidate Dataset Builder Report

This report describes a real public GitHub PR candidate dataset created for later manual validation.
The builder does not assign final gold labels and does not use synthetic data.

- Seed input: `data\external\project_case_study\pr_candidate_seeds.example.jsonl`
- Candidate output: `data\external\project_case_study\real_pr_candidates_v1.jsonl`
- Accepted candidate records: `3`
- Rejected seed records: `0`

## Leakage Policy

Allowed model input fields:

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

Audit-only fields:

- `source_url`
- `repository`
- `pr_number`
- `pr_title`
- `pr_state`
- `merged_at`
- `base_sha`
- `head_sha`
- `changed_files`
- `docs_changed_files`
- `docs_diff_excerpt`
- `docs_after_excerpt`
- `gold_docs_update_required`
- `gold_doc_category`
- `gold_target_doc_file`
- `gold_target_section`
- `gold_patch_summary`
- `label_confidence`
- `manual_label_notes`
- `candidate_evidence`

## Candidate Counts

- Candidate type counts: `{'code_and_docs_changed_needs_manual_validation': 3}`
- Language counts: `{'typescript': 3}`
- Label confidence counts: `{'needs_manual_review': 3}`

## Accepted Candidates

| Case | Repository | PR | Language | Code files | Docs files | Candidate type | Title |
| --- | --- | ---: | --- | ---: | ---: | --- | --- |
| `GH-CAND-0001` | `ragpark/controltower` | `2` | `typescript` | `25` | `5` | `code_and_docs_changed_needs_manual_validation` | Align ingestion to the ActiveHub export schema and fix container/mapping defects |
| `GH-CAND-0002` | `d-hinders/Haven-AI` | `1314` | `typescript` | `4` | `4` | `code_and_docs_changed_needs_manual_validation` | feat(mcp+sdk): structured next_action/agent_summary/warnings contract (#1308) |
| `GH-CAND-0003` | `eclipsefdn-ai-registry/ai-registry-core` | `79` | `typescript` | `23` | `3` | `code_and_docs_changed_needs_manual_validation` | Add Agent Plugin (agent-plugins.org) as a fourth artifact type |

## Interpretation Boundary

- This is a dataset construction step, not a model result.
- Candidate labels are intentionally left as `needs_manual_review`.
- Documentation-after text and documentation-file changes are stored only for audit/labeling.
- Model-facing evaluation scripts must use only `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`.