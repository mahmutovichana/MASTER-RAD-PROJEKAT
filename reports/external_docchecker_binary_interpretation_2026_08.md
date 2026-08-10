# External DocChecker Binary Interpretation 2026-08

This is the first true external binary proxy evaluation for DocGuard. The benchmark is a proxy for code-comment inconsistency, not full project-level Markdown documentation update detection.

The current synthetic-trained model achieves high recall but very poor specificity. On the 500-record Deep-JIT test-partition sample it reaches 100.00% recall while predicting 248/250 external consistent/no-update examples as update-required.

This result shows that synthetic-trained DocGuard does not yet generalize to external consistent/no-update comment examples. It does not invalidate the project; it identifies a concrete domain/task shift that synthetic-only experiments and positive-only CoDocBench recall could not expose.

Recommended thesis wording:

- The model functions as a high-recall detector but over-predicts documentation-update needs on external binary proxy data.
- External binary evaluation reveals a domain/task shift not visible in synthetic-only experiments.

This should not be reported as deployment-ready system performance.
