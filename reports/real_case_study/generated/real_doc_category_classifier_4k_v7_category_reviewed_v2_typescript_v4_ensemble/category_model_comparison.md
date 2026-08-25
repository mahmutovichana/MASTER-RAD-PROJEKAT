# Real PR Documentation Category Classifier V4 — ML-Only Ensemble

## Purpose

This experiment trains a second-stage documentation category classifier for positive documentation-update cases.

The binary classifier decides whether documentation should be updated. This classifier predicts the documentation category after a positive update decision.

## ML-only input policy

The classifier uses only safe pre-decision input fields:

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

No category-specific hand-written prediction rules are used.

Raw file paths are used only as raw lexical text. The model does not receive manually encoded features such as `path_flag_api_route`, `path_flag_configuration`, `path_flag_schema_contract`, or `path_flag_test_or_fixture`.

## V4 method

V4 uses a validation-selected soft-voting ensemble and validation-only probability calibration.

The calibration step learns class multipliers on the validation split only. It does not inspect locked-test results and it does not use keyword rules.

## Supported categories

- `api_reference`
- `configuration`
- `developer_setup`
- `model_contract`

## Dataset summary

```json
{
  "class_distribution": {
    "locked_test": {
      "api_reference": 134,
      "configuration": 108,
      "developer_setup": 63,
      "model_contract": 90
    },
    "train": {
      "api_reference": 625,
      "configuration": 507,
      "developer_setup": 290,
      "model_contract": 424
    },
    "validation": {
      "api_reference": 134,
      "configuration": 109,
      "developer_setup": 62,
      "model_contract": 91
    }
  },
  "language_filter": "typescript",
  "row_counts": {
    "locked_test": 395,
    "train": 1846,
    "validation": 396
  }
}
```

## Selected ensemble

```json
{
  "ensemble_size": 5,
  "selected_model_names": [
    "path_raw_word_char_logreg_balanced_c8.0",
    "path_raw_word_char_logreg_balanced_c4.0",
    "code_docs_path_raw_logreg_balanced_c8.0",
    "path_raw_word_char_logreg_balanced_c2.0",
    "word_char_logreg_balanced_c8.0"
  ],
  "validation_weights": {
    "code_docs_path_raw_logreg_balanced_c8.0": 0.67284747079011,
    "path_raw_word_char_logreg_balanced_c2.0": 0.6717137647755408,
    "path_raw_word_char_logreg_balanced_c4.0": 0.6782502247143315,
    "path_raw_word_char_logreg_balanced_c8.0": 0.68185990478724,
    "word_char_logreg_balanced_c8.0": 0.6625321691370822
  },
  "weights_source": "validation_macro_f1"
}
```

## Single-model comparison

