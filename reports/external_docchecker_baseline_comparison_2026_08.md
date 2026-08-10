# External DocChecker Baseline Comparison 2026-08

| System | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Existing DocGuard | 250 | 248 | 2 | 0 | 50.40% | 50.20% | 100.00% | 66.84% | 99.20% |
| Always positive | 250 | 250 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| Always negative | 0 | 0 | 250 | 250 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Random balanced baseline, seed 42 | 117 | 133 | 117 | 133 | 46.80% | 46.80% | 46.80% | 46.80% | 53.20% |

## Interpretation

Existing DocGuard is very close to the always-positive baseline on this external binary proxy. It improves true negatives from 0 to 2, but keeps recall at 100.00% and still produces a 99.20% false-positive rate.
