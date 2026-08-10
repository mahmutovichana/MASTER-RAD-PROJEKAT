# External Binary Evaluation Design 2026-08

This design applies only after a real external dataset with explicit binary labels is prepared.

## Metrics

- Precision
- Recall
- F1
- Accuracy
- False-positive rate
- False-negative rate
- Calibration and confidence distribution
- Per-dataset reporting

## Evaluation Modes

- `code_comment_pair_only`: for static code/comment consistency datasets.
- `code_diff_only`: for datasets with code before/after or diffs.
- `code_diff_plus_comment_before`: for datasets with code change plus previous comment.
- `code_diff_plus_doc_before`: for CoDocBench-style records with code change and current documentation context.

## Dataset Separation

CoDocBench positive-only validation must remain separate from binary external evaluation. It supports positive sensitivity claims, not external precision/F1.

Synthetic negative sanity controls should be reported as controls only. They should not be combined with CoDocBench positives as final external F1.

## Required Inputs Before Reporting F1

1. Explicit positive and negative external labels.
2. Documented label provenance.
3. Mapping audit for code/comment fields.
4. Leakage audit confirming no future comment/doc diff is included in fair input modes.
5. Per-source metric table.
