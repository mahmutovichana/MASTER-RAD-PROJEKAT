# External Deep-JIT Binary Classifier Evaluation 2026-08

- Train records: `23508`
- Validation records: `2630`
- Test records: `2906`
- Train label distribution: `{1: 11754, 0: 11754}`
- Validation label distribution: `{1: 1315, 0: 1315}`
- Test label distribution: `{1: 1453, 0: 1453}`
- Best saved model: `models\external_deep_jit_combined_validation\binary_tfidf_logreg.joblib`
- Best model: `tfidf_linear_svc`
- Best input mode: `old_comment_plus_code_diff`
- Best model selection: validation F1, with validation balanced accuracy as tie-breaker.
- Best validation F1: `0.7303`
- Label polarity status: `plausible_manual_verification_needed`
- Leakage rule: model inputs exclude `new_comment_raw`, `doc_after`, and `doc_diff`.

## Combined Test Metrics

| System | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | FNR | Specificity | Balanced accuracy | MCC | Median confidence/margin |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `always_positive` | `old_comment_plus_code_diff` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 0.00% | 50.00% | 0.0000 | 1.0000 |
| `always_negative` | `old_comment_plus_code_diff` | 0 | 0 | 1453 | 1453 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 100.00% | 50.00% | 0.0000 | 1.0000 |
| `majority` | `old_comment_plus_code_diff` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 0.00% | 50.00% | 0.0000 | 1.0000 |
| `tfidf_logreg` | `old_comment_plus_code_diff` | 849 | 316 | 1137 | 604 | 68.34% | 72.88% | 58.43% | 64.86% | 21.75% | 41.57% | 78.25% | 68.34% | 0.3743 | 0.6706 |
| `tfidf_linear_svc` | `old_comment_plus_code_diff` | 872 | 395 | 1058 | 581 | 66.41% | 68.82% | 60.01% | 64.12% | 27.19% | 39.99% | 72.81% | 66.41% | 0.3310 | 0.4629 |
| `always_positive` | `old_comment_plus_old_new_code` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 0.00% | 50.00% | 0.0000 | 1.0000 |
| `always_negative` | `old_comment_plus_old_new_code` | 0 | 0 | 1453 | 1453 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 100.00% | 50.00% | 0.0000 | 1.0000 |
| `majority` | `old_comment_plus_old_new_code` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 0.00% | 50.00% | 0.0000 | 1.0000 |
| `tfidf_logreg` | `old_comment_plus_old_new_code` | 791 | 352 | 1101 | 662 | 65.11% | 69.20% | 54.44% | 60.94% | 24.23% | 45.56% | 75.77% | 65.11% | 0.3093 | 0.6535 |
| `tfidf_linear_svc` | `old_comment_plus_old_new_code` | 848 | 439 | 1014 | 605 | 64.07% | 65.89% | 58.36% | 61.90% | 30.21% | 41.64% | 69.79% | 64.07% | 0.2833 | 0.4444 |
| `always_positive` | `code_diff_only` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 0.00% | 50.00% | 0.0000 | 1.0000 |
| `always_negative` | `code_diff_only` | 0 | 0 | 1453 | 1453 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 100.00% | 50.00% | 0.0000 | 1.0000 |
| `majority` | `code_diff_only` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 0.00% | 50.00% | 0.0000 | 1.0000 |
| `tfidf_logreg` | `code_diff_only` | 880 | 348 | 1105 | 573 | 68.31% | 71.66% | 60.56% | 65.65% | 23.95% | 39.44% | 76.05% | 68.31% | 0.3706 | 0.6571 |
| `tfidf_linear_svc` | `code_diff_only` | 868 | 432 | 1021 | 585 | 65.00% | 66.77% | 59.74% | 63.06% | 29.73% | 40.26% | 70.27% | 65.00% | 0.3017 | 0.4329 |
| `always_positive` | `old_comment_plus_new_code` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 0.00% | 50.00% | 0.0000 | 1.0000 |
| `always_negative` | `old_comment_plus_new_code` | 0 | 0 | 1453 | 1453 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 100.00% | 50.00% | 0.0000 | 1.0000 |
| `majority` | `old_comment_plus_new_code` | 1453 | 1453 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 0.00% | 50.00% | 0.0000 | 1.0000 |
| `tfidf_logreg` | `old_comment_plus_new_code` | 752 | 336 | 1117 | 701 | 64.32% | 69.12% | 51.75% | 59.19% | 23.12% | 48.25% | 76.88% | 64.32% | 0.2958 | 0.6587 |
| `tfidf_linear_svc` | `old_comment_plus_new_code` | 800 | 419 | 1034 | 653 | 63.11% | 65.63% | 55.06% | 59.88% | 28.84% | 44.94% | 71.16% | 63.11% | 0.2657 | 0.4281 |

## Per-Subset Test Metrics

