# External Deep-JIT Label Polarity Evidence 2026-08

## Status

- Current status: `plausible_manual_verification_needed`
- Current mapping: raw `label=1` -> inconsistent/update-required; raw `label=0` -> consistent/no-update.

## Evidence Found

Deep-JIT repository task framing says the project is for just-in-time inconsistency detection between comments and source code. The README describes an `Inconsistency Detection` task and the paper abstract frames the goal as detecting whether a comment becomes inconsistent after a code change.

Source: https://github.com/panthap2/deep-jit-inconsistency-detection

The Deep-JIT `run_comment_model.py` code treats `label == 1` as the retained class for `--positive_only` training:

```python
train_examples = [ex for ex in train_examples if ex.label == 1]
valid_examples = [ex for ex in valid_examples if ex.label == 1]
```

Source: https://raw.githubusercontent.com/panthap2/deep-jit-inconsistency-detection/master/run_comment_model.py

The Deep-JIT `detection_evaluation_utils.py` code treats truthy gold labels as the positive class when computing true positives and false negatives.

Source: https://raw.githubusercontent.com/panthap2/deep-jit-inconsistency-detection/master/detection_evaluation_utils.py

Manual sampled examples in `reports/external_docchecker_label_polarity_audit_2026_08.md` support this mapping: raw `label=1` examples generally show changed comments that track code changes, while raw `label=0` examples generally preserve comments across code changes.

## Interpretation

The evidence strongly supports that `label=1` is the positive class and that the positive class corresponds to the inconsistency/update-needed side of the Deep-JIT task. However, because the downloaded data files and README do not include an explicit label legend saying `1 = inconsistent` and `0 = consistent`, final thesis wording should keep the status as plausible/manual verification needed unless another primary source is found.

## Thesis-Safe Wording

The Deep-JIT numeric label polarity was mapped as `1 = inconsistent/update-required` and `0 = consistent/no-update`. This mapping is supported by the task framing, repository code that treats `label == 1` as the positive class, and manual inspection of sampled examples, but the repository README does not provide an explicit numeric label legend.
