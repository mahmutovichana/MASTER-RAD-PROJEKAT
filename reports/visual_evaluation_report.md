# Visual Evaluation Report

These figures summarize dataset v0.3 and the rule-based baseline. ROC and precision-recall curves use simple baseline scores: 1.0 for confident positive, 0.0 for confident negative, and 0.5 for unknown or unsupported changes. They are included for completeness; these curves will be more meaningful for the later NLP-assisted model.

Figure generation tries to use matplotlib first. In this local environment matplotlib was unavailable, so the script can fall back to a small built-in PNG renderer while preserving the same output filenames.

## baseline_metrics_v0_1_v0_2_v0_3

![baseline_metrics_v0_1_v0_2_v0_3](figures/baseline_metrics_v0_1_v0_2_v0_3.png)

## binary_confusion_matrix_v0_3

![binary_confusion_matrix_v0_3](figures/binary_confusion_matrix_v0_3.png)

## dataset_version_record_counts

![dataset_version_record_counts](figures/dataset_version_record_counts.png)

## doc_category_distribution_v0_3

![doc_category_distribution_v0_3](figures/doc_category_distribution_v0_3.png)

## per_doc_category_accuracy_v0_3

![per_doc_category_accuracy_v0_3](figures/per_doc_category_accuracy_v0_3.png)

## per_scenario_accuracy_v0_3

![per_scenario_accuracy_v0_3](figures/per_scenario_accuracy_v0_3.png)

## positive_negative_distribution_v0_3

![positive_negative_distribution_v0_3](figures/positive_negative_distribution_v0_3.png)

## precision_recall_curve_v0_3

![precision_recall_curve_v0_3](figures/precision_recall_curve_v0_3.png)

## roc_curve_v0_3

![roc_curve_v0_3](figures/roc_curve_v0_3.png)

## scenario_confusion_matrix_v0_3

![scenario_confusion_matrix_v0_3](figures/scenario_confusion_matrix_v0_3.png)

## scenario_distribution_v0_3

![scenario_distribution_v0_3](figures/scenario_distribution_v0_3.png)

## split_distribution_v0_3

![split_distribution_v0_3](figures/split_distribution_v0_3.png)
