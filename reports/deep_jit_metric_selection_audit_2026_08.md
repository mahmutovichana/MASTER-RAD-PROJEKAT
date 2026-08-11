# Deep-JIT Metric And Model-Selection Audit 2026-08

## Summary

The current selection procedure is methodologically acceptable but should be described carefully. Validation F1 is reasonable for a balanced binary proxy, but it is not the only relevant criterion. For thesis interpretation, specificity, false-positive rate, balanced accuracy, and MCC are more informative because the zero-shot model has a misleadingly high F1 from near always-positive behavior.

## Current Procedure

- Model selection: validation F1, with validation balanced accuracy as tie-breaker.
- Final model metrics: reported once on test.
- Threshold tuning: selected on validation balanced accuracy/F1 and applied once to test.
- No threshold is tuned on test.

## Audit Findings

| Question | Assessment |
| --- | --- |
| Is validation F1 the right selection criterion? | Acceptable, but not ideal alone. F1 hides true-negative quality and can reward positive-heavy behavior. |
| Should balanced accuracy or MCC be primary? | For thesis interpretation, yes. For model selection, balanced accuracy or MCC would better match the specificity problem. |
| Should the thesis report multiple operating points? | Yes. Report default classifier threshold and validation-selected threshold as two operating points. |
| Does threshold 0.45 improve F1 but worsen FPR? | Compared with default selected model, threshold 0.45 improves F1 from 65.24% to 67.32%, but worsens FPR from 21.27% to 31.31%. It trades specificity for recall. |
| Are specificity, balanced accuracy, MCC, FPR, and FNR reported where needed? | Now yes in Deep-JIT model comparison, zero-shot comparison, best-model error analysis, threshold tuning, and thesis evidence map. |
| Is zero-shot F1 contextualized? | Yes. It is described as misleading because zero-shot behaves near always-positive with 99.20% FPR and 0.80% specificity. |

## Recommended Thesis Reporting

Report the Deep-JIT trained classifier in two rows:

1. Default `tfidf_logreg` decision, selected by validation F1:
   - Accuracy 68.72%
   - Precision 73.41%
   - Recall 58.71%
   - F1 65.24%
   - FPR 21.27%
   - Specificity 78.73%
   - MCC 0.3821

2. Validation-selected threshold 0.45:
   - Accuracy 67.65%
   - Precision 68.03%
   - Recall 66.62%
   - F1 67.32%
   - FPR 31.31%
   - Specificity 68.69%
   - MCC 0.3531

Interpretation: threshold tuning improves recall/F1 but sacrifices specificity. Since the main scientific issue was false positives, the default decision rule may be more attractive despite lower F1.

## Recommended Future Improvement

Rerun selection with MCC or balanced accuracy as the primary validation criterion after adding Summary validation coverage. This is not required to keep current results, but it would make the model-selection story cleaner.

## Robustness Experiment Added

The Summary validation carve-out was implemented and the combined-validation run selected `tfidf_linear_svc + old_comment_plus_code_diff` by validation F1. Its default test metrics were:

- Accuracy: 66.41%
- Precision: 68.82%
- Recall: 60.01%
- F1: 64.12%
- FPR: 27.19%
- Specificity: 72.81%
- Balanced accuracy: 66.41%
- MCC: 0.3310

This is slightly weaker than the previous Return-only-validation selected model. The change confirms that model selection is sensitive to validation subset composition. The combined-validation result should be preferred methodologically because Summary appears in validation, even though it is not the most favorable result numerically.

Note: within the combined-validation test table, `tfidf_logreg + old_comment_plus_code_diff` has stronger test metrics than the selected SVC model, but it was not selected by validation F1. It should not replace the selected model unless the model-selection criterion is changed and rerun on validation only.
