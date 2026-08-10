# External Negative Sampling Strategy 2026-08

CoDocBench currently gives DocGuard a strong external positive signal: real code and docstring/comment co-changes mined from maintenance history. It should not be treated as a complete binary benchmark by itself.

Do not infer negatives from arbitrary code-only commits. A code-only commit may still require documentation, may be undocumented technical debt, or may have documentation updated elsewhere.

## Safe Negative Options

1. Use existing synthetic negatives only for controlled comparison, while clearly reporting that they are synthetic.
2. Use external datasets that provide explicit consistency/inconsistency or update/no-update labels.
3. Mine weak negatives only from conservative categories such as formatting-only, test-only, or internal refactor changes, then manually audit the sampling rules.
4. Use code-comment consistency datasets if they provide negative or inconsistent labels.

## Reporting Policy

Strong labels and weak labels must be reported separately. Any future external F1 score requires a defensible negative set with documented provenance and audit results.
