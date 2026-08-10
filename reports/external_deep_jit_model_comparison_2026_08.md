# External Deep-JIT Binary Classifier Evaluation 2026-08

- Train records: `24348`
- Validation records: `1790`
- Test records: `2906`
- Train label distribution: `{1: 12174, 0: 12174}`
- Validation label distribution: `{1: 895, 0: 895}`
- Test label distribution: `{1: 1453, 0: 1453}`
- Best saved model: `models\external_deep_jit\binary_tfidf_logreg.joblib`
- Best model: `tfidf_logreg`
- Best input mode: `code_diff_only`
- Label polarity status: `plausible_manual_verification_needed`
- Leakage rule: model inputs exclude `new_comment_raw`, `doc_after`, and `doc_diff`.

## Combined Test Metrics

| System | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | FNR | Median confidence/margin |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `always_positive` | `old_comment_plus_code_diff` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 1.0000 |
| `always_negative` | `old_comment_plus_code_diff` | 0 | 0 | 1453 | 1453 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 1.0000 |
| `majority` | `old_comment_plus_code_diff` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 1.0000 |
| `tfidf_logreg` | `old_comment_plus_code_diff` | 853 | 309 | 1144 | 600 | 68.72% | 73.41% | 58.71% | 65.24% | 21.27% | 41.29% | 0.6723 |
| `tfidf_linear_svc` | `old_comment_plus_code_diff` | 870 | 391 | 1062 | 583 | 66.48% | 68.99% | 59.88% | 64.11% | 26.91% | 40.12% | 0.4676 |
| `always_positive` | `old_comment_plus_old_new_code` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 1.0000 |
| `always_negative` | `old_comment_plus_old_new_code` | 0 | 0 | 1453 | 1453 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 1.0000 |
| `majority` | `old_comment_plus_old_new_code` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 1.0000 |
| `tfidf_logreg` | `old_comment_plus_old_new_code` | 793 | 357 | 1096 | 660 | 65.00% | 68.96% | 54.58% | 60.93% | 24.57% | 45.42% | 0.6543 |
| `tfidf_linear_svc` | `old_comment_plus_old_new_code` | 852 | 441 | 1012 | 601 | 64.14% | 65.89% | 58.64% | 62.05% | 30.35% | 41.36% | 0.4415 |
| `always_positive` | `code_diff_only` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 1.0000 |
| `always_negative` | `code_diff_only` | 0 | 0 | 1453 | 1453 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 1.0000 |
| `majority` | `code_diff_only` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 1.0000 |
| `tfidf_logreg` | `code_diff_only` | 879 | 339 | 1114 | 574 | 68.58% | 72.17% | 60.50% | 65.82% | 23.33% | 39.50% | 0.6574 |
| `tfidf_linear_svc` | `code_diff_only` | 861 | 425 | 1028 | 592 | 65.00% | 66.95% | 59.26% | 62.87% | 29.25% | 40.74% | 0.4405 |
| `always_positive` | `old_comment_plus_new_code` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 1.0000 |
| `always_negative` | `old_comment_plus_new_code` | 0 | 0 | 1453 | 1453 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 1.0000 |
| `majority` | `old_comment_plus_new_code` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 1.0000 |
| `tfidf_logreg` | `old_comment_plus_new_code` | 749 | 343 | 1110 | 704 | 63.97% | 68.59% | 51.55% | 58.86% | 23.61% | 48.45% | 0.6589 |
| `tfidf_linear_svc` | `old_comment_plus_new_code` | 795 | 433 | 1020 | 658 | 62.46% | 64.74% | 54.71% | 59.31% | 29.80% | 45.29% | 0.4274 |

## Per-Subset Test Metrics

