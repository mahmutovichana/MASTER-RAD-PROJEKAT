# External Deep-JIT Validation Threshold Tuning 2026-08

- Model: `tfidf_linear_svc`
- Input mode: `old_comment_plus_code_diff`
- Score rule: LinearSVC positive-class decision margin; not calibrated probability
- Selection rule: choose threshold on validation by balanced accuracy, with F1 as tie-breaker.
- Selected validation threshold: `0.00`
- Test set is used once after threshold selection; no threshold is tuned on test.

## Validation Sweep

| Threshold | Pred + | Pred - | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| -1.00 | 2430 | 200 | 1292 | 1138 | 177 | 23 | 55.86% | 53.17% | 98.25% | 69.00% | 86.54% | 13.46% | 55.86% | 0.2209 |
| -0.75 | 2212 | 418 | 1259 | 953 | 362 | 56 | 61.63% | 56.92% | 95.74% | 71.39% | 72.47% | 27.53% | 61.63% | 0.3182 |
| -0.50 | 1913 | 717 | 1195 | 718 | 597 | 120 | 68.14% | 62.47% | 90.87% | 74.04% | 54.60% | 45.40% | 68.14% | 0.4073 |
| -0.25 | 1540 | 1090 | 1070 | 470 | 845 | 245 | 72.81% | 69.48% | 81.37% | 74.96% | 35.74% | 64.26% | 72.81% | 0.4631 |
| 0.00 | 1180 | 1450 | 911 | 269 | 1046 | 404 | 74.41% | 77.20% | 69.28% | 73.03% | 20.46% | 79.54% | 74.41% | 0.4908 |
| 0.25 | 873 | 1757 | 737 | 136 | 1179 | 578 | 72.85% | 84.42% | 56.05% | 67.37% | 10.34% | 89.66% | 72.85% | 0.4853 |
| 0.50 | 626 | 2004 | 578 | 48 | 1267 | 737 | 70.15% | 92.33% | 43.95% | 59.56% | 3.65% | 96.35% | 70.15% | 0.4732 |
| 0.75 | 452 | 2178 | 439 | 13 | 1302 | 876 | 66.20% | 97.12% | 33.38% | 49.69% | 0.99% | 99.01% | 66.20% | 0.4293 |
| 1.00 | 304 | 2326 | 303 | 1 | 1314 | 1012 | 61.48% | 99.67% | 23.04% | 37.43% | 0.08% | 99.92% | 61.48% | 0.3591 |

## Test Result At Validation-Selected Threshold

| Threshold | Pred + | Pred - | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00 | 1267 | 1639 | 872 | 395 | 1058 | 581 | 66.41% | 68.82% | 60.01% | 64.12% | 27.19% | 72.81% | 66.41% | 0.3310 |

## Interpretation

Threshold tuning is diagnostic because the score is not calibrated as a production probability. It is still useful for showing whether validation-set thresholding can trade recall for specificity without touching test labels.
