# External DocChecker Threshold Sweep 2026-08

Thresholds are diagnostic only. The staged confidence score was not calibrated as an external binary probability, so these results should be interpreted as review/abstention behavior, not final decision thresholds.

| Threshold | Pred + | Pred negative/abstained | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | FNR |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00 | 498 | 2 | 250 | 248 | 2 | 0 | 50.40% | 50.20% | 100.00% | 66.84% | 99.20% | 0.00% |
| 0.05 | 498 | 2 | 250 | 248 | 2 | 0 | 50.40% | 50.20% | 100.00% | 66.84% | 99.20% | 0.00% |
| 0.10 | 394 | 106 | 199 | 195 | 55 | 51 | 50.80% | 50.51% | 79.60% | 61.80% | 78.00% | 20.40% |
| 0.15 | 134 | 366 | 79 | 55 | 195 | 171 | 54.80% | 58.96% | 31.60% | 41.15% | 22.00% | 68.40% |
| 0.20 | 45 | 455 | 32 | 13 | 237 | 218 | 53.80% | 71.11% | 12.80% | 21.69% | 5.20% | 87.20% |
| 0.25 | 18 | 482 | 12 | 6 | 244 | 238 | 51.20% | 66.67% | 4.80% | 8.96% | 2.40% | 95.20% |
| 0.30 | 4 | 496 | 4 | 0 | 250 | 246 | 50.80% | 100.00% | 1.60% | 3.15% | 0.00% | 98.40% |
| 0.40 | 0 | 500 | 0 | 0 | 250 | 250 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |
| 0.50 | 0 | 500 | 0 | 0 | 250 | 250 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |
| 0.75 | 0 | 500 | 0 | 0 | 250 | 250 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |

## Diagnostic Takeaway

The highest diagnostic F1 in this sweep is 66.84% at threshold `0.00`. Raising the threshold reduces false positives only by converting many low-confidence positive predictions into negative/abstained decisions, and it also starts losing true positives.
