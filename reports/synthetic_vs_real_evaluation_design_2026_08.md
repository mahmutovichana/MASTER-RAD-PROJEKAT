# Synthetic vs Real Evaluation Design 2026-08

## Synthetic v0.4

- Use as a controlled benchmark.
- Report clean test metrics.
- Report no-leak input results.
- Report stress-test results.
- Do not overclaim generalization.

## External Real Dataset

- Use for real-world validation.
- Start with binary update detection.
- If target documentation is a comment/docstring, adapt `target_kind` accordingly.
- Report separately from synthetic metrics.
- Keep strong and weak labels separate.

## Comparison Table Template

| Dataset | Source | Synthetic/real | Task | Label type | Records | Balance | Binary F1 | Precision | Recall | Macro F1 | Notes |
| --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| DocGuard v0.4 | generated | synthetic | docs update detection + routing | controlled | 6000 | 50/50 | TBD | TBD | TBD | TBD | controlled prototype |
| CoDocBench sample | mined commits | real | code-doc update detection | strong positives, negatives TBD | 100-500 pilot | TBD | TBD | TBD | TBD | TBD | first external validation |

## Recommendation

The final thesis should emphasize transfer: whether models that perform well on controlled synthetic data also perform acceptably on real-world mined code-documentation data.

