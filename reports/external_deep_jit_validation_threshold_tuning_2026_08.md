# External Deep-JIT Validation Threshold Tuning 2026-08

- Model: `tfidf_logreg`
- Input mode: `old_comment_plus_code_diff`
- Score rule: positive-class LogisticRegression probability; not externally calibrated
- Selection rule: choose threshold on validation by balanced accuracy, with F1 as tie-breaker.
- Selected validation threshold: `0.45`
- Test set is used once after threshold selection; no threshold is tuned on test.

## Validation Sweep

| Threshold | Pred + | Pred - | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.10 | 1757 | 33 | 891 | 866 | 29 | 4 | 51.40% | 50.71% | 99.55% | 67.19% | 96.76% | 3.24% | 51.40% | 0.1038 |
| 0.20 | 1609 | 181 | 868 | 741 | 154 | 27 | 57.09% | 53.95% | 96.98% | 69.33% | 82.79% | 17.21% | 57.09% | 0.2353 |
| 0.30 | 1338 | 452 | 822 | 516 | 379 | 73 | 67.09% | 61.43% | 91.84% | 73.62% | 57.65% | 42.35% | 67.09% | 0.3935 |
| 0.40 | 1007 | 783 | 705 | 302 | 593 | 190 | 72.51% | 70.01% | 78.77% | 74.13% | 33.74% | 66.26% | 72.51% | 0.4538 |
| 0.45 | 876 | 914 | 657 | 219 | 676 | 238 | 74.47% | 75.00% | 73.41% | 74.20% | 24.47% | 75.53% | 74.47% | 0.4895 |
| 0.50 | 733 | 1057 | 582 | 151 | 744 | 313 | 74.08% | 79.40% | 65.03% | 71.50% | 16.87% | 83.13% | 74.08% | 0.4897 |
| 0.55 | 620 | 1170 | 523 | 97 | 798 | 372 | 73.80% | 84.35% | 58.44% | 69.04% | 10.84% | 89.16% | 73.80% | 0.5002 |
| 0.60 | 532 | 1258 | 474 | 58 | 837 | 421 | 73.24% | 89.10% | 52.96% | 66.43% | 6.48% | 93.52% | 73.24% | 0.5085 |
| 0.70 | 422 | 1368 | 399 | 23 | 872 | 496 | 71.01% | 94.55% | 44.58% | 60.59% | 2.57% | 97.43% | 71.01% | 0.4949 |
| 0.80 | 321 | 1469 | 316 | 5 | 890 | 579 | 67.37% | 98.44% | 35.31% | 51.97% | 0.56% | 99.44% | 67.37% | 0.4529 |
| 0.90 | 192 | 1598 | 191 | 1 | 894 | 704 | 60.61% | 99.48% | 21.34% | 35.14% | 0.11% | 99.89% | 60.61% | 0.3430 |

## Test Result At Validation-Selected Threshold

| Threshold | Pred + | Pred - | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.45 | 1423 | 1483 | 968 | 455 | 998 | 485 | 67.65% | 68.03% | 66.62% | 67.32% | 31.31% | 68.69% | 67.65% | 0.3531 |

## Interpretation

Threshold tuning is diagnostic because the score is not calibrated as a production probability. It is still useful for showing whether validation-set thresholding can trade recall for specificity without touching test labels.
