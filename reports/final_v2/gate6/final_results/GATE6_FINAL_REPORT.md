# Gate 6 Final Human/Reference Evaluation

**Status:** `COMPLETED_FROZEN_HUMAN_EVALUATION`

The protocol and blind review template were frozen before scoring at commit `99d6ac11b04e33cd5ddbc5fc11da48388f38cb82`. The completed workbook passed the frozen membership, order, schema, no-output, completeness, and leakage checks. `review_status = approved` means that the human review is completed and valid; it does **not** mean `human_accept_as_is = yes`.

## Primary outcome

- System coverage: **14/100 (14.0%)** generated/scorable outputs.
- No-output system failure: **86/100 (86.0%)**.
- End-to-end accept-as-is: **0/100 (0.0%)**.
- Conditional accept-as-is: **0/14 (0.0%)**.

The 86 no-output rows retain structural `N/A` ratings. They count against end-to-end acceptance but were not assigned synthetic numeric quality scores.

## Conditional-on-output human quality

| Dimension | n | Mean | Median | Scores 1/2/3/4/5 | Bootstrap 95% CI for mean |
|---|---:|---:|---:|---:|---:|
| Factual correctness | 14 | 4.142857 | 4.0 | 1/0/1/6/6 | [3.533929, 4.642857] |
| Semantic completeness | 14 | 4.357143 | 5.0 | 1/1/1/0/11 | [3.605357, 5.000000] |
| Developer usefulness | 14 | 2.000000 | 2.0 | 1/12/1/0/0 | [1.785714, 2.214286] |
| Readability | 14 | 4.714286 | 5.0 | 0/0/1/2/11 | [4.357143, 5.000000] |
| Style fit | 14 | 2.071429 | 2.0 | 1/12/0/1/0 | [1.785714, 2.428571] |

## Reference diagnostics

No eligible post-change reference text was present for the 14 generated-output rows (`0/14`). Word overlap, TF-IDF cosine, and exact match are therefore **not calculated**. The evaluator's zero-valued empty-set sentinel is not interpreted as performance. Reference similarity remains diagnostic only and does not replace human judgment.

## Safety diagnostics

Frozen Stage 3 execution on the primary sample invoked generation for **24/100** rows and produced **14/100** accepted pipeline outputs. Final statuses: `{"accepted_after_repair": 2, "accepted_first_pass": 12, "human_review_required": 10, "retrieval_context_unavailable": 76}`. Verifier violations: `{"target_not_retrieved": 5, "unsupported_fact": 1}`. Execution errors: `{"input_token_budget_exceeded": 7, "invalid_structured_llm_output": 1}`. These are provenance/safety diagnostics, not human accept-as-is judgments.

## Secondary sample

The supplementary category-stress sample contains 83 rows and is `NOT_HUMAN_EVALUATED`. It is not pooled into the primary result.

## Methodology closure

Human evaluation, reference diagnostics, and safety diagnostics remain separate. No opaque combined accuracy is computed, no post-review methodology change was made, and no Gate 5 artifact was modified.
