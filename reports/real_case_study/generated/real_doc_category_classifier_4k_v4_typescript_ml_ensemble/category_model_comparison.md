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
      "api_reference": 765,
      "configuration": 510,
      "developer_setup": 343,
      "model_contract": 527
    },
    "validation": {
      "api_reference": 191,
      "configuration": 162,
      "developer_setup": 74,
      "model_contract": 92
    }
  },
  "language_filter": "typescript",
  "row_counts": {
    "locked_test": 386,
    "train": 2145,
    "validation": 519
  }
}
```

## Selected ensemble

```json
{
  "ensemble_size": 5,
  "selected_model_names": [
    "path_raw_word_char_logreg_balanced_c4.0",
    "path_raw_word_char_logreg_balanced_c2.0",
    "path_raw_word_char_logreg_balanced_c8.0",
    "code_docs_path_raw_logreg_balanced_c8.0",
    "path_raw_word_char_logreg_balanced_c0.5"
  ],
  "validation_weights": {
    "code_docs_path_raw_logreg_balanced_c8.0": 0.4542917064073172,
    "path_raw_word_char_logreg_balanced_c0.5": 0.4438116541965564,
    "path_raw_word_char_logreg_balanced_c2.0": 0.4736401861523588,
    "path_raw_word_char_logreg_balanced_c4.0": 0.4765914771159002,
    "path_raw_word_char_logreg_balanced_c8.0": 0.4707825084014957
  },
  "weights_source": "validation_macro_f1"
}
```

## Single-model comparison

| Model | Validation macro-F1 | Validation weighted-F1 | Validation accuracy | Locked macro-F1 | Locked weighted-F1 | Locked accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `word_logreg_c0.05` | 0.1345 | 0.1980 | 0.3680 | 0.1472 | 0.2455 | 0.4171 |
| `word_logreg_balanced_c0.05` | 0.2641 | 0.2845 | 0.4143 | 0.2906 | 0.3622 | 0.4715 |
| `word_char_logreg_balanced_c0.05` | 0.2817 | 0.2986 | 0.4085 | 0.3302 | 0.4111 | 0.4896 |
| `path_raw_word_char_logreg_balanced_c0.05` | 0.3820 | 0.4304 | 0.4759 | 0.3814 | 0.4372 | 0.5052 |
| `code_docs_path_raw_logreg_balanced_c0.05` | 0.3133 | 0.3453 | 0.4277 | 0.3504 | 0.4131 | 0.4922 |
| `word_logreg_c0.1` | 0.1345 | 0.1980 | 0.3680 | 0.1472 | 0.2455 | 0.4171 |
| `word_logreg_balanced_c0.1` | 0.2623 | 0.2816 | 0.4066 | 0.2963 | 0.3612 | 0.4715 |
| `word_char_logreg_balanced_c0.1` | 0.3172 | 0.3419 | 0.4316 | 0.3850 | 0.4423 | 0.5078 |
| `path_raw_word_char_logreg_balanced_c0.1` | 0.4012 | 0.4504 | 0.4971 | 0.3917 | 0.4477 | 0.5104 |
| `code_docs_path_raw_logreg_balanced_c0.1` | 0.3474 | 0.3787 | 0.4470 | 0.3716 | 0.4247 | 0.5000 |
| `word_logreg_c0.25` | 0.1349 | 0.1986 | 0.3680 | 0.1528 | 0.2511 | 0.4197 |
| `word_logreg_balanced_c0.25` | 0.2825 | 0.3074 | 0.4181 | 0.3085 | 0.3743 | 0.4767 |
| `word_char_logreg_balanced_c0.25` | 0.3481 | 0.3774 | 0.4470 | 0.4126 | 0.4590 | 0.5181 |
| `path_raw_word_char_logreg_balanced_c0.25` | 0.4324 | 0.4842 | 0.5260 | 0.3919 | 0.4523 | 0.5130 |
| `code_docs_path_raw_logreg_balanced_c0.25` | 0.3905 | 0.4221 | 0.4721 | 0.3823 | 0.4330 | 0.5026 |
| `word_logreg_c0.5` | 0.1608 | 0.2235 | 0.3796 | 0.1946 | 0.2946 | 0.4404 |
| `word_logreg_balanced_c0.5` | 0.3007 | 0.3260 | 0.4258 | 0.3464 | 0.3913 | 0.4845 |
| `word_char_logreg_balanced_c0.5` | 0.3767 | 0.4086 | 0.4605 | 0.4304 | 0.4677 | 0.5233 |
| `path_raw_word_char_logreg_balanced_c0.5` | 0.4438 | 0.4908 | 0.5279 | 0.3849 | 0.4394 | 0.5026 |
| `code_docs_path_raw_logreg_balanced_c0.5` | 0.4065 | 0.4416 | 0.4855 | 0.3829 | 0.4360 | 0.5026 |
| `word_logreg_c1.0` | 0.1781 | 0.2454 | 0.3873 | 0.2520 | 0.3453 | 0.4637 |
| `word_logreg_balanced_c1.0` | 0.3027 | 0.3317 | 0.4239 | 0.3786 | 0.4118 | 0.4974 |
| `word_char_logreg_balanced_c1.0` | 0.3855 | 0.4280 | 0.4778 | 0.4481 | 0.4861 | 0.5363 |
| `path_raw_word_char_logreg_balanced_c1.0` | 0.4429 | 0.4927 | 0.5299 | 0.3962 | 0.4472 | 0.5078 |
| `code_docs_path_raw_logreg_balanced_c1.0` | 0.4242 | 0.4577 | 0.4952 | 0.3747 | 0.4290 | 0.4974 |
| `word_logreg_c2.0` | 0.2010 | 0.2654 | 0.3931 | 0.2587 | 0.3518 | 0.4637 |
| `word_logreg_balanced_c2.0` | 0.3071 | 0.3416 | 0.4220 | 0.3756 | 0.4139 | 0.4974 |
| `word_char_logreg_balanced_c2.0` | 0.4253 | 0.4646 | 0.5029 | 0.4435 | 0.4787 | 0.5311 |
| `path_raw_word_char_logreg_balanced_c2.0` | 0.4736 | 0.5228 | 0.5530 | 0.3966 | 0.4446 | 0.5078 |
| `code_docs_path_raw_logreg_balanced_c2.0` | 0.4374 | 0.4715 | 0.5048 | 0.3677 | 0.4215 | 0.4922 |
| `word_logreg_c4.0` | 0.2255 | 0.2833 | 0.3969 | 0.2549 | 0.3477 | 0.4585 |
| `word_logreg_balanced_c4.0` | 0.3082 | 0.3458 | 0.4181 | 0.3788 | 0.4170 | 0.4974 |
| `word_char_logreg_balanced_c4.0` | 0.4305 | 0.4671 | 0.5010 | 0.4402 | 0.4788 | 0.5311 |
| `path_raw_word_char_logreg_balanced_c4.0` | 0.4766 | 0.5236 | 0.5530 | 0.3926 | 0.4376 | 0.5026 |
| `code_docs_path_raw_logreg_balanced_c4.0` | 0.4429 | 0.4763 | 0.5087 | 0.3592 | 0.4138 | 0.4870 |
| `word_logreg_c8.0` | 0.2378 | 0.2960 | 0.3969 | 0.2757 | 0.3616 | 0.4637 |
| `word_logreg_balanced_c8.0` | 0.3220 | 0.3585 | 0.4239 | 0.3927 | 0.4287 | 0.5052 |
| `word_char_logreg_balanced_c8.0` | 0.4405 | 0.4748 | 0.5048 | 0.4399 | 0.4813 | 0.5337 |
| `path_raw_word_char_logreg_balanced_c8.0` | 0.4708 | 0.5157 | 0.5453 | 0.3959 | 0.4412 | 0.5052 |
| `code_docs_path_raw_logreg_balanced_c8.0` | 0.4543 | 0.4879 | 0.5183 | 0.3565 | 0.4113 | 0.4870 |

## Ensemble metrics

```json
{
  "locked_test": {
    "accuracy": 0.5544041450777202,
    "classification_report": {
      "accuracy": 0.5544041450777202,
      "api_reference": {
        "f1-score": 0.6855524079320113,
        "precision": 0.6302083333333334,
        "recall": 0.7515527950310559,
        "support": 161.0
      },
      "configuration": {
        "f1-score": 0.40476190476190477,
        "precision": 0.4788732394366197,
        "recall": 0.35051546391752575,
        "support": 97.0
      },
      "developer_setup": {
        "f1-score": 0.5116279069767442,
        "precision": 0.43137254901960786,
        "recall": 0.6285714285714286,
        "support": 35.0
      },
      "macro avg": {
        "f1-score": 0.5126067670388772,
        "precision": 0.5135857526696124,
        "recall": 0.5321222874714004,
        "support": 386.0
      },
      "model_contract": {
        "f1-score": 0.4484848484848485,
        "precision": 0.5138888888888888,
        "recall": 0.3978494623655914,
        "support": 93.0
      },
      "weighted avg": {
        "f1-score": 0.5421033940213357,
        "precision": 0.5461242273947454,
        "recall": 0.5544041450777202,
        "support": 386.0
      }
    },
    "confusion_matrix": [
      [
        121,
        22,
        11,
        7
      ],
      [
        32,
        34,
        13,
        18
      ],
      [
        1,
        2,
        22,
        10
      ],
      [
        38,
        13,
        5,
        37
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
    "macro_f1": 0.5126067670388772,
    "pred_distribution": {
      "api_reference": 192,
      "configuration": 71,
      "developer_setup": 51,
      "model_contract": 72
    },
    "weighted_f1": 0.5421033940213357
  },
  "train": {
    "accuracy": 0.9571095571095571,
    "classification_report": {
      "accuracy": 0.9571095571095571,
      "api_reference": {
        "f1-score": 0.9462809917355371,
        "precision": 1.0,
        "recall": 0.8980392156862745,
        "support": 765.0
      },
      "configuration": {
        "f1-score": 0.9698736637512148,
        "precision": 0.9614643545279383,
        "recall": 0.9784313725490196,
        "support": 510.0
      },
      "developer_setup": {
        "f1-score": 0.9384404924760602,
        "precision": 0.884020618556701,
        "recall": 1.0,
        "support": 343.0
      },
      "macro avg": {
        "f1-score": 0.9566914586048032,
        "precision": 0.9491207895506517,
        "recall": 0.9676944971537002,
        "support": 2145.0
      },
      "model_contract": {
        "f1-score": 0.9721706864564007,
        "precision": 0.9509981851179673,
        "recall": 0.9943074003795066,
        "support": 527.0
      },
      "weighted avg": {
        "f1-score": 0.9569974675396818,
        "precision": 0.9602526510635738,
        "recall": 0.9571095571095571,
        "support": 2145.0
      }
    },
    "confusion_matrix": [
      [
        687,
        20,
        32,
        26
      ],
      [
        0,
        499,
        10,
        1
      ],
      [
        0,
        0,
        343,
        0
      ],
      [
        0,
        0,
        3,
        524
      ]
    ],
    "gold_distribution": {
      "api_reference": 765,
      "configuration": 510,
      "developer_setup": 343,
      "model_contract": 527
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.9566914586048032,
    "pred_distribution": {
      "api_reference": 687,
      "configuration": 519,
      "developer_setup": 388,
      "model_contract": 551
    },
    "weighted_f1": 0.9569974675396818
  },
  "validation": {
    "accuracy": 0.6223506743737958,
    "classification_report": {
      "accuracy": 0.6223506743737958,
      "api_reference": {
        "f1-score": 0.6796657381615598,
        "precision": 0.7261904761904762,
        "recall": 0.6387434554973822,
        "support": 191.0
      },
      "configuration": {
        "f1-score": 0.6684210526315789,
        "precision": 0.5825688073394495,
        "recall": 0.7839506172839507,
        "support": 162.0
      },
      "developer_setup": {
        "f1-score": 0.5271317829457365,
        "precision": 0.6181818181818182,
        "recall": 0.4594594594594595,
        "support": 74.0
      },
      "macro avg": {
        "f1-score": 0.5864517022582483,
        "precision": 0.6099404036330641,
        "recall": 0.5792340352341111,
        "support": 519.0
      },
      "model_contract": {
        "f1-score": 0.47058823529411764,
        "precision": 0.5128205128205128,
        "recall": 0.43478260869565216,
        "support": 92.0
      },
      "weighted avg": {
        "f1-score": 0.617345348940688,
        "precision": 0.6281377061007968,
        "recall": 0.6223506743737958,
        "support": 519.0
      }
    },
    "confusion_matrix": [
      [
        122,
        44,
        8,
        17
      ],
      [
        23,
        127,
        3,
        9
      ],
      [
        4,
        24,
        34,
        12
      ],
      [
        19,
        23,
        10,
        40
      ]
    ],
    "gold_distribution": {
      "api_reference": 191,
      "configuration": 162,
      "developer_setup": 74,
      "model_contract": 92
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.5864517022582483,
    "pred_distribution": {
      "api_reference": 168,
      "configuration": 218,
      "developer_setup": 55,
      "model_contract": 78
    },
    "weighted_f1": 0.617345348940688
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
    "api_reference": 0.5,
    "configuration": 1.0,
    "developer_setup": 1.5,
    "model_contract": 1.25
  },
  "validation_metrics_after_calibration": {
    "accuracy": 0.6223506743737958,
    "classification_report": {
      "accuracy": 0.6223506743737958,
      "api_reference": {
        "f1-score": 0.6796657381615598,
        "precision": 0.7261904761904762,
        "recall": 0.6387434554973822,
        "support": 191.0
      },
      "configuration": {
        "f1-score": 0.6684210526315789,
        "precision": 0.5825688073394495,
        "recall": 0.7839506172839507,
        "support": 162.0
      },
      "developer_setup": {
        "f1-score": 0.5271317829457365,
        "precision": 0.6181818181818182,
        "recall": 0.4594594594594595,
        "support": 74.0
      },
      "macro avg": {
        "f1-score": 0.5864517022582483,
        "precision": 0.6099404036330641,
        "recall": 0.5792340352341111,
        "support": 519.0
      },
      "model_contract": {
        "f1-score": 0.47058823529411764,
        "precision": 0.5128205128205128,
        "recall": 0.43478260869565216,
        "support": 92.0
      },
      "weighted avg": {
        "f1-score": 0.617345348940688,
        "precision": 0.6281377061007968,
        "recall": 0.6223506743737958,
        "support": 519.0
      }
    },
    "confusion_matrix": [
      [
        122,
        44,
        8,
        17
      ],
      [
        23,
        127,
        3,
        9
      ],
      [
        4,
        24,
        34,
        12
      ],
      [
        19,
        23,
        10,
        40
      ]
    ],
    "gold_distribution": {
      "api_reference": 191,
      "configuration": 162,
      "developer_setup": 74,
      "model_contract": 92
    },
    "labels": [
      "api_reference",
      "configuration",
      "developer_setup",
      "model_contract"
    ],
    "macro_f1": 0.5864517022582483,
    "pred_distribution": {
      "api_reference": 168,
      "configuration": 218,
      "developer_setup": 55,
      "model_contract": 78
    },
    "weighted_f1": 0.617345348940688
  }
}
```

## Outputs

```json
{
  "category_model": "models\\real_doc_category_classifier_4k_v4_typescript_ml_ensemble\\best_category_model.joblib",
  "model_comparison_json": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v4_typescript_ml_ensemble\\category_model_comparison.json",
  "model_comparison_md": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v4_typescript_ml_ensemble\\category_model_comparison.md",
  "predictions_jsonl": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v4_typescript_ml_ensemble\\category_predictions.jsonl",
  "summary_json": "reports\\real_case_study\\generated\\real_doc_category_classifier_4k_v4_typescript_ml_ensemble\\category_classifier_summary.json"
}
```

## Methodological note

This is a second-stage category classifier. It is trained and evaluated only on cases where documentation update is required and where the category can be harmonized into one of the supported thesis categories.

Model selection, ensemble selection, and probability calibration use the validation split only. The locked-test split is used only for final reporting.
