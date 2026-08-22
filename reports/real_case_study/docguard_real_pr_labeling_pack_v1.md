# DocGuard Real PR Manual Labeling Pack

This file is for human validation of real public GitHub PR candidate cases.

**Important:** this is not model input. It includes audit context such as documentation diffs and docs-after text so a human can assign gold labels. Model/evaluation scripts must use only the explicitly allowed model input fields.

- Source candidates: `data\external\project_case_study\real_pr_candidates_v1.jsonl`
- Records to review: `3`
- Candidate type counts: `{'code_and_docs_changed_needs_manual_validation': 3}`
- Language counts: `{'typescript': 3}`

## Allowed Model Input Fields

- `language`
- `code_changed_files`
- `code_diff_excerpt`
- `docs_before_excerpt`

## Audit / Human Labeling Context

- `source_url`
- `repository`
- `pr_number`
- `pr_title`
- `docs_changed_files`
- `docs_diff_excerpt`
- `docs_after_excerpt`
- `candidate_evidence`
- `gold_docs_update_required`
- `gold_doc_category`
- `gold_target_doc_file`
- `gold_target_section`
- `gold_patch_summary`
- `label_confidence`
- `manual_label_notes`

## Labeling Rules

- Mark `gold_docs_update_required = true` only when the code change has visible user/developer/operator/API/data/config/testing/workflow documentation impact.
- Mark `gold_docs_update_required = false` when the change is internal-only, test-only, fixture/mock/storybook-only, formatting-only, import-only, or implementation detail without documentation impact.
- Use `label_confidence = high` only when the decision is clear.
- Use `label_confidence = medium` when likely but not perfectly obvious.
- Use `label_confidence = low` or `ambiguous` when absence/presence of docs is not enough to decide.
- Use `exclude` for cases that are too large, unrelated, generated, binary-heavy, or impossible to judge from the extracted context.
- Never use `docs_after_excerpt` as model input. It is only for gold label validation.

## Compact Review Table

| Case | Source | Language | Candidate type | Code files | Docs files | Current label |
| --- | --- | --- | --- | ---: | ---: | --- |
| `GH-CAND-0001` | https://github.com/ragpark/controltower/pull/2 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `25` | `5` | `needs_manual_review` |
| `GH-CAND-0002` | https://github.com/d-hinders/Haven-AI/pull/1314 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `4` | `4` | `needs_manual_review` |
| `GH-CAND-0003` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/79 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `23` | `3` | `needs_manual_review` |

## Detailed Review Cases

### `GH-CAND-0001`

- Source URL: https://github.com/ragpark/controltower/pull/2
- Repository: `ragpark/controltower`
- PR number: `2`
- PR title: Align ingestion to the ActiveHub export schema and fix container/mapping defects
- Language: `typescript`
- Code changed files: `['apps/api/Dockerfile', 'apps/api/package.json', 'apps/api/prisma/migrations/20260811120000_activehub_fields/migration.sql', 'apps/api/prisma/schema.prisma', 'apps/api/prisma/seed-data.ts', 'apps/api/prisma/seed.ts', 'apps/api/src/imports/orchestrator.service.ts', 'apps/api/src/orders/dto.ts', 'apps/api/src/orders/orders.service.ts', 'apps/api/src/rules/seed-rules.spec.ts', 'apps/api/test/app.e2e-spec.ts', 'apps/api/tsconfig.build.json', 'apps/web/src/app/settings/sources/page.tsx', 'apps/web/src/components/OrderDrawer.tsx', 'apps/web/src/components/OrdersGrid.tsx', 'package-lock.json', 'packages/shared-types/src/order.ts', 'packages/shared-types/src/source.ts', 'services/ingestion/src/__tests__/csv-parser.spec.ts', 'services/ingestion/src/__tests__/dedup.spec.ts', 'services/ingestion/src/__tests__/normalizer.spec.ts', 'services/ingestion/src/csv-parser.ts', 'services/ingestion/src/dedup.ts', 'services/ingestion/src/normalizer.ts', 'services/ingestion/src/types.ts']`
- Docs changed files: `['README.md', 'docs/api-contracts.md', 'docs/architecture.md', 'docs/erd.md', 'sample-data/README.md']`

Gold label fields to fill:

```json
{
  "gold_docs_update_required": null,
  "gold_doc_category": null,
  "gold_target_doc_file": null,
  "gold_target_section": null,
  "gold_patch_summary": null,
  "label_confidence": "needs_manual_review",
  "manual_label_notes": ""
}
```

Allowed model input — code diff excerpt:

```diff
diff --git a/apps/api/Dockerfile b/apps/api/Dockerfile
--- a/apps/api/Dockerfile
+++ b/apps/api/Dockerfile
@@ -20,6 +20,13 @@ COPY apps/api apps/api
 RUN npm run prisma:generate -w @control-tower/api \
  && npm run build:libs \
  && npm run build:api \
+ && npx tsc apps/api/prisma/seed.ts --outDir apps/api/dist-seed \
+      --module commonjs --target ES2022 --esModuleInterop --skipLibCheck \
+ # Fail the build if the entrypoints are not where the runtime expects them.
+ # The emitted layout shifts if the compilation set gains a file outside src/,
+ # which would otherwise only surface as a crash loop after deployment.
+ && test -f apps/api/dist/main.js \
+ && test -f apps/api/dist-seed/seed.js \
  && npm prune --omit=dev
 
 # ── Runtime stage ───────────────────────────────────────────────────────
@@ -31,6 +38,7 @@ COPY --from=build /repo/node_modules ./node_modules
 COPY --from=build /repo/packages ./packages
 COPY --from=build /repo/services ./services
 COPY --from=build /repo/apps/api/dist ./apps/api/dist
+COPY --from=build /repo/apps/api/dist-seed ./apps/api/dist-seed
 COPY --from=build /repo/apps/api/prisma ./apps/api/prisma
 COPY --from=build /repo/apps/api/package.json ./apps/api/
 COPY apps/api/docker-entrypoint.sh ./apps/api/docker-entrypoint.sh

diff --git a/apps/api/package.json b/apps/api/package.json
--- a/apps/api/package.json
+++ b/apps/api/package.json
@@ -39,6 +39,7 @@
     "jwks-rsa": "^3.1.0",
     "passport": "^0.7.0",
     "passport-jwt": "^4.0.1",
+    "prisma": "^6.2.1",
     "prom-client": "^15.1.3",
     "reflect-metadata": "^0.2.2",
     "rxjs": "^7.8.1"
@@ -53,7 +54,6 @@
     "@types/passport-jwt": "^4.0.1",
     "@types/supertest": "^6.0.2",
     "jest": "^29.7.0",
-    "prisma": "^6.2.1",
     "supertest": "^7.0.0",
     "ts-jest": "^29.2.5",
     "ts-node": "^10.9.2",

diff --git a/apps/api/prisma/migrations/20260811120000_activehub_fields/migration.sql b/apps/api/prisma/migrations/20260811120000_activehub_fields/migration.sql
--- a/apps/api/prisma/migrations/20260811120000_activehub_fields/migration.sql
+++ b/apps/api/prisma/migrations/20260811120000_activehub_fields/migration.sql
@@ -0,0 +1,14 @@
+-- ActiveHub order model alignment: sales channel, customer email and the
+-- Licence Manager reconciliation flags carried by the ActiveHub export.
+
+-- AlterTable
+ALTER TABLE "orders" ADD COLUMN     "order_source" TEXT,
+                     ADD COLUMN     "customer_email" TEXT,
+                     ADD COLUMN     "licence_order_match" TEXT,
+                     ADD COLUMN     "licence_isbn_match" TEXT;
+
+-- CreateIndex
+CREATE INDEX "orders_customer_email_idx" ON "orders"("customer_email");
+
+-- CreateIndex
+CREATE INDEX "orders_order_source_idx" ON "orders"("order_source");

diff --git a/apps/api/prisma/schema.prisma b/apps/api/prisma/schema.prisma
--- a/apps/api/prisma/schema.prisma
+++ b/apps/api/prisma/schema.prisma
@@ -83,12 +83,16 @@ model Order {
   id                   String          @id @default(uuid()) @db.Uuid
   sourceOrderId        String?         @map("source_order_id")
   orderNumber          String          @map("order_number")
+  orderSource          String?         @map("order_source")
   customerId           String?         @map("customer_id")
   customerName         String?         @map("customer_name")
+  customerEmail        String?         @map("customer_email")
   productCode          String          @map("product_code")
   productName          String?         @map("product_name")
   orderStatus          String?         @map("order_status")
   orderState           String?         @map("order_state")
+  licenceOrderMatch    String?         @map("licence_order_match")
+  licenceIsbnMatch     String?         @map("licence_isbn_match")
   classification       Classification?
   classificationReason String?         @map("classification_reason")
   classifiedAt         DateTime?       @map("classified_at")
@@ -111,6 +115,8 @@ model Order {
   @@index([classification])
   @@index([orderDate])
   @@index([customerName])
+  @@index([customerEmail])
+  @@index([orderSource])
   @@index([importedAt])
   @@map("orders")
 }

diff --git a/apps/api/prisma/seed-data.ts b/apps/api/prisma/seed-data.ts
--- a/apps/api/prisma/seed-data.ts
+++ b/apps/api/prisma/seed-data.ts
@@ -0,0 +1,196 @@
+import { Classification, Prisma } from '@prisma/client';
+
+/** Mirrors the ActiveHub orders export headers. */
+export const DEFAULT_MAPPING = {
+  orderSource: 'order_source',
+  orderNumber: 'order_id',
+  orderState: 'Custom Status',
+  orderStatus: 'order_status',
+  orderDate: 'order_created_date_time',
+  customerName: 'full_name',
+  customerEmail: 'email',
+  customerId: 'TEPAccountNumber',
+  productCode: 'productcode',
+  productName: 'productlongname',
+  licenceOrderMatch: 'LicenceManagerOrderMatch',
+  licenceIsbnMatch: 'LicenceManagerISBNMatch',
+};
+
+export interface SeedRule {
+  name: string;
+  description: string;
+  priority: number;
+  strategy: string;
+  ruleDefinition: Prisma.InputJsonObject;
+  outcome: Classification;
+}
+
+/**
+ * The canonical rule set. Evaluated in ascending priority; first match wins.
+ * The Licence Manager flags carry the operational meaning: a store order that
+ * completed but has no matching licence means the customer has paid and cannot
+ * access the product.
+ */
+export const CLASSIFICATION_RULES: SeedRule[] = [
+  {
+    name: 'Cancelled orders',
+    description: 'Order cancelled, refunded or declined',
+    priority: 10,
+    strategy: 'field-match',
+    ruleDefinition: {
+      match: 'any',
+      conditions: [
+        {
+          field: 'orderStatus',
+          operator: 'in',
+          value: ['Cancelled', 'Canceled', 'Refunded', 'Declined', 'Void'],
+        },
+        { field: 'orderState', operator: 'contains', value: 'cancel' },
+      ],
+    },
+    outcome: Classification.CANCELLED,
+  },
+  {
+    name: 'Paid but no licence provisioned',
+    description:
+      'Order completed in the store but Licence Manager has no matching order — ' +
+      'the customer has paid and cannot access the product',
+    priority: 20,
+    strategy: 'field-match',
+    ruleDefinition: {
+      conditions: [
+        { field: 'orderStatus', operator: 'in', value: ['Complete', 'Completed', 'Shipped'] },
+        { field: 'licenceOrderMatch', operator: 'eq', value: 'Not Match' },
+      ],
+    },
+    outcome: Classification.CUSTOMER_IMPACTED,
+  },
+  {
+    name: 'Wrong product licensed',
+    description:
+      'Licence Manager matched the order but not the ISBN — the customer may have ' +
+      'access to the wrong product',
+    priority: 30,
+    strategy: 'field-match',
+    ruleDefinition: {
+      conditions: [
+        { field: 'licenceOrderMatch', operator: 'eq', value: 'Match' },
+        { field: 'licenceIsbnMatch', operator: 'eq', value: 'Not Match' },
+      ],
+    },
+    outcome: Classification.INVESTIGATE_REQUIRED,
+  },
+  {
+    name: 'Data quality exception',
+    description: 'Orders with no identifiable customer cannot be reconciled',
+    priority: 40,
+    strategy: 'field-match',
+    ruleDefinition: {
+      conditions: [
+        { field: 'customerName', operator: 'isEmpty' },
+        { field: 'customerEmail', operator: 'isEmpty' },
+      ],
+    },
+    outcome: Classification.EXCEPTION,
+  },
+  {
+    name: 'Completed and fully reconciled',
+    description: 'Store order complete and Licence Manager matches on both order and ISBN',
+    priority: 50,
+    strategy: 'field-match',
+    ruleDefinition: {
+      conditions: [
+        { field: 'orderStatus', operator: 'in', value: ['Complete', 'Completed'] },
+        { field: 'licenceOrderMatch', operator: 'eq', value: 'Match' },
+        // Both flags must be positive — an unknown or missing ISBN result is not
+        // reconciled and must fall through to the catch-all for a human to check.
+        { field: 'licenceIsbnMatch', operator: 'eq', value: 'Match' },
+      ],
+    },
+    outcome: Classification.COMPLETED,
+  },
+  {
+    name: 'Stale incomplete order',
+    description: 'Still incomplete more than 7 days after it was created',
+    priority: 60,
+    strategy: 'order-age',
+    ruleDefinition: {
+      olderThanDays: 7,
+      dateField: 'orderDate',
+      whenStatusIn: ['Incomplete', 'Pending', 'Awaiting Payment'],
+    },
+    outcome: Classification.INVESTIGATE_REQUIRED,
+  },
+  {
+    name: 'In fulfilment',
+    description: 'Payment taken and the order is progressing',
+    priority: 70,
+    strategy: 'field-match',
+    ruleDefinition: {
+      match: 'any',
+      conditions: [
+        {
+          field: 'orderStatus',
+          operator: 'in',
+          value: ['Awaiting Fulfillment', 'Awaiting Shipment', 'Processing', 'Shipped', 'Dispatched'],
+        },
+      ],
+    },
+    outcome: Classification.PLACED,
+  },
+  {
+    name: 'Pending orders',
+    description: 'Incomplete baskets and orders awaiting payment',
+    priorit...
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ a41b04e959b3512e63d0831c83fb7f370b00ba8a -->
# Order Control Tower

A production-ready operational platform that replaces an Excel order dashboard:
configurable data-source ingestion, a database-driven classification rule
engine, operational queues, executive dashboards, and full audit/traceability —
built as a modern SaaS-style web application.

| Layer | Tech |
|---|---|
| Frontend | React 19 · Next.js 15 · TypeScript · Material UI · TanStack Query · Zustand · Recharts |
| Backend | Node.js · NestJS 11 · TypeScript · event-driven orchestration |
| Data | PostgreSQL 16 · Prisma ORM |
| Auth | Microsoft Entra ID (OIDC) with RBAC app roles (`admin` / `operator` / `viewer`) |
| Ops | Docker · Docker Compose · Azure Container Apps / App Service · OpenTelemetry · Prometheus metrics |

📐 [Architecture diagram](docs/architecture.md) · 🗄️ [Database ERD](docs/erd.md) · 🔌 [API contracts](docs/api-contracts.md) · 🚀 [Deployment](infrastructure/deployment/README.md)

## Repository layout

```
apps/
  web/                  Next.js frontend (dashboard, queues, settings)
  api/                  NestJS API (REST v1, orchestration, auth, observability)
