# HF Fine-Tuning Plan v0.4

This plan is optional and future-facing. It should not be part of the default CPU safety checks because sequence fine-tuning may be slow on a CPU-only machine.

## DistilRoBERTa

```bash
python -m docguard_hf_classifier.cli train-sequence --version v0_4 --task docs_update_required --base-model distilroberta-base --epochs 1 --limit-train 1000 --limit-eval 200
python -m docguard_hf_classifier.cli train-sequence --version v0_4 --task doc_category --base-model distilroberta-base --epochs 1 --limit-train 1000 --limit-eval 200
python -m docguard_hf_classifier.cli train-sequence --version v0_4 --task scenario_type --base-model distilroberta-base --epochs 1 --limit-train 1000 --limit-eval 200
```

## CodeBERT

```bash
python -m docguard_hf_classifier.cli train-sequence --version v0_4 --task docs_update_required --base-model microsoft/codebert-base --epochs 1 --limit-train 1000 --limit-eval 200
python -m docguard_hf_classifier.cli train-sequence --version v0_4 --task doc_category --base-model microsoft/codebert-base --epochs 1 --limit-train 1000 --limit-eval 200
python -m docguard_hf_classifier.cli train-sequence --version v0_4 --task scenario_type --base-model microsoft/codebert-base --epochs 1 --limit-train 1000 --limit-eval 200
```

These runs are thesis-relevant because they compare frozen embeddings against task-specific supervised transformer fine-tuning. They are best run on GPU, Colab/Kaggle, or a machine with enough CPU time.
