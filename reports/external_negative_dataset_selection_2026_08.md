# External Negative Dataset Selection 2026-08

## Goal

DocGuard needs a defensible external negative or binary evaluation set before reporting external precision, F1, false-positive rate, or negative classification quality.

## Candidate Paths

### 1. External code-comment inconsistency datasets

These may provide consistent/inconsistent code-comment pairs. They are not identical to update-required labels, but they can support a binary consistency evaluation and may be the safest source of explicit negative or inconsistent examples.

### 2. Panthaplackel comment-update dataset

This dataset family is useful for positive comment-update pairs. The next step is to inspect whether it includes non-update examples, explicit negatives, or only update pairs. If it only contains update pairs, it should be treated like CoDocBench: valuable for positive recall, insufficient for precision/F1.

### 3. Conservative real commit mining

Real commit mining is possible but risky. Weak negatives should only come from conservative categories such as formatting-only, test-only, internal refactor, or comments-only changes, and they require manual audit. Labels should use names such as `weak_negative_manual_audit` or `weak_negative_conservative_rule`, never strong negative labels.

### 4. Existing synthetic negatives

Existing synthetic negatives are useful for controls and development. They are not sufficient for final external precision/F1 because they share generator assumptions with the training/evaluation setup.

## Recommended Concrete Path

1. Run synthetic negative sanity controls to check for constant-positive behavior.
2. Inspect one external dataset with explicit negative or inconsistency labels.
3. Define a small external binary evaluation schema.
4. Manually audit label provenance.
5. Only then report external precision/F1.
