# Gate 2 UniXcoder Colab runbook

Local CUDA is unavailable. Colab Pro is used only as compute infrastructure; repository scripts remain canonical.

## Exact one Colab action

Open one GPU runtime, add `HF_TOKEN` through Colab **Secrets** (never paste it into a notebook cell), then run the committed Gate 2 wrapper cells/commands below at the recorded preregistration commit.

```bash
!git clone https://github.com/mahmutovichana/MASTER-RAD-PROJEKAT.git /content/docguard
%cd /content/docguard
!git checkout PREREGISTRATION_COMMIT_SHA
!git lfs pull --include="experiments/consolidated_enriched_training_v2/gold/*.jsonl"
!python -m pip install --only-binary=:all: "transformers==4.56.2" "tokenizers==0.22.0" "accelerate==1.10.1" "huggingface_hub==0.35.3" "safetensors==0.6.2" "scikit-learn>=1.7,<1.9" "scipy>=1.15,<1.17"
```

```python
import os, platform, torch, transformers, tokenizers, accelerate, huggingface_hub
from google.colab import userdata
os.environ["HF_TOKEN"] = userdata.get("HF_TOKEN")
print("Python", platform.python_version())
print("torch", torch.__version__)
print("CUDA availability", torch.cuda.is_available())
print("CUDA device", torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
print("transformers", transformers.__version__)
print("tokenizers", tokenizers.__version__)
print("accelerate", accelerate.__version__)
print("huggingface_hub", huggingface_hub.__version__)
assert torch.cuda.is_available()
```

```bash
!python scripts/verify_final_v2_gold_freeze.py
!python scripts/extract_gate2_unixcoder_embeddings.py --config configs/final_v2/gate2_model_study.json --output-dir /content/gate2_embeddings
!python scripts/run_gate2_model_study.py --config configs/final_v2/gate2_model_study.json --embedding-dir /content/gate2_embeddings --output-dir /content/gate2_results --families M2 M3
!python scripts/verify_gate2_return_artifacts.py --config configs/final_v2/gate2_model_study.json --embedding-dir /content/gate2_embeddings --result-dir /content/gate2_results
!tar -czf /content/gate2_colab_return.tar.gz -C /content gate2_embeddings gate2_results
```

Download only `/content/gate2_colab_return.tar.gz` and place it locally for verification and final aggregation. Do not return model weights or Hugging Face cache directories. The scripts must report the resolved revision `5604afdc964f6c53782a6813140ade5216b99006`, 22,166 aligned row IDs, zero confirmation rows, and artifact hashes.
