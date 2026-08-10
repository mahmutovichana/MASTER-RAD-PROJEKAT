# External CoDocBench Label Quality Notes 2026-08

- CoDocBench positive labels are code-documentation co-change labels.
- These labels are stronger than synthetic labels for real-world validation because they come from mined maintenance history.
- They are not identical to broad project-level Markdown documentation update labels.
- Negative labels should not be inferred from code-only commits without careful rules.
- The first pilot should evaluate whether DocGuard can process real code-doc changes, not whether it can fully patch project documentation files.
- Keep strong positive labels and any future weak negative labels separated in reports.