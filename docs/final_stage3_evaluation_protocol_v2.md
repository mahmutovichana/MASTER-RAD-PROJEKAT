# DocGuard Final Stage 3 Evaluation Protocol V2

This protocol defines the final thesis-safe evaluation infrastructure for DocGuard Stage 3 V2 documentation generation.

## Boundary

Stage 3 V2 generation quality is not measured by the historical heuristic `patch_quality` usefulness score. The final flow separates:

- safety/provenance validation
- post-hoc reference comparison
- blind human quality evaluation

The provenance verifier is safety-only. It checks whether generated documentation is supported by available evidence and whether unsafe or unsupported claims appear. It is not a human-quality metric.

## Freeze

Before confirmation evaluation, `scripts/freeze_stage3_v2.py` freezes:

- Stage 3 V2 config hash
- model identifiers
- temperature and token settings
- document retrieval top-k
- repair-attempt policy
- relevant pipeline source hashes
- development summary hash

The freeze manifest records `confirmation_accessed = false` and does not read confirmation examples.

## Samples

The primary final Stage 3 sample is a natural-distribution random sample of predicted-positive cases. It does not balance by category, language, repository, or label.

A secondary category-stratified stress sample may be built across:

- `api_reference`
- `configuration`
- `developer_setup`
- `model_contract`

The stress sample is supplementary only and must not be described as the primary final quality result.

## Reference Evaluation

Reference evaluation is post-hoc and diagnostic. It may use real `docs_after`, documentation diffs, or gold patch summaries where available. These fields must never enter generation prompts or safety verification.

Reference metrics may include lexical overlap and TF-IDF cosine similarity. Exact match is not a primary quality metric.

Cases without a real reference remain valid for blind human evaluation.

## Blind Human Evaluation

Blind review sheets show only:

- case id
- language
- safe code change context
- docs-before context
- selected target document
- generated documentation patch

They do not reveal generation source, first-pass versus repaired status, model confidence, verifier result, gold patch, docs-after, developer documentation change, reference score, grounded output, or historical Qwen output.

Human reviewers score 1-5:

- factual correctness
- semantic completeness
- developer usefulness
- readability
- style fit

Reviewers also provide `human_accept_as_is` as yes/no and optional notes.

## Agreement

An optional second-reviewer comparison supports raw agreement, weighted Cohen's kappa for ordinal scores, and Cohen's kappa for yes/no accept-as-is. Reliability claims require sufficient overlapping approved rows.

## Aggregation

Final aggregation keeps safety, reference metrics, and human ratings in separate report sections. Primary final quality claims prioritize:

- human factual correctness
- human semantic completeness
- human developer usefulness
- human accept-as-is rate

Safety pass rate is reported separately. Reference similarity is supporting evidence only. The final report must not collapse all evidence into one opaque accuracy percentage.

## Historical V1 Boundary

Historical Qwen100 results:

- grounded acceptable: 76%
- Qwen acceptable: 67%
- hybrid cascade acceptable: 87%

These are V1 internal verifier acceptance rates. They are not accuracy, not human quality, and not Final V2 performance.
