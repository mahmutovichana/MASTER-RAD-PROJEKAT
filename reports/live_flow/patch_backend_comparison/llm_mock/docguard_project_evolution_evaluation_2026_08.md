# DocGuard Project Evolution Evaluation 2026-08

This is a synthetic project-evolution live demo. It simulates multiple PR-like changes across invented projects and runs `docguard_hybrid.predict()` with sanitized input only: code-side changed files, code diff, docs-before excerpt, project id, and case id.

- Patch backend: `llm-mock`

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
| `patch_non_empty_rate_for_positive_cases` | 100.00% |
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
- Patch backend/verifier: `llm-mock` / `pass`
- Patch model/generation: `none` / `ok`
- LLM error: ``
- Grounded tokens found: `POST`
- Patch verifier warnings: ``
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
+Mock LLM patch: document `POST` based on the supplied code diff.
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
- Patch backend/verifier: `llm-mock` / `pass`
- Patch model/generation: `none` / `ok`
- LLM error: ``
- Grounded tokens found: `3`
- Patch verifier warnings: ``
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
+Mock LLM patch: document `3` based on the supplied code diff.
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
- Patch backend/verifier: `llm-mock` / `pass`
- Patch model/generation: `none` / `ok`
- LLM error: ``
- Grounded tokens found: `ReviewDto`
- Patch verifier warnings: ``
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
@@ docs/models.md
+Mock LLM patch: document `ReviewDto` based on the supplied code diff.
```

