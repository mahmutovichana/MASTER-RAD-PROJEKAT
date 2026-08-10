# External Deep-JIT Zero-Shot vs Trained Classifier 2026-08

| System | Accuracy | Precision | Recall | F1 | FPR |
| --- | ---: | ---: | ---: | ---: | ---: |
| Existing synthetic-trained DocGuard zero-shot | 50.40% | 50.20% | 100.00% | 66.84% | 99.20% |
| Best external-trained lightweight classifier (`tfidf_logreg`, `code_diff_only`) | 68.58% | 72.17% | 60.50% | 65.82% | 23.33% |

Zero-shot transfer exposes a domain/task shift. External training should be kept separate from the project-level synthetic DocGuard benchmark and interpreted as a code-comment consistency proxy adaptation.