| Model | Validation macro-F1 | Validation weighted-F1 | Validation accuracy | Locked macro-F1 | Locked weighted-F1 | Locked accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `word_logreg_c0.05` | 0.3724 | 0.4341 | 0.5025 | 0.3573 | 0.4166 | 0.4810 |
| `word_logreg_balanced_c0.05` | 0.5413 | 0.5713 | 0.5783 | 0.5076 | 0.5312 | 0.5316 |
| `word_char_logreg_balanced_c0.05` | 0.5624 | 0.5913 | 0.5960 | 0.5232 | 0.5465 | 0.5443 |
| `path_raw_word_char_logreg_balanced_c0.05` | 0.5706 | 0.6013 | 0.6035 | 0.5271 | 0.5573 | 0.5544 |
| `code_docs_path_raw_logreg_balanced_c0.05` | 0.5767 | 0.6061 | 0.6086 | 0.5400 | 0.5648 | 0.5620 |
| `word_logreg_c0.1` | 0.4526 | 0.4977 | 0.5379 | 0.4397 | 0.4889 | 0.5266 |
| `word_logreg_balanced_c0.1` | 0.5463 | 0.5775 | 0.5833 | 0.5093 | 0.5326 | 0.5316 |
| `word_char_logreg_balanced_c0.1` | 0.5687 | 0.5987 | 0.6010 | 0.5344 | 0.5569 | 0.5544 |
| `path_raw_word_char_logreg_balanced_c0.1` | 0.5743 | 0.6047 | 0.6061 | 0.5563 | 0.5831 | 0.5797 |
| `code_docs_path_raw_logreg_balanced_c0.1` | 0.5908 | 0.6171 | 0.6187 | 0.5582 | 0.5823 | 0.5797 |
| `word_logreg_c0.25` | 0.5164 | 0.5599 | 0.5859 | 0.4808 | 0.5194 | 0.5392 |
| `word_logreg_balanced_c0.25` | 0.5654 | 0.5979 | 0.6010 | 0.5162 | 0.5409 | 0.5392 |
| `word_char_logreg_balanced_c0.25` | 0.5929 | 0.6218 | 0.6212 | 0.5495 | 0.5708 | 0.5671 |
| `path_raw_word_char_logreg_balanced_c0.25` | 0.6084 | 0.6351 | 0.6338 | 0.5674 | 0.5958 | 0.5924 |
| `code_docs_path_raw_logreg_balanced_c0.25` | 0.6155 | 0.6409 | 0.6414 | 0.5861 | 0.6100 | 0.6076 |
| `word_logreg_c0.5` | 0.5432 | 0.5797 | 0.5960 | 0.4995 | 0.5359 | 0.5519 |
| `word_logreg_balanced_c0.5` | 0.5896 | 0.6156 | 0.6162 | 0.5327 | 0.5547 | 0.5519 |
| `word_char_logreg_balanced_c0.5` | 0.6066 | 0.6350 | 0.6338 | 0.5837 | 0.6054 | 0.6025 |
| `path_raw_word_char_logreg_balanced_c0.5` | 0.6356 | 0.6595 | 0.6591 | 0.5982 | 0.6254 | 0.6228 |
| `code_docs_path_raw_logreg_balanced_c0.5` | 0.6403 | 0.6638 | 0.6641 | 0.6087 | 0.6320 | 0.6304 |
| `word_logreg_c1.0` | 0.5671 | 0.6029 | 0.6162 | 0.5383 | 0.5718 | 0.5823 |
| `word_logreg_balanced_c1.0` | 0.6036 | 0.6322 | 0.6313 | 0.5579 | 0.5781 | 0.5747 |
| `word_char_logreg_balanced_c1.0` | 0.6225 | 0.6488 | 0.6490 | 0.6232 | 0.6426 | 0.6405 |
| `path_raw_word_char_logreg_balanced_c1.0` | 0.6555 | 0.6772 | 0.6768 | 0.6283 | 0.6523 | 0.6506 |
| `code_docs_path_raw_logreg_balanced_c1.0` | 0.6577 | 0.6809 | 0.6818 | 0.6284 | 0.6532 | 0.6532 |
| `word_logreg_c2.0` | 0.6073 | 0.6338 | 0.6414 | 0.5723 | 0.6012 | 0.6076 |
| `word_logreg_balanced_c2.0` | 0.6210 | 0.6493 | 0.6490 | 0.5921 | 0.6101 | 0.6076 |
| `word_char_logreg_balanced_c2.0` | 0.6452 | 0.6665 | 0.6667 | 0.6403 | 0.6571 | 0.6557 |
| `path_raw_word_char_logreg_balanced_c2.0` | 0.6717 | 0.6922 | 0.6919 | 0.6466 | 0.6670 | 0.6658 |
| `code_docs_path_raw_logreg_balanced_c2.0` | 0.6554 | 0.6786 | 0.6793 | 0.6495 | 0.6686 | 0.6684 |
| `word_logreg_c4.0` | 0.6239 | 0.6484 | 0.6540 | 0.5840 | 0.6136 | 0.6177 |
| `word_logreg_balanced_c4.0` | 0.6291 | 0.6540 | 0.6540 | 0.6135 | 0.6338 | 0.6329 |
| `word_char_logreg_balanced_c4.0` | 0.6527 | 0.6768 | 0.6768 | 0.6389 | 0.6537 | 0.6532 |
| `path_raw_word_char_logreg_balanced_c4.0` | 0.6783 | 0.6963 | 0.6970 | 0.6574 | 0.6738 | 0.6734 |
| `code_docs_path_raw_logreg_balanced_c4.0` | 0.6616 | 0.6850 | 0.6869 | 0.6663 | 0.6836 | 0.6835 |
| `word_logreg_c8.0` | 0.6350 | 0.6579 | 0.6616 | 0.6087 | 0.6316 | 0.6329 |
| `word_logreg_balanced_c8.0` | 0.6343 | 0.6598 | 0.6616 | 0.6334 | 0.6489 | 0.6481 |
| `word_char_logreg_balanced_c8.0` | 0.6625 | 0.6835 | 0.6843 | 0.6486 | 0.6611 | 0.6608 |
| `path_raw_word_char_logreg_balanced_c8.0` | 0.6819 | 0.7029 | 0.7045 | 0.6659 | 0.6815 | 0.6810 |
| `code_docs_path_raw_logreg_balanced_c8.0` | 0.6728 | 0.6955 | 0.6970 | 0.6645 | 0.6813 | 0.6810 |

