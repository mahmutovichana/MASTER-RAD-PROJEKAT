# External Deep-JIT Adaptation Interpretation 2026-08

Existing DocGuard generalizes as a high-recall detector but not as a binary consistency classifier on Deep-JIT. External task-specific training is necessary for specificity.

The best lightweight external classifier is `tfidf_logreg` with `old_comment_plus_code_diff` input. It reaches 68.72% accuracy, 73.41% precision, 58.71% recall, 65.24% F1, 21.27% FPR, 78.73% specificity, 68.72% balanced accuracy, and MCC 0.3821 on the Deep-JIT test split.

Deep-JIT remains a proxy for code-comment consistency, not full Markdown documentation patching. This strengthens the thesis by showing why external validation matters: synthetic-only and positive-only evidence did not reveal the specificity problem.
