# DocGuard Project Evolution Improvement 2026-08

This report documents a focused improvement to the synthetic project-evolution live demo. It does not modify labels, generated cases, expected facts, or docs-after text.

## Change

`docguard_hybrid/doc_router.py` now gives `docs_already_updated` precedence over positive documentation-update signals. This handles cases where the code diff contains a visible API-like change, but the current documentation excerpt already describes that change.

The rule is general and evidence-based:

- It uses the runtime `docs_before` excerpt.
- It does not use project names, case ids, gold labels, expected facts, expected patch summaries, or docs-after text.
- It prevents unnecessary patches when current documentation already appears consistent with the visible code change.

## Before

The previous project-evolution run had one hard false positive:

- Total cases: 24
- Binary accuracy: 95.83%
- Precision: 94.44%
- Recall: 100.00%
- F1: 97.14%
- Category accuracy: 95.83%
- Target file accuracy: 95.83%
- Scenario accuracy: 95.83%
- False positives: 1
- False negatives: 0

The failure was `ATLAS-REVIEW-API-PR-08`, where `route_added` and `docs_already_updated` were both detected, but the positive route signal won.

## After

After the router precedence fix and regenerated evaluation:

- Total cases: 24
- Binary accuracy: 100.00%
- Precision: 100.00%
- Recall: 100.00%
- F1: 100.00%
- Category accuracy: 100.00%
- Target file accuracy: 100.00%
- Scenario accuracy: 100.00%
- False positives: 0
- False negatives: 0

## Interpretation

This is a useful implementation result for the DocGuard live-demo flow because it improves behavior users would expect in an IDE: if documentation already covers the changed behavior, DocGuard should not propose a redundant patch.

This remains synthetic project-evolution evidence. It should not be reported as external benchmark performance, production readiness, or proof of generalization to arbitrary repositories.
