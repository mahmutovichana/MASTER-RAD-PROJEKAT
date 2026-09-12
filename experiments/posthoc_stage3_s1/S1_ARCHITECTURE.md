# S1 Repository-Grounded Documentation Agent

S1 is a separate post-hoc Stage 3 challenger. It does not replace or mutate canonical Gates 4–6.

## Execution graph

1. Resolve only an explicit pre-change source: natural rows use the 40-hex commit in the frozen provenance marker; controlled rows use the frozen unchanged local source copy. Missing objects fail closed; `HEAD` and branches are forbidden.
2. Discover documentation deterministically, exclude dependency/build/generated/history trees, prioritize nearest/module documentation, and split content by headings.
3. Build a query from changed paths, diff, identifiers, category and existing docs excerpt. Union path-aware TF-IDF top-k and Qwen dense top-k.
4. Qwen reranker reduces the union to three distinct documents. A separate structured target decision may select any of the three or abstain; rank 1 is never automatic.
5. A structured plan may decide that no developer-facing update is needed.
6. The 14B coder produces one minimal patch using only local pre-change evidence and same-document style. A grounded critic accepts, abstains, or requests the single allowed repair; the repaired patch receives a final critic pass.

Final states are `ACCEPTED`, `ABSTAINED_NO_TARGET`, `ABSTAINED_INSUFFICIENT_EVIDENCE`, `ABSTAINED_UNSUPPORTED_CLAIMS`, `ABSTAINED_LOW_UTILITY`, or `FAILED_EXECUTION`.

## Separation and selection

Only frozen Gate 4 development memberships enter configuration selection. Natural and controlled target metrics are not conflated: explicit target-document evidence exists only for controlled cases. Gate 6 row-level scores, notes and decisions are forbidden. No fresh post-hoc final evaluation is part of this task.

The only selectable values are lexical top-k 5/10, dense top-k 5/10, confidence 0.35/0.50/0.65, and P1/P2. Reranker output is fixed at three documents; inference is deterministic and permits one repair.

To keep repository processing bounded, candidate discovery retains the first 64 documents in deterministic locality order before semantic chunking (4,000 characters per chunk). This fixed resource limit is not development-selected. Dense encoding uses batches of eight. Retrieval combinations are selected only on the 79 controlled rows with target evidence. Threshold outcomes are derived from one minimum-threshold execution; prompts are not selected from self-critic scores alone.
