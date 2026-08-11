# External Deep-JIT Validation Strategy Comparison 2026-08

## Compared Setups

| Setup | Validation composition | Best model | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Previous Return-only validation | Return valid only | `tfidf_logreg + old_comment_plus_code_diff` | 68.72% | 73.41% | 58.71% | 65.24% | 21.27% | 78.73% | 68.72% | 0.3821 |
| Combined validation robustness | Return valid + deterministic Summary train carve-out | `tfidf_linear_svc + old_comment_plus_code_diff` | 66.41% | 68.82% | 60.01% | 64.12% | 27.19% | 72.81% | 66.41% | 0.3310 |

## Interpretation

Model choice changed. This indicates the earlier Return-only validation setup was sensitive to subset composition and the combined-validation result should be preferred.

The old Return-only validation result should be kept as a historical baseline. The combined-validation setup should become the cleaner thesis result because it includes Summary examples during validation while keeping Summary test untouched.

## Combined-Validation Threshold Result

- Selected threshold: `0.00`
- Test accuracy: `66.41%`
- Test precision: `68.82%`
- Test recall: `60.01%`
- Test F1: `64.12%`
- Test FPR: `27.19%`
- Test specificity: `72.81%`
- Test MCC: `0.3310`