## Ensemble metrics

```json
{
  "locked_test": {
    "accuracy": 0.6835443037974683,
    "classification_report": {
      "accuracy": 0.6835443037974683,
      "api_reference": {
        "f1-score": 0.7670250896057348,
        "precision": 0.7379310344827587,
        "recall": 0.7985074626865671,
        "support": 134.0
      },
      "configuration": {
        "f1-score": 0.6666666666666666,
        "precision": 0.7471264367816092,
        "recall": 0.6018518518518519,
        "support": 108.0
      },
      "developer_setup": {
        "f1-score": 0.5984251968503937,
        "precision": 0.59375,
        "recall": 0.6031746031746031,
        "support": 63.0
      },
      "macro avg": {
        "f1-score": 0.6667593970108575,
        "precision": 0.6712170193312434,
        "recall": 0.6675501460949221,
        "support": 395.0
      },
      "model_contract": {
        "f1-score": 0.6349206349206349,
        "precision": 0.6060606060606061,
        "recall": 0.6666666666666666,
        "support": 90.0
      },
      "weighted avg": {
        "f1-score": 0.682594953295191,
        "precision": 0.6874028312368557,
        "recall": 0.6835443037974683,
        "support": 395.0
      }
    },
    "confusion_matrix": [
      [
        107,
        10,
        8,
        9
      ],
      [
        16,
        65,
        9,
        18
      ],
      [
        5,
        8,
        38,
        12
      ],
      [
        17,
        4,
        9,
        60
      ]
    ],
    "gold_distribution": {
      "api_reference": 134,
      "configuration": 108,
      "developer_setup": 63,
      "model_contract": 90
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.6667593970108575,
    "pred_distribution": {
      "api_reference": 145,
      "configuration": 87,
      "developer_setup": 64,
      "model_contract": 99
    },
    "weighted_f1": 0.682594953295191
  },
  "train": {
    "accuracy": 0.9962080173347779,
    "classification_report": {
      "accuracy": 0.9962080173347779,
      "api_reference": {
        "f1-score": 0.9984,
        "precision": 0.9984,
        "recall": 0.9984,
        "support": 625.0
      },
      "configuration": {
        "f1-score": 0.9940476190476191,
        "precision": 1.0,
        "recall": 0.9881656804733728,
        "support": 507.0
      },
      "developer_setup": {
        "f1-score": 0.9931506849315068,
        "precision": 0.9863945578231292,
        "recall": 1.0,
        "support": 290.0
      },
      "macro avg": {
        "f1-score": 0.9958113407006638,
        "precision": 0.9950249305355945,
        "recall": 0.9966414201183432,
        "support": 1846.0
      },
      "model_contract": {
        "f1-score": 0.9976470588235294,
        "precision": 0.9953051643192489,
        "recall": 1.0,
        "support": 424.0
      },
      "weighted avg": {
        "f1-score": 0.9962070392353501,
        "precision": 0.9962425847454328,
        "recall": 0.9962080173347779,
        "support": 1846.0
      }
    },
    "confusion_matrix": [
      [
        624,
        0,
        1,
        0
      ],
      [
        1,
        501,
        3,
        2
      ],
      [
        0,
        0,
        290,
        0
      ],
      [
        0,
        0,
        0,
        424
      ]
    ],
    "gold_distribution": {
      "api_reference": 625,
      "configuration": 507,
      "developer_setup": 290,
      "model_contract": 424
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.9958113407006638,
    "pred_distribution": {
      "api_reference": 625,
      "configuration": 501,
      "developer_setup": 294,
      "model_contract": 426
    },
    "weighted_f1": 0.9962070392353501
  },
  "validation": {
    "accuracy": 0.7070707070707071,
    "classification_report": {
      "accuracy": 0.7070707070707071,
      "api_reference": {
        "f1-score": 0.8014184397163121,
        "precision": 0.7635135135135135,
        "recall": 0.8432835820895522,
        "support": 134.0
      },
      "configuration": {
        "f1-score": 0.6926829268292682,
        "precision": 0.7395833333333334,
        "recall": 0.6513761467889908,
        "support": 109.0
      },
      "developer_setup": {
        "f1-score": 0.6101694915254238,
        "precision": 0.6428571428571429,
        "recall": 0.5806451612903226,
        "support": 62.0
      },
      "macro avg": {
        "f1-score": 0.686495522004382,
        "precision": 0.6927384974259975,
        "recall": 0.6836613873773812,
        "support": 396.0
      },
      "model_contract": {
        "f1-score": 0.6417112299465241,
        "precision": 0.625,
        "recall": 0.6593406593406593,
        "support": 91.0
      },
      "weighted avg": {
        "f1-score": 0.7048453039042577,
        "precision": 0.7062059015184015,
        "recall": 0.7070707070707071,
        "support": 396.0
      }
    },
    "confusion_matrix": [
      [
        113,
        7,
        4,
        10
      ],
      [
        15,
        71,
        9,
        14
      ],
      [
        5,
        9,
        36,
        12
      ],
      [
        15,
        9,
        7,
        60
      ]
    ],
    "gold_distribution": {
      "api_reference": 134,
      "configuration": 109,
      "developer_setup": 62,
      "model_contract": 91
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.686495522004382,
    "pred_distribution": {
      "api_reference": 148,
      "configuration": 96,
      "developer_setup": 56,
      "model_contract": 96
    },
    "weighted_f1": 0.7048453039042577
  }
}
```

