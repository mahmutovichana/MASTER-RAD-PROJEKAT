# Blind Label Audit Evaluation

## Input files

- Review CSV: `reports\real_case_study\blind_label_audit_4k_v2\blind_review_sample_labeled_corrected.csv`
- Key JSONL: `reports\real_case_study\blind_label_audit_4k_v2\blind_review_key.jsonl`

## Validation

- Status: `ok`
- Review rows: `233`

## Review label distribution

```json
{
  "binary": {
    "True": 102,
    "unknown": 131
  },
  "category": {
    "api_reference": 19,
    "configuration": 16,
    "developer_setup": 9,
    "model_contract": 58,
    "no_update": 131
  },
  "confidence": {
    "high": 86,
    "low": 34,
    "medium": 113
  }
}
```

## Protocol label distribution

```json
{
  "binary": {
    "True": 120,
    "unknown": 113
  },
  "category": {
    "api_reference": 42,
    "configuration": 27,
    "developer_setup": 9,
    "model_contract": 23,
    "no_update": 113,
    "project_documentation": 9,
    "security": 2,
    "testing": 6,
    "workflow_documentation": 2
  },
  "confidence": {
    "protocol_high": 152,
    "protocol_medium": 81
  },
  "source": {
    "protocol_derived_large_scale_label_v1": 233
  }
}
```

## Review vs protocol labels

- Binary agreement: `0.6824`
- Cohen's kappa: `0.3672`

```json
{
  "accuracy": 0.6824034334763949,
  "balanced_accuracy": 0.6871725789552462,
  "f1": 0.6666666666666666,
  "false_negatives": 28,
  "false_positive_rate": 0.3511450381679389,
  "false_positives": 46,
  "gold_distribution": {
    "False": 131,
    "True": 102
  },
  "mcc": 0.3716020566222173,
  "precision": 0.6166666666666667,
  "pred_distribution": {
    "False": 113,
    "True": 120
  },
  "recall": 0.7254901960784313,
  "specificity": 0.648854961832061,
  "total_cases": 233,
  "true_negatives": 85,
  "true_positives": 74
}
```

## V2 model vs human-corrected review labels

```json
{
  "accuracy": 0.6609442060085837,
  "balanced_accuracy": 0.6615776081424936,
  "f1": 0.6325581395348837,
  "false_negatives": 34,
  "false_positive_rate": 0.3435114503816794,
  "false_positives": 45,
  "gold_distribution": {
    "False": 131,
    "True": 102
  },
  "mcc": 0.32078722121046266,
  "precision": 0.6017699115044248,
  "pred_distribution": {
    "False": 120,
    "True": 113
  },
  "recall": 0.6666666666666666,
  "specificity": 0.6564885496183206,
  "total_cases": 233,
  "true_negatives": 86,
  "true_positives": 68
}
```

## V2 model vs protocol labels on the same audit sample

```json
{
  "accuracy": 0.5150214592274678,
  "balanced_accuracy": 0.5154867256637168,
  "f1": 0.5150214592274679,
  "false_negatives": 60,
  "false_positive_rate": 0.4690265486725664,
  "false_positives": 53,
  "gold_distribution": {
    "False": 113,
    "True": 120
  },
  "mcc": 0.030973451327433628,
  "precision": 0.5309734513274337,
  "pred_distribution": {
    "False": 120,
    "True": 113
  },
  "recall": 0.5,
  "specificity": 0.5309734513274337,
  "total_cases": 233,
  "true_negatives": 60,
  "true_positives": 60
}
```

## Disagreements by language

```json
{
  "go": {
    "agree": 4
  },
  "python": {
    "agree": 16,
    "protocol_false_review_true": 2,
    "protocol_true_review_false": 5
  },
  "typescript": {
    "agree": 139,
    "protocol_false_review_true": 26,
    "protocol_true_review_false": 41
  }
}
```

## Disagreements by candidate type

```json
{
  "code_and_docs_changed_needs_manual_validation": {
    "agree": 35,
    "protocol_true_review_false": 8
  },
  "code_only_needs_manual_validation": {
    "agree": 87,
    "protocol_false_review_true": 28,
    "protocol_true_review_false": 38
  },
  "code_only_test_or_fixture_candidate_negative_review": {
    "agree": 37
  }
}
```

## Methodological note

This audit evaluates agreement between protocol-derived labels and the human-corrected review labels on a stratified subset. The model performance against review labels should be interpreted as an audit-subset estimate, not as a replacement for the frozen locked-test result.
