# Project Recovery Audit 2026-08

Thesis title: "Inteligentni NLP agent za analizu konzistentnosti softverskih projekata"

## 1. Current Repository Status

- Repository path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT`
- Remote: `https://github.com/mahmutovichana/MASTER-RAD-PROJEKAT.git`
- Current branch: `main`
- Branch relation: `main...origin/main`
- Latest commit: `0b3e24c v0.4, confusion matrix`
- Recent commits include v0.4 dataset, raw-diff no-leak HF evaluation, HF classifier, granular hybrid signals, and v0.3 LLM experiments.
- Current working tree is not clean. Local-only/uncommitted items include `.gitignore`, `README.md`, `docguard_runtime/`, `examples/`, `tests/`, `vscode-docguard/`, and `reports/vscode_extension_mvp_v0_5.md`.
- A tracked or modified cache artifact appears: `docguard/__pycache__/evaluator.cpython-314.pyc`.
- A model artifact is modified: `models/hf_v0_4/raw_diff_plus_docs/embedding_classifier_staged.joblib`.

## 2. Components That Exist

- `docguard/`: original/rule-based baseline components.
- `docguard_ml/`: CPU-friendly ML/fallback classifier path.
- `docguard_hf_classifier/`: HF embedding classifier experiments, input modes, ablations, staged/flat classifier support.
- `docguard_hybrid/`: deterministic signal extraction, routing, hybrid validator/evaluator.
- `docguard_llm/`: mock and real local HF generative LLM experiment path.
- `docguard_runtime/`: local Python runtime bridge for practical tooling.
- `vscode-docguard/`: VS Code extension MVP files, plus local `node_modules/` and `out/` generated artifacts.
- `examples/vscode_demo/`: small VS Code/demo workspace.
- `scripts/`: dataset generation, validation, figures, ablation, manual audit helpers.
- `data/`: active v0.4 JSONL dataset, split files, HF exports/predictions, LLM prediction files.
- `dataset_versions/`: frozen earlier dataset versions.
- `models/`: fallback model and HF embedding classifier models.
- `reports/`: extensive dataset, ML, HF, hybrid, LLM, visual, and VS Code MVP reports.

## 3. Missing or Incomplete Components

- External real-world dataset integration is not implemented yet.
- `docguard_external/` did not exist before this recovery task; it is now scaffolded but does not download/convert real datasets yet.
- VS Code extension is an MVP, not a polished thesis artifact; it should not be debugged further until methodology/data direction is settled.
- Real-world validation reports are missing.
- Strong negative labels from external real-world data are not yet available.
- Fine-tuned transformer sequence classifier remains optional/future.

## 4. Reliable Results

- The v0.4 synthetic dataset structure appears well documented and validated.
- v0.4 has 6000 records, 30 generated projects, 3000 positive and 3000 negative examples, with train/validation/test around 4200/1000/800.
- The dataset split leakage check reports no project overlap and no near-duplicate input/diff hashes for `raw_diff_plus_docs`.
- HF `raw_diff_plus_docs` synthetic results are useful as a clean controlled benchmark result.
- Stress testing shows binary detection remained strong while fine-grained prediction degraded.

## 5. Questionable Results

- Very high or perfect synthetic results are not final evidence of real-world generalization.
- `full_current` is explicitly an upper-bound assisted setting because summaries/signals can leak label semantics.
- Synthetic scenario names and code patterns may make classification easier than real project changes.
- Negative subtype accuracy is diagnostic and weaker than binary no-update detection.
- VS Code extension behavior has not been validated as a polished user study or production-ready tool.

## 6. Artifacts to Preserve

- v0.4 synthetic dataset and generated projects.
- v0.3 frozen artifacts and historical LLM reports.
- HF embedding input ablation reports and prediction files.
- Negative subtype and stress-test reports.
- Runtime/VS Code MVP as practical demonstration work.
- Model artifacts, but only with intentional versioning decisions.

## 7. Artifacts Not Yet Suitable as Final Thesis Evidence

- Synthetic-only perfect accuracy claims.
- `full_current` upper-bound results as if they were fair no-leak results.
- Mock LLM reports as model-quality evidence.
- VS Code extension MVP as scientific validation.
- Any external dataset conclusion before a real adapter pilot is complete.

## 8. Local-Only vs Likely Pushed

- Pushed to GitHub up to `0b3e24c` on `origin/main`.
- Local-only/uncommitted: v0.5 runtime/extension files, examples, tests, README edits, `.gitignore`, and VS Code MVP report.
- Local generated folders include `node_modules/`, `out/`, `.pnpm-store/`, and `__pycache__/`; these should remain untracked.

## 9. Immediate Cleanup Recommendations

- Remove tracked `.pyc`/`__pycache__` artifacts from git index if tracked.
- Keep `node_modules/`, `.pnpm-store/`, `out/`, `.vscode-test/`, `coverage/`, and `.DS_Store` ignored.
- Review model `.joblib` files before committing; decide whether they are thesis artifacts or reproducible outputs.
- Avoid committing large external datasets directly.
- Commit recovery reports and external adapter scaffolding separately from extension/debug changes.

## 10. Next Recommended Development Path

Do not restart from scratch. Continue from DocGuard as a controlled synthetic prototype and developer workflow demo, but add external real-world validation before making thesis-level claims. The next implementation step should be a 100-500 record CoDocBench pilot mapped into the normalized external schema, followed by separate synthetic-vs-real evaluation.

