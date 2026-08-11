# External Deep-JIT Classical V2 Model Comparison 2026-08

This experiment is a stronger CPU-friendly classical baseline for the Deep-JIT / DocChecker-style external binary proxy. It does not replace the project-level DocGuard Markdown documentation task.

- Train records: `23508`
- Validation records: `2630`
- Test records: `2906`
- Train label distribution: `{1: 11754, 0: 11754}`
- Validation label distribution: `{1: 1315, 0: 1315}`
- Test label distribution: `{1: 1453, 0: 1453}`
- Best saved model: `models\external_deep_jit_classical_v2\binary_classical_v2.joblib`
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
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 940 | 148 | 1167 | 375 | 80.11% | 86.40% | 71.48% | 78.24% | 11.25% | 88.75% | 80.11% | 0.6115 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 1003 | 227 | 1088 | 312 | 79.51% | 81.54% | 76.27% | 78.82% | 17.26% | 82.74% | 79.51% | 0.5914 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 968 | 208 | 1107 | 347 | 78.90% | 82.31% | 73.61% | 77.72% | 15.82% | 84.18% | 78.90% | 0.5812 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 1043 | 283 | 1032 | 272 | 78.90% | 78.66% | 79.32% | 78.99% | 21.52% | 78.48% | 78.90% | 0.5780 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 973 | 217 | 1098 | 342 | 78.75% | 81.76% | 73.99% | 77.68% | 16.50% | 83.50% | 78.75% | 0.5775 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 949 | 199 | 1116 | 366 | 78.52% | 82.67% | 72.17% | 77.06% | 15.13% | 84.87% | 78.52% | 0.5750 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 967 | 217 | 1098 | 348 | 78.52% | 81.67% | 73.54% | 77.39% | 16.50% | 83.50% | 78.52% | 0.5732 |
| `sgd_log_loss_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 974 | 231 | 1084 | 341 | 78.25% | 80.83% | 74.07% | 77.30% | 17.57% | 82.43% | 78.25% | 0.5670 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 959 | 221 | 1094 | 356 | 78.06% | 81.27% | 72.93% | 76.87% | 16.81% | 83.19% | 78.06% | 0.5642 |
| `logreg_balanced` | `word_char_tfidf` | `code_diff_only` | 958 | 226 | 1089 | 357 | 77.83% | 80.91% | 72.85% | 76.67% | 17.19% | 82.81% | 77.83% | 0.5594 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `code_diff_only` | 985 | 253 | 1062 | 330 | 77.83% | 79.56% | 74.90% | 77.16% | 19.24% | 80.76% | 77.83% | 0.5576 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 858 | 146 | 1169 | 457 | 77.07% | 85.46% | 65.25% | 74.00% | 11.10% | 88.90% | 77.07% | 0.5573 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 981 | 252 | 1063 | 334 | 77.72% | 79.56% | 74.60% | 77.00% | 19.16% | 80.84% | 77.72% | 0.5555 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 990 | 262 | 1053 | 325 | 77.68% | 79.07% | 75.29% | 77.13% | 19.92% | 80.08% | 77.68% | 0.5542 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 982 | 267 | 1048 | 333 | 77.19% | 78.62% | 74.68% | 76.60% | 20.30% | 79.70% | 77.19% | 0.5444 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 939 | 228 | 1087 | 376 | 77.03% | 80.46% | 71.41% | 75.66% | 17.34% | 82.66% | 77.03% | 0.5441 |
| `linear_svc_balanced` | `word_char_tfidf` | `code_diff_only` | 979 | 272 | 1043 | 336 | 76.88% | 78.26% | 74.45% | 76.31% | 20.68% | 79.32% | 76.88% | 0.5383 |
| `sgd_log_loss_balanced` | `char_tfidf` | `code_diff_only` | 969 | 271 | 1044 | 346 | 76.54% | 78.15% | 73.69% | 75.85% | 20.61% | 79.39% | 76.54% | 0.5317 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 959 | 268 | 1047 | 356 | 76.27% | 78.16% | 72.93% | 75.45% | 20.38% | 79.62% | 76.27% | 0.5267 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 998 | 308 | 1007 | 317 | 76.24% | 76.42% | 75.89% | 76.15% | 23.42% | 76.58% | 76.24% | 0.5247 |
| `logreg_balanced` | `char_tfidf` | `code_diff_only` | 939 | 258 | 1057 | 376 | 75.89% | 78.45% | 71.41% | 74.76% | 19.62% | 80.38% | 75.89% | 0.5200 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 1016 | 334 | 981 | 299 | 75.93% | 75.26% | 77.26% | 76.25% | 25.40% | 74.60% | 75.93% | 0.5188 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `code_diff_only` | 974 | 294 | 1021 | 341 | 75.86% | 76.81% | 74.07% | 75.42% | 22.36% | 77.64% | 75.86% | 0.5174 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 966 | 288 | 1027 | 349 | 75.78% | 77.03% | 73.46% | 75.20% | 21.90% | 78.10% | 75.78% | 0.5161 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 908 | 237 | 1078 | 407 | 75.51% | 79.30% | 69.05% | 73.82% | 18.02% | 81.98% | 75.51% | 0.5146 |
| `sgd_log_loss_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 924 | 257 | 1058 | 391 | 75.36% | 78.24% | 70.27% | 74.04% | 19.54% | 80.46% | 75.36% | 0.5099 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 1010 | 343 | 972 | 305 | 75.36% | 74.65% | 76.81% | 75.71% | 26.08% | 73.92% | 75.36% | 0.5074 |
| `linear_svc_balanced` | `char_tfidf` | `code_diff_only` | 968 | 308 | 1007 | 347 | 75.10% | 75.86% | 73.61% | 74.72% | 23.42% | 76.58% | 75.10% | 0.5021 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 932 | 276 | 1039 | 383 | 74.94% | 77.15% | 70.87% | 73.88% | 20.99% | 79.01% | 74.94% | 0.5005 |
| `complement_nb` | `word_char_tfidf` | `old_comment_plus_code_diff` | 900 | 250 | 1065 | 415 | 74.71% | 78.26% | 68.44% | 73.02% | 19.01% | 80.99% | 74.71% | 0.4982 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 866 | 233 | 1082 | 449 | 74.07% | 78.80% | 65.86% | 71.75% | 17.72% | 82.28% | 74.07% | 0.4880 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `code_diff_only` | 964 | 324 | 991 | 351 | 74.33% | 74.84% | 73.31% | 74.07% | 24.64% | 75.36% | 74.33% | 0.4868 |
| `logreg_balanced` | `word_tfidf` | `code_diff_only` | 900 | 272 | 1043 | 415 | 73.88% | 76.79% | 68.44% | 72.38% | 20.68% | 79.32% | 73.88% | 0.4804 |
| `sgd_log_loss_balanced` | `word_tfidf` | `code_diff_only` | 935 | 314 | 1001 | 380 | 73.61% | 74.86% | 71.10% | 72.93% | 23.88% | 76.12% | 73.61% | 0.4728 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 913 | 295 | 1020 | 402 | 73.50% | 75.58% | 69.43% | 72.37% | 22.43% | 77.57% | 73.50% | 0.4715 |
| `linear_svc_balanced` | `word_tfidf` | `code_diff_only` | 926 | 317 | 998 | 389 | 73.16% | 74.50% | 70.42% | 72.40% | 24.11% | 75.89% | 73.16% | 0.4638 |
| `complement_nb` | `word_char_tfidf` | `code_diff_only` | 905 | 306 | 1009 | 410 | 72.78% | 74.73% | 68.82% | 71.65% | 23.27% | 76.73% | 72.78% | 0.4569 |
| `complement_nb` | `word_tfidf` | `old_comment_plus_code_diff` | 782 | 202 | 1113 | 533 | 72.05% | 79.47% | 59.47% | 68.03% | 15.36% | 84.64% | 72.05% | 0.4557 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 932 | 335 | 980 | 383 | 72.70% | 73.56% | 70.87% | 72.19% | 25.48% | 74.52% | 72.70% | 0.4543 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 849 | 264 | 1051 | 466 | 72.24% | 76.28% | 64.56% | 69.93% | 20.08% | 79.92% | 72.24% | 0.4502 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 901 | 313 | 1002 | 414 | 72.36% | 74.22% | 68.52% | 71.25% | 23.80% | 76.20% | 72.36% | 0.4485 |
| `complement_nb` | `char_tfidf` | `old_comment_plus_code_diff` | 921 | 339 | 976 | 394 | 72.13% | 73.10% | 70.04% | 71.53% | 25.78% | 74.22% | 72.13% | 0.4430 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 899 | 321 | 994 | 416 | 71.98% | 73.69% | 68.37% | 70.93% | 24.41% | 75.59% | 71.98% | 0.4407 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | 809 | 242 | 1073 | 506 | 71.56% | 76.97% | 61.52% | 68.39% | 18.40% | 81.60% | 71.56% | 0.4401 |
| `sgd_log_loss_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | 850 | 281 | 1034 | 465 | 71.63% | 75.15% | 64.64% | 69.50% | 21.37% | 78.63% | 71.63% | 0.4370 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `code_diff_only` | 910 | 344 | 971 | 405 | 71.52% | 72.57% | 69.20% | 70.84% | 26.16% | 73.84% | 71.52% | 0.4309 |
| `sgd_log_loss_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | 871 | 309 | 1006 | 444 | 71.37% | 73.81% | 66.24% | 69.82% | 23.50% | 76.50% | 71.37% | 0.4296 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | 861 | 302 | 1013 | 454 | 71.25% | 74.03% | 65.48% | 69.49% | 22.97% | 77.03% | 71.25% | 0.4280 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | 864 | 309 | 1006 | 451 | 71.10% | 73.66% | 65.70% | 69.45% | 23.50% | 76.50% | 71.10% | 0.4245 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 903 | 347 | 968 | 412 | 71.14% | 72.24% | 68.67% | 70.41% | 26.39% | 73.61% | 71.14% | 0.4233 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | 892 | 346 | 969 | 423 | 70.76% | 72.05% | 67.83% | 69.88% | 26.31% | 73.69% | 70.76% | 0.4159 |
| `complement_nb` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 888 | 348 | 967 | 427 | 70.53% | 71.84% | 67.53% | 69.62% | 26.46% | 73.54% | 70.53% | 0.4114 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 930 | 392 | 923 | 385 | 70.46% | 70.35% | 70.72% | 70.53% | 29.81% | 70.19% | 70.46% | 0.4091 |
| `complement_nb` | `word_tfidf` | `code_diff_only` | 786 | 260 | 1055 | 529 | 70.00% | 75.14% | 59.77% | 66.58% | 19.77% | 80.23% | 70.00% | 0.4086 |
| `complement_nb` | `char_tfidf` | `code_diff_only` | 930 | 393 | 922 | 385 | 70.42% | 70.29% | 70.72% | 70.51% | 29.89% | 70.11% | 70.42% | 0.4084 |
| `complement_nb` | `word_tfidf` | `old_comment_plus_old_new_code` | 858 | 324 | 991 | 457 | 70.30% | 72.59% | 65.25% | 68.72% | 24.64% | 75.36% | 70.30% | 0.4082 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | 883 | 354 | 961 | 432 | 70.11% | 71.38% | 67.15% | 69.20% | 26.92% | 73.08% | 70.11% | 0.4030 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | 869 | 377 | 938 | 446 | 68.71% | 69.74% | 66.08% | 67.86% | 28.67% | 71.33% | 68.71% | 0.3747 |
| `complement_nb` | `char_tfidf` | `old_comment_plus_old_new_code` | 882 | 423 | 892 | 433 | 67.45% | 67.59% | 67.07% | 67.33% | 32.17% | 67.83% | 67.45% | 0.3491 |

