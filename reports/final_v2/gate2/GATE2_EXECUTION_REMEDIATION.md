# Gate 2 execution remediation

This is a protocol-preserving implementation repair, not a new experiment or preregistration amendment. The governing preregistration remains commit `e89cedfa87edbc1469d467713451a9441aa1360f`.

## Unchanged scientific state

No data, labels, taxonomy, safe fields, repository boundary, outer/inner fold, seed, model family, encoder or tokenizer revision, token length, truncation, pooling, semantic input, relation representation, lexical configuration, hyperparameter grid, class weighting option, semantic scale, threshold, metric, winner rule, or tie tolerance changed. Confirmation remains sealed.

## Execution-only changes

1. The partition manifest is verified by canonical JSON identity and by the exact Gate 1 commit/blob provenance, while retaining the original recorded CRLF byte SHA. LF and CRLF equivalents pass; semantic changes fail.
2. A single fail-closed wrapper executes verification, environment checks, development loading, embedding extraction, M1/M2/M3, artifact verification, and packaging in order. Any non-zero stage stops every later stage and records FAILED.
3. UniXcoder output is checkpointed to persistent float32 memmaps after every batch. Identity metadata binds gold, development view, row order, encoder/tokenizer, pooling, max length, dtype, shapes, and completed row count.
4. Every completed outer fold is immediately saved with hashed predictions/probabilities, validation IDs, selected inner configuration/threshold, metrics, scientific config hash, development identity, and fold-assignment hash. Resume restores OOF state and runs only missing folds.
5. Google Drive is persistent compute storage only. It is not a scientific data source, and embeddings/model weights are excluded from the returned archive.

The failed Colab run remains recorded and contributes no admissible performance result.
