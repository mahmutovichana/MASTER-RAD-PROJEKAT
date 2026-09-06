# Gate 4 Kaggle execution runbook

Gate 4 is development-only. Confirmation remains sealed.

The Kaggle environment MUST NOT fetch, mount, upload, read, or reference the
confirmation split or any full-gold artifact containing confirmation rows.
Only the already-frozen Gate 4 primary and secondary development samples are
needed for external Qwen execution.

## Kaggle requirements

- Accelerator: 2x Tesla T4 (already preflighted).
- Precision: FP16; no quantization.
- Model: Qwen/Qwen2.5-Coder-7B-Instruct.
- Internet enabled for the initial Hugging Face model download, or attach a
  read-only cached model dataset.
- A Hugging Face token is optional for this public model and must be supplied
  through Kaggle Secrets if used, never committed.

## Safe repository checkout

Before cloning, disable automatic Git LFS smudging so sealed LFS artifacts are
not downloaded:

```bash
export GIT_LFS_SKIP_SMUDGE=1

git clone https://github.com/mahmutovichana/MASTER-RAD-PROJEKAT.git
cd MASTER-RAD-PROJEKAT

git checkout <GATE4_PREPARATION_COMMIT>

git lfs install --local
git lfs pull --include="reports/final_v2/gate4/primary_sample.jsonl,reports/final_v2/gate4/secondary_stress_sample.jsonl"
```

Do NOT run an unrestricted `git lfs pull`.

In particular, do not fetch:

- `experiments/consolidated_enriched_training_v2/gold/confirmation.jsonl`
- `experiments/consolidated_enriched_training_v2/gold/final_human_gold.jsonl`
- any other confirmation/reference artifact.

The external runner needs only the two frozen development samples, the regular
Git-tracked Stage 3 configuration, and the hashed source files.

## Runtime dependencies

Use the versions validated during the Stage 3 GPU preflight:

```bash
python -m pip install -q \
  "transformers==4.56.2" \
  "tokenizers==0.22.0" \
  "accelerate==1.10.1" \
  "huggingface_hub==0.35.3" \
  "safetensors==0.6.2" \
  sentencepiece
```

## External-input validation

The full local Gate 4 preparation verifier has already passed before this
commit. Do not download sealed datasets merely to repeat that verifier on
Kaggle.

Validate only the external-compute contract:

```bash
python - <<'PY'
from pathlib import Path
from scripts.run_gate4_external_qwen import validate_external_inputs

root = Path(".").resolve()
manifest = root / "reports/final_v2/gate4/external_run_input_manifest.json"

parsed, rows, config = validate_external_inputs(root, manifest)

assert parsed["confirmation_accessed"] is False
assert parsed["confirmation_paths_allowed"] is False
assert len(rows) == 200

print("GATE4_EXTERNAL_INPUT_VALIDATION=PASS")
print("rows=", len(rows))
print("model=", config["analysis_model"])
PY
```

## Real Qwen development execution

```bash
python scripts/run_gate4_external_qwen.py \
  --input-manifest reports/final_v2/gate4/external_run_input_manifest.json \
  --output-dir reports/final_v2/gate4/external_return
```

The runner validates source hashes, sample hashes, the frozen Stage 3 config,
and the development-only partition contract before loading Qwen.

Rows without canonical retrieval context are emitted as
`retrieval_context_unavailable` with zero LLM calls and no generated patch.

## Resume behavior

If execution is interrupted, rerun the exact same command without deleting the
output directory.

Completed `sample_name::case_id` keys are skipped. Request-specific deterministic
seeds prevent resume position from changing the sampling seed for later LLM
calls. The final result JSONL is rewritten in canonical sample order without
duplicate run keys.

## Return files

Download these three files from
`reports/final_v2/gate4/external_return/`:

1. `gate4_external_return.zip`
2. `gate4_external_return.sha256`
3. `development_generation_checkpoint.jsonl`

The ZIP is the canonical external return package. The checkpoint is retained as
recovery evidence.

Do not run Stage 3 confirmation generation and do not create a Stage 3 freeze
manifest on Kaggle. Returned development-only evidence must first be verified
locally.