## Test Metrics

| Model | Feature set | Input mode | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 1017 | 273 | 1180 | 436 | 75.60% | 78.84% | 69.99% | 74.15% | 18.79% | 81.21% | 75.60% | 0.5153 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 950 | 245 | 1208 | 503 | 74.26% | 79.50% | 65.38% | 71.75% | 16.86% | 83.14% | 74.26% | 0.4930 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 1020 | 331 | 1122 | 433 | 73.71% | 75.50% | 70.20% | 72.75% | 22.78% | 77.22% | 73.71% | 0.4754 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 998 | 309 | 1144 | 455 | 73.71% | 76.36% | 68.69% | 72.32% | 21.27% | 78.73% | 73.71% | 0.4766 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 1057 | 410 | 1043 | 396 | 72.26% | 72.05% | 72.75% | 72.40% | 28.22% | 71.78% | 72.26% | 0.4453 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 987 | 325 | 1128 | 466 | 72.78% | 75.23% | 67.93% | 71.39% | 22.37% | 77.63% | 72.78% | 0.4578 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 985 | 305 | 1148 | 468 | 73.40% | 76.36% | 67.79% | 71.82% | 20.99% | 79.01% | 73.40% | 0.4710 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 1021 | 279 | 1174 | 432 | 75.53% | 78.54% | 70.27% | 74.17% | 19.20% | 80.80% | 75.53% | 0.5135 |
| `sgd_log_loss_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 1001 | 358 | 1095 | 452 | 72.13% | 73.66% | 68.89% | 71.19% | 24.64% | 75.36% | 72.13% | 0.4435 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 990 | 335 | 1118 | 463 | 72.54% | 74.72% | 68.13% | 71.27% | 23.06% | 76.94% | 72.54% | 0.4526 |
| `logreg_balanced` | `word_char_tfidf` | `code_diff_only` | 990 | 287 | 1166 | 463 | 74.19% | 77.53% | 68.13% | 72.53% | 19.75% | 80.25% | 74.19% | 0.4874 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `code_diff_only` | 1007 | 362 | 1091 | 446 | 72.20% | 73.56% | 69.30% | 71.37% | 24.91% | 75.09% | 72.20% | 0.4447 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 868 | 238 | 1215 | 585 | 71.68% | 78.48% | 59.74% | 67.84% | 16.38% | 83.62% | 71.68% | 0.4465 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 1011 | 344 | 1109 | 442 | 72.95% | 74.61% | 69.58% | 72.01% | 23.68% | 76.32% | 72.95% | 0.4601 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 992 | 348 | 1105 | 461 | 72.16% | 74.03% | 68.27% | 71.03% | 23.95% | 76.05% | 72.16% | 0.4446 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 998 | 399 | 1054 | 455 | 70.61% | 71.44% | 68.69% | 70.04% | 27.46% | 72.54% | 70.61% | 0.4126 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 968 | 322 | 1131 | 485 | 72.23% | 75.04% | 66.62% | 70.58% | 22.16% | 77.84% | 72.23% | 0.4474 |
| `linear_svc_balanced` | `word_char_tfidf` | `code_diff_only` | 987 | 368 | 1085 | 466 | 71.30% | 72.84% | 67.93% | 70.30% | 25.33% | 74.67% | 71.30% | 0.4270 |
| `sgd_log_loss_balanced` | `char_tfidf` | `code_diff_only` | 1011 | 377 | 1076 | 442 | 71.82% | 72.84% | 69.58% | 71.17% | 25.95% | 74.05% | 71.82% | 0.4368 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 977 | 383 | 1070 | 476 | 70.44% | 71.84% | 67.24% | 69.46% | 26.36% | 73.64% | 70.44% | 0.4096 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | 1001 | 402 | 1051 | 452 | 70.61% | 71.35% | 68.89% | 70.10% | 27.67% | 72.33% | 70.61% | 0.4125 |
| `logreg_balanced` | `char_tfidf` | `code_diff_only` | 972 | 336 | 1117 | 481 | 71.89% | 74.31% | 66.90% | 70.41% | 23.12% | 76.88% | 71.89% | 0.4399 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 1047 | 419 | 1034 | 406 | 71.61% | 71.42% | 72.06% | 71.74% | 28.84% | 71.16% | 71.61% | 0.4322 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `code_diff_only` | 989 | 375 | 1078 | 464 | 71.13% | 72.51% | 68.07% | 70.22% | 25.81% | 74.19% | 71.13% | 0.4234 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | 982 | 397 | 1056 | 471 | 70.13% | 71.21% | 67.58% | 69.35% | 27.32% | 72.68% | 70.13% | 0.4031 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | 856 | 367 | 1086 | 597 | 66.83% | 69.99% | 58.91% | 63.98% | 25.26% | 74.74% | 66.83% | 0.3408 |
| `sgd_log_loss_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 907 | 380 | 1073 | 546 | 68.13% | 70.47% | 62.42% | 66.20% | 26.15% | 73.85% | 68.13% | 0.3651 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 1029 | 491 | 962 | 424 | 68.51% | 67.70% | 70.82% | 69.22% | 33.79% | 66.21% | 68.51% | 0.3707 |
| `linear_svc_balanced` | `char_tfidf` | `code_diff_only` | 1012 | 404 | 1049 | 441 | 70.92% | 71.47% | 69.65% | 70.55% | 27.80% | 72.20% | 70.92% | 0.4186 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 905 | 408 | 1045 | 548 | 67.10% | 68.93% | 62.28% | 65.44% | 28.08% | 71.92% | 67.10% | 0.3436 |
| `complement_nb` | `word_char_tfidf` | `old_comment_plus_code_diff` | 845 | 368 | 1085 | 608 | 66.41% | 69.66% | 58.16% | 63.39% | 25.33% | 74.67% | 66.41% | 0.3329 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 882 | 329 | 1124 | 571 | 69.03% | 72.83% | 60.70% | 66.22% | 22.64% | 77.36% | 69.03% | 0.3860 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `code_diff_only` | 1006 | 448 | 1005 | 447 | 69.20% | 69.19% | 69.24% | 69.21% | 30.83% | 69.17% | 69.20% | 0.3840 |
| `logreg_balanced` | `word_tfidf` | `code_diff_only` | 899 | 328 | 1125 | 554 | 69.65% | 73.27% | 61.87% | 67.09% | 22.57% | 77.43% | 69.65% | 0.3978 |
| `sgd_log_loss_balanced` | `word_tfidf` | `code_diff_only` | 916 | 412 | 1041 | 537 | 67.34% | 68.98% | 63.04% | 65.88% | 28.36% | 71.64% | 67.34% | 0.3482 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | 890 | 420 | 1033 | 563 | 66.17% | 67.94% | 61.25% | 64.42% | 28.91% | 71.09% | 66.17% | 0.3250 |
| `linear_svc_balanced` | `word_tfidf` | `code_diff_only` | 893 | 422 | 1031 | 560 | 66.21% | 67.91% | 61.46% | 64.52% | 29.04% | 70.96% | 66.21% | 0.3256 |
| `complement_nb` | `word_char_tfidf` | `code_diff_only` | 893 | 417 | 1036 | 560 | 66.38% | 68.17% | 61.46% | 64.64% | 28.70% | 71.30% | 66.38% | 0.3292 |
| `complement_nb` | `word_tfidf` | `old_comment_plus_code_diff` | 707 | 345 | 1108 | 746 | 62.46% | 67.21% | 48.66% | 56.45% | 23.74% | 76.26% | 62.46% | 0.2592 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | 903 | 428 | 1025 | 550 | 66.35% | 67.84% | 62.15% | 64.87% | 29.46% | 70.54% | 66.35% | 0.3281 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 872 | 399 | 1054 | 581 | 66.28% | 68.61% | 60.01% | 64.02% | 27.46% | 72.54% | 66.28% | 0.3281 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 928 | 481 | 972 | 525 | 65.38% | 65.86% | 63.87% | 64.85% | 33.10% | 66.90% | 65.38% | 0.3078 |
| `complement_nb` | `char_tfidf` | `old_comment_plus_code_diff` | 890 | 430 | 1023 | 563 | 65.83% | 67.42% | 61.25% | 64.19% | 29.59% | 70.41% | 65.83% | 0.3179 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 904 | 484 | 969 | 549 | 64.45% | 65.13% | 62.22% | 63.64% | 33.31% | 66.69% | 64.45% | 0.2893 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | 808 | 357 | 1096 | 645 | 65.52% | 69.36% | 55.61% | 61.73% | 24.57% | 75.43% | 65.52% | 0.3167 |
| `sgd_log_loss_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | 849 | 419 | 1034 | 604 | 64.80% | 66.96% | 58.43% | 62.40% | 28.84% | 71.16% | 64.80% | 0.2984 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `code_diff_only` | 835 | 404 | 1049 | 618 | 64.83% | 67.39% | 57.47% | 62.04% | 27.80% | 72.20% | 64.83% | 0.2999 |
| `sgd_log_loss_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | 864 | 497 | 956 | 589 | 62.63% | 63.48% | 59.46% | 61.41% | 34.21% | 65.79% | 62.63% | 0.2531 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | 854 | 451 | 1002 | 599 | 63.87% | 65.44% | 58.77% | 61.93% | 31.04% | 68.96% | 63.87% | 0.2788 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | 858 | 455 | 998 | 595 | 63.87% | 65.35% | 59.05% | 62.04% | 31.31% | 68.69% | 63.87% | 0.2787 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | 886 | 460 | 993 | 567 | 64.66% | 65.82% | 60.98% | 63.31% | 31.66% | 68.34% | 64.66% | 0.2940 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | 877 | 538 | 915 | 576 | 61.67% | 61.98% | 60.36% | 61.16% | 37.03% | 62.97% | 61.67% | 0.2334 |
| `complement_nb` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 870 | 454 | 999 | 583 | 64.32% | 65.71% | 59.88% | 62.66% | 31.25% | 68.75% | 64.32% | 0.2874 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | 936 | 535 | 918 | 517 | 63.80% | 63.63% | 64.42% | 64.02% | 36.82% | 63.18% | 63.80% | 0.2760 |
| `complement_nb` | `word_tfidf` | `code_diff_only` | 753 | 412 | 1041 | 700 | 61.73% | 64.64% | 51.82% | 57.52% | 28.36% | 71.64% | 61.73% | 0.2394 |
| `complement_nb` | `char_tfidf` | `code_diff_only` | 912 | 472 | 981 | 541 | 65.14% | 65.90% | 62.77% | 64.29% | 32.48% | 67.52% | 65.14% | 0.3032 |
| `complement_nb` | `word_tfidf` | `old_comment_plus_old_new_code` | 856 | 460 | 993 | 597 | 63.63% | 65.05% | 58.91% | 61.83% | 31.66% | 68.34% | 63.63% | 0.2738 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | 870 | 492 | 961 | 583 | 63.01% | 63.88% | 59.88% | 61.81% | 33.86% | 66.14% | 63.01% | 0.2607 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | 835 | 540 | 913 | 618 | 60.15% | 60.73% | 57.47% | 59.05% | 37.16% | 62.84% | 60.15% | 0.2033 |
| `complement_nb` | `char_tfidf` | `old_comment_plus_old_new_code` | 849 | 499 | 954 | 604 | 62.04% | 62.98% | 58.43% | 60.62% | 34.34% | 65.66% | 62.04% | 0.2415 |

