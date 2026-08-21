# DocGuard Project Evolution Evaluation 2026-08

This is a synthetic project-evolution live demo. It simulates multiple PR-like changes across invented projects and runs `docguard_hybrid.predict()` with sanitized input only: code-side changed files, code diff, docs-before excerpt, project id, and case id.

- Patch backend: `llm-hf`

## Summary Metrics

| Metric | Value |
| --- | ---: |
| `total_cases` | 3 |
| `binary_accuracy` | 100.00% |
| `precision` | 100.00% |
| `recall` | 100.00% |
| `f1` | 100.00% |
| `category_accuracy` | 100.00% |
| `target_file_accuracy` | 100.00% |
| `scenario_accuracy` | 100.00% |
| `patch_non_empty_rate_for_positive_cases` | 66.67% |
| `false_positives` | 0 |
| `false_negatives` | 0 |
| `unknown_scenarios` | 0 |

## By Project

| Name | Total | Binary | Category | Target | Scenario |
| --- | ---: | ---: | ---: | ---: | ---: |
| `atlas_review_api` | 3 | 100.00% | 100.00% | 100.00% | 100.00% |

## By Category

| Name | Total | Binary | Category | Target | Scenario |
| --- | ---: | ---: | ---: | ---: | ---: |
| `api_reference` | 2 | 100.00% | 100.00% | 100.00% | 100.00% |
| `model_contract` | 1 | 100.00% | 100.00% | 100.00% | 100.00% |

## By Difficulty

| Name | Total | Binary | Category | Target | Scenario |
| --- | ---: | ---: | ---: | ---: | ---: |
| `easy` | 2 | 100.00% | 100.00% | 100.00% | 100.00% |
| `medium` | 1 | 100.00% | 100.00% | 100.00% | 100.00% |

## Per-Case Walkthrough Table

| Case | Project | Difficulty | Binary | Category | Target | Scenario | Gold target | Pred target | Signals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ATLAS-REVIEW-API-PR-01` | `atlas_review_api` | `easy` | `True` | `True` | `True` | `True` | `docs/api.md` | `docs/api.md` | `route_added` |
| `ATLAS-REVIEW-API-PR-02` | `atlas_review_api` | `medium` | `True` | `True` | `True` | `True` | `docs/api.md` | `docs/api.md` | `validation_min_change, validation_max_change, zod_validation_change, comments_only` |
| `ATLAS-REVIEW-API-PR-03` | `atlas_review_api` | `easy` | `True` | `True` | `True` | `True` | `docs/models.md` | `docs/models.md` | `dto_model_change, dto_field_added` |

## Case Details

### `ATLAS-REVIEW-API-PR-01` Add review creation endpoint

- Project: `atlas_review_api`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `api_reference` / `api_reference`
- Gold/pred scenario: `new_endpoint` / `new_endpoint`
- Gold/pred target: `docs/api.md` / `docs/api.md`
- Expected patch summary: Document new POST /reviews endpoint.
- Router reason: Matched positive signal `route_added` from: route_added
- Signals: `route_added`
- Patch backend/verifier: `llm-hf` / `fail`
- Patch model/generation: `Qwen/Qwen2.5-1.5B-Instruct` / `ok`
- LLM error: ``
- Grounded tokens found: `POST, /reviews, 201, id, reviewStatus`
- Patch verifier warnings: `removed noisy model output line; removed noisy model output line; normalized patch into lightweight diff form; patch includes request fields although none are visible in allowed facts`
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
+router.post('/reviews', createReview);
+res.status(201).json({ id: saved.id, reviewStatus: saved.status });
```

Docs before:

```md
# API Reference

Existing endpoints are documented here.
```

Generated patch:

```diff
@@ docs/api.md
+---
+Request Fields:
+---
+Response Fields:
+- id
+- reviewStatus
+Status Codes:
+- 201
+Endpoint Path/Method:
+- /reviews
+- POST
```

### `ATLAS-REVIEW-API-PR-02` Tighten review comment validation

- Project: `atlas_review_api`
- Difficulty: `medium`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `api_reference` / `api_reference`
- Gold/pred scenario: `changed_validation_min` / `changed_validation_min`
- Gold/pred target: `docs/api.md` / `docs/api.md`
- Expected patch summary: Update documented review comment validation.
- Router reason: Matched positive signal `validation_min_change` from: validation_min_change, validation_max_change, zod_validation_change, comments_only
- Signals: `validation_min_change, validation_max_change, zod_validation_change, comments_only`
- Patch backend/verifier: `llm-hf` / `fail`
- Patch model/generation: `Qwen/Qwen2.5-1.5B-Instruct` / `ok`
- LLM error: ``
- Grounded tokens found: ``
- Patch verifier warnings: `normalized patch into lightweight diff form; unsupported field/identifier claims: GET, POST; unsupported quoted/example values: GET, description, id, method, name; patch includes request fields although none are visible in allowed facts; patch does not include any concrete token extracted from the diff; patch is large for a minimal documentation patch`
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
-comment: z.string().min(3).max(500)
+comment: z.string().min(10).max(280)
```

Docs before:

```md
# API Reference

Existing endpoints are documented here.
```

Generated patch:

```diff
@@ docs/api.md
+# API Reference
+The existing endpoints are documented here.
+## Endpoints
+### `/api/v1/endpoint`
+#### GET /api/v1/endpoint
+Get an endpoint's details.
+**Request Fields**
+- **path**: The path to the endpoint (e.g., `/api/v1/endpoint`).
+**Response Fields**
+- **id**: The unique identifier for the endpoint.
+- **name**: The name of the endpoint.
+- **description**: A brief description of the endpoint.
+- **method**: The HTTP method used for this endpoint (`GET`, `POST`, etc.).
+**Status Codes**
+- **200 OK**
+- **400 Bad Request**
+- **404 Not Found**
+**Example Response**
+```json
+{
+  "id": 1,
+  "name": "Endpoint Name",
+  "description": "This is an example endpoint.",
+  "method": "GET"
+}
```

### `ATLAS-REVIEW-API-PR-03` Expose reviewer id in review DTO

- Project: `atlas_review_api`
- Difficulty: `easy`
- Gold/pred docs update: `True` / `True`
- Gold/pred category: `model_contract` / `model_contract`
- Gold/pred scenario: `added_dto_model_field` / `added_dto_model_field`
- Gold/pred target: `docs/models.md` / `docs/models.md`
- Expected patch summary: Document reviewerId in model contract.
- Router reason: Matched positive signal `dto_field_added` from: dto_model_change, dto_field_added
- Signals: `dto_model_change, dto_field_added`
- Patch backend/verifier: `llm-hf` / `fail`
- Patch model/generation: `Qwen/Qwen2.5-1.5B-Instruct` / `error`
- LLM error: `(MaxRetryError('HTTPSConnectionPool(host=\'huggingface.co\', port=443): Max retries exceeded with url: /api/models/Qwen/Qwen2.5-1.5B-Instruct (Caused by NameResolutionError("HTTPSConnection(host=\'huggingface.co\', port=443): Failed to resolve \'huggingface.co\' ([Errno 11001] getaddrinfo failed)"))'), '(Request ID: 4ea58343-196e-40db-8f58-e83d69eaadfd)')`
- Grounded tokens found: ``
- Patch verifier warnings: `empty patch; positive prediction has empty patch`
- Interpretation: DocGuard matched the intended route.

Code diff:

```diff
export interface ReviewDto {
   id: string;
+reviewerId: string;
   status: string;
 }
```

Docs before:

```md
# Models

Core DTOs and response contracts are documented here.
```

Generated patch:

```diff
not_applicable
```

