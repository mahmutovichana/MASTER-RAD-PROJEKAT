# Report Language Corrections 2026-08

## Purpose

This file lists wording that should be softened before thesis writing. Existing reports are preserved; this is a correction guide.

## Statements to Soften

- Any statement implying DocGuard "solves" documentation consistency should be changed to "evaluates documentation-update detection on controlled synthetic data and requires external validation."
- Perfect HF results should be described as "achieved perfect accuracy on synthetic v0.4 clean test data" rather than as evidence of real-world generalization.
- `full_current` results should be described as "upper-bound assisted setting" because summaries and signals may leak label semantics.
- Mock LLM reports should be described as pipeline validation, not real model quality.
- VS Code extension v0.5 should be described as an MVP practical demonstration, not production readiness.

## Preferred Phrasing

- "The model achieved perfect binary accuracy on synthetic v0.4 clean test data; external validation is required."
- "Synthetic v0.4 is a controlled prototype benchmark."
- "CoDocBench or a similar mined dataset is needed for real-world validation."
- "The VS Code extension demonstrates workflow integration."