services/
  ingestion/            Connector registry + CSV parsing/mapping/validation/dedup
  classification/       Rule engine (strategy pattern, priority evaluation, tracing)
  reporting/            Trend bucketing + operational health calculators
packages/
  shared-types/         Enums, DTOs and event contracts shared end-to-end
  ui-components/        Reusable MUI components (+ component tests)
infrastructure/
  docker-compose/       Local/single-VM stack (db + api + web)
  migrations/           SQL copy of the Prisma migration history
  deployment/           Azure Container Apps Bicep + App Service guide
sample-data/            CSVs exercising every classification outcome
docs/                   Architecture, ERD, API contracts
```

The three `services/*` packages hold the domain logic and are consumed by the
API as libraries (modular monolith). They have no NestJS or Prisma
dependencies, so any of them can be split into a standalone worker later
without rewriting the domain code.

## Quick start (Docker)

```bash
docker compose -f infrastructure/docker-compose/docker-compose.yml up --build
```

- Web: http://localhost:3000 · API: http://localhost:4000 · Swagger: http://localhost:4000/api/docs
- Migrations apply and default rules/sources seed automatically.
- Go to **Import History**, pick the *Manual CSV upload* source and upload
  [`sample-data/orders_sample.csv`](sample-data/orders_sample.csv), then
  `orders_update_sample.csv` to see dedup + record history + reclassification.

## Quick start (local development)

```bash
npm install
docker compose -f infrastructure/docker-compose/docker-compose.yml up -d db

cp .env.example .env                       # defaults work out of the box
npm run prisma:generate
npm run prisma:migrate                     # apply migrations
npm run prisma:seed                        # default rules + sources

npm run build:libs                         # build shared packages once
npm run dev:api                            # NestJS on :4000
npm run dev:web                            # Next.js on :3000  (second terminal)
```

Auth is **off by default** (`AUTH_ENABLED=false`) — the API injects a local
admin identity so the whole stack runs without an Entra tenant. Flip
`AUTH_ENABLED` / `NEXT_PUBLIC_AUTH_ENABLED` to `true` and fill in the Entra
settings for real environments (see
[deployment guide](infrastructure/deployment/README.md#entra-id-setup)).

## How it works

### Ingestion orchestration (event-driven)

Per import: **detect → fetch → parse/map → validate → dedupe → persist
(+history) → classify → aggregate → publish**. Scheduled sources get a cron
job each (managed from Settings); manual uploads hit the same pipeline.
Events (`OrderImported`, `OrderUpdated`, `OrderClassified`,
`OrderReclassified`, `ImportCompleted`, `ImportFailed`) drive the audit trail
and daily aggregates, and are centrally typed so the in-process bus can be
swapped for Azure Service Bus.

Connectors implement one interface and register in a registry — CSV upload,
CSV file drop, REST API and Azure Blob (SAS) are implemented; SFTP,
SharePoint and Tableau are registered as planned connectors that surface
cleanly in the UI. All source configuration (connector settings, column
mapping, delimiter, schedule) is editable in **Settings → Data Sources**,
including *Test connection*, *Run now* and per-source import history.

### Deduplication & history

Natural key **(orderNumber, productCode)** — a unique constraint enforces it.
Re-imports update the existing order; the previous state is snapshotted into
`order_history` with the changed fields, and changed orders are re-classified.

### Rule engine

Rules live in the `classification_rules` table and are evaluated in ascending
priority; the first match wins, with `INVESTIGATE_REQUIRED` as fallback.
Strategies...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -49,9 +49,10 @@ docker compose -f infrastructure/docker-compose/docker-compose.yml up --build
 
 - Web: http://localhost:3000 · API: http://localhost:4000 · Swagger: http://localhost:4000/api/docs
 - Migrations apply and default rules/sources seed automatically.
-- Go to **Import History**, pick the *Manual CSV upload* source and upload
-  [`sample-data/orders_sample.csv`](sample-data/orders_sample.csv), then
-  `orders_update_sample.csv` to see dedup + record history + reclassification.
+- Go to **Import History**, pick the *ActiveHub manual upload* source and upload
+  [`sample-data/activehub_orders_sample.csv`](sample-data/activehub_orders_sample.csv),
+  then `activehub_orders_update_sample.csv` to see dedup + record history +
+  reclassification.
 
 ## Quick start (local development)
 
@@ -94,11 +95,28 @@ cleanly in the UI. All source configuration (connector settings, column
 mapping, delimiter, schedule) is editable in **Settings → Data Sources**,
 including *Test connection*, *Run now* and per-source import history.
 
+### Data model
+
+The canonical order model targets the **ActiveHub orders export** — BigCommerce
+orders reconciled against Licence Manager — carrying the sales channel, customer
+name/email/TEP account, ISBN, store status, custom status and the two Licence
+Manager match flags. Every source maps its own headers onto these canonical
+fields in Settings, so the model is not tied to one export format. See
+[`sample-data/README.md`](sample-data/README.md) for the full column mapping.
+
+Two real-world export hazards are handled explicitly: sheets padded with
+thousands of empty rows are skipped (not counted, not reported as errors), and
+ISBNs that Excel mangled into scientific notation (`9.78141E+12`) are **rejected
+with actionable guidance** rather than expanded — expanding them would collapse
+every ISBN sharing a prefix onto one deduplication key.
+
 ### Deduplication & history
 
 Natural key **(orderNumber, productCode)** — a unique constraint enforces it.
 Re-imports update the existing order; the previous state is snapshotted into
 `order_history` with the changed fields, and changed orders are re-classified.
+A licence flag flipping `Not Match` → `Match` therefore moves the order out of
+the Customer Impacted queue automatically, with the change recorded in history.
 
 ### Rule engine

diff --git a/docs/api-contracts.md b/docs/api-contracts.md
--- a/docs/api-contracts.md
+++ b/docs/api-contracts.md
@@ -20,7 +20,7 @@ Paginated list shape:
 
 | Method | Path | Role | Description |
 |---|---|---|---|
-| GET | `/orders` | viewer | Paged list. Query: `page`, `pageSize`, `search`, `classification`, `sourceId`, `customerName`, `productCode`, `orderState`, `dateFrom`, `dateTo`, `sortBy`, `sortDir` |
+| GET | `/orders` | viewer | Paged list. Query: `page`, `pageSize`, `search`, `classification`, `sourceId`, `orderSource`, `customerName`, `productCode`, `orderState`, `licenceOrderMatch`, `licenceIsbnMatch`, `dateFrom`, `dateTo`, `sortBy`, `sortDir`. `search` spans order number, customer name/email/account, product code and name |
 | GET | `/orders/export` | viewer | CSV export with the same filters |
 | GET | `/orders/:id` | viewer | Order detail: order + source + latest import run |
 | GET | `/orders/:id/trace` | viewer | Rule execution trace of latest evaluation (grouped by `evaluationId`) |

diff --git a/docs/architecture.md b/docs/architecture.md
--- a/docs/architecture.md
+++ b/docs/architecture.md
@@ -87,8 +87,13 @@ flowchart TB
 2. **Fetch** — the connector for the source type retrieves file(s)
    (`services/ingestion` connector registry — strategy pattern, new connectors
    register without touching the orchestrator).
-3. **Parse & map** — CSV parsed with a per-source column mapping (configured in the UI).
-4. **Validate** — required fields, types; row-level failures recorded on the import run log.
+3. **Parse & map** — CSV parsed with a per-source column mapping (configured in
+   the UI). Defaults target the ActiveHub export headers. BOM, CRLF and the
+   thousands of empty filler rows Excel appends are handled transparently.
+4. **Validate** — required fields, types; row-level failures recorded on the
+   import run log. Product codes exported in scientific notation
+   (`9.78141E+12`) are rejected rather than expanded, because the lost digits
+   would collapse distinct ISBNs onto one deduplication key.
 5. **Deduplicate** — natural key `(orderNumber, productCode)`; existing orders are
    updated and a full snapshot is written to `order_history`.
 6. **Classify** — the rule engine evaluates enabled rules in priority order;

diff --git a/docs/erd.md b/docs/erd.md
--- a/docs/erd.md
+++ b/docs/erd.md
@@ -44,12 +44,16 @@ erDiagram
         uuid id PK
         text source_order_id
         text order_number "UK with product_code"
-        text customer_id
+        text order_source "sales channel, e.g. Big Commerce"
+        text customer_id "TEP account number"
         text customer_name
-        text product_code "UK with order_number"
+        text customer_email
+        text product_code "UK with order_number — ISBN"
         text product_name
         text order_status "raw status from source"
-        text order_state "normalised operational state"
+        text order_state "Custom Status from source"
+        text licence_order_match "Licence Manager: Match | Not Match"
+        text licence_isbn_match "Licence Manager: Match | Not Match"
         Classification classification "PENDING | PLACED | COMPLETED | CANCELLED | CUSTOMER_IMPACTED | INVESTIGATE_REQUIRED | EXCEPTION"
         text classification_reason
         timestamptz classified_at
@@ -135,4 +139,14 @@ erDiagram
 | `order_history.order_id` FK cascade | History travels with the order |
 | `rule_executions.rule_id` FK `SET NULL` | Trace survives rule deletion (name retained) |
 | `daily_aggregates (date, classification)` unique | Idempotent aggregate upserts |
-| Indexes on `orders.classification`, `orders.order_date`, `orders.customer_name`, `audit_logs (entity_type, entity_id)` | Queue filtering, trends, audit drill-down |
+| Indexes on `orders.classification`, `orders.order_date`, `orders.customer_name`, `orders.customer_email`, `orders.order_source`, `audit_logs (entity_type, entity_id)` | Queue filtering, trends, audit drill-down |
+
+## Source data model
+
+The canonical `orders` table is populated from the **ActiveHub orders export**
+(BigCommerce orders reconciled against Licence Manager) via the per-source
+column mapping in `sources.config_json`. The two `licence_*_match` columns drive
+the highest-value rules: an order that is `Complete` in the store but
+`Not Match` in Licence Manager means the customer has paid and cannot access the
+product — classified **Customer Impacted**. Other sources map their own headers
+onto the same canonical fields, so the model is not tied to one export format.

diff --git a/sample-data/README.md b/sample-data/README.md
--- a/sample-data/README.md
+++ b/sample-data/README.md
@@ -1,23 +1,62 @@
 # Sample data
 
-- `orders_sample.csv` — 24 rows covering every classification outcome:
-  completed, placed, pending, cancelled, customer-impacted (failed delivery /
-  returns / customer hold), a data-quality exception (missing customer), an
-  unrecognised status (falls through to *Investigate Required*), stale open
-  orders, and an in-file duplicate (`ORD-1002` appears twice with different
-  product codes — both kept; duplicates share the *(orderNumber, productCode)*
-  key only when both fields match).
-- `orders_update_sample.csv` — a follow-up file that updates three existing
-  orders (status changes → history snapshots + reclassification) and adds one
-  new order. Upload it second to see deduplication and record history working.
-
-Dates use the UK `dd/mm/yyyy` export format on purpose — the parser accepts
-both this and ISO 8601.
-
-Upload via **Import History → Upload CSV** (against the seeded
-"Manual CSV upload" source) or:
-
-```bash
-curl -F sourceId=<source-id> -F file=@sample-data/orders_sample.csv \
-  http://localhost:4000/api/v1/imports/upload
-```
+Both files use the **ActiveHub orders export** schema (BigCommerce orders
+reconciled against Licence Manager), which is the format the default column
+mapping targets:
+
+| Column | Canonical field |
+|---|---|
+| `order_source` | `orderSource` (sales channel) |
+| `order_id` | `orderNumber` ✱ |
+| `Custom Status` | `orderState` |
+| `order_status` | `orderStatus` |
+| `order_created_date_time` | `orderDate` (`dd/mm/yyyy hh:mm`) |
+| `full_name` | `customerName` |
+| `email` | `customerEmail` |
+| `TEPAccountNumber` | `customerId` |
+| `productcode` | `productCode` ✱ (ISBN) |
+| `productlongname` | `productName` |
+| `LicenceManagerOrderMatch` | `licenceOrderMatch` |
+| `LicenceManagerISBNMatch` | `licenceIsbnMatch` |
+
+✱ together these form the deduplication...
```

Audit context only — docs after excerpt:

```markdown
<!-- README.md @ 1dfa80405635a8908dda05d7471cfe9cfa81efd0 -->
# Order Control Tower

A production-ready operational platform that replaces an Excel order dashboard:
configurable data-source ingestion, a database-driven classification rule
engine, operational queues, executive dashboards, and full audit/traceability —
built as a modern SaaS-style web application.

| Layer | Tech |
|---|---|
| Frontend | React 19 · Next.js 15 · TypeScript · Material UI · TanStack Query · Zustand · Recharts |
| Backend | Node.js · NestJS 11 · TypeScript · event-driven orchestration |
| Data | PostgreSQL 16 · Prisma ORM |
| Auth | Microsoft Entra ID (OIDC) with RBAC app roles (`admin` / `operator` / `viewer`) |
| Ops | Docker · Docker Compose · Azure Container Apps / App Service · OpenTelemetry · Prometheus metrics |

📐 [Architecture diagram](docs/architecture.md) · 🗄️ [Database ERD](docs/erd.md) · 🔌 [API contracts](docs/api-contracts.md) · 🚀 [Deployment](infrastructure/deployment/README.md)

## Repository layout

```
apps/
  web/                  Next.js frontend (dashboard, queues, settings)
  api/                  NestJS API (REST v1, orchestration, auth, observability)
services/
  ingestion/            Connector registry + CSV parsing/mapping/validation/dedup
  classification/       Rule engine (strategy pattern, priority evaluation, tracing)
  reporting/            Trend bucketing + operational health calculators
packages/
  shared-types/         Enums, DTOs and event contracts shared end-to-end
  ui-components/        Reusable MUI components (+ component tests)
infrastructure/
  docker-compose/       Local/single-VM stack (db + api + web)
  migrations/           SQL copy of the Prisma migration history
  deployment/           Azure Container Apps Bicep + App Service guide
sample-data/            CSVs exercising every classification outcome
docs/                   Architecture, ERD, API contracts
```

The three `services/*` packages hold the domain logic and are consumed by the
API as libraries (modular monolith). They have no NestJS or Prisma
dependencies, so any of them can be split into a standalone worker later
without rewriting the domain code.

## Quick start (Docker)

```bash
docker compose -f infrastructure/docker-compose/docker-compose.yml up --build
```

- Web: http://localhost:3000 · API: http://localhost:4000 · Swagger: http://localhost:4000/api/docs
- Migrations apply and default rules/sources seed automatically.
- Go to **Import History**, pick the *ActiveHub manual upload* source and upload
  [`sample-data/activehub_orders_sample.csv`](sample-data/activehub_orders_sample.csv),
  then `activehub_orders_update_sample.csv` to see dedup + record history +
  reclassification.

## Quick start (local development)

```bash
npm install
docker compose -f infrastructure/docker-compose/docker-compose.yml up -d db

cp .env.example .env                       # defaults work out of the box
npm run prisma:generate
npm run prisma:migrate                     # apply migrations
npm run prisma:seed                        # default rules + sources

npm run build:libs                         # build shared packages once
npm run dev:api                            # NestJS on :4000
npm run dev:web                            # Next.js on :3000  (second terminal)
```

Auth is **off by default** (`AUTH_ENABLED=false`) — the API injects a local
admin identity so the whole stack runs without an Entra tenant. Flip
`AUTH_ENABLED` / `NEXT_PUBLIC_AUTH_ENABLED` to `true` and fill in the Entra
settings for real environments (see
[deployment guide](infrastructure/deployment/README.md#entra-id-setup)).

## How it works

### Ingestion orchestration (event-driven)

Per import: **detect → fetch → parse/map → validate → dedupe → persist
(+history) → classify → aggregate → publish**. Scheduled sources get a cron
job each (managed from Settings); manual uploads hit the same pipeline.
Events (`OrderImported`, `OrderUpdated`, `OrderClassified`,
`OrderReclassified`, `ImportCompleted`, `ImportFailed`) drive the audit trail
and daily aggregates, and are centrally typed so the in-process bus can be
swapped for Azure Service Bus.

Connectors implement one interface and register in a registry — CSV upload,
CSV file drop, REST API and Azure Blob (SAS) are implemented; SFTP,
SharePoint and Tableau are registered as planned connectors that surface
cleanly in the UI. All source configuration (connector settings, column
mapping, delimiter, schedule) is editable in **Settings → Data Sources**,
including *Test connection*, *Run now* and per-source import history.

### Data model

The canonical order model targets the **ActiveHub orders export** — BigCommerce
orders reconciled against Licence Manager — carrying the sales channel, customer
name/email/TEP account, ISBN, store status, custom status and the two Licence
Manager match flags. Every source maps its own headers onto these canonical
fields in Settings, so the model is not tied to one export format. See
[`s...
```

### `GH-CAND-0002`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1314
- Repository: `d-hinders/Haven-AI`
- PR number: `1314`
- PR title: feat(mcp+sdk): structured next_action/agent_summary/warnings contract (#1308)
- Language: `typescript`
- Code changed files: `['packages/mcp-server/src/tools.test.ts', 'packages/mcp-server/src/tools.ts', 'packages/sdk/src/index.ts', 'packages/sdk/src/types.ts']`
- Docs changed files: `['docs/architecture/04-x402-payment-sequence.md', 'docs/architecture/07-edge-signer.md', 'docs/operations/mcp-runtime-compatibility.md', 'docs/regulatory/casp-risk-guardrails.md']`

Gold label fields to fill:

```json
{
  "gold_docs_update_required": null,
  "gold_doc_category": null,
  "gold_target_doc_file": null,
  "gold_target_section": null,
  "gold_patch_summary": null,
  "label_confidence": "needs_manual_review",
  "manual_label_notes": ""
}
```

Allowed model input — code diff excerpt:

```diff
diff --git a/packages/mcp-server/src/tools.test.ts b/packages/mcp-server/src/tools.test.ts
--- a/packages/mcp-server/src/tools.test.ts
+++ b/packages/mcp-server/src/tools.test.ts
@@ -1720,3 +1720,85 @@ describe('merchant MCP endpoint discovery (#1271)', () => {
     expect(calls.filter((c) => c.method === 'POST').length).toBe(1)
   })
 })
+
+// ── #1308: structured next-step contract ─────────────────────────────────────
+
+describe('structured agent guidance (#1308)', () => {
+  const paymentRequiredHeader = () => btoa(JSON.stringify(PAYMENT_REQUIRED))
+  const stubs = () => ({
+    'GET /machine-payments/agent': { status: 200 as const, body: AGENT_RESPONSE },
+    'POST /x402': { status: 201 as const, body: X402_INTENT_RESPONSE },
+    'POST /mcp': {
+      status: 402 as const,
+      responseHeaders: { 'PAYMENT-REQUIRED': paymentRequiredHeader() },
+    },
+  })
+  const pay = () =>
+    handlers().haven_pay_mcp_tool({
+      merchant_url: 'http://merchant.test/mcp',
+      tool_name: 'buy_vpn',
+      arguments: { plan: 'basic' },
+    })
+
+  it('a signable quote tells the agent EXACTLY what to do next — from the existing taxonomy', async () => {
+    stubFetch(stubs())
+    const result = ok<{
+      next_action: string
+      next_tool: string
+      next_arguments: Record<string, unknown>
+      safe_to_continue: boolean
+      agent_summary: Record<string, unknown>
+      warnings: Array<{ code: string; message: string }>
+    }>(await pay())
+
+    expect(result.data.next_action).toBe('sign_and_submit_payment') // AgentPaymentNextAction value, no parallel vocabulary
+    expect(result.data.next_tool).toBe('mcp__haven-signer__haven_sign_x402')
+    expect(result.data.next_arguments).toEqual({ payment_id: 'pay_x402' })
+    expect(result.data.safe_to_continue).toBe(true)
+    expect(result.data.agent_summary).toMatchObject({ payment_id: 'pay_x402', status: 'pending_signature' })
+  })
+
+  it('warnings absorb the cap nudge as MISSING_MAX_AMOUNT while cap_warning stays for compat', async () => {
+    stubFetch(stubs())
+    const result = ok<{ cap_warning?: string; warnings: Array<{ code: string }> }>(await pay())
+
+    expect(result.data.cap_warning).toBeDefined()
+    expect(result.data.warnings.some((w) => w.code === 'MISSING_MAX_AMOUNT')).toBe(true)
+  })
+
+  it('passing max_amount clears BOTH the legacy field and the structured warning', async () => {
+    stubFetch(stubs())
+    const result = ok<{ cap_warning?: string; warnings: Array<{ code: string }> }>(
+      await handlers().haven_pay_mcp_tool({
+        merchant_url: 'http://merchant.test/mcp',
+        tool_name: 'buy_vpn',
+        arguments: { plan: 'basic' },
+        max_amount: '2000000',
+      }),
+    )
+    expect(result.data.cap_warning).toBeUndefined()
+    expect(result.data.warnings.some((w) => w.code === 'MISSING_MAX_AMOUNT')).toBe(false)
+  })
+
+  it('pending approval is UNSAFE to continue and points at status polling', async () => {
+    stubFetch({
+      ...stubs(),
+      'POST /x402': {
+        status: 202,
+        body: { payment_id: 'pay_pending', status: 'pending_approval' },
+      },
+    })
+    const result = ok<{
+      status: string
+      next_action: string
+      next_tool: string
+      safe_to_continue: boolean
+      agent_summary: Record<string, unknown>
+    }>(await pay())
+
+    expect(result.data.status).toBe('pending_approval')
+    expect(result.data.next_action).toBe('wait_for_user_approval')
+    expect(result.data.next_tool).toBe('mcp__haven__haven_get_payment_status')
+    expect(result.data.safe_to_continue).toBe(false)
+  })
+})

diff --git a/packages/mcp-server/src/tools.ts b/packages/mcp-server/src/tools.ts
--- a/packages/mcp-server/src/tools.ts
+++ b/packages/mcp-server/src/tools.ts
@@ -5,6 +5,10 @@ import {
   HavenApiError,
   MerchantTimeoutError,
   X402UnexpectedStatusError,
+  AgentPaymentWarningCode,
+  type AgentNextStep,
+  type AgentPaymentWarning,
+  type AgentSummary,
   HavenClient,
   HavenError,
   HavenPaymentStateError,
@@ -288,6 +292,7 @@ const SUBMIT_DESCRIPTION = [
 const PAY_MCP_TOOL_DESCRIPTION = composeDescription({
   ...sharedDescriptions.payMcpTool,
   behavior:
+    'FOLLOW THE STRUCTURED FIELDS FIRST (#1308): responses carry next_action, next_tool, next_arguments, agent_summary and warnings — act on those; the prose below is fallback and debugging detail. ' +
     'Builds the JSON-RPC tools/call envelope and probes the merchant to obtain the x402 payment_required. merchant_url may be the exact MCP endpoint or a BASE merchant URL (#1271): a non-402 miss triggers one bounded same-origin discovery pass of the merchant discovery document and one retry; the returned merchant_url is the resolved endpoint — pass THAT to settle/complete. ' +
     'Creates a funding intent and returns { payment_id, payload_hash, expires_at, payment_required, x402, signer_compatibility, merchant_url, tool_name, arguments, mcp_transport }. ' +
     'The funding/quote window expires at expires_at; if it expires, re-run haven_pay_mcp_tool with the same idempotency_key before signing again. ' +
@@ -346,6 +351,8 @@ const QUOTE_X402_DESCRIPTION = composeDescription({
 })
 
 const PAY_X402_QUOTE_DESCRIPTION = [
+  'FOLLOW THE STRUCTURED FIELDS FIRST (#1308): responses carry next_action, next_tool,',
+  'next_arguments, agent_summary and warnings — act on those; prose is fallback.',
   'Construct the funding step for an x402 payment and return the unsigned hash for the local',
   'signer to sign. For read-only allowance, budget, spend-limit, remaining-amount, or',
   'reset-period questions, call haven_get_allowances instead of calling this tool.',
@@ -768,10 +775,54 @@ export function createToolHandlers(
             tool_name: args.tool_name,
             arguments: args.arguments ?? {},
             ...(quote.mcpTransport ? { mcp_transport: serializeMcpTransport(quote.mcpTransport) } : {}),
+            // #1308: machine-readable next step — the agent follows this
+            // before parsing any prose.
+            ...buildAgentGuidance({
+              nextAction: AgentPaymentNextAction.SignAndSubmitPayment,
+              nextTool: 'mcp__haven-signer__haven_sign_x402',
+              nextArguments: { payment_id: intent.paymentId },
+              safeToContinue: true,
+              reason:
+                'Sign locally: call next_tool with next_arguments plus payment_required taken ' +
+                'VERBATIM from this response, then haven_settle_mcp_tool with the returned ' +
+                'signature + payment_header and the merchant_url/tool_name/arguments/mcp_transport ' +
+                'from this response.',
+              summary: {
+                payment_id: intent.paymentId,
+                status: intent.status,
+                amount: quote.amount,
+                amount_atomic: quote.amountAtomic,
+                token: quote.token,
+                network: intent.network,
+                expires_at: intent.expiresAt,
+                product: args.tool_name,
+              },
+              warnings: quoteWarnings({
+                maxAmount: args.max_amount as string | undefined,
+                expiresAt: intent.expiresAt,
+                ...(merchantUrl !== args.merchant_url ? { discoveredFrom: args.merchant_url } : {}),
+              }),
+            }),
           }
         } catch (err) {
           if (err instanceof HavenPaymentStateError && isPendingApproval(err.status)) {
-            return { payment_id: err.paymentId, status: 'pending_approval', payload_hash: null }
+            return {
+              payment_id: err.paymentId,
+              status: 'pending_approval',
+              payload_hash: null,
+              // #1308: over-budget is a USER decision — never continue silently.
+              ...buildAgentGuidance({
+                nextAction: AgentPaymentNextAction.WaitForUserApproval,
+                nextTool: 'mcp__haven__haven_get_payment_status',
+                nextArguments: { payment_id: err.paymentId ?? null },
+                safeToContinue: false,
+                reason:
+                  'The amount exceeds the remaining budget, so the payment is queued for the ' +
+                  'wallet owner. Tell the user, then poll next_tool — do NOT re-quote or re-pay ' +
+                  'the same purchase while it is pending.',
+                summary: { payment_id: err.paymentId ?? 'unknown', status: 'pending_approval' },
+              }),
+            }
           }
           throw err
         }
@@ -814,6 +865,18 @@ export function createToolHandlers(
           settled: true,
           result: merchant.result,
           settlement_tx_hash: merchant.settlement_tx_hash,
+          // #1308: done — nothing left but reporting.
+          ...buildAgentGuidance({
+            nextAction: AgentPaymentNextAction.None,
+            safeToContinue: true,
+            reason:
+              'Funding and merchant settlement both su...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/architecture/04-x402-payment-sequence.md @ 696e9f1b5015f9536d7180b76c0c1c3add20f842 -->
---
owner: "@d-hinders"
status: current
contract: true
covers:
  - packages/backend/src/routes/x402.ts
  - packages/backend/src/modules/x402/**
  - packages/backend/src/routes/x402-resources.ts
  - packages/backend/src/modules/payments/agent-payment-status.ts
  - packages/backend/src/domain/payment-coverage.ts
  - packages/backend/src/modules/x402/x402-delegation.ts
  - packages/backend/src/rails/delegation-rail.ts
  - packages/sdk/src/client.ts
  - packages/sdk/src/x402.ts
  - packages/mcp/src/tools.ts
  - packages/mcp-server/src/tools.ts
  - packages/signer/src/core.ts
  - packages/signer/src/tools.ts
  - packages/frontend/src/components/ApprovalQueue.tsx
  - packages/qa-agent/src/scenarios/x402-hosted-mcp-signer.ts
last-verified: "2026-08-11" # #1300 review: merchant timeout calibrated to 300s; funded-timeout verify-then-sweep routing
---

# Haven - x402 Payment Execution Sequence

How an agent pays for an x402-protected resource through Haven today.
Standard merchant-verifiable x402 support is `exact`-scheme USDC on Base and
Base Sepolia. Haven can parse some additional network/token forms for legacy
proofs and display, but they are not part of the standard settlement path.

Standard merchant x402 has two legs:

1. Haven funding leg: within budget, an agent-signed Safe AllowanceModule
   transfer funds the delegate wallet. Over budget, the user must approve and
   execute a Safe funding transaction.
2. Merchant leg: the agent signs the standard EIP-3009 `X-PAYMENT` header from
   the delegate wallet and retries the merchant/resource request.

> **This doc describes the legacy AllowanceModule rail** (import-only, existing
> accounts) with its two-leg funding model. New accounts
> (`account_type='delegator_hybrid'`) settle x402 in a **single direct leg** via
> ERC-7710 — see [Delegation rail x402](#delegation-rail-x402-new-accounts)
> below. The Smart Sessions **session rail is retired** (#834): the machine-payment
> path answers HTTP 410 for `session_key` accounts, fail-closed.

In SDK, local MCP, and generic hosted split flows, the agent retries the merchant
request. For paid MCP tools, hosted MCP can proxy the HTTP/MCP request and
deliver an already signed payment header. It remains keyless and does not act as
a facilitator/acquirer, hold merchant funds, or create the payment signature.

Source of truth:

- [`packages/sdk/src/x402.ts`](../../packages/sdk/src/x402.ts)
- [`packages/sdk/src/client.ts`](../../packages/sdk/src/client.ts)
- [`packages/backend/src/routes/x402.ts`](../../packages/backend/src/routes/x402.ts) — request
  validation, auth wiring, rate-limit config, and response serialization only.
  The authorize orchestration (scheme routing, funding-leg prep, erc7710 child
  building, the #961 replay/resume logic) and settle assembly live in
  [`packages/backend/src/modules/x402/`](../../packages/backend/src/modules/x402/index.ts)
  (#996, epic #980 M4). `x402-delegation.ts` lives inside that module (folded
  in by #998 — its only production consumers were already inside it) — it is
  the settlement *compiler* (typed-data / header assembly primitives), not
  route orchestration.
- [`packages/backend/src/domain/payment-coverage.ts`](../../packages/backend/src/domain/payment-coverage.ts)
- [`packages/mcp/src/tools.ts`](../../packages/mcp/src/tools.ts)
- [`packages/mcp-server/src/tools.ts`](../../packages/mcp-server/src/tools.ts)
- [`docs/regulatory/casp-risk-guardrails.md`](../regulatory/casp-risk-guardrails.md)

## Challenge And Header Semantics

The SDK normalizes the merchant's 402 response into a `PaymentRequired` object.
It accepts the v2 `PAYMENT-REQUIRED` header, the v1 `X-PAYMENT` challenge
header, and a JSON-body fallback. When the delegate address is known, probes
also send `x402-wallet`. The paid retry uses `X-PAYMENT`; a successful merchant
response may include `PAYMENT-RESPONSE` evidence.

`quoteX402()` and `haven_quote_x402` are read-only. They parse the challenge but
do not create a Haven payment, approval request, signature, or on-chain
transaction.

Every merchant-facing SDK fetch (probes, MCP handshakes, paid retries,
resume retries) is bounded since #1300: `config.merchantTimeout` (default
**300 s**, calibrated to the protocol contract — the merchant's own
`maxTimeoutSeconds: 300` and viem's 180 s settlement wait; a test pins the
default at or above it), caller signals combined, timeout surfaced as the
typed `MerchantTimeoutError` (504, names the URL). A non-402 quote answer is
the typed `X402UnexpectedStatusError`. A timeout AFTER confirmed funding is
routed to `MERCHANT_UNRESPONSIVE_AFTER_FUNDING` with verify-then-sweep
guidance — an unanswered retry is not proof of rejection, and the merchant
may still settle late against its valid EIP-3009 authorization.

Hosted `haven_pay_mcp_tool` additionally accepts a **base merchant URL**
(#1271): when the probe misses (non-402), it mak...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/architecture/04-x402-payment-sequence.md b/docs/architecture/04-x402-payment-sequence.md
--- a/docs/architecture/04-x402-payment-sequence.md
+++ b/docs/architecture/04-x402-payment-sequence.md
@@ -18,7 +18,7 @@ covers:
   - packages/signer/src/tools.ts
   - packages/frontend/src/components/ApprovalQueue.tsx
   - packages/qa-agent/src/scenarios/x402-hosted-mcp-signer.ts
-last-verified: "2026-08-11" # #1300 review: merchant timeout calibrated to 300s; funded-timeout verify-then-sweep routing
+last-verified: "2026-08-11" # #1308 structured next-step contract on hosted purchase responses (+ #1300/#1301 same train)
 ---
 
 # Haven - x402 Payment Execution Sequence
@@ -89,6 +89,14 @@ routed to `MERCHANT_UNRESPONSIVE_AFTER_FUNDING` with verify-then-sweep
 guidance — an unanswered retry is not proof of rejection, and the merchant
 may still settle late against its valid EIP-3009 authorization.
 
+Since #1308 the hosted purchase responses carry a **structured next-step
+contract**: `next_action` (values from the existing AgentPaymentNextAction
+taxonomy), `next_tool` + small literal `next_arguments`, `safe_to_continue`
+(false on pending approval — over-budget is a user decision), a compact
+`agent_summary`, and an advisory `warnings[]` (MISSING_MAX_AMOUNT absorbs the
+#1275 cap nudge; QUOTE_EXPIRES_SOON; MERCHANT_URL_DISCOVERED). Warnings never
+replace refusals; failure codes stay authoritative.
+
 Hosted `haven_pay_mcp_tool` additionally accepts a **base merchant URL**
 (#1271): when the probe misses (non-402), it makes one bounded same-origin
 discovery pass — GET `/.well-known/haven-demo-merchant` then `/`, no

diff --git a/docs/architecture/07-edge-signer.md b/docs/architecture/07-edge-signer.md
--- a/docs/architecture/07-edge-signer.md
+++ b/docs/architecture/07-edge-signer.md
@@ -27,7 +27,7 @@ covers:
   - docs/architecture/04-x402-payment-sequence.md
   - docs/architecture/06-hosted-mcp-connect-flow.md
   - docs/regulatory/casp-risk-guardrails.md
-last-verified: "2026-08-11" # #1300-kalibrering (300s, unresponsive-routing) + #1272/#1271 same train
+last-verified: "2026-08-11" # #1308: quote/settle-svar bär next_action-kontraktet; signerytan oförändrad
 ---
 
 # Haven — Edge Signer

diff --git a/docs/operations/mcp-runtime-compatibility.md b/docs/operations/mcp-runtime-compatibility.md
--- a/docs/operations/mcp-runtime-compatibility.md
+++ b/docs/operations/mcp-runtime-compatibility.md
@@ -8,7 +8,7 @@ covers:
   - packages/signer/**
   - packages/mcp-server/src/tools.ts
   - .github/workflows/publish.yml
-last-verified: "2026-08-11" # #1300-kalibrering: 300s merchant-default + MERCHANT_UNRESPONSIVE_AFTER_FUNDING; ingen floor/manifest-ändring
+last-verified: "2026-08-11" # #1308: hosted responses gained structured guidance fields (additiva); ingen floor/manifest-ändring
 ---
 
 # MCP Runtime Compatibility

diff --git a/docs/regulatory/casp-risk-guardrails.md b/docs/regulatory/casp-risk-guardrails.md
--- a/docs/regulatory/casp-risk-guardrails.md
+++ b/docs/regulatory/casp-risk-guardrails.md
@@ -796,3 +796,4 @@ one — the staleness audit ranks on it.
 - **#1273/#1274** — the demo merchant's `list_products` now returns stable, machine-readable per-product metadata (`product_id`, `arguments_schema`, `supported_settlement_methods`, `default_settlement_method`, `mcp_url`, …) built from the same #1266 settlement-method resolution the merchant already advertises — it consumes, never re-decides, the eip3009-first/erc7710-pinned-manager gate, so that contract is inherited rather than restated. `buy_vpn`/`buy_cloud_storage` now also return a top-level `summary` (status, product, amounts, tx hash) read straight off the already-SETTLED `SettledPayment`, never re-derived from the quoted catalog price. Both are DISPLAY/REPORTING data only, documented as such in code: the `x-receipt-json` header, invoice and on-chain settlement state are untouched, and `status: 'confirmed'` is reachable only after on-chain settlement is proven. Demo merchant only, no Haven custody, merchant-acquiring, fee, or settlement-provider role added. Perimeter unchanged.
 - **#1300** — every merchant-facing SDK fetch (x402/MPP probes, MCP handshakes, paid retries, resume retries — ten call sites) is now bounded by `merchantTimeout` (default 60 s, caller signals combined via AbortSignal.any), with a timeout surfaced as a clear 504 naming the URL; and quoteX402's non-402 miss became the typed `X402UnexpectedStatusError`. Availability hardening and error typing only: no authority, route, signing surface, custody boundary or refusal changed — a hung merchant can no longer hold a hosted tool call open indefinitely, which narrows a DoS surface rather than widening anything. Perimeter unchanged.
 - **#1300 (calibration)** — the post-merge review found the 60 s merchant-fetch default contradicted the repo's own tolerances (the merchant's advertised `maxTimeoutSeconds: 300`; viem's 180 s settlement wait), risking client-side aborts of legitimately-settling payments; the default is now 300 s (test-pinned ≥ the contract) and a timeout AFTER confirmed funding is routed to a distinct `MERCHANT_UNRESPONSIVE_AFTER_FUNDING` code whose guidance is verify-then-sweep — an unanswered paid retry is NOT proof of rejection, the merchant holds a valid EIP-3009 authorization and may settle late, so blind sweeping could race a late settlement. Availability calibration and failure classification only; no authority, route, signing surface or custody boundary changed. Perimeter unchanged.
+- **#1308** — x402 MCP purchase responses gained a structured next-step contract (`next_action` from the existing taxonomy, `next_tool`/`next_arguments`, `safe_to_continue`, `agent_summary`, advisory `warnings[]` where MISSING_MAX_AMOUNT absorbs the #1275 cap nudge back-compatibly). Guidance and observability only: warnings never replace a refusal, failure codes are unchanged, pending-approval explicitly marks `safe_to_continue: false` so an agent cannot read over-budget as continuable, and no authority, route, signing surface or custody boundary moved. Perimeter unchanged.
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/architecture/04-x402-payment-sequence.md @ e7ce3640c159e380d3fa4996451c3dc0024039c0 -->
---
owner: "@d-hinders"
status: current
contract: true
covers:
  - packages/backend/src/routes/x402.ts
  - packages/backend/src/modules/x402/**
  - packages/backend/src/routes/x402-resources.ts
  - packages/backend/src/modules/payments/agent-payment-status.ts
  - packages/backend/src/domain/payment-coverage.ts
  - packages/backend/src/modules/x402/x402-delegation.ts
  - packages/backend/src/rails/delegation-rail.ts
  - packages/sdk/src/client.ts
  - packages/sdk/src/x402.ts
  - packages/mcp/src/tools.ts
  - packages/mcp-server/src/tools.ts
  - packages/signer/src/core.ts
  - packages/signer/src/tools.ts
  - packages/frontend/src/components/ApprovalQueue.tsx
  - packages/qa-agent/src/scenarios/x402-hosted-mcp-signer.ts
last-verified: "2026-08-11" # #1308 structured next-step contract on hosted purchase responses (+ #1300/#1301 same train)
---

# Haven - x402 Payment Execution Sequence

How an agent pays for an x402-protected resource through Haven today.
Standard merchant-verifiable x402 support is `exact`-scheme USDC on Base and
Base Sepolia. Haven can parse some additional network/token forms for legacy
proofs and display, but they are not part of the standard settlement path.

Standard merchant x402 has two legs:

1. Haven funding leg: within budget, an agent-signed Safe AllowanceModule
   transfer funds the delegate wallet. Over budget, the user must approve and
   execute a Safe funding transaction.
2. Merchant leg: the agent signs the standard EIP-3009 `X-PAYMENT` header from
   the delegate wallet and retries the merchant/resource request.

> **This doc describes the legacy AllowanceModule rail** (import-only, existing
> accounts) with its two-leg funding model. New accounts
> (`account_type='delegator_hybrid'`) settle x402 in a **single direct leg** via
> ERC-7710 — see [Delegation rail x402](#delegation-rail-x402-new-accounts)
> below. The Smart Sessions **session rail is retired** (#834): the machine-payment
> path answers HTTP 410 for `session_key` accounts, fail-closed.

In SDK, local MCP, and generic hosted split flows, the agent retries the merchant
request. For paid MCP tools, hosted MCP can proxy the HTTP/MCP request and
deliver an already signed payment header. It remains keyless and does not act as
a facilitator/acquirer, hold merchant funds, or create the payment signature.

Source of truth:

- [`packages/sdk/src/x402.ts`](../../packages/sdk/src/x402.ts)
- [`packages/sdk/src/client.ts`](../../packages/sdk/src/client.ts)
- [`packages/backend/src/routes/x402.ts`](../../packages/backend/src/routes/x402.ts) — request
  validation, auth wiring, rate-limit config, and response serialization only.
  The authorize orchestration (scheme routing, funding-leg prep, erc7710 child
  building, the #961 replay/resume logic) and settle assembly live in
  [`packages/backend/src/modules/x402/`](../../packages/backend/src/modules/x402/index.ts)
  (#996, epic #980 M4). `x402-delegation.ts` lives inside that module (folded
  in by #998 — its only production consumers were already inside it) — it is
  the settlement *compiler* (typed-data / header assembly primitives), not
  route orchestration.
- [`packages/backend/src/domain/payment-coverage.ts`](../../packages/backend/src/domain/payment-coverage.ts)
- [`packages/mcp/src/tools.ts`](../../packages/mcp/src/tools.ts)
- [`packages/mcp-server/src/tools.ts`](../../packages/mcp-server/src/tools.ts)
- [`docs/regulatory/casp-risk-guardrails.md`](../regulatory/casp-risk-guardrails.md)

## Challenge And Header Semantics

The SDK normalizes the merchant's 402 response into a `PaymentRequired` object.
It accepts the v2 `PAYMENT-REQUIRED` header, the v1 `X-PAYMENT` challenge
header, and a JSON-body fallback. When the delegate address is known, probes
also send `x402-wallet`. The paid retry uses `X-PAYMENT`; a successful merchant
response may include `PAYMENT-RESPONSE` evidence.

`quoteX402()` and `haven_quote_x402` are read-only. They parse the challenge but
do not create a Haven payment, approval request, signature, or on-chain
transaction.

Every merchant-facing SDK fetch (probes, MCP handshakes, paid retries,
resume retries) is bounded since #1300: `config.merchantTimeout` (default
**300 s**, calibrated to the protocol contract — the merchant's own
`maxTimeoutSeconds: 300` and viem's 180 s settlement wait; a test pins the
default at or above it), caller signals combined, timeout surfaced as the
typed `MerchantTimeoutError` (504, names the URL). A non-402 quote answer is
the typed `X402UnexpectedStatusError`. A timeout AFTER confirmed funding is
routed to `MERCHANT_UNRESPONSIVE_AFTER_FUNDING` with verify-then-sweep
guidance — an unanswered retry is not proof of rejection, and the merchant
may still settle late against its valid EIP-3009 authorization.

Since #1308 the hosted purchase responses carry a **structured next-step
contract**: `next_action` (values from the exist...
```

### `GH-CAND-0003`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/79
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `79`
- PR title: Add Agent Plugin (agent-plugins.org) as a fourth artifact type
- Language: `typescript`
- Code changed files: `['schemas/organization.schema.json', 'schemas/plugin-approval.schema.json', 'src/consolidate.test.ts', 'src/consolidate.ts', 'src/plugin-source.test.ts', 'src/plugin-source.ts', 'src/skill-source.ts', 'src/validate.test.ts', 'src/validate.ts', 'website/src/components/ArtifactList.tsx', 'website/src/components/OrgBadges.tsx', 'website/src/components/OrgList.tsx', 'website/src/components/PluginDetail.tsx', 'website/src/components/PluginList.tsx', 'website/src/components/ServerDetail.tsx', 'website/src/components/ServerList.tsx', 'website/src/components/SkillList.tsx', 'website/src/hooks/useRegistryData.ts', 'website/src/pages/AboutPage.tsx', 'website/src/pages/ApiDocsPage.tsx', 'website/src/pages/HomePage.tsx', 'website/src/pages/ToolPage.tsx', 'website/src/types.ts']`
- Docs changed files: `['AGENTS.md', 'README.md', 'skills/create-plugin-approval/SKILL.md']`

Gold label fields to fill:

```json
{
  "gold_docs_update_required": null,
  "gold_doc_category": null,
  "gold_target_doc_file": null,
  "gold_target_section": null,
  "gold_patch_summary": null,
  "label_confidence": "needs_manual_review",
  "manual_label_notes": ""
}
```

Allowed model input — code diff excerpt:

```diff
diff --git a/schemas/organization.schema.json b/schemas/organization.schema.json
--- a/schemas/organization.schema.json
+++ b/schemas/organization.schema.json
@@ -62,6 +62,11 @@
             "type": "string",
             "description": "URL prefix for auto-generating MCP server install URLs. The artifact serverId is appended literally.",
             "examples": ["theia://install-mcp?id="]
+          },
+          "pluginInstallUrlPrefix": {
+            "type": "string",
+            "description": "URL prefix for auto-generating Agent Plugin install URLs. The artifact pluginId is appended literally.",
+            "examples": ["theia://install-plugin?id="]
           }
         }
       }

diff --git a/schemas/plugin-approval.schema.json b/schemas/plugin-approval.schema.json
--- a/schemas/plugin-approval.schema.json
+++ b/schemas/plugin-approval.schema.json
@@ -0,0 +1,68 @@
+{
+  "$schema": "http://json-schema.org/draft-07/schema#",
+  "$id": "https://ai.open-vsx.org/schemas/plugin-approval.schema.json",
+  "title": "Plugin Approval",
+  "description": "Vendor approval for an Agent Plugin (agent-plugins.org) in the AI Registry",
+  "type": "object",
+  "required": ["pluginId", "date", "source"],
+  "additionalProperties": false,
+  "properties": {
+    "pluginId": {
+      "type": "string",
+      "minLength": 1,
+      "description": "Plugin identifier using reverse-domain notation (e.g., io.github.gemini-cli-extensions/bigquery-data-analytics)"
+    },
+    "date": {
+      "type": "string",
+      "format": "date",
+      "description": "ISO date of approval (YYYY-MM-DD)"
+    },
+    "source": {
+      "type": "object",
+      "required": ["url"],
+      "additionalProperties": false,
+      "description": "Location of the plugin folder in a git repository",
+      "properties": {
+        "url": {
+          "type": "string",
+          "format": "uri",
+          "description": "Git repository URL containing the plugin"
+        },
+        "path": {
+          "type": "string",
+          "minLength": 1,
+          "pattern": "^(?!\\.\\.?(?:/|$))[A-Za-z0-9._-]+(?:/(?!\\.\\.?(?:/|$))[A-Za-z0-9._-]+)*$",
+          "description": "Path within the repository to the plugin folder (containing plugin.json). Omit if the plugin is at the repository root. Restricted to safe path characters (no whitespace or shell metacharacters, since this value is passed to a git sparse-checkout command during consolidation) and no '.' or '..' path segments (no traversal, no empty segments from a double slash). A segment may still start with a dot otherwise (e.g. '.claude/plugins/foo')."
+        }
+      }
+    },
+    "installConfigs": {
+      "type": "array",
+      "description": "Tool-specific installation configurations. Omit if no tool-specific configuration is needed.",
+      "items": {
+        "type": "object",
+        "required": ["tool"],
+        "additionalProperties": false,
+        "properties": {
+          "tool": {
+            "type": "string",
+            "description": "Tool ID this config targets (must match a tool in the AI Registry)"
+          },
+          "installUrl": {
+            "type": "string",
+            "format": "uri",
+            "description": "Deep-link URL for one-click install (tool-specific protocol)"
+          },
+          "config": {
+            "type": "object",
+            "description": "Tool-specific configuration object"
+          },
+          "instructions": {
+            "type": "string",
+            "description": "Human-readable setup instructions"
+          }
+        }
+      }
+    }
+  }
+}

diff --git a/src/consolidate.test.ts b/src/consolidate.test.ts
--- a/src/consolidate.test.ts
+++ b/src/consolidate.test.ts
@@ -4,6 +4,7 @@ import {
   addOrganization,
   addApproval,
   addSkillApproval,
+  addPluginApproval,
   resolveSkillInstallUrls,
   resolveSkillTrust,
   filterValidSkillTrusts,
@@ -15,18 +16,21 @@ import {
   resolveMcpCrossVendorConfigs,
   buildToolView,
   buildToolSkillView,
+  buildToolPluginView,
   type ConsolidatedOutput,
   type ApprovalData,
   type SkillApprovalData,
+  type PluginApprovalData,
   type Approval,
   type McpEntry,
   type SkillEntry,
+  type PluginEntry,
   type SkillTrustEntry,
   type McpTrustEntry,
 } from "./consolidate.js";
 
 function emptyOutput(): ConsolidatedOutput {
-  return { organizations: [], tools: [], mcp: [], skills: [] };
+  return { organizations: [], tools: [], mcp: [], skills: [], plugins: [] };
 }
 
 describe("addOrganization", () => {
@@ -691,6 +695,157 @@ describe("addSkillApproval", () => {
   });
 });
 
+describe("addPluginApproval", () => {
+  const pluginApproval: PluginApprovalData = {
+    pluginId: "io.example/my-plugin",
+    date: "2026-08-01",
+    source: {
+      url: "https://github.com/example/my-plugin.git",
+    },
+    installConfigs: [{ tool: "tool-a" }],
+  };
+
+  it("creates a new plugin entry", () => {
+    const output = emptyOutput();
+    addPluginApproval(pluginApproval, "acme", output);
+
+    assert.equal(output.plugins.length, 1);
+    assert.equal(output.plugins[0].pluginId, "io.example/my-plugin");
+    assert.equal(output.plugins[0].name, "io.example/my-plugin");
+    assert.equal(output.plugins[0].description, "");
+    assert.equal(output.plugins[0].contentHash, "");
+    assert.deepEqual(output.plugins[0].containedSkills, []);
+    assert.deepEqual(output.plugins[0].containedMcpServers, []);
+    assert.equal(output.plugins[0].approvals.length, 1);
+    assert.equal(output.plugins[0].approvals[0].organizationId, "acme");
+  });
+
+  it("merges approvals from multiple vendors for the same plugin", () => {
+    const output = emptyOutput();
+    addPluginApproval(pluginApproval, "acme", output);
+    addPluginApproval(
+      { ...pluginApproval, installConfigs: [{ tool: "tool-b" }] },
+      "other-org",
+      output,
+    );
+
+    assert.equal(output.plugins.length, 1);
+    assert.equal(output.plugins[0].approvals.length, 2);
+    assert.equal(output.plugins[0].approvals[1].organizationId, "other-org");
+  });
+
+  it("produces a stable configHash", () => {
+    const output1 = emptyOutput();
+    const output2 = emptyOutput();
+    addPluginApproval(pluginApproval, "acme", output1);
+    addPluginApproval(pluginApproval, "acme", output2);
+
+    assert.equal(
+      output1.plugins[0].approvals[0].configHash,
+      output2.plugins[0].approvals[0].configHash,
+    );
+  });
+
+  it("produces different configHash when approval data changes", () => {
+    const output1 = emptyOutput();
+    const output2 = emptyOutput();
+    addPluginApproval(pluginApproval, "acme", output1);
+    addPluginApproval(
+      { ...pluginApproval, date: "2026-08-02" },
+      "acme",
+      output2,
+    );
+
+    assert.notEqual(
+      output1.plugins[0].approvals[0].configHash,
+      output2.plugins[0].approvals[0].configHash,
+    );
+  });
+
+  it("defaults installConfigs to an empty array when omitted", () => {
+    const output = emptyOutput();
+    addPluginApproval(
+      {
+        pluginId: "io.example/bare",
+        date: "2026-08-01",
+        source: pluginApproval.source,
+      },
+      "acme",
+      output,
+    );
+    assert.deepEqual(output.plugins[0].approvals[0].installConfigs, []);
+  });
+
+  it("keeps the first-collected source when a second vendor's source differs", () => {
+    const output = emptyOutput();
+    addPluginApproval(pluginApproval, "acme", output);
+    addPluginApproval(
+      {
+        ...pluginApproval,
+        source: { url: "https://github.com/other/fork.git" },
+      },
+      "other-org",
+      output,
+    );
+
+    assert.equal(output.plugins.length, 1);
+    assert.deepEqual(output.plugins[0].source, pluginApproval.source);
+  });
+
+  it("still records both approvals when sources differ", () => {
+    const output = emptyOutput();
+    addPluginApproval(pluginApproval, "acme", output);
+    addPluginApproval(
+      {
+        ...pluginApproval,
+        source: { url: "https://github.com/other/fork.git" },
+      },
+      "other-org",
+      output,
+    );
+
+    assert.equal(output.plugins[0].approvals.length, 2);
+    assert.equal(output.plugins[0].approvals[0].organizationId, "acme");
+    assert.equal(output.plugins[0].approvals[1].organizationId, "other-org");
+  });
+
+  it("does not warn when a second vendor's source matches exactly", () => {
+    const output = emptyOutput();
+    const warnCalls: unknown[][] = [];
+    const originalWarn = console.warn;
+    console.warn = (...args: unknown[]) => warnCalls.push(args);
+    try {
+      addPluginApproval(pluginApproval, "acme", output);
+      addPluginApproval(pluginApproval, "other-org", output);
+    } finally {
+      console.warn = originalWarn;
+    }
+    assert.equal(warnCalls.length, 0);
+  });
+
+  it("warns when a second vendor's source differs", () => {
+    const output = emptyOutput();
+    const warnCalls: unknown[][] = [];
+    const originalWarn = c...
```

Allowed model input — docs before excerpt:

```markdown
<!-- AGENTS.md @ eb89c086c7fa2488d75cc8c833771ae91e2d2c45 -->
# AI Registry — Agent Guide

Vendor-neutral, federated trust registry for MCP servers and Agent Skills, hosted at the Eclipse Foundation. This is the core repo — it contains schemas, validation, consolidation, and the website. Approval files live in separate organization-specific vendor repos (e.g., `ai-registry-theia`).

## Architecture

Two artifact types, same approval model:

- **MCP servers** — referenced by `serverId` in the Anthropic MCP registry. Metadata (name, description, version) enriched during consolidation.
- **Agent Skills** — referenced by `skillId` pointing to a git repo + path. `source.path` can be a single string, an array of paths, or a glob pattern (`"skills/*"`) for batch approvals — consolidation expands these into individual entries. Metadata (name, description) extracted from SKILL.md frontmatter; content hash computed via sparse checkout during consolidation.

Organizations can provide tools (with `installConfigs`) or just approve artifacts without tool-specific configuration. Both use the same approval file format — `installConfigs` is optional.

## Data flow

```
Vendor repos → validate → collect → enrich (MCP registry + skill sources) → write static JSON → deploy website
```

Unreachable MCP servers get `mcpRegistryVerified: false`. Unreachable skill sources are skipped with a warning.

## Key conventions

- **IDs**: Reverse-domain notation with `/` separator (e.g., `io.github.anthropics/code-review`)
- **Filenames**: ID with `/` replaced by `--` + `.json` (e.g., `io.github.anthropics--code-review.json`)
- **Directories**: `mcp/` for server approvals, `skills/` for skill approvals
- **Schemas**: `schemas/*.schema.json` — source of truth for all approval formats
- **Pure functions**: Core validation and consolidation logic has no I/O for testability. I/O wrappers are thin layers on top.

## Project layout

```
schemas/                    JSON Schema definitions
src/
  validate.ts               Validation (schema + cross-checks)
  consolidate.ts            Consolidation pipeline (collect, enrich, write)
  skill-source.ts           Skill enrichment (sparse checkout, frontmatter, hashing)
  anthropic-registry.ts     MCP server metadata lookup
  cli-validate.ts           CLI entry: validate a vendor repo
  cli-consolidate.ts        CLI entry: consolidate all vendors
website/                    React + Vite static website
skills/                     Claude Code skills for generating approvals
vendors.json                Registered vendor repos
```

## Commands

```bash
npm run check               # typecheck + lint + format check + tests
npm test                    # tests only (Node.js built-in test runner via tsx)
npm run validate-vendor -- <path>   # validate a vendor repo
npm run consolidate         # consolidate all vendors to dist/api/v1/
npm run dev                 # consolidate + start website dev server
npm run format              # auto-format with Prettier
```

## Testing

Tests use Node.js built-in `node:test` with `assert/strict`. Pure function tests — no mocking, no external dependencies. Run with `npm test`.

## Before committing

Run `npm run format` then `npm run check`. The check includes typecheck, lint, format verification, and tests.

## When editing

- Schemas are the contract — change schemas first, then update validation and consolidation to match.
- `installConfigs` and `tools` are optional. Handle missing values with `?? []`.
- Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification). Phases 2-3 warn on failure, don't block.
- Consolidation is split: collect (no network) → enrich MCP (network, fatal on error) → enrich skills (network, skip on error) → write.
- Website types in `website/src/types.ts` mirror but don't import from `src/consolidate.ts` — keep them in sync manually.

<!-- README.md @ eb89c086c7fa2488d75cc8c833771ae91e2d2c45 -->
# AI Registry

> **Preview** — This registry is currently in preview. Data, APIs, and the website may change as we iterate on the concept.

A vendor-neutral, federated trust registry for AI artifacts, hosted at the Eclipse Foundation. Supports [Model Context Protocol](https://modelcontextprotocol.io) (MCP) servers and [Agent Skills](https://agentskills.io).

## How It Works

The registry follows a federated model: **vendors** maintain their own repositories with approval files for AI artifacts (MCP servers and Agent Skills) they endorse. A **central repository** consolidates all vendor data into a single JSON file that tools can consume.

```
Vendor Repos                    Central Repo                    Consumers
┌──────────────┐
│ Theia IDE    │──┐
│ (approvals)  │  │         ┌─────────────────┐          ┌──────────────┐
└──────────────┘  ├──────►  │  Consolidation  │────────► │  all.json    │
┌──────────────┐  │         │  + Validation   │          │  Website     │
│ Vendor B     │──┘         │  + Met...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/AGENTS.md b/AGENTS.md
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -1,29 +1,30 @@
 # AI Registry — Agent Guide
 
-Vendor-neutral, federated trust registry for MCP servers and Agent Skills, hosted at the Eclipse Foundation. This is the core repo — it contains schemas, validation, consolidation, and the website. Approval files live in separate organization-specific vendor repos (e.g., `ai-registry-theia`).
+Vendor-neutral, federated trust registry for MCP servers, Agent Skills, and Agent Plugins, hosted at the Eclipse Foundation. This is the core repo — it contains schemas, validation, consolidation, and the website. Approval files live in separate organization-specific vendor repos (e.g., `ai-registry-theia`).
 
 ## Architecture
 
-Two artifact types, same approval model:
+Three artifact types, same approval model:
 
 - **MCP servers** — referenced by `serverId` in the Anthropic MCP registry. Metadata (name, description, version) enriched during consolidation.
 - **Agent Skills** — referenced by `skillId` pointing to a git repo + path. `source.path` can be a single string, an array of paths, or a glob pattern (`"skills/*"`) for batch approvals — consolidation expands these into individual entries. Metadata (name, description) extracted from SKILL.md frontmatter; content hash computed via sparse checkout during consolidation.
+- **Agent Plugins** ([agent-plugins.org](https://agent-plugins.org)) — referenced by `pluginId` pointing to a git repo + path (single directory, no glob/array). Consolidation fetches the whole plugin directory via sparse checkout to read `plugin.json` (name, description, version, author, homepage, keywords) and enumerate contents: skills under `skills/*/SKILL.md` and MCP servers in `mcp.json`, surfaced as read-only `containedSkills`/`containedMcpServers` metadata — not as separate standalone entries.
 
-Organizations can provide tools (with `installConfigs`) or just approve artifacts without tool-specific configuration. Both use the same approval file format — `installConfigs` is optional.
+Organizations can provide tools (with `installConfigs`) or just approve artifacts without tool-specific configuration. All three use the same approval file format — `installConfigs` is optional.
 
 ## Data flow
 
 ```
