# Thesis Evidence Map 2026-08

This document separates the evidence streams for the DocGuard MSc thesis so results are not overclaimed across tasks.

| Evidence stream | Dataset | What it supports | Key result | What not to claim |
| --- | --- | --- | --- | --- |
| Controlled synthetic benchmark | DocGuard synthetic v0.4 | End-to-end DocGuard pipeline on controlled REST API documentation scenarios | Hybrid/HF embedding reports show perfect synthetic test performance | Do not treat this alone as real-world generalization because generator/template bias is possible. |
| Real positive sensitivity | CoDocBench positive sample | The zero-shot model detects real code-doc/comment co-change positives | `code_diff_only` positive recall 100.00% on 500 positives | Do not report precision/F1/FPR because the sample is positive-only. |
| Synthetic negative sanity | Synthetic no-update controls | The model is not constant-positive on in-domain synthetic negatives | 0/500 false positives in both tested input modes | Do not treat this as external negative evidence. |
| External binary proxy zero-shot | Deep-JIT / DocChecker-style code-comment consistency | External binary proxy exposes domain/task shift | Accuracy 50.40%, recall 100.00%, FPR 99.20%, specificity 0.80%, MCC 0.0635 | Do not call this deployment-ready or project-level Markdown documentation performance. |
| External task-specific adaptation | Deep-JIT classical v2 classifier | External training improves binary specificity on code-comment consistency | Current best: accuracy 75.60%, precision 78.84%, recall 69.99%, F1 74.15%, FPR 18.79%, specificity 81.21%, MCC 0.5153 | Do not merge this into the main DocGuard synthetic benchmark or claim Markdown patch generation. |
| Project-level real case study | Manually labeled GitHub commits/PRs | Directly evaluates the DocGuard agent workflow on real software-project documentation cases | 20 real public GitHub PR cases collected, hardened, and validator passed; runner deferred pending adapter | Do not report this small study as a large benchmark or use audit-only fields as model input. |
| Live flow playground | Invented `atlas_review_api` mini project | End-to-end implementation sanity/demo for DocGuard agent flow across documentation classes | 15 synthetic live cases generated and run through `docguard_hybrid.predict()` | Do not report as benchmark performance or real-world evidence. |
| Project evolution live demo | Three invented evolving projects | Explains the end-to-end DocGuard workflow across realistic PR-like synthetic changes | 24 synthetic PR-like changes; binary/category/target/scenario accuracy 95.83%; walkthrough report generated | Do not report as external benchmark evidence or production readiness. |
| Optional LLM patch-generation architecture | Project evolution mock backend | Prepares richer grounded documentation patch drafting after routing | Mock backend, postprocessor, and verifier implemented; no model downloaded or run | Do not report as real LLM performance or patch-quality benchmark. |

## Thesis-Safe Claims

- DocGuard is a prototype NLP agent for code/documentation consistency analysis.
- The controlled synthetic benchmark demonstrates that the pipeline can learn the intended detection, routing, categorization, and patch-targeting structure.
- External positive validation shows strong sensitivity to real code-documentation co-change signals.
- External binary proxy validation reveals that synthetic-trained zero-shot DocGuard over-predicts update needs on real consistent comments.
- Task-specific external adaptation substantially improves specificity, showing that external calibration/training is necessary for practical binary consistency detection.
- The next required alignment step is a project-level real case study that evaluates DocGuard detection, category/target routing, and patch usefulness.

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

## Classical V2 Update

The stronger classical v2 Deep-JIT proxy baseline now supersedes the earlier combined-validation TF-IDF baseline as the primary Deep-JIT proxy result. It uses `logreg_balanced` with `word_char_tfidf_plus_manual_features` and `old_comment_plus_code_diff`, selected by validation MCC. On the untouched combined-validation test split it reaches 75.60% accuracy, 78.84% precision, 69.99% recall, 74.15% F1, 18.79% FPR, 81.21% specificity, and MCC 0.5153.