| System | Input mode | Subset | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `always_positive` | `old_comment_plus_code_diff` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `always_positive` | `old_comment_plus_code_diff` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `always_negative` | `old_comment_plus_code_diff` | `Return` | 0 | 0 | 920 | 920 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `always_negative` | `old_comment_plus_code_diff` | `Summary` | 0 | 0 | 533 | 533 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `majority` | `old_comment_plus_code_diff` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `majority` | `old_comment_plus_code_diff` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `tfidf_logreg` | `old_comment_plus_code_diff` | `Return` | 617 | 175 | 745 | 303 | 74.02% | 77.90% | 67.07% | 72.08% | 19.02% |
| `tfidf_logreg` | `old_comment_plus_code_diff` | `Summary` | 236 | 134 | 399 | 297 | 59.57% | 63.78% | 44.28% | 52.27% | 25.14% |
| `tfidf_linear_svc` | `old_comment_plus_code_diff` | `Return` | 625 | 233 | 687 | 295 | 71.30% | 72.84% | 67.93% | 70.30% | 25.33% |
| `tfidf_linear_svc` | `old_comment_plus_code_diff` | `Summary` | 245 | 158 | 375 | 288 | 58.16% | 60.79% | 45.97% | 52.35% | 29.64% |
| `always_positive` | `old_comment_plus_old_new_code` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `always_positive` | `old_comment_plus_old_new_code` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `always_negative` | `old_comment_plus_old_new_code` | `Return` | 0 | 0 | 920 | 920 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `always_negative` | `old_comment_plus_old_new_code` | `Summary` | 0 | 0 | 533 | 533 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `majority` | `old_comment_plus_old_new_code` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `majority` | `old_comment_plus_old_new_code` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `tfidf_logreg` | `old_comment_plus_old_new_code` | `Return` | 595 | 202 | 718 | 325 | 71.36% | 74.65% | 64.67% | 69.31% | 21.96% |
| `tfidf_logreg` | `old_comment_plus_old_new_code` | `Summary` | 198 | 155 | 378 | 335 | 54.03% | 56.09% | 37.15% | 44.70% | 29.08% |
| `tfidf_linear_svc` | `old_comment_plus_old_new_code` | `Return` | 625 | 263 | 657 | 295 | 69.67% | 70.38% | 67.93% | 69.14% | 28.59% |
| `tfidf_linear_svc` | `old_comment_plus_old_new_code` | `Summary` | 227 | 178 | 355 | 306 | 54.60% | 56.05% | 42.59% | 48.40% | 33.40% |
| `always_positive` | `code_diff_only` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `always_positive` | `code_diff_only` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `always_negative` | `code_diff_only` | `Return` | 0 | 0 | 920 | 920 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `always_negative` | `code_diff_only` | `Summary` | 0 | 0 | 533 | 533 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `majority` | `code_diff_only` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `majority` | `code_diff_only` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `tfidf_logreg` | `code_diff_only` | `Return` | 634 | 206 | 714 | 286 | 73.26% | 75.48% | 68.91% | 72.05% | 22.39% |
| `tfidf_logreg` | `code_diff_only` | `Summary` | 245 | 133 | 400 | 288 | 60.51% | 64.81% | 45.97% | 53.79% | 24.95% |
| `tfidf_linear_svc` | `code_diff_only` | `Return` | 619 | 257 | 663 | 301 | 69.67% | 70.66% | 67.28% | 68.93% | 27.93% |
| `tfidf_linear_svc` | `code_diff_only` | `Summary` | 242 | 168 | 365 | 291 | 56.94% | 59.02% | 45.40% | 51.33% | 31.52% |
| `always_positive` | `old_comment_plus_new_code` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `always_positive` | `old_comment_plus_new_code` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `always_negative` | `old_comment_plus_new_code` | `Return` | 0 | 0 | 920 | 920 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `always_negative` | `old_comment_plus_new_code` | `Summary` | 0 | 0 | 533 | 533 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `majority` | `old_comment_plus_new_code` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `majority` | `old_comment_plus_new_code` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% |
| `tfidf_logreg` | `old_comment_plus_new_code` | `Return` | 559 | 191 | 729 | 361 | 70.00% | 74.53% | 60.76% | 66.95% | 20.76% |
| `tfidf_logreg` | `old_comment_plus_new_code` | `Summary` | 190 | 152 | 381 | 343 | 53.56% | 55.56% | 35.65% | 43.43% | 28.52% |
| `tfidf_linear_svc` | `old_comment_plus_new_code` | `Return` | 581 | 249 | 671 | 339 | 68.04% | 70.00% | 63.15% | 66.40% | 27.07% |
| `tfidf_linear_svc` | `old_comment_plus_new_code` | `Summary` | 214 | 184 | 349 | 319 | 52.81% | 53.77% | 40.15% | 45.97% | 34.52% |

## Sentence Embedding Model

Skipped by default. `sentence_transformers` is optional and can be slower or require model download; this run focuses on CPU-friendly TF-IDF models.

- Requested sentence embeddings: `False`
