# External Positive vs Synthetic Negative Sanity 2026-08

| Dataset | Label type | Input mode | Total records | Predicted update-required | Recall or negative accuracy | False negatives or false positives | Median confidence | Low confidence <0.25 | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| CoDocBench | external strong positives | `code_diff_only` | 500 | 500 | 100.00% | 0 false negatives | 0.1204 | 479 | positive recall only |
| CoDocBench | external strong positives | `code_diff_plus_doc_before` | 500 | 499 | 99.80% | 1 false negatives | 0.1245 | 473 | positive recall only |
| Synthetic v0.4 | synthetic negatives sanity control | `code_diff_only` | 500 | 0 | 100.00% | 0 false positives | 0.1360 | 270 | constant-positive sanity check, not external F1 |
| Synthetic v0.4 | synthetic negatives sanity control | `code_diff_plus_doc_before` | 500 | 0 | 100.00% | 0 false positives | 0.1325 | 270 | constant-positive sanity check, not external F1 |

This table does not report final external F1. It checks whether the current predictor behaves as a constant-positive classifier when confronted with known synthetic no-update examples.
