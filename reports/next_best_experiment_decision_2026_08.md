# Next Best Experiment Decision 2026-08

## Decision

Run the stronger classical v2 baseline first. It is CPU-friendly, methodologically clean, and directly targets the weak combined-validation Deep-JIT result.

This step has now been executed. The best v2 model is `logreg_balanced` with `word_char_tfidf_plus_manual_features` and `old_comment_plus_code_diff`. It reaches 75.60% accuracy, 78.84% precision, 69.99% recall, 74.15% F1, 18.79% FPR, 81.21% specificity, and MCC 0.5153 on the untouched Deep-JIT combined-validation test split.

## Frozen Code Encoder

Run the frozen pretrained code-encoder baseline second if GPU/Colab time is available. Local dependencies exist, but CUDA is unavailable, so a full encoder sweep is deferred rather than faked.

## Colab Fine-Tuning

Use Colab only after the classical v2 and frozen encoder results are known. Full fine-tuning is useful if the target result remains unmet, but it adds overfitting, truncation, runtime, and reproducibility risk.

## Minimum Target Before Thesis Writing

Proceed to thesis writing when the evidence package contains:

- Deep-JIT external proxy around >=70% accuracy or >=0.40 MCC, or a clear explanation of why the proxy remains hard. The v2 classical run meets this target.
- FPR below roughly 25-30%. The v2 classical run meets this target with 18.79% FPR.
- Stronger specificity than zero-shot DocGuard.
- Project-level case study evidence for the actual DocGuard agent workflow.

## Best Path

1. Implement and run `train-binary-v2` on the combined-validation split.
2. If it misses the target, run frozen UniXcoder/CodeBERT embeddings.
3. If still below target and time permits, move transformer fine-tuning to Colab.
4. In parallel, prepare the small project-level human-audited DocGuard case study.
