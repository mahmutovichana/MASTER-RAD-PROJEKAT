# External Validation Evidence Comparison 2026-08

| Evidence type | Dataset | Status | Key result | Interpretation |
| --- | --- | --- | --- | --- |
| Controlled synthetic evidence | Synthetic v0.4 | complete | see v0.4 reports | Controlled pipeline benchmark. |
| Real positive sensitivity evidence | CoDocBench | complete | 100.00% code_diff_only positive recall on 500 positives | Positive-only, no precision/F1. |
| Sanity-control evidence | Synthetic negatives | complete | 0/500 false positives in two modes | Not constant-positive under synthetic control. |
| True external binary proxy evidence | Deep-JIT / DocChecker-style sample | complete | F1 66.84%, precision 50.20%, recall 100.00%, FPR 99.20% | Code-comment consistency proxy; high recall but near always-positive behavior. |
