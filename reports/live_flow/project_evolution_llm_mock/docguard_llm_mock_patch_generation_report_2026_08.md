# DocGuard LLM Mock Patch Generation Report 2026-08

This report exercises the optional LLM patch-generation architecture with the mock backend. No HuggingFace model is downloaded or executed.

- cases evaluated: 24
- patch backend: `llm-mock`
- verifier status counts: `{"pass": 24}`

When a real HuggingFace instruction model is plugged in, the same prompt builder, postprocessor, and verifier remain in place. Only the generation backend changes from `mock` to `hf`.

## Prompt Examples

### `ATLAS-REVIEW-API-PR-01`

Prompt:

```text
You are a senior software technical writer.
Use only the supplied code diff and current documentation.
Do not invent endpoints, fields, defaults, roles, commands, response values, or security mechanisms.
If information is missing, write a minimal safe patch rather than inventing details.
Output Markdown patch only.
Keep the patch minimal and in the style of the project documentation.
Avoid placeholders such as new_endpoint, added_environment_variable, or changed_background_job_schedule.
Do not mention internal gold labels, scenario labels, router labels, or evaluation metadata in the final patch.
Focus on API paths, HTTP methods, request fields, response fields, status codes, validation rules, and auth requirements that are directly visible in the diff.

Project id: atlas_review_api
Target document: docs/api.md
Target section: docs/api.md
Documentation category: api_reference
Router scenario hint: new_endpoint
Detected signals: route_added
Router reason: Matched positive signal `route_added` from: route_added
Concrete tokens extracted from diff: /reviews, 201

Current documentation:
```md
# API Reference

Existing endpoints are documented here.
```

Code diff:
```diff
+router.post('/reviews', createReview);
+res.status(201).json({ id: saved.id, reviewStatus: saved.status });
```

Return only the Markdown patch.
```

Raw mock patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `/reviews` based on the supplied code diff.
```

Postprocessed patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `/reviews` based on the supplied code diff.
```

Verifier: `pass`; warnings: `[]`; grounded tokens: `['/reviews']`

### `ATLAS-REVIEW-API-PR-02`

Prompt:

```text
You are a senior software technical writer.
Use only the supplied code diff and current documentation.
Do not invent endpoints, fields, defaults, roles, commands, response values, or security mechanisms.
If information is missing, write a minimal safe patch rather than inventing details.
Output Markdown patch only.
Keep the patch minimal and in the style of the project documentation.
Avoid placeholders such as new_endpoint, added_environment_variable, or changed_background_job_schedule.
Do not mention internal gold labels, scenario labels, router labels, or evaluation metadata in the final patch.
Focus on API paths, HTTP methods, request fields, response fields, status codes, validation rules, and auth requirements that are directly visible in the diff.

Project id: atlas_review_api
Target document: docs/api.md
Target section: docs/api.md
Documentation category: api_reference
Router scenario hint: changed_validation_min
Detected signals: validation_min_change, validation_max_change, zod_validation_change, comments_only
Router reason: Matched positive signal `validation_min_change` from: validation_min_change, validation_max_change, zod_validation_change, comments_only
Concrete tokens extracted from diff: none

Current documentation:
```md
# API Reference

Existing endpoints are documented here.
```

Code diff:
```diff
-comment: z.string().min(3).max(500)
+comment: z.string().min(10).max(280)
```

Return only the Markdown patch.
```

Raw mock patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `/api` based on the supplied code diff.
```

Postprocessed patch:

```diff
@@ docs/api.md
+Mock LLM patch: document `/api` based on the supplied code diff.
```

Verifier: `pass`; warnings: `[]`; grounded tokens: `[]`

### `ATLAS-REVIEW-API-PR-03`

Prompt:

```text
You are a senior software technical writer.
Use only the supplied code diff and current documentation.
Do not invent endpoints, fields, defaults, roles, commands, response values, or security mechanisms.
If information is missing, write a minimal safe patch rather than inventing details.
Output Markdown patch only.
Keep the patch minimal and in the style of the project documentation.
Avoid placeholders such as new_endpoint, added_environment_variable, or changed_background_job_schedule.
Do not mention internal gold labels, scenario labels, router labels, or evaluation metadata in the final patch.
Focus on DTOs, schemas, model fields, field types, and response contract changes that are directly visible in the diff.

Project id: atlas_review_api
Target document: docs/models.md
Target section: docs/models.md
Documentation category: model_contract
Router scenario hint: added_dto_model_field
Detected signals: dto_model_change, dto_field_added
Router reason: Matched positive signal `dto_field_added` from: dto_model_change, dto_field_added
Concrete tokens extracted from diff: reviewerId

Current documentation:
```md
# Models

Core DTOs and response contracts are documented here.
```

Code diff:
```diff
export interface ReviewDto {
   id: string;
+reviewerId: string;
   status: string;
 }
```

Return only the Markdown patch.
```

Raw mock patch:

```diff
@@ docs/models.md
+Mock LLM patch: document `reviewerId` based on the supplied code diff.
```

Postprocessed patch:

```diff
@@ docs/models.md
+Mock LLM patch: document `reviewerId` based on the supplied code diff.
```

Verifier: `pass`; warnings: `[]`; grounded tokens: `['reviewerId']`