-Vendor repos → validate → collect → enrich (MCP registry + skill sources) → write static JSON → deploy website
+Vendor repos → validate → collect → enrich (MCP registry + skill sources + plugin sources) → write static JSON → deploy website
 ```
 
-Unreachable MCP servers get `mcpRegistryVerified: false`. Unreachable skill sources are skipped with a warning.
+Unreachable MCP servers get `mcpRegistryVerified: false`. Unreachable skill and plugin sources are skipped with a warning.
 
 ## Key conventions
 
 - **IDs**: Reverse-domain notation with `/` separator (e.g., `io.github.anthropics/code-review`)
 - **Filenames**: ID with `/` replaced by `--` + `.json` (e.g., `io.github.anthropics--code-review.json`)
-- **Directories**: `mcp/` for server approvals, `skills/` for skill approvals
+- **Directories**: `mcp/` for server approvals, `skills/` for skill approvals, `plugins/` for plugin approvals
 - **Schemas**: `schemas/*.schema.json` — source of truth for all approval formats
 - **Pure functions**: Core validation and consolidation logic has no I/O for testability. I/O wrappers are thin layers on top.
 
@@ -35,6 +36,7 @@ src/
   validate.ts               Validation (schema + cross-checks)
   consolidate.ts            Consolidation pipeline (collect, enrich, write)
   skill-source.ts           Skill enrichment (sparse checkout, frontmatter, hashing)
+  plugin-source.ts          Plugin enrichment (sparse checkout, manifest + contents)
   anthropic-registry.ts     MCP server metadata lookup
   cli-validate.ts           CLI entry: validate a vendor repo
   cli-consolidate.ts        CLI entry: consolidate all vendors
@@ -66,6 +68,6 @@ Run `npm run format` then `npm run check`. The check includes typecheck, lint, f
 
 - Schemas are the contract — change schemas first, then update validation and consolidation to match.
 - `installConfigs` and `tools` are optional. Handle missing values with `?? []`.
-- Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification). Phases 2-3 warn on failure, don't block.
-- Consolidation is split: collect (no network) → enrich MCP (network, fatal on error) → enrich skills (network, skip on error) → write.
+- Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification), Phase 4 (plugin manifest verification). Phases 2-4 warn on failure, don't block.
+- Consolidation is split: collect (no network) → enrich MCP (network, fatal on error) → enrich skills (network, skip on error) → enrich plugins (network, skip on error) → write.
 - Website types in `website/src/types.ts` mirror but don't import from `src/consolidate.ts` — keep them in sync manually.

diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -2,11 +2,11 @@
 
 > **Preview** — This registry is currently in preview. Data, APIs, and the website may change as we iterate on the concept.
 
-A vendor-neutral, federated trust registry for AI artifacts, hosted at the Eclipse Foundation. Supports [Model Context Protocol](https://modelcontextprotocol.io) (MCP) servers and [Agent Skills](https://agentskills.io).
+A vendor-neutral, federated trust registry for AI artifacts, hosted at the Eclipse Foundation. Supports [Model Context Protocol](https://modelcontextprotocol.io) (MCP) servers, [Agent Skills](https://agentskills.io), and [Agent Plugins](https://agent-plugins.org).
 
 ## How It Works
 
-The registry follows a federated model: **vendors** maintain their own repositories with approval files for AI artifacts (MCP servers and Agent Skills) they endorse. A **central repository** consolidates all vendor data into a single JSON file that tools can consume.
+The registry follows a federated model: **vendors** maintain their own repositories with approval files for AI artifacts (MCP servers, Agent Skills, and Agent Plugins) they endorse. A **central repository** consolidates all vendor data into a single JSON file that tools can consume.
 
 ```
 Vendor Repos                    Central Repo                    Consumers
@@ -25,15 +25,17 @@ Vendor Repos                    Central Repo                    Consumers
 - `organization.json` — organization identity and (optionally) tools
 - `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
 - `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository
+- `plugins/*.json` — one approval file per approved Agent Plugin, pointing to the plugin's source repository
 
 **The central repo** provides:
 
 - JSON schemas that define the contract for all participants
 - A consolidation pipeline that pulls, validates, and merges vendor data
 - Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
 - Metadata enrichment from skill source repos (name, description, content hash)
+- Metadata enrichment from plugin source repos (name, description, version, author, contained skills/MCP servers, content hash)
 - A static website deployed to GitHub Pages for browsing the registry
-- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files
+- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md), [skill](skills/create-skill-approval/SKILL.md), and [plugin](skills/create-plugin-approval/SKILL.md) approval files
 
 ## Repositories
 
@@ -44,10 +46,10 @@ Vendor Repos                    Central Repo                    Consumers
 
 ## Data Flow
 
-1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
+1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md), [skills](skills/create-skill-approval/SKILL.md), or [plugins](skills/create-plugin-approval/SKILL.md))
 2. Vendor commits and pushes — CI validates against the central schemas
 3. On successful push to main, the vendor CI triggers the central consolidation workflow
-4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
+4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata, skill source metadata, and plugin source metadata
 5. The website and consolidated JSON are built and deployed to GitHub Pages
 6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL
 
@@ -63,6 +65,8 @@ mcp/
   <server-id>.json         # one file per approved MCP server
 skills/
   <skill-id>.json          # one...
```

Audit context only — docs after excerpt:

```markdown
<!-- AGENTS.md @ 368cf10f3129fdc3120f156f2e86bc090406cdf8 -->
# AI Registry — Agent Guide

Vendor-neutral, federated trust registry for MCP servers, Agent Skills, and Agent Plugins, hosted at the Eclipse Foundation. This is the core repo — it contains schemas, validation, consolidation, and the website. Approval files live in separate organization-specific vendor repos (e.g., `ai-registry-theia`).

## Architecture

Three artifact types, same approval model:

- **MCP servers** — referenced by `serverId` in the Anthropic MCP registry. Metadata (name, description, version) enriched during consolidation.
- **Agent Skills** — referenced by `skillId` pointing to a git repo + path. `source.path` can be a single string, an array of paths, or a glob pattern (`"skills/*"`) for batch approvals — consolidation expands these into individual entries. Metadata (name, description) extracted from SKILL.md frontmatter; content hash computed via sparse checkout during consolidation.
- **Agent Plugins** ([agent-plugins.org](https://agent-plugins.org)) — referenced by `pluginId` pointing to a git repo + path (single directory, no glob/array). Consolidation fetches the whole plugin directory via sparse checkout to read `plugin.json` (name, description, version, author, homepage, keywords) and enumerate contents: skills under `skills/*/SKILL.md` and MCP servers in `mcp.json`, surfaced as read-only `containedSkills`/`containedMcpServers` metadata — not as separate standalone entries.

Organizations can provide tools (with `installConfigs`) or just approve artifacts without tool-specific configuration. All three use the same approval file format — `installConfigs` is optional.

## Data flow

```
Vendor repos → validate → collect → enrich (MCP registry + skill sources + plugin sources) → write static JSON → deploy website
```

Unreachable MCP servers get `mcpRegistryVerified: false`. Unreachable skill and plugin sources are skipped with a warning.

## Key conventions

- **IDs**: Reverse-domain notation with `/` separator (e.g., `io.github.anthropics/code-review`)
- **Filenames**: ID with `/` replaced by `--` + `.json` (e.g., `io.github.anthropics--code-review.json`)
- **Directories**: `mcp/` for server approvals, `skills/` for skill approvals, `plugins/` for plugin approvals
- **Schemas**: `schemas/*.schema.json` — source of truth for all approval formats
- **Pure functions**: Core validation and consolidation logic has no I/O for testability. I/O wrappers are thin layers on top.

## Project layout

```
schemas/                    JSON Schema definitions
src/
  validate.ts               Validation (schema + cross-checks)
  consolidate.ts            Consolidation pipeline (collect, enrich, write)
  skill-source.ts           Skill enrichment (sparse checkout, frontmatter, hashing)
  plugin-source.ts          Plugin enrichment (sparse checkout, manifest + contents)
  anthropic-registry.ts     MCP server metadata lookup
  cli-validate.ts           CLI entry: validate a vendor repo
  cli-consolidate.ts        CLI entry: consolidate all vendors
website/                    React + Vite static website
skills/                     Claude Code skills for generating approvals
vendors.json                Registered vendor repos
```

## Commands

```bash
npm run check               # typecheck + lint + format check + tests
npm test                    # tests only (Node.js built-in test runner via tsx)
npm run validate-vendor -- <path>   # validate a vendor repo
npm run consolidate         # consolidate all vendors to dist/api/v1/
npm run dev                 # consolidate + start website dev server
npm run format              # auto-format with Prettier
```

## Testing

Tests use Node.js built-in `node:test` with `assert/strict`. Pure function tests — no mocking, no external dependencies. Run with `npm test`.

## Before committing

Run `npm run format` then `npm run check`. The check includes typecheck, lint, format verification, and tests.

## When editing

- Schemas are the contract — change schemas first, then update validation and consolidation to match.
- `installConfigs` and `tools` are optional. Handle missing values with `?? []`.
- Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification), Phase 4 (plugin manifest verification). Phases 2-4 warn on failure, don't block.
- Consolidation is split: collect (no network) → enrich MCP (network, fatal on error) → enrich skills (network, skip on error) → enrich plugins (network, skip on error) → write.
- Website types in `website/src/types.ts` mirror but don't import from `src/consolidate.ts` — keep them in sync manually.

<!-- README.md @ 368cf10f3129fdc3120f156f2e86bc090406cdf8 -->
# AI Registry

> **Preview** — This registry is currently in preview. Data, APIs, and the website may change as we iterate on the concept.

A vendor-neutral, federated trust registry for AI artifacts, hosted at the Eclipse Foundation. Supports [Model Context Prot...
```
