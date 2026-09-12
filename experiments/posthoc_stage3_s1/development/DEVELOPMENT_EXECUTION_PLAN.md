# Frozen S1 development execution plan

The GPU run uses only the 200 ordered Gate 4 development memberships. It first evaluates the four permitted lexical/dense top-k combinations and selects by controlled-only target Hit@3, MRR, Hit@1, then lower lexical and dense k. Target suitability is generated once at the minimum confidence threshold; 0.50 and 0.65 outcomes are derived without extra inference. P1 and P2 are both recorded.

Self-critic judgments are safety gates, not human ground truth. If deterministic target/safety/coverage diagnostics cannot resolve P1 versus P2, the run stops at selection pending. A blind development sample must then be frozen, and authorization requested before any manual-review workbook is generated.

Required outputs are reconstruction/candidate coverage, controlled-only target metrics, generation invocation and accept/abstain/error rates, unsupported-fact and target-not-retrieved rates, and first-pass/repaired acceptance. Primary and secondary memberships remain identified in case-level outputs. Confirmation and Gate 6 reviewer data are inaccessible to the runner.
