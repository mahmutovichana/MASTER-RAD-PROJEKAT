# Thesis Alignment And Result Improvement Plan 2026-08

## Original Thesis Goal

The thesis goal is an intelligent NLP agent for consistency analysis of software projects: code diff -> update-required detection -> category/target routing -> documentation patch suggestion -> developer workflow. In the current repository, this is represented by DocGuard rather than by the Deep-JIT classifier alone.

## Current Repo Alignment

The central DocGuard artifact is still present:

- `docguard/` implements deterministic change analysis, classification, evaluation, and patch generation.
- `docguard_llm/` implements an LLM-assisted agent path with prompt building, label normalization, JSON parsing, and Hugging Face/local backends.
- `docguard_hf_classifier/` implements embedding/classifier experiments for the synthetic DocGuard task.
- `vscode-docguard/` and `examples/vscode_demo/` support the developer workflow story.
- `scripts/`, `schema/`, `data/`, and `dataset_versions/` preserve the controlled synthetic benchmark structure.

## Proxy Benchmark Components

The Deep-JIT / DocChecker-style flow in `docguard_external/` is a proxy benchmark for binary code-comment consistency. It is useful external evidence, but it is not the full project-level Markdown documentation task because it does not evaluate documentation file routing or patch usefulness.

CoDocBench positive-only evaluation is also external evidence, but it supports positive sensitivity only. It does not provide precision, F1, or false-positive quality without a defensible negative set.

## Drift Assessment

The project has not drifted too far if Deep-JIT remains an external validation stream. It would drift if the thesis framed the Deep-JIT classifier as the central contribution. The central artifact must remain the DocGuard agent: a code/documentation consistency assistant that detects update needs, routes targets/categories, and proposes documentation patches.

## Weak Claims

- Synthetic v0.4 performance is too clean to stand alone as final real-world evidence.
- CoDocBench positive recall cannot support precision, F1, or false-positive claims.
- Deep-JIT zero-shot exposes poor specificity and should not be hidden.
- The combined-validation Deep-JIT trained result is methodologically cleaner but numerically modest: 66.41% accuracy, 64.12% F1, 27.19% FPR, MCC 0.3310.
- Deep-JIT label polarity remains `plausible_manual_verification_needed` until explicitly documented or manually audited at sufficient depth.

## Results To Improve Before Thesis Writing

- Improve the Deep-JIT external binary proxy beyond the current combined-validation baseline, preferably toward >=70% accuracy or >=0.40 MCC while keeping FPR below roughly 25-30%.
- Add a project-level real-world DocGuard case study with human audit of detection, routing, target file, and patch usefulness.
- Preserve existing weak results as evidence of domain shift rather than deleting or softening them.

## CPU-Feasible Improvements

- Stronger classical TF-IDF baselines with word 1-3 grams, char 3-5 grams, word+char unions, and manual numerical features.
- Validation-MCC or balanced-accuracy model selection instead of F1-only selection.
- Frozen pretrained code-encoder embeddings followed by LogisticRegression or LinearSVC, if dependencies and model downloads are available.
- Small manually audited project-level case study.

## GPU / Colab Improvements

- UniXcoder or CodeBERT sequence classifier fine-tuning.
- Last-2-layer unfreeze experiments.
- Full transformer fine-tuning with careful early stopping.

## Recommended Direction

Keep DocGuard as the thesis artifact. Use Deep-JIT as external binary proxy evidence and improve it with stronger CPU baselines first. Then run a frozen code-encoder baseline if local dependencies and download/hardware allow. Use Colab only if CPU baselines remain below target and thesis time permits.