## Per-Subset Test Metrics

| Model | Feature set | Input mode | Subset | TP | FP | TN | FN | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Return` | 679 | 132 | 788 | 241 | 79.73% | 83.72% | 73.80% | 78.45% | 14.35% | 85.65% | 79.73% | 0.5988 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Summary` | 338 | 141 | 392 | 195 | 68.48% | 70.56% | 63.41% | 66.80% | 26.45% | 73.55% | 68.48% | 0.3715 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Return` | 667 | 125 | 795 | 253 | 79.46% | 84.22% | 72.50% | 77.92% | 13.59% | 86.41% | 79.46% | 0.5949 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Summary` | 283 | 120 | 413 | 250 | 65.29% | 70.22% | 53.10% | 60.47% | 22.51% | 77.49% | 65.29% | 0.3153 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Return` | 698 | 179 | 741 | 222 | 78.21% | 79.59% | 75.87% | 77.69% | 19.46% | 80.54% | 78.21% | 0.5647 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Summary` | 322 | 152 | 381 | 211 | 65.95% | 67.93% | 60.41% | 63.95% | 28.52% | 71.48% | 65.95% | 0.3209 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Return` | 696 | 198 | 722 | 224 | 77.07% | 77.85% | 75.65% | 76.74% | 21.52% | 78.48% | 77.07% | 0.5415 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Summary` | 302 | 111 | 422 | 231 | 67.92% | 73.12% | 56.66% | 63.85% | 20.83% | 79.17% | 67.92% | 0.3678 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Return` | 733 | 236 | 684 | 187 | 77.01% | 75.64% | 79.67% | 77.61% | 25.65% | 74.35% | 77.01% | 0.5410 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Summary` | 324 | 174 | 359 | 209 | 64.07% | 65.06% | 60.79% | 62.85% | 32.65% | 67.35% | 64.07% | 0.2820 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Return` | 688 | 175 | 745 | 232 | 77.88% | 79.72% | 74.78% | 77.17% | 19.02% | 80.98% | 77.88% | 0.5587 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 299 | 150 | 383 | 234 | 63.98% | 66.59% | 56.10% | 60.90% | 28.14% | 71.86% | 63.98% | 0.2831 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Return` | 683 | 156 | 764 | 237 | 78.64% | 81.41% | 74.24% | 77.66% | 16.96% | 83.04% | 78.64% | 0.5751 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 302 | 149 | 384 | 231 | 64.35% | 66.96% | 56.66% | 61.38% | 27.95% | 72.05% | 64.35% | 0.2905 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Return` | 700 | 173 | 747 | 220 | 78.64% | 80.18% | 76.09% | 78.08% | 18.80% | 81.20% | 78.64% | 0.5736 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Summary` | 321 | 106 | 427 | 212 | 70.17% | 75.18% | 60.23% | 66.88% | 19.89% | 80.11% | 70.17% | 0.4116 |
| `sgd_log_loss_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Return` | 678 | 195 | 725 | 242 | 76.25% | 77.66% | 73.70% | 75.63% | 21.20% | 78.80% | 76.25% | 0.5257 |
| `sgd_log_loss_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 323 | 163 | 370 | 210 | 65.01% | 66.46% | 60.60% | 63.40% | 30.58% | 69.42% | 65.01% | 0.3014 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Return` | 674 | 189 | 731 | 246 | 76.36% | 78.10% | 73.26% | 75.60% | 20.54% | 79.46% | 76.36% | 0.5282 |
| `logreg_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Summary` | 316 | 146 | 387 | 217 | 65.95% | 68.40% | 59.29% | 63.52% | 27.39% | 72.61% | 65.95% | 0.3218 |
| `logreg_balanced` | `word_char_tfidf` | `code_diff_only` | `Return` | 700 | 181 | 739 | 220 | 78.21% | 79.46% | 76.09% | 77.73% | 19.67% | 80.33% | 78.21% | 0.5646 |
| `logreg_balanced` | `word_char_tfidf` | `code_diff_only` | `Summary` | 290 | 106 | 427 | 243 | 67.26% | 73.23% | 54.41% | 62.43% | 19.89% | 80.11% | 67.26% | 0.3572 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `code_diff_only` | `Return` | 706 | 231 | 689 | 214 | 75.82% | 75.35% | 76.74% | 76.04% | 25.11% | 74.89% | 75.82% | 0.5164 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `code_diff_only` | `Summary` | 301 | 131 | 402 | 232 | 65.95% | 69.68% | 56.47% | 62.38% | 24.58% | 75.42% | 65.95% | 0.3248 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Return` | 611 | 139 | 781 | 309 | 75.65% | 81.47% | 66.41% | 73.17% | 15.11% | 84.89% | 75.65% | 0.5220 |
| `sgd_log_loss_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Summary` | 257 | 99 | 434 | 276 | 64.82% | 72.19% | 48.22% | 57.82% | 18.57% | 81.43% | 64.82% | 0.3143 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Return` | 704 | 211 | 709 | 216 | 76.79% | 76.94% | 76.52% | 76.73% | 22.93% | 77.07% | 76.79% | 0.5359 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Summary` | 307 | 133 | 400 | 226 | 66.32% | 69.77% | 57.60% | 63.10% | 24.95% | 75.05% | 66.32% | 0.3315 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Return` | 690 | 185 | 735 | 230 | 77.45% | 78.86% | 75.00% | 76.88% | 20.11% | 79.89% | 77.45% | 0.5496 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 302 | 163 | 370 | 231 | 63.04% | 64.95% | 56.66% | 60.52% | 30.58% | 69.42% | 63.04% | 0.2629 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Return` | 682 | 226 | 694 | 238 | 74.78% | 75.11% | 74.13% | 74.62% | 24.57% | 75.43% | 74.78% | 0.4957 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 316 | 173 | 360 | 217 | 63.41% | 64.62% | 59.29% | 61.84% | 32.46% | 67.54% | 63.41% | 0.2692 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Return` | 667 | 177 | 743 | 253 | 76.63% | 79.03% | 72.50% | 75.62% | 19.24% | 80.76% | 76.63% | 0.5344 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 301 | 145 | 388 | 232 | 64.63% | 67.49% | 56.47% | 61.49% | 27.20% | 72.80% | 64.63% | 0.2967 |
| `linear_svc_balanced` | `word_char_tfidf` | `code_diff_only` | `Return` | 701 | 233 | 687 | 219 | 75.43% | 75.05% | 76.20% | 75.62% | 25.33% | 74.67% | 75.43% | 0.5088 |
| `linear_svc_balanced` | `word_char_tfidf` | `code_diff_only` | `Summary` | 286 | 135 | 398 | 247 | 64.17% | 67.93% | 53.66% | 59.96% | 25.33% | 74.67% | 64.17% | 0.2898 |
| `sgd_log_loss_balanced` | `char_tfidf` | `code_diff_only` | `Return` | 706 | 242 | 678 | 214 | 75.22% | 74.47% | 76.74% | 75.59% | 26.30% | 73.70% | 75.22% | 0.5046 |
| `sgd_log_loss_balanced` | `char_tfidf` | `code_diff_only` | `Summary` | 305 | 135 | 398 | 228 | 65.95% | 69.32% | 57.22% | 62.69% | 25.33% | 74.67% | 65.95% | 0.3239 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Return` | 674 | 226 | 694 | 246 | 74.35% | 74.89% | 73.26% | 74.07% | 24.57% | 75.43% | 74.35% | 0.4871 |
| `linear_svc_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Summary` | 303 | 157 | 376 | 230 | 63.70% | 65.87% | 56.85% | 61.03% | 29.46% | 70.54% | 63.70% | 0.2765 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Return` | 701 | 228 | 692 | 219 | 75.71% | 75.46% | 76.20% | 75.82% | 24.78% | 75.22% | 75.71% | 0.5142 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 300 | 174 | 359 | 233 | 61.82% | 63.29% | 56.29% | 59.58% | 32.65% | 67.35% | 61.82% | 0.2379 |
| `logreg_balanced` | `char_tfidf` | `code_diff_only` | `Return` | 682 | 214 | 706 | 238 | 75.43% | 76.12% | 74.13% | 75.11% | 23.26% | 76.74% | 75.43% | 0.5089 |
| `logreg_balanced` | `char_tfidf` | `code_diff_only` | `Summary` | 290 | 122 | 411 | 243 | 65.76% | 70.39% | 54.41% | 61.38% | 22.89% | 77.11% | 65.76% | 0.3236 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Return` | 713 | 268 | 652 | 207 | 74.18% | 72.68% | 77.50% | 75.01% | 29.13% | 70.87% | 74.18% | 0.4848 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Summary` | 334 | 151 | 382 | 199 | 67.17% | 68.87% | 62.66% | 65.62% | 28.33% | 71.67% | 67.17% | 0.3447 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `code_diff_only` | `Return` | 703 | 238 | 682 | 217 | 75.27% | 74.71% | 76.41% | 75.55% | 25.87% | 74.13% | 75.27% | 0.5056 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `code_diff_only` | `Summary` | 286 | 137 | 396 | 247 | 63.98% | 67.61% | 53.66% | 59.83% | 25.70% | 74.30% | 63.98% | 0.2857 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Return` | 688 | 236 | 684 | 232 | 74.57% | 74.46% | 74.78% | 74.62% | 25.65% | 74.35% | 74.57% | 0.4913 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 294 | 161 | 372 | 239 | 62.48% | 64.62% | 55.16% | 59.51% | 30.21% | 69.79% | 62.48% | 0.2522 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Return` | 674 | 234 | 686 | 246 | 73.91% | 74.23% | 73.26% | 73.74% | 25.43% | 74.57% | 73.91% | 0.4783 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_code_diff` | `Summary` | 182 | 133 | 400 | 351 | 54.60% | 57.78% | 34.15% | 42.92% | 24.95% | 75.05% | 54.60% | 0.1007 |
| `sgd_log_loss_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Return` | 643 | 224 | 696 | 277 | 72.77% | 74.16% | 69.89% | 71.96% | 24.35% | 75.65% | 72.77% | 0.4562 |
| `sgd_log_loss_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Summary` | 264 | 156 | 377 | 269 | 60.13% | 62.86% | 49.53% | 55.40% | 29.27% | 70.73% | 60.13% | 0.2073 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Return` | 692 | 296 | 624 | 228 | 71.52% | 70.04% | 75.22% | 72.54% | 32.17% | 67.83% | 71.52% | 0.4316 |
| `sgd_modified_huber_balanced` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Summary` | 337 | 195 | 338 | 196 | 63.32% | 63.35% | 63.23% | 63.29% | 36.59% | 63.41% | 63.32% | 0.2664 |
| `linear_svc_balanced` | `char_tfidf` | `code_diff_only` | `Return` | 706 | 261 | 659 | 214 | 74.18% | 73.01% | 76.74% | 74.83% | 28.37% | 71.63% | 74.18% | 0.4843 |
| `linear_svc_balanced` | `char_tfidf` | `code_diff_only` | `Summary` | 306 | 143 | 390 | 227 | 65.29% | 68.15% | 57.41% | 62.32% | 26.83% | 73.17% | 65.29% | 0.3097 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Return` | 645 | 236 | 684 | 275 | 72.23% | 73.21% | 70.11% | 71.63% | 25.65% | 74.35% | 72.23% | 0.4450 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Summary` | 260 | 172 | 361 | 273 | 58.26% | 60.19% | 48.78% | 53.89% | 32.27% | 67.73% | 58.26% | 0.1681 |
| `complement_nb` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Return` | 665 | 230 | 690 | 255 | 73.64% | 74.30% | 72.28% | 73.28% | 25.00% | 75.00% | 73.64% | 0.4730 |
| `complement_nb` | `word_char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 180 | 138 | 395 | 353 | 53.94% | 56.60% | 33.77% | 42.30% | 25.89% | 74.11% | 53.94% | 0.0861 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Return` | 628 | 186 | 734 | 292 | 74.02% | 77.15% | 68.26% | 72.43% | 20.22% | 79.78% | 74.02% | 0.4837 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Summary` | 254 | 143 | 390 | 279 | 60.41% | 63.98% | 47.65% | 54.62% | 26.83% | 73.17% | 60.41% | 0.2154 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `code_diff_only` | `Return` | 705 | 286 | 634 | 215 | 72.77% | 71.14% | 76.63% | 73.78% | 31.09% | 68.91% | 72.77% | 0.4568 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `code_diff_only` | `Summary` | 301 | 162 | 371 | 232 | 63.04% | 65.01% | 56.47% | 60.44% | 30.39% | 69.61% | 63.04% | 0.2631 |
| `logreg_balanced` | `word_tfidf` | `code_diff_only` | `Return` | 642 | 201 | 719 | 278 | 73.97% | 76.16% | 69.78% | 72.83% | 21.85% | 78.15% | 73.97% | 0.4810 |
| `logreg_balanced` | `word_tfidf` | `code_diff_only` | `Summary` | 257 | 127 | 406 | 276 | 62.20% | 66.93% | 48.22% | 56.05% | 23.83% | 76.17% | 62.20% | 0.2540 |
| `sgd_log_loss_balanced` | `word_tfidf` | `code_diff_only` | `Return` | 647 | 254 | 666 | 273 | 71.36% | 71.81% | 70.33% | 71.06% | 27.61% | 72.39% | 71.36% | 0.4273 |
| `sgd_log_loss_balanced` | `word_tfidf` | `code_diff_only` | `Summary` | 269 | 158 | 375 | 264 | 60.41% | 63.00% | 50.47% | 56.04% | 29.64% | 70.36% | 60.41% | 0.2125 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Return` | 666 | 260 | 660 | 254 | 72.07% | 71.92% | 72.39% | 72.16% | 28.26% | 71.74% | 72.07% | 0.4413 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `code_diff_only` | `Summary` | 224 | 160 | 373 | 309 | 56.00% | 58.33% | 42.03% | 48.85% | 30.02% | 69.98% | 56.00% | 0.1251 |
| `linear_svc_balanced` | `word_tfidf` | `code_diff_only` | `Return` | 637 | 258 | 662 | 283 | 70.60% | 71.17% | 69.24% | 70.19% | 28.04% | 71.96% | 70.60% | 0.4121 |
| `linear_svc_balanced` | `word_tfidf` | `code_diff_only` | `Summary` | 256 | 164 | 369 | 277 | 58.63% | 60.95% | 48.03% | 53.73% | 30.77% | 69.23% | 58.63% | 0.1766 |
| `complement_nb` | `word_char_tfidf` | `code_diff_only` | `Return` | 665 | 255 | 665 | 255 | 72.28% | 72.28% | 72.28% | 72.28% | 27.72% | 72.28% | 72.28% | 0.4457 |
| `complement_nb` | `word_char_tfidf` | `code_diff_only` | `Summary` | 228 | 162 | 371 | 305 | 56.19% | 58.46% | 42.78% | 49.40% | 30.39% | 69.61% | 56.19% | 0.1285 |
| `complement_nb` | `word_tfidf` | `old_comment_plus_code_diff` | `Return` | 555 | 220 | 700 | 365 | 68.21% | 71.61% | 60.33% | 65.49% | 23.91% | 76.09% | 68.21% | 0.3687 |
| `complement_nb` | `word_tfidf` | `old_comment_plus_code_diff` | `Summary` | 152 | 125 | 408 | 381 | 52.53% | 54.87% | 28.52% | 37.53% | 23.45% | 76.55% | 52.53% | 0.0578 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Return` | 652 | 249 | 671 | 268 | 71.90% | 72.36% | 70.87% | 71.61% | 27.07% | 72.93% | 71.90% | 0.4381 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `old_comment_plus_code_diff` | `Summary` | 251 | 179 | 354 | 282 | 56.75% | 58.37% | 47.09% | 52.13% | 33.58% | 66.42% | 56.75% | 0.1377 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 627 | 224 | 696 | 293 | 71.90% | 73.68% | 68.15% | 70.81% | 24.35% | 75.65% | 71.90% | 0.4393 |
| `logreg_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 245 | 175 | 358 | 288 | 56.57% | 58.33% | 45.97% | 51.42% | 32.83% | 67.17% | 56.57% | 0.1344 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 656 | 281 | 639 | 264 | 70.38% | 70.01% | 71.30% | 70.65% | 30.54% | 69.46% | 70.38% | 0.4077 |
| `sgd_log_loss_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 272 | 200 | 333 | 261 | 56.75% | 57.63% | 51.03% | 54.13% | 37.52% | 62.48% | 56.75% | 0.1360 |
| `complement_nb` | `char_tfidf` | `old_comment_plus_code_diff` | `Return` | 683 | 272 | 648 | 237 | 72.34% | 71.52% | 74.24% | 72.85% | 29.57% | 70.43% | 72.34% | 0.4471 |
| `complement_nb` | `char_tfidf` | `old_comment_plus_code_diff` | `Summary` | 207 | 158 | 375 | 326 | 54.60% | 56.71% | 38.84% | 46.10% | 29.64% | 70.36% | 54.60% | 0.0969 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 639 | 286 | 634 | 281 | 69.18% | 69.08% | 69.46% | 69.27% | 31.09% | 68.91% | 69.18% | 0.3837 |
| `linear_svc_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 265 | 198 | 335 | 268 | 56.29% | 57.24% | 49.72% | 53.21% | 37.15% | 62.85% | 56.29% | 0.1268 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | `Return` | 599 | 197 | 723 | 321 | 71.85% | 75.25% | 65.11% | 69.81% | 21.41% | 78.59% | 71.85% | 0.4410 |
| `logreg_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 209 | 160 | 373 | 324 | 54.60% | 56.64% | 39.21% | 46.34% | 30.02% | 69.98% | 54.60% | 0.0966 |
| `sgd_log_loss_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | `Return` | 624 | 236 | 684 | 296 | 71.09% | 72.56% | 67.83% | 70.11% | 25.65% | 74.35% | 71.09% | 0.4226 |
| `sgd_log_loss_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 225 | 183 | 350 | 308 | 53.94% | 55.15% | 42.21% | 47.82% | 34.33% | 65.67% | 53.94% | 0.0811 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `code_diff_only` | `Return` | 591 | 250 | 670 | 329 | 68.53% | 70.27% | 64.24% | 67.12% | 27.17% | 72.83% | 68.53% | 0.3720 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `code_diff_only` | `Summary` | 244 | 154 | 379 | 289 | 58.44% | 61.31% | 45.78% | 52.42% | 28.89% | 71.11% | 58.44% | 0.1745 |
| `sgd_log_loss_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 603 | 287 | 633 | 317 | 67.17% | 67.75% | 65.54% | 66.63% | 31.20% | 68.80% | 67.17% | 0.3437 |
| `sgd_log_loss_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 261 | 210 | 323 | 272 | 54.78% | 55.41% | 48.97% | 51.99% | 39.40% | 60.60% | 54.78% | 0.0963 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 610 | 265 | 655 | 310 | 68.75% | 69.71% | 66.30% | 67.97% | 28.80% | 71.20% | 68.75% | 0.3754 |
| `logreg_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 244 | 186 | 347 | 289 | 55.44% | 56.74% | 45.78% | 50.67% | 34.90% | 65.10% | 55.44% | 0.1109 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | `Return` | 621 | 256 | 664 | 299 | 69.84% | 70.81% | 67.50% | 69.12% | 27.83% | 72.17% | 69.84% | 0.3972 |
| `linear_svc_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 237 | 199 | 334 | 296 | 53.56% | 54.36% | 44.47% | 48.92% | 37.34% | 62.66% | 53.56% | 0.0725 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Return` | 659 | 295 | 625 | 261 | 69.78% | 69.08% | 71.63% | 70.33% | 32.07% | 67.93% | 69.78% | 0.3959 |
| `complement_nb` | `word_char_tfidf_plus_manual_features` | `old_comment_plus_old_new_code` | `Summary` | 227 | 165 | 368 | 306 | 55.82% | 57.91% | 42.59% | 49.08% | 30.96% | 69.04% | 55.82% | 0.1206 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 615 | 310 | 610 | 305 | 66.58% | 66.49% | 66.85% | 66.67% | 33.70% | 66.30% | 66.58% | 0.3315 |
| `linear_svc_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 262 | 228 | 305 | 271 | 53.19% | 53.47% | 49.16% | 51.22% | 42.78% | 57.22% | 53.19% | 0.0640 |
| `complement_nb` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 649 | 287 | 633 | 271 | 69.67% | 69.34% | 70.54% | 69.94% | 31.20% | 68.80% | 69.67% | 0.3935 |
| `complement_nb` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 221 | 167 | 366 | 312 | 55.07% | 56.96% | 41.46% | 47.99% | 31.33% | 68.67% | 55.07% | 0.1053 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 664 | 325 | 595 | 256 | 68.42% | 67.14% | 72.17% | 69.57% | 35.33% | 64.67% | 68.42% | 0.3695 |
| `sgd_modified_huber_balanced` | `word_char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 272 | 210 | 323 | 261 | 55.82% | 56.43% | 51.03% | 53.60% | 39.40% | 60.60% | 55.82% | 0.1169 |
| `complement_nb` | `word_tfidf` | `code_diff_only` | `Return` | 572 | 253 | 667 | 348 | 67.34% | 69.33% | 62.17% | 65.56% | 27.50% | 72.50% | 67.34% | 0.3486 |
| `complement_nb` | `word_tfidf` | `code_diff_only` | `Summary` | 181 | 159 | 374 | 352 | 52.06% | 53.24% | 33.96% | 41.47% | 29.83% | 70.17% | 52.06% | 0.0443 |
| `complement_nb` | `char_tfidf` | `code_diff_only` | `Return` | 671 | 299 | 621 | 249 | 70.22% | 69.18% | 72.93% | 71.01% | 32.50% | 67.50% | 70.22% | 0.4049 |
| `complement_nb` | `char_tfidf` | `code_diff_only` | `Summary` | 241 | 173 | 360 | 292 | 56.38% | 58.21% | 45.22% | 50.90% | 32.46% | 67.54% | 56.38% | 0.1309 |
| `complement_nb` | `word_tfidf` | `old_comment_plus_old_new_code` | `Return` | 637 | 295 | 625 | 283 | 68.59% | 68.35% | 69.24% | 68.79% | 32.07% | 67.93% | 68.59% | 0.3718 |
| `complement_nb` | `word_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 219 | 165 | 368 | 314 | 55.07% | 57.03% | 41.09% | 47.76% | 30.96% | 69.04% | 55.07% | 0.1055 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | `Return` | 621 | 287 | 633 | 299 | 68.15% | 68.39% | 67.50% | 67.94% | 31.20% | 68.80% | 68.15% | 0.3631 |
| `sgd_modified_huber_balanced` | `word_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 249 | 205 | 328 | 284 | 54.13% | 54.85% | 46.72% | 50.46% | 38.46% | 61.54% | 54.13% | 0.0835 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 599 | 325 | 595 | 321 | 64.89% | 64.83% | 65.11% | 64.97% | 35.33% | 64.67% | 64.89% | 0.2978 |
| `sgd_modified_huber_balanced` | `char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 236 | 215 | 318 | 297 | 51.97% | 52.33% | 44.28% | 47.97% | 40.34% | 59.66% | 51.97% | 0.0399 |
| `complement_nb` | `char_tfidf` | `old_comment_plus_old_new_code` | `Return` | 629 | 312 | 608 | 291 | 67.23% | 66.84% | 68.37% | 67.60% | 33.91% | 66.09% | 67.23% | 0.3447 |
| `complement_nb` | `char_tfidf` | `old_comment_plus_old_new_code` | `Summary` | 220 | 187 | 346 | 313 | 53.10% | 54.05% | 41.28% | 46.81% | 35.08% | 64.92% | 53.10% | 0.0637 |

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

The v2 baseline is selected without test tuning. It should be reported as an external code-comment consistency proxy result and kept separate from the main DocGuard agent benchmark.
