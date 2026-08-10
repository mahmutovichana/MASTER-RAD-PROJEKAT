# External Dataset Roadmap 2026-08

1. CoDocBench positive pilot, 100 records: completed.
2. CoDocBench stratified positive sample, 500-1000 records.
3. Existing DocGuard positive recall evaluation.
4. Manual audit of false negatives and low-confidence predictions.
5. Negative sampling strategy.
6. Add a second external dataset, likely the Panthaplackel comment-update dataset.
7. Train or evaluate an external-specific classifier only after schema and labels are stable.
8. Compare synthetic and external results, keeping label provenance separate.

CoDocBench should remain framed as real-world validation for code-docstring/comment maintenance behavior, not as a replacement for the synthetic project-level Markdown documentation benchmark.
