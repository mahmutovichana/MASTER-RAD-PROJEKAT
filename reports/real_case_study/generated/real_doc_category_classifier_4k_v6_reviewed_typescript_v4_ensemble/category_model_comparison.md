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
      "api_reference": 161,
      "configuration": 97,
      "developer_setup": 35,
      "model_contract": 93
    },
    "train": {
      "api_reference": 730,
      "configuration": 523,
      "developer_setup": 342,
      "model_contract": 532
    },
    "validation": {
      "api_reference": 163,
      "configuration": 201,
      "developer_setup": 73,
      "model_contract": 73
    }
  },
  "language_filter": "typescript",
  "row_counts": {
    "locked_test": 386,
    "train": 2127,
    "validation": 510
  }
}
```

## Selected ensemble

```json
{
  "ensemble_size": 5,
  "selected_model_names": [
    "path_raw_word_char_logreg_balanced_c4.0",
    "path_raw_word_char_logreg_balanced_c1.0",
    "path_raw_word_char_logreg_balanced_c2.0",
    "code_docs_path_raw_logreg_balanced_c4.0",
    "path_raw_word_char_logreg_balanced_c8.0"
  ],
  "validation_weights": {
    "code_docs_path_raw_logreg_balanced_c4.0": 0.5265778000615358,
    "path_raw_word_char_logreg_balanced_c1.0": 0.5297333586687113,
    "path_raw_word_char_logreg_balanced_c2.0": 0.5289624602485552,
    "path_raw_word_char_logreg_balanced_c4.0": 0.5359740774753715,
    "path_raw_word_char_logreg_balanced_c8.0": 0.5223700791891259
  },
  "weights_source": "validation_macro_f1"
}
```

## Single-model comparison

| Model | Validation macro-F1 | Validation weighted-F1 | Validation accuracy | Locked macro-F1 | Locked weighted-F1 | Locked accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `word_logreg_c0.05` | 0.1211 | 0.1548 | 0.3196 | 0.1472 | 0.2455 | 0.4171 |
| `word_logreg_balanced_c0.05` | 0.2664 | 0.2563 | 0.3765 | 0.3047 | 0.3775 | 0.4793 |
| `word_char_logreg_balanced_c0.05` | 0.3425 | 0.3566 | 0.4275 | 0.3332 | 0.4119 | 0.4819 |
| `path_raw_word_char_logreg_balanced_c0.05` | 0.4471 | 0.5191 | 0.5431 | 0.3924 | 0.4413 | 0.4948 |
| `code_docs_path_raw_logreg_balanced_c0.05` | 0.3831 | 0.4188 | 0.4608 | 0.3497 | 0.4088 | 0.4767 |
| `word_logreg_c0.1` | 0.1211 | 0.1548 | 0.3196 | 0.1472 | 0.2455 | 0.4171 |
| `word_logreg_balanced_c0.1` | 0.2903 | 0.2910 | 0.3922 | 0.3289 | 0.3955 | 0.4896 |
| `word_char_logreg_balanced_c0.1` | 0.3664 | 0.3942 | 0.4510 | 0.3425 | 0.4206 | 0.4819 |
| `path_raw_word_char_logreg_balanced_c0.1` | 0.4795 | 0.5535 | 0.5784 | 0.3962 | 0.4471 | 0.5000 |
| `code_docs_path_raw_logreg_balanced_c0.1` | 0.4488 | 0.4949 | 0.5216 | 0.3693 | 0.4184 | 0.4819 |
| `word_logreg_c0.25` | 0.1349 | 0.1637 | 0.3235 | 0.1744 | 0.2733 | 0.4301 |
| `word_logreg_balanced_c0.25` | 0.3367 | 0.3593 | 0.4314 | 0.3279 | 0.3946 | 0.4845 |
| `word_char_logreg_balanced_c0.25` | 0.4134 | 0.4599 | 0.4961 | 0.3995 | 0.4459 | 0.4948 |
| `path_raw_word_char_logreg_balanced_c0.25` | 0.5139 | 0.5956 | 0.6235 | 0.3838 | 0.4400 | 0.4922 |
| `code_docs_path_raw_logreg_balanced_c0.25` | 0.4735 | 0.5259 | 0.5490 | 0.3909 | 0.4371 | 0.4922 |
| `word_logreg_c0.5` | 0.1807 | 0.2181 | 0.3510 | 0.2158 | 0.3168 | 0.4508 |
| `word_logreg_balanced_c0.5` | 0.3744 | 0.4051 | 0.4608 | 0.3673 | 0.4139 | 0.4948 |
| `word_char_logreg_balanced_c0.5` | 0.4497 | 0.5079 | 0.5392 | 0.4089 | 0.4480 | 0.4974 |
| `path_raw_word_char_logreg_balanced_c0.5` | 0.5125 | 0.5936 | 0.6216 | 0.4017 | 0.4537 | 0.5026 |
| `code_docs_path_raw_logreg_balanced_c0.5` | 0.4914 | 0.5512 | 0.5706 | 0.3917 | 0.4410 | 0.4948 |
| `word_logreg_c1.0` | 0.2087 | 0.2603 | 0.3725 | 0.2587 | 0.3521 | 0.4637 |
| `word_logreg_balanced_c1.0` | 0.3705 | 0.4148 | 0.4667 | 0.3838 | 0.4247 | 0.5000 |
| `word_char_logreg_balanced_c1.0` | 0.4482 | 0.5164 | 0.5510 | 0.4366 | 0.4720 | 0.5155 |
| `path_raw_word_char_logreg_balanced_c1.0` | 0.5297 | 0.6056 | 0.6294 | 0.4114 | 0.4578 | 0.5052 |
| `code_docs_path_raw_logreg_balanced_c1.0` | 0.5073 | 0.5616 | 0.5784 | 0.3998 | 0.4514 | 0.5026 |
| `word_logreg_c2.0` | 0.2756 | 0.3293 | 0.4137 | 0.2623 | 0.3556 | 0.4637 |
| `word_logreg_balanced_c2.0` | 0.3776 | 0.4374 | 0.4824 | 0.3743 | 0.4147 | 0.4922 |
| `word_char_logreg_balanced_c2.0` | 0.4838 | 0.5436 | 0.5706 | 0.4336 | 0.4697 | 0.5181 |
| `path_raw_word_char_logreg_balanced_c2.0` | 0.5290 | 0.6000 | 0.6196 | 0.4037 | 0.4483 | 0.4974 |
| `code_docs_path_raw_logreg_balanced_c2.0` | 0.5179 | 0.5747 | 0.5902 | 0.3980 | 0.4507 | 0.5026 |
| `word_logreg_c4.0` | 0.3204 | 0.3786 | 0.4431 | 0.2716 | 0.3645 | 0.4637 |
| `word_logreg_balanced_c4.0` | 0.3946 | 0.4563 | 0.4961 | 0.3844 | 0.4221 | 0.4974 |
| `word_char_logreg_balanced_c4.0` | 0.5023 | 0.5537 | 0.5745 | 0.4418 | 0.4784 | 0.5233 |
| `path_raw_word_char_logreg_balanced_c4.0` | 0.5360 | 0.6026 | 0.6216 | 0.3956 | 0.4410 | 0.4922 |
| `code_docs_path_raw_logreg_balanced_c4.0` | 0.5266 | 0.5791 | 0.5941 | 0.3913 | 0.4430 | 0.4974 |
| `word_logreg_c8.0` | 0.3426 | 0.3971 | 0.4529 | 0.2699 | 0.3638 | 0.4611 |
| `word_logreg_balanced_c8.0` | 0.3905 | 0.4592 | 0.4980 | 0.3859 | 0.4281 | 0.5000 |
| `word_char_logreg_balanced_c8.0` | 0.5028 | 0.5570 | 0.5784 | 0.4342 | 0.4754 | 0.5207 |
| `path_raw_word_char_logreg_balanced_c8.0` | 0.5224 | 0.5903 | 0.6098 | 0.3844 | 0.4343 | 0.4870 |
| `code_docs_path_raw_logreg_balanced_c8.0` | 0.5193 | 0.5721 | 0.5882 | 0.4019 | 0.4512 | 0.5052 |

## Ensemble metrics

```json
{
  "locked_test": {
    "accuracy": 0.5284974093264249,
    "classification_report": {
      "accuracy": 0.5284974093264249,
      "api_reference": {
        "f1-score": 0.6720430107526881,
        "precision": 0.5924170616113744,
        "recall": 0.7763975155279503,
        "support": 161.0
      },
      "configuration": {
        "f1-score": 0.28378378378378377,
        "precision": 0.4117647058823529,
        "recall": 0.21649484536082475,
        "support": 97.0
      },
      "developer_setup": {
        "f1-score": 0.5227272727272727,
        "precision": 0.4339622641509434,
        "recall": 0.6571428571428571,
        "support": 35.0
      },
      "macro avg": {
        "f1-score": 0.4763458338891069,
        "precision": 0.482775444530886,
        "recall": 0.5065948260132844,
        "support": 386.0
      },
      "model_contract": {
        "f1-score": 0.4268292682926829,
        "precision": 0.49295774647887325,
        "recall": 0.3763440860215054,
        "support": 93.0
      },
      "weighted avg": {
        "f1-score": 0.5018562908157613,
        "precision": 0.5086893084399942,
        "recall": 0.5284974093264249,
        "support": 386.0
      }
    },
    "confusion_matrix": [
      [
        125,
        17,
        10,
        9
      ],
      [
        44,
        21,
        15,
        17
      ],
      [
        1,
        1,
        23,
        10
      ],
      [
        41,
        12,
        5,
        35
      ]
    ],
    "gold_distribution": {
      "api_reference": 161,
      "configuration": 97,
      "developer_setup": 35,
      "model_contract": 93
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.4763458338891069,
    "pred_distribution": {
      "api_reference": 211,
      "configuration": 51,
      "developer_setup": 53,
      "model_contract": 71
    },
    "weighted_f1": 0.5018562908157613
  },
  "train": {
    "accuracy": 0.9689703808180536,
    "classification_report": {
      "accuracy": 0.9689703808180536,
      "api_reference": {
        "f1-score": 0.9739985945186226,
        "precision": 1.0,
        "recall": 0.9493150684931507,
        "support": 730.0
      },
      "configuration": {
        "f1-score": 0.9708171206225681,
        "precision": 0.9881188118811881,
        "recall": 0.9541108986615678,
        "support": 523.0
      },
      "developer_setup": {
        "f1-score": 0.9382716049382716,
        "precision": 0.8837209302325582,
        "recall": 1.0,
        "support": 342.0
      },
      "macro avg": {
        "f1-score": 0.9661163365375565,
        "precision": 0.9610411163402446,
        "recall": 0.9735068677285292,
        "support": 2127.0
      },
      "model_contract": {
        "f1-score": 0.9813780260707635,
        "precision": 0.9723247232472325,
        "recall": 0.9906015037593985,
        "support": 532.0
      },
      "weighted avg": {
        "f1-score": 0.9693175020417174,
        "precision": 0.9714600138791367,
        "recall": 0.9689703808180536,
        "support": 2127.0
      }
    },
    "confusion_matrix": [
      [
        693,
        6,
        22,
        9
      ],
      [
        0,
        499,
        18,
        6
      ],
      [
        0,
        0,
        342,
        0
      ],
      [
        0,
        0,
        5,
        527
      ]
    ],
    "gold_distribution": {
      "api_reference": 730,
      "configuration": 523,
      "developer_setup": 342,
      "model_contract": 532
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.9661163365375565,
    "pred_distribution": {
      "api_reference": 693,
      "configuration": 505,
      "developer_setup": 387,
      "model_contract": 542
    },
    "weighted_f1": 0.9693175020417174
  },
  "validation": {
    "accuracy": 0.6764705882352942,
    "classification_report": {
      "accuracy": 0.6764705882352942,
      "api_reference": {
        "f1-score": 0.721763085399449,
        "precision": 0.655,
        "recall": 0.803680981595092,
        "support": 163.0
      },
      "configuration": {
        "f1-score": 0.7320954907161804,
        "precision": 0.7840909090909091,
        "recall": 0.6865671641791045,
        "support": 201.0
      },
      "developer_setup": {
        "f1-score": 0.5303030303030303,
        "precision": 0.5932203389830508,
        "recall": 0.4794520547945205,
        "support": 73.0
      },
      "macro avg": {
        "f1-score": 0.6345539151181784,
        "precision": 0.6447444786851566,
        "recall": 0.6328360090462888,
        "support": 510.0
      },
      "model_contract": {
        "f1-score": 0.5540540540540541,
        "precision": 0.5466666666666666,
        "recall": 0.5616438356164384,
        "support": 73.0
      },
      "weighted avg": {
        "f1-score": 0.6744247915924109,
        "precision": 0.6815274983131414,
        "recall": 0.6764705882352942,
        "support": 510.0
      }
    },
    "confusion_matrix": [
      [
        131,
        15,
        5,
        12
      ],
      [
        42,
        138,
        12,
        9
      ],
      [
        14,
        11,
        35,
        13
      ],
      [
        13,
        12,
        7,
        41
      ]
    ],
    "gold_distribution": {
      "api_reference": 163,
      "configuration": 201,
      "developer_setup": 73,
      "model_contract": 73
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.6345539151181784,
    "pred_distribution": {
      "api_reference": 200,
      "configuration": 176,
      "developer_setup": 59,
      "model_contract": 75
    },
    "weighted_f1": 0.6744247915924109
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
    "api_reference": 0.75,
    "configuration": 1.0,
    "developer_setup": 2.0,
    "model_contract": 1.5
  },
  "validation_metrics_after_calibration": {
    "accuracy": 0.6764705882352942,
    "classification_report": {
      "accuracy": 0.6764705882352942,
      "api_reference": {
        "f1-score": 0.721763085399449,
        "precision": 0.655,
        "recall": 0.803680981595092,
        "support": 163.0
      },
      "configuration": {
        "f1-score": 0.7320954907161804,
        "precision": 0.7840909090909091,
        "recall": 0.6865671641791045,
        "support": 201.0
      },
      "developer_setup": {
        "f1-score": 0.5303030303030303,
        "precision": 0.5932203389830508,
        "recall": 0.4794520547945205,
        "support": 73.0
      },
      "macro avg": {
        "f1-score": 0.6345539151181784,
        "precision": 0.6447444786851566,
        "recall": 0.6328360090462888,
        "support": 510.0
      },
      "model_contract": {
        "f1-score": 0.5540540540540541,
        "precision": 0.5466666666666666,
        "recall": 0.5616438356164384,
        "support": 73.0
      },
      "weighted avg": {
        "f1-score": 0.6744247915924109,
        "precision": 0.6815274983131414,
        "recall": 0.6764705882352942,
        "support": 510.0
      }
    },
    "confusion_matrix": [
      [
        131,
        15,
        5,
        12
      ],
      [
        42,
        138,
        12,
        9
      ],
      [
        14,
        11,
        35,
        13
      ],
      [
        13,
        12,
        7,
        41
      ]
    ],
    "gold_distribution": {
      "api_reference": 163,
      "configuration": 201,
      "developer_setup": 73,
      "model_contract": 73
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.6345539151181784,
    "pred_distribution": {
      "api_reference": 200,
      "configuration": 176,
      "developer_setup": 59,
      "model_contract": 75
    },
    "weighted_f1": 0.6744247915924109
  }
}
```

## Outputs

```json
{
  "category_model": "models\\real_doc_category_classifier_4k_v6_reviewed_typescript_v4_ensemble\\best_category_model.joblib",
  "model_comparison_json": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v6_reviewed_typescript_v4_ensemble\\category_model_comparison.json",
  "model_comparison_md": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v6_reviewed_typescript_v4_ensemble\\category_model_comparison.md",
  "predictions_jsonl": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v6_reviewed_typescript_v4_ensemble\\category_predictions.jsonl",
  "summary_json": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v6_reviewed_typescript_v4_ensemble\\category_classifier_summary.json"
}
```

## Methodological note

This is a second-stage category classifier. It is trained and evaluated only on cases where documentation update is required and where the category can be harmonized into one of the supported thesis categories.

Model selection, ensemble selection, and probability calibration use the validation split only. The locked-test split is used only for final reporting.
