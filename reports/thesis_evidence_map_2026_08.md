# Thesis Evidence Map 2026-08

This document separates the evidence streams for the DocGuard MSc thesis so results are not overclaimed across tasks.

| Evidence stream | Dataset | What it supports | Key result | What not to claim |
| --- | --- | --- | --- | --- |
| Controlled synthetic benchmark | DocGuard synthetic v0.4 | End-to-end DocGuard pipeline on controlled REST API documentation scenarios | Hybrid/HF embedding reports show perfect synthetic test performance | Do not treat this alone as real-world generalization because generator/template bias is possible. |
| Real positive sensitivity | CoDocBench positive sample | The zero-shot model detects real code-doc/comment co-change positives | `code_diff_only` positive recall 100.00% on 500 positives | Do not report precision/F1/FPR because the sample is positive-only. |
| Synthetic negative sanity | Synthetic no-update controls | The model is not constant-positive on in-domain synthetic negatives | 0/500 false positives in both tested input modes | Do not treat this as external negative evidence. |
| External binary proxy zero-shot | Deep-JIT / DocChecker-style code-comment consistency | External binary proxy exposes domain/task shift | Accuracy 50.40%, recall 100.00%, FPR 99.20%, specificity 0.80%, MCC 0.0635 | Do not call this deployment-ready or project-level Markdown documentation performance. |
| External task-specific adaptation | Deep-JIT classical v2 classifier | External training improves binary specificity on code-comment consistency | Current best: accuracy 75.60%, precision 78.84%, recall 69.99%, F1 74.15%, FPR 18.79%, specificity 81.21%, MCC 0.5153 | Do not merge this into the main DocGuard synthetic benchmark or claim Markdown patch generation. |
| Project-level real case study | Manually labeled GitHub commits/PRs | Directly evaluates the DocGuard agent workflow on real software-project documentation cases | 20 real public GitHub PR cases collected, hardened, and validator passed; runner deferred pending adapter | Do not report this small study as a large benchmark or use audit-only fields as model input. |

## Thesis-Safe Claims

- DocGuard is a prototype NLP agent for code/documentation consistency analysis.
- The controlled synthetic benchmark demonstrates that the pipeline can learn the intended detection, routing, categorization, and patch-targeting structure.
- External positive validation shows strong sensitivity to real code-documentation co-change signals.
- External binary proxy validation reveals that synthetic-trained zero-shot DocGuard over-predicts update needs on real consistent comments.
- Task-specific external adaptation substantially improves specificity, showing that external calibration/training is necessary for practical binary consistency detection.
- The next required alignment step is a project-level real case study that evaluates DocGuard detection, category/target routing, and patch usefulness.

## Claims To Avoid

- Do not claim production readiness.
- Do not report synthetic v0.4 metrics as final real-world performance.
- Do not report CoDocBench positive recall as precision or F1.
- Do not report Deep-JIT as full project-level Markdown API documentation evaluation.
- Do not call Deep-JIT numeric label polarity fully confirmed until original documentation or preprocessing code explicitly confirms it.

## Remaining Methodological Caveat

Deep-JIT numeric label polarity remains `plausible_manual_verification_needed`. The current mapping is supported by sampled examples and task framing, but final thesis text should either cite an explicit polarity source or describe the mapping as manually audited and plausible.

## Robustness Update

A deterministic Summary validation carve-out robustness experiment was added to reduce Return-only validation bias. The model choice changed and test metrics became slightly weaker, which shows that the earlier Return-only validation setup was sensitive to subset composition. The combined-validation result should be considered the cleaner Deep-JIT model-selection setup, while the older Return-only result remains a useful historical baseline.

## Classical V2 Update

The stronger classical v2 Deep-JIT proxy baseline now supersedes the earlier combined-validation TF-IDF baseline as the primary Deep-JIT proxy result. It uses `logreg_balanced` with `word_char_tfidf_plus_manual_features` and `old_comment_plus_code_diff`, selected by validation MCC. On the untouched combined-validation test split it reaches 75.60% accuracy, 78.84% precision, 69.99% recall, 74.15% F1, 18.79% FPR, 81.21% specificity, and MCC 0.5153.

The older combined-validation result remains a historical baseline: 66.41% accuracy, 68.82% precision, 60.01% recall, 64.12% F1, 27.19% FPR, 72.81% specificity, and MCC 0.3310.

## Project-Level Case Study Update

A project-level case-study schema and validator have been added to keep DocGuard aligned with the thesis title. The first real file contains 20 public GitHub PR cases: 15 positive documentation-update cases and 5 negative no-update cases. Methodology hardening lowered three weaker negative cases to low confidence, leaving 15 high, 2 medium, and 3 low confidence labels. Validation passed. This is the next DocGuard-agent-centered evidence stream; Deep-JIT remains supporting proxy evidence only.

The automatic case-study runner is deferred because the current DocGuard runtime expects synthetic records and synthetic REST route patterns. Safe automatic inputs are limited to `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`. Documentation-file presence (`changed_files`/`docs_changed_files`), manually assigned `change_type`, docs-after text, and gold/manual fields are audit-only. A real-case adapter should be added before computing automatic case-study scores.
