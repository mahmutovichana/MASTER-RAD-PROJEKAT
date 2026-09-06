# Gate 4 development-only analysis

## Interpretation boundary

The primary sample is the natural-distribution development-validation result.
The secondary sample is a supplementary predicted-category stress study and
must not be pooled with the primary sample as a natural-distribution quality
estimate.

System retrieval-context coverage and conditional generation quality are
reported separately. Confirmation was not accessed.

## Primary natural-distribution sample

- Sampled predicted positives: 100
- Retrieval context available: 8
- Retrieval context unavailable: 92
- Stage 3 invocation rate: 8.0%
- Invoked cases: 8
- Accepted first pass: 1
- Accepted after repair: 1
- Total accepted: 2
- Conditional accepted rate: 25.0%
- Human review required: 6
- Execution errors: 4

Because the primary sample contains only
8 context-available cases, conditional
generation-quality estimates must be interpreted with substantial uncertainty.

## Secondary category stress sample

- Sample rows: 100
- Retrieval context available: 83
- Retrieval context unavailable: 17
- Stage 3 invocation rate: 83.0%
- Invoked cases: 83
- Accepted first pass: 47
- Accepted after repair: 0
- Total accepted: 47
- Conditional accepted rate: 56.6%
- Human review required: 36
- Execution errors: 15

## Required thesis reporting rule

Do not report one combined Gate 4 "accuracy". Report:

1. primary system coverage;
2. primary conditional generation outcomes;
3. supplementary stress-sample outcomes;
4. execution errors separately;
5. safety/provenance violations separately;
6. latency and LLM-call diagnostics separately.
