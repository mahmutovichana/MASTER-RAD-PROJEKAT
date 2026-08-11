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
+patch
+docs/api.md:
+- # API Reference
+## API Reference
+### Endpoints
+**POST /reviews**
+Creates a new review for an existing resource.
+
+**Request Fields**
+| Field | Type | Description |
+--------+-------------------+--------------------------------------------------------------------------------------------------------------------+
+| title  | string           | The title of the review.                                                                                             |
+        +-------------------+--------------------------------------------------------------------------------------------------------------------+
+**Response Fields**
+| Field | Type | Description |
+--------+-------------------+--------------------------------------------------------------------------------------------------------------------+
+| id     | string          | The ID of the created review.                                                                                           |
+| status | string          | The status of the review (e.g., "pending", "approved").                                                             |
+**Status Codes**
+| Code | Description |
+--------+--------------------------------------------------------------------------------------------------------------------+
+| 201   | Created - The review has been successfully created.                                                                                   |
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
@@ docs/models.md
+patch
+docs/models.md
+- # Models
+ # Models
+
+## DTOs
+
+### ReviewDto
+
+**DTO:** Core DTO for reviews.
+
+| Field | Type | Description |
+|-------|------|-------------|
+| id | string | Unique identifier for the review. |
+| reviewerId | string | Identifier for the user who created the review. |
+| status | string | Current status of the review (e.g., "pending", "approved", "rejected"). |
```

Patch usefulness: useful as a concise starting patch. The patch is intentionally generic and should be reviewed by a developer before applying.
