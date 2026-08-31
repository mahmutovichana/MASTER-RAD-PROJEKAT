# Phase 7 recommendation

## Direct answers

1. Semantic better than TF-IDF V8: **yes**.
2. Two-channel lexical better than concatenated TF-IDF V8: **yes**.
3. Semantically represented docs_before improves over semantic code-only in a matched natural-only OVR comparison: **yes** (Macro-F1 delta **+0.0203**).
4. Controlled-data deltas are reported in `recommendation.json`; they are retained only if natural-validation generalization improves.
5. Controlled examples recommended for final training: **no** under the predefined matched-family decision rule. Recommended natural-only model: `hybrid__natural_only__multinomial_logreg` (Macro-F1 **0.4485**, balanced accuracy **0.4709**). The augmented candidate remains an experimental upper bound, not the final recommendation.
6. Best developer_setup F1: **0.0741**.
7. Best API false positives: **45**, versus **109** for TF-IDF V8.
8. Remaining evidence indicates a combination of representation limitations, natural-data scarcity, and controlled-to-natural domain shift.
9. Collect more natural positives only after model freeze review; prioritize categories with weak natural support and unstable F1.
10. If acquisition resumes, prioritize natural developer_setup across more repositories, followed by model_contract and configuration repositories unlike the controlled templates.

No confirmation evaluation, new acquisition, augmentation, or Stage 3 generation was performed.

The best augmented candidate (`hybrid__natural_plus_controlled__ovr_logreg`) reaches Macro-F1 **0.4542**, but its matched controlled-vs-natural delta is only **+0.0065** Macro-F1, **−0.0084** balanced accuracy, with paired-bootstrap Macro-F1 95% CI **[−0.0344, +0.0576]**. This does not justify retaining controlled examples.
