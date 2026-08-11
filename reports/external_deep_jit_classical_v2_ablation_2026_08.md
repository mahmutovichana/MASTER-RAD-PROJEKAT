# External Deep-JIT Classical V2 Ablation 2026-08

This experiment ablates the strongest CPU-friendly classical Deep-JIT / DocChecker-style external binary proxy setup. It does not replace the project-level DocGuard Markdown documentation task.

- Train records: `23508`
- Validation records: `2630`
- Test records: `2906`
- Train label distribution: `{1: 11754, 0: 11754}`
- Validation label distribution: `{1: 1315, 0: 1315}`
- Test label distribution: `{1: 1453, 0: 1453}`
- Best saved model: `models\external_deep_jit_classical_v2\binary_classical_v2_ablation.joblib`
- Best model: `logreg_balanced`
- Best feature set: `word_char_tfidf_plus_manual_features`
- Best input mode: `old_comment_plus_code_diff`
- Best model selection: validation MCC, with validation balanced accuracy and F1 as tie-breakers.
- Leakage rule: model inputs exclude `new_comment_raw`, `doc_after`, and `doc_diff`.
- Calibrated LinearSVC included: `False`

## Best Test Result

- Accuracy: `75.60%`
- Precision: `78.84%`
- Recall: `69.99%`
- F1: `74.15%`
- FPR: `18.79%`
- Specificity: `81.21%`
- Balanced accuracy: `75.60%`
- MCC: `0.5153`

## Validation Metrics

| Model | Feature set | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 991 | 186 | 1129 | 324 | 80.61% | 84.20% | 75.36% | 79.53% | 14.14% | 85.86% | 80.61% | 0.6156 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 1003 | 227 | 1088 | 312 | 79.51% | 81.54% | 76.27% | 78.82% | 17.26% | 82.74% | 79.51% | 0.5914 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 949 | 199 | 1116 | 366 | 78.52% | 82.67% | 72.17% | 77.06% | 15.13% | 84.87% | 78.52% | 0.5750 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 990 | 262 | 1053 | 325 | 77.68% | 79.07% | 75.29% | 77.13% | 19.92% | 80.08% | 77.68% | 0.5542 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 982 | 267 | 1048 | 333 | 77.19% | 78.62% | 74.68% | 76.60% | 20.30% | 79.70% | 77.19% | 0.5444 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 939 | 228 | 1087 | 376 | 77.03% | 80.46% | 71.41% | 75.66% | 17.34% | 82.66% | 77.03% | 0.5441 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 932 | 276 | 1039 | 383 | 74.94% | 77.15% | 70.87% | 73.88% | 20.99% | 79.01% | 74.94% | 0.5005 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 866 | 233 | 1082 | 449 | 74.07% | 78.80% | 65.86% | 71.75% | 17.72% | 82.28% | 74.07% | 0.4880 |
| `logreg_balanced` | `manual_features_only` | `old_comment_plus_code_diff` | 858 | 414 | 901 | 457 | 66.88% | 67.45% | 65.25% | 66.33% | 31.48% | 68.52% | 66.88% | 0.3378 |
| `linear_svc_balanced` | `manual_features_only` | `old_comment_plus_code_diff` | 866 | 423 | 892 | 449 | 66.84% | 67.18% | 65.86% | 66.51% | 32.17% | 67.83% | 66.84% | 0.3369 |

## Test Metrics

| Model | Feature set | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 1017 | 273 | 1180 | 436 | 75.60% | 78.84% | 69.99% | 74.15% | 18.79% | 81.21% | 75.60% | 0.5153 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 1020 | 331 | 1122 | 433 | 73.71% | 75.50% | 70.20% | 72.75% | 22.78% | 77.22% | 73.71% | 0.4754 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 985 | 305 | 1148 | 468 | 73.40% | 76.36% | 67.79% | 71.82% | 20.99% | 79.01% | 73.40% | 0.4710 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 992 | 348 | 1105 | 461 | 72.16% | 74.03% | 68.27% | 71.03% | 23.95% | 76.05% | 72.16% | 0.4446 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 998 | 399 | 1054 | 455 | 70.61% | 71.44% | 68.69% | 70.04% | 27.46% | 72.54% | 70.61% | 0.4126 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 968 | 322 | 1131 | 485 | 72.23% | 75.04% | 66.62% | 70.58% | 22.16% | 77.84% | 72.23% | 0.4474 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 905 | 408 | 1045 | 548 | 67.10% | 68.93% | 62.28% | 65.44% | 28.08% | 71.92% | 67.10% | 0.3436 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 882 | 329 | 1124 | 571 | 69.03% | 72.83% | 60.70% | 66.22% | 22.64% | 77.36% | 69.03% | 0.3860 |
| `logreg_balanced` | `manual_features_only` | `old_comment_plus_code_diff` | 946 | 498 | 955 | 507 | 65.42% | 65.51% | 65.11% | 65.31% | 34.27% | 65.73% | 65.42% | 0.3083 |
| `linear_svc_balanced` | `manual_features_only` | `old_comment_plus_code_diff` | 962 | 507 | 946 | 491 | 65.66% | 65.49% | 66.21% | 65.85% | 34.89% | 65.11% | 65.66% | 0.3132 |

## Per-Subset Test Metrics