| System | Input mode | Subset | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `always_positive` | `old_comment_plus_code_diff` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `always_positive` | `old_comment_plus_code_diff` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `always_negative` | `old_comment_plus_code_diff` | `Return` | 0 | 0 | 920 | 920 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 50.00% | 0.0000 |
| `always_negative` | `old_comment_plus_code_diff` | `Summary` | 0 | 0 | 533 | 533 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 50.00% | 0.0000 |
| `majority` | `old_comment_plus_code_diff` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `majority` | `old_comment_plus_code_diff` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `tfidf_logreg` | `old_comment_plus_code_diff` | `Return` | 610 | 176 | 744 | 310 | 73.59% | 77.61% | 66.30% | 71.51% | 19.13% | 80.87% | 73.59% | 0.4768 |
| `tfidf_logreg` | `old_comment_plus_code_diff` | `Summary` | 239 | 140 | 393 | 294 | 59.29% | 63.06% | 44.84% | 52.41% | 26.27% | 73.73% | 59.29% | 0.1940 |
| `tfidf_linear_svc` | `old_comment_plus_code_diff` | `Return` | 626 | 237 | 683 | 294 | 71.14% | 72.54% | 68.04% | 70.22% | 25.76% | 74.24% | 71.14% | 0.4236 |
| `tfidf_linear_svc` | `old_comment_plus_code_diff` | `Summary` | 246 | 158 | 375 | 287 | 58.26% | 60.89% | 46.15% | 52.51% | 29.64% | 70.36% | 58.26% | 0.1702 |
| `always_positive` | `old_comment_plus_old_new_code` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `always_positive` | `old_comment_plus_old_new_code` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `always_negative` | `old_comment_plus_old_new_code` | `Return` | 0 | 0 | 920 | 920 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 50.00% | 0.0000 |
| `always_negative` | `old_comment_plus_old_new_code` | `Summary` | 0 | 0 | 533 | 533 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 50.00% | 0.0000 |
| `majority` | `old_comment_plus_old_new_code` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `majority` | `old_comment_plus_old_new_code` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `tfidf_logreg` | `old_comment_plus_old_new_code` | `Return` | 592 | 200 | 720 | 328 | 71.30% | 74.75% | 64.35% | 69.16% | 21.74% | 78.26% | 71.30% | 0.4303 |
| `tfidf_logreg` | `old_comment_plus_old_new_code` | `Summary` | 199 | 152 | 381 | 334 | 54.41% | 56.70% | 37.34% | 45.02% | 28.52% | 71.48% | 54.41% | 0.0938 |
| `tfidf_linear_svc` | `old_comment_plus_old_new_code` | `Return` | 623 | 258 | 662 | 297 | 69.84% | 70.72% | 67.72% | 69.18% | 28.04% | 71.96% | 69.84% | 0.3971 |
| `tfidf_linear_svc` | `old_comment_plus_old_new_code` | `Summary` | 225 | 181 | 352 | 308 | 54.13% | 55.42% | 42.21% | 47.92% | 33.96% | 66.04% | 54.13% | 0.0850 |
| `always_positive` | `code_diff_only` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `always_positive` | `code_diff_only` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `always_negative` | `code_diff_only` | `Return` | 0 | 0 | 920 | 920 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 50.00% | 0.0000 |
| `always_negative` | `code_diff_only` | `Summary` | 0 | 0 | 533 | 533 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 50.00% | 0.0000 |
| `majority` | `code_diff_only` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `majority` | `code_diff_only` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `tfidf_logreg` | `code_diff_only` | `Return` | 633 | 213 | 707 | 287 | 72.83% | 74.82% | 68.80% | 71.69% | 23.15% | 76.85% | 72.83% | 0.4580 |
| `tfidf_logreg` | `code_diff_only` | `Summary` | 247 | 135 | 398 | 286 | 60.51% | 64.66% | 46.34% | 53.99% | 25.33% | 74.67% | 60.51% | 0.2191 |
| `tfidf_linear_svc` | `code_diff_only` | `Return` | 630 | 264 | 656 | 290 | 69.89% | 70.47% | 68.48% | 69.46% | 28.70% | 71.30% | 69.89% | 0.3980 |
| `tfidf_linear_svc` | `code_diff_only` | `Summary` | 238 | 168 | 365 | 295 | 56.57% | 58.62% | 44.65% | 50.69% | 31.52% | 68.48% | 56.57% | 0.1352 |
| `always_positive` | `old_comment_plus_new_code` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `always_positive` | `old_comment_plus_new_code` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `always_negative` | `old_comment_plus_new_code` | `Return` | 0 | 0 | 920 | 920 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 50.00% | 0.0000 |
| `always_negative` | `old_comment_plus_new_code` | `Summary` | 0 | 0 | 533 | 533 | 50.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% | 50.00% | 0.0000 |
| `majority` | `old_comment_plus_new_code` | `Return` | 920 | 920 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `majority` | `old_comment_plus_new_code` | `Summary` | 533 | 533 | 0 | 0 | 50.00% | 50.00% | 100.00% | 66.67% | 100.00% | 0.00% | 50.00% | 0.0000 |
| `tfidf_logreg` | `old_comment_plus_new_code` | `Return` | 562 | 185 | 735 | 358 | 70.49% | 75.23% | 61.09% | 67.43% | 20.11% | 79.89% | 70.49% | 0.4172 |
| `tfidf_logreg` | `old_comment_plus_new_code` | `Summary` | 190 | 151 | 382 | 343 | 53.66% | 55.72% | 35.65% | 43.48% | 28.33% | 71.67% | 53.66% | 0.0784 |
| `tfidf_linear_svc` | `old_comment_plus_new_code` | `Return` | 583 | 239 | 681 | 337 | 68.70% | 70.92% | 63.37% | 66.93% | 25.98% | 74.02% | 68.70% | 0.3761 |
| `tfidf_linear_svc` | `old_comment_plus_new_code` | `Summary` | 217 | 180 | 353 | 316 | 53.47% | 54.66% | 40.71% | 46.67% | 33.77% | 66.23% | 53.47% | 0.0718 |

## Sentence Embedding Model

Skipped by default. `sentence_transformers` is optional and can be slower or require model download; this run focuses on CPU-friendly TF-IDF models.

- Requested sentence embeddings: `False`
