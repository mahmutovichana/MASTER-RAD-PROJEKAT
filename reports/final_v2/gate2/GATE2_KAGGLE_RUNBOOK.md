# Gate 2 free Kaggle execution runbook

Scientific preregistration: `e89cedfa87edbc1469d467713451a9441aa1360f`.

Pinned protocol-preserving execution commit: `648eee910653e95a5e1f71f5ccc50ef9b9a7a9e9`.

This is a replacement technical execution environment for the same frozen Gate 2 study. It does not define a new experiment. Gate 0 and Gate 1 remain frozen, the confirmation partition remains sealed, and the previous Colab incident remains part of the execution record.

## 1. Start a free Kaggle notebook

Create a Kaggle Notebook, enable **Internet** and select the free **GPU** accelerator. The GPU is required only while UniXcoder embeddings are incomplete. `/kaggle/working/docguard_gate2` is persistent for the current notebook session; export its portable checkpoint before the session ends.

In the first cell run:

```bash
!git clone https://github.com/mahmutovichana/MASTER-RAD-PROJEKAT.git /kaggle/working/docguard
%cd /kaggle/working/docguard
!git checkout 648eee910653e95a5e1f71f5ccc50ef9b9a7a9e9
!git lfs install
!git lfs pull --include="experiments/consolidated_enriched_training_v2/gold/*.jsonl"
!python -m pip install --only-binary=:all: "transformers==4.56.2" "tokenizers==0.22.0" "accelerate==1.10.1" "huggingface_hub==0.35.3" "safetensors==0.6.2" "scikit-learn>=1.7,<1.9" "scipy>=1.15,<1.17" threadpoolctl
```

Do not reinstall or downgrade Kaggle's CUDA-enabled PyTorch build.

Verify the runtime and frozen Gate 1 input:

```bash
!python - <<'PY'
import torch, transformers, tokenizers, accelerate, huggingface_hub
print("torch", torch.__version__)
print("CUDA available", torch.cuda.is_available())
print("CUDA device", torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
print("transformers", transformers.__version__)
print("tokenizers", tokenizers.__version__)
print("accelerate", accelerate.__version__)
print("huggingface_hub", huggingface_hub.__version__)
assert torch.cuda.is_available(), "Use a Kaggle GPU session until embeddings are COMPLETE"
PY
!python scripts/verify_final_v2_gold_freeze.py
```

`microsoft/unixcoder-base` is public, so `HF_TOKEN` is **not required**. Authentication can help only if Hugging Face applies anonymous download rate limits. If needed, add `HF_TOKEN` through Kaggle Secrets and load it into the process environment; never paste it into a cell, file, archive, or repository.

## 2. Fresh run

Start with no `/kaggle/working/docguard_gate2` directory, then invoke the unchanged canonical wrapper:

```bash
!rm -rf /kaggle/working/docguard_gate2
!python scripts/run_gate2_external_compute.py --config configs/final_v2/gate2_model_study.json --persistent-dir /kaggle/working/docguard_gate2 --return-archive /kaggle/working/gate2_kaggle_return.tar.gz
```

The wrapper verifies Gate 1, dependency versions, the development-only view, embedding identity, every completed fold, and the final return artifacts. It stops fail-closed on any mismatch. It does not access confirmation.

## 3. Export a portable checkpoint

When the wrapper is stopped or has returned to the notebook prompt, create a deterministic, hash-verified checkpoint archive:

```bash
!python scripts/manage_gate2_checkpoint.py export --config configs/final_v2/gate2_model_study.json --persistent-dir /kaggle/working/docguard_gate2 --archive /kaggle/working/gate2_checkpoint.tar.gz
```

Download `/kaggle/working/gate2_checkpoint.tar.gz`, or save it as a private Kaggle output/dataset for the next session. It contains only embedding checkpoint memmaps/metadata, completed fold checkpoints, the run registry, and minimal workflow manifests. It excludes Hugging Face cache, model weights, confirmation data/results, and secrets.

Do not export while the extraction or model process is actively writing a checkpoint.

## 4. Resume in a later Kaggle session

Repeat section 1 and attach the previous checkpoint archive as a private Kaggle input. Restore it into an empty persistent directory; replace `<checkpoint-dataset>` with the attached input name:

```bash
!python scripts/manage_gate2_checkpoint.py restore --config configs/final_v2/gate2_model_study.json --persistent-dir /kaggle/working/docguard_gate2 --archive /kaggle/input/<checkpoint-dataset>/gate2_checkpoint.tar.gz
!python scripts/run_gate2_external_compute.py --config configs/final_v2/gate2_model_study.json --persistent-dir /kaggle/working/docguard_gate2 --return-archive /kaggle/working/gate2_kaggle_return.tar.gz
```

Restore rejects a corrupt archive, an unexpected file, or any mismatch in gold SHA, development-view SHA, row order, scientific config, UniXcoder/tokenizer revision, pooling, length, dtype, fold assignment, task, family, or fold.

If the portable embedding checkpoint is `COMPLETE`, the extraction script reconstructs and verifies the final embedding artifact directly from the memmaps without loading UniXcoder and without CUDA. M1/M2/M3 may then continue on a CPU/high-RAM Kaggle session. If embeddings are incomplete, CUDA remains mandatory.

## 5. Final verified return

Only a fully successful canonical wrapper creates:

`/kaggle/working/gate2_kaggle_return.tar.gz`

Download that archive after the wrapper reports `COMPLETE`. It contains the verified M1/M2/M3 study results and embedding manifest, but not the large embeddings, transient memmaps, model cache, weights, tokens, or confirmation data.

## Protocol-preserving operational optimizations

- UniXcoder embeddings remain preregistered `float32` and checkpointed as memmaps.
- A COMPLETE portable memmap checkpoint can be finalized on CPU; incomplete extraction still requires GPU.
- The semantic relation representation is generated in bounded chunks into a verified `float32` mmap rather than retained as an additional dense RAM copy.
- M3 fits its unchanged TF-IDF block once per inner fold and materializes only one preregistered semantic scale at a time.
- Temporary matrices and fitted models are released between scales/folds, with explicit garbage collection.
- The external wrapper caps BLAS/OpenMP pools at two threads to limit peak contention/memory; this does not change models, grids, folds, seeds, thresholds, or metrics.
- Families and folds remain sequential and resumable; no confirmation artifact is loaded or packaged.
