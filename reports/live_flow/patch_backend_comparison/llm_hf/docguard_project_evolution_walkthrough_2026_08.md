# DocGuard Project Evolution Walkthrough 2026-08

This narrative report is for human inspection and thesis/demo screenshots. It shows what changed, what the documentation said before, what DocGuard detected, where it routed, and what patch it proposed.

## `ATLAS-REVIEW-API-PR-01` Add review creation endpoint

Simulated developer change: Document new POST /reviews endpoint.

Relevant code diff:

```diff
+router.post('/reviews', createReview);
+res.status(201).json({ id: saved.id, reviewStatus: saved.status });
```

Documentation before:

```md
# API Reference

Existing endpoints are documented here.
```

What DocGuard understood: docs update `True`, category `api_reference`, scenario `new_endpoint`.

DocGuard detected signals: `route_added`.

Where DocGuard wanted to write: `docs/api.md`.

Why DocGuard decided that: Matched positive signal `route_added` from: route_added

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

Patch usefulness: useful as a concise starting patch. The patch is intentionally generic and should be reviewed by a developer before applying.

## `ATLAS-REVIEW-API-PR-03` Expose reviewer id in review DTO

Simulated developer change: Document reviewerId in model contract.

Relevant code diff:

```diff
export interface ReviewDto {
   id: string;
+reviewerId: string;
   status: string;
 }
```

Documentation before:

```md
# Models

Core DTOs and response contracts are documented here.
```

What DocGuard understood: docs update `True`, category `model_contract`, scenario `added_dto_model_field`.

DocGuard detected signals: `dto_model_change, dto_field_added`.

Where DocGuard wanted to write: `docs/models.md`.

Why DocGuard decided that: Matched positive signal `dto_field_added` from: dto_model_change, dto_field_added

Generated patch:

```diff
not_applicable
```

Patch usefulness: not applicable because DocGuard predicted no update. The patch is intentionally generic and should be reviewed by a developer before applying.
