# DocGuard Project-Level Real Case Study Plan 2026-08

## Goal

Re-align the thesis evidence with the original DocGuard agent goal: intelligent NLP analysis of software project consistency. This study evaluates the practical DocGuard workflow, not only Deep-JIT binary code-comment classification.

## Target Sample

Create 15-30 manually labeled real GitHub cases. Each case should be small enough for human audit and should include a code diff excerpt plus documentation-before excerpt.

Recommended mix:

- API endpoint changes
- validation changes
- request/response schema changes
- configuration changes
- testing command changes
- workflow changes
- documentation already updated
- internal refactors with no documentation update needed

## Why This Supports The Thesis Better Than Deep-JIT Alone

Deep-JIT v2 is useful external binary proxy evidence, but it only measures whether an old code comment became inconsistent after a code change. The thesis artifact is broader: DocGuard should identify whether project documentation needs an update, route the change to a category/target, and suggest a documentation patch.

This case study directly evaluates that agent behavior on real project-level examples.

## Evaluation Targets

- Binary `docs_update_required` detection.
- Documentation category prediction.
- Target documentation file prediction.
- Target section prediction when visible.
- Patch usefulness by human review.

## Metrics

- Accuracy, precision, recall, and F1 for binary detection.
- Category accuracy for positive cases.
- Target-file accuracy for cases with a visible target file.
- Human patch usefulness rating: acceptable, partially acceptable, not acceptable.

## Limitations

- Small sample size.
- Manual labels may contain reviewer judgment.
- Qualitative/semi-quantitative rather than a large benchmark.
- Not a replacement for a large real-world dataset.
- Should be reported alongside, not instead of, synthetic benchmark and external proxy evidence.

## Required Artifacts

- `data/external/project_case_study/manual_cases.jsonl`
- `reports/docguard_project_case_study_predictions_2026_08.jsonl`
- `reports/docguard_project_case_study_evaluation_2026_08.md`
- reviewer notes for uncertain and failed cases
