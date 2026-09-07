# Gate 5 preflight

Status: **PREPARED_NOT_ACTIVATED**.

This is a pre-confirmation infrastructure phase. The sealed confirmation split
must not be opened, read, parsed, sampled, counted, hashed, evaluated, or used
for generation while this preflight is being prepared.

## Frozen upstream

- Gate 4 closure commit:
  `fc49c94d6c6e4c575299e7a4df15985bcea71484`
- Binary model SHA-256:
  `7d6a9263e1262c5c54db3d2e100209707c6a7681133fb1505f44125efa954462`
- Binary threshold: `0.15`
- Category model SHA-256:
  `2d8123ac398568b5c9586b0f8d26d6c4079ddfebd504889b934f77bef65b9f59`
- Gate 4 Stage 3 freeze SHA-256:
  `8d2d7911330d15d04e8b628200252e6c1a614344651596064b293b17b707076f`
- Frozen Stage 3 config SHA-256:
  `27c234a3f998c34256025b0d914ddf3fd2a202eb3466b37a25f5aed0283e3192`

## Confirmation metrics

Binary primary metric is MCC. Category primary metric is intrinsic Macro-F1.

Confidence intervals are repository-cluster bootstrap intervals with:

- 2,000 replicates;
- seed 42;
- alpha 0.05;
- repository as the sampling unit;
- all rows from every sampled repository included;
- a repeated sampled repository contributing its full cluster repeatedly.

The Binary threshold, Category model, Stage 3 configuration, prompts,
retrieval/generation route, input-token budget, and verifier policy are frozen.

## Stage 3

Stage 3 runs only on frozen Binary predicted-positive confirmation cases.
The frozen Category classifier supplies the predicted documentation category.

Rows without canonical retrieval context receive
`retrieval_context_unavailable`, zero LLM calls, and no generated patch.

Generation remains fail-closed for input-budget failures, CUDA OOM and invalid
structured LLM output. Gold/reference/post-change documentation is prohibited
from the generation payload.

## One-shot rule

No real Gate 5 evaluation is performed during preflight.

The canonical one-shot runner will require an explicit execution flag. The
master completion receipt is written only after all frozen Binary, Category and
Stage 3 outputs are complete. Once a master receipt exists for the frozen
identities, canonical rerun is forbidden.

## Gate 6 preregistration

After Gate 5, the primary human-evaluation sample is a seed-42 random
natural-distribution sample of at most 100 frozen Binary predicted positives,
sampled before retrieval-context filtering.

A supplementary stress sample uses up to 25 cases per frozen predicted
documentation category. It must not be pooled with the primary sample.
