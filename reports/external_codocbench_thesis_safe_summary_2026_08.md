# External CoDocBench Thesis-Safe Summary 2026-08

## Sample

- Source dataset: CoDocBench
- Sample size: 500 records
- Label source: `strong_positive_code_doc_cochange`
- Label type: real external positive code-docstring/comment co-change examples

## Leakage Audit Conclusion

The earlier 99.80% positive-recall run did not use `doc_diff` for the current 500-record sample because all records had `doc_before`. It should be labeled `assisted`, not leakage. The previous fallback to `doc_diff` when `doc_before` was missing was a future leakage risk and has now been replaced by explicit input modes.

## Input Modes Tested

| Input mode | Label | Description |
| --- | --- | --- |
| `code_diff_only` | fair | Uses changed file, function name, and code diff only. |
| `code_diff_plus_doc_before` | assisted/fair | Uses changed file, function name, code diff, and current documentation before the update. |
| `code_diff_plus_doc_diff_upper_bound` | upper-bound leakage-risk | Includes future documentation diff and is not final thesis evidence. |

## Positive Recall Results

| Input mode | Total positives | Predicted update-required | False negatives | Positive recall | Median confidence | Low confidence <0.25 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `code_diff_only` | 500 | 500 | 0 | 100.00% | 0.1204 | 479 |
| `code_diff_plus_doc_before` | 500 | 499 | 1 | 99.80% | 0.1245 | 473 |
| `code_diff_plus_doc_diff_upper_bound` | 500 | 499 | 1 | 99.80% | 0.1247 | 472 |

## Confidence Weakness

The model is highly sensitive to positive code-doc co-changes, but confidence is weak. Most predictions are below 0.25 confidence, so these results should not be presented as calibrated developer-facing certainty.

## Why Precision/F1 Cannot Be Reported Yet

The CoDocBench pilot contains positives only. Without a defensible external negative set, it cannot support external precision, F1, false-positive rate, or negative classification quality.

## Recommended Thesis Wording

DocGuard's existing HF staged classifier achieved very high positive recall on a 500-record real CoDocBench positive sample under leakage-audited input modes. The strict `code_diff_only` mode reached 100.00% positive recall, and the `code_diff_plus_doc_before` mode reached 99.80%. However, confidence was low and the evaluation remains positive-only, so these results demonstrate sensitivity to real code-doc co-changes rather than complete external generalization.

## Recommended Next Step

Use synthetic negative sanity controls only as a development check, then construct or obtain a real external negative/binary set before reporting precision or F1.

## Current Evidence Hierarchy

1. Synthetic v0.4 benchmark: controlled pipeline evidence on known generated scenarios.
2. CoDocBench positive validation: real positive sensitivity evidence for code-docstring/comment co-changes.
3. Synthetic negative control: non-constant-positive sanity evidence using known no-update synthetic records.
4. Missing piece: external binary/negative validation with explicit real consistent/inconsistent or update/no-update labels.
