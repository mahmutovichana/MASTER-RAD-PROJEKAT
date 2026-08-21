# DocGuard Patch Backend Comparison 2026-08

HF backend was not run; pass both `--include-hf` and `--hf-model` to compare a real HuggingFace model.

## Summary Counts

Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions.

| Backend | Role | Quality labels | Hallucination risk |
| --- | --- | --- | --- |
| `legacy` | deterministic fallback | `{'needs_review': 5}` | `{'medium': 5}` |
| `llm-hf` | real model output when explicitly requested | `{}` | `{}` |
| `llm-mock` | architecture sanity only | `{'excellent': 5}` | `{'low': 5}` |

## Comparison Table

| Case | Target doc | Backend | Patch preview | Verifier | Warnings | Grounded tokens | Quality | Groundedness | Usefulness | Hallucination risk | Observation |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| `ATLAS-REVIEW-API-PR-01` | `docs/api.md` | `legacy` | `@@ Documentation +new_endpoint.` | `warn` | `patch does not include any concrete token extracted from the diff` | `` | `needs_review` | 0.00 | 0.38 | `medium` | Patch needs review because it is generic, weakly grounded, or verifier warnings remain. |
| `ATLAS-REVIEW-API-PR-01` | `docs/api.md` | `llm-mock` | `@@ docs/api.md +Mock LLM patch: document 'POST' based on the supplied code diff.` | `pass` | `` | `POST` | `excellent` | 0.75 | 0.87 | `low` | Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions. |
| `ATLAS-REVIEW-API-PR-02` | `docs/api.md` | `legacy` | `@@ Documentation +changed_validation_min.` | `warn` | `patch does not include any concrete token extracted from the diff` | `` | `needs_review` | 0.00 | 0.38 | `medium` | Patch needs review because it is generic, weakly grounded, or verifier warnings remain. |
| `ATLAS-REVIEW-API-PR-02` | `docs/api.md` | `llm-mock` | `@@ docs/api.md +Mock LLM patch: document '3' based on the supplied code diff.` | `pass` | `` | `3` | `excellent` | 0.75 | 0.87 | `low` | Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions. |
| `ATLAS-REVIEW-API-PR-03` | `docs/models.md` | `legacy` | `@@ Documentation +added_dto_model_field.` | `warn` | `patch does not include any concrete token extracted from the diff` | `` | `needs_review` | 0.00 | 0.38 | `medium` | Patch needs review because it is generic, weakly grounded, or verifier warnings remain. |
| `ATLAS-REVIEW-API-PR-03` | `docs/models.md` | `llm-mock` | `@@ docs/models.md +Mock LLM patch: document 'ReviewDto' based on the supplied code diff.` | `pass` | `` | `ReviewDto` | `excellent` | 0.75 | 0.87 | `low` | Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions. |
| `ATLAS-REVIEW-API-PR-04` | `docs/configuration.md` | `legacy` | `@@ Documentation +added_environment_variable.` | `warn` | `patch does not include any concrete token extracted from the diff` | `` | `needs_review` | 0.00 | 0.38 | `medium` | Patch needs review because it is generic, weakly grounded, or verifier warnings remain. |
| `ATLAS-REVIEW-API-PR-04` | `docs/configuration.md` | `llm-mock` | `@@ docs/configuration.md +Mock LLM patch: document 'REVIEW_FEATURE_FLAG' based on the supplied code diff.` | `pass` | `` | `REVIEW_FEATURE_FLAG` | `excellent` | 1.00 | 0.98 | `low` | Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions. |
| `ATLAS-REVIEW-API-PR-05` | `docs/workflows.md` | `legacy` | `@@ Documentation +changed_background_job_schedule.` | `warn` | `patch does not include any concrete token extracted from the diff` | `` | `needs_review` | 0.00 | 0.38 | `medium` | Patch needs review because it is generic, weakly grounded, or verifier warnings remain. |
| `ATLAS-REVIEW-API-PR-05` | `docs/workflows.md` | `llm-mock` | `@@ docs/workflows.md +Mock LLM patch: document '0 * * * *' based on the supplied code diff.` | `pass` | `` | `0 * * * *` | `excellent` | 0.75 | 0.87 | `low` | Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions. |

## Detailed Patch Outputs

### `ATLAS-REVIEW-API-PR-01`

#### `legacy`

- target file: `docs/api.md`
- verifier: `warn`
- quality: `needs_review`
- hallucination risk: `medium`
- observation: Patch needs review because it is generic, weakly grounded, or verifier warnings remain.

````diff
@@ Documentation
+new_endpoint.
````

#### `llm-mock`

- target file: `docs/api.md`
- verifier: `pass`
- quality: `excellent`
- hallucination risk: `low`
- observation: Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions.

````diff
@@ docs/api.md
+Mock LLM patch: document `POST` based on the supplied code diff.
````

### `ATLAS-REVIEW-API-PR-02`

#### `legacy`

- target file: `docs/api.md`
- verifier: `warn`
- quality: `needs_review`
- hallucination risk: `medium`
- observation: Patch needs review because it is generic, weakly grounded, or verifier warnings remain.

````diff
@@ Documentation
+changed_validation_min.
````

#### `llm-mock`

- target file: `docs/api.md`
- verifier: `pass`
- quality: `excellent`
- hallucination risk: `low`
- observation: Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions.

````diff
@@ docs/api.md
+Mock LLM patch: document `3` based on the supplied code diff.
````

### `ATLAS-REVIEW-API-PR-03`

#### `legacy`

- target file: `docs/models.md`
- verifier: `warn`
- quality: `needs_review`
- hallucination risk: `medium`
- observation: Patch needs review because it is generic, weakly grounded, or verifier warnings remain.

````diff
@@ Documentation
+added_dto_model_field.
````

#### `llm-mock`

- target file: `docs/models.md`
- verifier: `pass`
- quality: `excellent`
- hallucination risk: `low`
- observation: Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions.

````diff
@@ docs/models.md
+Mock LLM patch: document `ReviewDto` based on the supplied code diff.
````

### `ATLAS-REVIEW-API-PR-04`

#### `legacy`

- target file: `docs/configuration.md`
- verifier: `warn`
- quality: `needs_review`
- hallucination risk: `medium`
- observation: Patch needs review because it is generic, weakly grounded, or verifier warnings remain.

````diff
@@ Documentation
+added_environment_variable.
````

#### `llm-mock`

- target file: `docs/configuration.md`
- verifier: `pass`
- quality: `excellent`
- hallucination risk: `low`
- observation: Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions.

````diff
@@ docs/configuration.md
+Mock LLM patch: document `REVIEW_FEATURE_FLAG` based on the supplied code diff.
````

### `ATLAS-REVIEW-API-PR-05`

#### `legacy`

- target file: `docs/workflows.md`
- verifier: `warn`
- quality: `needs_review`
- hallucination risk: `medium`
- observation: Patch needs review because it is generic, weakly grounded, or verifier warnings remain.

````diff
@@ Documentation
+changed_background_job_schedule.
````

#### `llm-mock`

- target file: `docs/workflows.md`
- verifier: `pass`
- quality: `excellent`
- hallucination risk: `low`
- observation: Mock backend validates prompt/postprocess/verifier flow only; it is excluded from real LLM quality conclusions.

````diff
@@ docs/workflows.md
+Mock LLM patch: document `0 * * * *` based on the supplied code diff.
````

