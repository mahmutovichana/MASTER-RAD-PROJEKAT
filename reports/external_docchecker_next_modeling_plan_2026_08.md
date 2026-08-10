# External DocChecker Next Modeling Plan 2026-08

1. Confirm label polarity manually against the original Deep-JIT paper, preprocessing code, or dataset release notes.
2. If labels are confirmed, create explicit train/validation/test splits from Deep-JIT without mixing them into the synthetic DocGuard benchmark.
3. Train a lightweight external binary classifier using code + comment pair input with LogisticRegression or LinearSVC over TF-IDF and/or sentence-transformer embeddings.
4. Compare synthetic-trained DocGuard zero-shot transfer, an external-trained binary classifier, and a hybrid approach.
5. Keep task-specific results separate: DocGuard project-level synthetic benchmark, CoDocBench positive update benchmark, and Deep-JIT binary consistency proxy benchmark.

Do not retrain the production DocGuard path until label polarity and sample quality are manually checked.
