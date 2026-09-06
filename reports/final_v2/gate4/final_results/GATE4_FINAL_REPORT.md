# Gate 4 final Stage 3 development report

Status: **PASS / FROZEN**.

## Experimental boundary

Gate 4 used development-only evidence. The sealed confirmation split was not
accessed, scored, generated, inspected, or used for tuning.

The final external run used the exact source commit
`c3ddac2d64f71127082f66fba53850f64e071ec3`.

Stage 3 uses Qwen/Qwen2.5-Coder-7B-Instruct in FP16, temperature 0.1,
top-k document retrieval of 3, at most one repair, purpose-specific generation
limits of 512 tokens, and a maximum input prompt size of 4096 tokens.

Oversized prompts are not silently truncated. They fail closed to human review.
Malformed structured output also fails closed.

## Primary natural-distribution sample

The primary sample contains 100 frozen Binary predicted-positive development
validation cases sampled with seed 42 before retrieval-context availability is
inspected.

- Retrieval context available: 8/100 (8.0%)
- Retrieval context unavailable: 92/100 (92.0%)
- Accepted first pass: 1/8
- Accepted after repair: 1/8
- Total conditionally accepted: 2/8 (25.0%)
- Human review required: 6/8 (75.0%)
- Wilson 95% interval for conditional acceptance: 7.1% to 59.1%

The primary result demonstrates that retrieval-context coverage, rather than
generation alone, is the dominant end-to-end Stage 3 bottleneck. Conditional
generation quality on this slice is highly uncertain because only eight cases
were invokable.

## Secondary predicted-category stress sample

The supplementary development stress sample contains 25 predicted positives per
predicted documentation category.

- Retrieval context available: 83/100 (83.0%)
- Retrieval context unavailable: 17/100 (17.0%)
- Accepted first pass: 47/83
- Accepted after repair: 0/83
- Total conditionally accepted: 47/83 (56.6%)
- Human review required: 36/83 (43.4%)
- Wilson 95% interval for conditional acceptance: 45.9% to 66.8%

This stress sample is supplementary and must not be pooled with the primary
sample as a natural-distribution quality estimate.

## Predicted-category stress results

| Predicted category | Context available | Accepted | Conditional acceptance |
| --- | ---: | ---: | ---: |
| api_reference | 24/25 | 1/24 | 4.2% |
| configuration | 20/25 | 14/20 | 70.0% |
| developer_setup | 22/25 | 17/22 | 77.3% |
| model_contract | 17/25 | 15/17 | 88.2% |

The large category asymmetry is retained as a development finding rather than
removed through post-hoc category-specific tuning. In particular,
`api_reference` is a clear Stage 3 limitation and should be discussed explicitly
in the thesis.

## Execution robustness

Across all 91 context-available memberships:

- accepted first pass: 48
- accepted after repair: 1
- human review required: 42
- total LLM calls: 187
- input-token-budget failures: 6
- invalid structured-output failures: 13
- CUDA out-of-memory failures in the final run: 0

The final memory-safety hardening therefore prevented the previously observed
oversized-prompt CUDA crash from aborting the batch.

## Safety and provenance

Recorded verifier violation events:

- unsupported_fact: 50
- target_not_retrieved: 2

These are violation-event counts, not counts of unique cases.

Generation did not receive post-change documentation, gold labels, human-review
labels, or confirmation reference fields.

## Freeze decision

No preregistered minimum Stage 3 acceptance threshold was defined for Gate 4.
The Gate 4 pass criterion is reproducible capture of the development-selected
configuration, source hashes, generation route, external-run evidence, and the
sealed-confirmation boundary.

The observed category asymmetry and low primary retrieval coverage are therefore
reported as limitations rather than used for additional post-hoc tuning.

Stage 3 is frozen after Gate 4 PASS. Any Binary/Category model, threshold,
retrieval route, prompt, generation setting, input-token budget, or safety-policy
change after this point is forbidden for the one-shot Gate 5 confirmation.
