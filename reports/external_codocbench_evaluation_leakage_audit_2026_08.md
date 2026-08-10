# External CoDocBench Evaluation Leakage Audit 2026-08

- Input sample: `data\external\codocbench_sample_500.jsonl`
- Records inspected: `500`
- Records with `code_diff`: `500`
- Records with `doc_before`: `500`
- Records with `doc_after`: `500`
- Records with `doc_diff`: `500`

## Current Evaluation Input Construction

- Previous bridge behavior used `docs_before_excerpt = doc_before or doc_diff or ""`.
- On the current 500-record sample, `doc_before` is present for every row, so `doc_diff` was not actually selected by that expression.
- However, the fallback to `doc_diff` was leakage-risk if future samples lacked `doc_before`.
- `doc_after` was not passed to the predictor.
- The predictor received `changed_files`, `code_diff`, `docs_before_excerpt`, ids/labels used by the classifier wrapper, and target metadata.
- It did not receive full `doc_after` unless a future code path were changed to include it.

## Direct Answers

| Question | Answer |
| --- | --- |
| Was `doc_diff` / `diff_docstring` included in the model input? | `No` for this 500-record run because `doc_before` existed for all rows; `yes, possible fallback` in the previous generic code path if `doc_before` was missing. |
| Was it used as `docs_before_excerpt` or equivalent? | `No` for the current sample; the previous code could have used it as `docs_before_excerpt` fallback. |
| Was `doc_after` included? | `No`. |
| Was only `code_diff` used? | `No`; the previous run also included `doc_before` as current documentation context. |
| Is the current 99.80% recall fair, assisted, or leakage-risk? | `assisted` for the current sample because it used `doc_before`; the old implementation was `upper_bound_leakage_risk` for samples missing `doc_before`. |
| What input mode should be primary fair external evaluation? | `code_diff_plus_doc_before` if doc_before is reliable; otherwise `code_diff_only` is the strictest fair mode. |

## Input Mode Labels

- `fair`: no future doc diff or doc after.
- `assisted`: current docs before only.
- `upper_bound_leakage_risk`: includes doc diff or doc after.
