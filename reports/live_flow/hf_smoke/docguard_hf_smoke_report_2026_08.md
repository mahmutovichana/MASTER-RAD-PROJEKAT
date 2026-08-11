# DocGuard HuggingFace Patch Generation Smoke Report 2026-08

- model: `Qwen/Qwen2.5-1.5B-Instruct`
- cases: 3
- generation status counts: `{"ok": 3}`

This smoke report is produced only when the user explicitly runs the HF command. It may download the requested model through HuggingFace.

## `ATLAS-REVIEW-API-PR-01`

- target doc: `docs/api.md`
- generation status: `ok`
- verifier status: `pass`
- grounded tokens: `/reviews, 201`
- error: ``

Patch:

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

## `ATLAS-REVIEW-API-PR-02`

- target doc: `docs/api.md`
- generation status: `ok`
- verifier status: `pass`
- grounded tokens: ``
- error: ``

Patch:

```diff
@@ docs/api.md
+# API Reference
+- comment: z.string().min(10).max(280)
```

## `ATLAS-REVIEW-API-PR-03`

- target doc: `docs/models.md`
- generation status: `ok`
- verifier status: `pass`
- grounded tokens: `reviewerId`
- error: ``

Patch:

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

