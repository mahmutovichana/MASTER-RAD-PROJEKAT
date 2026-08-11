# External Deep-JIT Adaptation Interpretation 2026-08

Existing DocGuard generalizes as a high-recall detector but not as a binary consistency classifier on Deep-JIT. External task-specific training is necessary for specificity.

The best lightweight external classifier is `tfidf_linear_svc` with `old_comment_plus_code_diff` input. It reaches 66.41% accuracy, 68.82% precision, 60.01% recall, 64.12% F1, 27.19% FPR, 72.81% specificity, 66.41% balanced accuracy, and MCC 0.3310 on the Deep-JIT test split.

Deep-JIT remains a proxy for code-comment consistency, not full Markdown documentation patching. This strengthens the thesis by showing why external validation matters: synthetic-only and positive-only evidence did not reveal the specificity problem.
