# Phase 7 recommendation

## Direct answers

1. Semantic better than TF-IDF V8: **yes**.
2. Two-channel lexical better than concatenated TF-IDF V8: **yes**.
3. Semantically represented docs_before improves over semantic code-only: **yes** (Macro-F1 delta **+0.0016**).
4. Controlled-data deltas are reported in `recommendation.json`; they are retained only if natural-validation generalization improves.
5. Controlled examples recommended for final training: **no** under the predefined matched-family decision rule.
6. Best developer_setup F1: **0.0741**.
7. Best API false positives: **45**, versus **109** for TF-IDF V8.
8. Remaining evidence indicates a combination of representation limitations, natural-data scarcity, and controlled-to-natural domain shift.
9. Collect more natural positives only after model freeze review; prioritize categories with weak natural support and unstable F1.
10. If acquisition resumes, prioritize natural developer_setup across more repositories, followed by model_contract and configuration repositories unlike the controlled templates.

No confirmation evaluation, new acquisition, augmentation, or Stage 3 generation was performed.
