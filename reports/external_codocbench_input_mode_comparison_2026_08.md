# External CoDocBench Input Mode Comparison 2026-08

| External input mode | Leakage risk | Total positives | Predicted update-required | False negatives | Positive recall | Median confidence | Low confidence <0.25 | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `code_diff_only` | `fair` | 500 | 500 | 0 | 100.00% | 0.1204 | 479 | Uses changed file, function name, and code_diff only. No documentation text is included. |
| `code_diff_plus_doc_before` | `assisted` | 500 | 499 | 1 | 99.80% | 0.1245 | 473 | Uses changed file, function name, code_diff, and doc_before only. No future doc diff or doc_after is included. |
| `code_diff_plus_doc_diff_upper_bound` | `upper_bound_leakage_risk` | 500 | 499 | 1 | 99.80% | 0.1247 | 472 | Uses code_diff and doc_diff. This exposes the future documentation change and is not a primary fair result. |

The primary fair external result should be `code_diff_only` or `code_diff_plus_doc_before`. The preferred mode is `code_diff_plus_doc_before` when `doc_before` is reliably reconstructed or available because it matches DocGuard's intended access to current documentation before an update.

`code_diff_plus_doc_diff_upper_bound` is useful only as an upper-bound diagnostic because it includes the future documentation change.

This is still positive-only evaluation. It cannot report precision, F1, false-positive rate, or negative quality without a defensible external negative set.
