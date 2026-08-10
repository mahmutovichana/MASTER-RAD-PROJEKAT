# External Deep-JIT Adaptation Interpretation 2026-08

Existing DocGuard generalizes as a high-recall detector but not as a binary consistency classifier on Deep-JIT. External task-specific training is necessary for specificity.

The best lightweight external classifier is `tfidf_logreg` with `code_diff_only` input. It reaches 68.58% accuracy, 72.17% precision, 60.50% recall, 65.82% F1, and 23.33% FPR on the Deep-JIT test split.

Deep-JIT remains a proxy for code-comment consistency, not full Markdown documentation patching. This strengthens the thesis by showing why external validation matters: synthetic-only and positive-only evidence did not reveal the specificity problem.