## Probability calibration

```json
{
  "grid_values": [
    0.5,
    0.75,
    1.0,
    1.25,
    1.5,
    2.0
  ],
  "locked_test_policy": "final_reporting_only",
  "method": "validation_only_class_probability_multipliers",
  "selected_multipliers": {
    "api_reference": 1.5,
    "configuration": 1.0,
    "developer_setup": 1.25,
    "model_contract": 1.25
  },
  "validation_metrics_after_calibration": {
    "accuracy": 0.7070707070707071,
    "classification_report": {
      "accuracy": 0.7070707070707071,
      "api_reference": {
        "f1-score": 0.8014184397163121,
        "precision": 0.7635135135135135,
        "recall": 0.8432835820895522,
        "support": 134.0
      },
      "configuration": {
        "f1-score": 0.6926829268292682,
        "precision": 0.7395833333333334,
        "recall": 0.6513761467889908,
        "support": 109.0
      },
      "developer_setup": {
        "f1-score": 0.6101694915254238,
        "precision": 0.6428571428571429,
        "recall": 0.5806451612903226,
        "support": 62.0
      },
      "macro avg": {
        "f1-score": 0.686495522004382,
        "precision": 0.6927384974259975,
        "recall": 0.6836613873773812,
        "support": 396.0
      },
      "model_contract": {
        "f1-score": 0.6417112299465241,
        "precision": 0.625,
        "recall": 0.6593406593406593,
        "support": 91.0
      },
      "weighted avg": {
        "f1-score": 0.7048453039042577,
        "precision": 0.7062059015184015,
        "recall": 0.7070707070707071,
        "support": 396.0
      }
    },
    "confusion_matrix": [
      [
        113,
        7,
        4,
        10
      ],
      [
        15,
        71,
        9,
        14
      ],
      [
        5,
        9,
        36,
        12
      ],
      [
        15,
        9,
        7,
        60
      ]
    ],
    "gold_distribution": {
      "api_reference": 134,
      "configuration": 109,
      "developer_setup": 62,
      "model_contract": 91
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.686495522004382,
    "pred_distribution": {
      "api_reference": 148,
      "configuration": 96,
      "developer_setup": 56,
      "model_contract": 96
    },
    "weighted_f1": 0.7048453039042577
  }
}
```

## Outputs

```json
{
  "category_model": "models\\real_doc_category_classifier_4k_v7_category_reviewed_v2_typescript_v4_ensemble\\best_category_model.joblib",
  "model_comparison_json": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v7_category_reviewed_v2_typescript_v4_ensemble\\category_model_comparison.json",
  "model_comparison_md": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v7_category_reviewed_v2_typescript_v4_ensemble\\category_model_comparison.md",
  "predictions_jsonl": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v7_category_reviewed_v2_typescript_v4_ensemble\\category_predictions.jsonl",
  "summary_json": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v7_category_reviewed_v2_typescript_v4_ensemble\\category_classifier_summary.json"
}
```

## Methodological note

This is a second-stage category classifier. It is trained and evaluated only on cases where documentation update is required and where the category can be harmonized into one of the supported thesis categories.

Model selection, ensemble selection, and probability calibration use the validation split only. The locked-test split is used only for final reporting.
