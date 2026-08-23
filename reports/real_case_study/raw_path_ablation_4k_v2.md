# Raw Path Ablation — Real Gold Classifier 4k V2

## Purpose

This ablation evaluates whether the V2 improvement depends on manually engineered path flags such as:

- `path_flag_api_route`
- `path_flag_schema_contract`
- `path_flag_configuration`
- `path_flag_test_or_fixture`

The ablation adds raw-path variants that use file paths as lexical features without manual path-category flags.

The goal is to verify that the improvement is not merely caused by hand-written decision rules.

## Methodological status

This is an ablation experiment.

The primary frozen V2 model remains:

- `path_heavy_word_char_logreg`
- threshold: `0.80`
- selected by validation using `constrained_f1`
- locked-test used only for final reporting

The raw-path models are not promoted to primary model based on locked-test performance.

## Locked-test comparison

| Model | Threshold | Precision | Recall | F1 | Specificity | MCC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `word_logreg` | 0.85 | 0.9606 | 0.7394 | 0.8356 | 0.8800 | 0.5106 |
| `word_logreg_balanced` | 0.65 | 0.9709 | 0.7414 | 0.8408 | 0.9120 | 0.5374 |
| `char_logreg` | 0.80 | 0.9561 | 0.7475 | 0.8390 | 0.8640 | 0.5065 |
| `word_char_logreg` | 0.85 | 0.9706 | 0.7333 | 0.8354 | 0.9120 | 0.5292 |
| `word_char_logreg_balanced` | 0.60 | 0.9651 | 0.7818 | 0.8638 | 0.8880 | 0.5622 |
| `path_raw_word_char_logreg` | 0.75 | 0.9413 | 0.8424 | 0.8891 | 0.7920 | 0.5636 |
| `path_raw_word_char_logreg_balanced` | 0.55 | 0.9492 | 0.8303 | 0.8858 | 0.8240 | 0.5720 |
| `path_heavy_word_char_logreg` | 0.80 | 0.9543 | 0.8020 | 0.8716 | 0.8480 | 0.5550 |
| `path_heavy_word_char_logreg_balanced` | 0.60 | 0.9591 | 0.8061 | 0.8760 | 0.8640 | 0.5722 |
| `linear_svc_word_char` | 0.85 | 0.9884 | 0.6909 | 0.8133 | 0.9680 | 0.5323 |
| `linear_svc_word_char_balanced` | 0.85 | 0.9881 | 0.6727 | 0.8005 | 0.9680 | 0.5161 |

## Interpretation

The raw-path models perform strongly even without manual path flags.

This supports the conclusion that path information is useful as a learned lexical signal, rather than merely acting as a hand-coded rule system.

The strongest raw-path variant achieves:

- F1: `0.8891`
- precision: `0.9413`
- recall: `0.8424`
- specificity: `0.7920`
- MCC: `0.5636`

The balanced raw-path variant achieves the strongest MCC among the raw-path models:

- F1: `0.8858`
- precision: `0.9492`
- recall: `0.8303`
- specificity: `0.8240`
- MCC: `0.5720`

The primary frozen V2 model remains `path_heavy_word_char_logreg`, because model selection is based on validation, not on locked-test inspection.

## Thesis-safe conclusion

The ablation indicates that the improvement of the V2 classifier is not dependent on manually encoded path-category flags. Strong performance is retained when file paths are represented through raw lexical path features only.

This reduces the risk that the model behaves as a manually tuned rule system.