# DocGuard VS Code Extension MVP

DocGuard analyzes current git changes, asks the Python runtime whether documentation should be updated, and previews a minimal documentation patch.

## Run Locally

```bash
npm install
npm run compile
```

Open this folder in VS Code and press `F5` with `Run DocGuard Extension Demo`. The Extension Development Host opens `examples/vscode_demo` automatically.

For the fastest visual demo, prepare a reproducible workspace change first:

```bash
cd ..
python scripts/prepare_vscode_demo.py --scenario config-env
```

Then, in the Extension Development Host, open `examples/vscode_demo` and run `DocGuard: Analyze Workspace Changes`.

Expected result:

- DocGuard detects an added environment variable in `src/config.ts`.
- The panel targets `docs/configuration.md`.
- The patch preview proposes documenting `REVIEW_WINDOW`.
- After `Apply Patch`, running analysis again reports that no documentation update is required.

For the real LLM patch path, run:

- `DocGuard: Analyze Workspace Changes with LLM Patch`

This uses the same live workspace diff and docs-before text, but asks the configured LLM backend to draft the patch. The panel shows generation status, verifier status, quality label, hallucination risk, and warnings. If the LLM patch is rejected, DocGuard keeps it visible and offers a safe grounded fallback patch instead.

Recommended stronger backend options:

OpenAI-compatible endpoint, including vLLM, LM Studio server, or a hosted chat-completions-compatible model:

```powershell
$env:DOCGUARD_LLM_BASE_URL="http://localhost:8000/v1"
$env:DOCGUARD_LLM_API_KEY="local-or-provider-key"
```

Then set VS Code settings:

```json
{
  "docguard.analysisBackend": "llm-openai-compatible",
  "docguard.analysisModel": "Qwen/Qwen2.5-Coder-32B-Instruct",
  "docguard.patchBackend": "llm-openai-compatible",
  "docguard.patchModel": "Qwen/Qwen2.5-Coder-32B-Instruct",
  "docguard.llmBaseUrl": "https://router.huggingface.co/v1",
  "docguard.patchMaxNewTokens": 384,
  "docguard.patchTemperature": 0.1
}
```

For Hugging Face Router, set the endpoint and token in the same PowerShell session used to launch VS Code:

```powershell
$env:DOCGUARD_LLM_BASE_URL="https://router.huggingface.co/v1"
$env:DOCGUARD_LLM_API_KEY="<hugging-face-token>"
```

Before the visual demo, compare the currently available remote models from the repository root:

```powershell
python scripts/check_hf_router_models.py
python scripts/compare_live_llm_patch_models.py --models "Qwen/Qwen2.5-Coder-32B-Instruct" "Qwen/Qwen2.5-Coder-7B-Instruct" "meta-llama/Llama-3.1-8B-Instruct" --max-new-tokens 384 --temperature 0.1
```

Open `reports/live_flow/vscode_llm_patch_model_comparison_2026_08.md`, choose the model with a passing verifier and usable or excellent quality label, then put that model in both `docguard.analysisModel` and `docguard.patchModel` for the full LLM demo.

Ollama local server:

```powershell
$env:DOCGUARD_OLLAMA_BASE_URL="http://localhost:11434"
```

Then set:

```json
{
  "docguard.patchBackend": "llm-ollama",
  "docguard.patchModel": "qwen2.5-coder:7b-instruct-q4_K_M"
}
```

Other prepared scenarios:

```bash
python scripts/prepare_vscode_demo.py --scenario new-endpoint
python scripts/prepare_vscode_demo.py --scenario no-update
python scripts/prepare_vscode_demo.py --scenario clean
```

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

The VS Code demo defaults to the fast `hybrid_router` architecture. Train the recommended classifier only before demoing the optional HF path:

```bash
python -m docguard_hf_classifier.cli train-embeddings --version v0_4 --model sentence-transformers/all-MiniLM-L6-v2 --input-mode raw_diff_plus_docs --classifier-architecture staged
```

If the model is missing or `docguard.classifierArchitecture` is set to `hybrid_router`, the Python runtime uses the deterministic hybrid router for detection/routing.

Local CPU note: `Qwen/Qwen2.5-Coder-0.5B-Instruct` can run on CPU but may produce rejected patches; `Qwen/Qwen2.5-Coder-1.5B-Instruct` was too slow locally for smooth VS Code use. Use a stronger GPU, quantized, or remote backend for high-quality LLM patch drafting.
