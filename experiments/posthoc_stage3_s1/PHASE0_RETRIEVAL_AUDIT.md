# S1 Phase 0 retrieval audit

Status: post-hoc Stage 3 challenger, development only. Confirmation was not accessed, and no Gate 6 row-level human data was accessed.

## Finding

Canonical Stage 3 had repository retrieval available only when a row already carried `doc_context_*` candidates. The adapter did not turn `docs_before_excerpt` into a path-bearing candidate and the pipeline failed closed before any model call when candidates were absent. Across the frozen Gate 4 development memberships this produced 109/200 context-unavailable rows. Of 91 invoked rows, 42 ended as human review required because of fail-closed grounding/target checks or bounded runtime/structured-output failures. The published aggregate Gate 6 outcome follows the same mechanism: 76 context-unavailable, then 14 accepted outputs and 10 human-review-required among 24 invocations.

## Pre-change reconstruction and candidate coverage

- Development cases: **200** (primary 100; secondary 100; never pooled for canonical inference).
- Explicit pre-change state reconstructed: **200/200 (100.0%)**.
- At least one eligible documentation candidate: **200/200 (100.0%)**.
- Canonical attached-context availability: **91/200 (45.5%)**.
- Known target-document evidence: **79/200 (39.5%)**, exclusively controlled rows.
- Candidate count: min **2**, median **66.0**, max **813**.

Every row contains repository name, language, changed paths, a stored diff excerpt, and a docs-before excerpt. The provenance marker supplies 121 natural pre-change Git commits; 79 controlled rows join to frozen baseline copies and known synthetic target paths. Fifty-two stored diff excerpts end with an explicit truncation marker. No development documentation-after/reference text is exposed to S1. Natural GitHub URLs are derived from owner/repository; no mutable local checkout is trusted.

Natural repositories are read from bare caches at the exact 40-hex commit recorded in the frozen `docs_before_excerpt` provenance marker. Controlled cases use their frozen unchanged source copies. `HEAD`, branch tips, and post-change fallbacks are forbidden. A missing explicit object is marked unavailable.

## Methodological disposition

The majority-reconstruction stop condition is **NOT TRIGGERED**. Natural rows do not carry target-document gold; Hit@k/MRR may therefore be reported only for the 79 controlled rows and must not be generalized to the natural subset.