The older combined-validation result remains a historical baseline: 66.41% accuracy, 68.82% precision, 60.01% recall, 64.12% F1, 27.19% FPR, 72.81% specificity, and MCC 0.3310.

## Project-Level Case Study Update

A project-level case-study schema and validator have been added to keep DocGuard aligned with the thesis title. The first real file contains 20 public GitHub PR cases: 15 positive documentation-update cases and 5 negative no-update cases. Methodology hardening lowered three weaker negative cases to low confidence, leaving 15 high, 2 medium, and 3 low confidence labels. Validation passed. This is the next DocGuard-agent-centered evidence stream; Deep-JIT remains supporting proxy evidence only.

The automatic case-study runner is deferred because the current DocGuard runtime expects synthetic records and synthetic REST route patterns. Safe automatic inputs are limited to `language`, `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt`. Documentation-file presence (`changed_files`/`docs_changed_files`), manually assigned `change_type`, docs-after text, and gold/manual fields are audit-only. A real-case adapter should be added before computing automatic case-study scores.

## Live Flow Playground Update

A small synthetic live-flow playground was added under `docguard_demo/`. It generates an invented `atlas_review_api` mini project and 15 live demo cases covering API reference, model contract, configuration, testing instructions, workflow documentation, architecture flow, developer setup, changelog, and no-update categories. It is useful as a final implementation sanity/demo layer before thesis writing, but it is not a benchmark and should not be used as real-world performance evidence.

## Project Evolution Live Demo Update

A stronger synthetic project-evolution demo now generates `atlas_review_api`, `beacon_billing_service`, and `nova_task_platform` under `generated_live_demo_projects/project_evolution/`. It simulates 24 PR-like changes across API reference, model contract, configuration, testing instructions, workflow documentation, architecture flow, developer setup, changelog, and no-update categories.

The runner uses sanitized prediction input only: project id, case id, code-side changed files, code diff, and docs-before excerpt. It does not pass docs-after text, gold labels, expected facts, manually assigned scenario type, manually assigned category, or target doc file into `docguard_hybrid.predict()`.

Current project-evolution metrics are 95.83% binary accuracy, 94.44% precision, 100.00% recall, 97.14% F1, 95.83% category accuracy, 95.83% target file accuracy, and 95.83% scenario accuracy. One hard false positive remains visible where docs-before already says the endpoint is documented but the positive route-added signal wins. The walkthrough report is useful for thesis/demo screenshots because it shows the code change, documentation before, DocGuard's interpretation, target document, generated patch, and routing reason.

## LLM Patch-Generation Architecture Update

An optional LLM documentation patch-generation layer has been prepared in `docguard_llm/`. It keeps detection and routing separate in `docguard_hybrid`, then builds a patch prompt using only sanitized runtime inputs: code diff, docs-before excerpt, predicted category, predicted target file, router signals, router reason, and project id. Gold labels, expected facts, expected patch summaries, docs-after text, and manual notes are excluded.

The default project-evolution runner still uses the legacy rule-based patch generator. The `llm-mock` backend exercises prompt building, mock generation, postprocessing, and lightweight verifier checks without downloading a model, training, or requiring GPU. The optional `llm-hf` backend is now wired for explicit HuggingFace zero-shot/few-shot patch generation with a user-provided model name, but it is not run during normal validation. Recommended first models are `Qwen/Qwen2.5-1.5B-Instruct` and, if resources allow, `Qwen/Qwen2.5-3B-Instruct`; 7B models should be reserved for cheap GPU/Colab.

This remains architecture and optional-inference evidence only. It should not be reported as real LLM patch-quality performance unless an explicit HF smoke/evaluation run is executed and documented.

The first Qwen 1.5B smoke run exposed unsupported patch details, so the LLM patch path now includes allowed-fact extraction, stricter prompts, and a stronger verifier. This is a methodological hardening step, not a new performance benchmark.
