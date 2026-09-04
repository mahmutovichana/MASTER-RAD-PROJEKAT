# Gate 2 external-compute incident 002 — Kaggle timeout without persistence

## Classification

Technical execution failure only. No finalized Gate 2 result exists from this run, no scientific decision was changed, and confirmation was not accessed.

## Observed execution state

- UniXcoder development embeddings completed.
- Binary M1 completed 5/5 outer folds.
- Binary M2 completed 5/5 outer folds.
- Binary M3 completed outer fold 0.
- Binary M3 outer fold 1 remained inside long-running work without intermediate candidate/fit output.
- The free Kaggle session expired at its 12-hour boundary.
- Kaggle persistence was disabled, so runtime checkpoints were not recoverable.

## Root cause

The scientific workload was valid but the execution layer had insufficient visibility inside an outer fold. M3 performs 54 registered inner candidate fits per outer fold (3 inner folds × 3 semantic scales × 3 C values × 2 class-weight choices), followed by the selected outer fit. A single `LogisticRegression.fit()` could remain silent for a long period. The durable checkpoint boundary existed only after a complete outer fold, and the notebook was run without persisted files.

## Remediation boundary

The remediation is execution/observability-only:

- structured phase, candidate, fold, family, and whole-study progress;
- a 60-second live-fit heartbeat;
- timers for preprocessing, matrix assembly, solver fit, prediction, hashing, GC, and checkpoint I/O;
- validated resume-plan reporting;
- candidate-level scheduling with conservative thread limits;
- stronger semantic fold-to-embedding identity binding;
- portable checkpoint verification and documented Kaggle Files-only persistence.

No dataset row, label, safe field, fold, model family, representation, encoder revision, grid, seed, threshold, metric, or winner rule is changed. Mid-outer-fold checkpointing remains deliberately unsupported because a compact partial state that proves uninterrupted-equivalent inner selection was not sufficiently simple or robust. Completed outer folds remain the safe resume boundary.

Confirmation sealed: **YES**  
Confirmation accessed: **NO**
