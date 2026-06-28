# HF Input Ablation v0.4

| Input mode | Split | Precision | Recall | F1 | FP | FN | Pos. doc category | Pos. target file | Pos. scenario | Negative acc. | Macro scenario F1 | Macro doc category F1 | Avg latency | Model | Classifier |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `raw_diff_only` | `validation` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 0.9840 | 1.0000 | 1.0000 | 0.8512 | 1.0000 | 0.0127 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
| `raw_diff_only` | `test` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 0.9900 | 1.0000 | 1.0000 | 0.8543 | 1.0000 | 0.0139 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
| `raw_diff_plus_docs` | `validation` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8549 | 1.0000 | 0.0140 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
| `raw_diff_plus_docs` | `test` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8582 | 1.0000 | 0.0157 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
| `raw_diff_plus_signals` | `validation` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0184 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
| `raw_diff_plus_signals` | `test` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0190 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
| `raw_diff_plus_summary` | `validation` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0212 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
| `raw_diff_plus_summary` | `test` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0233 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
| `full_current` | `validation` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0291 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
| `full_current` | `test` | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0206 | sentence-transformers/all-MiniLM-L6-v2 | LogisticRegression |