| Model | Feature set | Input mode | Subset | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Return` | 679 | 132 | 788 | 241 | 79.73% | 83.72% | 73.80% | 78.45% | 14.35% | 85.65% | 79.73% | 0.5988 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Summary` | 338 | 141 | 392 | 195 | 68.48% | 70.56% | 63.41% | 66.80% | 26.45% | 73.55% | 68.48% | 0.3715 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Return` | 698 | 179 | 741 | 222 | 78.21% | 79.59% | 75.87% | 77.69% | 19.46% | 80.54% | 78.21% | 0.5647 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Summary` | 322 | 152 | 381 | 211 | 65.95% | 67.93% | 60.41% | 63.95% | 28.52% | 71.48% | 65.95% | 0.3209 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Return` | 683 | 156 | 764 | 237 | 78.64% | 81.41% | 74.24% | 77.66% | 16.96% | 83.04% | 78.64% | 0.5751 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 302 | 149 | 384 | 231 | 64.35% | 66.96% | 56.66% | 61.38% | 27.95% | 72.05% | 64.35% | 0.2905 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Return` | 690 | 185 | 735 | 230 | 77.45% | 78.86% | 75.00% | 76.88% | 20.11% | 79.89% | 77.45% | 0.5496 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 302 | 163 | 370 | 231 | 63.04% | 64.95% | 56.66% | 60.52% | 30.58% | 69.42% | 63.04% | 0.2629 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Return` | 682 | 226 | 694 | 238 | 74.78% | 75.11% | 74.13% | 74.62% | 24.57% | 75.43% | 74.78% | 0.4957 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 316 | 173 | 360 | 217 | 63.41% | 64.62% | 59.29% | 61.84% | 32.46% | 67.54% | 63.41% | 0.2692 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Return` | 667 | 177 | 743 | 253 | 76.63% | 79.03% | 72.50% | 75.62% | 19.24% | 80.76% | 76.63% | 0.5344 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 301 | 145 | 388 | 232 | 64.63% | 67.49% | 56.47% | 61.49% | 27.20% | 72.80% | 64.63% | 0.2967 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Return` | 645 | 236 | 684 | 275 | 72.23% | 73.21% | 70.11% | 71.63% | 25.65% | 74.35% | 72.23% | 0.4450 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Summary` | 260 | 172 | 361 | 273 | 58.26% | 60.19% | 48.78% | 53.89% | 32.27% | 67.73% | 58.26% | 0.1681 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Return` | 628 | 186 | 734 | 292 | 74.02% | 77.15% | 68.26% | 72.43% | 20.22% | 79.78% | 74.02% | 0.4837 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Summary` | 254 | 143 | 390 | 279 | 60.41% | 63.98% | 47.65% | 54.62% | 26.83% | 73.17% | 60.41% | 0.2154 |
| `logreg_balanced` | `manual_features_only` | `old_comment_plus_code_diff` | `Return` | 618 | 340 | 580 | 302 | 65.11% | 64.51% | 67.17% | 65.81% | 36.96% | 63.04% | 65.11% | 0.3024 |
| `logreg_balanced` | `manual_features_only` | `old_comment_plus_code_diff` | `Summary` | 328 | 158 | 375 | 205 | 65.95% | 67.49% | 61.54% | 64.38% | 29.64% | 70.36% | 65.95% | 0.3202 |
| `linear_svc_balanced` | `manual_features_only` | `old_comment_plus_code_diff` | `Return` | 625 | 344 | 576 | 295 | 65.27% | 64.50% | 67.93% | 66.17% | 37.39% | 62.61% | 65.27% | 0.3059 |
| `linear_svc_balanced` | `manual_features_only` | `old_comment_plus_code_diff` | `Summary` | 337 | 163 | 370 | 196 | 66.32% | 67.40% | 63.23% | 65.25% | 30.58% | 69.42% | 66.32% | 0.3271 |

## Comparison Against Previous Best

| System | Accuracy | F1 | FPR | MCC |
| --- | ---: | ---: | ---: | ---: |
| Previous combined-validation best (`tfidf_linear_svc`, `old_comment_plus_code_diff`) | 66.41% | 64.12% | 27.19% | 0.3310 |
| Classical v2 best (`logreg_balanced`, `word_char_tfidf_plus_manual_features`, `old_comment_plus_code_diff`) | 75.60% | 74.15% | 18.79% | 0.5153 |

## Comparison Against Zero-Shot DocGuard

| System | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Existing synthetic-trained DocGuard zero-shot | 50.40% | 50.20% | 100.00% | 66.84% | 99.20% | 0.80% | 50.40% | 0.0635 |
| Classical v2 best | 75.60% | 78.84% | 69.99% | 74.15% | 18.79% | 81.21% | 75.60% | 0.5153 |

## Interpretation

The ablation is selected without test tuning. It should be reported as an external code-comment consistency proxy result and kept separate from the main DocGuard agent benchmark.

## Ablation Interpretation

Manual features alone are safe but not sufficient: the best manual-only result reaches 65.66% accuracy, 65.85% F1, 34.89% FPR, and MCC 0.3132 on test. This is weaker than word-only, char-only, and word+char TF-IDF.

Character n-grams are a major contributor. The best char-only result reaches 72.23% accuracy and MCC 0.4474, outperforming word-only on MCC and capturing code/comment morphology that word tokens miss.

The best lexical-only setup is `word_char_tfidf` with LogisticRegression: 73.40% accuracy, 71.82% F1, 20.99% FPR, and MCC 0.4710. Adding manual features improves this to 75.60% accuracy, 74.15% F1, 18.79% FPR, and MCC 0.5153.

The improvement therefore comes mainly from the word+char TF-IDF representation, with manual features providing a useful additional lift rather than carrying the model alone. Summary remains harder than Return: best v2 MCC is 0.5988 on Return and 0.3715 on Summary.
