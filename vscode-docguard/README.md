# DocGuard VS Code Extension MVP

DocGuard analyzes current git changes, asks the Python runtime whether documentation should be updated, and previews a minimal documentation patch.

## Run Locally

```bash
npm install
npm run compile
```

Open this folder in VS Code and press `F5` to launch an Extension Development Host.

## Commands

- `DocGuard: Analyze Workspace Changes`
- `DocGuard: Analyze Current File`
- `DocGuard: Open Panel`
- `DocGuard: Apply Suggested Documentation Patch`

## Runtime

The extension calls:

```bash
python -m docguard_runtime.runtime_cli analyze-workspace --workspace <path> --format json
```

Train the recommended classifier before demoing the full HF path:

```bash
python -m docguard_hf_classifier.cli train-embeddings --version v0_4 --model sentence-transformers/all-MiniLM-L6-v2 --input-mode raw_diff_plus_docs --classifier-architecture staged
```

If the model is missing, the Python runtime falls back to the deterministic hybrid router.
