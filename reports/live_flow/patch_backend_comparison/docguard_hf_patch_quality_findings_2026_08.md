# DocGuard HF Patch Quality Findings 2026-08

- model: `Qwen/Qwen2.5-1.5B-Instruct`
- HF cases actually evaluated: 3
- HF quality label counts: `{'rejected': 3}`
- HF hallucination risk counts: `{'high': 3}`
- HF verifier status counts: `{'fail': 3}`

## Best HF Examples

No usable/excellent HF examples were present in this comparison.
## Rejected HF Examples

### `ATLAS-REVIEW-API-PR-01`

- quality: `rejected`
- hallucination risk: `high`
- verifier: `fail`
- warnings: `removed noisy model output line; removed noisy model output line; normalized patch into lightweight diff form; patch includes request fields although none are visible in allowed facts`

````diff
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
````

### `ATLAS-REVIEW-API-PR-02`

- quality: `rejected`
- hallucination risk: `high`
- verifier: `fail`
- warnings: `normalized patch into lightweight diff form; unsupported field/identifier claims: GET, POST; unsupported quoted/example values: GET, description, id, method, name; patch includes request fields although none are visible in allowed facts; patch does not include any concrete token extracted from the diff; patch is large for a minimal documentation patch`

````diff
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
````

### `ATLAS-REVIEW-API-PR-03`

- quality: `rejected`
- hallucination risk: `high`
- verifier: `fail`
- warnings: `empty patch; positive prediction has empty patch`

````diff
not_applicable
````

## Conclusion

- HF can produce richer grounded patches than the legacy fallback when generation succeeds.
- HF can hallucinate unsupported documentation details and must be guarded.
- The verifier and patch-quality evaluator caught a failed/high-risk HF output in this comparison.
- The deterministic layer is a guardrail and evaluator around generation, not the final generator.
- The project-evolution setup remains synthetic demo evidence, not an external benchmark.
- These results are not a production-readiness claim.

