# External Deep-JIT Zero-Shot vs Trained Classifier 2026-08

| System | Accuracy | Precision | Recall | F1 | FPR | Specificity | Balanced accuracy | MCC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Existing synthetic-trained DocGuard zero-shot | 50.40% | 50.20% | 100.00% | 66.84% | 99.20% | 0.80% | 50.40% | 0.0635 |
| Best external-trained lightweight classifier (`tfidf_logreg`, `old_comment_plus_code_diff`) | 68.72% | 73.41% | 58.71% | 65.24% | 21.27% | 78.73% | 68.72% | 0.3821 |

Zero-shot transfer exposes a domain/task shift. The trained classifier may have similar or slightly lower F1, but its specificity, balanced accuracy, and MCC show a much healthier binary classifier. External training should be kept separate from the project-level synthetic DocGuard benchmark and interpreted as a code-comment consistency proxy adaptation.
