# DocGuard Real Dataset Split Report

- Input: `data\external\project_case_study\real_pr_labeling_pack_collected_v1.jsonl`
- Output directory: `reports\real_case_study\splits_collected_v1`
- Split strategy: `repository_group`
- Split seed: `42`
- Total records: `30`
- Repository overlap: `False`

## Split Summary

| Split | Records | Repositories | Languages | Candidate types | Label confidence |
| --- | ---: | --- | --- | --- | --- |
| `train` | `20` | `{'eclipsefdn-ai-registry/ai-registry-core': 10, 'd-hinders/Haven-AI': 10}` | `{'typescript': 20}` | `{'code_only_needs_manual_validation': 4, 'code_and_docs_changed_needs_manual_validation': 16}` | `{'needs_manual_review': 20}` |
| `validation` | `4` | `{'torbido-hq/cicerone': 4}` | `{'python': 4}` | `{'code_and_docs_changed_needs_manual_validation': 4}` | `{'needs_manual_review': 4}` |
| `locked_test` | `6` | `{'ragpark/controltower': 6}` | `{'typescript': 6}` | `{'code_and_docs_changed_needs_manual_validation': 3, 'code_only_needs_manual_validation': 3}` | `{'needs_manual_review': 6}` |

## Repository Overlap

```json
{
  "has_repository_overlap": false,
  "overlaps": []
}
```

## Interpretation Boundary

- This script does not assign labels.
- For final model training/evaluation, use only high-confidence gold-labeled records.
- Repository-group split is preferred for the final locked test because it reduces repository-pattern leakage.
- Random split may be used only for quick development diagnostics.