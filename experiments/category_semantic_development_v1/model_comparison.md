# Model comparison

| Candidate | Train source | Train Macro-F1 | Validation Macro-F1 | Balanced accuracy | developer_setup F1 | Gap |
|---|---:|---:|---:|---:|---:|---:|
| `hybrid__natural_plus_controlled__ovr_logreg` | natural_plus_controlled | 0.9717 | 0.4542 | 0.4645 | 0.0741 | 0.5175 |
| `hybrid__natural_only__multinomial_logreg` | natural_only | 0.9279 | 0.4485 | 0.4709 | 0.0000 | 0.4793 |
| `hybrid__natural_only__ovr_logreg` | natural_only | 0.8812 | 0.4478 | 0.4729 | 0.0000 | 0.4335 |
| `hybrid__natural_plus_controlled__multinomial_logreg` | natural_plus_controlled | 0.9813 | 0.4312 | 0.4464 | 0.0000 | 0.5502 |
| `semantic__natural_only__ovr_logreg` | natural_only | 0.7579 | 0.4148 | 0.4241 | 0.0000 | 0.3432 |
| `semantic_code_only__natural_only__multinomial_logreg` | natural_only | 0.6463 | 0.4132 | 0.4271 | 0.0870 | 0.2331 |
| `semantic_code_only__natural_plus_controlled__multinomial_logreg` | natural_plus_controlled | 0.9128 | 0.3971 | 0.4105 | 0.1500 | 0.5157 |
| `semantic__natural_plus_controlled__multinomial_logreg` | natural_plus_controlled | 0.9546 | 0.3952 | 0.3963 | 0.0588 | 0.5594 |
| `semantic_code_only__natural_only__ovr_logreg` | natural_only | 0.6178 | 0.3945 | 0.4176 | 0.0000 | 0.2234 |
| `two_channel_lexical__natural_plus_controlled__calibrated_linear_svm` | natural_plus_controlled | 0.9987 | 0.3934 | 0.4287 | 0.0667 | 0.6053 |
| `hybrid__natural_plus_controlled__calibrated_linear_svm` | natural_plus_controlled | 0.9993 | 0.3929 | 0.4110 | 0.0000 | 0.6064 |
| `semantic__natural_only__multinomial_logreg` | natural_only | 0.8000 | 0.3894 | 0.3990 | 0.0000 | 0.4105 |
| `two_channel_lexical__natural_only__multinomial_logreg` | natural_only | 0.8861 | 0.3852 | 0.4319 | 0.0000 | 0.5009 |
| `semantic__natural_plus_controlled__ovr_logreg` | natural_plus_controlled | 0.9436 | 0.3808 | 0.3784 | 0.0465 | 0.5628 |
| `semantic__natural_plus_controlled__calibrated_linear_svm` | natural_plus_controlled | 0.9840 | 0.3688 | 0.3717 | 0.0000 | 0.6152 |
| `two_channel_lexical__natural_plus_controlled__multinomial_logreg` | natural_plus_controlled | 0.9735 | 0.3676 | 0.4146 | 0.0000 | 0.6059 |
| `semantic_code_only__natural_plus_controlled__ovr_logreg` | natural_plus_controlled | 0.9045 | 0.3638 | 0.3840 | 0.1509 | 0.5407 |
| `two_channel_lexical__natural_only__ovr_logreg` | natural_only | 0.8173 | 0.3485 | 0.4053 | 0.0000 | 0.4688 |
| `two_channel_lexical__natural_plus_controlled__ovr_logreg` | natural_plus_controlled | 0.9615 | 0.3259 | 0.3796 | 0.0000 | 0.6356 |
| `hybrid__natural_only__calibrated_linear_svm` | natural_only | 0.6470 | 0.2665 | 0.3325 | 0.0000 | 0.3805 |
| `two_channel_lexical__natural_only__calibrated_linear_svm` | natural_only | 0.6191 | 0.2325 | 0.3202 | 0.0000 | 0.3866 |
| `semantic__natural_only__calibrated_linear_svm` | natural_only | 0.3649 | 0.1620 | 0.2717 | 0.0000 | 0.2029 |
