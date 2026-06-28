# HF Leakage Risk Analysis v0.4

`full_current` is useful as an assisted upper-bound setting, but it can inflate performance because it combines raw diffs with derived summaries and rule-derived signal names.

Change summaries and change-intent summaries can leak label semantics because generated phrases often name the scenario or documentation category directly. Extracted signals are useful engineering features, but they are partially produced by deterministic rules, so they should not be treated as a purely learned no-leak representation.

Recommended thesis reporting:

- Primary fair HF result: `raw_diff_plus_docs`
- Assisted HF result: `raw_diff_plus_signals`
- Upper-bound assisted result: `full_current`

`raw_diff_only` is the strictest setting. `raw_diff_plus_docs` is the recommended default because the model sees the code change and the existing documentation context without gold-like summaries or handcrafted scenario signals.
