# DocGuard Real GitHub PR Candidate Dataset Builder Report

This report describes a real public GitHub PR candidate dataset created for later manual validation.
The builder does not assign final gold labels and does not use synthetic data.

- Seed input: `data\external\project_case_study\pr_candidate_seeds_collected_v1.jsonl`
- Candidate output: `data\external\project_case_study\real_pr_candidates_collected_v1.jsonl`
- Accepted candidate records: `1`
- Rejected seed records: `29`

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

- Candidate type counts: `{'code_and_docs_changed_needs_manual_validation': 1}`
- Language counts: `{'typescript': 1}`
- Label confidence counts: `{'needs_manual_review': 1}`

## Accepted Candidates

| Case | Repository | PR | Language | Code files | Docs files | Candidate type | Title |
| --- | --- | ---: | --- | ---: | ---: | --- | --- |
| `GH-CAND-0001` | `ragpark/controltower` | `14` | `typescript` | `15` | `1` | `code_and_docs_changed_needs_manual_validation` | ENG-1102, ENG-1104: Duplicate order diagnostics and resolution |

## Rejected Seeds

| Case | Repository | PR | Reason |
| --- | --- | ---: | --- |
| `GH-CAND-0002` | `ragpark/controltower` | `6` | `github_fetch_failed` |
| `GH-CAND-0003` | `ragpark/controltower` | `5` | `github_fetch_failed` |
| `GH-CAND-0004` | `ragpark/controltower` | `4` | `github_fetch_failed` |
| `GH-CAND-0005` | `ragpark/controltower` | `3` | `github_fetch_failed` |
| `GH-CAND-0006` | `ragpark/controltower` | `2` | `github_fetch_failed` |
| `GH-CAND-0007` | `d-hinders/Haven-AI` | `1783` | `github_fetch_failed` |
| `GH-CAND-0008` | `d-hinders/Haven-AI` | `1782` | `github_fetch_failed` |
| `GH-CAND-0009` | `d-hinders/Haven-AI` | `1781` | `github_fetch_failed` |
| `GH-CAND-0010` | `d-hinders/Haven-AI` | `1780` | `github_fetch_failed` |
| `GH-CAND-0011` | `d-hinders/Haven-AI` | `1778` | `github_fetch_failed` |
| `GH-CAND-0012` | `d-hinders/Haven-AI` | `1775` | `github_fetch_failed` |
| `GH-CAND-0013` | `d-hinders/Haven-AI` | `1776` | `github_fetch_failed` |
| `GH-CAND-0014` | `d-hinders/Haven-AI` | `1770` | `github_fetch_failed` |
| `GH-CAND-0015` | `d-hinders/Haven-AI` | `1769` | `github_fetch_failed` |
| `GH-CAND-0016` | `d-hinders/Haven-AI` | `1765` | `github_fetch_failed` |
| `GH-CAND-0017` | `eclipsefdn-ai-registry/ai-registry-core` | `88` | `github_fetch_failed` |
| `GH-CAND-0018` | `eclipsefdn-ai-registry/ai-registry-core` | `87` | `github_fetch_failed` |
| `GH-CAND-0019` | `eclipsefdn-ai-registry/ai-registry-core` | `85` | `github_fetch_failed` |
| `GH-CAND-0020` | `eclipsefdn-ai-registry/ai-registry-core` | `78` | `github_fetch_failed` |
| `GH-CAND-0021` | `eclipsefdn-ai-registry/ai-registry-core` | `69` | `github_fetch_failed` |
| `GH-CAND-0022` | `eclipsefdn-ai-registry/ai-registry-core` | `72` | `github_fetch_failed` |
| `GH-CAND-0023` | `eclipsefdn-ai-registry/ai-registry-core` | `70` | `github_fetch_failed` |
| `GH-CAND-0024` | `eclipsefdn-ai-registry/ai-registry-core` | `63` | `github_fetch_failed` |
| `GH-CAND-0025` | `eclipsefdn-ai-registry/ai-registry-core` | `64` | `github_fetch_failed` |
| `GH-CAND-0026` | `eclipsefdn-ai-registry/ai-registry-core` | `62` | `github_fetch_failed` |
| `GH-CAND-0027` | `torbido-hq/cicerone` | `112` | `github_fetch_failed` |
| `GH-CAND-0028` | `torbido-hq/cicerone` | `107` | `github_fetch_failed` |
| `GH-CAND-0029` | `torbido-hq/cicerone` | `97` | `github_fetch_failed` |
| `GH-CAND-0030` | `torbido-hq/cicerone` | `101` | `github_fetch_failed` |

## Interpretation Boundary

- This is a dataset construction step, not a model result.
- Candidate labels are intentionally left as `needs_manual_review`.
- Documentation-after text and documentation-file changes are stored only for audit/labeling.
- Model-facing evaluation scripts must use only `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`.