# DocGuard Live Flow Existing Runtime Audit 2026-08

## Recommendation

Use `docguard_hybrid.predict()` for the live playground.

## Component Findings

| Component | Usefulness for live playground | Input shape | Limitations |
| --- | --- | --- | --- |
| `docguard/cli.py` + `docguard/evaluator.py` | Too narrow | Synthetic dataset records with legacy REST API fields | Mainly supports older REST scenarios such as new endpoint, validation min, auth, response field, and internal refactor. It does not cover the full documentation-class taxonomy. |
| `docguard_hybrid/hybrid_agent.py` | Best fit | Dict records with `id`, `project_id`, `changed_files`, `code_diff`, gold fields for evaluation, docs context, and expected facts | Supports broad routing classes through deterministic signals, but patch generation is generic and signal extraction still contains synthetic-evaluation shortcuts. |
| `docguard_hybrid/doc_router.py` | Broadest class routing | Uses signals from `signal_extractor` | Covers API reference, model contract, configuration, testing, workflow, architecture, developer setup, changelog, and no-update categories. |
| `docguard_hybrid/signal_extractor.py` | Main signal source | Reads `changed_files`, `code_diff`, and currently `scenario_type` | Good for controlled synthetic live demos. Not yet a clean real-world runner because reading `scenario_type` can leak gold labels in synthetic records. |
| `docguard_runtime/` | Useful developer-workflow foundation | Workspace/runtime structures | Better for VS Code/runtime integration than this class-coverage live flow; not currently the broadest category evaluator. |

## Conclusion

The live playground should use `docguard_hybrid.predict()` because it supports the broadest documentation classes. The older `docguard` path is narrower and mostly legacy REST API logic. The live flow must be reported as an invented synthetic sanity/demo layer, not as a benchmark or real-world metric.
