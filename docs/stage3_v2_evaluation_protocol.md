# DocGuard Stage 3 V2 Evaluation Protocol

Stage 3 V2 evaluates semantic LLM documentation generation after the Final V2 classifiers have already predicted that a documentation update is needed and selected a broad documentation category.

## Development Boundary

Prompt, retrieval, verifier, and repair changes may use only `development_train` and `development_validation` records. The confirmation partition and frozen historical Qwen-100 artifacts are not used for prompt tuning, model choice, thresholds, or manual iteration.

The Stage 3 V2 configuration is stored in `configs/stage3_semantic_generation_v2.json`. The configuration must be frozen before any final confirmation run, and its SHA-256 should be recorded with the evaluation report.

## Architecture Under Test

Stage 3 V2 is evaluated as:

1. Stage 1 classifier predicts whether documentation should change.
2. Stage 2 classifier predicts a broad documentation category for positive cases.
3. Stage 3 V2 analyzes the code change, validates quoted evidence, retrieves candidate documentation from the pre-change documentation context, asks an LLM to write documentation prose, verifies provenance safety, and allows one LLM repair attempt.

If the first patch and the single repair both fail safety verification, the final output is `human_review_required`. The system must not use deterministic documentation text as final output for Stage 3 V2.

## Quality Evaluation

The primary Stage 3 V2 quality study should use a natural-distribution random sample of predicted-positive records from development validation or a later sealed confirmation run. A secondary category-stratified sample may be used as a stress test, but it must be reported separately.

Human evaluation should score each patch on a 1-5 scale for:

- factual correctness
- completeness
- specificity
- readability
- usefulness for a developer

Pairwise preference against a baseline patch may be reported when both outputs are shown blind and in randomized order.

Reference-based metrics may be computed only after generation is complete. Reference text, gold labels, `docs_after`, and documentation diffs must never be placed in the generation prompt or used by the safety verifier.

## Reporting Rules

Reports must separate:

- accepted first-pass LLM patches
- accepted repair patches
- rejected patches requiring human review
- safety violation types
- latency and LLM-call counts

The Deep-JIT proxy remains an external binary inconsistency proxy. It is not a full Markdown DocGuard benchmark and does not evaluate Stage 3 V2 documentation generation quality.
