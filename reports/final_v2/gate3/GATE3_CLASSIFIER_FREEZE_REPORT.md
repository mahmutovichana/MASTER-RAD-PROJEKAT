# Gate 3 Final Classifier Freeze

**Status: PASS.** Gate 3 used development data only. Confirmation remained sealed; Gate 4 and Gate 5 were not executed.

## Upstream evidence

- Gate 0, Gate 1 and Gate 2: PASS
- Gate 2 closure commit: `eb9448648f52b6d0156e8d905ba516c0e5b008e1`
- Frozen gold SHA-256: `68ebe23ab4dd8a02ee1ea459e3b6a374a3efa2891afc8d344a533676eb3b5a08`
- Gate 2 return SHA-256: `0b5840e1ce600f0df44f935f9c2ec9ce4608694e0dc0e73eb0f9a2e75b63abfd`

## Freeze-time selection procedure

Gate 2 selected M1 for both tasks. To obtain one final configuration without averaging fold-specific choices, Gate 3 generated repository-grouped OOF predictions over the immutable five Gate 2 folds for every candidate in the already-registered M1 grid. The registered metric and tie-break selected the final configuration. This is freeze-time tuning evidence, not a new evaluation estimate; Gate 2 nested CV remains the development evaluation.

- Binary: C=`0.25`, class_weight=`None`, threshold=`0.15`, rows=22166.
- Category: C=`4.0`, class_weight=`balanced`, rows=4820.
- Category classes: api_reference, configuration, developer_setup, model_contract.

## Artifacts

- Binary model: `models/final_v2/gate3/binary_m1_gate3.joblib` (`7d6a9263e1262c5c54db3d2e100209707c6a7681133fb1505f44125efa954462`)
- Category model: `models/final_v2/gate3/category_m1_gate3.joblib` (`2d8123ac398568b5c9586b0f8d26d6c4079ddfebd504889b934f77bef65b9f59`)
- Binary selection evidence: `reports/final_v2/gate3/binary_full_development_selection_evidence.json`
- Category selection evidence: `reports/final_v2/gate3/category_full_development_selection_evidence.json`

## Reproducibility and interpretation

Both pipelines passed a second deterministic rebuild: exact predictions and vocabulary, and probabilities/coefficients equal within `1e-12`. Joblib byte identity is not required because serialization metadata can vary.

Training provenance is non-circular: commit `eb9448648f52b6d0156e8d905ba516c0e5b008e1` is the upstream repository state at training time, while `GATE3_TRAINING_PROVENANCE.json` records SHA-256 identities of the then-uncommitted Gate 3 implementation sources that actually produced the frozen models. The formal closure commit merely versions those already-used source files and does not claim to predate model generation.

The Gate 2 generalization limitation remains unchanged: aggregate scores are materially influenced by controlled augmentation; natural-only and Natural Diversity slices are substantially weaker. This finding did not reopen model selection.

No training-set score is reported as final evaluation. Gate 2 development CV remains the only current evaluation evidence.

## Formal closure verification

- Standalone verifier: **PASS** (`python scripts/verify_gate3_classifier_freeze.py`).
- Complete safe non-confirmation suite: **428 passed**, 0 failed, 0 skipped, 30 warnings (`python -m pytest -q`).

## Boundary

Confirmation accessed: **NO**. Gate 4: **NOT_EXECUTED**. Gate 5: **NOT_EXECUTED**.
