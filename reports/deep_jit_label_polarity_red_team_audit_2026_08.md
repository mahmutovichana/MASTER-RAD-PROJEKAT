# Deep-JIT Label Polarity Red-Team Audit 2026-08

## Summary

The current mapping remains plausible and supported, but not fully confirmed by an explicit numeric label legend. Keep `plausible_manual_verification_needed`.

## Source Review

| Source | What it supports | Polarity conclusion |
| --- | --- | --- |
| Deep-JIT README | The repository task is inconsistency detection between comments and source code. | Supports task meaning but not numeric label legend. |
| `run_comment_model.py` | `positive_only` keeps examples where `ex.label == 1`. | Confirms `label=1` is the positive class in training code. |
| `detection_evaluation_utils.py` | Evaluation treats truthy gold labels as positive for TP/FN calculations. | Confirms truthy/1 is positive for metrics. |
| `data_loader.py` / `data_utils.py` | Loads label field into examples. | Supports that labels are carried directly, but does not define text meaning. |
| `detection_module.py` | Uses labels for binary classification objective. | Supports binary detection setup, not explicit natural-language polarity. |
| Manual sampled examples | `label=1` examples usually require comment update; `label=0` examples often keep comment unchanged. | Empirically supports `1=inconsistent/update-required`, `0=consistent/no-update`. |

## Direct Answers

| Question | Answer |
| --- | --- |
| Does the code confirm that `label=1` is the positive class? | Yes. `run_comment_model.py` and evaluation utilities treat label 1/truthy as positive. |
| Does any source explicitly say positive means inconsistent/outdated? | The repository/paper framing says the task is inconsistency detection, but no inspected source gives an explicit numeric legend saying `1 = inconsistent`. |
| Does the current mapping remain plausible? | Yes. It is the most plausible mapping. |
| Is there evidence the mapping might be reversed? | No strong evidence. Sampled examples do not suggest reversal. |
| Should the status remain `plausible_manual_verification_needed`? | Yes. |

## Thesis-Safe Wording

Use:

> Deep-JIT labels were mapped as `1 = positive/inconsistent/update-required` and `0 = negative/consistent/no-update`. This mapping is supported by the repository task framing, code paths that treat `label == 1` as the positive class, and manual inspection of sampled examples. However, because the repository README does not provide an explicit numeric label legend, the polarity is reported as plausible and manually audited rather than fully confirmed.

Avoid:

> Deep-JIT documentation explicitly confirms that `1` means inconsistent and `0` means consistent.

That exact explicit documentation was not found.
