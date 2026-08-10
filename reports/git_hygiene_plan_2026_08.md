# Git Hygiene Plan 2026-08

## Current Observations

- Working tree is not clean.
- Local-only folders include `docguard_runtime/`, `examples/`, `tests/`, and `vscode-docguard/`.
- `vscode-docguard/node_modules/`, `vscode-docguard/out/`, and `.pnpm-store/` exist locally and should not be tracked.
- A `.pyc` file appears modified under `docguard/__pycache__/`.
- A staged HF model artifact appears modified: `models/hf_v0_4/raw_diff_plus_docs/embedding_classifier_staged.joblib`.

## Recommendations

- Do not track `__pycache__/` or `.pyc`.
- Do not track `node_modules/`.
- Do not track `.pnpm-store/`.
- Do not track `.vscode-test/`, `coverage/`, or `.DS_Store`.
- Decide explicitly whether `vscode-docguard/out/` should be committed. Default recommendation: do not commit generated extension output.
- Review `.joblib` models before committing. They may be useful reproducibility artifacts, but they are generated binaries.
- Version dataset snapshots intentionally. Do not blindly commit large external datasets.
- Keep `data/external/` samples small or document how to reproduce them.

## `.gitignore` Update

The following ignore patterns were added or confirmed:

```text
**/__pycache__/
*.pyc
node_modules/
.pnpm-store/
.vscode-test/
coverage/
.DS_Store
out/
```

