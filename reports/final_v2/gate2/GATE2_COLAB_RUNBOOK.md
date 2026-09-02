# Gate 2 fail-closed and resumable Colab runbook

Scientific preregistration: `e89cedfa87edbc1469d467713451a9441aa1360f`. This runbook executes the unchanged M1/M2/M3 study. Google Drive is persistent compute storage only.

## 1. Start the pinned repository environment

Use a Colab Pro **GPU + high-RAM** runtime for the first or incomplete embedding extraction. Run:

```bash
!git clone https://github.com/mahmutovichana/MASTER-RAD-PROJEKAT.git /content/docguard
%cd /content/docguard
!git checkout 4cbbacb05bad52466dc5c02be4fd08727b45ca0b
!git lfs install
!git lfs pull --include="experiments/consolidated_enriched_training_v2/gold/*.jsonl"
!python -m pip install --only-binary=:all: "transformers==4.56.2" "tokenizers==0.22.0" "accelerate==1.10.1" "huggingface_hub==0.35.3" "safetensors==0.6.2" "scikit-learn>=1.7,<1.9" "scipy>=1.15,<1.17"
```

Do not reinstall or downgrade Colab's CUDA-enabled Torch build.

## 2. Mount persistent storage and load the token from Colab Secrets

Create a Colab Secret named `HF_TOKEN`, then run:

```python
import os
from google.colab import drive, userdata

drive.mount("/content/drive")
os.environ["HF_TOKEN"] = userdata.get("HF_TOKEN")
assert os.environ["HF_TOKEN"]
```

Never paste the token into a committed cell or file.

## 3. Run exactly one canonical command

```bash
!python scripts/run_gate2_external_compute.py --config configs/final_v2/gate2_model_study.json --persistent-dir /content/drive/MyDrive/docguard_gate2
```

This one command is fail-closed. It stops immediately if Gate 1, environment, development identity, embedding identity, model study, or return verification fails. It records technical failure status on Drive.

The persistent convention is `/content/drive/MyDrive/docguard_gate2/`. It contains embedding memmaps/checkpoints, completed fold checkpoints, the append-only run registry, verified results, and finally `gate2_colab_return.tar.gz`.

If Colab interrupts, start another runtime and repeat these same three sections. The wrapper verifies every identity, reuses a COMPLETE embedding artifact, restores completed folds, and computes only missing work. Do not delete the Drive folder and do not use `--force-rerun` unless a separately documented implementation defect requires it.

If GPU is unavailable before embeddings are COMPLETE, **stop and wait for GPU availability**. If Drive already contains a COMPLETE, hash-verified embedding artifact, the wrapper permits the remaining M1/M2/M3 resume on a high-RAM CPU runtime. It never regenerates a valid completed embedding unnecessarily.

After COMPLETE, download only:

`/content/drive/MyDrive/docguard_gate2/gate2_colab_return.tar.gz`

The archive contains verified study results and the embedding manifest, but excludes memmaps, the large embedding NPZ, Hugging Face cache, model weights, and tokens.
