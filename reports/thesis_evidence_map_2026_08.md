# Thesis Evidence Map 2026-08

This document separates the evidence streams for the DocGuard MSc thesis so results are not overclaimed across tasks.

| Evidence stream | Dataset | What it supports | Key result | What not to claim |
| --- | --- | --- | --- | --- |
| Controlled synthetic benchmark | DocGuard synthetic v0.4 | End-to-end DocGuard pipeline on controlled REST API documentation scenarios | Hybrid/HF embedding reports show perfect synthetic test performance | Do not treat this alone as real-world generalization because generator/template bias is possible. |
| Real positive sensitivity | CoDocBench positive sample | The zero-shot model detects real code-doc/comment co-change positives | `code_diff_only` positive recall 100.00% on 500 positives | Do not report precision/F1/FPR because the sample is positive-only. |
| Synthetic negative sanity | Synthetic no-update controls | The model is not constant-positive on in-domain synthetic negatives | 0/500 false positives in both tested input modes | Do not treat this as external negative evidence. |
| External binary proxy zero-shot | Deep-JIT / DocChecker-style code-comment consistency | External binary proxy exposes domain/task shift | Accuracy 50.40%, recall 100.00%, FPR 99.20%, specificity 0.80%, MCC 0.0635 | Do not call this deployment-ready or project-level Markdown documentation performance. |
| External task-specific adaptation | Deep-JIT TF-IDF classifier | External training improves binary specificity on code-comment consistency | Accuracy 66.41%, precision 68.82%, recall 60.01%, FPR 27.19%, specificity 72.81%, MCC 0.3310 | Do not merge this into the main DocGuard synthetic benchmark or claim Markdown patch generation. |

## Thesis-Safe Claims

- DocGuard is a prototype NLP agent for code/documentation consistency analysis.
- The controlled synthetic benchmark demonstrates that the pipeline can learn the intended detection, routing, categorization, and patch-targeting structure.
- External positive validation shows strong sensitivity to real code-documentation co-change signals.
- External binary proxy validation reveals that synthetic-trained zero-shot DocGuard over-predicts update needs on real consistent comments.
- Task-specific external adaptation substantially improves specificity, showing that external calibration/training is necessary for practical binary consistency detection.

## Claims To Avoid

- Do not claim production readiness.
- Do not report synthetic v0.4 metrics as final real-world performance.
- Do not report CoDocBench positive recall as precision or F1.
- Do not report Deep-JIT as full project-level Markdown API documentation evaluation.
- Do not call Deep-JIT numeric label polarity fully confirmed until original documentation or preprocessing code explicitly confirms it.

## Remaining Methodological Caveat

Deep-JIT numeric label polarity remains `plausible_manual_verification_needed`. The current mapping is supported by sampled examples and task framing, but final thesis text should either cite an explicit polarity source or describe the mapping as manually audited and plausible.

## Robustness Update

A deterministic Summary validation carve-out robustness experiment was added to reduce Return-only validation bias. The model choice changed and test metrics became slightly weaker, which shows that the earlier Return-only validation setup was sensitive to subset composition. The combined-validation result should be considered the cleaner Deep-JIT model-selection setup, while the older Return-only result remains a useful historical baseline.
