# Reproducibility And Git Hygiene Audit 2026-08

## Summary

Git hygiene is mostly sound. Raw external datasets and large normalized/model artifacts are ignored. README commands are sufficient to regenerate Deep-JIT normalized files and the external TF-IDF model if raw data is present locally. The main reproducibility caveat is that raw Google Drive / external dataset downloads are not automatically fetched, so the thesis should document manual acquisition.

## Git Ignore Check

`.gitignore` includes:

- `data/external/raw/`
- `data/external/deep_jit_binary/`
- `models/external_deep_jit/`

This is appropriate. The normalized Deep-JIT train JSONL is over 100 MB locally and should not be committed. The external TF-IDF model artifact should also remain ignored.

## Large File Check

Large local artifacts include:

- `data/external/raw/deep_jit_inconsistency/...`
- `data/external/deep_jit_binary/train.jsonl`
- `models/external_deep_jit/binary_tfidf_logreg.joblib`

These are either raw external data or generated artifacts and should not be committed to GitHub.

## Commands Documented

README includes commands for:

- Inspecting DocChecker / Deep-JIT local data.
- Preparing and evaluating the 500-record Deep-JIT proxy sample.
- Running Deep-JIT split audit.
- Exporting normalized Deep-JIT binary JSONL.
- Training the external Deep-JIT classifier.

Validation commands are also present across reports. The most important reproducibility commands are:

```bash
python -m compileall -q docguard_external
python -m docguard_external.cli deep-jit-split-audit --data-dir data/external/raw/deep_jit_inconsistency
python -m docguard_external.cli export-deep-jit-binary --data-dir data/external/raw/deep_jit_inconsistency --output-dir data/external/deep_jit_binary
python -m docguard_external.cli train-binary --train data/external/deep_jit_binary/train.jsonl --validation data/external/deep_jit_binary/validation.jsonl --test data/external/deep_jit_binary/test.jsonl --model-output models/external_deep_jit/binary_tfidf_logreg.joblib --report reports/external_deep_jit_binary_classifier_evaluation_2026_08.md
```

## Current Git Status Observation

Before this audit, `git status --short` showed only `m examples/vscode_demo` as an unrelated local change in the working tree visible at that moment. This audit does not modify or rely on the VS Code demo.

## Recommendations

1. Do not commit raw external datasets.
2. Do not commit `data/external/deep_jit_binary/` unless split files are deliberately downsampled and documented.
3. Do not commit `models/external_deep_jit/` unless model artifacts are moved to a release/artifact store.
4. Commit small reports and code only.
5. Include manual data-acquisition instructions in the thesis appendix or reproducibility section.
