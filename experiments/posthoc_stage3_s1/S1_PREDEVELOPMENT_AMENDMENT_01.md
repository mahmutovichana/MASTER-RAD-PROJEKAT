# S1 pre-development technical amendment 01

Status: **FROZEN BEFORE S1 DEVELOPMENT NEURAL EXECUTION**.

The mandatory Kaggle canary reached deterministic structured generation with the pinned 4-bit generator, then returned a syntactically valid critic JSON object missing the required `grounded` field. No S1 development GPU study or configuration selection had run. Confirmation was not accessed, and no Gate 6 row-level human scores, notes, or decisions were accessed.

## Amendment

Every target-decision, documentation-plan, generation/repair, critic and final-critic response is now validated against an explicit registered schema. Missing keys and unambiguous type/domain errors trigger exactly one deterministic schema-correction retry. The retry receives the identical original evidence and prompt, the exact validation errors, and the required JSON shape. It may only serialize the same decision completely; it may not add facts or change the underlying decision. Python supplies no missing semantic defaults. A second invalid response fails closed.

Each structured call records `initial_schema_valid`, `schema_retry_used`, `schema_retry_valid`, and `schema_errors`. These diagnostics contain no hidden reasoning.

The schema retry is serialization infrastructure and is not a documentation-patch repair. The maximum number of semantic documentation repairs remains exactly one.

## Frozen boundary

- Trigger: critic JSON missing required key `grounded`.
- Reason: structured-output reliability.
- Development results seen: false.
- Confirmation accessed: false.
- Gate 6 row-level human data accessed: false.
- Models and revisions: unchanged.
- Retrieval grid and target confidence thresholds: unchanged.
- P1/P2 prompt files: unchanged.
- Target-selection and safety rules: unchanged.
- Schema-correction retries per structured call: 1.
- Semantic documentation repairs: 1.

The original scientific freeze `38f9afb479f738081301172176d3133e4056bd7c` remains preserved in Git history. For S1 execution it is superseded only by this documented pre-development structured-output amendment and subsequent portability-only runtime commits containing it.
