# External Confidence Calibration Notes 2026-08

High positive recall with low confidence should not be overclaimed. It shows that the existing predictor is sensitive to many real CoDocBench code-doc co-changes, but the score distribution suggests uncertainty under external data.

The most likely explanation is a combination of synthetic-to-real domain shift and probability calibration. The HF embedding classifier was trained on synthetic DocGuard v0.4 examples, while CoDocBench contains Python docstring/comment maintenance from many real projects. The classifier can often choose the positive class, but its downstream category, scenario, and target-file classifiers are operating outside their original project-level Markdown label space.

LogisticRegression probabilities over sentence embeddings are not guaranteed to be calibrated under distribution shift. The current confidence is also a joint/minimum confidence across staged decisions, so one uncertain downstream label can make an otherwise correct positive decision look low-confidence.

Low confidence matters for VS Code usage because a developer-facing assistant should distinguish confident update-required warnings from review-needed suggestions. A low-confidence positive may be useful, but it should not feel like a definitive instruction.

## Recommended Future Work

1. Calibrate confidence on validation data.
2. Use external real-data fine-tuning after labels stabilize.
3. Report recall at multiple confidence thresholds.
4. Add an abstain or review-needed state for low-confidence predictions.
5. Use external negatives before reporting precision or F1.
