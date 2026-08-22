# DocGuard Real PR Manual Labeling Pack

This file is for human validation of real public GitHub PR candidate cases.

**Important:** this is not model input. It includes audit context such as documentation diffs and docs-after text so a human can assign gold labels. Model/evaluation scripts must use only the explicitly allowed model input fields.

- Source candidates: `data\external\project_case_study\real_pr_candidates_collected_v1.jsonl`
- Records to review: `30`
- Candidate type counts: `{'code_and_docs_changed_needs_manual_validation': 23, 'code_only_needs_manual_validation': 7}`
- Language counts: `{'typescript': 26, 'python': 4}`

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
| `GH-CAND-0001` | https://github.com/ragpark/controltower/pull/14 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `15` | `1` | `needs_manual_review` |
| `GH-CAND-0002` | https://github.com/ragpark/controltower/pull/6 | `typescript` | `code_only_needs_manual_validation` | `11` | `0` | `needs_manual_review` |
| `GH-CAND-0003` | https://github.com/ragpark/controltower/pull/5 | `typescript` | `code_only_needs_manual_validation` | `9` | `0` | `needs_manual_review` |
| `GH-CAND-0004` | https://github.com/ragpark/controltower/pull/4 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `36` | `1` | `needs_manual_review` |
| `GH-CAND-0005` | https://github.com/ragpark/controltower/pull/3 | `typescript` | `code_only_needs_manual_validation` | `5` | `0` | `needs_manual_review` |
| `GH-CAND-0006` | https://github.com/ragpark/controltower/pull/2 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `25` | `5` | `needs_manual_review` |
| `GH-CAND-0007` | https://github.com/d-hinders/Haven-AI/pull/1783 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `13` | `2` | `needs_manual_review` |
| `GH-CAND-0008` | https://github.com/d-hinders/Haven-AI/pull/1782 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `9` | `1` | `needs_manual_review` |
| `GH-CAND-0009` | https://github.com/d-hinders/Haven-AI/pull/1781 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `3` | `1` | `needs_manual_review` |
| `GH-CAND-0010` | https://github.com/d-hinders/Haven-AI/pull/1780 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `18` | `2` | `needs_manual_review` |
| `GH-CAND-0011` | https://github.com/d-hinders/Haven-AI/pull/1778 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `2` | `1` | `needs_manual_review` |
| `GH-CAND-0012` | https://github.com/d-hinders/Haven-AI/pull/1775 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `4` | `1` | `needs_manual_review` |
| `GH-CAND-0013` | https://github.com/d-hinders/Haven-AI/pull/1776 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `7` | `2` | `needs_manual_review` |
| `GH-CAND-0014` | https://github.com/d-hinders/Haven-AI/pull/1770 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `5` | `3` | `needs_manual_review` |
| `GH-CAND-0015` | https://github.com/d-hinders/Haven-AI/pull/1769 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `21` | `2` | `needs_manual_review` |
| `GH-CAND-0016` | https://github.com/d-hinders/Haven-AI/pull/1765 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `10` | `4` | `needs_manual_review` |
| `GH-CAND-0017` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/88 | `typescript` | `code_only_needs_manual_validation` | `5` | `0` | `needs_manual_review` |
| `GH-CAND-0018` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/87 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `9` | `5` | `needs_manual_review` |
| `GH-CAND-0019` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/85 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `15` | `8` | `needs_manual_review` |
| `GH-CAND-0020` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/78 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `19` | `3` | `needs_manual_review` |
| `GH-CAND-0021` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/69 | `typescript` | `code_only_needs_manual_validation` | `16` | `0` | `needs_manual_review` |
| `GH-CAND-0022` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/72 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `7` | `1` | `needs_manual_review` |
| `GH-CAND-0023` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/70 | `typescript` | `code_only_needs_manual_validation` | `1` | `0` | `needs_manual_review` |
| `GH-CAND-0024` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/63 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `4` | `2` | `needs_manual_review` |
| `GH-CAND-0025` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/64 | `typescript` | `code_only_needs_manual_validation` | `1` | `0` | `needs_manual_review` |
| `GH-CAND-0026` | https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/62 | `typescript` | `code_and_docs_changed_needs_manual_validation` | `8` | `2` | `needs_manual_review` |
| `GH-CAND-0027` | https://github.com/torbido-hq/cicerone/pull/112 | `python` | `code_and_docs_changed_needs_manual_validation` | `1` | `2` | `needs_manual_review` |
| `GH-CAND-0028` | https://github.com/torbido-hq/cicerone/pull/107 | `python` | `code_and_docs_changed_needs_manual_validation` | `2` | `2` | `needs_manual_review` |
| `GH-CAND-0029` | https://github.com/torbido-hq/cicerone/pull/97 | `python` | `code_and_docs_changed_needs_manual_validation` | `18` | `5` | `needs_manual_review` |
| `GH-CAND-0030` | https://github.com/torbido-hq/cicerone/pull/101 | `python` | `code_and_docs_changed_needs_manual_validation` | `5` | `5` | `needs_manual_review` |

## Detailed Review Cases

### `GH-CAND-0001`

- Source URL: https://github.com/ragpark/controltower/pull/14
- Repository: `ragpark/controltower`
- PR number: `14`
- PR title: ENG-1102, ENG-1104: Duplicate order diagnostics and resolution
- Language: `typescript`
- Code changed files: `['apps/api/src/app.module.ts', 'apps/api/src/duplicates/dto.ts', 'apps/api/src/duplicates/duplicates.controller.ts', 'apps/api/src/duplicates/duplicates.module.ts', 'apps/api/src/duplicates/duplicates.service.spec.ts', 'apps/api/src/duplicates/duplicates.service.ts', 'apps/api/src/failures/failures.service.spec.ts', 'apps/api/src/failures/failures.service.ts', 'apps/web/src/app/duplicates/page.tsx', 'apps/web/src/components/AppShell.tsx', 'apps/web/src/lib/queries.ts', 'packages/shared-types/src/order.ts', 'services/ingestion/src/__tests__/duplicate-resolution.spec.ts', 'services/ingestion/src/duplicate-resolution.ts', 'services/ingestion/src/index.ts']`
- Docs changed files: `['docs/sdd/control-tower-spec.yaml']`

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
diff --git a/apps/api/src/app.module.ts b/apps/api/src/app.module.ts
--- a/apps/api/src/app.module.ts
+++ b/apps/api/src/app.module.ts
@@ -14,6 +14,7 @@ import { RequestLoggerMiddleware } from './observability/request-logger.middlewa
 import { SourcesModule } from './sources/sources.module';
 import { ImportsModule } from './imports/imports.module';
 import { RulesModule } from './rules/rules.module';
+import { DuplicatesModule } from './duplicates/duplicates.module';
 import { FailuresModule } from './failures/failures.module';
 import { OrdersModule } from './orders/orders.module';
 import { DashboardModule } from './dashboard/dashboard.module';
@@ -33,6 +34,7 @@ import { HealthModule } from './health/health.module';
     AggregatesModule,
     RulesModule,
     FailuresModule,
+    DuplicatesModule,
     ImportsModule,
     SourcesModule,
     OrdersModule,

diff --git a/apps/api/src/duplicates/dto.ts b/apps/api/src/duplicates/dto.ts
--- a/apps/api/src/duplicates/dto.ts
+++ b/apps/api/src/duplicates/dto.ts
@@ -0,0 +1,16 @@
+import { ApiProperty } from '@nestjs/swagger';
+import { ArrayNotEmpty, IsArray, IsString } from 'class-validator';
+
+export class ResolveDuplicatesDto {
+  @ApiProperty({
+    description:
+      'Natural keys of the duplicate groups to resolve, taken from the duplicate report. ' +
+      'Every group is confirmed explicitly — there is no resolve-everything call.',
+    type: [String],
+    example: ['ord-1::9780141036144'],
+  })
+  @IsArray()
+  @ArrayNotEmpty({ message: 'Select at least one duplicate group to resolve.' })
+  @IsString({ each: true })
+  keys!: string[];
+}

diff --git a/apps/api/src/duplicates/duplicates.controller.ts b/apps/api/src/duplicates/duplicates.controller.ts
--- a/apps/api/src/duplicates/duplicates.controller.ts
+++ b/apps/api/src/duplicates/duplicates.controller.ts
@@ -0,0 +1,54 @@
+import { Body, Controller, Get, Header, Post } from '@nestjs/common';
+import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
+import { ApiUser, Role } from '@control-tower/shared-types';
+import { CurrentUser } from '../auth/current-user.decorator';
+import { Roles } from '../auth/roles.decorator';
+import { ResolveDuplicatesDto } from './dto';
+import { DuplicatesService } from './duplicates.service';
+
+@ApiTags('duplicates')
+@ApiBearerAuth()
+@Controller('duplicates')
+export class DuplicatesController {
+  constructor(private readonly duplicates: DuplicatesService) {}
+
+  @Get()
+  @Roles(Role.VIEWER)
+  @ApiOperation({
+    summary: 'Report suspected duplicate order lines',
+    description:
+      'Read-only. Groups order lines whose natural key differs only by letter case and ' +
+      'nominates the most recently imported row as the survivor. Writes nothing.',
+  })
+  report() {
+    return this.duplicates.report();
+  }
+
+  @Get('export')
+  @Roles(Role.VIEWER)
+  @Header('Content-Type', 'text/csv')
+  @Header('Content-Disposition', 'attachment; filename="duplicate-orders.csv"')
+  @ApiOperation({
+    summary: 'Export the duplicate report as CSV',
+    description:
+      'Identifiers, provenance and disposition only. Customer name and email are not ' +
+      'selected by the underlying query, so they cannot appear in the file.',
+  })
+  exportCsv() {
+    return this.duplicates.exportCsv();
+  }
+
+  @Post('resolve')
+  @Roles(Role.OPERATOR)
+  @ApiOperation({
+    summary: 'Remove superseded duplicate order lines',
+    description:
+      'Keeps the most recently imported row in each named group and removes the rest. ' +
+      'History and rule executions are re-pointed to the survivor and the removed rows are ' +
+      'snapshotted into its history before deletion, so the order line keeps its past. ' +
+      'Every group must be named explicitly; there is no resolve-everything call.',
+  })
+  resolve(@Body() dto: ResolveDuplicatesDto, @CurrentUser() user: ApiUser) {
+    return this.duplicates.resolve(dto.keys, user.name);
+  }
+}

diff --git a/apps/api/src/duplicates/duplicates.module.ts b/apps/api/src/duplicates/duplicates.module.ts
--- a/apps/api/src/duplicates/duplicates.module.ts
+++ b/apps/api/src/duplicates/duplicates.module.ts
@@ -0,0 +1,12 @@
+import { Module } from '@nestjs/common';
+import { FailuresModule } from '../failures/failures.module';
+import { DuplicatesController } from './duplicates.controller';
+import { DuplicatesService } from './duplicates.service';
+
+@Module({
+  imports: [FailuresModule],
+  controllers: [DuplicatesController],
+  providers: [DuplicatesService],
+  exports: [DuplicatesService],
+})
+export class DuplicatesModule {}

diff --git a/apps/api/src/duplicates/duplicates.service.spec.ts b/apps/api/src/duplicates/duplicates.service.spec.ts
--- a/apps/api/src/duplicates/duplicates.service.spec.ts
+++ b/apps/api/src/duplicates/duplicates.service.spec.ts
@@ -0,0 +1,278 @@
+import { ConflictException, NotFoundException } from '@nestjs/common';
+import { DuplicatesService } from './duplicates.service';
+
+const d = (iso: string) => new Date(iso);
+
+const order = (over: Partial<Record<string, unknown>> = {}) => ({
+  id: 'id-1',
+  orderNumber: 'ORD-1',
+  productCode: '9780141036144',
+  productName: 'A Book',
+  orderStatus: 'Complete',
+  classification: 'COMPLETED',
+  importedAt: d('2026-08-10T00:00:00Z'),
+  createdAt: d('2026-08-10T00:00:00Z'),
+  updatedAt: d('2026-08-10T00:00:00Z'),
+  sourceFile: 'monday.csv',
+  sourceId: 'src-1',
+  importRunId: 'run-1',
+  ...over,
+});
+
+function build(rows: ReturnType<typeof order>[]) {
+  const tx = {
+    orderHistory: {
+      updateMany: jest.fn().mockResolvedValue({ count: 2 }),
+      createMany: jest.fn().mockResolvedValue({ count: 1 }),
+    },
+    ruleExecution: { updateMany: jest.fn().mockResolvedValue({ count: 3 }) },
+    order: {
+      findMany: jest.fn().mockImplementation(({ where }) => {
+        if (where.id) return Promise.resolve(rows.filter((r) => where.id.in.includes(r.id)));
+        // Revalidation read: case-insensitive match on the group's key.
+        const eq = (a: string, b: string) => a.trim().toLowerCase() === b.trim().toLowerCase();
+        return Promise.resolve(
+          rows.filter(
+            (r) =>
+              eq(r.orderNumber, where.orderNumber.equals) &&
+              eq(r.productCode, where.productCode.equals),
+          ),
+        );
+      }),
+      deleteMany: jest.fn().mockResolvedValue({ count: 1 }),
+    },
+  };
+  const prisma = {
+    order: { findMany: jest.fn().mockResolvedValue(rows) },
+    $transaction: jest
+      .fn()
+      .mockImplementation((fn: (t: typeof tx) => unknown, _opts?: unknown) => fn(tx)),
+  };
+  const audit = { record: jest.fn().mockResolvedValue(undefined) };
+  const failures = {
+    syncAndReclassify: jest
+      .fn()
+      .mockResolvedValue({ linkedOrders: 1, unmatchedOrderNumbers: [], reclassified: 1 }),
+  };
+  const service = new DuplicatesService(
+    prisma as never,
+    audit as never,
+    failures as never,
+  );
+  return { service, prisma, tx, audit, failures };
+}
+
+const caseVariants = [
+  order({ id: 'old', orderNumber: 'ORD-1', importedAt: d('2026-08-10T00:00:00Z'), sourceFile: 'mon.csv' }),
+  order({ id: 'new', orderNumber: 'ord-1', importedAt: d('2026-08-11T00:00:00Z'), sourceFile: 'tue.csv' }),
+];
+
+describe('DuplicatesService.report', () => {
+  it('groups case-only variants and marks the newest import as survivor', async () => {
+    const { service } = build(caseVariants);
+    const report = await service.report();
+
+    expect(report.groupCount).toBe(1);
+    expect(report.removableCount).toBe(1);
+    const [group] = report.groups;
+    expect(group.variantCount).toBe(2);
+    expect(group.variants.find((v) => v.survivor)?.id).toBe('new');
+    // Provenance is what lets an operator see which import introduced which row.
+    expect(group.variants.map((v) => v.sourceFile).sort()).toEqual(['mon.csv', 'tue.csv']);
+  });
+
+  it('writes nothing', async () => {
+    const { service, prisma, audit } = build(caseVariants);
+    await service.report();
+
+    expect(prisma.$transaction).not.toHaveBeenCalled();
+    expect(audit.record).not.toHaveBeenCalled();
+  });
+
+  it('reports nothing for a multi-line order', async () => {
+    const { service } = build([
+      order({ id: 'a', productCode: 'ISBN-1' }),
+      order({ id: 'b', productCode: 'ISBN-2' }),
+    ]);
+
+    const report = await service.report();
+    expect(report.groupCount).toBe(0);
+    expect(report.removableCount).toBe(0);
+  });
+});
+
+describe('DuplicatesService.exportCsv', () => {
+  it('carries no customer name or email', async () => {
+    const { service } = build(caseVariants);
+    const csv = await service.exportCsv();
+
+    expect(csv).not.toMatch(/customer_name|customer_email/i);
+    // The query never selects them, so they cannot be present to leak.
+    expect(csv.split('\n')[0]).toBe(
+      'group_key,order_number,product_code,disposition,classification,orde...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/sdd/control-tower-spec.yaml @ 59d5185bfa6484094089ec879c624a4a2492a0ed -->
# 🟠 DRAFT — HUMAN REVIEW REQUIRED — NOT CERTIFIED
#
# Pearson SDD specification record for the ActiveHub Control Tower.
#
# This file is the machine-readable snapshot of the AHCTL-02 persisted record
# as of 08/12/2026. Content was populated by inheritance from OCT-001
# (mysites@cluepony.com, 2026-08-12) with attribution preserved.
#
# AHCTL-02 is the AUTHORITATIVE specification of record for the Control Tower
# capability. OCT-001 is superseded by reconciliation decision of Paul Coyne
# (accountable owner of AHCTL-02) on 08/12/2026. Reconciliation is UNILATERAL
# and awaits countersignature from the OCT-001 owner and endorsement from an
# authorised Architecture reviewer.
#
# "delivered: true" means code exists and passes its tests in the OCT-001
# codebase. It does NOT mean reviewed, certified or release-ready. BLK-01
# (production authentication disabled) is LIVE and must be handled as an
# incident independently of this specification's progress.

schema_metadata:
  schema_name: pearson-spec-schema
  schema_version: 2.0.0
  status: enterprise_draft_for_human_review
  description: >-
    Machine-readable Pearson SDD specification for the ActiveHub Control
    Tower (AHCTL-02), reconciled as authoritative successor to OCT-001.

specification:

  metadata:
    spec_id: AHCTL-02
    title: ActiveHub Control Tower
    version: 1.1.1-draft
    status: draft
    ratified:
      - delta: SD-01
        ratified_by: paul.coyne@pearson.com
        ratified_at: '2026-08-12'
        evidence: PR #9 merged to main
    pending_owner_confirmation:
      - task: ENG-900
        summary: Condensed definitions restored; BLK-18 remediation awaiting confirmation
    classification: internal
    business_unit: null
    product_area: ActiveHub
    platform: activehub-control-tower
    delivery_context: >-
      Internal platform for order lifecycle visibility across the ActiveHub
      order-to-provision journey, replacing a manually maintained Excel
      dashboard. Software is already delivered under the superseded OCT-001
      identifier and runs on Railway. See reconciliation and exceptions.
    accountable_owner: paul.coyne@pearson.com
    initiating_contributor: paul.coyne@pearson.com
    created_by: paul.coyne@pearson.com
    created_at: '2026-08-12'
    last_updated_by: claude-agent   # ENG-900
    last_updated_at: '2026-08-14'
    certification_status: not_started
    human_review_required: true
    supersedes:
      spec_id: OCT-001
      title: Order Control Tower
      original_owner: mysites@cluepony.com
      supersession_decided_by: paul.coyne@pearson.com
      supersession_decided_at: '2026-08-12'
      supersession_status: unilateral_awaiting_countersignature
      basis: accountable_owner_authority_under_sdd_lifecycle
    ownership_questions:
      - product_owner_not_named
      - technical_owner_not_named
      - business_owner_not_named
      - architecture_governance_not_named
      - privacy_owner_not_named
      - security_owner_not_named
      - service_owner_not_named

  persistence:
    required: true
    repository:
      system: git
      site_or_environment: github.com/ragpark/controltower
      pearson_owned: false
      migration_question: OQ-A2-03
      document_library: docs/sdd
      register: null
    identifiers:
      persistent_record_id: AHCTL-02
      predecessor_record_id: OCT-001
      markdown_file_url: docs/sdd/control-tower-delivery-pack.md
      yaml_file_url: docs/sdd/control-tower-spec.yaml
      evidence_folder_url: null
      contribution_log_url: null
    lifecycle:
      status: draft
      stage: content_populated_awaiting_reconciliation_endorsement
      locked_for_review: false
      locked_by: null
      submitted_version: null
    versioning:
      major_version: 1
      minor_version: 1
      patch_version: 1
      version_history_required: true
      change_summary: >-
        ENG-900 implementation of ratified delta SD-01. Restores the FR, ADR,
        TC, UX journey, component, API, event, data-entity and persona
        definitions that had been condensed out of AHCTL-02, making the record
        self-contained. No requirement is added or changed.
      previous_versions:
        - version: 1.1.0-draft
          summary: >-
            SD-01 spec delta: spec-operations tooling (G-07, ADR-16, ADR-17,
            ENG-900…906), CLAUDE.md registered retroactively, derived blocker
            counts corrected. Ratified by the accountable owner; PR #9 merged.
        - version: 1.0.0-draft
          summary: >-
            Initial AHCTL-02 record. Content inherited from OCT-001 (six merged
            delivery increments) with attribution preserved. Reconciliation
            decision recorded: AHCTL-02 supersedes OCT-001.
    collaboration:
      multi_user_contribution: true
      section_level_ownership_required: true
      unresolved_conflicts:
        - id: CONFLICT-01...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/sdd/control-tower-spec.yaml b/docs/sdd/control-tower-spec.yaml
--- a/docs/sdd/control-tower-spec.yaml
+++ b/docs/sdd/control-tower-spec.yaml
@@ -30,13 +30,39 @@ specification:
   metadata:
     spec_id: AHCTL-02
     title: ActiveHub Control Tower
-    version: 1.1.1-draft
+    version: 1.3.2-draft
     status: draft
     ratified:
       - delta: SD-01
+        summary: Spec-operations tooling
         ratified_by: paul.coyne@pearson.com
         ratified_at: '2026-08-12'
         evidence: PR #9 merged to main
+      - delta: SD-02
+        summary: Team owner directory — FR-20, ADR-18, ENG-1001…1006
+        ratified_by: paul.coyne@pearson.com
+        ratified_at: '2026-08-14'
+        evidence: PR #10 merged to main
+        implementation_still_gated:
+          human_sign_off_required: retention_or_pii_handling_changes
+          sign_off_status: not_obtained
+          deployment_gate: BLK-01
+          note: >-
+            Ratification settles the what. FR-20 introduces a new personal data
+            category, so implementation may not start until sign-off is
+            recorded, and may not reach production while BLK-01 is open.
+      - delta: SD-03
+        summary: Duplicate order diagnostics (DEF-01) and Top Products scoped to Completed — FR-21, FR-22
+        ratified_by: paul.coyne@pearson.com
+        ratified_at: '2026-08-14'
+        evidence: PR #11 merged to main
+        implementation_still_gated:
+          human_sign_off_required: [deduplication_key_changes, database_migrations_affecting_customer_data]
+          sign_off_status: not_obtained
+          note: >-
+            ENG-1103 (Top Products) needs no sign-off and may proceed.
+            ENG-1101 needs the deduplication sign-off. ENG-1104 remains
+            gated_not_authorised pending BLK-11.
     pending_owner_confirmation:
       - task: ENG-900
         summary: Condensed definitions restored; BLK-18 remediation awaiting confirmation
@@ -98,15 +124,37 @@ specification:
       submitted_version: null
     versioning:
       major_version: 1
-      minor_version: 1
-      patch_version: 1
+      minor_version: 3
+      patch_version: 2
       version_history_required: true
       change_summary: >-
-        ENG-900 implementation of ratified delta SD-01. Restores the FR, ADR,
-        TC, UX journey, component, API, event, data-entity and persona
-        definitions that had been condensed out of AHCTL-02, making the record
-        self-contained. No requirement is added or changed.
+        ENG-1102 and ENG-1104 implementation of ratified delta SD-03: duplicate
+        diagnostics and the removal of superseded duplicate order lines,
+        keeping the most recently imported row. Adds one acceptance criterion
+        to ENG-1104 at the owner's direction and records EXC-06, because
+        ENG-1104's BLK-11 precondition is not met.
       previous_versions:
+        - version: 1.3.1-draft
+          summary: >-
+            Record repair. Restored the SD-02 content dropped by the PR #12
+            merge resolution and brought the FR and ADR statuses into step with
+            the ratifications. PR #13.
+        - version: 1.3.0-draft
+          summary: >-
+            SD-03 spec delta: duplicate order diagnostics (DEF-01, FR-21) and
+            Top Products scoped to Completed (FR-22); ENG-1101…1104,
+            TC-27…TC-33. Ratified by the accountable owner; PR #11 merged.
+        - version: 1.2.0-draft
+          summary: >-
+            SD-02 spec delta: team owner directory (FR-20, ADR-18, UX-J06,
+            team_owners), ENG-1001…1006, TC-19…TC-26. Ratified by the
+            accountable owner; PR #10 merged.
+        - version: 1.1.1-draft
+          summary: >-
+            ENG-900 implementation of ratified delta SD-01. Restored the FR,
+            ADR, TC, UX journey, component, API, event, data-entity and persona
+            definitions that had been condensed out of AHCTL-02, making the
+            record self-contained. PR #12 merged.
         - version: 1.1.0-draft
           summary: >-
             SD-01 spec delta: spec-operations tooling (G-07, ADR-16, ADR-17,
@@ -829,7 +877,8 @@ specification:
       - id: FR-20
         title: Team owner directory
         delta: SD-02
-        status: proposed_awaiting_ratification
+        status: ratified
+        ratified_by_delta: SD-02   # PR #10 merged 2026-08-14
         description: >-
           An admin-only Settings page holding the teams that own provisioning
           failures — a stable code, a display name and a contact email address
@@ -882,7 +931,10 @@ specification:
       - id: FR-21
         title: Duplicate order diagnostics
         delta: SD-03
-        status: proposed_awaiting_ratification
+        status: ratified
+        ratified_by_delta: SD-03   # PR #11 merged 2026-08-14
+        delivered: true
+        delivered_at: '2026-08-14'
         description: >-
           A read-only Operations view listing suspected duplicate order lines,
           grouped by the case-insensitive natural key, showing each stored
@@ -912,7 +964,8 @@ specification:
       - id: FR-22
         title: Top Products counts completed orders only
         delta: SD-03
-        status: proposed_awaiting_ratification
+        status: ratified
+        ratified_by_delta: SD-03   # PR #11 merged 2026-08-14
         description: >-
           The Top Products chart on the dashboard counts only orders classified
           COMPLETED. Pending, Placed, Customer Impacted, Exception,
@@ -994,6 +1047,21 @@ specification:
           - Configure connection and column mapping
           - Test, then enable, optionally with a schedule
         surfaces: [settings/sources]
+      # Added by SD-02
+      - id: UX-J06
+        name: Maintain the team owner directory and reach an owner
+        persona: P-04 (maintain) / P-01 (reach)
+        delta: SD-02
+        steps:
+          - Admin opens Settings, Team Owners
+          - Adds or edits a team code, display name and contact email
+          - Operator opens the Provisioning Failures queue
+          - Sees the owning team with its contact address resolved
+          - Reassigns by choosing a team from the directory, not by typing a name
+        states_required:
+          empty: no teams configured yet — the queue still lists failures, with an unresolved-owner indicator
+          error: directory unavailable — the queue degrades to showing the stamped owner name only
+          loading: address resolution must not block the queue rendering
     interaction_requirements:
       - Server-driven grid: pagination, sorting and filtering are round-tripped.
       - Drill-through preserves the active date range as query parameters.
@@ -1276,7 +1344,7 @@ specification:
           decision: >-
             The YAML is the normative specification record. The Markdown
             delivery pack is generated from it and is never hand-edited.
-          status: proposed_awaiting_ratification
+          status: ratified_awaiting_implementation   # SD-01, PR #9 merged 2026-08-12
           rationale: >-
             Two hand-maintained representations of one record always diverge.
             Today the pack holds FR, ADR, TC and UX detail that the YAML does
@@ -1290,7 +1358,7 @@ specification:
           decision: >-
             Specification compliance is enforced mechanically in CI and in
             branch protection, not by convention or by agent instruction.
-          status: proposed_awaiting_ratification
+          status: ratified_awaiting_implementation   # SD-01, PR #9 merged 2026-08-12
           rationale: >-
             CLAUDE.md binds Claude sessions only. It does not bind a different
             tool, a different agent, or a human in a hurry. The reconciliation
@@ -1304,7 +1372,7 @@ specification:
             The team owner directory holds identity only. The routing decision
             stays stamped on the provisioning failure at import time, as a
             stable team code; contact details are resolved for display.
-          status: proposed_awaiting_ratification
+          status: ratified_awaiting_implementation   # SD-02, PR #10 merged 2026-08-14
           delta: SD-02
           extends: ADR-08
           rationale: >-
@@ -1338,7 +1406,34 @@ specification:
 
   data_and_integration:
     inherited_from: OCT-001
-    personal_data_entities: [orders, order_history, audit_logs, saved_views]
+    personal_data_entities: [orders, order_history, audit_logs, saved_views, team_owners]
+    # Added by SD-02
+    new_entities:
+      - name: team_owners
+        delta: SD-02
+        description: Teams that own provisioning failures, with a contact address
+        fields:
+          - { name: code,         type: string, unique: true, note: 'stable key; what provisioning_failures references' }
+          - { name: display_name, type: string }
+          - { name: email,        type: string, pe...
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/sdd/control-tower-spec.yaml @ 9fe04419295523584f8222eae2ac6102857783d2 -->
# 🟠 DRAFT — HUMAN REVIEW REQUIRED — NOT CERTIFIED
#
# Pearson SDD specification record for the ActiveHub Control Tower.
#
# This file is the machine-readable snapshot of the AHCTL-02 persisted record
# as of 08/12/2026. Content was populated by inheritance from OCT-001
# (mysites@cluepony.com, 2026-08-12) with attribution preserved.
#
# AHCTL-02 is the AUTHORITATIVE specification of record for the Control Tower
# capability. OCT-001 is superseded by reconciliation decision of Paul Coyne
# (accountable owner of AHCTL-02) on 08/12/2026. Reconciliation is UNILATERAL
# and awaits countersignature from the OCT-001 owner and endorsement from an
# authorised Architecture reviewer.
#
# "delivered: true" means code exists and passes its tests in the OCT-001
# codebase. It does NOT mean reviewed, certified or release-ready. BLK-01
# (production authentication disabled) is LIVE and must be handled as an
# incident independently of this specification's progress.

schema_metadata:
  schema_name: pearson-spec-schema
  schema_version: 2.0.0
  status: enterprise_draft_for_human_review
  description: >-
    Machine-readable Pearson SDD specification for the ActiveHub Control
    Tower (AHCTL-02), reconciled as authoritative successor to OCT-001.

specification:

  metadata:
    spec_id: AHCTL-02
    title: ActiveHub Control Tower
    version: 1.3.2-draft
    status: draft
    ratified:
      - delta: SD-01
        summary: Spec-operations tooling
        ratified_by: paul.coyne@pearson.com
        ratified_at: '2026-08-12'
        evidence: PR #9 merged to main
      - delta: SD-02
        summary: Team owner directory — FR-20, ADR-18, ENG-1001…1006
        ratified_by: paul.coyne@pearson.com
        ratified_at: '2026-08-14'
        evidence: PR #10 merged to main
        implementation_still_gated:
          human_sign_off_required: retention_or_pii_handling_changes
          sign_off_status: not_obtained
          deployment_gate: BLK-01
          note: >-
            Ratification settles the what. FR-20 introduces a new personal data
            category, so implementation may not start until sign-off is
            recorded, and may not reach production while BLK-01 is open.
      - delta: SD-03
        summary: Duplicate order diagnostics (DEF-01) and Top Products scoped to Completed — FR-21, FR-22
        ratified_by: paul.coyne@pearson.com
        ratified_at: '2026-08-14'
        evidence: PR #11 merged to main
        implementation_still_gated:
          human_sign_off_required: [deduplication_key_changes, database_migrations_affecting_customer_data]
          sign_off_status: not_obtained
          note: >-
            ENG-1103 (Top Products) needs no sign-off and may proceed.
            ENG-1101 needs the deduplication sign-off. ENG-1104 remains
            gated_not_authorised pending BLK-11.
    pending_owner_confirmation:
      - task: ENG-900
        summary: Condensed definitions restored; BLK-18 remediation awaiting confirmation
    classification: internal
    business_unit: null
    product_area: ActiveHub
    platform: activehub-control-tower
    delivery_context: >-
      Internal platform for order lifecycle visibility across the ActiveHub
      order-to-provision journey, replacing a manually maintained Excel
      dashboard. Software is already delivered under the superseded OCT-001
      identifier and runs on Railway. See reconciliation and exceptions.
    accountable_owner: paul.coyne@pearson.com
    initiating_contributor: paul.coyne@pearson.com
    created_by: paul.coyne@pearson.com
    created_at: '2026-08-12'
    last_updated_by: claude-agent   # ENG-900
    last_updated_at: '2026-08-14'
    certification_status: not_started
    human_review_required: true
    supersedes:
      spec_id: OCT-001
      title: Order Control Tower
      original_owner: mysites@cluepony.com
      supersession_decided_by: paul.coyne@pearson.com
      supersession_decided_at: '2026-08-12'
      supersession_status: unilateral_awaiting_countersignature
      basis: accountable_owner_authority_under_sdd_lifecycle
    ownership_questions:
      - product_owner_not_named
      - technical_owner_not_named
      - business_owner_not_named
      - architecture_governance_not_named
      - privacy_owner_not_named
      - security_owner_not_named
      - service_owner_not_named

  persistence:
    required: true
    repository:
      system: git
      site_or_environment: github.com/ragpark/controltower
      pearson_owned: false
      migration_question: OQ-A2-03
      document_library: docs/sdd
      register: null
    identifiers:
      persistent_record_id: AHCTL-02
      predecessor_record_id: OCT-001
      markdown_file_url: docs/sdd/control-tower-delivery-pack.md
      yaml_file_url: docs/sdd/control-tower-spec.yaml
      evidence_folder_url: null
      contribution_log_url: null
    lifecycle:
      status: draft
      stage: co...
```

### `GH-CAND-0002`

- Source URL: https://github.com/ragpark/controltower/pull/6
- Repository: `ragpark/controltower`
- PR number: `6`
- PR title: Show order trend as stacked bars with range-scoped headline metrics
- Language: `typescript`
- Code changed files: `['apps/web/Dockerfile', 'apps/web/package.json', 'apps/web/src/app/page.tsx', 'apps/web/src/app/queues/[queue]/page.tsx', 'apps/web/src/components/OrdersGrid.tsx', 'apps/web/src/components/RangeMetricPills.tsx', 'apps/web/src/components/charts.tsx', 'package-lock.json', 'services/reporting/src/__tests__/summary.spec.ts', 'services/reporting/src/index.ts', 'services/reporting/src/summary.ts']`
- Docs changed files: `[]`

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
diff --git a/apps/web/Dockerfile b/apps/web/Dockerfile
--- a/apps/web/Dockerfile
+++ b/apps/web/Dockerfile
@@ -4,17 +4,22 @@ WORKDIR /repo
 
 COPY package.json package-lock.json* ./
 COPY tsconfig.base.json ./
+# Every workspace the web app depends on must be present before npm install,
+# or the workspace links cannot resolve and the Next build fails on the import.
 COPY packages/shared-types/package.json packages/shared-types/
 COPY packages/ui-components/package.json packages/ui-components/
+COPY services/reporting/package.json services/reporting/
 COPY apps/web/package.json apps/web/
 RUN npm install --workspaces --include-workspace-root --ignore-scripts
 
 COPY packages/shared-types packages/shared-types
 COPY packages/ui-components packages/ui-components
+COPY services/reporting services/reporting
 COPY apps/web apps/web
 
-# shared-types is consumed from dist by its package.json main
-RUN npm run build -w @control-tower/shared-types
+# shared-types and reporting are consumed from dist via their package.json main
+RUN npm run build -w @control-tower/shared-types \
+ && npm run build -w @control-tower/reporting
 
 ARG NEXT_PUBLIC_API_URL=http://localhost:4000
 ARG NEXT_PUBLIC_AUTH_ENABLED=false

diff --git a/apps/web/package.json b/apps/web/package.json
--- a/apps/web/package.json
+++ b/apps/web/package.json
@@ -11,6 +11,7 @@
   "dependencies": {
     "@azure/msal-browser": "^4.0.1",
     "@azure/msal-react": "^3.0.1",
+    "@control-tower/reporting": "1.0.0",
     "@control-tower/shared-types": "1.0.0",
     "@control-tower/ui-components": "1.0.0",
     "@emotion/cache": "^11.14.0",

diff --git a/apps/web/src/app/page.tsx b/apps/web/src/app/page.tsx
--- a/apps/web/src/app/page.tsx
+++ b/apps/web/src/app/page.tsx
@@ -26,6 +26,8 @@ import {
   useTrend,
 } from '@/lib/queries';
 import { BreakdownBar, ChartCard, SourcePie, TrendChart } from '@/components/charts';
+import { buildRangeMetrics, RangeMetricPills } from '@/components/RangeMetricPills';
+import { summariseTrend } from '@control-tower/reporting';
 
 const QUEUE_LINKS: Partial<Record<Classification, string>> = {
   [Classification.PENDING]: '/queues/pending',
@@ -35,16 +37,48 @@ const QUEUE_LINKS: Partial<Record<Classification, string>> = {
   [Classification.EXCEPTION]: '/queues/exceptions',
 };
 
+/** Window covered by each granularity, kept in one place so the chart query
+ *  and the range caption can never disagree. */
+const RANGE_DAYS: Record<TrendGranularity, number> = {
+  daily: 30,
+  weekly: 90,
+  monthly: 365,
+};
+
+const RANGE_LABEL: Record<TrendGranularity, string> = {
+  daily: 'Last 30 days',
+  weekly: 'Last 90 days',
+  monthly: 'Last 12 months',
+};
+
 export default function DashboardPage() {
   const router = useRouter();
   const [granularity, setGranularity] = useState<TrendGranularity>('daily');
   const { data: summary, isLoading: summaryLoading } = useDashboardSummary();
   const { data: byStatus } = useBreakdown('by-status');
   const { data: byProduct } = useBreakdown('by-product');
   const { data: bySource } = useBreakdown('by-source');
-  const { data: trend } = useTrend(granularity, granularity === 'daily' ? 30 : granularity === 'weekly' ? 90 : 365);
+  const {
+    data: trend,
+    isPending: trendPending,
+    isError: trendError,
+  } = useTrend(granularity, RANGE_DAYS[granularity]);
   const { data: health } = useOperationalHealth();
 
+  // Derived from the buckets the chart is rendering, so the pills and the bars
+  // can never tell different stories.
+  const rangeSummary = summariseTrend(trend ?? []);
+  const rangeMetrics = buildRangeMetrics(rangeSummary.total, rangeSummary.byClassification);
+
+  // The window actually queried, not the first/last bucket — a monthly bucket
+  // starts on the 1st, so bucket bounds would understate the current month.
+  const windowFrom = new Date(Date.now() - RANGE_DAYS[granularity] * 86_400_000)
+    .toISOString()
+    .slice(0, 10);
+  const windowTo = new Date().toISOString().slice(0, 10);
+  const rangeCaption = `${RANGE_LABEL[granularity]} · ${windowFrom} to ${windowTo}`;
+  const trendState = trendPending ? 'loading' : trendError ? 'error' : 'ready';
+
   const cards: Array<{ label: string; value: number; classification?: Classification }> = [
     { label: 'Total orders', value: summary?.total ?? 0 },
     { label: 'Completed', value: summary?.byClassification.COMPLETED ?? 0, classification: Classification.COMPLETED },
@@ -81,21 +115,32 @@ export default function DashboardPage() {
 
       <Grid container spacing={2} sx={{ mb: 3 }}>
         <Grid size={{ xs: 12, lg: 8 }}>
-          <ChartCard
-            title="Order trend"
-            height={300}
-          >
+          <ChartCard title="Order trend" height={392}>
             <Tabs
               value={granularity}
               onChange={(_e, v) => setGranularity(v)}
-              sx={{ minHeight: 32, mb: 1, '& .MuiTab-root': { minHeight: 32, py: 0 } }}
+              sx={{ minHeight: 32, '& .MuiTab-root': { minHeight: 32, py: 0 } }}
             >
               <Tab value="daily" label="Daily" />
               <Tab value="weekly" label="Weekly" />
               <Tab value="monthly" label="Monthly" />
             </Tabs>
+            <Box sx={{ my: 1.5 }}>
+              <RangeMetricPills
+                metrics={rangeMetrics}
+                caption={rangeCaption}
+                state={trendState}
+                onSelect={(metric) => {
+                  const href =
+                    metric.classification && QUEUE_LINKS[metric.classification];
+                  // Carry the window through, or the queue would list all
+                  // history and contradict the figure that was clicked.
+                  if (href) router.push(`${href}?dateFrom=${windowFrom}&dateTo=${windowTo}`);
+                }}
+              />
+            </Box>
             <Box sx={{ height: 240 }}>
-              <TrendChart data={trend ?? []} />
+              <TrendChart data={trend ?? []} granularity={granularity} />
             </Box>
           </ChartCard>
         </Grid>

diff --git a/apps/web/src/app/queues/[queue]/page.tsx b/apps/web/src/app/queues/[queue]/page.tsx
--- a/apps/web/src/app/queues/[queue]/page.tsx
+++ b/apps/web/src/app/queues/[queue]/page.tsx
@@ -1,5 +1,5 @@
 'use client';
-import { notFound, useParams } from 'next/navigation';
+import { notFound, useParams, useSearchParams } from 'next/navigation';
 import Box from '@mui/material/Box';
 import { Classification } from '@control-tower/shared-types';
 import { PageHeader } from '@control-tower/ui-components';
@@ -35,13 +35,21 @@ const QUEUES: Record<string, { title: string; subtitle: string; classification:
 
 export default function QueuePage() {
   const params = useParams<{ queue: string }>();
+  // Seeded when arriving from a range-scoped dashboard pill, so the queue shows
+  // the same orders the figure that was clicked counted.
+  const searchParams = useSearchParams();
   const queue = QUEUES[params.queue];
   if (!queue) notFound();
 
   return (
     <Box>
       <PageHeader title={queue.title} subtitle={queue.subtitle} />
-      <OrdersGrid queue={params.queue} classification={queue.classification} />
+      <OrdersGrid
+        queue={params.queue}
+        classification={queue.classification}
+        initialDateFrom={searchParams.get('dateFrom') ?? undefined}
+        initialDateTo={searchParams.get('dateTo') ?? undefined}
+      />
     </Box>
   );
 }

diff --git a/apps/web/src/components/OrdersGrid.tsx b/apps/web/src/components/OrdersGrid.tsx
--- a/apps/web/src/components/OrdersGrid.tsx
+++ b/apps/web/src/components/OrdersGrid.tsx
@@ -46,6 +46,9 @@ export interface OrdersGridProps {
   /** Queue key for saved views; also fixes the classification filter. */
   queue: string;
   classification?: Classification;
+  /** Seeded from the URL when drilling in from a range-scoped dashboard pill. */
+  initialDateFrom?: string;
+  initialDateTo?: string;
 }
 
 /** Licence Manager reconciliation flag — "Not Match" is the actionable state. */
@@ -75,8 +78,15 @@ interface ViewConfig {
  * Server-driven data grid used by every operational queue:
  * search, filter, sort, export, saved views, bulk actions, drill-down.
  */
-export function OrdersGrid({ queue, classification }: OrdersGridProps) {
+export function OrdersGrid({
+  queue,
+  classification,
+  initialDateFrom,
+  initialDateTo,
+}: OrdersGridProps) {
   const openOrder = useAppStore((s) => s.openOrder);
+  const [dateFrom, setDateFrom] = useState(initialDateFrom);
+  const [dateTo, setDateTo] = useState(initialDateTo);
   const [pagination, setPagination] = useState<GridPaginationModel>({ page: 0, pageSize: 25 });
   const [sortModel, setSortModel] = useState<GridSortModel>([
     { field: 'importedAt', sort: 'desc' },
@@ -98,6 +108,8 @@ export function OrdersGrid({ queue, classification }: OrdersGridProps) {
     search: search || undefined,
     classification: classification ?...
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ c69b2aef8beb4eb2743c9162048c0d030ee3866b -->
# Order Control Tower

A production-ready operational platform that replaces the Tableau/ Excel order dashboard:
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
fields in Settings, so the model is not tied to one export forma...
```

Audit context only — docs diff excerpt:

```diff

```

Audit context only — docs after excerpt:

```markdown

```

### `GH-CAND-0003`

- Source URL: https://github.com/ragpark/controltower/pull/5
- Repository: `ragpark/controltower`
- PR number: `5`
- PR title: Make the upload picker follow the selected source, not assume CSV
- Language: `typescript`
- Code changed files: `['apps/api/src/imports/imports.controller.ts', 'apps/api/src/imports/orchestrator.service.ts', 'apps/web/src/app/imports/page.tsx', 'packages/shared-types/src/source.ts', 'services/ingestion/src/__tests__/connectors.spec.ts', 'services/ingestion/src/connectors/connector-registry.ts', 'services/ingestion/src/connectors/connector.ts', 'services/ingestion/src/connectors/csv-upload.connector.ts', 'services/ingestion/src/connectors/email-report.connector.ts']`
- Docs changed files: `[]`

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
diff --git a/apps/api/src/imports/imports.controller.ts b/apps/api/src/imports/imports.controller.ts
--- a/apps/api/src/imports/imports.controller.ts
+++ b/apps/api/src/imports/imports.controller.ts
@@ -65,11 +65,10 @@ export class ImportsController {
     @Body() body: UploadBody,
     @CurrentUser() user: ApiUser,
   ) {
-    if (!file) throw new BadRequestException('A CSV file is required (field name "file")');
-    const name = file.originalname.toLowerCase();
-    if (!name.endsWith('.csv') && !name.endsWith('.txt')) {
-      throw new BadRequestException('Only .csv and .txt files are supported');
-    }
+    if (!file) throw new BadRequestException('A file is required (field name "file")');
+    // Accepted extensions are validated in the orchestrator against the
+    // connector's own declaration — kept in one place so the browser's file
+    // filter and the server's rules cannot drift apart.
     return this.orchestrator.importUpload(
       body.sourceId,
       { filename: file.originalname, content: file.buffer },

diff --git a/apps/api/src/imports/orchestrator.service.ts b/apps/api/src/imports/orchestrator.service.ts
--- a/apps/api/src/imports/orchestrator.service.ts
+++ b/apps/api/src/imports/orchestrator.service.ts
@@ -1,7 +1,8 @@
-import { Injectable, Logger, NotFoundException } from '@nestjs/common';
+import { BadRequestException, Injectable, Logger, NotFoundException } from '@nestjs/common';
 import { ConfigService } from '@nestjs/config';
 import { EventEmitter2 } from '@nestjs/event-emitter';
 import {
+  allowedUploadExtensions,
   changedFields,
   ConnectorRegistry,
   createDefaultConnectorRegistry,
@@ -82,6 +83,23 @@ export class OrchestratorService {
   async importUpload(sourceId: string, file: FetchedFile, actor: string): Promise<ImportRun> {
     const source = await this.prisma.source.findUnique({ where: { id: sourceId } });
     if (!source) throw new NotFoundException('Source not found');
+
+    // Validate against what the connector itself advertises, so the extensions
+    // offered in the browser and those the server accepts cannot disagree.
+    const connector = this.connectors.get(source.type as SourceType);
+    if (!connector.supportsUpload) {
+      throw new BadRequestException(
+        `Source "${source.name}" does not accept uploads — it pulls data on a schedule.`,
+      );
+    }
+    const allowed = allowedUploadExtensions(connector.uploadAccept);
+    const filename = file.filename.toLowerCase();
+    if (allowed.length > 0 && !allowed.some((ext) => filename.endsWith(ext))) {
+      throw new BadRequestException(
+        `"${file.filename}" is not accepted by this source. Allowed: ${allowed.join(', ')}`,
+      );
+    }
+
     return this.importFile(source, file, actor);
   }

diff --git a/apps/web/src/app/imports/page.tsx b/apps/web/src/app/imports/page.tsx
--- a/apps/web/src/app/imports/page.tsx
+++ b/apps/web/src/app/imports/page.tsx
@@ -56,6 +56,13 @@ export default function ImportsPage() {
   );
   const uploadSources = (sources ?? []).filter((s) => uploadableTypes.has(s.type));
 
+  // The file dialog and button follow the selected source's connector, so a
+  // failure report is never presented as a CSV upload.
+  const selectedSource = uploadSources.find((s) => s.id === uploadSourceId);
+  const selectedTypeInfo = (sourceTypes ?? []).find((t) => t.type === selectedSource?.type);
+  const uploadAccept = selectedTypeInfo?.uploadAccept ?? '.csv,.txt,text/csv,text/plain';
+  const uploadNoun = selectedTypeInfo?.uploadLabel ?? 'file';
+
   const columns: GridColDef<ImportRunDto>[] = [
     {
       field: 'startTime',
@@ -90,7 +97,9 @@ export default function ImportsPage() {
       { sourceId: uploadSourceId, file },
       {
         onSuccess: (run) =>
-          setToast(`Imported ${run.successfulRows} rows (${run.failedRows} failed)`),
+          setToast(
+            `Imported ${run.successfulRows} record(s)${run.failedRows ? `, ${run.failedRows} failed` : ''}`,
+          ),
         onError: (error) =>
           setToast(error instanceof Error ? error.message : 'Upload failed'),
       },
@@ -111,7 +120,15 @@ export default function ImportsPage() {
               label="Upload to source"
               value={uploadSourceId}
               onChange={(e) => setUploadSourceId(e.target.value)}
-              sx={{ minWidth: 200 }}
+              helperText={
+                selectedTypeInfo
+                  ? `Accepts ${selectedTypeInfo.uploadAccept
+                      ?.split(',')
+                      .filter((a) => a.startsWith('.'))
+                      .join(' ')}`
+                  : undefined
+              }
+              sx={{ minWidth: 220 }}
             >
               {uploadSources.map((s) => (
                 <MenuItem key={s.id} value={s.id}>
@@ -125,14 +142,14 @@ export default function ImportsPage() {
               disabled={!uploadSourceId || upload.isPending}
               onClick={() => fileInputRef.current?.click()}
             >
-              {upload.isPending ? 'Uploading…' : 'Upload CSV'}
+              {upload.isPending ? 'Uploading…' : `Upload ${uploadNoun}`}
             </Button>
             <input
               ref={fileInputRef}
               type="file"
-              accept=".csv,.txt,text/csv,text/plain"
+              accept={uploadAccept}
               hidden
-              aria-label="CSV file"
+              aria-label={`${uploadNoun} file to upload`}
               onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
             />
           </Stack>

diff --git a/packages/shared-types/src/source.ts b/packages/shared-types/src/source.ts
--- a/packages/shared-types/src/source.ts
+++ b/packages/shared-types/src/source.ts
@@ -61,5 +61,9 @@ export interface SourceTypeInfo {
   label: string;
   supportsSchedule: boolean;
   supportsUpload: boolean;
+  /** `accept` attribute for the file dialog, declared by the connector. */
+  uploadAccept?: string;
+  /** Noun for the upload button, e.g. "CSV" or "report". */
+  uploadLabel?: string;
   configHints: Record<string, string>;
 }

diff --git a/services/ingestion/src/__tests__/connectors.spec.ts b/services/ingestion/src/__tests__/connectors.spec.ts
--- a/services/ingestion/src/__tests__/connectors.spec.ts
+++ b/services/ingestion/src/__tests__/connectors.spec.ts
@@ -5,7 +5,7 @@ import { SourceType } from '@control-tower/shared-types';
 import { createDefaultConnectorRegistry } from '../connectors/connector-registry';
 import { CsvFileConnector } from '../connectors/csv-file.connector';
 import { jsonArrayToCsv } from '../connectors/rest-api.connector';
-import { ConnectorNotImplementedError } from '../connectors/connector';
+import { allowedUploadExtensions, ConnectorNotImplementedError } from '../connectors/connector';
 
 describe('ConnectorRegistry', () => {
   const registry = createDefaultConnectorRegistry();
@@ -33,6 +33,46 @@ describe('ConnectorRegistry', () => {
     expect(await connector.fetch({})).toEqual([]);
   });
 
+  // The upload picker is driven entirely by this metadata, so a connector that
+  // accepts uploads without declaring them would render as a generic "file".
+  it('every upload-capable connector declares what it accepts and its label', () => {
+    const uploadable = registry.listTypes().filter((t) => t.supportsUpload);
+    expect(uploadable.map((t) => t.type).sort()).toEqual(
+      [SourceType.CSV_UPLOAD, SourceType.EMAIL_FAILURE_REPORT].sort(),
+    );
+    for (const type of uploadable) {
+      expect(type.uploadAccept).toBeTruthy();
+      expect(type.uploadLabel).toBeTruthy();
+    }
+  });
+
+  it('the failure report accepts .txt and the CSV source accepts .csv', () => {
+    const byType = new Map(registry.listTypes().map((t) => [t.type, t]));
+    expect(byType.get(SourceType.EMAIL_FAILURE_REPORT)!.uploadAccept).toContain('.txt');
+    expect(byType.get(SourceType.EMAIL_FAILURE_REPORT)!.uploadLabel).toBe('report');
+    expect(byType.get(SourceType.CSV_UPLOAD)!.uploadAccept).toContain('.csv');
+    // tab-delimited exports keep a .txt name; the parser detects the delimiter
+    expect(byType.get(SourceType.CSV_UPLOAD)!.uploadAccept).toContain('.txt');
+  });
+
+  it('non-upload connectors declare no upload metadata', () => {
+    for (const type of registry.listTypes().filter((t) => !t.supportsUpload)) {
+      expect(type.uploadAccept).toBeUndefined();
+    }
+  });
+
+  // The upload endpoint validates against these, so anything advertised in the
+  // browser must be a real extension the server will accept.
+  it('every advertised extension is parseable and non-empty', () => {
+    for (const type of registry.listTypes().filter((t) => t.supportsUpload)) {
+      const extensions = allowedUploadExtensions(type.uploadAccept);
+      expect(extensions.length).toBeGreaterThan(0);
+      for (const ext of extensions) {
+        expect(ext).toMatch(/^\.[a-z0-9]+$/);
+      }
+    }
+  });
+
   it('throws a helpful error...
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ 9968bd57f0e16b51f9361a93b3a4eb7ae4527147 -->
# Order Control Tower

A production-ready operational platform that replaces the Tableau/ Excel order dashboard:
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
fields in Settings, so the model is not tied to one export forma...
```

Audit context only — docs diff excerpt:

```diff

```

Audit context only — docs after excerpt:

```markdown

```

### `GH-CAND-0004`

- Source URL: https://github.com/ragpark/controltower/pull/4
- Repository: `ragpark/controltower`
- PR number: `4`
- PR title: Ingest the daily provisioning failure report and route ownership
- Language: `typescript`
- Code changed files: `['apps/api/prisma/migrations/20260811140000_provisioning_failures/migration.sql', 'apps/api/prisma/schema.prisma', 'apps/api/prisma/seed-data.ts', 'apps/api/prisma/seed.ts', 'apps/api/src/app.module.ts', 'apps/api/src/failures/failures.controller.ts', 'apps/api/src/failures/failures.module.ts', 'apps/api/src/failures/failures.service.spec.ts', 'apps/api/src/failures/failures.service.ts', 'apps/api/src/imports/imports.controller.ts', 'apps/api/src/imports/imports.module.ts', 'apps/api/src/imports/orchestrator.service.ts', 'apps/api/src/orders/orders.controller.ts', 'apps/api/src/orders/orders.service.ts', 'apps/api/src/rules/seed-rules.spec.ts', 'apps/web/src/app/failures/page.tsx', 'apps/web/src/app/imports/page.tsx', 'apps/web/src/components/AppShell.tsx', 'apps/web/src/components/OrderDrawer.tsx', 'apps/web/src/components/OrdersGrid.tsx', 'apps/web/src/lib/queries.ts', 'packages/shared-types/src/enums.ts', 'packages/shared-types/src/failure.ts', 'packages/shared-types/src/index.ts', 'services/ingestion/src/__tests__/connectors.spec.ts', 'services/ingestion/src/__tests__/failure-report-parser.spec.ts', 'services/ingestion/src/connectors/azure-blob.connector.ts', 'services/ingestion/src/connectors/connector-registry.ts', 'services/ingestion/src/connectors/connector.ts', 'services/ingestion/src/connectors/csv-file.connector.ts', 'services/ingestion/src/connectors/csv-upload.connector.ts', 'services/ingestion/src/connectors/email-report.connector.ts', 'services/ingestion/src/connectors/rest-api.connector.ts', 'services/ingestion/src/connectors/stub.connectors.ts', 'services/ingestion/src/failure-report-parser.ts', 'services/ingestion/src/index.ts']`
- Docs changed files: `['sample-data/README.md']`

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
diff --git a/apps/api/prisma/migrations/20260811140000_provisioning_failures/migration.sql b/apps/api/prisma/migrations/20260811140000_provisioning_failures/migration.sql
--- a/apps/api/prisma/migrations/20260811140000_provisioning_failures/migration.sql
+++ b/apps/api/prisma/migrations/20260811140000_provisioning_failures/migration.sql
@@ -0,0 +1,51 @@
+-- Downstream provisioning failures reported by the daily fulfilment email,
+-- joined to orders by order number, with ownership routing for the next step.
+
+-- AlterEnum
+ALTER TYPE "SourceType" ADD VALUE 'EMAIL_FAILURE_REPORT';
+
+-- CreateEnum
+CREATE TYPE "FailureCategory" AS ENUM ('TEP_ACCOUNT_MISSING', 'INVALID_CUSTOMER_DATA', 'DUPLICATE_ORG_MEMBERSHIP', 'LICENCE_CONFIG_ERROR', 'INTEGRATION_FAULT', 'UNCATEGORISED');
+
+-- AlterTable
+ALTER TABLE "orders" ADD COLUMN     "provisioning_category" "FailureCategory",
+                     ADD COLUMN     "provisioning_owner" TEXT,
+                     ADD COLUMN     "provisioning_failed_at" TIMESTAMP(3);
+
+-- CreateTable
+CREATE TABLE "provisioning_failures" (
+    "id" UUID NOT NULL,
+    "order_number" TEXT NOT NULL,
+    "contract_number" TEXT NOT NULL DEFAULT '',
+    "order_date" TIMESTAMP(3),
+    "raw_message" TEXT NOT NULL,
+    "category" "FailureCategory" NOT NULL,
+    "owner" TEXT NOT NULL,
+    "suggested_action" TEXT NOT NULL,
+    "occurrences" INTEGER NOT NULL DEFAULT 1,
+    "first_seen_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
+    "last_seen_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
+    "resolved_at" TIMESTAMP(3),
+    "resolved_by" TEXT,
+    "resolution_note" TEXT,
+    "import_run_id" UUID,
+    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
+    "updated_at" TIMESTAMP(3) NOT NULL,
+
+    CONSTRAINT "provisioning_failures_pkey" PRIMARY KEY ("id")
+);
+
+-- CreateIndex
+CREATE UNIQUE INDEX "provisioning_failures_order_number_contract_number_key" ON "provisioning_failures"("order_number", "contract_number");
+
+-- CreateIndex
+CREATE INDEX "provisioning_failures_category_idx" ON "provisioning_failures"("category");
+
+-- CreateIndex
+CREATE INDEX "provisioning_failures_owner_idx" ON "provisioning_failures"("owner");
+
+-- CreateIndex
+CREATE INDEX "provisioning_failures_resolved_at_idx" ON "provisioning_failures"("resolved_at");
+
+-- CreateIndex
+CREATE INDEX "orders_provisioning_category_idx" ON "orders"("provisioning_category");

diff --git a/apps/api/prisma/schema.prisma b/apps/api/prisma/schema.prisma
--- a/apps/api/prisma/schema.prisma
+++ b/apps/api/prisma/schema.prisma
@@ -15,6 +15,16 @@ enum SourceType {
   SFTP
   AZURE_BLOB
   TABLEAU
+  EMAIL_FAILURE_REPORT
+}
+
+enum FailureCategory {
+  TEP_ACCOUNT_MISSING
+  INVALID_CUSTOMER_DATA
+  DUPLICATE_ORG_MEMBERSHIP
+  LICENCE_CONFIG_ERROR
+  INTEGRATION_FAULT
+  UNCATEGORISED
 }
 
 enum SourceStatus {
@@ -93,6 +103,13 @@ model Order {
   orderState           String?         @map("order_state")
   licenceOrderMatch    String?         @map("licence_order_match")
   licenceIsbnMatch     String?         @map("licence_isbn_match")
+  // Denormalised summary of the latest unresolved provisioning failure for this
+  // order number. Kept on the order so queues, filters and the rule engine can
+  // use it without a join; the provisioning_failures table remains the record
+  // of truth, including history and resolution.
+  provisioningCategory FailureCategory? @map("provisioning_category")
+  provisioningOwner    String?          @map("provisioning_owner")
+  provisioningFailedAt DateTime?        @map("provisioning_failed_at")
   classification       Classification?
   classificationReason String?         @map("classification_reason")
   classifiedAt         DateTime?       @map("classified_at")
@@ -117,6 +134,7 @@ model Order {
   @@index([customerName])
   @@index([customerEmail])
   @@index([orderSource])
+  @@index([provisioningCategory])
   @@index([importedAt])
   @@map("orders")
 }
@@ -170,6 +188,37 @@ model RuleExecution {
   @@map("rule_executions")
 }
 
+/**
+ * A downstream provisioning failure reported by the daily fulfilment email.
+ * Joined to orders by order number — one failure can cover several order lines,
+ * and a failure may arrive before the order itself is imported.
+ */
+model ProvisioningFailure {
+  id              String          @id @default(uuid()) @db.Uuid
+  orderNumber     String          @map("order_number")
+  contractNumber  String          @default("") @map("contract_number")
+  orderDate       DateTime?       @map("order_date")
+  rawMessage      String          @map("raw_message")
+  category        FailureCategory
+  owner           String
+  suggestedAction String          @map("suggested_action")
+  occurrences     Int             @default(1)
+  firstSeenAt     DateTime        @default(now()) @map("first_seen_at")
+  lastSeenAt      DateTime        @default(now()) @map("last_seen_at")
+  resolvedAt      DateTime?       @map("resolved_at")
+  resolvedBy      String?         @map("resolved_by")
+  resolutionNote  String?         @map("resolution_note")
+  importRunId     String?         @map("import_run_id") @db.Uuid
+  createdAt       DateTime        @default(now()) @map("created_at")
+  updatedAt       DateTime        @updatedAt @map("updated_at")
+
+  @@unique([orderNumber, contractNumber])
+  @@index([category])
+  @@index([owner])
+  @@index([resolvedAt])
+  @@map("provisioning_failures")
+}
+
 model AuditLog {
   id         String   @id @default(uuid()) @db.Uuid
   entityType String   @map("entity_type")

diff --git a/apps/api/prisma/seed-data.ts b/apps/api/prisma/seed-data.ts
--- a/apps/api/prisma/seed-data.ts
+++ b/apps/api/prisma/seed-data.ts
@@ -50,6 +50,18 @@ export const CLASSIFICATION_RULES: SeedRule[] = [
     },
     outcome: Classification.CANCELLED,
   },
+  {
+    name: 'Provisioning failed downstream',
+    description:
+      'The fulfilment system reported a provisioning failure for this order — the ' +
+      'customer cannot access the product and a named team owns the next step',
+    priority: 15,
+    strategy: 'field-match',
+    ruleDefinition: {
+      conditions: [{ field: 'provisioningCategory', operator: 'notEmpty' }],
+    },
+    outcome: Classification.CUSTOMER_IMPACTED,
+  },
   {
     name: 'Paid but no licence provisioned',
     description:

diff --git a/apps/api/prisma/seed.ts b/apps/api/prisma/seed.ts
--- a/apps/api/prisma/seed.ts
+++ b/apps/api/prisma/seed.ts
@@ -70,6 +70,16 @@ async function seedSources() {
     },
     update: {},
   });
+  await prisma.source.upsert({
+    where: { name: 'Provisioning failure report' },
+    create: {
+      name: 'Provisioning failure report',
+      type: SourceType.EMAIL_FAILURE_REPORT,
+      enabled: true,
+      configJson: {},
+    },
+    update: {},
+  });
   console.log('Seeded default sources');
 }

diff --git a/apps/api/src/app.module.ts b/apps/api/src/app.module.ts
--- a/apps/api/src/app.module.ts
+++ b/apps/api/src/app.module.ts
@@ -14,6 +14,7 @@ import { RequestLoggerMiddleware } from './observability/request-logger.middlewa
 import { SourcesModule } from './sources/sources.module';
 import { ImportsModule } from './imports/imports.module';
 import { RulesModule } from './rules/rules.module';
+import { FailuresModule } from './failures/failures.module';
 import { OrdersModule } from './orders/orders.module';
 import { DashboardModule } from './dashboard/dashboard.module';
 import { ViewsModule } from './views/views.module';
@@ -31,6 +32,7 @@ import { HealthModule } from './health/health.module';
     AuditModule,
     AggregatesModule,
     RulesModule,
+    FailuresModule,
     ImportsModule,
     SourcesModule,
     OrdersModule,

diff --git a/apps/api/src/failures/failures.controller.ts b/apps/api/src/failures/failures.controller.ts
--- a/apps/api/src/failures/failures.controller.ts
+++ b/apps/api/src/failures/failures.controller.ts
@@ -0,0 +1,108 @@
+import { Body, Controller, Get, Param, ParseUUIDPipe, Post, Query } from '@nestjs/common';
+import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
+import { ApiUser, FailureCategory, Role } from '@control-tower/shared-types';
+import { Transform } from 'class-transformer';
+import {
+  ArrayNotEmpty,
+  IsArray,
+  IsBoolean,
+  IsEnum,
+  IsNotEmpty,
+  IsOptional,
+  IsString,
+  IsUUID,
+  MaxLength,
+} from 'class-validator';
+import { CurrentUser } from '../auth/current-user.decorator';
+import { Roles } from '../auth/roles.decorator';
+import { PaginationQuery } from '../common/pagination.dto';
+import { FailuresService } from './failures.service';
+
+class ListFailuresQuery extends PaginationQuery {
+  @IsOptional()
+  @IsEnum(FailureCategory)
+  category?: FailureCategory;
+
+  @IsOptional()
+  @IsString()
+  owner?: string;
+
+  @IsOptional()
+  @IsString()
+  @MaxLength(200)
+  search?: string;
+
+  // Boolean() on a query string is truthy for any non-empty value, so
+  // ?includeResolved=false would otherwise mean true....
```

Allowed model input — docs before excerpt:

```markdown
<!-- sample-data/README.md @ 746ffd02cc6c9e2cd3c868cbc21a4e120ee1fa38 -->
# Sample data

Both files use the **ActiveHub orders export** schema (BigCommerce orders
reconciled against Licence Manager), which is the format the default column
mapping targets:

| Column | Canonical field |
|---|---|
| `order_source` | `orderSource` (sales channel) |
| `order_id` | `orderNumber` ✱ |
| `Custom Status` | `orderState` |
| `order_status` | `orderStatus` |
| `order_created_date_time` | `orderDate` (`dd/mm/yyyy hh:mm`) |
| `full_name` | `customerName` |
| `email` | `customerEmail` |
| `TEPAccountNumber` | `customerId` |
| `productcode` | `productCode` ✱ (ISBN) |
| `productlongname` | `productName` |
| `LicenceManagerOrderMatch` | `licenceOrderMatch` |
| `LicenceManagerISBNMatch` | `licenceIsbnMatch` |

✱ together these form the deduplication key.

## `activehub_orders_sample.csv` — 22 rows

Exercises every classification outcome:

- **Customer Impacted** — order `Complete` but `LicenceManagerOrderMatch = Not Match`
  (paid, no licence provisioned — the highest-priority operational failure)
- **Investigate Required** — order matched but ISBN did not (wrong product licensed),
  plus a stale `Incomplete` order from June
- **Completed** — complete and matched on both order and ISBN
- **Cancelled** — `Cancelled`, `Refunded` and `Declined` statuses
- **Pending** / **Placed** — `Incomplete`, `Awaiting Payment`, `Processing`, `Shipped`
- **Exception** — a row with neither name nor email
- **Deduplication** — order `137` appears twice with *different* ISBNs, so both
  rows are kept (the key is order + product, not order alone)
- **Rejected row** — order `156` carries `9.78141E+12`, see below
- **Filler rows** — trailing all-empty rows, as produced by Excel

## `activehub_orders_update_sample.csv` — 4 rows

Upload this second. It re-imports three existing orders with changed licence
flags (`Not Match` → `Match`), producing history snapshots and reclassification
out of the Customer Impacted queue, and adds one new order.

## Two hazards this data reproduces deliberately

**Excel-mangled ISBNs.** The real export contained `9.78141E+12` — Excel
converted the ISBN to scientific notation and the trailing digits are gone.
Expanding it would yield `9781410000000` and silently collapse *every* ISBN
sharing that prefix onto one product code, corrupting the deduplication key and
merging unrelated orders. These rows are therefore **rejected** with a message
telling the operator to re-export with the column formatted as text. Fix it at
source: in the export, format the ISBN column as Text, or open the CSV via
Data → From Text/CSV and set the column type to Text rather than double-clicking
the file.

**Sheet padding.** Exports arrive with thousands of empty rows (`,,,,,,`). These
are skipped entirely — they are neither counted in the row total nor reported as
failures, so an import of one real row reads as "1 row" rather than "1 of 2,281
with 2,280 errors".

<!-- README.md @ 746ffd02cc6c9e2cd3c868cbc21a4e120ee1fa38 -->
# Order Control Tower

A production-ready operational platform that replaces the Tableau/ Excel order dashboard:
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
API as libra...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/sample-data/README.md b/sample-data/README.md
--- a/sample-data/README.md
+++ b/sample-data/README.md
@@ -60,3 +60,27 @@ the file.
 are skipped entirely — they are neither counted in the row total nor reported as
 failures, so an import of one real row reads as "1 row" rather than "1 of 2,281
 with 2,280 errors".
+
+## `provisioning_failure_report_sample.txt`
+
+The daily downstream failure email, in its native fixed-width layout — long
+error messages wrap onto indented continuation lines. Upload it against the
+**Provisioning failure report** source from Import History.
+
+Records join to orders on **order number** (one failure can cover several order
+lines), and each is categorised and routed to an owning team:
+
+| Error | Category | Owner |
+|---|---|---|
+| `CUSTOMER_ID or OrgId from TEP is NULL` | TEP account missing | Customer Data |
+| `lastName contains invalid characters` | Invalid customer data | Customer Data |
+| `User already part of another organization` | Duplicate org membership | ActiveHub Support |
+| `autoRenew must be YES or NO` | Licence configuration error | Order Management |
+| `AES sent API fault to middleware` | Integration fault | Platform Engineering |
+
+Anything unmatched routes to **Triage** rather than being dropped.
+
+The report is a snapshot of that day's failures, not a list of everything still
+outstanding, so a failure absent from a later report is **not** treated as
+fixed. Failures close when an operator resolves them, or automatically once
+every order line for that order number reconciles with Licence Manager.
```

Audit context only — docs after excerpt:

```markdown
<!-- sample-data/README.md @ 87307e2181606470d2b6b421f2d93bd5076a2e62 -->
# Sample data

Both files use the **ActiveHub orders export** schema (BigCommerce orders
reconciled against Licence Manager), which is the format the default column
mapping targets:

| Column | Canonical field |
|---|---|
| `order_source` | `orderSource` (sales channel) |
| `order_id` | `orderNumber` ✱ |
| `Custom Status` | `orderState` |
| `order_status` | `orderStatus` |
| `order_created_date_time` | `orderDate` (`dd/mm/yyyy hh:mm`) |
| `full_name` | `customerName` |
| `email` | `customerEmail` |
| `TEPAccountNumber` | `customerId` |
| `productcode` | `productCode` ✱ (ISBN) |
| `productlongname` | `productName` |
| `LicenceManagerOrderMatch` | `licenceOrderMatch` |
| `LicenceManagerISBNMatch` | `licenceIsbnMatch` |

✱ together these form the deduplication key.

## `activehub_orders_sample.csv` — 22 rows

Exercises every classification outcome:

- **Customer Impacted** — order `Complete` but `LicenceManagerOrderMatch = Not Match`
  (paid, no licence provisioned — the highest-priority operational failure)
- **Investigate Required** — order matched but ISBN did not (wrong product licensed),
  plus a stale `Incomplete` order from June
- **Completed** — complete and matched on both order and ISBN
- **Cancelled** — `Cancelled`, `Refunded` and `Declined` statuses
- **Pending** / **Placed** — `Incomplete`, `Awaiting Payment`, `Processing`, `Shipped`
- **Exception** — a row with neither name nor email
- **Deduplication** — order `137` appears twice with *different* ISBNs, so both
  rows are kept (the key is order + product, not order alone)
- **Rejected row** — order `156` carries `9.78141E+12`, see below
- **Filler rows** — trailing all-empty rows, as produced by Excel

## `activehub_orders_update_sample.csv` — 4 rows

Upload this second. It re-imports three existing orders with changed licence
flags (`Not Match` → `Match`), producing history snapshots and reclassification
out of the Customer Impacted queue, and adds one new order.

## Two hazards this data reproduces deliberately

**Excel-mangled ISBNs.** The real export contained `9.78141E+12` — Excel
converted the ISBN to scientific notation and the trailing digits are gone.
Expanding it would yield `9781410000000` and silently collapse *every* ISBN
sharing that prefix onto one product code, corrupting the deduplication key and
merging unrelated orders. These rows are therefore **rejected** with a message
telling the operator to re-export with the column formatted as text. Fix it at
source: in the export, format the ISBN column as Text, or open the CSV via
Data → From Text/CSV and set the column type to Text rather than double-clicking
the file.

**Sheet padding.** Exports arrive with thousands of empty rows (`,,,,,,`). These
are skipped entirely — they are neither counted in the row total nor reported as
failures, so an import of one real row reads as "1 row" rather than "1 of 2,281
with 2,280 errors".

## `provisioning_failure_report_sample.txt`

The daily downstream failure email, in its native fixed-width layout — long
error messages wrap onto indented continuation lines. Upload it against the
**Provisioning failure report** source from Import History.

Records join to orders on **order number** (one failure can cover several order
lines), and each is categorised and routed to an owning team:

| Error | Category | Owner |
|---|---|---|
| `CUSTOMER_ID or OrgId from TEP is NULL` | TEP account missing | Customer Data |
| `lastName contains invalid characters` | Invalid customer data | Customer Data |
| `User already part of another organization` | Duplicate org membership | ActiveHub Support |
| `autoRenew must be YES or NO` | Licence configuration error | Order Management |
| `AES sent API fault to middleware` | Integration fault | Platform Engineering |

Anything unmatched routes to **Triage** rather than being dropped.

The report is a snapshot of that day's failures, not a list of everything still
outstanding, so a failure absent from a later report is **not** treated as
fixed. Failures close when an operator resolves them, or automatically once
every order line for that order number reconciles with Licence Manager.

<!-- README.md @ 87307e2181606470d2b6b421f2d93bd5076a2e62 -->
# Order Control Tower

A production-ready operational platform that replaces the Tableau/ Excel order dashboard:
configurable data-source ingestion, a database-driven classification rule
engine, operational queues, executive dashboards, and full audit/traceability —
built as a modern SaaS-style web application.

| Layer | Tech |
|---|---|
| Frontend | React 19 · Next.js 15 · TypeScript · Material UI · TanStack Query · Zustand · Recharts |
| Backend | Node.js · NestJS 11 · TypeScript · event-driven orchestration |
| Data | PostgreSQL 16 · Prisma ORM |
| Auth | Microsoft Entra ID (OIDC) with RBAC app roles (`admin` / `operator` / `viewer`) |
| Ops | Docker · Docker Compose · Azure Container Apps / App Servic...
```

### `GH-CAND-0005`

- Source URL: https://github.com/ragpark/controltower/pull/3
- Repository: `ragpark/controltower`
- PR number: `3`
- PR title: Detect the CSV delimiter instead of blaming the column mapping
- Language: `typescript`
- Code changed files: `['apps/api/src/imports/orchestrator.service.ts', 'services/ingestion/src/__tests__/csv-parser.spec.ts', 'services/ingestion/src/csv-parser.ts', 'services/ingestion/src/normalizer.ts', 'services/ingestion/src/types.ts']`
- Docs changed files: `[]`

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
diff --git a/apps/api/src/imports/orchestrator.service.ts b/apps/api/src/imports/orchestrator.service.ts
--- a/apps/api/src/imports/orchestrator.service.ts
+++ b/apps/api/src/imports/orchestrator.service.ts
@@ -6,6 +6,7 @@ import {
   ConnectorRegistry,
   createDefaultConnectorRegistry,
   dedupeWithinBatch,
+  describeDelimiter,
   FetchedFile,
   NormalizedOrder,
   parseCsvOrders,
@@ -128,6 +129,17 @@ export class OrchestratorService {
         mapping: config.mapping,
         delimiter: config.delimiter,
       });
+      const configured = config.delimiter || ',';
+      if (parsed.delimiter !== configured) {
+        log.push(
+          logEntry(
+            'warn',
+            `File is ${describeDelimiter(parsed.delimiter)}-separated, not ` +
+              `${describeDelimiter(configured)}-separated — parsed with the detected ` +
+              'delimiter. Update the source\'s "delimiter" setting to silence this.',
+          ),
+        );
+      }
       for (const err of parsed.errors) {
         log.push(logEntry('error', err.message, err.row));
       }

diff --git a/services/ingestion/src/__tests__/csv-parser.spec.ts b/services/ingestion/src/__tests__/csv-parser.spec.ts
--- a/services/ingestion/src/__tests__/csv-parser.spec.ts
+++ b/services/ingestion/src/__tests__/csv-parser.spec.ts
@@ -1,4 +1,4 @@
-import { isBlankRow, parseCsvOrders } from '../csv-parser';
+import { describeDelimiter, detectDelimiter, isBlankRow, parseCsvOrders } from '../csv-parser';
 
 const HEADER =
   'order_source,order_id,Custom Status,order_status,order_created_date_time,full_name,email,TEPAccountNumber,productcode,productlongname,LicenceManagerOrderMatch,LicenceManagerISBNMatch';
@@ -149,7 +149,8 @@ describe('column mapping mismatch', () => {
     const csv = 'colA,colB\n1,2\n';
     const [error] = parseCsvOrders(csv, { mapping: LEGACY_MAPPING }).errors;
     expect(error.message).not.toContain('built-in ActiveHub mapping matches');
-    expect(error.message).toContain('colA, colB');
+    // headers are JSON-quoted so tabs and zero-width characters are visible
+    expect(error.message).toContain('"colA", "colB"');
   });
 
   it('flags a mapping that omits a required field entirely', () => {
@@ -165,6 +166,76 @@ describe('column mapping mismatch', () => {
   });
 });
 
+describe('delimiter detection', () => {
+  const COLUMNS = [
+    'order_source', 'order_id', 'Custom Status', 'order_status',
+    'order_created_date_time', 'full_name', 'email', 'TEPAccountNumber',
+    'productcode', 'productlongname', 'LicenceManagerOrderMatch', 'LicenceManagerISBNMatch',
+  ];
+  const VALUES = [
+    'Big Commerce', '136', 'Order Pending', 'Incomplete', '11/02/2026 13:04',
+    'Alexa Foley', 'a@b.com', '', '9781410000001', 'KS4 Maths', 'Match', 'Match',
+  ];
+  const build = (d: string) => `${COLUMNS.join(d)}\n${VALUES.join(d)}\n`;
+
+  // Excel's "Text"/"Unicode Text" save options emit tabs while keeping a .csv
+  // name; parsed as comma-separated the whole header becomes one column.
+  it.each([
+    ['\t', 'tab'],
+    [';', 'semicolon'],
+    ['|', 'pipe'],
+  ])('imports a %s-separated file even though the source says comma', (delimiter) => {
+    const result = parseCsvOrders(build(delimiter), { delimiter: ',' });
+    expect(result.delimiter).toBe(delimiter);
+    expect(result.errors).toEqual([]);
+    expect(result.orders).toHaveLength(1);
+    expect(result.orders[0]).toMatchObject({
+      orderNumber: '136',
+      productCode: '9781410000001',
+      licenceIsbnMatch: 'Match',
+    });
+  });
+
+  it('keeps the configured delimiter when it already splits the header', () => {
+    const result = parseCsvOrders(build(','), { delimiter: ',' });
+    expect(result.delimiter).toBe(',');
+    expect(result.orders).toHaveLength(1);
+  });
+
+  it('respects an explicitly configured non-comma delimiter', () => {
+    expect(detectDelimiter(build(';'), ';')).toBe(';');
+  });
+
+  it('falls back to the configured delimiter for a single-column file', () => {
+    expect(detectDelimiter('order_id\nA-1\n', ',')).toBe(',');
+  });
+
+  it('handles empty content without throwing', () => {
+    expect(detectDelimiter('', ',')).toBe(',');
+  });
+
+  it('names delimiters in human terms for the import log', () => {
+    expect(describeDelimiter('\t')).toBe('tab');
+    expect(describeDelimiter(',')).toBe('comma');
+    expect(describeDelimiter('^')).toBe('"^"');
+  });
+});
+
+describe('invisible characters in headers', () => {
+  it('matches headers containing zero-width spaces, BOMs and non-breaking spaces', () => {
+    const header =
+      '\uFEFForder_source,\u200Border_id,\u00A0productcode\u200B';
+    const result = parseCsvOrders(`${header}\nBig Commerce,136,9781410000001\n`, {
+      mapping: { orderNumber: 'order_id', productCode: 'productcode' },
+    });
+    expect(result.errors).toEqual([]);
+    expect(result.orders[0]).toMatchObject({
+      orderNumber: '136',
+      productCode: '9781410000001',
+    });
+  });
+});
+
 describe('isBlankRow', () => {
   it('detects all-empty and whitespace-only rows', () => {
     expect(isBlankRow({ a: '', b: '   ' })).toBe(true);

diff --git a/services/ingestion/src/csv-parser.ts b/services/ingestion/src/csv-parser.ts
--- a/services/ingestion/src/csv-parser.ts
+++ b/services/ingestion/src/csv-parser.ts
@@ -1,19 +1,86 @@
 import { parse } from 'csv-parse/sync';
 import { ColumnMapping } from '@control-tower/shared-types';
-import { DEFAULT_MAPPING, normalizeRow } from './normalizer';
+import { DEFAULT_MAPPING, normaliseHeader, normalizeRow } from './normalizer';
 import { ParseResult, RowError } from './types';
 
 export interface CsvParseOptions {
   mapping?: ColumnMapping;
   delimiter?: string;
 }
 
+/** Delimiters seen in the wild from spreadsheet "Save as" variants. */
+export const CANDIDATE_DELIMITERS = [',', '\t', ';', '|'];
+
+const DELIMITER_LABELS: Record<string, string> = {
+  ',': 'comma',
+  '\t': 'tab',
+  ';': 'semicolon',
+  '|': 'pipe',
+};
+
+export const describeDelimiter = (delimiter: string) =>
+  DELIMITER_LABELS[delimiter] ?? JSON.stringify(delimiter);
+
 /** True when every cell in the row is empty — spreadsheet filler, not data. */
 export function isBlankRow(row: Record<string, string>): boolean {
   return Object.values(row).every((value) => (value ?? '').trim() === '');
 }
 
-const normaliseHeader = (value: string) => value.trim().toLowerCase();
+function asText(content: Buffer | string): string {
+  return (typeof content === 'string' ? content : content.toString('utf8')).replace(
+    /^\uFEFF/,
+    '',
+  );
+}
+
+function firstNonEmptyLine(content: Buffer | string): string {
+  for (const line of asText(content).split(/\r?\n/)) {
+    if (line.trim() !== '') return line;
+  }
+  return '';
+}
+
+/**
+ * "Save as CSV" is not a guarantee: Excel's Text and Unicode Text options emit
+ * tab-separated data, and some locales default to semicolons. Parsed with the
+ * wrong delimiter the whole header collapses into one column, which then looks
+ * like a broken column mapping. Prefer the configured delimiter, but when it
+ * yields a single column and another candidate splits the header cleanly, use
+ * that instead.
+ */
+export function detectDelimiter(content: Buffer | string, configured?: string): string {
+  const preferred = configured || ',';
+  const header = firstNonEmptyLine(content);
+  if (!header) return preferred;
+
+  const columnCount = (delimiter: string): number => {
+    try {
+      const [row] = parse(header, {
+        delimiter,
+        bom: true,
+        trim: true,
+        relax_column_count: true,
+        relax_quotes: true,
+      }) as string[][];
+      return row?.length ?? 0;
+    } catch {
+      return 0;
+    }
+  };
+
+  if (columnCount(preferred) > 1) return preferred;
+
+  let best = preferred;
+  let bestCount = 1;
+  for (const candidate of CANDIDATE_DELIMITERS) {
+    const count = columnCount(candidate);
+    if (count > bestCount) {
+      best = candidate;
+      bestCount = count;
+    }
+  }
+  return best;
+}
 
 /**
  * The two fields that form the deduplication key must be mapped to real
@@ -37,25 +104,40 @@ function missingRequiredHeaders(
 /**
  * Builds a single actionable message for a mapping/header mismatch. Without
  * this the same "missing required field" error repeats for every row and never
- * says the real cause: the source's column mapping doesn't fit this file.
+ * says the real cause. Headers are JSON-quoted so tabs, zero-width characters
+ * and stray padding are visible rather than silently rendering as whitespace.
  */
 function mappingMismatchMessage(
   headers: string[],
   mapping: ColumnMapping,
   missing: Array<{ field: string; header: string }>,
+  delimiter: string,
 ): string {
   const expected = missing.map((m) => `"${m.header}" (for ${m.field})`).join(' and ');
+  const found = headers.map((h) => JSON.stringify(h)).join(', ');
   const parts = [
-    `This source's column mapping...
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ 25392aa9ede9e8ef3752d902af669890d790b3f5 -->
# Order Control Tower

A production-ready operational platform that replaces the Tableau/ Excel order dashboard:
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
fields in Settings, so the model is not tied to one export forma...
```

Audit context only — docs diff excerpt:

```diff

```

Audit context only — docs after excerpt:

```markdown

```

### `GH-CAND-0006`

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

### `GH-CAND-0007`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1783
- Repository: `d-hinders/Haven-AI`
- PR number: `1783`
- PR title: chore(release): bump all published packages to 0.1.29-alpha.0
- Language: `typescript`
- Code changed files: `['package-lock.json', 'packages/cli/package.json', 'packages/cli/src/commands.ts', 'packages/connect/package.json', 'packages/connect/src/runtime-manifest.ts', 'packages/connect/src/runtime.ts', 'packages/mcp-server/package.json', 'packages/mcp-server/src/server.ts', 'packages/mcp/package.json', 'packages/mcp/src/server.ts', 'packages/sdk/package.json', 'packages/signer/package.json', 'packages/signer/src/server.ts']`
- Docs changed files: `['docs/operations/mcp-runtime-compatibility.md', 'docs/regulatory/casp-changelog/2026-08-22-1783-release.md']`

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
diff --git a/package-lock.json b/package-lock.json
--- a/package-lock.json
+++ b/package-lock.json
@@ -15075,7 +15075,7 @@
     },
     "packages/cli": {
       "name": "@haven_ai/cli",
-      "version": "0.1.28-alpha.0",
+      "version": "0.1.29-alpha.0",
       "license": "MIT",
       "bin": {
         "haven": "dist/cli.js"
@@ -15196,12 +15196,12 @@
     },
     "packages/connect": {
       "name": "@haven_ai/connect",
-      "version": "0.1.28-alpha.0",
+      "version": "0.1.29-alpha.0",
       "license": "MIT",
       "dependencies": {
-        "@haven_ai/mcp": "0.1.28-alpha.0",
-        "@haven_ai/sdk": "0.1.28-alpha.0",
-        "@haven_ai/signer": "0.1.28-alpha.0",
+        "@haven_ai/mcp": "0.1.29-alpha.0",
+        "@haven_ai/sdk": "0.1.29-alpha.0",
+        "@haven_ai/signer": "0.1.29-alpha.0",
         "ethers": "^6.13.0",
         "yaml": "^2.9.0"
       },
@@ -16222,10 +16222,10 @@
     },
     "packages/mcp": {
       "name": "@haven_ai/mcp",
-      "version": "0.1.28-alpha.0",
+      "version": "0.1.29-alpha.0",
       "license": "MIT",
       "dependencies": {
-        "@haven_ai/sdk": "0.1.28-alpha.0",
+        "@haven_ai/sdk": "0.1.29-alpha.0",
         "@modelcontextprotocol/sdk": "^1.29.0",
         "zod": "^3.25.76"
       },
@@ -16243,7 +16243,7 @@
     },
     "packages/mcp-server": {
       "name": "@haven_ai/mcp-server",
-      "version": "0.1.28-alpha.0",
+      "version": "0.1.29-alpha.0",
       "license": "MIT",
       "dependencies": {
         "@haven_ai/sdk": "*",
@@ -16636,7 +16636,7 @@
     },
     "packages/sdk": {
       "name": "@haven_ai/sdk",
-      "version": "0.1.28-alpha.0",
+      "version": "0.1.29-alpha.0",
       "license": "MIT",
       "dependencies": {
         "ethers": "^6.13.0",
@@ -16762,10 +16762,10 @@
     },
     "packages/signer": {
       "name": "@haven_ai/signer",
-      "version": "0.1.28-alpha.0",
+      "version": "0.1.29-alpha.0",
       "license": "MIT",
       "dependencies": {
-        "@haven_ai/sdk": "0.1.28-alpha.0",
+        "@haven_ai/sdk": "0.1.29-alpha.0",
         "@modelcontextprotocol/sdk": "^1.29.0",
         "viem": "^2.51.0",
         "x402": "^1.2.0",

diff --git a/packages/cli/package.json b/packages/cli/package.json
--- a/packages/cli/package.json
+++ b/packages/cli/package.json
@@ -1,6 +1,6 @@
 {
   "name": "@haven_ai/cli",
-  "version": "0.1.28-alpha.0",
+  "version": "0.1.29-alpha.0",
   "description": "Haven CLI — a terminal-native, scriptable parallel to the dashboard (login, read, and backend-only management).",
   "type": "module",
   "bin": {

diff --git a/packages/cli/src/commands.ts b/packages/cli/src/commands.ts
--- a/packages/cli/src/commands.ts
+++ b/packages/cli/src/commands.ts
@@ -9,7 +9,7 @@ import { toCsv } from './csv.js'
 const DEFAULT_API = 'https://havenbackend-production-8a00.up.railway.app'
 // Self-reported CLI version. Owned by scripts/release-bump.mjs, which rewrites
 // the string literal below on every release — keep it a bare quoted literal.
-export const CLI_VERSION = '0.1.28-alpha.0'
+export const CLI_VERSION = '0.1.29-alpha.0'
 
 export interface RunDeps {
   sessionStore?: SessionStore

diff --git a/packages/connect/package.json b/packages/connect/package.json
--- a/packages/connect/package.json
+++ b/packages/connect/package.json
@@ -1,6 +1,6 @@
 {
   "name": "@haven_ai/connect",
-  "version": "0.1.28-alpha.0",
+  "version": "0.1.29-alpha.0",
   "description": "Haven Connect Agent 2 local connector — generates the agent signing key locally and registers only the public signing address.",
   "engines": {
     "node": ">=22"
@@ -48,9 +48,9 @@
     "directory": "packages/connect"
   },
   "dependencies": {
-    "@haven_ai/mcp": "0.1.28-alpha.0",
-    "@haven_ai/sdk": "0.1.28-alpha.0",
-    "@haven_ai/signer": "0.1.28-alpha.0",
+    "@haven_ai/mcp": "0.1.29-alpha.0",
+    "@haven_ai/sdk": "0.1.29-alpha.0",
+    "@haven_ai/signer": "0.1.29-alpha.0",
     "ethers": "^6.13.0",
     "yaml": "^2.9.0"
   },

diff --git a/packages/connect/src/runtime-manifest.ts b/packages/connect/src/runtime-manifest.ts
--- a/packages/connect/src/runtime-manifest.ts
+++ b/packages/connect/src/runtime-manifest.ts
@@ -12,9 +12,9 @@ export const MCP_RUNTIME_MANIFEST = {
   mcpPackage: '@haven_ai/mcp',
   mcpVersion: MCP_VERSION,
   sdkPackage: '@haven_ai/sdk',
-  sdkVersion: '0.1.28-alpha.0',
+  sdkVersion: '0.1.29-alpha.0',
   signerPackage: '@haven_ai/signer',
-  signerVersion: '0.1.28-alpha.0',
+  signerVersion: '0.1.29-alpha.0',
   // Sourced from the SDK, never a literal (#1161). This field read '20.0.0'
   // while every package's `engines` said `>=24` and the docs said `>=24.0.0`,
   // so the guard that was supposed to enforce the floor waved Node v23 through

diff --git a/packages/connect/src/runtime.ts b/packages/connect/src/runtime.ts
--- a/packages/connect/src/runtime.ts
+++ b/packages/connect/src/runtime.ts
@@ -30,7 +30,7 @@ import { resolveRuntimeByInstalledClientPrompt } from './installed-clients.js'
 import { assertSupportedNodeVersion } from './local-mcp-runtime.js'
 import { MCP_RUNTIME_MANIFEST } from './runtime-manifest.js'
 
-export const CONNECTOR_VERSION = '0.1.28-alpha.0'
+export const CONNECTOR_VERSION = '0.1.29-alpha.0'
 
 export interface ConnectOptions {
   setupToken: string

diff --git a/packages/mcp-server/package.json b/packages/mcp-server/package.json
--- a/packages/mcp-server/package.json
+++ b/packages/mcp-server/package.json
@@ -1,6 +1,6 @@
 {
   "name": "@haven_ai/mcp-server",
-  "version": "0.1.28-alpha.0",
+  "version": "0.1.29-alpha.0",
   "private": true,
   "description": "Hosted, keyless Haven MCP server — constructs and relays payments over Streamable HTTP. Never holds the delegate key; the edge signs.",
   "type": "module",

diff --git a/packages/mcp-server/src/server.ts b/packages/mcp-server/src/server.ts
--- a/packages/mcp-server/src/server.ts
+++ b/packages/mcp-server/src/server.ts
@@ -9,7 +9,7 @@ import {
 } from './tools.js'
 
 export const HOSTED_SERVER_NAME = '@haven_ai/mcp-server'
-export const HOSTED_SERVER_VERSION = '0.1.28-alpha.0'
+export const HOSTED_SERVER_VERSION = '0.1.29-alpha.0'
 
 /**
  * MCP `instructions` — the critical path, surfaced to the model at

diff --git a/packages/mcp/package.json b/packages/mcp/package.json
--- a/packages/mcp/package.json
+++ b/packages/mcp/package.json
@@ -1,6 +1,6 @@
 {
   "name": "@haven_ai/mcp",
-  "version": "0.1.28-alpha.0",
+  "version": "0.1.29-alpha.0",
   "description": "Haven MCP server for local, non-custodial agent payments",
   "engines": {
     "node": ">=22"
@@ -47,7 +47,7 @@
     "directory": "packages/mcp"
   },
   "dependencies": {
-    "@haven_ai/sdk": "0.1.28-alpha.0",
+    "@haven_ai/sdk": "0.1.29-alpha.0",
     "@modelcontextprotocol/sdk": "^1.29.0",
     "zod": "^3.25.76"
   },

diff --git a/packages/mcp/src/server.ts b/packages/mcp/src/server.ts
--- a/packages/mcp/src/server.ts
+++ b/packages/mcp/src/server.ts
@@ -87,7 +87,7 @@ export async function createHavenMcpServer(options: HavenMcpServerOptions = {}):
  * `agent_tool_invocations` rows are always attributed to the right tool.
  */
 export const MCP_NAME = '@haven_ai/mcp'
-export const MCP_VERSION = '0.1.28-alpha.0'
+export const MCP_VERSION = '0.1.29-alpha.0'
 
 /**
  * MCP `instructions` — the critical path, surfaced to the model at

diff --git a/packages/sdk/package.json b/packages/sdk/package.json
--- a/packages/sdk/package.json
+++ b/packages/sdk/package.json
@@ -1,6 +1,6 @@
 {
   "name": "@haven_ai/sdk",
-  "version": "0.1.28-alpha.0",
+  "version": "0.1.29-alpha.0",
   "description": "TypeScript SDK for Haven — agent wallet infrastructure",
   "engines": {
     "node": ">=22"

diff --git a/packages/signer/package.json b/packages/signer/package.json
--- a/packages/signer/package.json
+++ b/packages/signer/package.json
@@ -1,6 +1,6 @@
 {
   "name": "@haven_ai/signer",
-  "version": "0.1.28-alpha.0",
+  "version": "0.1.29-alpha.0",
   "description": "Haven edge signer — holds the delegate key locally and signs payment hashes + x402 headers. Pairs with the hosted, keyless @haven_ai/mcp-server.",
   "engines": {
     "node": ">=22"
@@ -47,7 +47,7 @@
     "directory": "packages/signer"
   },
   "dependencies": {
-    "@haven_ai/sdk": "0.1.28-alpha.0",
+    "@haven_ai/sdk": "0.1.29-alpha.0",
     "@modelcontextprotocol/sdk": "^1.29.0",
     "viem": "^2.51.0",
     "x402": "^1.2.0",

diff --git a/packages/signer/src/server.ts b/packages/signer/src/server.ts
--- a/packages/signer/src/server.ts
+++ b/packages/signer/src/server.ts
@@ -20,7 +20,7 @@ import {
 import { loadHavenIdentity } from './sign-context.js'
 
 export const SIGNER_NAME = '@haven_ai/signer'
-export const SIGNER_VERSION = '0.1.28-alpha.0'
+export const SIGNER_VERSION = '0.1.29-alpha.0'
 
 export interface SignerOptions {
   /** Path to a Haven credential JSON file (delegate_key is read from it). */
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/operations/mcp-runtime-compatibility.md @ b071f44e530501090d97e747b403ea1afc3c3d2a -->
---
owner: "@d-hinders"
status: current
contract: true
covers:
  - packages/mcp/**
  - packages/connect/**
  - packages/signer/**
  - packages/mcp-server/src/tools.ts
  - .github/workflows/publish.yml
last-verified: "2026-08-22" # #1719: the connector resolves its own runtime — the #1672 ladder gains an agent self-report rung (at hint precedence, so it still loses to detection) and an installed-client scan + TTY prompt that populates choices and NEVER selects, skipped entirely under --json / non-TTY; an unrecognised runtime name refuses (runtime_unrecognized) instead of falling through, or loses loudly to a detection; new stable codes runtime_undetermined, runtime_unrecognized, runtime_force_unrecognized, runtime_no_installed_clients, runtime_prompt_aborted (all pre-side-effect, connector-exit only) and runtime_config_unreadable (post-credential, reaches the dashboard, split from the retryable runtime_config_write_failed). No tool, capability, or version-skew surface moves; the Supported Runtime Manifest is unchanged. Prior: #1697: --doctor is per-agent — it enumerates every credential directory and classifies each wired/superseded/retired/orphaned instead of "newest wins", runs the full check set per WIRED agent, and exits non-zero if ANY wired agent fails ANY check; --json gains agents[] (slug/agentId/directory/classification/checks) while the flat checks[] still describes one agent so single-agent installs read unchanged. New identity_match check compares the agent the stored API key authenticates as (GET /machine-payments/agent, read-only) against signer.json's delegate_address — a mismatch fails hard. No tool, capability, or version-skew surface moves. Prior: #1696: connect gains --name <slug> — a NAMED agent writes the #1695 haven-<slug>/haven-signer-<slug> MCP pair, stores credentials at ~/.haven/agents/<slug>/ (unnamed keeps ~/.haven/agents/<agent-uuid>/), and records the slug as server_name in signer-runtime.json/mcp-runtime.json. The slug is validated at the ARGUMENT (before any key is minted or file written) and a taken slug refuses before registration, so a re-run can never orphan an agent or overwrite credentials; "haven"/"haven-signer" and the reserved signer/signer-* family are refused. Omitting --name is byte-identical to today. No tool, capability, or version-skew surface moves; --doctor/--repair stay bare-pair-scoped until #1697. Prior: #1695: every runtime config writer (Cursor/VS Code/Claude Desktop JSON, Codex TOML, Hermes YAML+env, Claude Code CLI) is parametrized on a server-name pair — an optional serverName slug yields haven-<slug>/haven-signer-<slug> entries (Hermes: its own MCP_HAVEN_<SLUG>_API_KEY) that coexist with the bare pair; a writer touches ONLY the pair it owns, which removes the #1569 clobbering class (slugs "signer"/"signer-*" are reserved — the one family whose derived names could collide across pairs). The UNNAMED path is byte-identical to before (pinned by characterization tests) — no wired host changes, no tool, capability, or version-skew surface moves; #1696 wires the --name flag. Prior: #1681: connect gains --tombstone <dir> (retire a credential directory in place: diagnostic wrapper + TOMBSTONE.json; no keys touched, nothing revoked, no token/--runtime) and --doctor reads tombstones in the superseded scan (keys removed => informational retired; key present => the #1688 live-probe verdict unchanged); restart guidance widens to EVERY long-lived host. No tool, capability, or version-skew surface moves. Prior: #1688 re-verify: --doctor gains the superseded_agents check (probes every unselected credential dir with its own key; live ⇒ failing check + revoke repair) and setup completion names superseded agents — diagnostics only, no tool, capability, or version-skew surface moves, and the doctor/repair contract this doc describes stands with one addition it now records. Prior: #1690: x402 expected-context VERSION 3 (payer identity) ships signer-first — SUPPORTED_X402_EXPECTED_VERSIONS widens to [1,2,3] (capability handshake and instructions render the new set automatically, both derived from the constant), the signer refuses another agent's quote naming both identities, and the backend keeps emitting v2 until the operator flips X402_EMIT_PAYER_CONTEXT per environment. The version-skew contract is unchanged in shape: a v3 context on a v1/v2 signer produces the existing machine-readable refusal carrying users to `npx @haven_ai/connect@alpha`. No tool schema moves; the signer tool boundary gains OPTIONAL payer_delegate/payer_agent_id passthrough fields. Prior: #1682: the runtime picker is name-first — the collapsed "AI agent" row is replaced by a flat product-name list, and a new "The picker is name-first" subsection carries the row→modality table, the folded vscode-insiders id, and the OpenClaw row's dependency on a published connect release. Detection precedence, the Node...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/operations/mcp-runtime-compatibility.md b/docs/operations/mcp-runtime-compatibility.md
--- a/docs/operations/mcp-runtime-compatibility.md
+++ b/docs/operations/mcp-runtime-compatibility.md
@@ -8,7 +8,7 @@ covers:
   - packages/signer/**
   - packages/mcp-server/src/tools.ts
   - .github/workflows/publish.yml
-last-verified: "2026-08-22" # #1719: the connector resolves its own runtime — the #1672 ladder gains an agent self-report rung (at hint precedence, so it still loses to detection) and an installed-client scan + TTY prompt that populates choices and NEVER selects, skipped entirely under --json / non-TTY; an unrecognised runtime name refuses (runtime_unrecognized) instead of falling through, or loses loudly to a detection; new stable codes runtime_undetermined, runtime_unrecognized, runtime_force_unrecognized, runtime_no_installed_clients, runtime_prompt_aborted (all pre-side-effect, connector-exit only) and runtime_config_unreadable (post-credential, reaches the dashboard, split from the retryable runtime_config_write_failed). No tool, capability, or version-skew surface moves; the Supported Runtime Manifest is unchanged. Prior: #1697: --doctor is per-agent — it enumerates every credential directory and classifies each wired/superseded/retired/orphaned instead of "newest wins", runs the full check set per WIRED agent, and exits non-zero if ANY wired agent fails ANY check; --json gains agents[] (slug/agentId/directory/classification/checks) while the flat checks[] still describes one agent so single-agent installs read unchanged. New identity_match check compares the agent the stored API key authenticates as (GET /machine-payments/agent, read-only) against signer.json's delegate_address — a mismatch fails hard. No tool, capability, or version-skew surface moves. Prior: #1696: connect gains --name <slug> — a NAMED agent writes the #1695 haven-<slug>/haven-signer-<slug> MCP pair, stores credentials at ~/.haven/agents/<slug>/ (unnamed keeps ~/.haven/agents/<agent-uuid>/), and records the slug as server_name in signer-runtime.json/mcp-runtime.json. The slug is validated at the ARGUMENT (before any key is minted or file written) and a taken slug refuses before registration, so a re-run can never orphan an agent or overwrite credentials; "haven"/"haven-signer" and the reserved signer/signer-* family are refused. Omitting --name is byte-identical to today. No tool, capability, or version-skew surface moves; --doctor/--repair stay bare-pair-scoped until #1697. Prior: #1695: every runtime config writer (Cursor/VS Code/Claude Desktop JSON, Codex TOML, Hermes YAML+env, Claude Code CLI) is parametrized on a server-name pair — an optional serverName slug yields haven-<slug>/haven-signer-<slug> entries (Hermes: its own MCP_HAVEN_<SLUG>_API_KEY) that coexist with the bare pair; a writer touches ONLY the pair it owns, which removes the #1569 clobbering class (slugs "signer"/"signer-*" are reserved — the one family whose derived names could collide across pairs). The UNNAMED path is byte-identical to before (pinned by characterization tests) — no wired host changes, no tool, capability, or version-skew surface moves; #1696 wires the --name flag. Prior: #1681: connect gains --tombstone <dir> (retire a credential directory in place: diagnostic wrapper + TOMBSTONE.json; no keys touched, nothing revoked, no token/--runtime) and --doctor reads tombstones in the superseded scan (keys removed => informational retired; key present => the #1688 live-probe verdict unchanged); restart guidance widens to EVERY long-lived host. No tool, capability, or version-skew surface moves. Prior: #1688 re-verify: --doctor gains the superseded_agents check (probes every unselected credential dir with its own key; live ⇒ failing check + revoke repair) and setup completion names superseded agents — diagnostics only, no tool, capability, or version-skew surface moves, and the doctor/repair contract this doc describes stands with one addition it now records. Prior: #1690: x402 expected-context VERSION 3 (payer identity) ships signer-first — SUPPORTED_X402_EXPECTED_VERSIONS widens to [1,2,3] (capability handshake and instructions render the new set automatically, both derived from the constant), the signer refuses another agent's quote naming both identities, and the backend keeps emitting v2 until the operator flips X402_EMIT_PAYER_CONTEXT per environment. The version-skew contract is unchanged in shape: a v3 context on a v1/v2 signer produces the existing machine-readable refusal carrying users to `npx @haven_ai/connect@alpha`. No tool schema moves; the signer tool boundary gains OPTIONAL payer_delegate/payer_agent_id passthrough fields. Prior: #1682: the runtime picker is name-first — the collapsed "AI agent" row is replaced by a flat product-name list, and a new "The picker is name-first" subsection carries the row→modality table, the folded vscode-insiders id, and the OpenClaw row's dependency on a published connect release. Detection precedence, the Node floor, and every skew/manifest claim re-read against the diff and unchanged. Prior: #1672: runtime selection is detection-first — the setup command drops --runtime on command-path runtimes, detection overrides a contradicting hint (notice printed; --runtime-force escape hatch), and no-detection-no-flag refuses before any side effect; new "Runtime selection is detection-first" section documents it. No manifest, tool, capability, or version-skew surface moves. Prior: Release 0.1.28-alpha.0: the Supported Runtime Manifest table is re-pinned to match packages/connect/src/runtime-manifest.ts. Version strings only — no tool, capability, or version-skew surface moves, and the skew contract paragraphs below re-read against the diff stand unchanged. The bump exists because the #1620 SDK decomposition epic (#1614, #1618, #1619, #1631, #1634, #1636, #1655) rewrote packages/sdk/src/client.ts AFTER 0.1.27-alpha.0 was published, and publish.yml skips versions already on npm — so without it the same version string holds different code on npm and in-repo, and the entries below that document that epic would describe an SDK npm does not yet ship. That epic reduced client.ts from ~2500 lines to a compatibility facade over extracted lifecycle modules, exactly the change class that could move a consumer-visible surface silently, so it was MEASURED rather than assumed: the built dist/index.d.ts diffed against the @haven_ai/sdk@0.1.27-alpha.0 tarball from npm shows 155 top-level declarations with zero added and zero removed, and no changed line in the 227-line type diff that is not a private member or a comment. What moved is which module owns a code path, never what a consumer may call. Prior: #1618 re-verify: the SDK's EIP-3009 x402 funding leg moved out of HavenClient into internal modules (x402-protocol.ts / x402-funding-leg.ts). Behaviour-preserving and INTERNAL — no tool schema, capability, runtime-floor, or version-skew surface moves, and the published set this doc governs is unchanged. This doc was pulled in only because connect's package-smoke test had a comment naming the renamed method; every claim here re-read against the diff stands. Prior: Release 0.1.27-alpha.0: the Supported Runtime Manifest table is re-pinned to match packages/connect/src/runtime-manifest.ts. Version strings only — no tool, capability, or version-skew surface moves, and the skew contract paragraphs below re-read against the diff stand unchanged. The bump exists because #1593, #1595, #1597 and #1598 changed connect, the hosted server and the SDK AFTER 0.1.26-alpha.0 was published, and publish.yml skips versions already on npm — so without it `npx @haven_ai/connect@alpha` keeps resolving to a build with no --doctor, and this table's own #1589/#1587/#1588 entries would document a connector that npm does not yet ship. Prior: #1593: the LOCAL MCP runtime install is hardened like #1586 did the signer's — same honest budget (SIGNER_INSTALL_TIMEOUT_MS, replacing the spurious 120s timeout) and 15s onProgress heartbeats, threaded through installRuntime (integration-proven; the unthreaded-callback mutation fails the test). Setup reliability only — no tool, capability, or version-skew surface moves. Prior: #1591: hosted tool-description prose slimmed ~49% with flow-generic guidance consolidated into the server instructions (sign-by-payment_id, settle shapes, expiry re-run, version-mismatch branch, sweep pointer) — prose only; no tool schema, capability, or version-skew surface moves, and the skew contract paragraphs re-read against the diff stand unchanged. Prior: #1590: haven_get_agent gains spend_authority_readiness (readiness stays as a deprecated same-value alias) — additive field + prose stating the local-signer exclusion; no tool schema, capability, or version-skew surface moves. Prior: #1589: --doctor/--repair documented. Prior: #1588: runtime-neutral next_tool_server/next_tool_name pair documented. Prior: #1587: hosted-topology setup hand...
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/operations/mcp-runtime-compatibility.md @ b3405bfc09b3a1e892d483cf6a8341b3e7ba635f -->
---
owner: "@d-hinders"
status: current
contract: true
covers:
  - packages/mcp/**
  - packages/connect/**
  - packages/signer/**
  - packages/mcp-server/src/tools.ts
  - .github/workflows/publish.yml
last-verified: "2026-08-22" # Release 0.1.29-alpha.0: the Supported Runtime Manifest table is re-pinned to match packages/connect/src/runtime-manifest.ts. Version strings only — no tool, capability, or version-skew surface moves, and the skew contract paragraphs below re-read against the diff stand unchanged. The bump exists because ten commits changed the published packages AFTER 0.1.28-alpha.0 was published (2026-08-21 07:05Z), and publish.yml skips versions already on npm — so the SAME version string currently holds different code on npm and in-repo. The gap is user-visible and was MEASURED, not assumed: the published 0.1.28-alpha.0 tarball contains none of #1672's markers (runtime-force, overrodeHint, "detected; ignoring" — 0 matches each, against 4/3/1 in the local build) nor #1719's, so npx @haven_ai/connect@alpha today resolves to a connector predating detection-first resolution entirely. Everything this doc's #1672/#1682/#1719 entries describe — the detection ladder, the name-first picker's OpenClaw row, the self-report and installed-client rungs, the runtime_* failure vocabulary — reaches users only on this release. Also carried: #1690 (x402 expected-context v3 payer identity), #1688/#1681/#1695/#1696/#1697 (connect named pairs, tombstones, per-agent doctor) and #1756 (SDK sweep confirmation bound). Prior: #1719: the connector resolves its own runtime — the #1672 ladder gains an agent self-report rung (at hint precedence, so it still loses to detection) and an installed-client scan + TTY prompt that populates choices and NEVER selects, skipped entirely under --json / non-TTY; an unrecognised runtime name refuses (runtime_unrecognized) instead of falling through, or loses loudly to a detection; new stable codes runtime_undetermined, runtime_unrecognized, runtime_force_unrecognized, runtime_no_installed_clients, runtime_prompt_aborted (all pre-side-effect, connector-exit only) and runtime_config_unreadable (post-credential, reaches the dashboard, split from the retryable runtime_config_write_failed). No tool, capability, or version-skew surface moves; the Supported Runtime Manifest is unchanged. Prior: #1697: --doctor is per-agent — it enumerates every credential directory and classifies each wired/superseded/retired/orphaned instead of "newest wins", runs the full check set per WIRED agent, and exits non-zero if ANY wired agent fails ANY check; --json gains agents[] (slug/agentId/directory/classification/checks) while the flat checks[] still describes one agent so single-agent installs read unchanged. New identity_match check compares the agent the stored API key authenticates as (GET /machine-payments/agent, read-only) against signer.json's delegate_address — a mismatch fails hard. No tool, capability, or version-skew surface moves. Prior: #1696: connect gains --name <slug> — a NAMED agent writes the #1695 haven-<slug>/haven-signer-<slug> MCP pair, stores credentials at ~/.haven/agents/<slug>/ (unnamed keeps ~/.haven/agents/<agent-uuid>/), and records the slug as server_name in signer-runtime.json/mcp-runtime.json. The slug is validated at the ARGUMENT (before any key is minted or file written) and a taken slug refuses before registration, so a re-run can never orphan an agent or overwrite credentials; "haven"/"haven-signer" and the reserved signer/signer-* family are refused. Omitting --name is byte-identical to today. No tool, capability, or version-skew surface moves; --doctor/--repair stay bare-pair-scoped until #1697. Prior: #1695: every runtime config writer (Cursor/VS Code/Claude Desktop JSON, Codex TOML, Hermes YAML+env, Claude Code CLI) is parametrized on a server-name pair — an optional serverName slug yields haven-<slug>/haven-signer-<slug> entries (Hermes: its own MCP_HAVEN_<SLUG>_API_KEY) that coexist with the bare pair; a writer touches ONLY the pair it owns, which removes the #1569 clobbering class (slugs "signer"/"signer-*" are reserved — the one family whose derived names could collide across pairs). The UNNAMED path is byte-identical to before (pinned by characterization tests) — no wired host changes, no tool, capability, or version-skew surface moves; #1696 wires the --name flag. Prior: #1681: connect gains --tombstone <dir> (retire a credential directory in place: diagnostic wrapper + TOMBSTONE.json; no keys touched, nothing revoked, no token/--runtime) and --doctor reads tombstones in the superseded scan (keys removed => informational retired; key present => the #1688 live-probe verdict unchanged); restart guidance widens to EVERY long-lived host. No tool, capability, or version-skew surface moves. Prior: #1688 re-verify: --doctor gains the superseded_agents check (probes every uns...
```

### `GH-CAND-0008`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1782
- Repository: `d-hinders/Haven-AI`
- PR number: `1782`
- PR title: fix(backend): a no-database test run fails, and says what it skipped after the summary (#1763)
- Language: `typescript`
- Code changed files: `['packages/backend/src/infra/__tests__/db-harness-isolation.test.ts', 'packages/backend/src/infra/__tests__/helpers/__tests__/db-availability.test.ts', 'packages/backend/src/infra/__tests__/helpers/db-availability.ts', 'packages/backend/src/infra/__tests__/helpers/db-harness.ts', 'packages/backend/src/infra/repositories/__tests__/hybrid-signers.test.ts', 'packages/backend/src/infra/repositories/__tests__/uuid-param-22p02.test.ts', 'packages/backend/vitest.config.ts', 'packages/backend/vitest.global-setup.ts', 'packages/backend/vitest.setup.ts']`
- Docs changed files: `['docs/contributing/testing-strategy.md']`

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
diff --git a/packages/backend/src/infra/__tests__/db-harness-isolation.test.ts b/packages/backend/src/infra/__tests__/db-harness-isolation.test.ts
--- a/packages/backend/src/infra/__tests__/db-harness-isolation.test.ts
+++ b/packages/backend/src/infra/__tests__/db-harness-isolation.test.ts
@@ -19,9 +19,14 @@ import { WORKER_SCHEMA, describeDb, initDbHarness } from './helpers/db-harness.j
 const CANARY = `harness_isolation_canary_1562_${WORKER_SCHEMA}`
 
 describeDb('db-harness isolation (#1562)', () => {
-  initDbHarness()
-
   beforeAll(async () => {
+    // #1763: this was a bare `initDbHarness()` at describe-REGISTRATION time —
+    // the un-awaited shape the harness docs warn about (#1555/#1559). A
+    // `describe.skip` body still executes to collect its skipped tests, so on
+    // a machine with no database the un-awaited promise rejected into an
+    // unhandled error and the "skipped" file failed anyway. Awaited in
+    // `beforeAll`, per the documented convention.
+    await initDbHarness()
     await db.query(`CREATE TABLE IF NOT EXISTS public.${CANARY} (id INT)`)
     await db.query(`INSERT INTO public.${CANARY} VALUES (1)`)
   })

diff --git a/packages/backend/src/infra/__tests__/helpers/__tests__/db-availability.test.ts b/packages/backend/src/infra/__tests__/helpers/__tests__/db-availability.test.ts
--- a/packages/backend/src/infra/__tests__/helpers/__tests__/db-availability.test.ts
+++ b/packages/backend/src/infra/__tests__/helpers/__tests__/db-availability.test.ts
@@ -0,0 +1,164 @@
+/**
+ * The guard on the skipping harness (#1763).
+ *
+ * These tests deliberately do NOT use `describeDb`. A guard against "the
+ * real-DB suites skipped and nobody noticed" that itself skipped when there
+ * is no database would be the same defect one level up — which is exactly
+ * the shape this repo keeps producing. Everything here is a pure function
+ * over booleans and strings, so it runs on every machine, with or without
+ * Postgres, in CI and out of it.
+ *
+ * Mutation evidence for each branch is recorded in the pull request for
+ * #1763: flipping any single return value below turns at least one of these
+ * red.
+ */
+import { readFile } from 'node:fs/promises'
+
+import { describe, expect, it } from 'vitest'
+
+import {
+  ciFailureMessage,
+  decideDbMode,
+  DEFAULT_TEST_DATABASE_URL,
+  readDbModeInputs,
+  redactDatabaseUrl,
+  resolveTestDatabaseUrl,
+  SKIP_ACK_ENV,
+  unacknowledgedFailureMessage,
+} from '../db-availability.js'
+
+describe('decideDbMode', () => {
+  it('runs the real-DB suites whenever a database is reachable', () => {
+    for (const ci of [true, false]) {
+      for (const acknowledged of [true, false]) {
+        expect(decideDbMode({ available: true, ci, acknowledged })).toBe('run')
+      }
+    }
+  })
+
+  it('FAILS in CI when the database is unreachable, acknowledged or not', () => {
+    expect(decideDbMode({ available: false, ci: true, acknowledged: false })).toBe('fail-ci')
+    // The acknowledgement is for a human at a terminal. It is not an override,
+    // and a CI job that could set it would be able to green a run that proved
+    // nothing — the outcome epic #1219 exists to prevent.
+    expect(decideDbMode({ available: false, ci: true, acknowledged: true })).toBe('fail-ci')
+  })
+
+  it('FAILS locally by default when the database is unreachable (#1763 inversion)', () => {
+    expect(decideDbMode({ available: false, ci: false, acknowledged: false })).toBe(
+      'fail-unacknowledged',
+    )
+  })
+
+  it('skips locally only when the narrowing is explicitly acknowledged', () => {
+    expect(decideDbMode({ available: false, ci: false, acknowledged: true })).toBe(
+      'skip-acknowledged',
+    )
+  })
+
+  it('never returns a mode that lets an unreachable database pass unremarked', () => {
+    // The property, stated once so a future branch has to satisfy it: with no
+    // database, every mode either fails or is an acknowledged skip. There is
+    // no path to 'run'.
+    for (const ci of [true, false]) {
+      for (const acknowledged of [true, false]) {
+        expect(decideDbMode({ available: false, ci, acknowledged })).not.toBe('run')
+      }
+    }
+  })
+})
+
+describe('readDbModeInputs', () => {
+  it('reads CI as present-and-non-empty, matching the harness it replaced', () => {
+    expect(readDbModeInputs({ CI: 'true' }).ci).toBe(true)
+    expect(readDbModeInputs({ CI: '1' }).ci).toBe(true)
+    expect(readDbModeInputs({}).ci).toBe(false)
+    expect(readDbModeInputs({ CI: '' }).ci).toBe(false)
+  })
+
+  it(`treats only ${SKIP_ACK_ENV}=1 as an acknowledgement`, () => {
+    expect(readDbModeInputs({ [SKIP_ACK_ENV]: '1' }).acknowledged).toBe(true)
+    // Not a truthiness check: a stray 'false' or '0' in a shell profile must
+    // not silently buy a narrowed run.
+    expect(readDbModeInputs({ [SKIP_ACK_ENV]: 'true' }).acknowledged).toBe(false)
+    expect(readDbModeInputs({ [SKIP_ACK_ENV]: '0' }).acknowledged).toBe(false)
+    expect(readDbModeInputs({}).acknowledged).toBe(false)
+  })
+})
+
+describe('resolveTestDatabaseUrl', () => {
+  it('prefers an explicit DATABASE_URL', () => {
+    expect(resolveTestDatabaseUrl({ DATABASE_URL: 'postgres://x@y:1/z' })).toBe(
+      'postgres://x@y:1/z',
+    )
+  })
+
+  it('falls back to the same default vitest.setup.ts applies', () => {
+    expect(resolveTestDatabaseUrl({})).toBe(DEFAULT_TEST_DATABASE_URL)
+  })
+
+  it('vitest.setup.ts IMPORTS that default rather than restating it', async () => {
+    // The assertion above is a tautology on its own (the function against its
+    // own constant) and could never catch the drift that matters: global setup
+    // probes before setup files run, so a second hand-copied literal in
+    // vitest.setup.ts would let the guard report on a host the workers never
+    // connect to. Structural, because the value equality cannot be checked —
+    // importing the setup file here would mutate this worker's env.
+    const setup = await readFile(
+      new URL('../../../../../vitest.setup.ts', import.meta.url),
+      'utf8',
+    )
+    expect(setup).toContain('DEFAULT_TEST_DATABASE_URL')
+    // The negative tripwire matches the LITERAL, not an assignment shape
+    // (review nit). A pattern like /DATABASE_URL \?\?= ['"]postgres:/ pins one
+    // syntax and is walked around by bracket access, `||`, a template literal,
+    // or staging the value through a third variable — a guard against a
+    // literal drifting back that a reformat can dodge is a guard that cannot
+    // fail in most of the cases it was written for. Compared against the
+    // constant rather than a second copy of the string, so this assertion
+    // cannot become the duplication it forbids.
+    expect(setup).not.toContain(DEFAULT_TEST_DATABASE_URL)
+  })
+})
+
+describe('redactDatabaseUrl', () => {
+  it('removes the password before a connection string reaches a log line', () => {
+    const redacted = redactDatabaseUrl('postgres://haven:hunter2@localhost:5432/haven')
+    expect(redacted).not.toContain('hunter2')
+    expect(redacted).toContain('localhost:5432')
+  })
+
+  it('keeps a password-less URL readable', () => {
+    expect(redactDatabaseUrl('postgres://localhost:5432/haven')).toContain('localhost:5432')
+  })
+
+  it('never throws on an unparseable value', () => {
+    expect(redactDatabaseUrl('not a url')).toBe('<unparseable DATABASE_URL>')
+  })
+})
+
+describe('failure messages', () => {
+  it('the CI message still names the epic it protects', () => {
+    expect(ciFailureMessage(DEFAULT_TEST_DATABASE_URL)).toContain('#1219')
+  })
+
+  it('the local message names BOTH ways out, so the error is actionable', () => {
+    const message = unacknowledgedFailureMessage(DEFAULT_TEST_DATABASE_URL)
+    expect(message).toContain('docker compose up -d postgres')
+    expect(message).toContain(SKIP_ACK_ENV)
+  })
+
+  it('the local message warns that a SCOPED run fails too (#1763 review nit 3)', () => {
+    // Global setup runs before collection and cannot see the file selection, so
+    // `vitest run one-pure-unit.test.ts` fails on a database-free machine as
+    // well. Surprising enough to belong in the message rather than only in the
+    // docs — pinned so a future edit cannot quietly drop it.
+    expect(unacknowledgedFailureMessage(DEFAULT_TEST_DATABASE_URL)).toContain('scoped')
+  })
+
+  it('neither message leaks a password', () => {
+    const url = 'postgres://haven:hunter2@localhost:5432/haven'
+    expect(ciFailureMessage(url)).not.toContain('hunter2')
+    expect(unacknowledgedFailureMessage(url)).not.toContain('hunter2')
+  })
+})

diff --git a/packages/backend/src/infra/__tests__/helpers/db-availability.ts b/packages/backend/src/infra/__tests__/helpers/db-availability.ts
--- a/packages/backend/src/infra/__tests__/helpers/db-availability.ts
+++ b/packages/backend/src/infra/__tests__/helpers/db-availability.ts
@@ -0,0 +1,170 @@
+/**
+ * Database availability po...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/contributing/testing-strategy.md @ 3ff1169b56fef0bea0840b1128a28fc6503176e4 -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/backend/src/infra/__tests__/helpers/db-harness.ts
  - packages/backend/vitest.setup.ts
  - scripts/db-mock-ratchet.mjs
  - packages/backend/db-mock-baseline.json
last-verified: "2026-08-19" # resetDb now awaits initDbHarness (the un-awaited-init 42P01/40P01 CI flake); harness section re-read against db-harness.ts, example unchanged and still the preferred shape
---

# Backend testing strategy: the real-database rule

The rule epic #1219 established, written down so it survives the people who
ran it. Without this page the convention lives in the heads of whoever
converted the repositories, and the next contributor reasonably copies the
nearest existing test — which for a while will still be a positional-mock one.

## The rule

> **Data-layer behaviour is proven against a real Postgres database, not
> against mocks.** If an assertion is about what the database does —
> idempotency, locking, constraints, transactional integrity, what a query
> returns — it belongs in a repository test using the real-DB harness.
> Mocking is for collaborators the test does not own (chain RPC, bundlers,
> external HTTP), not for the database.

The reasoning: a mock returning `{rows: [...]}` proves the handler can
consume rows; it cannot show that an `ON CONFLICT` dedupes a replayed
payment, that `FOR UPDATE` serialises two concurrent grant activations, or
that a `withTransaction` block rolls back. Those are the guarantees money
rests on, and for a long time they were the least-tested code in the backend
— 0.06 test-to-source ratio in `infra/repositories/` against 2.57 in
`routes/` when the epic's survey ran.

## The layer map

| Assertion is about… | Belongs in… | Database access |
|---|---|---|
| What Postgres does: dedup, locks, constraints, rollback, what a query returns | a repository test (`src/infra/repositories/__tests__/`) | **real**, via the harness |
| What the handler does: auth, validation, rail resolution, status codes, response shape | a route test (`src/routes/__tests__/`) | smallest possible stub — or real rows via the harness when data must exist |
| A collaborator the test does not own: chain RPC, bundler, external HTTP, signer | either | **mock** — this is what mocking is for |

A route test on a real database is fine and often clearer than a stub. The
rule is against *positional mocking* — `mockResolvedValueOnce` chains that
encode query order — not against mocking as such.

## Using the harness

`packages/backend/src/infra/__tests__/helpers/db-harness.ts`. One Postgres
schema per vitest worker (`test_w<id>`), bound through the connection string
before `config.ts` reads it, so even module-level `pool` imports resolve into
the worker schema. Migrations apply once per worker (idempotently — cheap on
re-entry); `resetDb()` truncates between tests — and **awaits harness init
itself** first, so a file that calls `initDbHarness()` without awaiting it (or
skips it entirely) still cannot race its own worker's migration DDL. That
guarantee exists because the #1555/#1559 outbound files DID call it bare at
describe-registration time, and whenever a new migration had to apply, their
first tests ran concurrently with the DDL — the intermittent 42P01/40P01 CI
failures of 2026-08-19. Prefer the explicit `beforeAll` await below anyway; it
says what happens. Locally the harness needs
`docker compose up -d postgres`; without a database the suites skip locally
and **fail in CI** — a green run that skipped every DB test would defeat the
point.

```ts
import db from '../../../db.js'
import { describeDb, initDbHarness, resetDb } from '../../__tests__/helpers/db-harness.js'
import { myRepositoryFunction } from '../my-repository.js'

describeDb('my-repository', () => {
  beforeAll(async () => { await initDbHarness() })
  beforeEach(async () => { await resetDb() })

  it('a replayed insert dedupes — the real ON CONFLICT, twice', async () => {
    await myRepositoryFunction(input)
    await myRepositoryFunction(input) // the second write is the test
    const rows = await db.query(`SELECT COUNT(*)::int AS n FROM my_table`)
    expect(rows.rows[0].n).toBe(1)
  })
})
```

Conventions the conversions settled: row builders stay **local to the test
file** (the harness is deliberately domain-free) and get promoted only when a
second file needs the same shape; seed only the parent rows the foreign keys
genuinely require; exercise every guard on **both** sides — the row that must
transition and the row that must not. The reference conversion is
`delegation-budgets.test.ts` (#1221); the concurrency patterns (claim CAS,
`FOR UPDATE` serialisation with two live transactions) are in
`payment-intents.test.ts` and `agent-connection-setups.test.ts`.

## The ratchet

`npm run lint:db-mocks` (`scripts/db-mock-ratchet.mjs`, blocking in
`backend_checks`) counts `vi.mock('…/db.js')` occurrences and
`moc...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/contributing/testing-strategy.md b/docs/contributing/testing-strategy.md
--- a/docs/contributing/testing-strategy.md
+++ b/docs/contributing/testing-strategy.md
@@ -3,10 +3,12 @@ owner: "@d-hinders"
 status: current
 covers:
   - packages/backend/src/infra/__tests__/helpers/db-harness.ts
+  - packages/backend/src/infra/__tests__/helpers/db-availability.ts
   - packages/backend/vitest.setup.ts
+  - packages/backend/vitest.global-setup.ts
   - scripts/db-mock-ratchet.mjs
   - packages/backend/db-mock-baseline.json
-last-verified: "2026-08-19" # resetDb now awaits initDbHarness (the un-awaited-init 42P01/40P01 CI flake); harness section re-read against db-harness.ts, example unchanged and still the preferred shape
+last-verified: "2026-08-22" # #1763: the no-database section is rewritten — the local default inverts to failing, HAVEN_SKIP_DB_TESTS=1 acknowledges a narrowed run, and the verdict prints after vitest's summary; harness section re-read against db-harness.ts, the beforeAll example unchanged and still preferred. Prior: resetDb now awaits initDbHarness (the un-awaited-init 42P01/40P01 CI flake); harness section re-read against db-harness.ts, example unchanged and still the preferred shape
 ---
 
 # Backend testing strategy: the real-database rule
@@ -58,10 +60,45 @@ guarantee exists because the #1555/#1559 outbound files DID call it bare at
 describe-registration time, and whenever a new migration had to apply, their
 first tests ran concurrently with the DDL — the intermittent 42P01/40P01 CI
 failures of 2026-08-19. Prefer the explicit `beforeAll` await below anyway; it
-says what happens. Locally the harness needs
-`docker compose up -d postgres`; without a database the suites skip locally
-and **fail in CI** — a green run that skipped every DB test would defeat the
-point.
+says what happens.
+
+### When there is no database (#1763)
+
+The harness needs `docker compose up -d postgres`. Without one, the backend
+run **fails** — in CI and, since #1763, locally too:
+
+| database | `CI` | `HAVEN_SKIP_DB_TESTS=1` | outcome |
+|---|---|---|---|
+| up | — | — | real-DB suites run; the run closes with a one-line confirmation |
+| down | yes | ignored | run fails (unchanged since #1220) |
+| down | no | no | **run fails before collection** with both remedies named |
+| down | no | yes | suites skip; the run closes with a banner naming how many real-DB files did not run |
+
+The local default inverted because the previous shape — one `console.warn` at
+import time, then exit 0 — put the only signal hundreds of lines above a green
+summary. Nobody scrolls back, and on 2026-08-21 an agent reported a "passing"
+run that had skipped every real-DB suite. A skipped data layer is now
+something you *say* you accept (one env var, named in the error), not
+something a probe timeout decides for you. The acknowledgement is deliberately
+powerless in CI: it is a statement by a human at a terminal, not an override.
+
+Two consequences worth knowing before you meet them:
+
+- **It fires on scoped runs too.** The check runs before collection, so it
+  cannot know your file selection — `vitest run one-pure-unit.test.ts` fails on
+  a database-free machine exactly like a full run. Export
+  `HAVEN_SKIP_DB_TESTS=1` in your shell once if you iterate that way.
+- **`npm run quality` at the repo root includes the backend leg**, so a
+  frontend-only contributor with no Postgres now hits this. That is the trade
+  #1763 accepted: the alternative is a run that reports green having proven
+  nothing about the data layer. The error text names both remedies.
+
+The policy is one pure function, `decideDbMode` in
+`src/infra/__tests__/helpers/db-availability.ts`, pinned by ordinary mocked
+tests that need no database — a guard against silent skipping must not itself
+skip silently. `vitest.global-setup.ts` owns the run-level verdict: it probes
+once before collection and prints the closing line *after* vitest's summary,
+which per-file harness state cannot do.
 
 ```ts
 import db from '../../../db.js'
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/contributing/testing-strategy.md @ 87a86c38a68f5cfdcbf4688cdcc014b1115cbe4f -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/backend/src/infra/__tests__/helpers/db-harness.ts
  - packages/backend/src/infra/__tests__/helpers/db-availability.ts
  - packages/backend/vitest.setup.ts
  - packages/backend/vitest.global-setup.ts
  - scripts/db-mock-ratchet.mjs
  - packages/backend/db-mock-baseline.json
last-verified: "2026-08-22" # #1763: the no-database section is rewritten — the local default inverts to failing, HAVEN_SKIP_DB_TESTS=1 acknowledges a narrowed run, and the verdict prints after vitest's summary; harness section re-read against db-harness.ts, the beforeAll example unchanged and still preferred. Prior: resetDb now awaits initDbHarness (the un-awaited-init 42P01/40P01 CI flake); harness section re-read against db-harness.ts, example unchanged and still the preferred shape
---

# Backend testing strategy: the real-database rule

The rule epic #1219 established, written down so it survives the people who
ran it. Without this page the convention lives in the heads of whoever
converted the repositories, and the next contributor reasonably copies the
nearest existing test — which for a while will still be a positional-mock one.

## The rule

> **Data-layer behaviour is proven against a real Postgres database, not
> against mocks.** If an assertion is about what the database does —
> idempotency, locking, constraints, transactional integrity, what a query
> returns — it belongs in a repository test using the real-DB harness.
> Mocking is for collaborators the test does not own (chain RPC, bundlers,
> external HTTP), not for the database.

The reasoning: a mock returning `{rows: [...]}` proves the handler can
consume rows; it cannot show that an `ON CONFLICT` dedupes a replayed
payment, that `FOR UPDATE` serialises two concurrent grant activations, or
that a `withTransaction` block rolls back. Those are the guarantees money
rests on, and for a long time they were the least-tested code in the backend
— 0.06 test-to-source ratio in `infra/repositories/` against 2.57 in
`routes/` when the epic's survey ran.

## The layer map

| Assertion is about… | Belongs in… | Database access |
|---|---|---|
| What Postgres does: dedup, locks, constraints, rollback, what a query returns | a repository test (`src/infra/repositories/__tests__/`) | **real**, via the harness |
| What the handler does: auth, validation, rail resolution, status codes, response shape | a route test (`src/routes/__tests__/`) | smallest possible stub — or real rows via the harness when data must exist |
| A collaborator the test does not own: chain RPC, bundler, external HTTP, signer | either | **mock** — this is what mocking is for |

A route test on a real database is fine and often clearer than a stub. The
rule is against *positional mocking* — `mockResolvedValueOnce` chains that
encode query order — not against mocking as such.

## Using the harness

`packages/backend/src/infra/__tests__/helpers/db-harness.ts`. One Postgres
schema per vitest worker (`test_w<id>`), bound through the connection string
before `config.ts` reads it, so even module-level `pool` imports resolve into
the worker schema. Migrations apply once per worker (idempotently — cheap on
re-entry); `resetDb()` truncates between tests — and **awaits harness init
itself** first, so a file that calls `initDbHarness()` without awaiting it (or
skips it entirely) still cannot race its own worker's migration DDL. That
guarantee exists because the #1555/#1559 outbound files DID call it bare at
describe-registration time, and whenever a new migration had to apply, their
first tests ran concurrently with the DDL — the intermittent 42P01/40P01 CI
failures of 2026-08-19. Prefer the explicit `beforeAll` await below anyway; it
says what happens.

### When there is no database (#1763)

The harness needs `docker compose up -d postgres`. Without one, the backend
run **fails** — in CI and, since #1763, locally too:

| database | `CI` | `HAVEN_SKIP_DB_TESTS=1` | outcome |
|---|---|---|---|
| up | — | — | real-DB suites run; the run closes with a one-line confirmation |
| down | yes | ignored | run fails (unchanged since #1220) |
| down | no | no | **run fails before collection** with both remedies named |
| down | no | yes | suites skip; the run closes with a banner naming how many real-DB files did not run |

The local default inverted because the previous shape — one `console.warn` at
import time, then exit 0 — put the only signal hundreds of lines above a green
summary. Nobody scrolls back, and on 2026-08-21 an agent reported a "passing"
run that had skipped every real-DB suite. A skipped data layer is now
something you *say* you accept (one env var, named in the error), not
something a probe timeout decides for you. The acknowledgement is deliberately
powerless in CI: it is a statement by a human at a terminal, not an override.

Two consequences worth knowing before you...
```

### `GH-CAND-0009`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1781
- Repository: `d-hinders/Haven-AI`
- PR number: `1781`
- PR title: test(frontend): anchor the mobile-shell guards against the viewport (#1779)
- Language: `typescript`
- Code changed files: `['packages/frontend/e2e/fixtures/haven-api.ts', 'packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts', 'packages/frontend/e2e/navigation.mobile.spec.ts']`
- Docs changed files: `['docs/contributing/ship-playbooks/frontend.md']`

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
diff --git a/packages/frontend/e2e/fixtures/haven-api.ts b/packages/frontend/e2e/fixtures/haven-api.ts
--- a/packages/frontend/e2e/fixtures/haven-api.ts
+++ b/packages/frontend/e2e/fixtures/haven-api.ts
@@ -560,6 +560,37 @@ export async function dismissMobileSidebar(page: Page) {
  * page BEHIND the dialog — still a real assertion, but not a check on the
  * dialog's own layout. Filed as #1773 rather than widened here: it wants its
  * own selector, its own call-site changes and its own mutation proof.
+ *
+ * ## The viewport-absolute fields, and why they are REPORTED and not asserted
+ *
+ * `viewportWidth` / `contentLeft` / `contentRight` measure the content region
+ * against the VIEWPORT rather than against itself (#1779). Both overflow
+ * metrics above compare a box to another box — `scrollWidth` to `clientWidth`,
+ * of the same element — so they are invariant under any transformation that
+ * moves the whole shell. Measured: swapping the mobile toggle's `fixed` for
+ * `relative` puts it in flow as a 32px flex item, `<main>` goes from
+ * `left 0, width 393` to `left 32, width 361`, and BOTH ratios are unchanged
+ * (`361 - 361 = 0`, exactly as `393 - 393 = 0` was). The whole app shell
+ * displaced 32px and every relative reading held. That is a property of the
+ * reference frame, not of how the assertion was phrased — no rewording of a
+ * "A relative to B" check can see A and B move together.
+ *
+ * These three are deliberately NOT asserted here, and that is the design rather
+ * than an omission. This helper has three classes of caller with three
+ * different CORRECT answers: below `lg` the drawer is `fixed`, so `<main>`
+ * spans the full viewport (`0 → innerWidth`); on desktop the drawer is
+ * `lg:static` and legitimately occupies the first 240px, so `contentLeft` is
+ * 240; and `/login` is outside the shell entirely and has no content region at
+ * all. A single anchor baked in here would have to be loose enough to hold for
+ * all three, which is another way of saying it would hold for the defect too.
+ *
+ * So the numbers come from here and the CONTRACT is asserted where it is known:
+ * `navigation.mobile.spec.ts` pins the mobile shell to `0 → innerWidth`. That
+ * split is also why `mobile-nav-layering.mobile.spec.ts` computes its own
+ * anchor instead of calling this helper — one shared anchor that every mobile
+ * suite trusts would be a single reference frame again, and a single reference
+ * frame is the thing #1779 is about. Two independent measurements can disagree;
+ * one cannot.
  */
 export async function expectNoHorizontalOverflow(page: Page) {
   return page.evaluate(() => {
@@ -572,6 +603,14 @@ export async function expectNoHorizontalOverflow(page: Page) {
     const main = document.getElementById('main-content')
     const contentScrollWidth = main ? main.scrollWidth : null
     const contentClientWidth = main ? main.clientWidth : null
+
+    // Where the content region sits IN THE VIEWPORT. Nothing above this line
+    // can see the shell move, because everything above compares a box to
+    // itself. `getBoundingClientRect` is viewport-relative by definition, so
+    // these are the anchored readings — see the JSDoc for why they are reported
+    // rather than asserted here (#1779).
+    const contentBox = main ? main.getBoundingClientRect() : null
+    const viewportWidth = window.innerWidth
     // Presence is NOT enough: an attached but unlaid-out `<main>` measures
     // `0 - 0 = 0`, which reads as "fits". Require a real box, so the no-op
     // path fails the `contentRegionFound` assertion instead of passing.
@@ -599,6 +638,11 @@ export async function expectNoHorizontalOverflow(page: Page) {
       contentOverflowBy,
       contentOverflows,
       hasOverflow: documentOverflows || contentOverflows,
+      // Viewport-absolute (#1779). Rounded: sub-pixel layout makes a raw
+      // `left` read `0.00001` and an `=== 0` assertion flake on it.
+      viewportWidth,
+      contentLeft: contentBox ? Math.round(contentBox.left) : null,
+      contentRight: contentBox ? Math.round(contentBox.right) : null,
     }
   })
 }

diff --git a/packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts b/packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts
--- a/packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts
+++ b/packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts
@@ -67,6 +67,52 @@ async function expectNavigationReachable(page: Page) {
   const open = page.getByRole('button', { name: 'Open sidebar' })
   await expect(open).toBeVisible()
 
+  // 0. The VIEWPORT-ABSOLUTE anchor (#1779), asserted BEFORE the hit-tests
+  //    because it is the frame they are all read in.
+  //
+  //    Every other assertion in this function measures one element against
+  //    another: the toggle against whatever `elementFromPoint` returns at the
+  //    toggle's own centre, the drawer against the header's own height. Those
+  //    are all preserved by a transformation that moves the whole shell, so
+  //    this spec passed the mutation that exposed the gap — the toggle's
+  //    `fixed` swapped for `relative`, which drops it into flow as a 32px flex
+  //    item and shifts `<header>` from x=0 to x=32 while every relative
+  //    reading holds. Measured, not predicted.
+  //
+  //    The top bar spanning the viewport edge to edge is the right anchor for
+  //    THIS spec specifically: the 56px band is its whole subject — the band
+  //    where the toggle and `TopBar` contest the stacking order — so pinning
+  //    that band to the screen says the geometry the layering claims are made
+  //    against has not moved under them.
+  //
+  //    Computed here rather than through `expectNoHorizontalOverflow`, on
+  //    purpose. `navigation.mobile.spec.ts` gets its anchor from that shared
+  //    helper; if this one did too, a single weakened helper would blind every
+  //    mobile suite at once and nothing would go red — one shared reference
+  //    frame that everything trusts is precisely the defect #1779 is about, and
+  //    re-introducing it one layer up would be the same mistake wearing the
+  //    fix's clothes. Two independently-computed anchors can disagree.
+  //
+  //    Expressed as two GAPS rather than as `right === innerWidth`, so a
+  //    failure prints how far the bar is off each edge instead of two absolute
+  //    numbers the reader then has to subtract.
+  const shell = await page.evaluate(() => {
+    const header = document.querySelector('header')
+    if (!header) return null
+    const b = header.getBoundingClientRect()
+    return {
+      leftGap: Math.round(b.left),
+      rightGap: Math.round(window.innerWidth - b.right),
+      viewportWidth: window.innerWidth,
+      headerWidth: Math.round(b.width),
+    }
+  })
+  expect(shell, 'no <header> — the shell never rendered').not.toBeNull()
+  expect(
+    { leftGap: shell!.leftGap, rightGap: shell!.rightGap },
+    `top bar is not anchored to the viewport: ${JSON.stringify(shell)}`,
+  ).toEqual({ leftGap: 0, rightGap: 0 })
+
   // 1. The hit-test from the original report. `elementFromPoint` answers "what
   //    would a tap here actually reach", which is the only question that
   //    matters — the button's own computed style was always correct.

diff --git a/packages/frontend/e2e/navigation.mobile.spec.ts b/packages/frontend/e2e/navigation.mobile.spec.ts
--- a/packages/frontend/e2e/navigation.mobile.spec.ts
+++ b/packages/frontend/e2e/navigation.mobile.spec.ts
@@ -133,6 +133,23 @@ test.describe('mobile viewport', () => {
       // must never be silent.
       await page.locator('#main-content').waitFor({ state: 'attached' })
 
+      // ...and wait for the SIDEBAR too, not just the content region (#1779).
+      //
+      // `Sidebar` is `dynamic(..., { ssr: false })`, so it renders a chunk
+      // later than `<main>` does. Until it does, the shell has no leading
+      // element at all and `<main>` sits at x=0 — which is the same reading a
+      // correctly-anchored shell gives. The viewport anchor below therefore
+      // passed under the very mutation it exists to catch, on 3 of 4 routes,
+      // in the run that was supposed to prove it: the measurement had simply
+      // happened first. The one route that went red was the slow one.
+      //
+      // Caught by running the mutation rather than by reading, and it is the
+      // same silent-no-op shape `contentRegionFound` was added for one issue
+      // ago — a guard that passes because the thing it measures had not
+      // rendered yet. The toggle is the sidebar's own `lg:hidden` control, so
+      // waiting for it is exactly "the mobile shell is now laid out".
+      await page.getByRole('button', { name: 'Open sidebar' }).waitFor()
+
       const overflow = await expectNoHorizontalOverflow(page)
       expect(overflow, 'content region was never found — measurement was a no-op').toMatchObject({
         contentRegionFound: tr...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/contributing/ship-playbooks/frontend.md @ 94c5021092e954eb04c4d402404d9da0d3b7ec7a -->
---
owner: "@d-hinders"
status: current
covers: []  # narrative — process playbook
last-verified: "2026-08-22" # #1771: §4's overflow paragraph rewritten — the shared helper now measures `<main>`'s scroll box too and CAN fail inside the shell; separates `documentOverflows` (unreachable) from `contentOverflows` (whole pane forced into horizontal scroll), and names the two-scroll-box measurement's structural limits. Prior: #1768: §4 gains the viewport-coverage table — both Playwright projects gate on every PR now, and `*.mobile.spec.ts` is how you write a mobile test. Prior: #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
---

# Frontend playbook

Loaded by `ship-next` for `area:frontend` issues. The goal: a UI issue is shipped on Haven's UX standards without the contributor having to name them. This playbook **links** the standards; it does not restate them.

## 1. Required reading (before implementing)

Read, in order — these are `AGENTS.md` → "Required Reading For UI Work":

1. [`product/README.md`](../../product/README.md) — product doctrine, IA, money-movement clarity, accessibility, and closeout checks.
2. [`product/design-system.md`](../../product/design-system.md) — tokens, typography, cards, buttons, motion, surface hierarchy.
3. [`product/copy-guidelines.md`](../../product/copy-guidelines.md) — user-facing wording and banned technical terms.
4. [`product/screen-recipes.md`](../../product/screen-recipes.md) — repeatable screen structures.
5. [`product/design-review.md`](../../product/design-review.md) — the finishing checklist (also used in §5).

If a `/design-system` route exists, inspect it before editing UX.

## 2. Reuse first

Inspect `packages/frontend/src/components/ui` (primitives) and `packages/frontend/src/components/haven` (domain components) before adding UI. Prefer composition; do **not** invent new card styles, spacing, shadows, radius, or typography unless the existing system genuinely can't express the need. Use the v2 tokens in `globals.css` and the Tailwind aliases.

**Absorb a pattern on its 2nd occurrence, not its 12th ([#901](https://github.com/d-hinders/Haven-AI/issues/901)).** If this diff writes the same markup shape a second time — a header band, badge, row, empty-state, inline `<svg>`, address slice — or re-creates something a primitive already covers, extract it into a `ui/`/`haven/` primitive **and** document it on `/design-system`, in this same PR. This is the Captain Self-Check Preflight's **Pattern Absorption** item; it's the mechanism that prevents the debt clusters epic #859 had to clean retroactively. Only skip it if the two uses will genuinely diverge — and say so.

**A new primitive must land on `/design-system` in the same PR ([#898](https://github.com/d-hinders/Haven-AI/issues/898)).** The design-system coupling gate flags any exported component added under `components/ui/**` or `components/haven/**` whose symbol never appears on `app/(authenticated)/design-system/page.tsx`. Two CI jobs, on every PR however it was opened ([#1023](https://github.com/d-hinders/Haven-AI/issues/1023)): **Design-system coupling** posts the sticky comment that explains the finding, and **Design-system coupling (strict)** blocks on it. Add a showcase entry (usage + variants) alongside the primitive, or — for a genuinely internal export, not a reusable primitive — mark the export line `// design-system-exempt: <reason>`. Check locally with `node packages/frontend/scripts/design-system-coupling.mjs --strict`.

## 3. Captain Self-Check Preflight

Run the matching items from the **Captain Self-Check Preflight** in [`../ai-agent-workflow.md`](../ai-agent-workflow.md) for the traps the diff touches — e.g. numeric formatters, counter/summary buckets, conditional copy predicates, async hook generations, signer-readiness gates, animation discipline, inline-gate placement, cross-surface display drift, loading-state inference. Each is one grep or one quick read. Do this **before** review so the reviewer finds fewer issues.

## 4. Verification

Verify the change in the **browser**, or — when the browser path is unavailable/flaky — add a **named headless equivalent** (vitest) that covers the skipped animation, layout, routing, loading, or interaction risk. Include empty, loading, error, and success states when the screen can enter them; check mobile and desktop.

**Which viewports actually gate ([#1768](https://github.com/d-hinders/Haven-AI/issues/1768)).** The *Frontend browser smoke* job runs **both** Playwright projects on every frontend PR, with no dispatch required:

| Project | Emulation | Runs | Gates a PR |
|---|---|---|---|
| `chromium-desktop` | Desktop Chrome — 1280×720 viewport, fine pointer, no touch, DSF 1 | every `e2e/*.spec.ts` **except** `*.mobile.spec.ts` | yes |
| `chromium-mobile` | **Pixel 5** — 393×727 viewport, coarse p...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/contributing/ship-playbooks/frontend.md b/docs/contributing/ship-playbooks/frontend.md
--- a/docs/contributing/ship-playbooks/frontend.md
+++ b/docs/contributing/ship-playbooks/frontend.md
@@ -2,7 +2,7 @@
 owner: "@d-hinders"
 status: current
 covers: []  # narrative — process playbook
-last-verified: "2026-08-22" # #1771: §4's overflow paragraph rewritten — the shared helper now measures `<main>`'s scroll box too and CAN fail inside the shell; separates `documentOverflows` (unreachable) from `contentOverflows` (whole pane forced into horizontal scroll), and names the two-scroll-box measurement's structural limits. Prior: #1768: §4 gains the viewport-coverage table — both Playwright projects gate on every PR now, and `*.mobile.spec.ts` is how you write a mobile test. Prior: #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
+last-verified: "2026-08-22" # #1779: §4 gains the viewport-anchor rule — "A relative to B" cannot see A and B move together, so a mobile-shell suite needs one measurement against the viewport; includes the two traps (do not collapse the anchors into one shared helper; an anchor is only real once the mutation turned that spec red). Prior: #1771: §4's overflow paragraph rewritten — the shared helper now measures `<main>`'s scroll box too and CAN fail inside the shell; separates `documentOverflows` (unreachable) from `contentOverflows` (whole pane forced into horizontal scroll), and names the two-scroll-box measurement's structural limits. Prior: #1768: §4 gains the viewport-coverage table — both Playwright projects gate on every PR now, and `*.mobile.spec.ts` is how you write a mobile test. Prior: #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
 ---
 
 # Frontend playbook
@@ -58,6 +58,10 @@ Before #1768, `chromium-mobile` existed but only a `workflow_dispatch` with `ui_
 
 Two failure modes, and they are not the same defect: `documentOverflows` means content escaped the page box and — under the shell's `overflow-hidden` — is genuinely **unreachable**; `contentOverflows` means `<main>` (which is `overflow-y-auto`, so `overflow-x` computes to `auto`) is wider than its box, dragging the **whole content pane into horizontal scroll** instead of the offending element scrolling inside its own `overflow-x-auto` wrapper. The second is reachable but wrong — it is the [#1772](https://github.com/d-hinders/Haven-AI/issues/1772) shape. Note the measurement compares two scroll boxes rather than walking ancestors, so an `overflow-hidden` *between* them still hides evidence; `position: fixed` overlays are invisible to both ([#1773](https://github.com/d-hinders/Haven-AI/issues/1773)).
 
+**Relative measurement is not sufficient for shell-level geometry — anchor at least one assertion to the viewport ([#1779](https://github.com/d-hinders/Haven-AI/issues/1779)).** Any assertion of the form "A relative to B" is blind to A and B moving together, and a shell-level defect moves everything at once. Measured, not argued: mutating the mobile toggle's `fixed` to `relative` drops it into flow as a 32px flex item and displaces the entire app shell — `<header>` and `<main>` both go from x=0 to x=32 — and **three separate mobile specs stayed green**, because the toggle was checked against the header, layering as one element against another, and overflow as a content box against its own scroll box. `contentOverflowBy` still read `361 - 361 = 0`, exactly as it had read `393 - 393 = 0`. No rewording of an individual assertion fixes this; it is a property of the reference frame. So a mobile-shell suite needs at least one measurement against something the defect cannot carry with it — `getBoundingClientRect()` against `window.innerWidth`. The three suites now each carry their own: `header.left === 0` (#1766), the top bar's two viewport gaps (#1749's layering spec), and `<main>` spanning `0 → innerWidth` (#1771's overflow guard, via `contentLeft`/`contentRight`/`viewportWidth` reported — not asserted — by the shared helper, because the mobile shell, the desktop shell and `/login` have three different correct answers).
+
+Two traps this generalises into, both paid for already. **Deliberately do not collapse the anchors into one shared helper every suite calls** — one shared reference frame that everything trusts is the defect itself, one layer up; independent anchors can disagree, a single one cannot. And **an anchor is only real once the mutation has turned that specific spec red**: the first version of the `<main>` anchor above passed the mutation on 3 of 4 routes, because `Sidebar` is `dynamic(ssr: false)` and the measurement ran before it rendered, leaving `<main>` at x=0 — the same silent-no-op shape `contentRegionFound` exists for. Wait for the shell (the `Open sidebar` toggle) before measuring it.
+
 **A known, filed defect is exempted by name, never by deletion.** `navigation.mobile.spec.ts` keeps a `KNOWN_CONTENT_OVERFLOW` map: the route still runs and still asserts rendering and console cleanliness, only the one known-failing assertion is skipped, and only with an issue number and the measured numbers next to it. Dropping the route instead is how a gate quietly stops covering things — which is the defect #1768 exists to close. Delete the entry in the PR that fixes the issue.
 
 Run them locally with `npm run test:e2e:mobile -w packages/frontend`, or both with `npm run test:e2e:gate -w packages/frontend` (exactly what CI runs).
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/contributing/ship-playbooks/frontend.md @ ab535a33b403b040f40cd888d2707769a30d32d3 -->
---
owner: "@d-hinders"
status: current
covers: []  # narrative — process playbook
last-verified: "2026-08-22" # #1779: §4 gains the viewport-anchor rule — "A relative to B" cannot see A and B move together, so a mobile-shell suite needs one measurement against the viewport; includes the two traps (do not collapse the anchors into one shared helper; an anchor is only real once the mutation turned that spec red). Prior: #1771: §4's overflow paragraph rewritten — the shared helper now measures `<main>`'s scroll box too and CAN fail inside the shell; separates `documentOverflows` (unreachable) from `contentOverflows` (whole pane forced into horizontal scroll), and names the two-scroll-box measurement's structural limits. Prior: #1768: §4 gains the viewport-coverage table — both Playwright projects gate on every PR now, and `*.mobile.spec.ts` is how you write a mobile test. Prior: #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
---

# Frontend playbook

Loaded by `ship-next` for `area:frontend` issues. The goal: a UI issue is shipped on Haven's UX standards without the contributor having to name them. This playbook **links** the standards; it does not restate them.

## 1. Required reading (before implementing)

Read, in order — these are `AGENTS.md` → "Required Reading For UI Work":

1. [`product/README.md`](../../product/README.md) — product doctrine, IA, money-movement clarity, accessibility, and closeout checks.
2. [`product/design-system.md`](../../product/design-system.md) — tokens, typography, cards, buttons, motion, surface hierarchy.
3. [`product/copy-guidelines.md`](../../product/copy-guidelines.md) — user-facing wording and banned technical terms.
4. [`product/screen-recipes.md`](../../product/screen-recipes.md) — repeatable screen structures.
5. [`product/design-review.md`](../../product/design-review.md) — the finishing checklist (also used in §5).

If a `/design-system` route exists, inspect it before editing UX.

## 2. Reuse first

Inspect `packages/frontend/src/components/ui` (primitives) and `packages/frontend/src/components/haven` (domain components) before adding UI. Prefer composition; do **not** invent new card styles, spacing, shadows, radius, or typography unless the existing system genuinely can't express the need. Use the v2 tokens in `globals.css` and the Tailwind aliases.

**Absorb a pattern on its 2nd occurrence, not its 12th ([#901](https://github.com/d-hinders/Haven-AI/issues/901)).** If this diff writes the same markup shape a second time — a header band, badge, row, empty-state, inline `<svg>`, address slice — or re-creates something a primitive already covers, extract it into a `ui/`/`haven/` primitive **and** document it on `/design-system`, in this same PR. This is the Captain Self-Check Preflight's **Pattern Absorption** item; it's the mechanism that prevents the debt clusters epic #859 had to clean retroactively. Only skip it if the two uses will genuinely diverge — and say so.

**A new primitive must land on `/design-system` in the same PR ([#898](https://github.com/d-hinders/Haven-AI/issues/898)).** The design-system coupling gate flags any exported component added under `components/ui/**` or `components/haven/**` whose symbol never appears on `app/(authenticated)/design-system/page.tsx`. Two CI jobs, on every PR however it was opened ([#1023](https://github.com/d-hinders/Haven-AI/issues/1023)): **Design-system coupling** posts the sticky comment that explains the finding, and **Design-system coupling (strict)** blocks on it. Add a showcase entry (usage + variants) alongside the primitive, or — for a genuinely internal export, not a reusable primitive — mark the export line `// design-system-exempt: <reason>`. Check locally with `node packages/frontend/scripts/design-system-coupling.mjs --strict`.

## 3. Captain Self-Check Preflight

Run the matching items from the **Captain Self-Check Preflight** in [`../ai-agent-workflow.md`](../ai-agent-workflow.md) for the traps the diff touches — e.g. numeric formatters, counter/summary buckets, conditional copy predicates, async hook generations, signer-readiness gates, animation discipline, inline-gate placement, cross-surface display drift, loading-state inference. Each is one grep or one quick read. Do this **before** review so the reviewer finds fewer issues.

## 4. Verification

Verify the change in the **browser**, or — when the browser path is unavailable/flaky — add a **named headless equivalent** (vitest) that covers the skipped animation, layout, routing, loading, or interaction risk. Include empty, loading, error, and success states when the screen can enter them; check mobile and desktop.

**Which viewports actually gate ([#1768](https://github.com/d-hinders/Haven-AI/issues/1768)).** The *Frontend browser smoke* job runs **both** Playwright projects on every fronte...
```

### `GH-CAND-0010`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1780
- Repository: `d-hinders/Haven-AI`
- PR number: `1780`
- PR title: feat(connect): resolve the runtime itself — agent self-report, installed-client prompt, real failure vocabulary (#1719)
- Language: `typescript`
- Code changed files: `['packages/backend/src/routes/__tests__/agent-connection-setups.test.ts', 'packages/backend/src/routes/agent-connection-setups.ts', 'packages/connect/src/args.ts', 'packages/connect/src/cli.test.ts', 'packages/connect/src/cli.ts', 'packages/connect/src/config-writers.test.ts', 'packages/connect/src/config-writers.ts', 'packages/connect/src/connect-error.ts', 'packages/connect/src/index.ts', 'packages/connect/src/installed-clients.test.ts', 'packages/connect/src/installed-clients.ts', 'packages/connect/src/runtime-registry.test.ts', 'packages/connect/src/runtime-registry.ts', 'packages/connect/src/runtime.test.ts', 'packages/connect/src/runtime.ts', 'packages/frontend/e2e/fixtures/haven-api.ts', 'packages/frontend/src/components/connect-agent/__tests__/runtime-status-copy.test.ts', 'packages/frontend/src/components/connect-agent/setup-copy.ts']`
- Docs changed files: `['docs/operations/mcp-runtime-compatibility.md', 'docs/regulatory/casp-changelog/2026-08-22-1719.md']`

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
diff --git a/packages/backend/src/routes/__tests__/agent-connection-setups.test.ts b/packages/backend/src/routes/__tests__/agent-connection-setups.test.ts
--- a/packages/backend/src/routes/__tests__/agent-connection-setups.test.ts
+++ b/packages/backend/src/routes/__tests__/agent-connection-setups.test.ts
@@ -319,7 +319,11 @@ describe('agent connection setup routes', () => {
     // #1545: the backend is the source of truth for the prompt — pin the
     // --json discoverability sentence and the gate's one name here, not only
     // in the frontend/e2e mirrors.
-    expect(body.setup_prompt).toContain('Appending --json is the ONLY permitted change to the command above.')
+    // #1719: the permitted-changes sentence now names the --runtime retry the
+    // connector asks an agent for by name, and still forbids everything else.
+    expect(body.setup_prompt).toContain('Only two changes to the command above are permitted, and no others: appending --json')
+    expect(body.setup_prompt).toContain('could not determine the agent runtime')
+    expect(body.setup_prompt).toContain('Never invent a runtime name')
     expect(body.setup_prompt).toContain('return to Haven to approve the budget')
     expect(body.setup_prompt).not.toContain('agent rules')
     expect(body.setup_prompt).not.toMatch(/delegate_key|private_key|sk_agent_/)

diff --git a/packages/backend/src/routes/agent-connection-setups.ts b/packages/backend/src/routes/agent-connection-setups.ts
--- a/packages/backend/src/routes/agent-connection-setups.ts
+++ b/packages/backend/src/routes/agent-connection-setups.ts
@@ -1233,7 +1233,14 @@ function buildSetupPrompt(command: string, runtime: string | null, apiUrl: strin
     // #1545: one sentence of discoverability for agent operators — the flag is
     // opt-in and the pasted command stays the prose-mode default, so the
     // relay-to-human narration keeps working when the operator ignores this.
-    'If you are orchestrating this setup programmatically, the connector also supports a --json mode: one machine-readable, secret-free result object on stdout, progress on stderr. Appending --json is the ONLY permitted change to the command above.',
+    'If you are orchestrating this setup programmatically, the connector also supports a --json mode: one machine-readable, secret-free result object on stdout, progress on stderr.',
+    // #1719: the old sentence said appending --json was the ONLY permitted
+    // change, which forbade the one retry the connector now asks an agent for
+    // by name. Exactly two changes are permitted, and the second is bounded to
+    // a value the refusal itself listed — an agent must never invent a runtime
+    // name, because the name selects which app gets an API key and a signing
+    // key written into it.
+    'Only two changes to the command above are permitted, and no others: appending --json, and — only if the connector refuses because it could not determine the agent runtime — re-running it once with --runtime <name> added, naming the harness you are running in, using one of the values that refusal lists. Never invent a runtime name and never change anything else.',
     '',
     // #1545: "budget" is the connect flow's one name for the approval gate —
     // the same word the connector's own wait loop and celebration use (#1542).

diff --git a/packages/connect/src/args.ts b/packages/connect/src/args.ts
--- a/packages/connect/src/args.ts
+++ b/packages/connect/src/args.ts
@@ -128,7 +128,9 @@ export function helpText(): string {
     '  --api <url>                Haven backend API URL. Defaults to HAVEN_API_URL or http://localhost:3001.',
     '  --runtime <name>           Agent runtime hint, such as claude-code, codex-cli, codex-desktop, cursor, vscode, claude-desktop, or hermes.',
     '                             Usually unnecessary: the connector detects the runtime it runs inside, and a detection',
-    '                             that contradicts this hint wins (with a printed notice). Needed only in a plain terminal.',
+    '                             that contradicts this hint wins (with a printed notice). When nothing is detected, an',
+    '                             interactive terminal is offered the agent clients installed on this machine; this flag is',
+    '                             how an agent, or a non-interactive run, answers instead. An unknown name is refused, never guessed.',
     '  --runtime-force <name>     Escape hatch: use exactly this runtime, ignoring environment detection.',
     '  --credentials-dir <path>   Credential directory fallback. Defaults to ~/.haven/agents.',
     '  --environment-label <text> Non-sensitive label shown in Haven setup review.',

diff --git a/packages/connect/src/cli.test.ts b/packages/connect/src/cli.test.ts
--- a/packages/connect/src/cli.test.ts
+++ b/packages/connect/src/cli.test.ts
@@ -5,6 +5,7 @@ import { pathToFileURL } from 'node:url'
 import { afterEach, describe, expect, it, vi } from 'vitest'
 import { isCliEntrypoint, runCli } from './cli.js'
 import * as runtime from './runtime.js'
+import { ConnectError } from './connect-error.js'
 
 let tempDir = ''
 
@@ -63,6 +64,68 @@ describe('--json wiring for the approval wait (#1377 D)', () => {
   })
 })
 
+describe('--json never prompts for a runtime (#1719)', () => {
+  // The interactive rung is the one thing that could make the automation
+  // contract block on stdin. --json must reach a machine-readable refusal
+  // instead, which is what `interactive: false` buys.
+  it('passes interactive:false under --json and true otherwise', async () => {
+    const seen: Array<boolean | undefined> = []
+    const spy = vi.spyOn(runtime, 'runConnect').mockImplementation(async (options) => {
+      seen.push(options.interactive)
+      return { outcome: { schema_version: 1, outcome: 'complete' } } as never
+    })
+    try {
+      const io = { stdout: () => undefined, stderr: () => undefined }
+      await runCli(['--setup', 'hv_setup_x', '--api', 'https://api.haven.example', '--json'], io)
+      await runCli(['--setup', 'hv_setup_x', '--api', 'https://api.haven.example'], io)
+    } finally {
+      spy.mockRestore()
+    }
+    expect(seen).toEqual([false, true])
+  })
+
+  it('reports an undetermined runtime as a code on stdout, and exits non-zero', async () => {
+    const stdout: string[] = []
+    const spy = vi.spyOn(runtime, 'runConnect').mockRejectedValue(
+      new ConnectError('runtime_undetermined', 'could not determine the agent runtime', 'rerun_connect_with_explicit_runtime'),
+    )
+    try {
+      const exitCode = await runCli(
+        ['--setup', 'hv_setup_x', '--api', 'https://api.haven.example', '--json'],
+        { stdout: (message) => stdout.push(message), stderr: () => undefined },
+      )
+      expect(exitCode).toBe(1)
+      expect(JSON.parse(stdout[0])).toMatchObject({
+        outcome: 'failed',
+        error: { code: 'runtime_undetermined', next_action: 'rerun_connect_with_explicit_runtime' },
+      })
+    } finally {
+      spy.mockRestore()
+    }
+  })
+
+  it('exits non-zero on an aborted prompt in prose mode, saying nothing was written', async () => {
+    const stderr: string[] = []
+    const spy = vi.spyOn(runtime, 'runConnect').mockRejectedValue(
+      new ConnectError(
+        'runtime_prompt_aborted',
+        'Runtime not chosen (the prompt was cancelled). Nothing was written.',
+        'rerun_connect_and_choose_a_runtime',
+      ),
+    )
+    try {
+      const exitCode = await runCli(
+        ['--setup', 'hv_setup_x', '--api', 'https://api.haven.example'],
+        { stdout: () => undefined, stderr: (message) => stderr.push(message) },
+      )
+      expect(exitCode).toBe(1)
+      expect(stderr.join('')).toContain('Nothing was written')
+    } finally {
+      spy.mockRestore()
+    }
+  })
+})
+
 describe('CLI entrypoint detection (#1379)', () => {
   it('recognizes an npm-style bin symlink without running ordinary imports', async () => {
     tempDir = await mkdtemp(join(tmpdir(), 'haven-connect-cli-'))

diff --git a/packages/connect/src/cli.ts b/packages/connect/src/cli.ts
--- a/packages/connect/src/cli.ts
+++ b/packages/connect/src/cli.ts
@@ -131,7 +131,15 @@ export async function runCli(
     // --json is the automation contract: emit the outcome promptly instead of
     // blocking up to the approval-wait bound (#1377 D).
     const result = await runConnect(
-      { ...parsed.options, waitForApproval: !parsed.json },
+      {
+        ...parsed.options,
+        waitForApproval: !parsed.json,
+        // #1719: only a human-facing run may be asked which installed client to
+        // configure. --json is the automation contract — it must fail with a
+        // machine-readable code, never block on stdin. runConnect additionally
+        // requires a real TTY before it prompts.
+        interactive: !parsed.json,
+      },
       {
         log: (message) => (parsed.json ? io.stderr : io.stdout)(`...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/operations/mcp-runtime-compatibility.md @ ccbc899eb6f833f8f81a73c38096b4fa13c2a35d -->
---
owner: "@d-hinders"
status: current
contract: true
covers:
  - packages/mcp/**
  - packages/connect/**
  - packages/signer/**
  - packages/mcp-server/src/tools.ts
  - .github/workflows/publish.yml
last-verified: "2026-08-21" # #1697: --doctor is per-agent — it enumerates every credential directory and classifies each wired/superseded/retired/orphaned instead of "newest wins", runs the full check set per WIRED agent, and exits non-zero if ANY wired agent fails ANY check; --json gains agents[] (slug/agentId/directory/classification/checks) while the flat checks[] still describes one agent so single-agent installs read unchanged. New identity_match check compares the agent the stored API key authenticates as (GET /machine-payments/agent, read-only) against signer.json's delegate_address — a mismatch fails hard. No tool, capability, or version-skew surface moves. Prior: #1696: connect gains --name <slug> — a NAMED agent writes the #1695 haven-<slug>/haven-signer-<slug> MCP pair, stores credentials at ~/.haven/agents/<slug>/ (unnamed keeps ~/.haven/agents/<agent-uuid>/), and records the slug as server_name in signer-runtime.json/mcp-runtime.json. The slug is validated at the ARGUMENT (before any key is minted or file written) and a taken slug refuses before registration, so a re-run can never orphan an agent or overwrite credentials; "haven"/"haven-signer" and the reserved signer/signer-* family are refused. Omitting --name is byte-identical to today. No tool, capability, or version-skew surface moves; --doctor/--repair stay bare-pair-scoped until #1697. Prior: #1695: every runtime config writer (Cursor/VS Code/Claude Desktop JSON, Codex TOML, Hermes YAML+env, Claude Code CLI) is parametrized on a server-name pair — an optional serverName slug yields haven-<slug>/haven-signer-<slug> entries (Hermes: its own MCP_HAVEN_<SLUG>_API_KEY) that coexist with the bare pair; a writer touches ONLY the pair it owns, which removes the #1569 clobbering class (slugs "signer"/"signer-*" are reserved — the one family whose derived names could collide across pairs). The UNNAMED path is byte-identical to before (pinned by characterization tests) — no wired host changes, no tool, capability, or version-skew surface moves; #1696 wires the --name flag. Prior: #1681: connect gains --tombstone <dir> (retire a credential directory in place: diagnostic wrapper + TOMBSTONE.json; no keys touched, nothing revoked, no token/--runtime) and --doctor reads tombstones in the superseded scan (keys removed => informational retired; key present => the #1688 live-probe verdict unchanged); restart guidance widens to EVERY long-lived host. No tool, capability, or version-skew surface moves. Prior: #1688 re-verify: --doctor gains the superseded_agents check (probes every unselected credential dir with its own key; live ⇒ failing check + revoke repair) and setup completion names superseded agents — diagnostics only, no tool, capability, or version-skew surface moves, and the doctor/repair contract this doc describes stands with one addition it now records. Prior: #1690: x402 expected-context VERSION 3 (payer identity) ships signer-first — SUPPORTED_X402_EXPECTED_VERSIONS widens to [1,2,3] (capability handshake and instructions render the new set automatically, both derived from the constant), the signer refuses another agent's quote naming both identities, and the backend keeps emitting v2 until the operator flips X402_EMIT_PAYER_CONTEXT per environment. The version-skew contract is unchanged in shape: a v3 context on a v1/v2 signer produces the existing machine-readable refusal carrying users to `npx @haven_ai/connect@alpha`. No tool schema moves; the signer tool boundary gains OPTIONAL payer_delegate/payer_agent_id passthrough fields. Prior: #1682: the runtime picker is name-first — the collapsed "AI agent" row is replaced by a flat product-name list, and a new "The picker is name-first" subsection carries the row→modality table, the folded vscode-insiders id, and the OpenClaw row's dependency on a published connect release. Detection precedence, the Node floor, and every skew/manifest claim re-read against the diff and unchanged. Prior: #1672: runtime selection is detection-first — the setup command drops --runtime on command-path runtimes, detection overrides a contradicting hint (notice printed; --runtime-force escape hatch), and no-detection-no-flag refuses before any side effect; new "Runtime selection is detection-first" section documents it. No manifest, tool, capability, or version-skew surface moves. Prior: Release 0.1.28-alpha.0: the Supported Runtime Manifest table is re-pinned to match packages/connect/src/runtime-manifest.ts. Version strings only — no tool, capability, or version-skew surface moves, and the skew contract paragraphs below re-read against the diff stand unchanged. The bump exists because the #1620 SDK decomposition epic (...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/operations/mcp-runtime-compatibility.md b/docs/operations/mcp-runtime-compatibility.md
--- a/docs/operations/mcp-runtime-compatibility.md
+++ b/docs/operations/mcp-runtime-compatibility.md
@@ -8,7 +8,7 @@ covers:
   - packages/signer/**
   - packages/mcp-server/src/tools.ts
   - .github/workflows/publish.yml
-last-verified: "2026-08-21" # #1697: --doctor is per-agent — it enumerates every credential directory and classifies each wired/superseded/retired/orphaned instead of "newest wins", runs the full check set per WIRED agent, and exits non-zero if ANY wired agent fails ANY check; --json gains agents[] (slug/agentId/directory/classification/checks) while the flat checks[] still describes one agent so single-agent installs read unchanged. New identity_match check compares the agent the stored API key authenticates as (GET /machine-payments/agent, read-only) against signer.json's delegate_address — a mismatch fails hard. No tool, capability, or version-skew surface moves. Prior: #1696: connect gains --name <slug> — a NAMED agent writes the #1695 haven-<slug>/haven-signer-<slug> MCP pair, stores credentials at ~/.haven/agents/<slug>/ (unnamed keeps ~/.haven/agents/<agent-uuid>/), and records the slug as server_name in signer-runtime.json/mcp-runtime.json. The slug is validated at the ARGUMENT (before any key is minted or file written) and a taken slug refuses before registration, so a re-run can never orphan an agent or overwrite credentials; "haven"/"haven-signer" and the reserved signer/signer-* family are refused. Omitting --name is byte-identical to today. No tool, capability, or version-skew surface moves; --doctor/--repair stay bare-pair-scoped until #1697. Prior: #1695: every runtime config writer (Cursor/VS Code/Claude Desktop JSON, Codex TOML, Hermes YAML+env, Claude Code CLI) is parametrized on a server-name pair — an optional serverName slug yields haven-<slug>/haven-signer-<slug> entries (Hermes: its own MCP_HAVEN_<SLUG>_API_KEY) that coexist with the bare pair; a writer touches ONLY the pair it owns, which removes the #1569 clobbering class (slugs "signer"/"signer-*" are reserved — the one family whose derived names could collide across pairs). The UNNAMED path is byte-identical to before (pinned by characterization tests) — no wired host changes, no tool, capability, or version-skew surface moves; #1696 wires the --name flag. Prior: #1681: connect gains --tombstone <dir> (retire a credential directory in place: diagnostic wrapper + TOMBSTONE.json; no keys touched, nothing revoked, no token/--runtime) and --doctor reads tombstones in the superseded scan (keys removed => informational retired; key present => the #1688 live-probe verdict unchanged); restart guidance widens to EVERY long-lived host. No tool, capability, or version-skew surface moves. Prior: #1688 re-verify: --doctor gains the superseded_agents check (probes every unselected credential dir with its own key; live ⇒ failing check + revoke repair) and setup completion names superseded agents — diagnostics only, no tool, capability, or version-skew surface moves, and the doctor/repair contract this doc describes stands with one addition it now records. Prior: #1690: x402 expected-context VERSION 3 (payer identity) ships signer-first — SUPPORTED_X402_EXPECTED_VERSIONS widens to [1,2,3] (capability handshake and instructions render the new set automatically, both derived from the constant), the signer refuses another agent's quote naming both identities, and the backend keeps emitting v2 until the operator flips X402_EMIT_PAYER_CONTEXT per environment. The version-skew contract is unchanged in shape: a v3 context on a v1/v2 signer produces the existing machine-readable refusal carrying users to `npx @haven_ai/connect@alpha`. No tool schema moves; the signer tool boundary gains OPTIONAL payer_delegate/payer_agent_id passthrough fields. Prior: #1682: the runtime picker is name-first — the collapsed "AI agent" row is replaced by a flat product-name list, and a new "The picker is name-first" subsection carries the row→modality table, the folded vscode-insiders id, and the OpenClaw row's dependency on a published connect release. Detection precedence, the Node floor, and every skew/manifest claim re-read against the diff and unchanged. Prior: #1672: runtime selection is detection-first — the setup command drops --runtime on command-path runtimes, detection overrides a contradicting hint (notice printed; --runtime-force escape hatch), and no-detection-no-flag refuses before any side effect; new "Runtime selection is detection-first" section documents it. No manifest, tool, capability, or version-skew surface moves. Prior: Release 0.1.28-alpha.0: the Supported Runtime Manifest table is re-pinned to match packages/connect/src/runtime-manifest.ts. Version strings only — no tool, capability, or version-skew surface moves, and the skew contract paragraphs below re-read against the diff stand unchanged. The bump exists because the #1620 SDK decomposition epic (#1614, #1618, #1619, #1631, #1634, #1636, #1655) rewrote packages/sdk/src/client.ts AFTER 0.1.27-alpha.0 was published, and publish.yml skips versions already on npm — so without it the same version string holds different code on npm and in-repo, and the entries below that document that epic would describe an SDK npm does not yet ship. That epic reduced client.ts from ~2500 lines to a compatibility facade over extracted lifecycle modules, exactly the change class that could move a consumer-visible surface silently, so it was MEASURED rather than assumed: the built dist/index.d.ts diffed against the @haven_ai/sdk@0.1.27-alpha.0 tarball from npm shows 155 top-level declarations with zero added and zero removed, and no changed line in the 227-line type diff that is not a private member or a comment. What moved is which module owns a code path, never what a consumer may call. Prior: #1618 re-verify: the SDK's EIP-3009 x402 funding leg moved out of HavenClient into internal modules (x402-protocol.ts / x402-funding-leg.ts). Behaviour-preserving and INTERNAL — no tool schema, capability, runtime-floor, or version-skew surface moves, and the published set this doc governs is unchanged. This doc was pulled in only because connect's package-smoke test had a comment naming the renamed method; every claim here re-read against the diff stands. Prior: Release 0.1.27-alpha.0: the Supported Runtime Manifest table is re-pinned to match packages/connect/src/runtime-manifest.ts. Version strings only — no tool, capability, or version-skew surface moves, and the skew contract paragraphs below re-read against the diff stand unchanged. The bump exists because #1593, #1595, #1597 and #1598 changed connect, the hosted server and the SDK AFTER 0.1.26-alpha.0 was published, and publish.yml skips versions already on npm — so without it `npx @haven_ai/connect@alpha` keeps resolving to a build with no --doctor, and this table's own #1589/#1587/#1588 entries would document a connector that npm does not yet ship. Prior: #1593: the LOCAL MCP runtime install is hardened like #1586 did the signer's — same honest budget (SIGNER_INSTALL_TIMEOUT_MS, replacing the spurious 120s timeout) and 15s onProgress heartbeats, threaded through installRuntime (integration-proven; the unthreaded-callback mutation fails the test). Setup reliability only — no tool, capability, or version-skew surface moves. Prior: #1591: hosted tool-description prose slimmed ~49% with flow-generic guidance consolidated into the server instructions (sign-by-payment_id, settle shapes, expiry re-run, version-mismatch branch, sweep pointer) — prose only; no tool schema, capability, or version-skew surface moves, and the skew contract paragraphs re-read against the diff stand unchanged. Prior: #1590: haven_get_agent gains spend_authority_readiness (readiness stays as a deprecated same-value alias) — additive field + prose stating the local-signer exclusion; no tool schema, capability, or version-skew surface moves. Prior: #1589: --doctor/--repair documented. Prior: #1588: runtime-neutral next_tool_server/next_tool_name pair documented. Prior: #1587: hosted-topology setup handshake-probes the local signer before reporting success; troubleshooting entry added. Prior: #1586: signer preinstall fails closed (no config write, no npx fallback), 10-min budget + heartbeats; troubleshooting entry added. Prior: #1549 re-verify: haven_pay_mcp_tool/haven_prepare_catalog_purchase stop echoing payment_required by default (the signer's #1355 payment_id fetch is the source; include_signing_payload=true restores it — the same replay escape this doc already documents for typed_data), and signer_compatibility.check is shorter prose with the #1309 machine fields unchanged. No tool schema, capability, or version-skew surface moves; the skew table's quote/prepare row and the #1309 contract paragraphs re-read against the diff and stand. Prior: #1548 re-verify: tool-description prose gains the...
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/operations/mcp-runtime-compatibility.md @ 59815088e1e4afc770b85082b144a43ddb52918a -->
---
owner: "@d-hinders"
status: current
contract: true
covers:
  - packages/mcp/**
  - packages/connect/**
  - packages/signer/**
  - packages/mcp-server/src/tools.ts
  - .github/workflows/publish.yml
last-verified: "2026-08-22" # #1719: the connector resolves its own runtime — the #1672 ladder gains an agent self-report rung (at hint precedence, so it still loses to detection) and an installed-client scan + TTY prompt that populates choices and NEVER selects, skipped entirely under --json / non-TTY; an unrecognised runtime name refuses (runtime_unrecognized) instead of falling through, or loses loudly to a detection; new stable codes runtime_undetermined, runtime_unrecognized, runtime_force_unrecognized, runtime_no_installed_clients, runtime_prompt_aborted (all pre-side-effect, connector-exit only) and runtime_config_unreadable (post-credential, reaches the dashboard, split from the retryable runtime_config_write_failed). No tool, capability, or version-skew surface moves; the Supported Runtime Manifest is unchanged. Prior: #1697: --doctor is per-agent — it enumerates every credential directory and classifies each wired/superseded/retired/orphaned instead of "newest wins", runs the full check set per WIRED agent, and exits non-zero if ANY wired agent fails ANY check; --json gains agents[] (slug/agentId/directory/classification/checks) while the flat checks[] still describes one agent so single-agent installs read unchanged. New identity_match check compares the agent the stored API key authenticates as (GET /machine-payments/agent, read-only) against signer.json's delegate_address — a mismatch fails hard. No tool, capability, or version-skew surface moves. Prior: #1696: connect gains --name <slug> — a NAMED agent writes the #1695 haven-<slug>/haven-signer-<slug> MCP pair, stores credentials at ~/.haven/agents/<slug>/ (unnamed keeps ~/.haven/agents/<agent-uuid>/), and records the slug as server_name in signer-runtime.json/mcp-runtime.json. The slug is validated at the ARGUMENT (before any key is minted or file written) and a taken slug refuses before registration, so a re-run can never orphan an agent or overwrite credentials; "haven"/"haven-signer" and the reserved signer/signer-* family are refused. Omitting --name is byte-identical to today. No tool, capability, or version-skew surface moves; --doctor/--repair stay bare-pair-scoped until #1697. Prior: #1695: every runtime config writer (Cursor/VS Code/Claude Desktop JSON, Codex TOML, Hermes YAML+env, Claude Code CLI) is parametrized on a server-name pair — an optional serverName slug yields haven-<slug>/haven-signer-<slug> entries (Hermes: its own MCP_HAVEN_<SLUG>_API_KEY) that coexist with the bare pair; a writer touches ONLY the pair it owns, which removes the #1569 clobbering class (slugs "signer"/"signer-*" are reserved — the one family whose derived names could collide across pairs). The UNNAMED path is byte-identical to before (pinned by characterization tests) — no wired host changes, no tool, capability, or version-skew surface moves; #1696 wires the --name flag. Prior: #1681: connect gains --tombstone <dir> (retire a credential directory in place: diagnostic wrapper + TOMBSTONE.json; no keys touched, nothing revoked, no token/--runtime) and --doctor reads tombstones in the superseded scan (keys removed => informational retired; key present => the #1688 live-probe verdict unchanged); restart guidance widens to EVERY long-lived host. No tool, capability, or version-skew surface moves. Prior: #1688 re-verify: --doctor gains the superseded_agents check (probes every unselected credential dir with its own key; live ⇒ failing check + revoke repair) and setup completion names superseded agents — diagnostics only, no tool, capability, or version-skew surface moves, and the doctor/repair contract this doc describes stands with one addition it now records. Prior: #1690: x402 expected-context VERSION 3 (payer identity) ships signer-first — SUPPORTED_X402_EXPECTED_VERSIONS widens to [1,2,3] (capability handshake and instructions render the new set automatically, both derived from the constant), the signer refuses another agent's quote naming both identities, and the backend keeps emitting v2 until the operator flips X402_EMIT_PAYER_CONTEXT per environment. The version-skew contract is unchanged in shape: a v3 context on a v1/v2 signer produces the existing machine-readable refusal carrying users to `npx @haven_ai/connect@alpha`. No tool schema moves; the signer tool boundary gains OPTIONAL payer_delegate/payer_agent_id passthrough fields. Prior: #1682: the runtime picker is name-first — the collapsed "AI agent" row is replaced by a flat product-name list, and a new "The picker is name-first" subsection carries the row→modality table, the folded vscode-insiders id, and the OpenClaw row's dependency on a published connect release. Detection precedence, the Node...
```

### `GH-CAND-0011`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1778
- Repository: `d-hinders/Haven-AI`
- PR number: `1778`
- PR title: fix(frontend): give the mobile sidebar toggle a 44px tap target without moving a pixel (#1766)
- Language: `typescript`
- Code changed files: `['packages/frontend/e2e/mobile-nav-tap-target.mobile.spec.ts', 'packages/frontend/src/components/sidebar/Sidebar.tsx']`
- Docs changed files: `['docs/product/design-system.md']`

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
diff --git a/packages/frontend/e2e/mobile-nav-tap-target.mobile.spec.ts b/packages/frontend/e2e/mobile-nav-tap-target.mobile.spec.ts
--- a/packages/frontend/e2e/mobile-nav-tap-target.mobile.spec.ts
+++ b/packages/frontend/e2e/mobile-nav-tap-target.mobile.spec.ts
@@ -0,0 +1,292 @@
+import { expect, test, type Page } from '@playwright/test'
+import { mockHavenApi, seedAuthenticatedSession } from './fixtures/haven-api'
+
+/**
+ * Mobile navigation toggle — tap target (#1766).
+ *
+ * The `Open sidebar` toggle paints a 32x32 box, 12px under the 44px comfort
+ * target `docs/product/design-system.md` § Buttons documents (#1726). It is a
+ * hand-rolled `<button>`, not the `Button` primitive, so it inherited none of
+ * that primitive's invisible hit-area extension. #1749 had just made this
+ * control REACHABLE for the first time below `lg` — it hit-tested under
+ * `TopBar` for the whole life of the shell — so the undersized target went from
+ * moot to load-bearing on the entry point to primary navigation.
+ *
+ * Measured on `/dashboard` under Pixel 5 emulation, before the fix:
+ *
+ *   painted box                        32 x 32   (x 16-48, y 16-48)
+ *   MEASURED hit rectangle             32 x 32   (x 16-47, y 16-47)
+ *   corners of the intended 44px area  all four land on <header>, not the toggle
+ *
+ * ...and after it:
+ *
+ *   painted box                        32 x 32   (unchanged — that is the point)
+ *   MEASURED hit rectangle             44 x 44   (x 10-54, y 10-54)
+ *   corners of the intended 44px area  all four reach the toggle
+ *
+ * Pixel conventions, because the two readings differ by one and both appear
+ * below: a 44px-wide box spanning x 10-54 has its LAST HITTING PIXEL at x=53.
+ * `hit.right` in the measurement is that last hitting pixel (53); "right edge
+ * x=54" in the clearance reasoning is the box edge. Same rectangle.
+ *
+ * ── Why every number above is MEASURED and not read off a class string ───────
+ * The obvious cheap test — assert the className contains `after:h-11 after:w-11`
+ * — cannot fail for the reason that matters. A pseudo-element overlay is a
+ * plausible-looking CSS trick with several silent no-op failure modes: a
+ * missing `content`, a positioning context that resolves somewhere else, an
+ * ancestor that clips it, or another element winning the stacking contest in
+ * that band (which is exactly what #1749 was). jsdom has no layout, no stacking
+ * contexts and no hit-testing, so none of that exists there. `elementFromPoint`
+ * in a real engine answers the only question worth asking: what would a tap
+ * here actually reach.
+ *
+ * The hit rectangle below is therefore not read from `getBoundingClientRect` —
+ * that returns the BORDER box and would report 32x32 even with a working 44px
+ * overlay. It is walked outward from the centre one pixel at a time, asking
+ * `elementFromPoint` at each step, so it is the rectangle a finger sees.
+ *
+ * ── Both halves of the invariant ────────────────────────────────────────────
+ * The target reaching 44px is only half the promise; the other half is that
+ * NOTHING MOVED. A test that only checks the hit area passes just as happily if
+ * someone "fixes" this by growing the visible box to `w-11 h-11`, which is the
+ * remedy #1726 explicitly rejected (it would crowd `NetworkSwitcher` in this
+ * 56px bar and churn the `/design-system` baselines). So the painted box is
+ * pinned at 32x32 in the same assertion pass.
+ */
+
+// The toggle is `lg:hidden`. The measured geometry is width-independent, so two
+// widths are enough to say so honestly: the narrowest phone we support, and the
+// last pixel below the `lg` breakpoint, where a regression would most plausibly
+// reappear. (`mobile-nav-layering.mobile.spec.ts` already proves the toggle
+// vanishes AT 1024px.)
+const WIDTHS = [320, 1023]
+
+const PAINTED_PX = 32
+const COMFORTABLE_TAP_TARGET_PX = 44
+
+type Measurement = {
+  painted: { w: number; h: number }
+  hit: { left: number; right: number; top: number; bottom: number; w: number; h: number }
+  corners: Record<string, string>
+  /** Nearest interactive control to the toggle's right, inside the top bar. */
+  neighbour: { label: string; left: number } | null
+  /**
+   * Where the top bar starts. The toggle is `fixed`, so it consumes NO layout —
+   * the bar it floats over begins at the viewport edge. See the assertion.
+   */
+  headerLeft: number
+}
+
+/**
+ * Everything the fix promises, measured against ONE page load.
+ *
+ * Deliberately not split per assertion: each test costs a full navigation, and
+ * this suite is meant to stay fast enough to gate every pull request (#1768).
+ */
+async function measureToggle(page: Page): Promise<Measurement> {
+  return page.evaluate(
+    ({ half }) => {
+      const btn = document.querySelector('button[aria-label="Open sidebar"]') as HTMLElement
+      const box = btn.getBoundingClientRect()
+      const cx = Math.round(box.left + box.width / 2)
+      const cy = Math.round(box.top + box.height / 2)
+
+      const reaches = (x: number, y: number) => {
+        const top = document.elementFromPoint(x, y)
+        return !!top && (top === btn || btn.contains(top))
+      }
+
+      // Walk outward until a tap stops landing on the toggle. This is the hit
+      // rectangle — the border box plus whatever the overlay adds — and it is
+      // the only measurement that can tell a working overlay from an inert one.
+      const walk = (dx: number, dy: number) => {
+        let n = 0
+        while (n < 80) {
+          const x = cx + dx * (n + 1)
+          const y = cy + dy * (n + 1)
+          if (x < 0 || y < 0 || x >= window.innerWidth || y >= window.innerHeight) break
+          if (!reaches(x, y)) break
+          n += 1
+        }
+        return n
+      }
+      const l = walk(-1, 0)
+      const r = walk(1, 0)
+      const u = walk(0, -1)
+      const d = walk(0, 1)
+
+      // Name what a failing corner actually hit, so a red run says WHAT is in
+      // the way rather than just `false` — the first question anyone asks next.
+      const describe = (x: number, y: number) => {
+        const top = document.elementFromPoint(x, y)
+        if (!top) return 'nothing'
+        if (top === btn || btn.contains(top)) return 'TOGGLE'
+        return `${top.tagName.toLowerCase()}.${String(top.className).trim().split(/\s+/).slice(0, 3).join('.')}`
+      }
+      const corners = {
+        centre: describe(cx, cy),
+        topLeft: describe(cx - half + 1, cy - half + 1),
+        topRight: describe(cx + half - 1, cy - half + 1),
+        bottomLeft: describe(cx - half + 1, cy + half - 1),
+        bottomRight: describe(cx + half - 1, cy + half - 1),
+      }
+
+      // The nearest interactive control to the toggle's right that shares its
+      // vertical band. The invisible target must not reach it: an overlay that
+      // swallows a neighbour's taps trades one mis-tap for another, and it is
+      // invisible by construction, so nothing but a measurement would notice.
+      const header = document.querySelector('header')!
+      let neighbour: { label: string; left: number } | null = null
+      for (const el of Array.from(
+        header.querySelectorAll<HTMLElement>('button, a[href], [role="button"]'),
+      )) {
+        const b = el.getBoundingClientRect()
+        if (b.width === 0 || b.height === 0) continue
+        if (b.left <= box.right) continue
+        if (b.bottom < box.top || b.top > box.bottom) continue
+        if (!neighbour || b.left < neighbour.left) {
+          neighbour = {
+            label: (el.getAttribute('aria-label') || el.textContent || el.tagName).trim().slice(0, 40),
+            left: Math.round(b.left),
+          }
+        }
+      }
+
+      return {
+        painted: { w: Math.round(box.width), h: Math.round(box.height) },
+        hit: { left: cx - l, right: cx + r, top: cy - u, bottom: cy + d, w: l + r + 1, h: u + d + 1 },
+        corners,
+        neighbour,
+        headerLeft: Math.round(header.getBoundingClientRect().left),
+      }
+    },
+    { half: Math.floor(COMFORTABLE_TAP_TARGET_PX / 2) },
+  )
+}
+
+test.describe('mobile navigation toggle tap target (#1766)', () => {
+  test.beforeEach(async ({ page }) => {
+    await mockHavenApi(page)
+    await seedAuthenticatedSession(page)
+  })
+
+  for (const width of WIDTHS) {
+    test.describe(`at ${width}px`, () => {
+      test.use({ viewport: { width, height: 844 } })
+
+      test('offers a 44px hit area without painting a pixel more', async ({ page }) => {
+        await page.goto('/dashboard')
+        await page.getByRole('button', { name: 'Open sidebar' }).waitFor()
+
+        const m = await measureToggle(page)
+
+        // 1. The hit rectangle a finger actually sees.
+        expect(m.hit.w).toBeGreaterThanOrEqual(COMFORTABLE_TAP_TARGET_PX)
+        expect(m.hit.h).toBeGreaterThanOrEqual(COMFORTABLE_TAP_TARGET_PX)
+
+        // 2. ...and the corners of that a...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/product/design-system.md @ 3ea080e082654a8a4fb8ed4a332379c3db661389 -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/frontend/src/app/globals.css
  - packages/frontend/tailwind.config.js
  - packages/frontend/src/components/ui/**
  - packages/frontend/src/app/layout.tsx
  - packages/frontend/src/app/page.tsx
  - packages/frontend/src/app/how-it-works/**
  - packages/frontend/src/app/protocols/**
  - packages/frontend/src/app/(authenticated)/design-system/**
  - packages/frontend/src/components/marketing/**
  - packages/frontend/src/components/sidebar/**
  - packages/frontend/src/components/TopBar.tsx
  - packages/frontend/src/components/haven/TransactionActivityRow.tsx
  - packages/frontend/src/components/haven/TransactionMovement.tsx
  - packages/frontend/src/components/transactions/**
last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate # #1749: new "Layering (z-index)" § under Tokens — the shell's stacking order is now a named scale in globals.css, and the mobile nav overlay deliberately outranks the chrome. Only § Tokens re-verified in this pass
---

# Haven Design System

This is the source of truth for Haven's current light visual language. Companion to the product UX guide (`docs/product/README.md`, which documents product doctrine, vocabulary, and IA — those rules **still apply**). If older docs mention a dark app surface system, **this document supersedes them**.

The production authenticated app and `/design-system` are the live references for product UX. The production marketing routes are the live references for marketing UX: `/`, `/how-it-works`, `/protocols/x402`, and `/protocols/mpp`. When in doubt, open the live route, inspect the element, and match the system here.

---

## 1. Tokens

All tokens live as CSS custom properties at `:root` in `packages/frontend/src/app/globals.css`. Core color, radius, and shadow tokens are mirrored in `packages/frontend/tailwind.config.js` so they are usable as `bg-bg`, `text-ink`, `border-border`, etc. Newer production tokens such as typography utilities, raised cards, popovers, modal backdrop, and the brand gradient may exist as CSS variables/classes only until they are promoted into Tailwind.

### Surfaces

| Token | Value | Use |
|---|---|---|
| `--v2-bg` | `#ffffff` | Page background |
| `--v2-surface` | `#f6f9fc` | Alternating section bands, card hover backgrounds |
| `--v2-surface-2` | `#eef2f7` | Disabled states, deeper card stacking |
| `--v2-surface-code` | `#0b1120` | Dark code blocks on light pages (Stripe pattern) |
| `--v2-surface-hover` | `#f0f4f9` | Sidebar/user-menu row hover and subtle interactive shells |
| `--v2-modal-backdrop` | `rgba(26, 31, 54, 0.66)` | Modal backdrop with blur |

### Ink (text)

| Token | Value | Use |
|---|---|---|
| `--v2-ink` | `#1a1f36` | Headings, primary text, amounts |
| `--v2-ink-2` | `#525f7f` | Body text, secondary information |
| `--v2-ink-3` | `#5d6c85` | Tertiary text, eyebrows, captions — AA-safe (≥4.5:1) on white and all tinted surfaces |
| `--v2-ink-on-brand` | `#ffffff` | Text on brand‑colored or dark surfaces |

### Borders

| Token | Value | Use |
|---|---|---|
| `--v2-border` | `#e6ebf1` | Default hairline (cards, dividers) |
| `--v2-border-strong` | `#d6dbe3` | Hover, ghost button borders, flow arrows |

### Brand

| Token | Value | Use |
|---|---|---|
| `--v2-brand` | `#4f46e5` (indigo‑600) | Primary CTA bg, links, accents, brand mark |
| `--v2-brand-strong` | `#4338ca` (indigo‑700) | Primary CTA hover |
| `--v2-brand-soft` | `#eef2ff` | Brand‑tinted card backgrounds, focus rings |
| `--v2-brand-gradient` | `linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)` | Gradient wordmark or one restrained brand accent |

Use `.v2-brand-gradient-text` for the production app wordmark. In product UI, do not use the gradient for buttons, badges, large panels, or repeated decoration.

### Semantic

| Token | Value | Soft variant | Use |
|---|---|---|---|
| `--v2-success` | `#047857` | `--v2-success-soft` `#ecfdf5` | Settled, confirmed, incoming |
| `--v2-debit` | `#0369a1` | `--v2-debit-soft` `#f0f9ff` | Outgoing / sent money (sibling to success; never a warning) |
| `--v2-warning` | `#b54708` | `--v2-warning-soft` `#fef3c7` | 402 Payment Required, pending review |
| `--v2-danger` | `#b42318` | `--v2-danger-soft` `#fef2f2` | Failed, destructive |

Same rule as v1: **never repurpose a semantic color**.

**Contrast guarantee:** every ink and semantic text token meets WCAG AA (≥4.5:1) against white, its own `-soft` background, and the tinted surfaces (`--v2-surface`, `--v2-surface-2`, hover)....
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/product/design-system.md b/docs/product/design-system.md
--- a/docs/product/design-system.md
+++ b/docs/product/design-system.md
@@ -16,7 +16,7 @@ covers:
   - packages/frontend/src/components/haven/TransactionActivityRow.tsx
   - packages/frontend/src/components/haven/TransactionMovement.tsx
   - packages/frontend/src/components/transactions/**
-last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate # #1749: new "Layering (z-index)" § under Tokens — the shell's stacking order is now a named scale in globals.css, and the mobile nav overlay deliberately outranks the chrome. Only § Tokens re-verified in this pass
+last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate # #1749: new "Layering (z-index)" § under Tokens — the shell's stacking order is now a named scale in globals.css, and the mobile nav overlay deliberately outranks the chrome. Only § Tokens re-verified in this pass # #1766: § Buttons' Tap targets rule gains "the rule outlives the primitive" — the mobile sidebar toggle borrows the ::after mechanism as a non-Button, growing in both axes because an icon-only square has no long axis, and must not take `relative`. § Buttons re-read against Button.tsx and sidebar/Sidebar.tsx; nothing else re-verified in this pass
 ---
 
 # Haven Design System
@@ -263,6 +263,39 @@ Consequences worth knowing:
   fight over the same pixels — this is the one new constraint the mechanism introduces.
 - Choosing `size` therefore stays a **density** decision, not an ergonomics one.
 
+**The rule outlives the primitive ([#1766](https://github.com/d-hinders/Haven-AI/issues/1766)).**
+A control that is not a `Button` inherits none of the above automatically, and the
+first one to need it was the mobile sidebar toggle — a hand-rolled 32px square that
+#1749 had just made reachable, so an undersized target went from moot to load-bearing
+on the entry point to primary navigation. It borrows the same mechanism (transparent
+`::after`, paint unchanged) with two deviations worth knowing before you copy it:
+
+- **An icon-only square grows in BOTH axes.** "Vertical only" is not the rule; it is a
+  consequence of a labelled `sm` Button's width already clearing 44px. A 32px square
+  has no long axis, so the overlay is `h-11 w-11` and centred on both. What still
+  applies is the *reason* behind the original rule — check what the widened target now
+  reaches, in **both** states the control has. For the toggle, closed: right box edge
+  x=54, nearest interactive control (`NetworkSwitcher`) at x=68, 14px of clearance.
+  Open: the target floats over the drawer's own logo band, which it already did at 32px
+  — what is asserted there is that the logo link is still reachable at its centre, not
+  that nothing overlaps. Both are pinned in `e2e/mobile-nav-tap-target.mobile.spec.ts`.
+- **Do not add `relative` to an already-positioned element.** `Button` needs it because
+  it is static. A `fixed` or `absolute` control is already a positioning context, and
+  adding `relative` un-fixes it — on the toggle that shifts the whole app shell 32px
+  and drops the control back under `TopBar`, which was #1749. Do not take this on the
+  prose's word: it is a claim about which of two same-property utilities the cascade
+  keeps, so it is pinned by a test rather than by this paragraph —
+  `e2e/mobile-nav-tap-target.mobile.spec.ts` asserts `header.left === 0` as an absolute
+  anchor, and that assertion exists **because** the mutation passed three other mobile
+  specs first.
+
+**Prove it rendered, not in the class string.** A pseudo-element overlay has several
+silent no-op failure modes (a clipping ancestor, a positioning context resolving
+elsewhere, another element winning the band), and none of them exist in jsdom — which
+has no layout, no stacking contexts and no hit-testing. Measure the hit rectangle by
+walking `elementFromPoint` outward from the centre in a real engine; `getBoundingClientRect`
+returns the border box and reports 32×32 even when the overlay works perfectly.
+
 ### Cards (`Card`)
 
 `bg-white border border-[var(--v2-border)] rounded-[10px] shadow-[var(--v2-shadow-card)]`. Padding by use: `p-7` standard, `p-5` compact, `p-7 md:p-10` hero‑adjacent.
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/product/design-system.md @ 2dcd97650c472a572f311bb63731d67257fc1dca -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/frontend/src/app/globals.css
  - packages/frontend/tailwind.config.js
  - packages/frontend/src/components/ui/**
  - packages/frontend/src/app/layout.tsx
  - packages/frontend/src/app/page.tsx
  - packages/frontend/src/app/how-it-works/**
  - packages/frontend/src/app/protocols/**
  - packages/frontend/src/app/(authenticated)/design-system/**
  - packages/frontend/src/components/marketing/**
  - packages/frontend/src/components/sidebar/**
  - packages/frontend/src/components/TopBar.tsx
  - packages/frontend/src/components/haven/TransactionActivityRow.tsx
  - packages/frontend/src/components/haven/TransactionMovement.tsx
  - packages/frontend/src/components/transactions/**
last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate # #1749: new "Layering (z-index)" § under Tokens — the shell's stacking order is now a named scale in globals.css, and the mobile nav overlay deliberately outranks the chrome. Only § Tokens re-verified in this pass # #1766: § Buttons' Tap targets rule gains "the rule outlives the primitive" — the mobile sidebar toggle borrows the ::after mechanism as a non-Button, growing in both axes because an icon-only square has no long axis, and must not take `relative`. § Buttons re-read against Button.tsx and sidebar/Sidebar.tsx; nothing else re-verified in this pass
---

# Haven Design System

This is the source of truth for Haven's current light visual language. Companion to the product UX guide (`docs/product/README.md`, which documents product doctrine, vocabulary, and IA — those rules **still apply**). If older docs mention a dark app surface system, **this document supersedes them**.

The production authenticated app and `/design-system` are the live references for product UX. The production marketing routes are the live references for marketing UX: `/`, `/how-it-works`, `/protocols/x402`, and `/protocols/mpp`. When in doubt, open the live route, inspect the element, and match the system here.

---

## 1. Tokens

All tokens live as CSS custom properties at `:root` in `packages/frontend/src/app/globals.css`. Core color, radius, and shadow tokens are mirrored in `packages/frontend/tailwind.config.js` so they are usable as `bg-bg`, `text-ink`, `border-border`, etc. Newer production tokens such as typography utilities, raised cards, popovers, modal backdrop, and the brand gradient may exist as CSS variables/classes only until they are promoted into Tailwind.

### Surfaces

| Token | Value | Use |
|---|---|---|
| `--v2-bg` | `#ffffff` | Page background |
| `--v2-surface` | `#f6f9fc` | Alternating section bands, card hover backgrounds |
| `--v2-surface-2` | `#eef2f7` | Disabled states, deeper card stacking |
| `--v2-surface-code` | `#0b1120` | Dark code blocks on light pages (Stripe pattern) |
| `--v2-surface-hover` | `#f0f4f9` | Sidebar/user-menu row hover and subtle interactive shells |
| `--v2-modal-backdrop` | `rgba(26, 31, 54, 0.66)` | Modal backdrop with blur |

### Ink (text)

| Token | Value | Use |
|---|---|---|
| `--v2-ink` | `#1a1f36` | Headings, primary text, amounts |
| `--v2-ink-2` | `#525f7f` | Body text, secondary information |
| `--v2-ink-3` | `#5d6c85` | Tertiary text, eyebrows, captions — AA-safe (≥4.5:1) on white and all tinted surfaces |
| `--v2-ink-on-brand` | `#ffffff` | Text on brand‑colored or dark surfaces |

### Borders

| Token | Value | Use |
|---|---|---|
| `--v2-border` | `#e6ebf1` | Default hairline (cards, dividers) |
| `--v2-border-strong` | `#d6dbe3` | Hover, ghost button borders, flow arrows |

### Brand

| Token | Value | Use |
|---|---|---|
| `--v2-brand` | `#4f46e5` (indigo‑600) | Primary CTA bg, links, accents, brand mark |
| `--v2-brand-strong` | `#4338ca` (indigo‑700) | Primary CTA hover |
| `--v2-brand-soft` | `#eef2ff` | Brand‑tinted card backgrounds, focus rings |
| `--v2-brand-gradient` | `linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)` | Gradient wordmark or one restrained brand accent |

Use `.v2-brand-gradient-text` for the production app wordmark. In product UI, do not use the gradient for buttons, badges, large panels, or repeated decoration.

### Semantic

| Token | Value | Soft variant | Use |
|---|---|---|---|
| `--v2-success` | `#047857` | `--v2-success-soft` `#ecfdf5` | Settled, confirmed, incoming |
| `--v2-debit` | `#0369a1` | `--v2-debit-soft` `#f0f9ff` | Outgoing / sent money (sibling to success; never a warning) |
| `--v2-warning` | `#b54708` | `--v2-warning-soft` `#fef3c7` | 402 Payment Required...
```

### `GH-CAND-0012`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1775
- Repository: `d-hinders/Haven-AI`
- PR number: `1775`
- PR title: fix(frontend): stop /transactions clipping 106px of its table on mobile (#1772)
- Language: `typescript`
- Code changed files: `['packages/frontend/e2e/navigation.mobile.spec.ts', 'packages/frontend/src/app/(authenticated)/design-system/page.tsx', 'packages/frontend/src/components/transactions/TransactionsTable.tsx', 'packages/frontend/src/components/ui/Table.tsx']`
- Docs changed files: `['docs/product/design-system.md']`

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
diff --git a/packages/frontend/e2e/navigation.mobile.spec.ts b/packages/frontend/e2e/navigation.mobile.spec.ts
--- a/packages/frontend/e2e/navigation.mobile.spec.ts
+++ b/packages/frontend/e2e/navigation.mobile.spec.ts
@@ -40,28 +40,28 @@ const ROUTES = ['/dashboard', '/agents', '/transactions', '/approvals'] as const
  * rendering and console errors are still asserted — only the overflow
  * assertion is exempted, and only with an issue number.
  *
- * `/transactions` was found by this gate on its first real run, which is the
- * gate working. It is exempted rather than fixed here because fixing it is a
- * rendered-UI change (the table wants an `overflow-x-auto` wrapper) with its
- * own review and its own evidence, and folding that into a CI-plumbing PR
- * would bury it.
+ * **Currently empty, and that is the point.** `/transactions` was the first
+ * and so far only entry: found by this gate on its own first real run, filed
+ * as #1772, exempted by name rather than dropped, and removed again when the
+ * fix landed. The assertion below now gates every route in `ROUTES`.
  *
- * Deliberately NOT a dropped route — that is how a gate quietly stops covering
- * things. Deliberately NOT `test.fail()` either: the measurement proved
- * timing-sensitive on a slow render (see the `found` assertion below), and a
- * `test.fail()` that flips to "expected to fail, but passed" on an unrelated
- * slow frame is a false alarm pointed at the wrong person.
+ * Rules for adding one back, learned from that round trip:
  *
- * Delete the entry when the issue closes; the assertion below is already
- * written and will start gating that route again the moment it goes.
+ *   - Only with an issue number AND the measured numbers, so the next reader
+ *     inherits the diagnosis instead of re-measuring it.
+ *   - Never drop the route instead. That is how a gate quietly stops covering
+ *     things, which is the failure #1768 exists to close.
+ *   - Never `test.fail()` either: the measurement is timing-sensitive on a
+ *     slow render (see the `contentRegionFound` assertion below), and a
+ *     `test.fail()` that flips to "expected to fail, but passed" on an
+ *     unrelated slow frame is a false alarm pointed at the wrong person.
+ *   - Delete the entry in the pull request that fixes the issue — not later.
+ *
+ * Note that this exempts the CONTENT half only. `documentOverflows` is
+ * asserted unconditionally above it and never had an exemption, so a route
+ * listed here is still gated against escaping the shell entirely.
  */
-const KNOWN_CONTENT_OVERFLOW: Partial<Record<(typeof ROUTES)[number], string>> = {
-  '/transactions':
-    '#1772 — transactions table renders without an overflow-x-auto wrapper, ' +
-    'so it drags the WHOLE content pane into horizontal scroll instead of ' +
-    'scrolling itself. Measured 94-124px past a 393px box (it varies with ' +
-    'how many rows render) — on CI and locally alike.',
-}
+const KNOWN_CONTENT_OVERFLOW: Partial<Record<(typeof ROUTES)[number], string>> = {}
 
 /**
  * The local `measureContentOverflow` that used to live here was folded into the

diff --git a/packages/frontend/src/app/(authenticated)/design-system/page.tsx b/packages/frontend/src/app/(authenticated)/design-system/page.tsx
--- a/packages/frontend/src/app/(authenticated)/design-system/page.tsx
+++ b/packages/frontend/src/app/(authenticated)/design-system/page.tsx
@@ -1388,12 +1388,45 @@ export default function DesignSystemPage() {
                 },
               ].map((row) => (
                 <tr key={row.title}>
-                  <td className="px-4 py-4 align-middle">
+                  {/* Narrow gutters below md mirror TransactionsTable (#1772).
+                      Without them this showcase rendered 375px wide inside a
+                      343px Card at 393px — clipped by the Card's
+                      `overflow-hidden`, i.e. the very defect the table below
+                      is meant to document the correct shape of. */}
+                  <td className="px-2 py-4 align-middle md:px-4">
                     <DirectionMark direction={row.direction} />
                   </td>
-                  <td className="px-4 py-4 align-middle">
-                    <div className="flex items-center gap-2">
-                      <p className="text-sm font-semibold text-[var(--v2-ink)]">{row.title}</p>
+                  {/* `max-w-0` BELOW md ONLY. Unconditional, it squashed the
+                      Activity column on DESKTOP too — the visual-regression
+                      gate caught "Recei…" / "x402 …" / "Faile…" at 1280px.
+                      TransactionsTable survives it unconditionally because
+                      every other column there carries an explicit `w-[…]`, so
+                      the leftover flows to Activity; this showcase sizes its
+                      columns purely from content, so capping one collapses it.
+                      Do not drop the `md:` here. */}
+                  <td className="max-w-0 px-4 py-4 align-middle md:max-w-none">
+                    {/* `truncate` + `flex-wrap` mirror TransactionsTable
+                        exactly (#1772). Without `truncate` the `max-w-0`
+                        above word-wraps instead of ellipsising, so the
+                        showcase would teach a shape the real component does
+                        not have. */}
+                    {/* `md:flex-nowrap` for the same reason as `md:max-w-none`
+                        above: this showcase's desktop titles WRAP to two
+                        lines, so a wrapping flex row pushed the Failed badge
+                        onto a third and grew the page by 12px. The visual
+                        gate measured it — 17746 -> 17758 — after the first
+                        attempt at this fix. Desktop must not move at all. */}
+                    <div className="flex flex-wrap items-center gap-x-2 gap-y-1 md:flex-nowrap">
+                      {/* Ellipsise below md, wrap normally at md and up — the
+                          `md:` half restores this showcase's original desktop
+                          rendering byte for byte, so only the mobile baseline
+                          moves. */}
+                      <p
+                        className="truncate text-sm font-semibold text-[var(--v2-ink)] md:overflow-visible md:whitespace-normal md:text-clip"
+                        title={row.title}
+                      >
+                        {row.title}
+                      </p>
                       {row.failed ? <StatusBadge tone="danger">Failed</StatusBadge> : null}
                     </div>
                     <div className="mt-1 md:hidden">
@@ -1409,13 +1442,13 @@ export default function DesignSystemPage() {
                   <td className="hidden px-4 py-4 align-middle text-sm text-[var(--v2-ink-3)] md:table-cell">
                     {row.date}
                   </td>
-                  <td className="px-4 py-4 align-middle text-right">
+                  <td className="px-2 py-4 align-middle text-right md:px-4">
                     <p>
                       <Amount value={row.value} symbol="USDC" direction={row.direction} failed={row.failed} />
                     </p>
                     <p className="mt-1 text-xs text-[var(--v2-ink-3)] md:hidden">{row.date}</p>
                   </td>
-                  <td className="px-4 py-4 align-middle text-right">
+                  <td className="px-2 py-4 align-middle text-right md:px-4">
                     <ExternalDetailsLink href="#" />
                   </td>
                 </tr>

diff --git a/packages/frontend/src/components/transactions/TransactionsTable.tsx b/packages/frontend/src/components/transactions/TransactionsTable.tsx
--- a/packages/frontend/src/components/transactions/TransactionsTable.tsx
+++ b/packages/frontend/src/components/transactions/TransactionsTable.tsx
@@ -104,15 +104,18 @@ interface TransactionsTableProps {
 function LoadingTable({ columns, padY }: { columns: TransactionColumnId[]; padY: string }) {
   const renders: Record<TransactionColumnId, (key: string) => ReactNode> = {
     direction: (key) => (
-      <td key={key} className={`w-9 px-4 ${padY}`}>
+      <td key={key} className={`w-9 px-2 ${padY} md:px-4`}>
         <Skeleton className="h-9 w-9 rounded-[10px]" />
       </td>
     ),
     activity: (key) => (
-      <td key={key} className={`px-4 ${padY}`}>
+      // `max-w-0` for the same reason as the real activity cell below (#1772),
+      // and the skeletons cap at the cell rather than at a fixed 160/224px —
+      // a 224px bar inside a ~109px cell is the loading state's own overflow.
+      <td key={key} className={`max-w-0 px-4 ${padY}`}>
         <div className="space-y-1.5">
-          <Skeleton variant="text" className="h-3 w-40" />
-          <Skeleton variant="text" className="h-2 w-56" />
+          <Skeleton variant="text" className="h-3...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/product/design-system.md @ 258bb89feaa69d436a5d55f8eb2a32981bd6e975 -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/frontend/src/app/globals.css
  - packages/frontend/tailwind.config.js
  - packages/frontend/src/components/ui/**
  - packages/frontend/src/app/layout.tsx
  - packages/frontend/src/app/page.tsx
  - packages/frontend/src/app/how-it-works/**
  - packages/frontend/src/app/protocols/**
  - packages/frontend/src/app/(authenticated)/design-system/**
  - packages/frontend/src/components/marketing/**
  - packages/frontend/src/components/sidebar/**
  - packages/frontend/src/components/TopBar.tsx
  - packages/frontend/src/components/haven/TransactionActivityRow.tsx
  - packages/frontend/src/components/haven/TransactionMovement.tsx
  - packages/frontend/src/components/transactions/**
last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate # #1749: new "Layering (z-index)" § under Tokens — the shell's stacking order is now a named scale in globals.css, and the mobile nav overlay deliberately outranks the chrome. Only § Tokens re-verified in this pass
---

# Haven Design System

This is the source of truth for Haven's current light visual language. Companion to the product UX guide (`docs/product/README.md`, which documents product doctrine, vocabulary, and IA — those rules **still apply**). If older docs mention a dark app surface system, **this document supersedes them**.

The production authenticated app and `/design-system` are the live references for product UX. The production marketing routes are the live references for marketing UX: `/`, `/how-it-works`, `/protocols/x402`, and `/protocols/mpp`. When in doubt, open the live route, inspect the element, and match the system here.

---

## 1. Tokens

All tokens live as CSS custom properties at `:root` in `packages/frontend/src/app/globals.css`. Core color, radius, and shadow tokens are mirrored in `packages/frontend/tailwind.config.js` so they are usable as `bg-bg`, `text-ink`, `border-border`, etc. Newer production tokens such as typography utilities, raised cards, popovers, modal backdrop, and the brand gradient may exist as CSS variables/classes only until they are promoted into Tailwind.

### Surfaces

| Token | Value | Use |
|---|---|---|
| `--v2-bg` | `#ffffff` | Page background |
| `--v2-surface` | `#f6f9fc` | Alternating section bands, card hover backgrounds |
| `--v2-surface-2` | `#eef2f7` | Disabled states, deeper card stacking |
| `--v2-surface-code` | `#0b1120` | Dark code blocks on light pages (Stripe pattern) |
| `--v2-surface-hover` | `#f0f4f9` | Sidebar/user-menu row hover and subtle interactive shells |
| `--v2-modal-backdrop` | `rgba(26, 31, 54, 0.66)` | Modal backdrop with blur |

### Ink (text)

| Token | Value | Use |
|---|---|---|
| `--v2-ink` | `#1a1f36` | Headings, primary text, amounts |
| `--v2-ink-2` | `#525f7f` | Body text, secondary information |
| `--v2-ink-3` | `#5d6c85` | Tertiary text, eyebrows, captions — AA-safe (≥4.5:1) on white and all tinted surfaces |
| `--v2-ink-on-brand` | `#ffffff` | Text on brand‑colored or dark surfaces |

### Borders

| Token | Value | Use |
|---|---|---|
| `--v2-border` | `#e6ebf1` | Default hairline (cards, dividers) |
| `--v2-border-strong` | `#d6dbe3` | Hover, ghost button borders, flow arrows |

### Brand

| Token | Value | Use |
|---|---|---|
| `--v2-brand` | `#4f46e5` (indigo‑600) | Primary CTA bg, links, accents, brand mark |
| `--v2-brand-strong` | `#4338ca` (indigo‑700) | Primary CTA hover |
| `--v2-brand-soft` | `#eef2ff` | Brand‑tinted card backgrounds, focus rings |
| `--v2-brand-gradient` | `linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)` | Gradient wordmark or one restrained brand accent |

Use `.v2-brand-gradient-text` for the production app wordmark. In product UI, do not use the gradient for buttons, badges, large panels, or repeated decoration.

### Semantic

| Token | Value | Soft variant | Use |
|---|---|---|---|
| `--v2-success` | `#047857` | `--v2-success-soft` `#ecfdf5` | Settled, confirmed, incoming |
| `--v2-debit` | `#0369a1` | `--v2-debit-soft` `#f0f9ff` | Outgoing / sent money (sibling to success; never a warning) |
| `--v2-warning` | `#b54708` | `--v2-warning-soft` `#fef3c7` | 402 Payment Required, pending review |
| `--v2-danger` | `#b42318` | `--v2-danger-soft` `#fef2f2` | Failed, destructive |

Same rule as v1: **never repurpose a semantic color**.

**Contrast guarantee:** every ink and semantic text token meets WCAG AA (≥4.5:1) against white, its own `-soft` background, and the tinted surfaces (`--v2-surface`, `--v2-surface-2`, hover)....
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/product/design-system.md b/docs/product/design-system.md
--- a/docs/product/design-system.md
+++ b/docs/product/design-system.md
@@ -325,6 +325,8 @@ Use `components/transactions/TransactionsTable.tsx` for full transaction history
 
 Use `TransactionActivityRow` for compact dashboard, account detail, or agent detail previews.
 
+A collapsing table like this one has to **fit** at mobile widths, not scroll: the `overflow-x-auto` wrapper the `Table` primitive recommends for dense admin tables is mutually exclusive with `Table.Head sticky`, because `overflow-x: auto` forces the computed `overflow-y` to `auto` and the wrapper then becomes the sticky scroll ancestor. When such a table overflows, the cause is usually a `truncate`d cell — `truncate` is `white-space: nowrap`, and an auto-layout column can never be narrower than its min-content, so the untruncated text widens the table instead of ellipsising. Put `max-w-0` on the one flexible cell. Both findings, with their measured numbers, live in `components/ui/Table.tsx`'s docstring ([#1772](https://github.com/d-hinders/Haven-AI/issues/1772)).
+
 ### Sections (`Section`)
 
 Standard rhythm:
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/product/design-system.md @ 411cbdb3ad045e312410df94d141b7595bb9f8fe -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/frontend/src/app/globals.css
  - packages/frontend/tailwind.config.js
  - packages/frontend/src/components/ui/**
  - packages/frontend/src/app/layout.tsx
  - packages/frontend/src/app/page.tsx
  - packages/frontend/src/app/how-it-works/**
  - packages/frontend/src/app/protocols/**
  - packages/frontend/src/app/(authenticated)/design-system/**
  - packages/frontend/src/components/marketing/**
  - packages/frontend/src/components/sidebar/**
  - packages/frontend/src/components/TopBar.tsx
  - packages/frontend/src/components/haven/TransactionActivityRow.tsx
  - packages/frontend/src/components/haven/TransactionMovement.tsx
  - packages/frontend/src/components/transactions/**
last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate # #1749: new "Layering (z-index)" § under Tokens — the shell's stacking order is now a named scale in globals.css, and the mobile nav overlay deliberately outranks the chrome. Only § Tokens re-verified in this pass
---

# Haven Design System

This is the source of truth for Haven's current light visual language. Companion to the product UX guide (`docs/product/README.md`, which documents product doctrine, vocabulary, and IA — those rules **still apply**). If older docs mention a dark app surface system, **this document supersedes them**.

The production authenticated app and `/design-system` are the live references for product UX. The production marketing routes are the live references for marketing UX: `/`, `/how-it-works`, `/protocols/x402`, and `/protocols/mpp`. When in doubt, open the live route, inspect the element, and match the system here.

---

## 1. Tokens

All tokens live as CSS custom properties at `:root` in `packages/frontend/src/app/globals.css`. Core color, radius, and shadow tokens are mirrored in `packages/frontend/tailwind.config.js` so they are usable as `bg-bg`, `text-ink`, `border-border`, etc. Newer production tokens such as typography utilities, raised cards, popovers, modal backdrop, and the brand gradient may exist as CSS variables/classes only until they are promoted into Tailwind.

### Surfaces

| Token | Value | Use |
|---|---|---|
| `--v2-bg` | `#ffffff` | Page background |
| `--v2-surface` | `#f6f9fc` | Alternating section bands, card hover backgrounds |
| `--v2-surface-2` | `#eef2f7` | Disabled states, deeper card stacking |
| `--v2-surface-code` | `#0b1120` | Dark code blocks on light pages (Stripe pattern) |
| `--v2-surface-hover` | `#f0f4f9` | Sidebar/user-menu row hover and subtle interactive shells |
| `--v2-modal-backdrop` | `rgba(26, 31, 54, 0.66)` | Modal backdrop with blur |

### Ink (text)

| Token | Value | Use |
|---|---|---|
| `--v2-ink` | `#1a1f36` | Headings, primary text, amounts |
| `--v2-ink-2` | `#525f7f` | Body text, secondary information |
| `--v2-ink-3` | `#5d6c85` | Tertiary text, eyebrows, captions — AA-safe (≥4.5:1) on white and all tinted surfaces |
| `--v2-ink-on-brand` | `#ffffff` | Text on brand‑colored or dark surfaces |

### Borders

| Token | Value | Use |
|---|---|---|
| `--v2-border` | `#e6ebf1` | Default hairline (cards, dividers) |
| `--v2-border-strong` | `#d6dbe3` | Hover, ghost button borders, flow arrows |

### Brand

| Token | Value | Use |
|---|---|---|
| `--v2-brand` | `#4f46e5` (indigo‑600) | Primary CTA bg, links, accents, brand mark |
| `--v2-brand-strong` | `#4338ca` (indigo‑700) | Primary CTA hover |
| `--v2-brand-soft` | `#eef2ff` | Brand‑tinted card backgrounds, focus rings |
| `--v2-brand-gradient` | `linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)` | Gradient wordmark or one restrained brand accent |

Use `.v2-brand-gradient-text` for the production app wordmark. In product UI, do not use the gradient for buttons, badges, large panels, or repeated decoration.

### Semantic

| Token | Value | Soft variant | Use |
|---|---|---|---|
| `--v2-success` | `#047857` | `--v2-success-soft` `#ecfdf5` | Settled, confirmed, incoming |
| `--v2-debit` | `#0369a1` | `--v2-debit-soft` `#f0f9ff` | Outgoing / sent money (sibling to success; never a warning) |
| `--v2-warning` | `#b54708` | `--v2-warning-soft` `#fef3c7` | 402 Payment Required, pending review |
| `--v2-danger` | `#b42318` | `--v2-danger-soft` `#fef2f2` | Failed, destructive |

Same rule as v1: **never repurpose a semantic color**.

**Contrast guarantee:** every ink and semantic text token meets WCAG AA (≥4.5:1) against white, its own `-soft` background, and the tinted surfaces (`--v2-surface`, `--v2-surface-2`, hover)....
```

### `GH-CAND-0013`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1776
- Repository: `d-hinders/Haven-AI`
- PR number: `1776`
- PR title: test(frontend): make the horizontal-overflow guard able to fail inside the app shell (#1771)
- Language: `typescript`
- Code changed files: `['packages/frontend/e2e/auth.spec.ts', 'packages/frontend/e2e/connect-agent.spec.ts', 'packages/frontend/e2e/dashboard.spec.ts', 'packages/frontend/e2e/fixtures/haven-api.ts', 'packages/frontend/e2e/hosted-mcp.spec.ts', 'packages/frontend/e2e/navigation.mobile.spec.ts', 'packages/frontend/e2e/transactions-detail.spec.ts']`
- Docs changed files: `['docs/contributing/ship-playbooks/frontend.md', 'docs/operations/e2e-qa-runbook.md']`

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
diff --git a/packages/frontend/e2e/auth.spec.ts b/packages/frontend/e2e/auth.spec.ts
--- a/packages/frontend/e2e/auth.spec.ts
+++ b/packages/frontend/e2e/auth.spec.ts
@@ -17,6 +17,11 @@ test.describe('authentication flows', () => {
     await expect(page).toHaveURL(/\/login$/)
     await expect(page.getByRole('heading', { name: 'Welcome back' })).toBeVisible()
     await expect(page.getByRole('button', { name: 'Log in' })).toBeVisible()
+    // `/login` is OUTSIDE the authenticated shell, so it has no
+    // `#main-content` and no clipping ancestor: the document metric is the one
+    // that works here, and this is the only call site in the repo where it was
+    // already gating on its own (#1771). Deliberately does not assert
+    // `contentRegionFound` — there is legitimately no content region.
     expect(await expectNoHorizontalOverflow(page)).toMatchObject({ hasOverflow: false })
     expect(unexpectedBrowserErrors(browserErrors)).toEqual([])
   })
@@ -36,7 +41,10 @@ test.describe('authentication flows', () => {
     await expect(page.getByText('$1,250.00')).toBeVisible()
     await expect(page.getByRole('link', { name: /Research agent Connected/ })).toBeVisible()
     await expect(page.getByRole('link', { name: 'Open approvals' })).toBeVisible()
-    expect(await expectNoHorizontalOverflow(page)).toMatchObject({ hasOverflow: false })
+    expect(await expectNoHorizontalOverflow(page)).toMatchObject({
+      hasOverflow: false,
+      contentRegionFound: true,
+    })
     expect(unexpectedBrowserErrors(browserErrors)).toEqual([])
   })
 
@@ -52,7 +60,10 @@ test.describe('authentication flows', () => {
     await expect(page.getByText('Total balance')).toBeVisible()
     await expect(page.getByRole('button', { name: 'Send' })).toBeVisible()
     await expect(page.getByRole('button', { name: 'Receive' })).toBeVisible()
-    expect(await expectNoHorizontalOverflow(page)).toMatchObject({ hasOverflow: false })
+    expect(await expectNoHorizontalOverflow(page)).toMatchObject({
+      hasOverflow: false,
+      contentRegionFound: true,
+    })
     expect(unexpectedBrowserErrors(browserErrors)).toEqual([])
   })
 })

diff --git a/packages/frontend/e2e/connect-agent.spec.ts b/packages/frontend/e2e/connect-agent.spec.ts
--- a/packages/frontend/e2e/connect-agent.spec.ts
+++ b/packages/frontend/e2e/connect-agent.spec.ts
@@ -59,7 +59,14 @@ test.describe('Connect agent setup acceptance', () => {
     await expect(dialog.getByText(/Connect a wallet or use a passkey/i)).toBeVisible()
     await expect(dialog).not.toContainText(/delegate_key|private_key|privateKey|HAVEN_DELEGATE_KEY/)
 
-    expect(await expectNoHorizontalOverflow(page)).toMatchObject({ hasOverflow: false })
+    // Measures `/agents` BEHIND the dialog, not the dialog. A fixed-position
+    // overlay contributes to neither scroll box — see the blind spot noted on
+    // `expectNoHorizontalOverflow` (#1771). Checking the dialog's own box is
+    // #1773.
+    expect(await expectNoHorizontalOverflow(page)).toMatchObject({
+      hasOverflow: false,
+      contentRegionFound: true,
+    })
     expect(unexpectedBrowserErrors(browserErrors)).toEqual([])
   })
 })

diff --git a/packages/frontend/e2e/dashboard.spec.ts b/packages/frontend/e2e/dashboard.spec.ts
--- a/packages/frontend/e2e/dashboard.spec.ts
+++ b/packages/frontend/e2e/dashboard.spec.ts
@@ -34,7 +34,14 @@ test.describe('dashboard browser UX', () => {
     await expect(modal.getByText('Operations')).toBeVisible()
     await expect(modal.getByText('Base', { exact: true })).toBeVisible()
     await expect(modal.getByText(testSafeAddress)).toBeVisible()
-    expect(await expectNoHorizontalOverflow(page)).toMatchObject({ hasOverflow: false })
+    // Measures the dashboard BEHIND the modal, not the modal. A fixed-position
+    // overlay contributes to neither scroll box — see the blind spot noted on
+    // `expectNoHorizontalOverflow` (#1771), measured rather than assumed.
+    // Checking the modal's own box is #1773.
+    expect(await expectNoHorizontalOverflow(page)).toMatchObject({
+      hasOverflow: false,
+      contentRegionFound: true,
+    })
     expect(unexpectedBrowserErrors(browserErrors)).toEqual([])
   })
 
@@ -49,7 +56,10 @@ test.describe('dashboard browser UX', () => {
     await expect(page.getByRole('heading', { name: 'Approvals' })).toBeVisible()
     await expect(page.getByText('Research agent', { exact: true })).toBeVisible()
     await expect(page.getByText('12.50 USDC')).toBeVisible()
-    expect(await expectNoHorizontalOverflow(page)).toMatchObject({ hasOverflow: false })
+    expect(await expectNoHorizontalOverflow(page)).toMatchObject({
+      hasOverflow: false,
+      contentRegionFound: true,
+    })
     expect(unexpectedBrowserErrors(browserErrors)).toEqual([])
   })
 })

diff --git a/packages/frontend/e2e/fixtures/haven-api.ts b/packages/frontend/e2e/fixtures/haven-api.ts
--- a/packages/frontend/e2e/fixtures/haven-api.ts
+++ b/packages/frontend/e2e/fixtures/haven-api.ts
@@ -478,17 +478,126 @@ export async function dismissMobileSidebar(page: Page) {
   }
 }
 
+/**
+ * Horizontal overflow, measured on BOTH scroll boxes that can hold it.
+ *
+ * ## Why there are two metrics (#1771)
+ *
+ * This helper used to compare the document alone —
+ * `documentElement.scrollWidth` / `body.scrollWidth` against
+ * `documentElement.clientWidth`. Inside the authenticated shell that
+ * comparison **cannot fail**. `(authenticated)/layout.tsx` wraps everything in
+ * `overflow-hidden` twice (the `flex h-screen … overflow-hidden` root and the
+ * `flex-1 flex flex-col min-w-0 overflow-hidden` column), so overflowing
+ * content never grows the document and the old metric reported a clean fit.
+ *
+ * That is worse than no check, because it gets cited as evidence. It was found
+ * only by mutation — #1768 shipped a deliberate `w-[120vw]` on `/dashboard`
+ * and CI run 32542736317 went green, with the overflow assertion explicitly
+ * passing.
+ *
+ * So the document metric is kept — it is the ONLY one that works on
+ * unauthenticated pages like `/login`, which have no shell and no
+ * `#main-content` — and the content-region metric is added beside it.
+ *
+ * ## What each metric actually means — they are DIFFERENT defects
+ *
+ * Do not collapse these two into "content is off-screen"; the next person
+ * debugging a failure needs to know which one fired.
+ *
+ * - `documentOverflows` — something escaped the page box itself. Where the
+ *   ancestors are `overflow-hidden` (the authenticated shell) this means the
+ *   content really is CLIPPED and unreachable, with no scrollbar anywhere.
+ *
+ * - `contentOverflows` — `<main id="main-content">` is wider than its own box.
+ *   `<main>` is `overflow-y-auto`, and per CSS Overflow §3 setting one axis to
+ *   a non-`visible` value computes the OTHER axis to `auto`, so its
+ *   `overflow-x` is `auto` and it is a genuine horizontal scroll box.
+ *   Measured directly rather than reasoned about: with a 120vw child at 393px,
+ *   `getComputedStyle(main).overflowX === 'auto'` and `main.scrollLeft` moves
+ *   to 79 — so the content is REACHABLE by scrolling the pane.
+ *
+ *   That is still a real defect, and it is the #1772 shape: one wide element
+ *   drags the WHOLE content pane into horizontal scroll — headings, cards and
+ *   all — instead of scrolling only itself inside an `overflow-x-auto`
+ *   wrapper. Read a `contentOverflows` failure as "the entire content pane is
+ *   forced into horizontal scroll", NOT as "the content cannot be reached".
+ *
+ * `hasOverflow` is the UNION, so every existing
+ * `toMatchObject({ hasOverflow: false })` call site starts gating for real
+ * without changing shape. The two booleans are also returned separately for a
+ * caller that needs to say which one it means.
+ *
+ * ## Assert `contentRegionFound` on authenticated routes
+ *
+ * When the content region is absent — or attached but not laid out — the
+ * content metric degrades to `0`, which reads as "fits": the silent no-op that
+ * this whole helper exists to prevent. So `contentRegionFound` requires a
+ * NON-ZERO `clientWidth`, not merely a node in the DOM; a hydration flash, a
+ * `display:none` mid-transition or a failed stylesheet all produce an attached
+ * `<main>` measuring `0 - 0 = 0`. The helper cannot tell on its own whether a
+ * page SHOULD have a content region, so authenticated call sites pass
+ * `{ hasOverflow: false, contentRegionFound: true }` and make the no-op path
+ * loud. `/login` legitimately has no content region and asserts only
+ * `hasOverflow`.
+ *
+ * ## Known blind spot, and it is structural
+ *
+ * This compares TWO scroll boxes; it does not walk the ancestor chain. So any
+ * `overflow-hidden` BETWEEN the two measured boxes swallows the evidence
+ * before either one sees it — a card inside `<main>` that clips a decorative
+ * element, and one day clips real content, recreates the exact #1768 failure
+ * one level...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/contributing/ship-playbooks/frontend.md @ c718f1c76b42b0ebabf3bc9d102d93d9618a5534 -->
---
owner: "@d-hinders"
status: current
covers: []  # narrative — process playbook
last-verified: "2026-08-22" # #1768: §4 gains the viewport-coverage table — both Playwright projects gate on every PR now, and `*.mobile.spec.ts` is how you write a mobile test. Prior: #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
---

# Frontend playbook

Loaded by `ship-next` for `area:frontend` issues. The goal: a UI issue is shipped on Haven's UX standards without the contributor having to name them. This playbook **links** the standards; it does not restate them.

## 1. Required reading (before implementing)

Read, in order — these are `AGENTS.md` → "Required Reading For UI Work":

1. [`product/README.md`](../../product/README.md) — product doctrine, IA, money-movement clarity, accessibility, and closeout checks.
2. [`product/design-system.md`](../../product/design-system.md) — tokens, typography, cards, buttons, motion, surface hierarchy.
3. [`product/copy-guidelines.md`](../../product/copy-guidelines.md) — user-facing wording and banned technical terms.
4. [`product/screen-recipes.md`](../../product/screen-recipes.md) — repeatable screen structures.
5. [`product/design-review.md`](../../product/design-review.md) — the finishing checklist (also used in §5).

If a `/design-system` route exists, inspect it before editing UX.

## 2. Reuse first

Inspect `packages/frontend/src/components/ui` (primitives) and `packages/frontend/src/components/haven` (domain components) before adding UI. Prefer composition; do **not** invent new card styles, spacing, shadows, radius, or typography unless the existing system genuinely can't express the need. Use the v2 tokens in `globals.css` and the Tailwind aliases.

**Absorb a pattern on its 2nd occurrence, not its 12th ([#901](https://github.com/d-hinders/Haven-AI/issues/901)).** If this diff writes the same markup shape a second time — a header band, badge, row, empty-state, inline `<svg>`, address slice — or re-creates something a primitive already covers, extract it into a `ui/`/`haven/` primitive **and** document it on `/design-system`, in this same PR. This is the Captain Self-Check Preflight's **Pattern Absorption** item; it's the mechanism that prevents the debt clusters epic #859 had to clean retroactively. Only skip it if the two uses will genuinely diverge — and say so.

**A new primitive must land on `/design-system` in the same PR ([#898](https://github.com/d-hinders/Haven-AI/issues/898)).** The design-system coupling gate flags any exported component added under `components/ui/**` or `components/haven/**` whose symbol never appears on `app/(authenticated)/design-system/page.tsx`. Two CI jobs, on every PR however it was opened ([#1023](https://github.com/d-hinders/Haven-AI/issues/1023)): **Design-system coupling** posts the sticky comment that explains the finding, and **Design-system coupling (strict)** blocks on it. Add a showcase entry (usage + variants) alongside the primitive, or — for a genuinely internal export, not a reusable primitive — mark the export line `// design-system-exempt: <reason>`. Check locally with `node packages/frontend/scripts/design-system-coupling.mjs --strict`.

## 3. Captain Self-Check Preflight

Run the matching items from the **Captain Self-Check Preflight** in [`../ai-agent-workflow.md`](../ai-agent-workflow.md) for the traps the diff touches — e.g. numeric formatters, counter/summary buckets, conditional copy predicates, async hook generations, signer-readiness gates, animation discipline, inline-gate placement, cross-surface display drift, loading-state inference. Each is one grep or one quick read. Do this **before** review so the reviewer finds fewer issues.

## 4. Verification

Verify the change in the **browser**, or — when the browser path is unavailable/flaky — add a **named headless equivalent** (vitest) that covers the skipped animation, layout, routing, loading, or interaction risk. Include empty, loading, error, and success states when the screen can enter them; check mobile and desktop.

**Which viewports actually gate ([#1768](https://github.com/d-hinders/Haven-AI/issues/1768)).** The *Frontend browser smoke* job runs **both** Playwright projects on every frontend PR, with no dispatch required:

| Project | Emulation | Runs | Gates a PR |
|---|---|---|---|
| `chromium-desktop` | Desktop Chrome — 1280×720 viewport, fine pointer, no touch, DSF 1 | every `e2e/*.spec.ts` **except** `*.mobile.spec.ts` | yes |
| `chromium-mobile` | **Pixel 5** — 393×727 viewport, coarse pointer, touch, Android UA, DSF 2.75 | `e2e/*.mobile.spec.ts` only | yes |

(Numbers read off Playwright's own `devices` table at the pinned version, not from memory. Pixel 5's `screen` is 393×851; the **viewport** — what the page actually gets — is 393×727.)

Both projects also inherit `SUITE_IGNORE` (`e2e/live...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/contributing/ship-playbooks/frontend.md b/docs/contributing/ship-playbooks/frontend.md
--- a/docs/contributing/ship-playbooks/frontend.md
+++ b/docs/contributing/ship-playbooks/frontend.md
@@ -2,7 +2,7 @@
 owner: "@d-hinders"
 status: current
 covers: []  # narrative — process playbook
-last-verified: "2026-08-22" # #1768: §4 gains the viewport-coverage table — both Playwright projects gate on every PR now, and `*.mobile.spec.ts` is how you write a mobile test. Prior: #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
+last-verified: "2026-08-22" # #1771: §4's overflow paragraph rewritten — the shared helper now measures `<main>`'s scroll box too and CAN fail inside the shell; separates `documentOverflows` (unreachable) from `contentOverflows` (whole pane forced into horizontal scroll), and names the two-scroll-box measurement's structural limits. Prior: #1768: §4 gains the viewport-coverage table — both Playwright projects gate on every PR now, and `*.mobile.spec.ts` is how you write a mobile test. Prior: #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
 ---
 
 # Frontend playbook
@@ -54,7 +54,9 @@ Before #1768, `chromium-mobile` existed but only a `workflow_dispatch` with `ui_
 
 **Writing a mobile test:** name the file `*.mobile.spec.ts` and it runs under real Pixel 5 emulation. Do **not** reach for `test.use({ viewport: … })` inside a desktop spec — it narrows the window but leaves `maxTouchPoints` at 0, the pointer fine and the UA desktop, so touch and hit-testing behaviour is not actually covered. Conversely, keep viewport-independent behaviour out of `*.mobile.spec.ts`: the two projects run disjoint spec sets on purpose, and duplicating a spec buys nothing but CI minutes. `e2e/navigation.mobile.spec.ts` is the reference, including the meta-guard that fails if the project ever stops being device-emulated.
 
-**Measure overflow on the scroll box, not the document.** The authenticated shell is `overflow-hidden`, so content wider than the screen is *clipped* rather than growing `documentElement.scrollWidth` — which means the page-level `expectNoHorizontalOverflow` helper **cannot fail** on any authenticated route ([#1771](https://github.com/d-hinders/Haven-AI/issues/1771)). This was found by the #1768 mutation, not by reading. Compare `<main id="main-content">`'s own `scrollWidth` against its `clientWidth`; `navigation.mobile.spec.ts`'s `measureContentOverflow` is the reference. Clipped content on mobile is *unreachable*, not merely ugly, so this is the assertion that matters.
+**Measure overflow on the scroll box, not the document.** The authenticated shell is `overflow-hidden`, so content wider than the screen never grows `documentElement.scrollWidth` — which meant the page-level `expectNoHorizontalOverflow` helper **could not fail** on any authenticated route. Found by the #1768 mutation, not by reading, and fixed in [#1771](https://github.com/d-hinders/Haven-AI/issues/1771): the shared helper now measures `<main id="main-content">`'s own scroll box alongside the document, and `hasOverflow` is the union, so every caller gates for real. Assert `contentRegionFound: true` on authenticated routes — otherwise a `<main>` that is missing or not yet laid out measures `0` and reads as "fits".
+
+Two failure modes, and they are not the same defect: `documentOverflows` means content escaped the page box and — under the shell's `overflow-hidden` — is genuinely **unreachable**; `contentOverflows` means `<main>` (which is `overflow-y-auto`, so `overflow-x` computes to `auto`) is wider than its box, dragging the **whole content pane into horizontal scroll** instead of the offending element scrolling inside its own `overflow-x-auto` wrapper. The second is reachable but wrong — it is the [#1772](https://github.com/d-hinders/Haven-AI/issues/1772) shape. Note the measurement compares two scroll boxes rather than walking ancestors, so an `overflow-hidden` *between* them still hides evidence; `position: fixed` overlays are invisible to both ([#1773](https://github.com/d-hinders/Haven-AI/issues/1773)).
 
 **A known, filed defect is exempted by name, never by deletion.** `navigation.mobile.spec.ts` keeps a `KNOWN_CONTENT_OVERFLOW` map: the route still runs and still asserts rendering and console cleanliness, only the one known-failing assertion is skipped, and only with an issue number and the measured numbers next to it. Dropping the route instead is how a gate quietly stops covering things — which is the defect #1768 exists to close. Delete the entry in the PR that fixes the issue.

diff --git a/docs/operations/e2e-qa-runbook.md b/docs/operations/e2e-qa-runbook.md
--- a/docs/operations/e2e-qa-runbook.md
+++ b/docs/operations/e2e-qa-runbook.md
@@ -23,7 +23,7 @@ covers:
   - packages/frontend/src/lib/transaction-csv.ts
   - packages/frontend/src/lib/__tests__/transaction-csv.test.ts
   - docs/bug-reports/_run-report-template.md
-last-verified: "2026-08-21" # #1682: the per-environment run list notes the name-first picker (a row per environment again); steps themselves unchanged. Prior: #1672: noted the collapsed AI-agent picker entry in the per-environment run list; steps themselves unchanged. Prior: #1346 runtime-specific activation + read-only Connect verification re-checked; #1330 Hermes .env credential-reference verification
+last-verified: "2026-08-22" # #1771: corrected the "Already automated" row that credited `hosted-mcp.spec.ts` with mobile-overflow coverage — that test asserted a helper which could not fail inside the app shell and was removed; mobile overflow is covered by `navigation.mobile.spec.ts` under Pixel 5 emulation. Scope of this re-verification: the "Already automated" table only; the hand-test steps were NOT re-run. Prior: #1682: the per-environment run list notes the name-first picker (a row per environment again); steps themselves unchanged. Prior: #1672: noted the collapsed AI-agent picker entry in the per-environment run list; steps themselves unchanged. Prior: #1346 runtime-specific activation + read-only Connect verification re-checked; #1330 Hermes .env credential-reference verification
 ---
 
 # E2E QA runbook — agent connection (#419) & x402 payments (#420)
@@ -50,7 +50,8 @@ document for the remaining exploratory checklist.
 | Base Sepolia money-flow invariants: settle, queue, reject, x402 settle, sweep recovery | `packages/qa-agent`; local `npm run qa:dev -w packages/qa-agent` or Actions `qa-dev.yml` |
 | Unmocked login/dashboard smoke against a Vercel preview + dev backend | `packages/frontend/e2e/live`; local `test:e2e:live` or Actions `qa-live.yml` |
 | Connect-agent modal: create setup → prompt → connected-local → approval screen, no secrets leaked | `e2e/connect-agent.spec.ts` |
-| Hosted-MCP agent/allowance/CTA states and mobile overflow | `e2e/hosted-mcp.spec.ts` |
+| Hosted-MCP agent/allowance/CTA states | `e2e/hosted-mcp.spec.ts` |
+| Mobile-viewport layout overflow on the primary authenticated routes | `e2e/navigation.mobile.spec.ts` (Pixel 5 emulation, gates every PR since #1770) |
 | Hosted connect copy, commands, and deep-link behavior | `HostedConnectCard.test.tsx`; `hosted-connect.test.ts` |
 | **x402 tx displays in history + opens the per-type detail panel** (#420 UI half) | `e2e/transactions-detail.spec.ts` |
 | Approver add/remove/reuse/passkey logic, last-owner guard | unit tests (`ManageApprovers`, `safe-owner-tx`, route tests) |
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/contributing/ship-playbooks/frontend.md @ bae60ad7c3db30c099641bbef842a2c80a351336 -->
---
owner: "@d-hinders"
status: current
covers: []  # narrative — process playbook
last-verified: "2026-08-22" # #1771: §4's overflow paragraph rewritten — the shared helper now measures `<main>`'s scroll box too and CAN fail inside the shell; separates `documentOverflows` (unreachable) from `contentOverflows` (whole pane forced into horizontal scroll), and names the two-scroll-box measurement's structural limits. Prior: #1768: §4 gains the viewport-coverage table — both Playwright projects gate on every PR now, and `*.mobile.spec.ts` is how you write a mobile test. Prior: #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
---

# Frontend playbook

Loaded by `ship-next` for `area:frontend` issues. The goal: a UI issue is shipped on Haven's UX standards without the contributor having to name them. This playbook **links** the standards; it does not restate them.

## 1. Required reading (before implementing)

Read, in order — these are `AGENTS.md` → "Required Reading For UI Work":

1. [`product/README.md`](../../product/README.md) — product doctrine, IA, money-movement clarity, accessibility, and closeout checks.
2. [`product/design-system.md`](../../product/design-system.md) — tokens, typography, cards, buttons, motion, surface hierarchy.
3. [`product/copy-guidelines.md`](../../product/copy-guidelines.md) — user-facing wording and banned technical terms.
4. [`product/screen-recipes.md`](../../product/screen-recipes.md) — repeatable screen structures.
5. [`product/design-review.md`](../../product/design-review.md) — the finishing checklist (also used in §5).

If a `/design-system` route exists, inspect it before editing UX.

## 2. Reuse first

Inspect `packages/frontend/src/components/ui` (primitives) and `packages/frontend/src/components/haven` (domain components) before adding UI. Prefer composition; do **not** invent new card styles, spacing, shadows, radius, or typography unless the existing system genuinely can't express the need. Use the v2 tokens in `globals.css` and the Tailwind aliases.

**Absorb a pattern on its 2nd occurrence, not its 12th ([#901](https://github.com/d-hinders/Haven-AI/issues/901)).** If this diff writes the same markup shape a second time — a header band, badge, row, empty-state, inline `<svg>`, address slice — or re-creates something a primitive already covers, extract it into a `ui/`/`haven/` primitive **and** document it on `/design-system`, in this same PR. This is the Captain Self-Check Preflight's **Pattern Absorption** item; it's the mechanism that prevents the debt clusters epic #859 had to clean retroactively. Only skip it if the two uses will genuinely diverge — and say so.

**A new primitive must land on `/design-system` in the same PR ([#898](https://github.com/d-hinders/Haven-AI/issues/898)).** The design-system coupling gate flags any exported component added under `components/ui/**` or `components/haven/**` whose symbol never appears on `app/(authenticated)/design-system/page.tsx`. Two CI jobs, on every PR however it was opened ([#1023](https://github.com/d-hinders/Haven-AI/issues/1023)): **Design-system coupling** posts the sticky comment that explains the finding, and **Design-system coupling (strict)** blocks on it. Add a showcase entry (usage + variants) alongside the primitive, or — for a genuinely internal export, not a reusable primitive — mark the export line `// design-system-exempt: <reason>`. Check locally with `node packages/frontend/scripts/design-system-coupling.mjs --strict`.

## 3. Captain Self-Check Preflight

Run the matching items from the **Captain Self-Check Preflight** in [`../ai-agent-workflow.md`](../ai-agent-workflow.md) for the traps the diff touches — e.g. numeric formatters, counter/summary buckets, conditional copy predicates, async hook generations, signer-readiness gates, animation discipline, inline-gate placement, cross-surface display drift, loading-state inference. Each is one grep or one quick read. Do this **before** review so the reviewer finds fewer issues.

## 4. Verification

Verify the change in the **browser**, or — when the browser path is unavailable/flaky — add a **named headless equivalent** (vitest) that covers the skipped animation, layout, routing, loading, or interaction risk. Include empty, loading, error, and success states when the screen can enter them; check mobile and desktop.

**Which viewports actually gate ([#1768](https://github.com/d-hinders/Haven-AI/issues/1768)).** The *Frontend browser smoke* job runs **both** Playwright projects on every frontend PR, with no dispatch required:

| Project | Emulation | Runs | Gates a PR |
|---|---|---|---|
| `chromium-desktop` | Desktop Chrome — 1280×720 viewport, fine pointer, no touch, DSF 1 | every `e2e/*.spec.ts` **except** `*.mobile.spec.ts` | yes |
| `chromium-mobile` | **Pixel 5** — 393×727 viewport, coarse p...
```

### `GH-CAND-0014`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1770
- Repository: `d-hinders/Haven-AI`
- PR number: `1770`
- PR title: ci(frontend): gate every PR on a real mobile viewport (#1768)
- Language: `typescript`
- Code changed files: `['.github/workflows/ci.yml', 'packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts', 'packages/frontend/e2e/navigation.mobile.spec.ts', 'packages/frontend/package.json', 'packages/frontend/playwright.config.ts']`
- Docs changed files: `['docs/bug-reports/_run-report-template.md', 'docs/contributing/pr-workflow-checklist.md', 'docs/contributing/ship-playbooks/frontend.md']`

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
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -5,16 +5,12 @@ on:
     branches: [main, dev]
   pull_request:
     branches: [main, dev]
+  # #1768: the `ui_suite` choice input is gone. Its only purpose was to select
+  # between the desktop-only browser suite and "desktop + mobile"; both
+  # projects now gate on every pull request, so the input selected between a
+  # thing and itself — a control that looks like it widens coverage while
+  # doing nothing is the same defect this issue closed one layer up.
   workflow_dispatch:
-    inputs:
-      ui_suite:
-        description: Browser test suite to run
-        required: true
-        default: full
-        type: choice
-        options:
-          - desktop
-          - full
 
 concurrency:
   group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
@@ -511,16 +507,21 @@ jobs:
         run: npx playwright install --with-deps chromium
         working-directory: packages/frontend
 
-      - name: Run frontend browser smoke tests
-        if: github.event_name != 'workflow_dispatch' || inputs.ui_suite != 'full'
-        run: npm run test:e2e:desktop -w packages/frontend
-        env:
-          NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID: ci-placeholder
-          NEXT_TELEMETRY_DISABLED: 1
-
-      - name: Run full frontend browser tests
-        if: github.event_name == 'workflow_dispatch' && inputs.ui_suite == 'full'
-        run: npm run test:e2e:full -w packages/frontend
+      # #1768: BOTH Playwright projects gate here, unconditionally — desktop
+      # (Desktop Chrome) and mobile (Pixel 5 device emulation). This step used
+      # to run `test:e2e:desktop` only, with `chromium-mobile` reachable solely
+      # via a `workflow_dispatch` with `ui_suite=full`. That meant no mobile
+      # viewport was exercised on any pull request, while a configured project
+      # made it look like one was — which is how #1749 shipped a primary
+      # navigation that could not be opened below `lg`.
+      #
+      # The projects run disjoint spec sets (`*.mobile.spec.ts` → mobile,
+      # everything else → desktop), so this is one browser project more, not
+      # the whole suite twice; the reasoning lives in `playwright.config.ts`
+      # next to the `testMatch`/`testIgnore` that implement it. One command,
+      # not two steps, so a single Next server boot serves both projects.
+      - name: Run frontend browser smoke tests (desktop + mobile)
+        run: npm run test:e2e:gate -w packages/frontend
         env:
           NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID: ci-placeholder
           NEXT_TELEMETRY_DISABLED: 1

diff --git a/packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts b/packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts
--- a/packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts
+++ b/packages/frontend/e2e/mobile-nav-layering.mobile.spec.ts
@@ -28,13 +28,27 @@ import { mockHavenApi, seedAuthenticatedSession } from './fixtures/haven-api'
  * actionable" do not exist there in any meaningful form. The defect is purely
  * a rendered-layout property. Only a real engine can see it.
  *
- * ── Why it declares its own viewport ────────────────────────────────────────
- * The gating CI job runs `test:e2e:desktop` (`--project=chromium-desktop`);
- * the `chromium-mobile` project runs only on a manual `ui_suite=full`
- * dispatch. A mobile-project spec therefore would NOT gate a pull request —
- * which is a large part of why this survived. `test.use({ viewport })`
- * overrides the project's viewport, so these run inside the desktop project
- * and are genuinely blocking.
+ * ── Which project this runs in, and why it still declares viewports ─────────
+ * This was `mobile-nav-layering.spec.ts` in `chromium-desktop`, using
+ * `test.use({ viewport })` — for the reason its original header stated
+ * plainly: the gating CI job ran `test:e2e:desktop`, `chromium-mobile` ran
+ * only on a manual `ui_suite=full` dispatch, and so a mobile-project spec
+ * would not have gated a pull request at all. #1768 removed that constraint.
+ * Both projects now gate every PR, `*.mobile.spec.ts` selects into the Pixel 5
+ * one, and the workaround is retired: the spec lives in the project it always
+ * belonged to.
+ *
+ * The gain is not cosmetic. A viewport override inside `chromium-desktop`
+ * leaves `maxTouchPoints` at 0, `pointer: coarse` false and the UA desktop —
+ * so every hit-test below was being answered for a MOUSE in a narrow window.
+ * They now run under real device emulation, which is the pointer a phone
+ * actually uses, on the one defect class where that distinction is the whole
+ * point.
+ *
+ * `test.use({ viewport })` stays, and is no longer a lie about the project: a
+ * project pins ONE viewport, and the point of this spec is the sweep across
+ * the band the toggle is `lg:hidden` for. The override sets the width; the
+ * touch/UA emulation the project provides is unaffected by it.
  */
 
 // The toggle is `lg:hidden`, so everything from the narrowest phone up to one

diff --git a/packages/frontend/e2e/navigation.mobile.spec.ts b/packages/frontend/e2e/navigation.mobile.spec.ts
--- a/packages/frontend/e2e/navigation.mobile.spec.ts
+++ b/packages/frontend/e2e/navigation.mobile.spec.ts
@@ -0,0 +1,201 @@
+/**
+ * Mobile-viewport gating smoke (#1768).
+ *
+ * Runs under the `chromium-mobile` project (Pixel 5 device emulation) — see the
+ * project comment in `playwright.config.ts`. This file exists because until
+ * #1768 no mobile viewport gated a pull request at all: `chromium-mobile` was
+ * configured but only a manual `workflow_dispatch` ever ran it, so #1749 (the
+ * "Open sidebar" toggle hit-tested under `TopBar` and unopenable below `lg` on
+ * every authenticated route) could ship without a single check going red.
+ *
+ * WHAT BELONGS HERE: behaviour that is only wrong at a small width or under a
+ * touch pointer — layout overflow, hit-testing, tap targets, mobile-only
+ * disclosure. Behaviour that does not depend on the viewport belongs in the
+ * desktop specs; duplicating it here just doubles CI time.
+ *
+ * WHAT DOES NOT BELONG HERE: anything carrying committed SCREENSHOT BASELINES.
+ * `design-system.visual.spec.ts` sets its own viewports and its baselines are
+ * captured at deviceScaleFactor 1 with no project suffix in the filename;
+ * re-running it under Pixel 5's DSF 2.75 would fail on scale rather than on a
+ * defect. Note the rule is about baselines, not about setting a viewport —
+ * `mobile-nav-layering.mobile.spec.ts` sweeps five widths in this project quite
+ * happily, because it compares geometry rather than pixels.
+ */
+import { expect, test, type Page } from '@playwright/test'
+import {
+  collectBrowserErrors,
+  expectNoHorizontalOverflow,
+  mockHavenApi,
+  seedAuthenticatedSession,
+  unexpectedBrowserErrors,
+} from './fixtures/haven-api'
+
+// Authenticated routes a user reaches from primary navigation. Each is checked
+// for the one failure mode that is invisible at 1280px: content wider than the
+// screen.
+const ROUTES = ['/dashboard', '/agents', '/transactions', '/approvals'] as const
+
+/**
+ * Routes with a KNOWN, FILED content-overflow defect. The route still runs —
+ * rendering and console errors are still asserted — only the overflow
+ * assertion is exempted, and only with an issue number.
+ *
+ * `/transactions` was found by this gate on its first real run, which is the
+ * gate working. It is exempted rather than fixed here because fixing it is a
+ * rendered-UI change (the table wants an `overflow-x-auto` wrapper) with its
+ * own review and its own evidence, and folding that into a CI-plumbing PR
+ * would bury it.
+ *
+ * Deliberately NOT a dropped route — that is how a gate quietly stops covering
+ * things. Deliberately NOT `test.fail()` either: the measurement proved
+ * timing-sensitive on a slow render (see the `found` assertion below), and a
+ * `test.fail()` that flips to "expected to fail, but passed" on an unrelated
+ * slow frame is a false alarm pointed at the wrong person.
+ *
+ * Delete the entry when the issue closes; the assertion below is already
+ * written and will start gating that route again the moment it goes.
+ */
+const KNOWN_CONTENT_OVERFLOW: Partial<Record<(typeof ROUTES)[number], string>> = {
+  '/transactions':
+    '#1772 — transactions table renders without an overflow-x-auto wrapper. ' +
+    'Measured 94-124px of content clipped out of a 393px box (it varies ' +
+    'with how many rows render) — on CI and locally alike.',
+}
+
+/**
+ * Horizontal overflow of the CONTENT REGION, measured on its own scroll box.
+ *
+ * Why the shared `expectNoHorizontalOverflow` is not enough — found the hard
+ * way, by the #1768 mutation, which this spec's first version passed:
+ *
+ *   The authenticated shell wraps everything in `overflow-hidden` twice
+ *   (`layout.tsx`: the `f...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/bug-reports/_run-report-template.md @ d4f42d0812bb6d071f033d9def2ddef83f0a7d1c -->
---
owner: "@d-hinders"
status: current
covers:
  - docs/operations/e2e-qa-runbook.md
  - docs/operations/agent-qa.md
  - packages/frontend/package.json
  - packages/frontend/playwright.config.ts
  - packages/frontend/playwright.live.config.ts
  - packages/frontend/e2e/**
  - packages/frontend/src/components/ConnectAgentModal.tsx
  - packages/connect/src/**
  - packages/backend/src/routes/agent-connection-setups.ts
  - packages/backend/src/routes/machine-payments.ts
  - packages/backend/src/rails/sweep.ts
  - packages/backend/src/config.ts
  - packages/sdk/src/sweep.ts
  - packages/qa-agent/**
  - .github/workflows/ci.yml
  - .github/workflows/qa-dev.yml
  - .github/workflows/qa-live.yml
  - .claude/commands/qa-dev.md
  - .claude/commands/qa-explore-ui.md
last-verified: "2026-08-09" # re-verified for #1227 (db-mock ratchet joins the gates) — no claim here affected
---

<!--
Per-run QA report.
Copy to `<yyyy-mm-ddThhmmssZ>-<mode>-<flow>-<env>.md` using a slugged UTC
timestamp, or include the CI run id/short SHA so concurrent runs cannot collide.
File concrete bugs as separate GitHub issues and link them here.
Procedures: ../operations/e2e-qa-runbook.md and ../operations/agent-qa.md.
-->

# QA run report — <mode> — <flow> — <environment>

> **Secret-safety rule:** Never paste private keys, API keys, JWTs/cookies,
> setup tokens or token-bearing prompts, credential files, Authorization
> headers, or secret-bearing logs. Record safe prefixes only where necessary,
> plus public addresses, payment IDs, transaction hashes, sanitized URLs, and
> redacted artifacts. Confirm artifacts were checked for secrets before commit.

## Run Metadata

- **Run mode:** mocked Playwright | deployed live Playwright | deterministic `qa:dev` | manual live runtime/merchant | browser exploration
- **Flow/scenarios:**
- **Started / finished (UTC):**
- **Runner:**
- **Exact command:**
- **Process exit code:**
- **Git branch / SHA:** `<branch from dev>` / `<sha>`
- **Frontend URL / build SHA:** `<per-PR preview or localhost>` / `<sha>`
- **Backend URL / deploy SHA:**
- **Merchant URL / version:** `<sanitized hostname>` / `<version>`
- **Chain:** `<name>` (`<chain id>`)
- **Runtime/browser:** `<runtime + version or Playwright project/device>`
- **Package versions:** connect `<version>` · SDK `<version>` · QA harness `<sha/version>`
- **CI workflow/run:** `<link or n/a>`
- **Public QA identity:** user/agent id or safe/delegate address where useful
- **Overall result:** pass | pass with friction | partial/blocked | fail
- **Completeness:** `<passed>/<required> passed · <failed> failed · <skipped> skipped`

A required skipped scenario makes the overall run **partial/blocked**, even when
the harness exits zero. Keep per-check pass/fail/skip separate from process exit
status. Mocked Playwright verifies UI structure and must not claim live
on-chain settlement.

## Preflight

Mark items `n/a` when the selected mode cannot exercise them; mocked Playwright
does not require funded wallets, relayer gas, or live credentials.

- [ ] Dev/testnet only; no production credentials, RPCs, or real funds.
- [ ] Correct frontend, backend, hosted MCP, and merchant targets confirmed.
- [ ] Safe test-token balance and remaining allowance recorded.
- [ ] Relayer has testnet gas.
- [ ] Delegate balance recorded when testing x402/recovery.
- [ ] Required local/CI secret names are present without printing values.

## Command And Artifacts

- **Command output summary:** `<test count / scenario count / exit code>`
- **Playwright base URL / project / retries:** `<when applicable>`
- **Artifacts:** `<trace, screenshot, video, HTML report, sanitized log paths>`
- **Default Playwright artifact paths:**
  - `output/playwright/test-results`
  - `output/playwright/html-report`
  - `output/playwright-live/test-results`
  - `output/playwright-live/html-report`
- **Artifact secret review completed:** yes (required before commit)

If the secret review fails, do not commit the report or artifacts. Redact or
remove the affected files first.

Canonical commands:

```sh
npm run test:e2e:desktop -w packages/frontend
npm run test:e2e:full -w packages/frontend
npm run test:e2e:live -w packages/frontend
npm run qa:dev -w packages/qa-agent
```

## Agent Connection — When In Scope

| Check | Expected evidence | Result | Actual evidence / notes |
|---|---|---|---|
| Setup prompt | Default flow shows one prompt/command and no private key or API key | pass / fail / skip | |
| Local credentials | Connector creates API and signing credentials locally; backend receives public signing address/proof and API-key hash/prefix | pass / fail / skip | Sanitized paths/registration evidence |
| Runtime wiring | Hosted MCP and local signer entries load, with correct restart/readiness behavior | pass / fail / skip | Runtime/config evidence |
| Wallet approval | Correct Haven wallet/network/rules shown; approval e...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/bug-reports/_run-report-template.md b/docs/bug-reports/_run-report-template.md
--- a/docs/bug-reports/_run-report-template.md
+++ b/docs/bug-reports/_run-report-template.md
@@ -21,7 +21,7 @@ covers:
   - .github/workflows/qa-live.yml
   - .claude/commands/qa-dev.md
   - .claude/commands/qa-explore-ui.md
-last-verified: "2026-08-09" # re-verified for #1227 (db-mock ratchet joins the gates) — no claim here affected
+last-verified: "2026-08-22" # #1768: canonical commands re-read against `packages/frontend/package.json` — `test:e2e:gate` replaces the desktop/full pair, `test:e2e:mobile` added. Prior: re-verified for #1227 (db-mock ratchet joins the gates) — no claim here affected
 ---
 
 <!--
@@ -95,8 +95,11 @@ remove the affected files first.
 Canonical commands:
 
 ```sh
+# Both gating Playwright projects — desktop + mobile (#1768). This is what CI runs.
+npm run test:e2e:gate -w packages/frontend
+# One project at a time, while iterating:
 npm run test:e2e:desktop -w packages/frontend
-npm run test:e2e:full -w packages/frontend
+npm run test:e2e:mobile -w packages/frontend
 npm run test:e2e:live -w packages/frontend
 npm run qa:dev -w packages/qa-agent
 ```

diff --git a/docs/contributing/pr-workflow-checklist.md b/docs/contributing/pr-workflow-checklist.md
--- a/docs/contributing/pr-workflow-checklist.md
+++ b/docs/contributing/pr-workflow-checklist.md
@@ -7,7 +7,7 @@ covers:
   - package.json
   - .agents/skills/haven-agent-workflow/references/reviewer.md
   - .agents/skills/haven-agent-workflow/references/design-reviewer.md
-last-verified: "2026-08-21" # the haven-reviewer rule is unconditional (owner decision 2026-08-21); the risk list this file carried was the licence for skipping it. AGENTS.md is canonical. Prior: #1227: lint:db-mocks added to the Backend/API verification row
+last-verified: "2026-08-22" # #1768: the Browser UX row now points at `test:e2e:gate` (desktop + mobile), not desktop-only. Prior: the haven-reviewer rule is unconditional (owner decision 2026-08-21); the risk list this file carried was the licence for skipping it. AGENTS.md is canonical. Prior: #1227: lint:db-mocks added to the Backend/API verification row
 ---
 
 # PR Workflow Checklist
@@ -135,7 +135,7 @@ Use the smallest reliable set that matches the change.
 | Frontend unit/UI | `npm run typecheck -w packages/frontend`, `npm run design:lint -w packages/frontend`, `npm run lint:copy`, `npm run test -w packages/frontend`, and `npm run build -w packages/frontend` |
 | SDK | `npm run typecheck -w packages/sdk`, `npm run test -w packages/sdk`, and `npm run build -w packages/sdk` |
 | Cross-package or release-risk | `npm run quality` |
-| Browser UX or routing | Relevant unit/build checks plus `npm run test:e2e:desktop -w packages/frontend` when the local Playwright server is working |
+| Browser UX or routing | Relevant unit/build checks plus `npm run test:e2e:gate -w packages/frontend` when the local Playwright server is working — that is both gating projects, desktop **and** mobile (#1768); `test:e2e:desktop` / `test:e2e:mobile` narrow it to one while iterating |
 
 Notes:

diff --git a/docs/contributing/ship-playbooks/frontend.md b/docs/contributing/ship-playbooks/frontend.md
--- a/docs/contributing/ship-playbooks/frontend.md
+++ b/docs/contributing/ship-playbooks/frontend.md
@@ -2,7 +2,7 @@
 owner: "@d-hinders"
 status: current
 covers: []  # narrative — process playbook
-last-verified: "2026-08-21" # #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
+last-verified: "2026-08-22" # #1768: §4 gains the viewport-coverage table — both Playwright projects gate on every PR now, and `*.mobile.spec.ts` is how you write a mobile test. Prior: #1738: full-page captures un-clip the shell and fail on a blank PNG — §4 re-read against the capture scripts
 ---
 
 # Frontend playbook
@@ -37,6 +37,29 @@ Run the matching items from the **Captain Self-Check Preflight** in [`../ai-agen
 
 Verify the change in the **browser**, or — when the browser path is unavailable/flaky — add a **named headless equivalent** (vitest) that covers the skipped animation, layout, routing, loading, or interaction risk. Include empty, loading, error, and success states when the screen can enter them; check mobile and desktop.
 
+**Which viewports actually gate ([#1768](https://github.com/d-hinders/Haven-AI/issues/1768)).** The *Frontend browser smoke* job runs **both** Playwright projects on every frontend PR, with no dispatch required:
+
+| Project | Emulation | Runs | Gates a PR |
+|---|---|---|---|
+| `chromium-desktop` | Desktop Chrome — 1280×720 viewport, fine pointer, no touch, DSF 1 | every `e2e/*.spec.ts` **except** `*.mobile.spec.ts` | yes |
+| `chromium-mobile` | **Pixel 5** — 393×727 viewport, coarse pointer, touch, Android UA, DSF 2.75 | `e2e/*.mobile.spec.ts` only | yes |
+
+(Numbers read off Playwright's own `devices` table at the pinned version, not from memory. Pixel 5's `screen` is 393×851; the **viewport** — what the page actually gets — is 393×727.)
+
+Both projects also inherit `SUITE_IGNORE` (`e2e/live/**`, and `*.visual.spec.ts` unless `VISUAL_REGRESSION=1`). That constant exists because a project-level `testIgnore` **replaces** the config-level one instead of extending it — a project that declares its own must spread `SUITE_IGNORE` back in, or the unmocked live smoke silently rejoins the fast suite.
+
+Plus the separate *Design visual regression* job, which pixel-compares `/design-system` at **1280** and **390** (`scripts/evidence-viewports.mjs`) — but under `chromium-desktop` at DSF 1, by setting the viewport inside the spec. That is a pixel gate, not a device gate: it sees layout, never touch or hit-testing.
+
+Before #1768, `chromium-mobile` existed but only a `workflow_dispatch` with `ui_suite=full` ever ran it — so **no mobile viewport gated anything**, which is a large part of why [#1749](https://github.com/d-hinders/Haven-AI/issues/1749) (primary navigation unopenable below `lg`) shipped. That input is now removed and both projects are unconditional.
+
+**Writing a mobile test:** name the file `*.mobile.spec.ts` and it runs under real Pixel 5 emulation. Do **not** reach for `test.use({ viewport: … })` inside a desktop spec — it narrows the window but leaves `maxTouchPoints` at 0, the pointer fine and the UA desktop, so touch and hit-testing behaviour is not actually covered. Conversely, keep viewport-independent behaviour out of `*.mobile.spec.ts`: the two projects run disjoint spec sets on purpose, and duplicating a spec buys nothing but CI minutes. `e2e/navigation.mobile.spec.ts` is the reference, including the meta-guard that fails if the project ever stops being device-emulated.
+
+**Measure overflow on the scroll box, not the document.** The authenticated shell is `overflow-hidden`, so content wider than the screen is *clipped* rather than growing `documentElement.scrollWidth` — which means the page-level `expectNoHorizontalOverflow` helper **cannot fail** on any authenticated route ([#1771](https://github.com/d-hinders/Haven-AI/issues/1771)). This was found by the #1768 mutation, not by reading. Compare `<main id="main-content">`'s own `scrollWidth` against its `clientWidth`; `navigation.mobile.spec.ts`'s `measureContentOverflow` is the reference. Clipped content on mobile is *unreachable*, not merely ugly, so this is the assertion that matters.
+
+**A known, filed defect is exempted by name, never by deletion.** `navigation.mobile.spec.ts` keeps a `KNOWN_CONTENT_OVERFLOW` map: the route still runs and still asserts rendering and console cleanliness, only the one known-failing assertion is skipped, and only with an issue number and the measured numbers next to it. Dropping the route instead is how a gate quietly stops covering things — which is the defect #1768 exists to close. Delete the entry in the PR that fixes the issue.
+
+Run them locally with `npm run test:e2e:mobile -w packages/frontend`, or both with `npm run test:e2e:gate -w packages/frontend` (exactly what CI runs).
+
 **Rendered-screen evidence is REQUIRED** for any diff that touches a rendered route or a shared UI primitive (`components/ui/*`, `components/haven/*`). Run `npm run screenshot -w packages/frontend -- <routes>` (see [#896](https://github.com/d-hinders/Haven-AI/issues/896)); it captures desktop (1280) + mobile (390) PNGs of `/design-system` plus the routes you pass, using a known auth/data fixture and the pre-installed browser. The fixture serves a deterministic **populated** dataset (a funded account, agents on both rails, transactions, a pending approval, contacts, agent activity and spend stats) so lists, tables and amounts render realistically — set `SCREENSHOT_FIXTURE=empty` when you specifically want empty states. The script also summarises any **console errors** per route; a red console means a fixture-shape gap or a real client bug — fix it before trusting the PNGs. **Attach the PNGs to the...
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/bug-reports/_run-report-template.md @ 7ff4b831fdb6bd79849b3268bb32b0a8da59f934 -->
---
owner: "@d-hinders"
status: current
covers:
  - docs/operations/e2e-qa-runbook.md
  - docs/operations/agent-qa.md
  - packages/frontend/package.json
  - packages/frontend/playwright.config.ts
  - packages/frontend/playwright.live.config.ts
  - packages/frontend/e2e/**
  - packages/frontend/src/components/ConnectAgentModal.tsx
  - packages/connect/src/**
  - packages/backend/src/routes/agent-connection-setups.ts
  - packages/backend/src/routes/machine-payments.ts
  - packages/backend/src/rails/sweep.ts
  - packages/backend/src/config.ts
  - packages/sdk/src/sweep.ts
  - packages/qa-agent/**
  - .github/workflows/ci.yml
  - .github/workflows/qa-dev.yml
  - .github/workflows/qa-live.yml
  - .claude/commands/qa-dev.md
  - .claude/commands/qa-explore-ui.md
last-verified: "2026-08-22" # #1768: canonical commands re-read against `packages/frontend/package.json` — `test:e2e:gate` replaces the desktop/full pair, `test:e2e:mobile` added. Prior: re-verified for #1227 (db-mock ratchet joins the gates) — no claim here affected
---

<!--
Per-run QA report.
Copy to `<yyyy-mm-ddThhmmssZ>-<mode>-<flow>-<env>.md` using a slugged UTC
timestamp, or include the CI run id/short SHA so concurrent runs cannot collide.
File concrete bugs as separate GitHub issues and link them here.
Procedures: ../operations/e2e-qa-runbook.md and ../operations/agent-qa.md.
-->

# QA run report — <mode> — <flow> — <environment>

> **Secret-safety rule:** Never paste private keys, API keys, JWTs/cookies,
> setup tokens or token-bearing prompts, credential files, Authorization
> headers, or secret-bearing logs. Record safe prefixes only where necessary,
> plus public addresses, payment IDs, transaction hashes, sanitized URLs, and
> redacted artifacts. Confirm artifacts were checked for secrets before commit.

## Run Metadata

- **Run mode:** mocked Playwright | deployed live Playwright | deterministic `qa:dev` | manual live runtime/merchant | browser exploration
- **Flow/scenarios:**
- **Started / finished (UTC):**
- **Runner:**
- **Exact command:**
- **Process exit code:**
- **Git branch / SHA:** `<branch from dev>` / `<sha>`
- **Frontend URL / build SHA:** `<per-PR preview or localhost>` / `<sha>`
- **Backend URL / deploy SHA:**
- **Merchant URL / version:** `<sanitized hostname>` / `<version>`
- **Chain:** `<name>` (`<chain id>`)
- **Runtime/browser:** `<runtime + version or Playwright project/device>`
- **Package versions:** connect `<version>` · SDK `<version>` · QA harness `<sha/version>`
- **CI workflow/run:** `<link or n/a>`
- **Public QA identity:** user/agent id or safe/delegate address where useful
- **Overall result:** pass | pass with friction | partial/blocked | fail
- **Completeness:** `<passed>/<required> passed · <failed> failed · <skipped> skipped`

A required skipped scenario makes the overall run **partial/blocked**, even when
the harness exits zero. Keep per-check pass/fail/skip separate from process exit
status. Mocked Playwright verifies UI structure and must not claim live
on-chain settlement.

## Preflight

Mark items `n/a` when the selected mode cannot exercise them; mocked Playwright
does not require funded wallets, relayer gas, or live credentials.

- [ ] Dev/testnet only; no production credentials, RPCs, or real funds.
- [ ] Correct frontend, backend, hosted MCP, and merchant targets confirmed.
- [ ] Safe test-token balance and remaining allowance recorded.
- [ ] Relayer has testnet gas.
- [ ] Delegate balance recorded when testing x402/recovery.
- [ ] Required local/CI secret names are present without printing values.

## Command And Artifacts

- **Command output summary:** `<test count / scenario count / exit code>`
- **Playwright base URL / project / retries:** `<when applicable>`
- **Artifacts:** `<trace, screenshot, video, HTML report, sanitized log paths>`
- **Default Playwright artifact paths:**
  - `output/playwright/test-results`
  - `output/playwright/html-report`
  - `output/playwright-live/test-results`
  - `output/playwright-live/html-report`
- **Artifact secret review completed:** yes (required before commit)

If the secret review fails, do not commit the report or artifacts. Redact or
remove the affected files first.

Canonical commands:

```sh
# Both gating Playwright projects — desktop + mobile (#1768). This is what CI runs.
npm run test:e2e:gate -w packages/frontend
# One project at a time, while iterating:
npm run test:e2e:desktop -w packages/frontend
npm run test:e2e:mobile -w packages/frontend
npm run test:e2e:live -w packages/frontend
npm run qa:dev -w packages/qa-agent
```

## Agent Connection — When In Scope

| Check | Expected evidence | Result | Actual evidence / notes |
|---|---|---|---|
| Setup prompt | Default flow shows one prompt/command and no private key or API key | pass / fail / skip | |
| Local credentials | Connector creates API and signing credentials locally; backend receives public sig...
```

### `GH-CAND-0015`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1769
- Repository: `d-hinders/Haven-AI`
- PR number: `1769`
- PR title: fix(frontend): make the mobile navigation toggle reachable, on a named z-index scale (#1749)
- Language: `typescript`
- Code changed files: `['packages/frontend/e2e/fixtures/haven-api.ts', 'packages/frontend/e2e/mobile-nav-layering.spec.ts', 'packages/frontend/src/__tests__/z-index-scale.test.ts', 'packages/frontend/src/app/(authenticated)/accounts/AccountsOverviewClient.tsx', 'packages/frontend/src/app/(authenticated)/accounts/[safeId]/AccountDetailClient.tsx', 'packages/frontend/src/app/(authenticated)/design-system/page.tsx', 'packages/frontend/src/app/(authenticated)/layout.tsx', 'packages/frontend/src/components/AddFundsModal.tsx', 'packages/frontend/src/components/AgentPanel.tsx', 'packages/frontend/src/components/ApprovalNotifications.tsx', 'packages/frontend/src/components/DashboardActionPickerModal.tsx', 'packages/frontend/src/components/EditAgentModal.tsx', 'packages/frontend/src/components/PaymentCredentialsModal.tsx', 'packages/frontend/src/components/ReceiveFundsModal.tsx', 'packages/frontend/src/components/SendModal.tsx', 'packages/frontend/src/components/TopBar.tsx', 'packages/frontend/src/components/sidebar/Sidebar.tsx', 'packages/frontend/src/components/ui/Modal.tsx', 'packages/frontend/src/components/ui/SidePanel.tsx', 'packages/frontend/src/components/ui/Toast.tsx', 'packages/frontend/src/components/ui/Tooltip.tsx']`
- Docs changed files: `['docs/product/design-system.md', 'docs/regulatory/casp-changelog/2026-08-22-1749.md']`

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
diff --git a/packages/frontend/e2e/fixtures/haven-api.ts b/packages/frontend/e2e/fixtures/haven-api.ts
--- a/packages/frontend/e2e/fixtures/haven-api.ts
+++ b/packages/frontend/e2e/fixtures/haven-api.ts
@@ -465,7 +465,15 @@ export async function dismissMobileSidebar(page: Page) {
 
   const closeButton = page.getByRole('button', { name: 'Close sidebar' })
   if (await closeButton.isVisible({ timeout: 1_000 }).catch(() => false)) {
-    await closeButton.click({ force: true })
+    // No `{ force: true }` (#1749). It used to be required, and that was the
+    // undiagnosed symptom: `force` skips the actionability check, and the
+    // check this helper was failing is the hit-test — TopBar's `z-[100]`
+    // covered the toggle's `z-[60]`, so the real user gesture was impossible
+    // on every authenticated route below `lg`. Keeping the plain click makes
+    // this helper the regression canary: if the layering breaks again, every
+    // mobile e2e test fails here with "intercepts pointer events" instead of
+    // quietly forcing its way through.
+    await closeButton.click()
     await page.getByRole('button', { name: 'Open sidebar' }).waitFor({ state: 'visible' })
   }
 }

diff --git a/packages/frontend/e2e/mobile-nav-layering.spec.ts b/packages/frontend/e2e/mobile-nav-layering.spec.ts
--- a/packages/frontend/e2e/mobile-nav-layering.spec.ts
+++ b/packages/frontend/e2e/mobile-nav-layering.spec.ts
@@ -0,0 +1,170 @@
+import { expect, test, type Page } from '@playwright/test'
+import { mockHavenApi, seedAuthenticatedSession } from './fixtures/haven-api'
+
+/**
+ * Mobile navigation layering (#1749).
+ *
+ * The `Open sidebar` toggle is `position: fixed` in the same 56px band that
+ * `TopBar` occupies. Whichever of the two wins the stacking contest owns the
+ * clicks in that band, and for the whole life of the shell `TopBar` did — so
+ * primary navigation was unopenable below `lg` on every authenticated route.
+ *
+ * Measured on the pre-fix code, at 320 / 390 / 768 / 1023px on `/dashboard`:
+ *
+ *   computed z-index            toggle 60, header 100
+ *   elementFromPoint(32, 32)    div.flex.items-center.gap-3   ← TopBar's inner div
+ *   non-forced .click()         "…intercepts pointer events"
+ *
+ * ...and after it, at the same four widths:
+ *
+ *   computed z-index            toggle 150, header 100
+ *   elementFromPoint(32, 32)    path                          ← the toggle's own icon
+ *   non-forced .click()         opens the drawer
+ *
+ * ── Why this is a browser spec and not a unit test ──────────────────────────
+ * A jsdom test can assert the class strings and would have passed throughout
+ * the entire period the bug was live: jsdom has no layout, no stacking
+ * contexts and no hit-testing, so `elementFromPoint` and "is this element
+ * actionable" do not exist there in any meaningful form. The defect is purely
+ * a rendered-layout property. Only a real engine can see it.
+ *
+ * ── Why it declares its own viewport ────────────────────────────────────────
+ * The gating CI job runs `test:e2e:desktop` (`--project=chromium-desktop`);
+ * the `chromium-mobile` project runs only on a manual `ui_suite=full`
+ * dispatch. A mobile-project spec therefore would NOT gate a pull request —
+ * which is a large part of why this survived. `test.use({ viewport })`
+ * overrides the project's viewport, so these run inside the desktop project
+ * and are genuinely blocking.
+ */
+
+// The toggle is `lg:hidden`, so everything from the narrowest phone up to one
+// pixel below the `lg` breakpoint is affected. 1023 is where a regression
+// would most plausibly reappear.
+const MOBILE_WIDTHS = [320, 390, 768, 1023]
+
+/**
+ * Every check that needs the shell rendered, against ONE page load.
+ *
+ * Deliberately not split into a test per assertion: each test costs a full
+ * navigation, and at four viewports that turned a layering check into 17 page
+ * loads in a smoke suite that is supposed to be fast.
+ */
+async function expectNavigationReachable(page: Page) {
+  const open = page.getByRole('button', { name: 'Open sidebar' })
+  await expect(open).toBeVisible()
+
+  // 1. The hit-test from the original report. `elementFromPoint` answers "what
+  //    would a tap here actually reach", which is the only question that
+  //    matters — the button's own computed style was always correct.
+  const hit = await page.evaluate(() => {
+    const btn = document.querySelector('button[aria-label="Open sidebar"]')
+    if (!btn) return { error: 'toggle not found' }
+    const r = btn.getBoundingClientRect()
+    const top = document.elementFromPoint(
+      Math.round(r.left + r.width / 2),
+      Math.round(r.top + r.height / 2),
+    )
+    return {
+      reachesToggle: top === btn || btn.contains(top),
+      // Named so a failure says WHAT is covering it rather than just "false" —
+      // the first question anyone asks next. On the pre-fix code this read
+      // `div.flex.items-center.gap-3`, TopBar's inner row.
+      obstructedBy: top
+        ? `${top.tagName.toLowerCase()}.${String(top.className).trim().split(/\s+/).slice(0, 3).join('.')}`
+        : null,
+    }
+  })
+  expect(hit).toMatchObject({ reachesToggle: true })
+
+  // 2. A NON-forced click. Playwright's actionability check runs the same
+  //    hit-test before clicking, so an obstructed toggle fails here with
+  //    "intercepts pointer events" rather than silently passing.
+  await open.click()
+
+  const nav = page.getByRole('navigation')
+  await expect(nav.getByRole('link', { name: 'Dashboard' })).toBeVisible()
+
+  // 3. The drawer owns its own top band. It is `inset-y-0`, so its 56px logo
+  //    band shares that band with TopBar; if TopBar wins there the drawer is
+  //    decapitated and the scrim dims everything except the bar it exists to
+  //    dim — the same root cause as the toggle, one layer down.
+  //
+  //    Wait for the 200ms slide to FINISH first. A visible link is not enough:
+  //    a transforming element still has a non-empty box, so hit-testing here
+  //    can land on a part-way drawer, return the scrim, and report a layering
+  //    defect that does not exist. That false failure hit three of four widths
+  //    on this spec's first run.
+  await page.waitForFunction(
+    () => Math.round(document.querySelector('aside')!.getBoundingClientRect().left) === 0,
+    undefined,
+    { timeout: 10_000 },
+  )
+
+  const layering = await page.evaluate(() => {
+    const aside = document.querySelector('aside')!
+    const header = document.querySelector('header')!
+    const r = aside.getBoundingClientRect()
+    const top = document.elementFromPoint(
+      Math.round(r.left + r.width / 2),
+      Math.round(header.getBoundingClientRect().height / 2),
+    )
+    return {
+      drawerOwnsItsTopBand: aside.contains(top),
+      topElement: top?.tagName.toLowerCase() ?? null,
+    }
+  })
+  expect(layering).toMatchObject({ drawerOwnsItsTopBand: true })
+
+  // 4. ...and back out. The Close affordance is the SAME button, so if the
+  //    drawer or its scrim covered it, the sidebar could be opened and then
+  //    never closed by the control that opened it.
+  const close = page.getByRole('button', { name: 'Close sidebar' })
+  await expect(close).toBeVisible()
+  await close.click()
+  await expect(page.getByRole('button', { name: 'Open sidebar' })).toBeVisible()
+}
+
+test.describe('mobile navigation is reachable below lg (#1749)', () => {
+  test.beforeEach(async ({ page }) => {
+    await mockHavenApi(page)
+    await seedAuthenticatedSession(page)
+  })
+
+  for (const width of MOBILE_WIDTHS) {
+    test.describe(`at ${width}px`, () => {
+      test.use({ viewport: { width, height: 844 } })
+
+      test('the toggle is hit-testable and the drawer layers above the top bar', async ({ page }) => {
+        await page.goto('/dashboard')
+        await expectNavigationReachable(page)
+      })
+    })
+  }
+
+  test.describe('on a second route', () => {
+    test.use({ viewport: { width: 390, height: 844 } })
+
+    // Both z-index values are hardcoded and route-independent, so one more
+    // route is enough to show this is the shell and not a `/dashboard` quirk —
+    // "route-independent" was an assumption in the original report rather than
+    // something anyone had checked.
+    test('the same holds on /agents', async ({ page }) => {
+      await page.goto('/agents')
+      await expectNavigationReachable(page)
+    })
+  })
+
+  test.describe('at the lg breakpoint', () => {
+    test.use({ viewport: { width: 1024, height: 844 } })
+
+    // The complement of the checks above: `lg:hidden` must still hide it, so a
+    // fix that raised the toggle above TopBar cannot have leaked a floating
+    // hamburger onto the desktop shell.
+    test('no mobile toggle renders at 1024px', async ({ page }) => {
+      await page.goto('/dashboard')
+      await expect(page.getByRole('navigation').getByRole('link', { name: 'Dashboar...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/product/design-system.md @ 7fb1a4fbec4947e98a977eb326ee233de41f0484 -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/frontend/src/app/globals.css
  - packages/frontend/tailwind.config.js
  - packages/frontend/src/components/ui/**
  - packages/frontend/src/app/layout.tsx
  - packages/frontend/src/app/page.tsx
  - packages/frontend/src/app/how-it-works/**
  - packages/frontend/src/app/protocols/**
  - packages/frontend/src/app/(authenticated)/design-system/**
  - packages/frontend/src/components/marketing/**
  - packages/frontend/src/components/sidebar/**
  - packages/frontend/src/components/TopBar.tsx
  - packages/frontend/src/components/haven/TransactionActivityRow.tsx
  - packages/frontend/src/components/haven/TransactionMovement.tsx
  - packages/frontend/src/components/transactions/**
last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate
---

# Haven Design System

This is the source of truth for Haven's current light visual language. Companion to the product UX guide (`docs/product/README.md`, which documents product doctrine, vocabulary, and IA — those rules **still apply**). If older docs mention a dark app surface system, **this document supersedes them**.

The production authenticated app and `/design-system` are the live references for product UX. The production marketing routes are the live references for marketing UX: `/`, `/how-it-works`, `/protocols/x402`, and `/protocols/mpp`. When in doubt, open the live route, inspect the element, and match the system here.

---

## 1. Tokens

All tokens live as CSS custom properties at `:root` in `packages/frontend/src/app/globals.css`. Core color, radius, and shadow tokens are mirrored in `packages/frontend/tailwind.config.js` so they are usable as `bg-bg`, `text-ink`, `border-border`, etc. Newer production tokens such as typography utilities, raised cards, popovers, modal backdrop, and the brand gradient may exist as CSS variables/classes only until they are promoted into Tailwind.

### Surfaces

| Token | Value | Use |
|---|---|---|
| `--v2-bg` | `#ffffff` | Page background |
| `--v2-surface` | `#f6f9fc` | Alternating section bands, card hover backgrounds |
| `--v2-surface-2` | `#eef2f7` | Disabled states, deeper card stacking |
| `--v2-surface-code` | `#0b1120` | Dark code blocks on light pages (Stripe pattern) |
| `--v2-surface-hover` | `#f0f4f9` | Sidebar/user-menu row hover and subtle interactive shells |
| `--v2-modal-backdrop` | `rgba(26, 31, 54, 0.66)` | Modal backdrop with blur |

### Ink (text)

| Token | Value | Use |
|---|---|---|
| `--v2-ink` | `#1a1f36` | Headings, primary text, amounts |
| `--v2-ink-2` | `#525f7f` | Body text, secondary information |
| `--v2-ink-3` | `#5d6c85` | Tertiary text, eyebrows, captions — AA-safe (≥4.5:1) on white and all tinted surfaces |
| `--v2-ink-on-brand` | `#ffffff` | Text on brand‑colored or dark surfaces |

### Borders

| Token | Value | Use |
|---|---|---|
| `--v2-border` | `#e6ebf1` | Default hairline (cards, dividers) |
| `--v2-border-strong` | `#d6dbe3` | Hover, ghost button borders, flow arrows |

### Brand

| Token | Value | Use |
|---|---|---|
| `--v2-brand` | `#4f46e5` (indigo‑600) | Primary CTA bg, links, accents, brand mark |
| `--v2-brand-strong` | `#4338ca` (indigo‑700) | Primary CTA hover |
| `--v2-brand-soft` | `#eef2ff` | Brand‑tinted card backgrounds, focus rings |
| `--v2-brand-gradient` | `linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)` | Gradient wordmark or one restrained brand accent |

Use `.v2-brand-gradient-text` for the production app wordmark. In product UI, do not use the gradient for buttons, badges, large panels, or repeated decoration.

### Semantic

| Token | Value | Soft variant | Use |
|---|---|---|---|
| `--v2-success` | `#047857` | `--v2-success-soft` `#ecfdf5` | Settled, confirmed, incoming |
| `--v2-debit` | `#0369a1` | `--v2-debit-soft` `#f0f9ff` | Outgoing / sent money (sibling to success; never a warning) |
| `--v2-warning` | `#b54708` | `--v2-warning-soft` `#fef3c7` | 402 Payment Required, pending review |
| `--v2-danger` | `#b42318` | `--v2-danger-soft` `#fef2f2` | Failed, destructive |

Same rule as v1: **never repurpose a semantic color**.

**Contrast guarantee:** every ink and semantic text token meets WCAG AA (≥4.5:1) against white, its own `-soft` background, and the tinted surfaces (`--v2-surface`, `--v2-surface-2`, hover). Guarded by `packages/frontend/src/__tests__/token-contrast.test.ts` — if you change a token, that test tells you whether it still clears the bar.

### Opacity on a token colour ([#1708](https://github.com/d-hinders...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/product/design-system.md b/docs/product/design-system.md
--- a/docs/product/design-system.md
+++ b/docs/product/design-system.md
@@ -16,7 +16,7 @@ covers:
   - packages/frontend/src/components/haven/TransactionActivityRow.tsx
   - packages/frontend/src/components/haven/TransactionMovement.tsx
   - packages/frontend/src/components/transactions/**
-last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate
+last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate # #1749: new "Layering (z-index)" § under Tokens — the shell's stacking order is now a named scale in globals.css, and the mobile nav overlay deliberately outranks the chrome. Only § Tokens re-verified in this pass
 ---
 
 # Haven Design System
@@ -138,6 +138,30 @@ Raised card elevation is reserved for the few surfaces that anchor a page, such
 
 **No glow shadows on text**, no colored shadows on buttons.
 
+### Layering (z-index) ([#1749](https://github.com/d-hinders/Haven-AI/issues/1749))
+
+Every stacking layer has a named token. **Reach for a token, never a fresh number.**
+
+```css
+--v2-z-content:        10;   /* in-flow overlaps: badges, gradient washes */
+--v2-z-sticky:         20;   /* sticky table headers */
+--v2-z-chrome:        100;   /* TopBar */
+--v2-z-chrome-popover: 110;  /* popovers anchored in the chrome */
+--v2-z-nav-scrim:     130;   /* mobile drawer scrim */
+--v2-z-nav-drawer:    140;   /* mobile drawer */
+--v2-z-nav-toggle:    150;   /* the Open / Close sidebar toggle */
+--v2-z-modal:         200;   /* Modal, SidePanel */
+--v2-z-tooltip:       210;
+--v2-z-panel:         250;   /* AgentPanel */
+--v2-z-toast:        9999;   /* Toast, skip-to-content link */
+```
+
+The rule the numbers encode: **the mobile navigation overlay outranks the app chrome it slides over, and modals outrank the navigation.** The drawer is `inset-y-0`, so its own logo band shares the top 56px with the bar, and its scrim exists to dim everything behind it — the bar included. Let the bar win and the drawer is decapitated, the scrim dims all but the top strip, and the toggle (which sits *inside* that strip by design, in the gap the bar reserves for it) cannot be tapped at all. That was #1749: a `z-[100]` header and a `z-[60]` toggle chosen independently in different files left mobile primary navigation unopenable on every authenticated route.
+
+Tiers are spaced by 10 so a new layer lands between two without renumbering. Adding a layer means picking the tier it belongs to; if none fits, add one to the scale first. A raw `z-[…]` in a shell component is the failure this scale prevents — `src/__tests__/z-index-scale.test.ts` fails on one, and on any inversion of the order above.
+
+That test reads source, so it cannot see stacking contexts or hit-testing. `e2e/mobile-nav-layering.spec.ts` is the half that can: it drives a real engine at four widths below `lg` and asserts `document.elementFromPoint` at the toggle's centre returns the toggle.
+
 ---
 
 ## 2. Typography

diff --git a/docs/regulatory/casp-changelog/2026-08-22-1749.md b/docs/regulatory/casp-changelog/2026-08-22-1749.md
--- a/docs/regulatory/casp-changelog/2026-08-22-1749.md
+++ b/docs/regulatory/casp-changelog/2026-08-22-1749.md
@@ -0,0 +1 @@
+- **#1749** — the mobile navigation toggle was painted AND hit-tested under `TopBar` (`z-[100]` over the toggle's `z-[60]`), making primary navigation unopenable below `lg` on every authenticated route; the fix introduces a named z-index scale in `globals.css` and raises the mobile navigation overlay above the app chrome. **No authority, custody or execution boundary moves and nothing new is grantable.** This change is entirely presentational: it alters which of two already-rendered layers wins a stacking contest, and touches no route, no request, no signing path, no delegation, no allowance and no policy evaluation. The gate flags it because the reviewer-driven half of the diff migrates ten `fixed inset-0` modal overlays onto the scale's `--v2-z-modal` tier, and six of those files are money-adjacent surfaces (`SendModal`, `AddFundsModal`, `ReceiveFundsModal`, `PaymentCredentialsModal`, `EditAgentModal`, `AccountDetailClient`). In every case the edit is a single Tailwind class on the overlay's outermost wrapper — `z-50`/`z-[100]`/`z-[110]`/`z-[200]` → `z-[var(--v2-z-modal)]` — with no change to what any modal renders, what it submits, what it asks the user to confirm, or when it appears; the amount, recipient and approval copy each dialog shows are untouched, so nothing a user authorises is presented differently. The direction of the modal migration is strictly UPWARD (50/100/110 → 200), which cannot hide a confirmation surface behind anything; it in fact FIXES three overlays (`AccountsOverviewClient`, `PaymentCredentialsModal`, `EditAgentModal`) that sat at `z-50` and were therefore rendering underneath `TopBar` — a pre-existing defect where part of a payment-credential or agent-edit dialog was occluded by the app bar. The user-visible effect on the money path is that dialogs which ask for confirmation are now fully visible rather than partially covered, and that navigation to money screens is reachable on mobile at all, which it was not. Nothing is auto-confirmed, nothing is dismissed on the user's behalf, and no dialog's dismissal semantics changed. Mutation-proven in five directions: restoring the original `z-[100]`/`z-[60]` fails the source-level scale guard AND fails five of six browser tests on `reachesToggle: false`; inverting the scale (`--v2-z-chrome: 160`) fails two independent ordering assertions; demoting one modal (`SendModal` → `z-[110]`) fails the new full-screen-overlay assertion, naming the file. The defect and the fix were both measured in a real browser rather than inferred from CSS — pre-fix, `document.elementFromPoint` at the toggle's centre returned `TopBar`'s inner row and a non-forced Playwright click failed with "intercepts pointer events", at 320/390/768/1023px; post-fix it returns the toggle's own icon and the click opens the drawer, at the same four widths. The full 23-test gating browser suite passes after the modal migration. Perimeter unchanged.
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/product/design-system.md @ 69a6ff0941dc9f7619cad638a546f9033d06cae2 -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/frontend/src/app/globals.css
  - packages/frontend/tailwind.config.js
  - packages/frontend/src/components/ui/**
  - packages/frontend/src/app/layout.tsx
  - packages/frontend/src/app/page.tsx
  - packages/frontend/src/app/how-it-works/**
  - packages/frontend/src/app/protocols/**
  - packages/frontend/src/app/(authenticated)/design-system/**
  - packages/frontend/src/components/marketing/**
  - packages/frontend/src/components/sidebar/**
  - packages/frontend/src/components/TopBar.tsx
  - packages/frontend/src/components/haven/TransactionActivityRow.tsx
  - packages/frontend/src/components/haven/TransactionMovement.tsx
  - packages/frontend/src/components/transactions/**
last-verified: "2026-08-21" # #1708: the documented primary/ghost focus ring was the dead arbitrary-value form; re-read against globals.css + tailwind.config.js and corrected, plus a new "Opacity on a token colour" rule. Token tables and the rest of the body NOT re-verified in this pass. # #1726: Buttons § gains the Tap targets rule — sm/md extend an invisible 44px hit area rather than raising h-9/h-10; the rest of § Buttons re-read and still accurate # #1749: new "Layering (z-index)" § under Tokens — the shell's stacking order is now a named scale in globals.css, and the mobile nav overlay deliberately outranks the chrome. Only § Tokens re-verified in this pass
---

# Haven Design System

This is the source of truth for Haven's current light visual language. Companion to the product UX guide (`docs/product/README.md`, which documents product doctrine, vocabulary, and IA — those rules **still apply**). If older docs mention a dark app surface system, **this document supersedes them**.

The production authenticated app and `/design-system` are the live references for product UX. The production marketing routes are the live references for marketing UX: `/`, `/how-it-works`, `/protocols/x402`, and `/protocols/mpp`. When in doubt, open the live route, inspect the element, and match the system here.

---

## 1. Tokens

All tokens live as CSS custom properties at `:root` in `packages/frontend/src/app/globals.css`. Core color, radius, and shadow tokens are mirrored in `packages/frontend/tailwind.config.js` so they are usable as `bg-bg`, `text-ink`, `border-border`, etc. Newer production tokens such as typography utilities, raised cards, popovers, modal backdrop, and the brand gradient may exist as CSS variables/classes only until they are promoted into Tailwind.

### Surfaces

| Token | Value | Use |
|---|---|---|
| `--v2-bg` | `#ffffff` | Page background |
| `--v2-surface` | `#f6f9fc` | Alternating section bands, card hover backgrounds |
| `--v2-surface-2` | `#eef2f7` | Disabled states, deeper card stacking |
| `--v2-surface-code` | `#0b1120` | Dark code blocks on light pages (Stripe pattern) |
| `--v2-surface-hover` | `#f0f4f9` | Sidebar/user-menu row hover and subtle interactive shells |
| `--v2-modal-backdrop` | `rgba(26, 31, 54, 0.66)` | Modal backdrop with blur |

### Ink (text)

| Token | Value | Use |
|---|---|---|
| `--v2-ink` | `#1a1f36` | Headings, primary text, amounts |
| `--v2-ink-2` | `#525f7f` | Body text, secondary information |
| `--v2-ink-3` | `#5d6c85` | Tertiary text, eyebrows, captions — AA-safe (≥4.5:1) on white and all tinted surfaces |
| `--v2-ink-on-brand` | `#ffffff` | Text on brand‑colored or dark surfaces |

### Borders

| Token | Value | Use |
|---|---|---|
| `--v2-border` | `#e6ebf1` | Default hairline (cards, dividers) |
| `--v2-border-strong` | `#d6dbe3` | Hover, ghost button borders, flow arrows |

### Brand

| Token | Value | Use |
|---|---|---|
| `--v2-brand` | `#4f46e5` (indigo‑600) | Primary CTA bg, links, accents, brand mark |
| `--v2-brand-strong` | `#4338ca` (indigo‑700) | Primary CTA hover |
| `--v2-brand-soft` | `#eef2ff` | Brand‑tinted card backgrounds, focus rings |
| `--v2-brand-gradient` | `linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)` | Gradient wordmark or one restrained brand accent |

Use `.v2-brand-gradient-text` for the production app wordmark. In product UI, do not use the gradient for buttons, badges, large panels, or repeated decoration.

### Semantic

| Token | Value | Soft variant | Use |
|---|---|---|---|
| `--v2-success` | `#047857` | `--v2-success-soft` `#ecfdf5` | Settled, confirmed, incoming |
| `--v2-debit` | `#0369a1` | `--v2-debit-soft` `#f0f9ff` | Outgoing / sent money (sibling to success; never a warning) |
| `--v2-warning` | `#b54708` | `--v2-warning-soft` `#fef3c7` | 402 Payment Required, pending review |
| `--v2-danger` | `#b42318` | `--v2-danger-soft` `#fef2f2` | Failed, destructive |

Same rule as v1: **never repurpose a semantic color**.

**Contrast guarantee:** every ink and semantic text token meets WCAG AA (≥4.5:1) against white, its own `-soft` background, and the tinted surfaces (`--v2-surface`, `--v2-surface-2`, hover)....
```

### `GH-CAND-0016`

- Source URL: https://github.com/d-hinders/Haven-AI/pull/1765
- Repository: `d-hinders/Haven-AI`
- PR number: `1765`
- PR title: fix(passport): a re-mint requires positive evidence the prior attest is dead (#1745)
- Language: `typescript`
- Code changed files: `['packages/backend/src/index.ts', 'packages/backend/src/infra/repositories/__tests__/outbound-txs.test.ts', 'packages/backend/src/infra/repositories/outbound-txs.ts', 'packages/backend/src/modules/passport/__tests__/anchor-seams-wired.test.ts', 'packages/backend/src/modules/passport/__tests__/anchor-tx-liveness.test.ts', 'packages/backend/src/modules/passport/__tests__/issuance-hardening.test.ts', 'packages/backend/src/modules/passport/__tests__/presumed-dropped-attest.test.ts', 'packages/backend/src/modules/passport/attestation.ts', 'packages/backend/src/modules/passport/index.ts', 'packages/backend/src/modules/passport/issuance.ts']`
- Docs changed files: `['docs/architecture/11-agent-passport-schema.md', 'docs/operations/backend-scaling.md', 'docs/operations/delegation-rail-vendor-ops.md', 'docs/regulatory/casp-changelog/2026-08-21-1745.md']`

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
diff --git a/packages/backend/src/index.ts b/packages/backend/src/index.ts
--- a/packages/backend/src/index.ts
+++ b/packages/backend/src/index.ts
@@ -28,8 +28,10 @@ import agentPassportRoutes from './routes/agent-passports.js'
 import {
   setAnchor,
   setAnchorRecovery,
+  setAnchorLiveness,
   anchorOnChain,
   recoverAnchorFromReceipt,
+  classifyAnchorTxLiveness,
   setRevoker,
   revokeOnChain,
   setReceiptSigningKey,
@@ -207,6 +209,11 @@ app.get('/chains', async () => {
 // (#972 / #973). Both are governance metadata: EAS-only targets, zero value.
 setAnchor(anchorOnChain)
 setAnchorRecovery(recoverAnchorFromReceipt)
+// A null receipt is not evidence the attest was dropped (#1745). The re-mint
+// is unlocked only by this probe finding the transaction's nonce burned by
+// something else; anything less leaves the passport retryable rather than
+// minting a second live credential.
+setAnchorLiveness(classifyAnchorTxLiveness)
 setRevoker(revokeOnChain)
 // Receipts the merchant-facing verifier hands out (#974) are signed with a
 // DEDICATED key, never the relayer's: the relayer pays gas for user-authorised

diff --git a/packages/backend/src/infra/repositories/__tests__/outbound-txs.test.ts b/packages/backend/src/infra/repositories/__tests__/outbound-txs.test.ts
--- a/packages/backend/src/infra/repositories/__tests__/outbound-txs.test.ts
+++ b/packages/backend/src/infra/repositories/__tests__/outbound-txs.test.ts
@@ -14,6 +14,7 @@ import {
   claimOrphanedOutboundTx,
   countLaneAttemptsAtNonce,
   enqueueOutboundTx,
+  findOutboundTxByHash,
   listUnminedOutboundTxs,
   markOutboundTxBroadcast,
   markOutboundTxFailed,
@@ -344,3 +345,76 @@ describeDb('bump tick end-to-end over the REAL repository (#1559 review)', () =>
     expect(rows.rows[1]).toMatchObject({ status: 'broadcast', nonce: '33' })
   })
 })
+
+/**
+ * #1745: the by-hash read. It exists to hand the passport recovery path ONE
+ * fact — the nonce a broadcast was stamped with — because that is what
+ * separates "this attest can still mine" from "its slot is already gone". A
+ * wrong answer here becomes a duplicate live credential, so the scoping and
+ * the normalisation are the tests.
+ */
+describeDb('findOutboundTxByHash (#1745)', () => {
+  beforeAll(() => initDbHarness())
+  beforeEach(async () => {
+    CHAIN = ++chainCounter
+    await resetDb()
+  })
+
+  it('returns the row with its stamped nonce, and normalises a MIXED-CASE hash', async () => {
+    const row = await enqueue('passport_attest')
+    await markOutboundTxBroadcast(row.id, { txHash: TX, nonce: 7n })
+
+    expect(await findOutboundTxByHash(CHAIN, TX)).toMatchObject({
+      id: row.id,
+      nonce: '7',
+      status: 'broadcast',
+    })
+
+    // Hashes are stored lowercased. A caller holding the checksummed form
+    // must not silently get "no record" — the probe reads that as "no
+    // evidence", which turns a recoverable stall into a permanent one.
+    const upper = '0x' + TX.slice(2).toUpperCase()
+    expect(await findOutboundTxByHash(CHAIN, upper)).toMatchObject({ id: row.id })
+  })
+
+  it('is CHAIN-SCOPED — the same hash on another chain is a different record', async () => {
+    const row = await enqueue('passport_attest')
+    await markOutboundTxBroadcast(row.id, { txHash: TX, nonce: 7n })
+
+    // The same relayer key signing the same calldata at the same nonce on a
+    // second chain produces the SAME hash. An unscoped read would hand back
+    // the other chain's nonce — the one fact the caller is here for.
+    const otherChain = ++chainCounter
+    const twin = await enqueueOutboundTx({
+      chainId: otherChain,
+      submitter: 'passport_attest',
+      toAddress: TO,
+      data: DATA,
+    })
+    await markOutboundTxBroadcast(twin.id, { txHash: TX, nonce: 99n })
+
+    expect(await findOutboundTxByHash(CHAIN, TX)).toMatchObject({ nonce: '7' })
+    expect(await findOutboundTxByHash(otherChain, TX)).toMatchObject({ nonce: '99' })
+  })
+
+  it('returns null for a hash nothing broadcast', async () => {
+    await enqueue('passport_attest') // queued, never stamped
+    expect(await findOutboundTxByHash(CHAIN, TX)).toBeNull()
+  })
+
+  it('returns the NEWEST row when one hash appears twice', async () => {
+    // Not reachable for `passport_attest` (never replaced, #1735), but the
+    // read is generic and an ambiguous answer here is an arbitrary nonce.
+    const older = await enqueue('sweep')
+    await markOutboundTxBroadcast(older.id, { txHash: TX, nonce: 1n })
+    await markOutboundTxMined(older.id)
+    await db.query(
+      `UPDATE outbound_txs SET created_at = NOW() - INTERVAL '1 hour' WHERE id = $1`,
+      [older.id],
+    )
+    const newer = await enqueue('sweep')
+    await markOutboundTxBroadcast(newer.id, { txHash: TX, nonce: 2n })
+
+    expect(await findOutboundTxByHash(CHAIN, TX)).toMatchObject({ id: newer.id, nonce: '2' })
+  })
+})

diff --git a/packages/backend/src/infra/repositories/outbound-txs.ts b/packages/backend/src/infra/repositories/outbound-txs.ts
--- a/packages/backend/src/infra/repositories/outbound-txs.ts
+++ b/packages/backend/src/infra/repositories/outbound-txs.ts
@@ -137,6 +137,42 @@ export const CLAIM_ORPHANED_OUTBOUND_TX_SQL = `UPDATE outbound_txs
 export const COUNT_LANE_ATTEMPTS_AT_NONCE_SQL = `SELECT COUNT(*)::int AS n FROM outbound_txs
    WHERE chain_id = $1 AND nonce = $2 AND status IN ('replaced', 'failed')`
 
+/**
+ * The durable record for one broadcast hash (#1745).
+ *
+ * Chain-scoped because `tx_hash` is only unique WITHIN a chain — the same
+ * relayer key signing identical calldata at the same nonce on two chains
+ * produces the same hash, and an unscoped read would hand back the wrong
+ * chain's nonce, which is the one fact the caller is here for.
+ *
+ * `ORDER BY created_at DESC` is not decoration: a bump writes a NEW row for
+ * the replacement, and while `passport_attest` is never replaced (#1735),
+ * this read is generic. Newest-first means the caller sees the row that
+ * describes the current attempt.
+ *
+ * No index backs this (061 indexes the lane, the unmined scan and the live
+ * nonce, not the hash). Deliberate — the only caller is the passport
+ * recovery path, which runs at most once per stuck anchor per backoff tick,
+ * and a migration for it would gate this fix on CODEOWNERS review. If a hot
+ * path ever wants this read, add the index then.
+ */
+export const FIND_OUTBOUND_TX_BY_HASH_SQL = `SELECT * FROM outbound_txs
+   WHERE chain_id = $1 AND tx_hash = $2
+   ORDER BY created_at DESC, id
+   LIMIT 1`
+
+export async function findOutboundTxByHash(
+  chainId: number,
+  txHash: string,
+  db: Executor = pool,
+): Promise<OutboundTxRow | null> {
+  const { rows } = await db.query<OutboundTxRow>(FIND_OUTBOUND_TX_BY_HASH_SQL, [
+    chainId,
+    txHash.toLowerCase(),
+  ])
+  return rows[0] ?? null
+}
+
 export async function enqueueOutboundTx(
   params: {
     chainId: number

diff --git a/packages/backend/src/modules/passport/__tests__/anchor-seams-wired.test.ts b/packages/backend/src/modules/passport/__tests__/anchor-seams-wired.test.ts
--- a/packages/backend/src/modules/passport/__tests__/anchor-seams-wired.test.ts
+++ b/packages/backend/src/modules/passport/__tests__/anchor-seams-wired.test.ts
@@ -0,0 +1,57 @@
+/**
+ * The passport anchor's three seams are actually WIRED at boot (#1745).
+ *
+ * `issuance.ts` is deliberately chain-free: the anchor, the receipt recovery
+ * and the liveness probe are all injected, which is what makes the state
+ * machine testable without ethers or a relayer. The cost of that design is
+ * that deleting a `setX(...)` line in `index.ts` breaks nothing visibly —
+ * every unit test injects its own seam and passes regardless.
+ *
+ * For the liveness probe that failure is silent AND severe: with no probe
+ * wired, `issuePassport` refuses every re-mint (the fail-safe default), so
+ * issuance would stall repo-wide rather than duplicate — loud eventually, but
+ * only via the attention counter. And if a future edit ever flipped that
+ * default the other way, an unwired probe would restore the pre-#1745
+ * duplicate-credential behaviour exactly.
+ *
+ * A source assertion rather than a boot: importing `index.ts` builds a Fastify
+ * app, opens a pool and starts timers. The repo already uses source scanning
+ * for guards of this shape (the bare-numeric-chain-fallback guard).
+ */
+import { readFileSync } from 'node:fs'
+import { fileURLToPath } from 'node:url'
+import { describe, expect, it } from 'vitest'
+
+const INDEX = readFileSync(
+  fileURLToPath(new URL('../../../index.ts', import.meta.url)),
+  'utf8',
+)
+
+/** Comments mention these names constantly — assert on the CALL, not the word. */
+function callsWith(fn: string, arg: string): boolean {
+  return new RegExp(`\\b${fn}\\s*\\(\\s*${arg}\\s*\\)`).test(INDEX)
+}
+
+describe('passport anchor seams are wired in index.ts', () => {
+  it.each([
+    ['setAnchor', 'anchorOnCh...
```

Allowed model input — docs before excerpt:

```markdown
<!-- docs/architecture/11-agent-passport-schema.md @ a5530299eca900069c7c38e892db8c2eff26b0a9 -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/backend/src/modules/passport/**
  - packages/backend/src/infra/repositories/agent-passports.ts
  - packages/backend/src/routes/agent-passports.ts
  - packages/backend/src/routes/passport-verify.ts
  - packages/backend/scripts/register-passport-schema.ts
  - packages/backend/src/db/migrations/048_agent_passports.ts
  - packages/backend/src/db/migrations/049_agent_passport_revocation.ts
  - packages/backend/src/db/migrations/050_agent_passport_revocation_index.ts
  - packages/backend/src/db/migrations/051_agent_passport_addresses.ts
last-verified: "2026-08-21" # #1742: the sweep's phase isolation protects against a THROW, not a hang — `revokeOnChain`'s bare `tx.wait()` could park the revocation phase and the stuck-revoke alarm downstream of it indefinitely. The wait is now bounded; the retry/backoff model, the no-terminal-failed-state rule and the verifier precedence are unchanged. Prior: #1735: the "recovered, never re-minted" claim is qualified — recovery is keyed off the persisted tx hash (hence the bump-worker exclusion) and presumes a null receipt means dropped, so a fee-stuck anchor can still re-mint (#1745). Anchor wait disposition on expiry recorded. Rest of the anchoring/revocation prose re-read against the code and unchanged.
---

# L0 Agent Passport — EAS schema

The passport is a signed, on-chain-anchored, revocable credential attesting an
agent's **provenance, enforced controls, and live status**. This doc fixes the
schema's field semantics and the two encodings that are easy to get wrong.
Epic: [#970](https://github.com/d-hinders/Haven-AI/issues/970); this schema is
[#971](https://github.com/d-hinders/Haven-AI/issues/971).

## What L0 attests — and what it does not

This distinction is the product, not a caveat. Blurring it is the one failure
mode that would matter.

| L0 **does** attest | L0 does **NOT** attest |
|---|---|
| **Issued by Haven** — this agent was provisioned by a known operator | **Who is accountable** — no legal or natural person is identified |
| **Bound to a treasury** — the account whose funds it can spend | Anything KYC-derived |
| **Enforced policy** — a pointer to the on-chain controls that bound it | That the agent behaves well, or that its operator is reputable |
| **Live status** — revocable, with revocation authoritative off-chain | Regulatory compliance of any kind |

Naming discipline, from the epic: say **issued / governed / revocable**.
*Verified* is reserved for L2 (ZK-anchored KYC) and must not appear in copy,
API fields, or docs describing L0. L0 attests **governance, not identity**.

**No PII is in the schema.** Everything person-shaped stays off-chain behind
Haven's API. Note the graph is permanently public regardless: treasury → N
agents → issued-by-Haven is visible to anyone reading the chain, even with
policy detail API-gated. That is a conscious trade (epic §open questions), not
an oversight.

**Field minimization is the only bound on that graph.** It limits what each
attestation says; it does not limit which agents appear in it. Every opted-in
agent is anchored whether or not it ever transacts — see
[anchoring happens at opt-in](#anchoring-happens-at-opt-in-and-that-is-a-revised-decision)
for why that exposure was accepted.

## Fields

Registered as one EAS schema, `revocable = true`, no resolver:

```text
address agentEoa,address smartAccount,address treasury,uint8 assuranceLevel,
string policyUri,uint64 issuedAt,uint64 expiresAt
```

| Field | Meaning |
|---|---|
| `agentEoa` | `agents.delegate_address`. **Required.** |
| `smartAccount` | The Hybrid delegator. **Optional** — zero address when absent. |
| `treasury` | The account the agent spends from — the "bound to" claim. |
| `assuranceLevel` | `uint8` ladder: `0` = L0 (issuable). `1`/`2` reserved. The verifier **reads** this from the row and refuses to issue a receipt for any level it cannot issue, rather than clamping to L0 — understating a tier is a wrong answer presented as a right one ([#975](https://github.com/d-hinders/Haven-AI/issues/975)). |
| `policyUri` | Pointer to the enforced controls; detail resolves via Haven's API. |
| `issuedAt` / `expiresAt` | Unix seconds. Expiry is a claim, not enforcement. |

> **The schema string is immutable once registered.** Field order, names and
> types all feed the UID; changing any of them mints a *different* schema and
> orphans every passport already attested. A change is a new schema plus a
> migration, never an edit.

## The two encodings that bite

### 1. Both addresses are bound, and either must verify

Owner decision 2026-07-24. [#946](https://github.com/d-hinders/Haven-AI/issues/946)
made settlement a **per-payment** choice, and a merchant sees a different
address on each path:

- **EIP-3009 leg** → the merchant sees the **agent EOA** as `from`.
- **erc7710 redemption** → the merchant see...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/docs/architecture/11-agent-passport-schema.md b/docs/architecture/11-agent-passport-schema.md
--- a/docs/architecture/11-agent-passport-schema.md
+++ b/docs/architecture/11-agent-passport-schema.md
@@ -11,7 +11,7 @@ covers:
   - packages/backend/src/db/migrations/049_agent_passport_revocation.ts
   - packages/backend/src/db/migrations/050_agent_passport_revocation_index.ts
   - packages/backend/src/db/migrations/051_agent_passport_addresses.ts
-last-verified: "2026-08-21" # #1742: the sweep's phase isolation protects against a THROW, not a hang — `revokeOnChain`'s bare `tx.wait()` could park the revocation phase and the stuck-revoke alarm downstream of it indefinitely. The wait is now bounded; the retry/backoff model, the no-terminal-failed-state rule and the verifier precedence are unchanged. Prior: #1735: the "recovered, never re-minted" claim is qualified — recovery is keyed off the persisted tx hash (hence the bump-worker exclusion) and presumes a null receipt means dropped, so a fee-stuck anchor can still re-mint (#1745). Anchor wait disposition on expiry recorded. Rest of the anchoring/revocation prose re-read against the code and unchanged.
+last-verified: "2026-08-22" # #1745: the SECOND limit on "recovered, never re-minted" is closed — a null receipt no longer presumes dropped; a re-mint needs positive evidence the prior tx can never mine (its nonce consumed by something else). The bounded-stall argument and the still-open time question (#1743) are recorded rather than implied. The first limit (hash-keyed recovery) stands. Prior: #1742: the sweep's phase isolation protects against a THROW, not a hang — `revokeOnChain`'s bare `tx.wait()` could park the revocation phase and the stuck-revoke alarm downstream of it indefinitely. The wait is now bounded; the retry/backoff model, the no-terminal-failed-state rule and the verifier precedence are unchanged. Prior: #1735: the "recovered, never re-minted" claim is qualified — recovery is keyed off the persisted tx hash (hence the bump-worker exclusion) and presumes a null receipt means dropped, so a fee-stuck anchor can still re-mint (#1745). Anchor wait disposition on expiry recorded. Rest of the anchoring/revocation prose re-read against the code and unchanged.
 ---
 
 # L0 Agent Passport — EAS schema
@@ -202,11 +202,44 @@ true today:
   expiry of the 120 s wait leaves the outbound record `broadcast` (for
   chain-first reconciliation) instead of closing it `failed` as a revert.
 - `getTransactionReceipt` returns `null` for a **pending** transaction exactly
-  as for a dropped one, and the retry presumes dropped — so a fee-stuck anchor
-  can still be re-minted at the next nonce, ≈180 s after broadcast. Tracked as
-  [#1745](https://github.com/d-hinders/Haven-AI/issues/1745); the
-  [vendor-ops runbook](../operations/delegation-rail-vendor-ops.md) §3
-  sequences operator action around it.
+  as for a dropped one, so the absence of a receipt is not evidence the
+  transaction died. Until
+  [#1745](https://github.com/d-hinders/Haven-AI/issues/1745) the retry presumed
+  dropped and re-minted at the next nonce ≈180 s after broadcast; it no longer
+  does. A re-mint now requires **positive evidence that the prior transaction
+  can never mine** — its nonce consumed by something else, read as the
+  relayer's mined `getTransactionCount` past the nonce the outbound record
+  (#1556) stamped at broadcast. A transaction only ever mines into its own
+  nonce and a nonce is spent once, so that is arithmetic rather than a
+  deadline. Anything weaker — a transaction any node still knows, a missing or
+  un-stamped record, a `replaced`/`mined` record, an unreadable provider, or a
+  receipt that appears on the confirming re-read — withholds the re-mint and
+  leaves the passport retryable.
+
+  Two consequences worth stating, because they are the shape of the trade.
+  **The stall ends when the nonce is burned, and in practice that is the
+  operator's cancel — not Haven's own traffic.** It is tempting to argue that a
+  dropped transaction stops reserving its nonce, so the relayer's next
+  broadcast takes the slot and issuance recovers by itself. It does not, and
+  the reason is worth knowing: `submitRecorded` allocates from
+  `getNonce('pending')`, but the stuck attest still holds a `broadcast` row at
+  that nonce, and migration 061's partial UNIQUE index on
+  `(chain_id, nonce) WHERE status = 'broadcast'` refuses the stamp — the queue
+  retries, re-reads the same nonce, and throws `could not win a nonce lane`.
+  So the lane #1735 already documents as blocked stays blocked, and what burns
+  the nonce is the same-nonce cancel in the
+  [vendor-ops runbook](../operations/delegation-rail-vendor-ops.md) §3. The
+  gain is that the cancel is now **sufficient on its own**: once it mines, the
+  burned nonce is exactly the evidence the sweep needs, so issuance completes
+  on its next tick with no further operator action and no duplicate to hunt
+  for first. While it waits, the row keeps failing retryably and alarms
+  through `ISSUANCE_ATTENTION_ATTEMPTS`. **The time question is deliberately
+  open:** how
+  long an attest whose nonce is *still open* may sit before Haven declares it
+  dead on its own is an owner decision with duplicate-credential consequences,
+  tracked as [#1743](https://github.com/d-hinders/Haven-AI/issues/1743) and not
+  taken in code. Until it is, such an attest is live for as long as it holds
+  its nonce.
 
 ## Revocation — what merchants must check

diff --git a/docs/operations/backend-scaling.md b/docs/operations/backend-scaling.md
--- a/docs/operations/backend-scaling.md
+++ b/docs/operations/backend-scaling.md
@@ -7,7 +7,7 @@ covers:
   - packages/backend/src/platform/leader-lock.ts
   - packages/backend/src/rails/hybrid-provisioning.ts
   - packages/backend/src/infra/relayer.ts
-last-verified: "2026-08-21" # #1735: the "self-healing on the queue lane" claim gains its exception — a stuck `passport_attest` is deliberately NOT fee-replaced (a replacement orphans the hash #1043 recovery is keyed off), so that lane blocks until an operator acts; cross-ref to the #1745 ordering constraint. Prior: #1722: the deploy lock's connection hold now has a real ceiling — the confirmation wait is `tx.wait(1, 120_000)`, bracketed under the bump worker's 180 s adoption age, and expiry hands the tx to that worker instead of marking the record failed. The rest of the accept (burst threshold, fail-open scoping, the 502 shape) re-read and unchanged. Prior: #1680: rate-limit counters join the list of things multiple replicas now handle — the plugin's in-process store made the real ceiling max × replicas, fixed with a shared Postgres tier (fail-open, 250 ms deadline, leader-gated sweep) on the same pattern as the #718 nonce watermark. Prior: #1559: queue-lane nonce correctness is DB-arbitrated (submitRecorded stamp-before-broadcast); multi-replica correctness now gated only on the Safe-bound legacy sites (#1440); #1558 bump worker noted on the stall point
+last-verified: "2026-08-22" # #1745: the "single point of stall" entry drops the ordering constraint it carried — no duplicate attest is queued while the stuck one is live — and records that the operator's same-nonce cancel now completes issuance by itself. The blocked-lane trade itself is unchanged. Prior: #1735: the "self-healing on the queue lane" claim gains its exception — a stuck `passport_attest` is deliberately NOT fee-replaced (a replacement orphans the hash #1043 recovery is keyed off), so that lane blocks until an operator acts; cross-ref to the #1745 ordering constraint. Prior: #1722: the deploy lock's connection hold now has a real ceiling — the confirmation wait is `tx.wait(1, 120_000)`, bracketed under the bump worker's 180 s adoption age, and expiry hands the tx to that worker instead of marking the record failed. The rest of the accept (burst threshold, fail-open scoping, the 502 shape) re-read and unchanged. Prior: #1680: rate-limit counters join the list of things multiple replicas now handle — the plugin's in-process store made the real ceiling max × replicas, fixed with a shared Postgres tier (fail-open, 250 ms deadline, leader-gated sweep) on the same pattern as the #718 nonce watermark. Prior: #1559: queue-lane nonce correctness is DB-arbitrated (submitRecorded stamp-before-broadcast); multi-replica correctness now gated only on the Safe-bound legacy sites (#1440); #1558 bump worker noted on the stall point
 ---
 
 # Backend Scaling
@@ -261,10 +261,20 @@ they queue behind the same key. Two consequences worth planning around:
    trade: a blocked lane is loud, bounded and human-recoverable; a duplicate
    attestation is silent and permanent. See
    [`delegation-rail-vendor-ops.md`](delegation-rail-vendor-ops.md) §3 for the
-   operator response — including the ordering constraint from
-   [#1745](https://github.com/d-hinders/Haven-AI/issues/1745), where the
-   passport's own retry sw...
```

Audit context only — docs after excerpt:

```markdown
<!-- docs/architecture/11-agent-passport-schema.md @ 4782cee87337d056592e0ed346f49b7a1ff00721 -->
---
owner: "@d-hinders"
status: current
covers:
  - packages/backend/src/modules/passport/**
  - packages/backend/src/infra/repositories/agent-passports.ts
  - packages/backend/src/routes/agent-passports.ts
  - packages/backend/src/routes/passport-verify.ts
  - packages/backend/scripts/register-passport-schema.ts
  - packages/backend/src/db/migrations/048_agent_passports.ts
  - packages/backend/src/db/migrations/049_agent_passport_revocation.ts
  - packages/backend/src/db/migrations/050_agent_passport_revocation_index.ts
  - packages/backend/src/db/migrations/051_agent_passport_addresses.ts
last-verified: "2026-08-22" # #1745: the SECOND limit on "recovered, never re-minted" is closed — a null receipt no longer presumes dropped; a re-mint needs positive evidence the prior tx can never mine (its nonce consumed by something else). The bounded-stall argument and the still-open time question (#1743) are recorded rather than implied. The first limit (hash-keyed recovery) stands. Prior: #1742: the sweep's phase isolation protects against a THROW, not a hang — `revokeOnChain`'s bare `tx.wait()` could park the revocation phase and the stuck-revoke alarm downstream of it indefinitely. The wait is now bounded; the retry/backoff model, the no-terminal-failed-state rule and the verifier precedence are unchanged. Prior: #1735: the "recovered, never re-minted" claim is qualified — recovery is keyed off the persisted tx hash (hence the bump-worker exclusion) and presumes a null receipt means dropped, so a fee-stuck anchor can still re-mint (#1745). Anchor wait disposition on expiry recorded. Rest of the anchoring/revocation prose re-read against the code and unchanged.
---

# L0 Agent Passport — EAS schema

The passport is a signed, on-chain-anchored, revocable credential attesting an
agent's **provenance, enforced controls, and live status**. This doc fixes the
schema's field semantics and the two encodings that are easy to get wrong.
Epic: [#970](https://github.com/d-hinders/Haven-AI/issues/970); this schema is
[#971](https://github.com/d-hinders/Haven-AI/issues/971).

## What L0 attests — and what it does not

This distinction is the product, not a caveat. Blurring it is the one failure
mode that would matter.

| L0 **does** attest | L0 does **NOT** attest |
|---|---|
| **Issued by Haven** — this agent was provisioned by a known operator | **Who is accountable** — no legal or natural person is identified |
| **Bound to a treasury** — the account whose funds it can spend | Anything KYC-derived |
| **Enforced policy** — a pointer to the on-chain controls that bound it | That the agent behaves well, or that its operator is reputable |
| **Live status** — revocable, with revocation authoritative off-chain | Regulatory compliance of any kind |

Naming discipline, from the epic: say **issued / governed / revocable**.
*Verified* is reserved for L2 (ZK-anchored KYC) and must not appear in copy,
API fields, or docs describing L0. L0 attests **governance, not identity**.

**No PII is in the schema.** Everything person-shaped stays off-chain behind
Haven's API. Note the graph is permanently public regardless: treasury → N
agents → issued-by-Haven is visible to anyone reading the chain, even with
policy detail API-gated. That is a conscious trade (epic §open questions), not
an oversight.

**Field minimization is the only bound on that graph.** It limits what each
attestation says; it does not limit which agents appear in it. Every opted-in
agent is anchored whether or not it ever transacts — see
[anchoring happens at opt-in](#anchoring-happens-at-opt-in-and-that-is-a-revised-decision)
for why that exposure was accepted.

## Fields

Registered as one EAS schema, `revocable = true`, no resolver:

```text
address agentEoa,address smartAccount,address treasury,uint8 assuranceLevel,
string policyUri,uint64 issuedAt,uint64 expiresAt
```

| Field | Meaning |
|---|---|
| `agentEoa` | `agents.delegate_address`. **Required.** |
| `smartAccount` | The Hybrid delegator. **Optional** — zero address when absent. |
| `treasury` | The account the agent spends from — the "bound to" claim. |
| `assuranceLevel` | `uint8` ladder: `0` = L0 (issuable). `1`/`2` reserved. The verifier **reads** this from the row and refuses to issue a receipt for any level it cannot issue, rather than clamping to L0 — understating a tier is a wrong answer presented as a right one ([#975](https://github.com/d-hinders/Haven-AI/issues/975)). |
| `policyUri` | Pointer to the enforced controls; detail resolves via Haven's API. |
| `issuedAt` / `expiresAt` | Unix seconds. Expiry is a claim, not enforcement. |

> **The schema string is immutable once registered.** Field order, names and
> types all feed the UID; changing any of them mints a *different* schema and
> orphans every passport already attested. A change is a new schema plus a
> migration, never an edit.

## The two en...
```

### `GH-CAND-0017`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/88
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `88`
- PR title: Extend trust delegation to Agent Plugins and A2A agents
- Language: `typescript`
- Code changed files: `['schemas/organization.schema.json', 'src/consolidate.test.ts', 'src/consolidate.ts', 'src/validate.test.ts', 'website/src/types.ts']`
- Docs changed files: `[]`

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
@@ -103,6 +103,16 @@
                 "type": "object",
                 "additionalProperties": false,
                 "description": "Trust the organization's MCP server approvals. Empty today — reserved for future per-type conditions."
+              },
+              "plugins": {
+                "type": "object",
+                "additionalProperties": false,
+                "description": "Trust the organization's Agent Plugin approvals. Empty today — reserved for future per-type conditions."
+              },
+              "agents": {
+                "type": "object",
+                "additionalProperties": false,
+                "description": "Trust the organization's A2A agent approvals. Empty today — reserved for future per-type conditions."
               }
             }
           }

diff --git a/src/consolidate.test.ts b/src/consolidate.test.ts
--- a/src/consolidate.test.ts
+++ b/src/consolidate.test.ts
@@ -8,9 +8,10 @@ import {
   addAgentApproval,
   resolveSkillInstallUrls,
   resolveSkillTrust,
-  filterValidSkillTrusts,
   resolveMcpTrust,
-  filterValidMcpTrusts,
+  resolvePluginTrust,
+  resolveAgentTrust,
+  filterValidTrusts,
   enrichWithRegistryData,
   resolveVendorMetadata,
   pickWinningGenericConfig,
@@ -32,8 +33,7 @@ import {
   type SkillEntry,
   type PluginEntry,
   type AgentEntry,
-  type SkillTrustEntry,
-  type McpTrustEntry,
+  type TrustEntry,
 } from "./consolidate.js";
 
 function emptyOutput(): ConsolidatedOutput {
@@ -1008,7 +1008,7 @@ describe("addAgentApproval", () => {
 describe("addOrganization — trust extraction", () => {
   it("collects a skill trust entry", () => {
     const output = emptyOutput();
-    const skillTrusts: SkillTrustEntry[] = [];
+    const skillTrusts: TrustEntry[] = [];
     addOrganization(
       {
         id: "theia",
@@ -1043,7 +1043,7 @@ describe("addOrganization — trust extraction", () => {
 
   it("ignores a trust entry with no recognized artifact type", () => {
     const output = emptyOutput();
-    const skillTrusts: SkillTrustEntry[] = [];
+    const skillTrusts: TrustEntry[] = [];
     addOrganization(
       {
         id: "theia",
@@ -1060,11 +1060,11 @@ describe("addOrganization — trust extraction", () => {
   });
 });
 
-describe("filterValidSkillTrusts", () => {
+describe("filterValidTrusts", () => {
   const vendorIds = new Set(["theia", "anthropic", "openai", "aws"]);
 
   it("keeps trust entries referencing registered vendors", () => {
-    const { valid, unknown } = filterValidSkillTrusts(
+    const { valid, unknown } = filterValidTrusts(
       [
         { org: "theia", trustedOrg: "anthropic" },
         { org: "theia", trustedOrg: "aws" },
@@ -1076,7 +1076,7 @@ describe("filterValidSkillTrusts", () => {
   });
 
   it("separates out trust entries referencing an unregistered org", () => {
-    const { valid, unknown } = filterValidSkillTrusts(
+    const { valid, unknown } = filterValidTrusts(
       [
         { org: "theia", trustedOrg: "anthropic" },
         { org: "theia", trustedOrg: "nonexistent" },
@@ -1904,8 +1904,8 @@ describe("buildOrgEntryView", () => {
 describe("addOrganization — mcp trust extraction", () => {
   it("collects an mcp trust entry", () => {
     const output = emptyOutput();
-    const skillTrusts: SkillTrustEntry[] = [];
-    const mcpTrusts: McpTrustEntry[] = [];
+    const skillTrusts: TrustEntry[] = [];
+    const mcpTrusts: TrustEntry[] = [];
     addOrganization(
       {
         id: "theia",
@@ -1926,8 +1926,8 @@ describe("addOrganization — mcp trust extraction", () => {
 
   it("collects both a skill and an mcp trust entry from the same organization", () => {
     const output = emptyOutput();
-    const skillTrusts: SkillTrustEntry[] = [];
-    const mcpTrusts: McpTrustEntry[] = [];
+    const skillTrusts: TrustEntry[] = [];
+    const mcpTrusts: TrustEntry[] = [];
     addOrganization(
       {
         id: "theia",
@@ -1950,6 +1950,82 @@ describe("addOrganization — mcp trust extraction", () => {
   });
 });
 
+describe("addOrganization — plugin/agent trust extraction", () => {
+  it("collects a plugin trust entry", () => {
+    const output = emptyOutput();
+    const pluginTrusts: TrustEntry[] = [];
+    addOrganization(
+      {
+        id: "theia",
+        name: "Theia IDE",
+        description: "IDE",
+        website: "https://theia-ide.org",
+        trusts: [{ org: "anthropic", artifactTypes: { plugins: {} } }],
+      },
+      output,
+      [],
+      [],
+      pluginTrusts,
+    );
+    assert.deepEqual(pluginTrusts, [{ org: "theia", trustedOrg: "anthropic" }]);
+  });
+
+  it("collects an agent trust entry", () => {
+    const output = emptyOutput();
+    const agentTrusts: TrustEntry[] = [];
+    addOrganization(
+      {
+        id: "theia",
+        name: "Theia IDE",
+        description: "IDE",
+        website: "https://theia-ide.org",
+        trusts: [{ org: "anthropic", artifactTypes: { agents: {} } }],
+      },
+      output,
+      [],
+      [],
+      [],
+      agentTrusts,
+    );
+    assert.deepEqual(agentTrusts, [{ org: "theia", trustedOrg: "anthropic" }]);
+  });
+
+  it("collects skill, mcp, plugin, and agent trust entries from the same organization", () => {
+    const output = emptyOutput();
+    const skillTrusts: TrustEntry[] = [];
+    const mcpTrusts: TrustEntry[] = [];
+    const pluginTrusts: TrustEntry[] = [];
+    const agentTrusts: TrustEntry[] = [];
+    addOrganization(
+      {
+        id: "theia",
+        name: "Theia IDE",
+        description: "IDE",
+        website: "https://theia-ide.org",
+        trusts: [
+          { org: "anthropic", artifactTypes: { skills: {} } },
+          { org: "eclipsesource", artifactTypes: { mcp: {} } },
+          { org: "gemini-cli-extensions", artifactTypes: { plugins: {} } },
+          { org: "mosaico", artifactTypes: { agents: {} } },
+        ],
+      },
+      output,
+      skillTrusts,
+      mcpTrusts,
+      pluginTrusts,
+      agentTrusts,
+    );
+    assert.deepEqual(skillTrusts, [{ org: "theia", trustedOrg: "anthropic" }]);
+    assert.deepEqual(mcpTrusts, [
+      { org: "theia", trustedOrg: "eclipsesource" },
+    ]);
+    assert.deepEqual(pluginTrusts, [
+      { org: "theia", trustedOrg: "gemini-cli-extensions" },
+    ]);
+    assert.deepEqual(agentTrusts, [{ org: "theia", trustedOrg: "mosaico" }]);
+  });
+});
+
 describe("addApproval — genericConfig", () => {
   it("populates Approval.genericConfig verbatim from the approval's own root config", () => {
     const output = emptyOutput();
@@ -2306,31 +2382,6 @@ describe("resolveMcpCrossVendorConfigs", () => {
   });
 });
 
-describe("filterValidMcpTrusts", () => {
-  it("keeps trust entries referencing registered vendors", () => {
-    const { valid, unknown } = filterValidMcpTrusts(
-      [{ org: "theia", trustedOrg: "eclipsesource" }],
-      new Set(["theia", "eclipsesource"]),
-    );
-    assert.equal(valid.length, 1);
-    assert.equal(unknown.length, 0);
-  });
-
-  it("separates out trust entries referencing an unregistered org", () => {
-    const { valid, unknown } = filterValidMcpTrusts(
-      [
-        { org: "theia", trustedOrg: "eclipsesource" },
-        { org: "theia", trustedOrg: "nonexistent" },
-      ],
-      new Set(["theia", "eclipsesource"]),
-    );
-    assert.equal(valid.length, 1);
-    assert.equal(valid[0].trustedOrg, "eclipsesource");
-    assert.equal(unknown.length, 1);
-    assert.equal(unknown[0].trustedOrg, "nonexistent");
-  });
-});
-
 describe("resolveMcpTrust", () => {
   function baseOutput(): ConsolidatedOutput {
     const output = emptyOutput();
@@ -2467,6 +2518,228 @@ describe("resolveMcpTrust", () => {
   });
 });
 
+describe("resolvePluginTrust", () => {
+  function pluginWithApproval(
+    pluginId: string,
+    organizationId: string,
+  ): PluginEntry {
+    return {
+      pluginId,
+      name: pluginId,
+      description: "",
+      source: { url: "https://github.com/example/plugin.git" },
+      contentHash: "",
+      containedSkills: [],
+      containedMcpServers: [],
+      approvals: [
+        {
+          organizationId,
+          date: "2026-08-04",
+          configHash: "abc123",
+          installConfigs: [],
+        },
+      ],
+    };
+  }
+
+  it("adds a derived approval tagged with viaTrust", () => {
+    const output = emptyOutput();
+    output.plugins = [
+      pluginWithApproval("io.example/my-plugin", "gemini-cli-extensions"),
+    ];
+
+    resolvePluginTrust(output, [
+      { org: "theia", trustedOrg: "gemini-cli-extensions" },
+    ]);
+
+    assert.equal(output.plugins[0].approvals.length, 2);
+    const derived = output.plugins[0].approvals[1];
+    assert.equal(derived.organizationId, "theia");
+    assert.equal(derived.viaTrust, "gemini-cli-extensions");
+    assert.equal(derived...
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ 933ad1edf1fd8057e6e347afbd394fb1c6fc58f8 -->
# AI Registry

> **Preview** — This registry is currently in preview. Data, APIs, and the website may change as we iterate on the concept.

A vendor-neutral, federated trust registry for AI artifacts, hosted at the Eclipse Foundation. Supports [Model Context Protocol](https://modelcontextprotocol.io) (MCP) servers, [Agent Skills](https://agentskills.io), [Agent Plugins](https://agent-plugins.org), and [A2A agents](https://a2a-protocol.org).

## How It Works

The registry follows a federated model: **vendors** maintain their own repositories with approval files for AI artifacts (MCP servers, Agent Skills, Agent Plugins, and A2A agents) they endorse. A **central repository** consolidates all vendor data into a single JSON file that tools can consume.

```
Vendor Repos                    Central Repo                    Consumers
┌──────────────┐
│ Theia IDE    │──┐
│ (approvals)  │  │         ┌─────────────────┐          ┌──────────────┐
└──────────────┘  ├──────►  │  Consolidation  │────────► │  all.json    │
┌──────────────┐  │         │  + Validation   │          │  Website     │
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository
- `plugins/*.json` — one approval file per approved Agent Plugin, pointing to the plugin's source repository
- `agents/*.json` — one approval file per approved A2A agent, pointing directly at its Agent Card URL

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- Metadata enrichment from plugin source repos (name, description, version, author, contained skills/MCP servers, content hash)
- Metadata enrichment from agent card URLs (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md), [skill](skills/create-skill-approval/SKILL.md), [plugin](skills/create-plugin-approval/SKILL.md), and [agent](skills/create-agent-approval/SKILL.md) approval files
- Guidance for implementing clients — as a [website page](https://ai.open-vsx.org/docs/clients) and as a [Claude Code skill](skills/implement-registry-client/SKILL.md)

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md), [skills](skills/create-skill-approval/SKILL.md), [plugins](skills/create-plugin-approval/SKILL.md), or [agents](skills/create-agent-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata, skill source metadata, plugin source metadata, and agent card metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
plugins/
  <plugin-id>.json         # one file per approved Agent Plugin
agents/
  <agent-id>.json          # one file per approved A2A agent
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Dec...
```

Audit context only — docs diff excerpt:

```diff

```

Audit context only — docs after excerpt:

```markdown

```

### `GH-CAND-0018`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/87
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `87`
- PR title: Add per-type and per-organization JSON feeds, with an org view page
- Language: `typescript`
- Code changed files: `['src/consolidate.test.ts', 'src/consolidate.ts', 'website/src/components/OrgList.tsx', 'website/src/components/docs/docsNav.ts', 'website/src/hooks/useRegistryData.ts', 'website/src/main.tsx', 'website/src/pages/OrgPage.tsx', 'website/src/pages/docs/ApiPage.tsx', 'website/src/pages/docs/ClientsPage.tsx']`
- Docs changed files: `['skills/implement-registry-client/SKILL.md', 'skills/implement-registry-client/references/content-hash.md', 'skills/implement-registry-client/references/deep-links.md', 'skills/implement-registry-client/references/detecting-tampering.md', 'skills/implement-registry-client/references/staying-current.md']`

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
diff --git a/src/consolidate.test.ts b/src/consolidate.test.ts
--- a/src/consolidate.test.ts
+++ b/src/consolidate.test.ts
@@ -19,6 +19,7 @@ import {
   buildToolSkillView,
   buildToolPluginView,
   buildToolAgentView,
+  buildOrgEntryView,
   findOrCreate,
   configHashOf,
   type ConsolidatedOutput,
@@ -1762,6 +1763,144 @@ describe("buildToolAgentView", () => {
   });
 });
 
+describe("buildOrgEntryView", () => {
+  function servers(): McpEntry[] {
+    return [
+      {
+        serverId: "io.example/server-1",
+        name: "Server 1",
+        description: "Approved by acme",
+        mcpRegistryVerified: true,
+        approvals: [
+          {
+            organizationId: "acme",
+            date: "2026-05-01",
+            configHash: "aaa",
+            installConfigs: [{ tool: "tool-a", instructions: "use tool-a" }],
+          },
+          {
+            organizationId: "other",
+            date: "2026-05-02",
+            configHash: "bbb",
+            installConfigs: [{ tool: "tool-b", instructions: "use tool-b" }],
+          },
+        ],
+      },
+      {
+        serverId: "io.example/server-2",
+        name: "Server 2",
+        description: "Approved by other only",
+        mcpRegistryVerified: true,
+        approvals: [
+          {
+            organizationId: "other",
+            date: "2026-05-01",
+            configHash: "ccc",
+            installConfigs: [{ tool: "tool-b", instructions: "use tool-b" }],
+          },
+        ],
+      },
+      {
+        serverId: "io.example/server-3",
+        name: "Server 3",
+        description: "Approved by acme via trust delegation",
+        mcpRegistryVerified: true,
+        approvals: [
+          {
+            organizationId: "acme",
+            date: "2026-05-03",
+            configHash: "ddd",
+            installConfigs: [{ tool: "tool-a" }],
+            viaTrust: "other",
+          },
+        ],
+      },
+    ];
+  }
+
+  it("only includes entries approved by the target org", () => {
+    const view = buildOrgEntryView("acme", servers());
+    assert.deepEqual(
+      view.map((s) => s.serverId),
+      ["io.example/server-1", "io.example/server-3"],
+    );
+  });
+
+  it("includes trust-derived approvals, since organizationId is the trusting org", () => {
+    const view = buildOrgEntryView("acme", servers());
+    const viaTrust = view.find((s) => s.serverId === "io.example/server-3")!;
+    assert.equal(viaTrust.approvals[0].viaTrust, "other");
+  });
+
+  it("excludes entries with no approval from the target org", () => {
+    const view = buildOrgEntryView("acme", servers());
+    assert.equal(
+      view.some((s) => s.serverId === "io.example/server-2"),
+      false,
+    );
+  });
+
+  it("keeps all approvals intact, including other orgs' install configs", () => {
+    const view = buildOrgEntryView("acme", servers());
+    const entry = view.find((s) => s.serverId === "io.example/server-1")!;
+    assert.equal(entry.approvals.length, 2);
+    const otherApproval = entry.approvals.find(
+      (a) => a.organizationId === "other",
+    )!;
+    assert.equal(otherApproval.installConfigs.length, 1);
+    assert.equal(otherApproval.installConfigs[0].tool, "tool-b");
+  });
+
+  it("does not mutate the original input", () => {
+    const original = servers();
+    buildOrgEntryView("acme", original);
+
+    assert.equal(original.length, 3);
+    assert.equal(original[0].approvals.length, 2);
+  });
+
+  it("works across entry types other than mcp", () => {
+    const skills: SkillEntry[] = [
+      {
+        skillId: "io.example/skill-1",
+        name: "Skill 1",
+        description: "Approved by acme",
+        source: { url: "https://github.com/example/skills.git" },
+        contentHash: "abc123",
+        approvals: [
+          {
+            organizationId: "acme",
+            date: "2026-05-01",
+            configHash: "aaa",
+            installConfigs: [],
+          },
+        ],
+      },
+      {
+        skillId: "io.example/skill-2",
+        name: "Skill 2",
+        description: "Approved by other only",
+        source: { url: "https://github.com/example/skills.git" },
+        contentHash: "def456",
+        approvals: [
+          {
+            organizationId: "other",
+            date: "2026-05-01",
+            configHash: "bbb",
+            installConfigs: [],
+          },
+        ],
+      },
+    ];
+
+    const view = buildOrgEntryView("acme", skills);
+    assert.deepEqual(
+      view.map((s) => s.skillId),
+      ["io.example/skill-1"],
+    );
+  });
+});
+
 describe("addOrganization — mcp trust extraction", () => {
   it("collects an mcp trust entry", () => {
     const output = emptyOutput();

diff --git a/src/consolidate.ts b/src/consolidate.ts
--- a/src/consolidate.ts
+++ b/src/consolidate.ts
@@ -547,6 +547,24 @@ export function buildToolView(toolId: string, servers: McpEntry[]): McpEntry[] {
   return buildToolEntryView(toolId, servers);
 }
 
+interface HasOrganizationId {
+  organizationId: string;
+}
+
+// Unlike buildToolEntryView, install configs are never stripped: the org
+// whitelist view is meant to show everything an org approved, including
+// other orgs' approvals of the same artifact (e.g. "also approved by"), so
+// filtering to the matching org's approvals alone would throw that context
+// away for no benefit — nothing in installConfigs is org-specific.
+export function buildOrgEntryView<
+  A extends HasInstallConfigs & HasOrganizationId,
+  E extends HasApprovals<A>,
+>(orgId: string, entries: E[]): E[] {
+  return entries.filter((entry) =>
+    entry.approvals.some((a) => a.organizationId === orgId),
+  );
+}
+
 export function addSkillApproval(
   approvalData: SkillApprovalData,
   organizationId: string,
@@ -999,6 +1017,22 @@ function writeOutput(output: ConsolidatedOutput): void {
   });
   console.log(`Written: ${orgsPath}`);
 
+  const mcpPath = resolve(outputDir, "mcp.json");
+  writeJson(mcpPath, { mcp: output.mcp });
+  console.log(`Written: ${mcpPath}`);
+
+  const skillsPath = resolve(outputDir, "skills.json");
+  writeJson(skillsPath, { skills: output.skills });
+  console.log(`Written: ${skillsPath}`);
+
+  const pluginsPath = resolve(outputDir, "plugins.json");
+  writeJson(pluginsPath, { plugins: output.plugins });
+  console.log(`Written: ${pluginsPath}`);
+
+  const agentsPath = resolve(outputDir, "agents.json");
+  writeJson(agentsPath, { agents: output.agents });
+  console.log(`Written: ${agentsPath}`);
+
   const toolsDir = resolve(outputDir, "tools");
   mkdirSync(toolsDir, { recursive: true });
 
@@ -1013,6 +1047,20 @@ function writeOutput(output: ConsolidatedOutput): void {
     console.log(`Written: ${toolPath}`);
   }
 
+  const orgsDir = resolve(outputDir, "orgs");
+  mkdirSync(orgsDir, { recursive: true });
+
+  for (const org of output.organizations) {
+    const orgPath = resolve(orgsDir, `${org.id}.json`);
+    writeJson(orgPath, {
+      mcp: buildOrgEntryView(org.id, output.mcp),
+      skills: buildOrgEntryView(org.id, output.skills),
+      plugins: buildOrgEntryView(org.id, output.plugins),
+      agents: buildOrgEntryView(org.id, output.agents),
+    });
+    console.log(`Written: ${orgPath}`);
+  }
+
   console.log(`\n  Organizations: ${output.organizations.length}`);
   console.log(`  Tools: ${output.tools.length}`);
   console.log(`  MCP servers: ${output.mcp.length}`);

diff --git a/website/src/components/OrgList.tsx b/website/src/components/OrgList.tsx
--- a/website/src/components/OrgList.tsx
+++ b/website/src/components/OrgList.tsx
@@ -1,4 +1,5 @@
 import { Link } from "react-router-dom";
+import { ChevronRight } from "lucide-react";
 import type {
   Organization,
   McpServer,
@@ -117,6 +118,13 @@ export function OrgList({
                 {approvalCount} approval{approvalCount !== 1 ? "s" : ""}
               </span>
             </div>
+            <Link
+              to={`/orgs/${org.id}`}
+              className="inline-flex items-center text-sm font-medium text-primary mt-4 no-underline"
+            >
+              View approved artifacts
+              <ChevronRight className="h-4 w-4 ml-1" />
+            </Link>
           </div>
         );
       })}

diff --git a/website/src/components/docs/docsNav.ts b/website/src/components/docs/docsNav.ts
--- a/website/src/components/docs/docsNav.ts
+++ b/website/src/components/docs/docsNav.ts
@@ -35,6 +35,7 @@ export const DOCS_NAV: DocsPageEntry[] = [
       { id: "mcp-servers", label: "MCP servers" },
       { id: "agent-skills", label: "Agent Skills" },
       { id: "agent-plugins", label: "Agent Plugins" },
+      { id: "a2a-agents", label: "A2A Agents" },
       { id: "disappearing-entries", label: "Disappearing entries" },
       { id: "staying-current", label: "Staying current" },
       { id: "detecting-tampering", label: "Detecting tampering" },

diff --git a/website/src/hooks/useRegistryData.ts b/website/src/hooks/useRegistryData.ts
--- a/website/src/hook...
```

Allowed model input — docs before excerpt:

```markdown
<!-- skills/implement-registry-client/SKILL.md @ 186acfb3f405ce3b4dd8ec399989b6cdc5ea668d -->
---
name: implement-registry-client
description: >
  Implement an AI Registry client in an agent, IDE, or development tool.
  Use when adding registry support for MCP servers, Agent Skills, or Agent Plugins,
  or when a tool needs to browse, install, update, or verify registry-approved artifacts.
---

# Implement an AI Registry client

A client reads the registry, shows users which artifacts their organizations endorsed, and installs them.

Implement any subset of the three artifact types.

## What the registry vouches for

The registry records that a named organization **endorsed** an artifact on a date. That is the whole claim.

It does not test, audit, sandbox, or certify anything. Endorsement is per organization, not a registry-wide certification. A client can present its per-tool list as its own and never name another organization, or it can show the endorsement chain behind each artifact. Both are valid; the second gives the user something to evaluate.

Three limits shape everything below:

- MCP servers are described by configuration, not by content. The registry publishes the command or URL to run. Nothing in the feed covers the server's code, and that code can change under a stable command at any time.
- Skills and plugins carry a content hash of their source as of the last consolidation run, which happens daily and on vendor push. Sources are referenced by repository URL and path with no commit pin, so the hash is the only pin available.
- Withdrawing an endorsement removes the entry from the feed, but so does a source that was briefly unreachable when consolidation ran. Nothing in the data separates the two, so there is no revocation signal a client can act on. See [Disappearing entries](#disappearing-entries).

## The data

Base URL: `https://ai.open-vsx.org/api/v1/`

| Endpoint               | What it gives you                                                            |
| :--------------------- | :--------------------------------------------------------------------------- |
| `tools/<tool-id>.json` | Artifacts endorsed for your tool, with other tools' install configs stripped |
| `organizations.json`   | Organization identity: name, description, website, colour                    |
| `all.json`             | Everything, unfiltered                                                       |

`tools/<tool-id>.json` is all you need to browse and install. Add `organizations.json` if you want to name the endorsing organizations, since the per-tool view carries `organizationId` strings and nothing else about them.

Use `all.json` when your tool has no registered tool id yet. It carries every artifact any organization endorsed, including install configs aimed at other tools, so treat it as a browsing view rather than an install source.

### Base URL and tool id are product configuration

Both decide who the user trusts. Bind them in product code and keep them out of user-facing settings. A user who can point the tool at another registry can change their trust anchor without seeing that as the decision it is.

### Refreshing

Fetch on startup, cache in memory, and refetch when the user asks or before an update check. A fetch that fails leaves the previous state intact: **failure to reach the registry is not evidence that anything changed.** Keep an empty response and a failed request distinct, because they mean opposite things.

## Core

Every artifact type follows the same five steps.

### 1. Read the entries you handle

Top-level keys are `organizations`, `tools`, `mcp`, `skills`, and `plugins`. New keys may appear, so ignore what you do not implement.

### 2. Resolve endorsements

Each entry carries an `approvals` array, one element per endorsing organization:

```json
{
  "serverId": "io.github.ChromeDevTools/chrome-devtools-mcp",
  "name": "Chrome DevTools",
  "description": "Debug and inspect pages in Chrome.",
  "mcpRegistryVerified": true,
  "approvals": [
    {
      "organizationId": "example-org",
      "date": "2026-05-12",
      "configHash": "a3f19c284b7e",
      "installConfigs": [
        {
          "tool": "example-tool",
          "config": {
            "servers": {
              "chrome-devtools": {
                "command": "npx",
                "args": ["-y", "chrome-devtools-mcp@latest"]
              }
            }
          }
        }
      ]
    }
  ]
}
```

Keep every `organizationId`. Pick one `installConfig` to install from by sorting on `date` descending, with `organizationId` ascending as the tie-break, so two clients given the same feed reach the same result.

`viaTrust` on an approval means the organization endorsed it by trusting another organization rather than by filing its own approval. Attribute it to the organization named in `organizationId`, and mention the delegation if you show approval detail.

### 3. Decide how much of the endorsement chain to show

Presence in...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/skills/implement-registry-client/SKILL.md b/skills/implement-registry-client/SKILL.md
--- a/skills/implement-registry-client/SKILL.md
+++ b/skills/implement-registry-client/SKILL.md
@@ -2,40 +2,47 @@
 name: implement-registry-client
 description: >
   Implement an AI Registry client in an agent, IDE, or development tool.
-  Use when adding registry support for MCP servers, Agent Skills, or Agent Plugins,
+  Use when adding registry support for MCP servers, Agent Skills, Agent Plugins, or A2A agents,
   or when a tool needs to browse, install, update, or verify registry-approved artifacts.
 ---
 
 # Implement an AI Registry client
 
 A client reads the registry, shows users which artifacts their organizations endorsed, and installs them.
 
-Implement any subset of the three artifact types.
+Implement any subset of the four artifact types.
 
 ## What the registry vouches for
 
 The registry records that a named organization **endorsed** an artifact on a date. That is the whole claim.
 
 It does not test, audit, sandbox, or certify anything. Endorsement is per organization, not a registry-wide certification. A client can present its per-tool list as its own and never name another organization, or it can show the endorsement chain behind each artifact. Both are valid; the second gives the user something to evaluate.
 
-Three limits shape everything below:
+Four limits shape everything below:
 
 - MCP servers are described by configuration, not by content. The registry publishes the command or URL to run. Nothing in the feed covers the server's code, and that code can change under a stable command at any time.
 - Skills and plugins carry a content hash of their source as of the last consolidation run, which happens daily and on vendor push. Sources are referenced by repository URL and path with no commit pin, so the hash is the only pin available.
+- Agents carry a content hash too, but of a single fetched Agent Card JSON file, not a directory — there is no path to pin.
 - Withdrawing an endorsement removes the entry from the feed, but so does a source that was briefly unreachable when consolidation ran. Nothing in the data separates the two, so there is no revocation signal a client can act on. See [Disappearing entries](#disappearing-entries).
 
 ## The data
 
 Base URL: `https://ai.open-vsx.org/api/v1/`
 
-| Endpoint               | What it gives you                                                            |
-| :--------------------- | :--------------------------------------------------------------------------- |
-| `tools/<tool-id>.json` | Artifacts endorsed for your tool, with other tools' install configs stripped |
-| `organizations.json`   | Organization identity: name, description, website, colour                    |
-| `all.json`             | Everything, unfiltered                                                       |
+| Endpoint                                                 | What it gives you                                                                                                                     |
+| :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
+| `tools/<tool-id>.json`                                   | Artifacts endorsed for your tool, with other tools' install configs stripped                                                          |
+| `orgs/<org-id>.json`                                     | Artifacts endorsed by one organization, across every tool, full install configs kept                                                  |
+| `organizations.json`                                     | Organization identity: name, description, website, colour                                                                             |
+| `mcp.json`, `skills.json`, `plugins.json`, `agents.json` | Every endorsed artifact of one type, across every tool, full install configs kept — each a single-key object, e.g. `{ "mcp": [...] }` |
+| `all.json`                                               | Everything, unfiltered                                                                                                                |
 
 `tools/<tool-id>.json` is all you need to browse and install. Add `organizations.json` if you want to name the endorsing organizations, since the per-tool view carries `organizationId` strings and nothing else about them.
 
+Reach for `orgs/<org-id>.json` or the per-type files when your client's boundary is an organization or an artifact type rather than a tool — for example, an organization publishing its own curated allowlist, or a client that only ever handles one artifact type.
+
+Both keep every entry's `approvals` and `installConfigs` exactly as filed, unlike `tools/<tool-id>.json`. Filter `approvals` by `organizationId` and `installConfigs[].tool` yourself before installing, or treat these as browsing views like `all.json`.
+
 Use `all.json` when your tool has no registered tool id yet. It carries every artifact any organization endorsed, including install configs aimed at other tools, so treat it as a browsing view rather than an install source.
 
 ### Base URL and tool id are product configuration
@@ -52,7 +59,7 @@ Every artifact type follows the same five steps.
 
 ### 1. Read the entries you handle
 
-Top-level keys are `organizations`, `tools`, `mcp`, `skills`, and `plugins`. New keys may appear, so ignore what you do not implement.
+Top-level keys are `organizations`, `tools`, `mcp`, `skills`, `plugins`, and `agents`. New keys may appear, so ignore what you do not implement.
 
 ### 2. Resolve endorsements
 
@@ -211,6 +218,35 @@ Two facts about the feed belong on this side of the line:
 
 Endorsement attaches to the plugin as a whole. No contained MCP server is endorsed independently, and since a plugin's MCP servers can run arbitrary local commands, say so before installing.
 
+## Agents
+
+An A2A agent's `source.url` points directly at its Agent Card, a single JSON file describing a remote agent — not a repository or a directory, and there is no `source.path`. `name` and `description` come from the card itself.
+
+```json
+{
+  "agentId": "eu.mosaico-project/ip-solution-agent",
+  "name": "IP Solution Agent",
+  "description": "Answers questions about IP licensing.",
+  "source": {
+    "url": "https://example.com/agents/ip-solution/agent_card.json"
+  },
+  "contentHash": "4d881ac8a3bd",
+  "approvals": [
+    {
+      "organizationId": "example-org",
+      "date": "2026-08-01",
+      "installConfigs": []
+    }
+  ]
+}
+```
+
+**`contentHash` covers the card's JSON text as fetched, not a directory.** Recompute it as a SHA-256 of the raw response body and take the first 12 hex characters — the same digest format [content hash](references/content-hash.md) documents for skills and plugins, but over one file instead of a walked tree.
+
+There is no plugin-root or skill-folder equivalent to download. Install means resolving the card from `source.url`, using it to reach the remote agent per the [A2A protocol](https://a2a-protocol.org), and registering that reference in your tool. `installConfigs[].config` carries whatever else your tool needs to do that — for a container-delivered agent, for example, an image, tag, port, or environment.
+
+Endorsement attaches to the agent as a whole, the same as for plugins: there is nothing smaller inside an Agent Card to endorse independently.
+
 ## Disappearing entries
 
 An installed artifact vanishing from the feed can mean an organization withdrew its endorsement. It can also mean consolidation skipped the entry because its source was briefly unreachable, or a vendor retargeted the approval, or an id was renamed. The data does not distinguish them.
@@ -235,7 +271,7 @@ Removing artifacts automatically deletes working installations whenever a source
 - [ ] Keep a failed fetch distinct from an empty response, and change nothing on failure
 - [ ] Ignore fields you do not recognise rather than rejecting the document
 - [ ] Pick an install config by `date` descending and `organizationId` ascending
-- [ ] Verify `contentHash` before installing a skill or plugin, and let the user override an explicit mismatch warning
+- [ ] Verify `contentHash` before installing a skill, plugin, or agent, and let the user override an explicit mismatch warning
 - [ ] Record provenance for everything you install, and never overwrite what you did not
 - [ ] Offer adoption when a local slot is already occupied
 - [ ] Install plugins whole, keyed by `pluginId`, and load from inside the plugin root
@@ -249,7 +285,7 @@ Removing artifacts automatically deletes working installations whenever a source
 
 **If you implement updates**
 
-- [ ] Use `configHash` for MCP servers and `contentHash` for skills and plugins
+- [ ] Use `configHash` for MCP servers and `contentHash` for skills, plugins, and agents
 - [ ]...
```

Audit context only — docs after excerpt:

```markdown
<!-- skills/implement-registry-client/SKILL.md @ 8f82f5d6cdbf181fdddfe0fef7e7ea68fcb92a67 -->
---
name: implement-registry-client
description: >
  Implement an AI Registry client in an agent, IDE, or development tool.
  Use when adding registry support for MCP servers, Agent Skills, Agent Plugins, or A2A agents,
  or when a tool needs to browse, install, update, or verify registry-approved artifacts.
---

# Implement an AI Registry client

A client reads the registry, shows users which artifacts their organizations endorsed, and installs them.

Implement any subset of the four artifact types.

## What the registry vouches for

The registry records that a named organization **endorsed** an artifact on a date. That is the whole claim.

It does not test, audit, sandbox, or certify anything. Endorsement is per organization, not a registry-wide certification. A client can present its per-tool list as its own and never name another organization, or it can show the endorsement chain behind each artifact. Both are valid; the second gives the user something to evaluate.

Four limits shape everything below:

- MCP servers are described by configuration, not by content. The registry publishes the command or URL to run. Nothing in the feed covers the server's code, and that code can change under a stable command at any time.
- Skills and plugins carry a content hash of their source as of the last consolidation run, which happens daily and on vendor push. Sources are referenced by repository URL and path with no commit pin, so the hash is the only pin available.
- Agents carry a content hash too, but of a single fetched Agent Card JSON file, not a directory — there is no path to pin.
- Withdrawing an endorsement removes the entry from the feed, but so does a source that was briefly unreachable when consolidation ran. Nothing in the data separates the two, so there is no revocation signal a client can act on. See [Disappearing entries](#disappearing-entries).

## The data

Base URL: `https://ai.open-vsx.org/api/v1/`

| Endpoint                                                 | What it gives you                                                                                                                     |
| :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| `tools/<tool-id>.json`                                   | Artifacts endorsed for your tool, with other tools' install configs stripped                                                          |
| `orgs/<org-id>.json`                                     | Artifacts endorsed by one organization, across every tool, full install configs kept                                                  |
| `organizations.json`                                     | Organization identity: name, description, website, colour                                                                             |
| `mcp.json`, `skills.json`, `plugins.json`, `agents.json` | Every endorsed artifact of one type, across every tool, full install configs kept — each a single-key object, e.g. `{ "mcp": [...] }` |
| `all.json`                                               | Everything, unfiltered                                                                                                                |

`tools/<tool-id>.json` is all you need to browse and install. Add `organizations.json` if you want to name the endorsing organizations, since the per-tool view carries `organizationId` strings and nothing else about them.

Reach for `orgs/<org-id>.json` or the per-type files when your client's boundary is an organization or an artifact type rather than a tool — for example, an organization publishing its own curated allowlist, or a client that only ever handles one artifact type.

Both keep every entry's `approvals` and `installConfigs` exactly as filed, unlike `tools/<tool-id>.json`. Filter `approvals` by `organizationId` and `installConfigs[].tool` yourself before installing, or treat these as browsing views like `all.json`.

Use `all.json` when your tool has no registered tool id yet. It carries every artifact any organization endorsed, including install configs aimed at other tools, so treat it as a browsing view rather than an install source.

### Base URL and tool id are product configuration

Both decide who the user trusts. Bind them in product code and keep them out of user-facing settings. A user who can point the tool at another registry can change their trust anchor without seeing that as the decision it is.

### Refreshing

Fetch on startup, cache in memory, and refetch when the user asks or before an update check. A fetch that fails leaves the previous state intact: **failure to reach the registry is not evidence that anything changed.** Keep an empty response and a failed request distinct, because they mean opposite things.

## Core

Eve...
```

### `GH-CAND-0019`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/85
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `85`
- PR title: Add client integration guidance and CLI install commands
- Language: `typescript`
- Code changed files: `['website/src/cliSource.ts', 'website/src/components/ApiPreviewNotice.tsx', 'website/src/components/Header.tsx', 'website/src/components/InstallFromCli.tsx', 'website/src/components/PluginDetail.tsx', 'website/src/components/SkillDetail.tsx', 'website/src/components/docs/Code.tsx', 'website/src/components/docs/DocsLayout.tsx', 'website/src/components/docs/DocsSection.tsx', 'website/src/components/docs/docsNav.ts', 'website/src/main.tsx', 'website/src/pages/AboutPage.tsx', 'website/src/pages/ApiDocsPage.tsx', 'website/src/pages/docs/ApiPage.tsx', 'website/src/pages/docs/ClientsPage.tsx']`
- Docs changed files: `['AGENTS.md', 'README.md', 'skills/implement-registry-client/SKILL.md', 'skills/implement-registry-client/references/client-owned.md', 'skills/implement-registry-client/references/content-hash.md', 'skills/implement-registry-client/references/deep-links.md', 'skills/implement-registry-client/references/detecting-tampering.md', 'skills/implement-registry-client/references/staying-current.md']`

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
diff --git a/website/src/cliSource.ts b/website/src/cliSource.ts
--- a/website/src/cliSource.ts
+++ b/website/src/cliSource.ts
@@ -0,0 +1,9 @@
+/**
+ * Turns a `source.url` into the argument the skills and plugins CLIs take. The
+ * GitHub prefix is stripped so the common case reads as the documented
+ * `owner/repo` shorthand; any other host falls through unchanged, which both
+ * CLIs also accept as a full URL.
+ */
+export function cliSource(url: string): string {
+  return url.replace(/^https:\/\/github\.com\//, "").replace(/\.git$/, "");
+}

diff --git a/website/src/components/ApiPreviewNotice.tsx b/website/src/components/ApiPreviewNotice.tsx
--- a/website/src/components/ApiPreviewNotice.tsx
+++ b/website/src/components/ApiPreviewNotice.tsx
@@ -3,8 +3,8 @@ import { InfoCallout } from "./InfoCallout";
 
 /**
  * Shared "API preview" copy shown on both the About and API-docs pages.
- * `linkToApiDocs` adds a pointer to /api-docs — omit it on the API-docs page
- * itself to avoid a self-referential link.
+ * `linkToApiDocs` adds a pointer to /docs/api — omit it on the docs pages
+ * themselves to avoid a self-referential link.
  */
 export function ApiPreviewNotice({
   linkToApiDocs = false,
@@ -19,7 +19,7 @@ export function ApiPreviewNotice({
         <>
           {" "}
           See the{" "}
-          <Link to="/api-docs" className="text-primary hover:underline">
+          <Link to="/docs/api" className="text-primary hover:underline">
             API documentation
           </Link>{" "}
           for current details.

diff --git a/website/src/components/Header.tsx b/website/src/components/Header.tsx
--- a/website/src/components/Header.tsx
+++ b/website/src/components/Header.tsx
@@ -35,10 +35,10 @@ export function Header() {
             About
           </Link>
           <Link
-            to="/api-docs"
+            to="/docs"
             className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
           >
-            API
+            Documentation
           </Link>
           <a
             href="https://github.com/eclipsefdn-ai-registry/ai-registry-core"

diff --git a/website/src/components/InstallFromCli.tsx b/website/src/components/InstallFromCli.tsx
--- a/website/src/components/InstallFromCli.tsx
+++ b/website/src/components/InstallFromCli.tsx
@@ -0,0 +1,41 @@
+import { useState } from "react";
+
+/**
+ * Copyable install command at the foot of a skill or plugin detail view.
+ *
+ * Deliberately quieter than the sections above it: a muted label rather than a
+ * heading, because the approvals are what the registry asserts and this is a
+ * convenience derived from metadata it happens to hold. The header row and copy
+ * affordance mirror `CollapsibleJson` so both copy boxes on the site behave the
+ * same.
+ */
+export function InstallFromCli({ command }: { command: string }) {
+  const [copied, setCopied] = useState(false);
+
+  const handleCopy = (e: React.MouseEvent) => {
+    e.stopPropagation();
+    navigator.clipboard.writeText(command).then(() => {
+      setCopied(true);
+      setTimeout(() => setCopied(false), 2000);
+    });
+  };
+
+  return (
+    <div className="mt-6">
+      <div className="flex items-center justify-between gap-2">
+        <span className="text-sm font-medium text-muted-foreground">
+          Install from CLI
+        </span>
+        <button
+          className="text-xs px-2 py-0.5 border border-border rounded hover:border-primary hover:text-primary transition-colors text-muted-foreground"
+          onClick={handleCopy}
+        >
+          {copied ? "Copied!" : "Copy"}
+        </button>
+      </div>
+      <pre className="mt-2 bg-background border border-border p-3 rounded-md overflow-x-auto text-xs leading-relaxed">
+        {command}
+      </pre>
+    </div>
+  );
+}

diff --git a/website/src/components/PluginDetail.tsx b/website/src/components/PluginDetail.tsx
--- a/website/src/components/PluginDetail.tsx
+++ b/website/src/components/PluginDetail.tsx
@@ -8,6 +8,8 @@ import type {
 } from "../types";
 import { sanitizeUrl } from "../sanitize";
 import { ApprovalCard } from "./ServerDetail";
+import { cliSource } from "../cliSource";
+import { InstallFromCli } from "./InstallFromCli";
 
 export function PluginDetail({
   plugin,
@@ -23,6 +25,9 @@ export function PluginDetail({
   const sourceUrl = plugin.source.path
     ? `${plugin.source.url.replace(/\.git$/, "")}/tree/main/${plugin.source.path}`
     : plugin.source.url.replace(/\.git$/, "");
+  // The plugins CLI takes a source and nothing else, so a plugin stored in a
+  // subdirectory resolves by discovery rather than by path.
+  const installCommand = `npx plugins add ${cliSource(plugin.source.url)}`;
 
   return (
     <div className="bg-card border border-primary/50 rounded-xl p-6 shadow-md">
@@ -108,6 +113,8 @@ export function PluginDetail({
           />
         ))}
       </div>
+
+      <InstallFromCli command={installCommand} />
     </div>
   );
 }

diff --git a/website/src/components/SkillDetail.tsx b/website/src/components/SkillDetail.tsx
--- a/website/src/components/SkillDetail.tsx
+++ b/website/src/components/SkillDetail.tsx
@@ -2,6 +2,8 @@ import { ArrowLeft } from "lucide-react";
 import type { Skill, Organization, Tool, SkillApproval } from "../types";
 import { sanitizeUrl } from "../sanitize";
 import { orgBadge } from "../orgBadge";
+import { cliSource } from "../cliSource";
+import { InstallFromCli } from "./InstallFromCli";
 
 export function SkillDetail({
   skill,
@@ -17,6 +19,12 @@ export function SkillDetail({
   const sourceUrl = skill.source.path
     ? `${skill.source.url.replace(/\.git$/, "")}/tree/main/${skill.source.path}`
     : skill.source.url.replace(/\.git$/, "");
+  // A repository holding several skills needs --skill to pick this one; when
+  // the skill is the repository root there is nothing to disambiguate. The
+  // flag matches on the SKILL.md frontmatter name, which is what `name` is.
+  const installCommand = `npx skills add ${cliSource(skill.source.url)}${
+    skill.source.path ? ` --skill ${skill.name}` : ""
+  }`;
 
   return (
     <div className="bg-card border border-primary/50 rounded-xl p-6 shadow-md">
@@ -61,6 +69,8 @@ export function SkillDetail({
           />
         ))}
       </div>
+
+      <InstallFromCli command={installCommand} />
     </div>
   );
 }

diff --git a/website/src/components/docs/Code.tsx b/website/src/components/docs/Code.tsx
--- a/website/src/components/docs/Code.tsx
+++ b/website/src/components/docs/Code.tsx
@@ -0,0 +1,70 @@
+import type { ReactNode } from "react";
+
+export function InlineCode({ children }: { children: ReactNode }) {
+  return (
+    <code className="bg-muted px-1.5 py-0.5 rounded text-xs">{children}</code>
+  );
+}
+
+export function CodeBlock({ children }: { children: ReactNode }) {
+  return (
+    <pre className="bg-[#1e293b] text-[#e2e8f0] p-3 rounded-lg overflow-x-auto text-sm leading-relaxed mb-3">
+      {children}
+    </pre>
+  );
+}
+
+export interface Field {
+  name: string;
+  type: string;
+  description: string;
+}
+
+/**
+ * Field reference for one response object. Every field the registry emits is
+ * listed, including ones a client ignores — an example that omits awkward
+ * fields produces clients that break on the real feed.
+ */
+export function FieldTable({
+  caption,
+  fields,
+}: {
+  caption: string;
+  fields: Field[];
+}) {
+  return (
+    <div className="mb-6">
+      <h3 className="font-semibold text-sm mt-5 mb-2">
+        <InlineCode>{caption}</InlineCode>
+      </h3>
+      <table className="w-full text-sm">
+        <thead>
+          <tr>
+            <th className="text-left py-2 pr-3 border-b-2 border-border font-semibold">
+              Field
+            </th>
+            <th className="text-left py-2 pr-3 border-b-2 border-border font-semibold">
+              Type
+            </th>
+            <th className="text-left py-2 border-b-2 border-border font-semibold">
+              Description
+            </th>
+          </tr>
+        </thead>
+        <tbody>
+          {fields.map((field) => (
+            <tr key={field.name} className="border-b border-border align-top">
+              <td className="py-2 pr-3 whitespace-nowrap">
+                <InlineCode>{field.name}</InlineCode>
+              </td>
+              <td className="py-2 pr-3 whitespace-nowrap text-muted-foreground text-xs">
+                {field.type}
+              </td>
+              <td className="py-2">{field.description}</td>
+            </tr>
+          ))}
+        </tbody>
+      </table>
+    </div>
+  );
+}

diff --git a/website/src/components/docs/DocsLayout.tsx b/website/src/components/docs/DocsLayout.tsx
--- a/website/src/components/docs/DocsLayout.tsx
+++ b/website/src/components/docs/DocsLayout.tsx
@@ -0,0 +1,63 @@
+import { NavLink, Outlet, useLocation } from "react-router-dom";
+import { DOCS_NAV } from "./docsNav";
+
+/**
+ *...
```

Allowed model input — docs before excerpt:

```markdown
<!-- AGENTS.md @ 0d105d32beb45a755e2cc3afd4028d12201fccf5 -->
# AI Registry — Agent Guide

Vendor-neutral, federated trust registry for MCP servers, Agent Skills, Agent Plugins, and A2A agents, hosted at the Eclipse Foundation. This is the core repo — it contains schemas, validation, consolidation, and the website. Approval files live in separate organization-specific vendor repos (e.g., `ai-registry-theia`).

## Architecture

Four artifact types, same approval model:

- **MCP servers** — referenced by `serverId` in the Anthropic MCP registry. Metadata (name, description, version) enriched during consolidation.
- **Agent Skills** — referenced by `skillId` pointing to a git repo + path. `source.path` can be a single string, an array of paths, or a glob pattern (`"skills/*"`) for batch approvals — consolidation expands these into individual entries. Metadata (name, description) extracted from SKILL.md frontmatter; content hash computed via sparse checkout during consolidation.
- **Agent Plugins** ([agent-plugins.org](https://agent-plugins.org)) — referenced by `pluginId` pointing to a git repo + path (single directory, no glob/array). Consolidation fetches the whole plugin directory via sparse checkout to read `plugin.json` (name, description, version, author, homepage, keywords) and enumerate contents: skills under `skills/*/SKILL.md` and MCP servers in `mcp.json`, surfaced as read-only `containedSkills`/`containedMcpServers` metadata — not as separate standalone entries.
- **A2A agents** — referenced by `agentId` pointing directly at a fetchable `agent_card.json` URL (no repo, no path — a single JSON file). Metadata (name, description) and a content hash are extracted from the fetched card during consolidation.

Organizations can provide tools (with `installConfigs`) or just approve artifacts without tool-specific configuration. All four use the same approval file format — `installConfigs` is optional.

## Data flow

```
Vendor repos → validate → collect → enrich (MCP registry + skill sources + plugin sources + agent card fetches) → write static JSON → deploy website
```

Unreachable MCP servers get `mcpRegistryVerified: false`. Unreachable skill and plugin sources are skipped with a warning. Unreachable agent card URLs are skipped with a warning.

## Key conventions

- **IDs**: Reverse-domain notation with `/` separator (e.g., `io.github.anthropics/code-review`)
- **Filenames**: ID with `/` replaced by `--` + `.json` (e.g., `io.github.anthropics--code-review.json`)
- **Directories**: `mcp/` for server approvals, `skills/` for skill approvals, `plugins/` for plugin approvals, `agents/` for agent approvals
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
  agent-source.ts           Agent enrichment (HTTP fetch, parse, hash)
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

**MANDATORY: run `npm run format` before every commit.** Do not skip this, even for small or "obviously fine" changes — unformatted code must never be committed. After formatting, run `npm run check` (typecheck, lint, format verification, and tests) and confirm it passes before committing.

## When editing

- Schemas are the contract — change schemas first, then update validation and consolidation to match.
- `installConfigs` and `tools` are optional. Handle missing values with `?? []`.
- Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification), Phase 4 (plugin manifest verification), Phase 5 (agent card verification). Phases 2-5 warn on...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/AGENTS.md b/AGENTS.md
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -73,3 +73,5 @@ Tests use Node.js built-in `node:test` with `assert/strict`. Pure function tests
 - Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification), Phase 4 (plugin manifest verification), Phase 5 (agent card verification). Phases 2-5 warn on failure, don't block.
 - Consolidation is split: collect (no network) → enrich MCP (network, fatal on error) → enrich skills (network, skip on error) → enrich plugins (network, skip on error) → enrich agents (network, skip on error) → write.
 - Website types in `website/src/types.ts` mirror but don't import from `src/consolidate.ts` — keep them in sync manually.
+- Guidance for implementing clients exists twice on purpose: `skills/implement-registry-client/` for agents, `/docs/clients` (`website/src/pages/docs/ClientsPage.tsx`) for people. Each is complete and neither links to the other, so a rule that changes needs both edited. Drift here is accepted, not a bug to fix by merging them.
+- Docs pages live under `/docs` with a sidebar driven by `website/src/components/docs/docsNav.ts`. Section titles come from that file via `DocsSection`, so a section is added by adding it there and rendering `<DocsSection id="...">` on the page.

diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -38,6 +38,7 @@ Vendor Repos                    Central Repo                    Consumers
 - Metadata enrichment from agent card URLs (name, description, content hash)
 - A static website deployed to GitHub Pages for browsing the registry
 - Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md), [skill](skills/create-skill-approval/SKILL.md), [plugin](skills/create-plugin-approval/SKILL.md), and [agent](skills/create-agent-approval/SKILL.md) approval files
+- Guidance for implementing clients — as a [website page](https://ai.open-vsx.org/docs/clients) and as a [Claude Code skill](skills/implement-registry-client/SKILL.md)
 
 ## Repositories
 
@@ -284,7 +285,7 @@ https://ai.open-vsx.org/api/v1/
 
 Schemas are also available at `/schemas/` (e.g., [`mcp-approval.schema.json`](https://ai.open-vsx.org/schemas/mcp-approval.schema.json), [`skill-approval.schema.json`](https://ai.open-vsx.org/schemas/skill-approval.schema.json), [`plugin-approval.schema.json`](https://ai.open-vsx.org/schemas/plugin-approval.schema.json), [`agent-approval.schema.json`](https://ai.open-vsx.org/schemas/agent-approval.schema.json)).
 
-A tool integration typically fetches `organizations.json` + its own `tools/<tool-id>.json`.
+A tool integration typically fetches `organizations.json` + its own `tools/<tool-id>.json`. See the [client implementation guidance](skills/implement-registry-client/SKILL.md) for what to do with them: resolving approvals, showing who approved an artifact, verifying content, installing, and keeping it current.
 
 ## Reliability
 
@@ -307,6 +308,7 @@ If collection or MCP enrichment fails, the build stops and the previous deployme
 - [Skill approval skill](skills/create-skill-approval/SKILL.md) — AI agent skill for generating skill approval files
 - [Plugin approval skill](skills/create-plugin-approval/SKILL.md) — AI agent skill for generating plugin approval files
 - [Agent approval skill](skills/create-agent-approval/SKILL.md) — AI agent skill for generating agent approval files
+- [Client implementation guidance](skills/implement-registry-client/SKILL.md) — AI agent skill for implementing an AI Registry client in a tool
 - [JSON schemas](schemas/) — organization and approval file schemas
 
 ## License

diff --git a/skills/implement-registry-client/SKILL.md b/skills/implement-registry-client/SKILL.md
--- a/skills/implement-registry-client/SKILL.md
+++ b/skills/implement-registry-client/SKILL.md
@@ -0,0 +1,260 @@
+---
+name: implement-registry-client
+description: >
+  Implement an AI Registry client in an agent, IDE, or development tool.
+  Use when adding registry support for MCP servers, Agent Skills, or Agent Plugins,
+  or when a tool needs to browse, install, update, or verify registry-approved artifacts.
+---
+
+# Implement an AI Registry client
+
+A client reads the registry, shows users which artifacts their organizations endorsed, and installs them.
+
+Implement any subset of the three artifact types.
+
+## What the registry vouches for
+
+The registry records that a named organization **endorsed** an artifact on a date. That is the whole claim.
+
+It does not test, audit, sandbox, or certify anything. Endorsement is per organization, not a registry-wide certification. A client can present its per-tool list as its own and never name another organization, or it can show the endorsement chain behind each artifact. Both are valid; the second gives the user something to evaluate.
+
+Three limits shape everything below:
+
+- MCP servers are described by configuration, not by content. The registry publishes the command or URL to run. Nothing in the feed covers the server's code, and that code can change under a stable command at any time.
+- Skills and plugins carry a content hash of their source as of the last consolidation run, which happens daily and on vendor push. Sources are referenced by repository URL and path with no commit pin, so the hash is the only pin available.
+- Withdrawing an endorsement removes the entry from the feed, but so does a source that was briefly unreachable when consolidation ran. Nothing in the data separates the two, so there is no revocation signal a client can act on. See [Disappearing entries](#disappearing-entries).
+
+## The data
+
+Base URL: `https://ai.open-vsx.org/api/v1/`
+
+| Endpoint               | What it gives you                                                            |
+| :--------------------- | :--------------------------------------------------------------------------- |
+| `tools/<tool-id>.json` | Artifacts endorsed for your tool, with other tools' install configs stripped |
+| `organizations.json`   | Organization identity: name, description, website, colour                    |
+| `all.json`             | Everything, unfiltered                                                       |
+
+`tools/<tool-id>.json` is all you need to browse and install. Add `organizations.json` if you want to name the endorsing organizations, since the per-tool view carries `organizationId` strings and nothing else about them.
+
+Use `all.json` when your tool has no registered tool id yet. It carries every artifact any organization endorsed, including install configs aimed at other tools, so treat it as a browsing view rather than an install source.
+
+### Base URL and tool id are product configuration
+
+Both decide who the user trusts. Bind them in product code and keep them out of user-facing settings. A user who can point the tool at another registry can change their trust anchor without seeing that as the decision it is.
+
+### Refreshing
+
+Fetch on startup, cache in memory, and refetch when the user asks or before an update check. A fetch that fails leaves the previous state intact: **failure to reach the registry is not evidence that anything changed.** Keep an empty response and a failed request distinct, because they mean opposite things.
+
+## Core
+
+Every artifact type follows the same five steps.
+
+### 1. Read the entries you handle
+
+Top-level keys are `organizations`, `tools`, `mcp`, `skills`, and `plugins`. New keys may appear, so ignore what you do not implement.
+
+### 2. Resolve endorsements
+
+Each entry carries an `approvals` array, one element per endorsing organization:
+
+```json
+{
+  "serverId": "io.github.ChromeDevTools/chrome-devtools-mcp",
+  "name": "Chrome DevTools",
+  "description": "Debug and inspect pages in Chrome.",
+  "mcpRegistryVerified": true,
+  "approvals": [
+    {
+      "organizationId": "example-org",
+      "date": "2026-05-12",
+      "configHash": "a3f19c284b7e",
+      "installConfigs": [
+        {
+          "tool": "example-tool",
+          "config": {
+            "servers": {
+              "chrome-devtools": {
+                "command": "npx",
+                "args": ["-y", "chrome-devtools-mcp@latest"]
+              }
+            }
+          }
+        }
+      ]
+    }
+  ]
+}
+```
+
+Keep every `organizationId`. Pick one `installConfig` to install from by sorting on `date` descending, with `organizationId` ascending as the tie-break, so two clients given the same feed reach the same result.
+
+`viaTrust` on an approval means the organization endorsed it by trusting another organization rather than by filing its own approval. Attribute it to the organization named in `organizationId`, and mention the delegation if you show approval detail.
+
+### 3. Decide how much of the endorsement chain to show
+
+Presence in your per-tool view already means endorsed for your tool, so a list with no organization names is a legitimate client. If you do show the...
```

Audit context only — docs after excerpt:

```markdown
<!-- AGENTS.md @ fa0083437de9974caf53a9440c55c989f0039821 -->
# AI Registry — Agent Guide

Vendor-neutral, federated trust registry for MCP servers, Agent Skills, Agent Plugins, and A2A agents, hosted at the Eclipse Foundation. This is the core repo — it contains schemas, validation, consolidation, and the website. Approval files live in separate organization-specific vendor repos (e.g., `ai-registry-theia`).

## Architecture

Four artifact types, same approval model:

- **MCP servers** — referenced by `serverId` in the Anthropic MCP registry. Metadata (name, description, version) enriched during consolidation.
- **Agent Skills** — referenced by `skillId` pointing to a git repo + path. `source.path` can be a single string, an array of paths, or a glob pattern (`"skills/*"`) for batch approvals — consolidation expands these into individual entries. Metadata (name, description) extracted from SKILL.md frontmatter; content hash computed via sparse checkout during consolidation.
- **Agent Plugins** ([agent-plugins.org](https://agent-plugins.org)) — referenced by `pluginId` pointing to a git repo + path (single directory, no glob/array). Consolidation fetches the whole plugin directory via sparse checkout to read `plugin.json` (name, description, version, author, homepage, keywords) and enumerate contents: skills under `skills/*/SKILL.md` and MCP servers in `mcp.json`, surfaced as read-only `containedSkills`/`containedMcpServers` metadata — not as separate standalone entries.
- **A2A agents** — referenced by `agentId` pointing directly at a fetchable `agent_card.json` URL (no repo, no path — a single JSON file). Metadata (name, description) and a content hash are extracted from the fetched card during consolidation.

Organizations can provide tools (with `installConfigs`) or just approve artifacts without tool-specific configuration. All four use the same approval file format — `installConfigs` is optional.

## Data flow

```
Vendor repos → validate → collect → enrich (MCP registry + skill sources + plugin sources + agent card fetches) → write static JSON → deploy website
```

Unreachable MCP servers get `mcpRegistryVerified: false`. Unreachable skill and plugin sources are skipped with a warning. Unreachable agent card URLs are skipped with a warning.

## Key conventions

- **IDs**: Reverse-domain notation with `/` separator (e.g., `io.github.anthropics/code-review`)
- **Filenames**: ID with `/` replaced by `--` + `.json` (e.g., `io.github.anthropics--code-review.json`)
- **Directories**: `mcp/` for server approvals, `skills/` for skill approvals, `plugins/` for plugin approvals, `agents/` for agent approvals
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
  agent-source.ts           Agent enrichment (HTTP fetch, parse, hash)
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

**MANDATORY: run `npm run format` before every commit.** Do not skip this, even for small or "obviously fine" changes — unformatted code must never be committed. After formatting, run `npm run check` (typecheck, lint, format verification, and tests) and confirm it passes before committing.

## When editing

- Schemas are the contract — change schemas first, then update validation and consolidation to match.
- `installConfigs` and `tools` are optional. Handle missing values with `?? []`.
- Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification), Phase 4 (plugin manifest verification), Phase 5 (agent card verification). Phases 2-5 warn on...
```

### `GH-CAND-0020`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/78
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `78`
- PR title: Add "agent" (A2A) artifact type
- Language: `typescript`
- Code changed files: `['schemas/agent-approval.schema.json', 'schemas/organization.schema.json', 'src/agent-source.test.ts', 'src/agent-source.ts', 'src/consolidate.test.ts', 'src/consolidate.ts', 'src/validate.test.ts', 'src/validate.ts', 'vendors.json', 'website/src/components/AgentDetail.tsx', 'website/src/components/AgentList.tsx', 'website/src/components/OrgList.tsx', 'website/src/filterArtifacts.ts', 'website/src/hooks/useRegistryData.ts', 'website/src/pages/AboutPage.tsx', 'website/src/pages/ApiDocsPage.tsx', 'website/src/pages/HomePage.tsx', 'website/src/pages/ToolPage.tsx', 'website/src/types.ts']`
- Docs changed files: `['AGENTS.md', 'README.md', 'skills/create-agent-approval/SKILL.md']`

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
diff --git a/schemas/agent-approval.schema.json b/schemas/agent-approval.schema.json
--- a/schemas/agent-approval.schema.json
+++ b/schemas/agent-approval.schema.json
@@ -0,0 +1,62 @@
+{
+  "$schema": "http://json-schema.org/draft-07/schema#",
+  "$id": "https://ai.open-vsx.org/schemas/agent-approval.schema.json",
+  "title": "Agent Approval",
+  "description": "Vendor approval for an A2A agent in the AI Registry",
+  "type": "object",
+  "required": ["agentId", "date", "source"],
+  "additionalProperties": false,
+  "properties": {
+    "agentId": {
+      "type": "string",
+      "minLength": 1,
+      "description": "Agent identifier using reverse-domain notation (e.g., eu.mosaico-project/ip-solution-agent)"
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
+      "description": "Location of the agent's A2A Agent Card JSON file",
+      "properties": {
+        "url": {
+          "type": "string",
+          "format": "uri",
+          "description": "Direct, fetchable URL to the agent_card.json file"
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
+            "description": "Tool-specific configuration object (e.g. Docker image/tag/port/env for container-delivered agents)"
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

diff --git a/schemas/organization.schema.json b/schemas/organization.schema.json
--- a/schemas/organization.schema.json
+++ b/schemas/organization.schema.json
@@ -67,6 +67,11 @@
             "type": "string",
             "description": "URL prefix for auto-generating Agent Plugin install URLs. The artifact pluginId is appended literally.",
             "examples": ["theia://install-plugin?id="]
+          },
+          "agentInstallUrlPrefix": {
+            "type": "string",
+            "description": "URL prefix for auto-generating agent install URLs. The artifact agentId is appended literally.",
+            "examples": ["theia://install-agent?id="]
           }
         }
       }

diff --git a/src/agent-source.test.ts b/src/agent-source.test.ts
--- a/src/agent-source.test.ts
+++ b/src/agent-source.test.ts
@@ -0,0 +1,226 @@
+import { describe, it, mock } from "node:test";
+import assert from "node:assert/strict";
+import { createHash } from "node:crypto";
+import {
+  parseAgentCard,
+  fetchAgentCard,
+  enrichAgentMetadata,
+} from "./agent-source.js";
+import type { AgentEntry } from "./consolidate.js";
+
+// --- parseAgentCard ---
+
+describe("parseAgentCard", () => {
+  it("extracts name and description from valid JSON", () => {
+    const raw = JSON.stringify({
+      name: "IP Solution Agent",
+      description: "Handles IP-related workflows.",
+    });
+    const result = parseAgentCard(raw);
+    assert.equal(result.name, "IP Solution Agent");
+    assert.equal(result.description, "Handles IP-related workflows.");
+  });
+
+  it("defaults name and description to empty strings when absent", () => {
+    const raw = JSON.stringify({ foo: "bar" });
+    const result = parseAgentCard(raw);
+    assert.equal(result.name, "");
+    assert.equal(result.description, "");
+  });
+
+  it("defaults to empty strings when name/description are non-string", () => {
+    const raw = JSON.stringify({ name: 123, description: null });
+    const result = parseAgentCard(raw);
+    assert.equal(result.name, "");
+    assert.equal(result.description, "");
+  });
+
+  it("throws on invalid JSON", () => {
+    assert.throws(() => parseAgentCard("not json"));
+  });
+});
+
+// --- fetchAgentCard ---
+
+describe("fetchAgentCard", () => {
+  it("fetches, hashes, and parses a valid agent card", async () => {
+    const rawText = JSON.stringify({
+      name: "IP Solution Agent",
+      description: "Handles IP-related workflows.",
+    });
+    mock.method(globalThis, "fetch", async () => {
+      return { ok: true, status: 200, text: async () => rawText } as Response;
+    });
+    try {
+      const metadata = await fetchAgentCard("https://example.com/agent.json");
+      assert.equal(metadata.name, "IP Solution Agent");
+      assert.equal(metadata.description, "Handles IP-related workflows.");
+      const expectedHash = createHash("sha256")
+        .update(rawText)
+        .digest("hex")
+        .slice(0, 12);
+      assert.equal(metadata.contentHash, expectedHash);
+    } finally {
+      mock.restoreAll();
+    }
+  });
+
+  it("throws with the URL included on a non-OK response", async () => {
+    mock.method(globalThis, "fetch", async () => {
+      return { ok: false, status: 404, text: async () => "" } as Response;
+    });
+    try {
+      await assert.rejects(
+        () => fetchAgentCard("https://example.com/missing.json"),
+        (err: unknown) => {
+          assert.ok(err instanceof Error);
+          assert.match(err.message, /https:\/\/example\.com\/missing\.json/);
+          assert.match(err.message, /404/);
+          return true;
+        },
+      );
+    } finally {
+      mock.restoreAll();
+    }
+  });
+
+  it("throws a descriptive error when the response body is invalid JSON", async () => {
+    mock.method(globalThis, "fetch", async () => {
+      return {
+        ok: true,
+        status: 200,
+        text: async () => "not json",
+      } as Response;
+    });
+    try {
+      await assert.rejects(
+        () => fetchAgentCard("https://example.com/agent.json"),
+        (err: unknown) => {
+          assert.ok(err instanceof Error);
+          assert.match(err.message, /https:\/\/example\.com\/agent\.json/);
+          return true;
+        },
+      );
+    } finally {
+      mock.restoreAll();
+    }
+  });
+
+  it("throws when fetch itself rejects (network error)", async () => {
+    mock.method(globalThis, "fetch", async () => {
+      throw new Error("network down");
+    });
+    try {
+      await assert.rejects(() =>
+        fetchAgentCard("https://example.com/agent.json"),
+      );
+    } finally {
+      mock.restoreAll();
+    }
+  });
+});
+
+// --- enrichAgentMetadata ---
+
+function makeAgentEntry(agentId: string, url: string): AgentEntry {
+  return {
+    agentId,
+    name: agentId,
+    description: "",
+    source: { url },
+    contentHash: "",
+    approvals: [],
+  };
+}
+
+describe("enrichAgentMetadata", () => {
+  it("returns an empty array unchanged", async () => {
+    const result = await enrichAgentMetadata([]);
+    assert.deepEqual(result, []);
+  });
+
+  it("enriches a single successful entry in place", async () => {
+    const rawText = JSON.stringify({ name: "Agent One", description: "Desc" });
+    mock.method(globalThis, "fetch", async () => {
+      return { ok: true, status: 200, text: async () => rawText } as Response;
+    });
+    try {
+      const entry = makeAgentEntry(
+        "io.example/agent-one",
+        "https://example.com/one.json",
+      );
+      const result = await enrichAgentMetadata([entry]);
+      assert.equal(result.length, 1);
+      assert.equal(result[0], entry);
+      assert.equal(entry.name, "Agent One");
+      assert.equal(entry.description, "Desc");
+      assert.ok(entry.contentHash.length === 12);
+    } finally {
+      mock.restoreAll();
+    }
+  });
+
+  it("falls back to agentId when the card has no name", async () => {
+    const rawText = JSON.stringify({ description: "Desc" });
+    mock.method(globalThis, "fetch", async () => {
+      return { ok: true, status: 200, text: async () => rawText } as Response;
+    });
+    try {
+      const entry = makeAgentEntry(
+        "io.example/agent-noname",
+        "https://example.com/noname.json",
+      );
+      const result = await enrichAgentMetadata([entry]);
+      assert.equal(result[0].name, "io.example/agent-noname");
+    } finally {
+      mock.restoreAll();
+    }
+  });
+
+  it("drops a failing entry with a warning, without throwing", async () => {
+    mock.method(globalThis, "fetch", async () => {
+      return { ok: false, status: 500, text: async () => "" } as Response;
+    });
+    const warnCalls: unknown[][] =...
```

Allowed model input — docs before excerpt:

```markdown
<!-- AGENTS.md @ 04cd812b2a38cec54958c161f88912dfca138c3e -->
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

<!-- README.md @ 04cd812b2a38cec54958c161f88912dfca138c3e -->
# AI Registry

> **Preview** — This registry is currently in preview. Data, APIs, and the website may change as we iterate on the concept.

A vendor-neutral, federated trust registry for AI artifacts, hosted at the Eclipse Foundation. Supports [Model Context Prot...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/AGENTS.md b/AGENTS.md
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -1,30 +1,31 @@
 # AI Registry — Agent Guide
 
-Vendor-neutral, federated trust registry for MCP servers, Agent Skills, and Agent Plugins, hosted at the Eclipse Foundation. This is the core repo — it contains schemas, validation, consolidation, and the website. Approval files live in separate organization-specific vendor repos (e.g., `ai-registry-theia`).
+Vendor-neutral, federated trust registry for MCP servers, Agent Skills, Agent Plugins, and A2A agents, hosted at the Eclipse Foundation. This is the core repo — it contains schemas, validation, consolidation, and the website. Approval files live in separate organization-specific vendor repos (e.g., `ai-registry-theia`).
 
 ## Architecture
 
-Three artifact types, same approval model:
+Four artifact types, same approval model:
 
 - **MCP servers** — referenced by `serverId` in the Anthropic MCP registry. Metadata (name, description, version) enriched during consolidation.
 - **Agent Skills** — referenced by `skillId` pointing to a git repo + path. `source.path` can be a single string, an array of paths, or a glob pattern (`"skills/*"`) for batch approvals — consolidation expands these into individual entries. Metadata (name, description) extracted from SKILL.md frontmatter; content hash computed via sparse checkout during consolidation.
 - **Agent Plugins** ([agent-plugins.org](https://agent-plugins.org)) — referenced by `pluginId` pointing to a git repo + path (single directory, no glob/array). Consolidation fetches the whole plugin directory via sparse checkout to read `plugin.json` (name, description, version, author, homepage, keywords) and enumerate contents: skills under `skills/*/SKILL.md` and MCP servers in `mcp.json`, surfaced as read-only `containedSkills`/`containedMcpServers` metadata — not as separate standalone entries.
+- **A2A agents** — referenced by `agentId` pointing directly at a fetchable `agent_card.json` URL (no repo, no path — a single JSON file). Metadata (name, description) and a content hash are extracted from the fetched card during consolidation.
 
-Organizations can provide tools (with `installConfigs`) or just approve artifacts without tool-specific configuration. All three use the same approval file format — `installConfigs` is optional.
+Organizations can provide tools (with `installConfigs`) or just approve artifacts without tool-specific configuration. All four use the same approval file format — `installConfigs` is optional.
 
 ## Data flow
 
 ```
-Vendor repos → validate → collect → enrich (MCP registry + skill sources + plugin sources) → write static JSON → deploy website
+Vendor repos → validate → collect → enrich (MCP registry + skill sources + plugin sources + agent card fetches) → write static JSON → deploy website
 ```
 
-Unreachable MCP servers get `mcpRegistryVerified: false`. Unreachable skill and plugin sources are skipped with a warning.
+Unreachable MCP servers get `mcpRegistryVerified: false`. Unreachable skill and plugin sources are skipped with a warning. Unreachable agent card URLs are skipped with a warning.
 
 ## Key conventions
 
 - **IDs**: Reverse-domain notation with `/` separator (e.g., `io.github.anthropics/code-review`)
 - **Filenames**: ID with `/` replaced by `--` + `.json` (e.g., `io.github.anthropics--code-review.json`)
-- **Directories**: `mcp/` for server approvals, `skills/` for skill approvals, `plugins/` for plugin approvals
+- **Directories**: `mcp/` for server approvals, `skills/` for skill approvals, `plugins/` for plugin approvals, `agents/` for agent approvals
 - **Schemas**: `schemas/*.schema.json` — source of truth for all approval formats
 - **Pure functions**: Core validation and consolidation logic has no I/O for testability. I/O wrappers are thin layers on top.
 
@@ -37,6 +38,7 @@ src/
   consolidate.ts            Consolidation pipeline (collect, enrich, write)
   skill-source.ts           Skill enrichment (sparse checkout, frontmatter, hashing)
   plugin-source.ts          Plugin enrichment (sparse checkout, manifest + contents)
+  agent-source.ts           Agent enrichment (HTTP fetch, parse, hash)
   anthropic-registry.ts     MCP server metadata lookup
   cli-validate.ts           CLI entry: validate a vendor repo
   cli-consolidate.ts        CLI entry: consolidate all vendors
@@ -62,12 +64,12 @@ Tests use Node.js built-in `node:test` with `assert/strict`. Pure function tests
 
 ## Before committing
 
-Run `npm run format` then `npm run check`. The check includes typecheck, lint, format verification, and tests.
+**MANDATORY: run `npm run format` before every commit.** Do not skip this, even for small or "obviously fine" changes — unformatted code must never be committed. After formatting, run `npm run check` (typecheck, lint, format verification, and tests) and confirm it passes before committing.
 
 ## When editing
 
 - Schemas are the contract — change schemas first, then update validation and consolidation to match.
 - `installConfigs` and `tools` are optional. Handle missing values with `?? []`.
-- Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification), Phase 4 (plugin manifest verification). Phases 2-4 warn on failure, don't block.
-- Consolidation is split: collect (no network) → enrich MCP (network, fatal on error) → enrich skills (network, skip on error) → enrich plugins (network, skip on error) → write.
+- Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification), Phase 4 (plugin manifest verification), Phase 5 (agent card verification). Phases 2-5 warn on failure, don't block.
+- Consolidation is split: collect (no network) → enrich MCP (network, fatal on error) → enrich skills (network, skip on error) → enrich plugins (network, skip on error) → enrich agents (network, skip on error) → write.
 - Website types in `website/src/types.ts` mirror but don't import from `src/consolidate.ts` — keep them in sync manually.

diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -2,11 +2,11 @@
 
 > **Preview** — This registry is currently in preview. Data, APIs, and the website may change as we iterate on the concept.
 
-A vendor-neutral, federated trust registry for AI artifacts, hosted at the Eclipse Foundation. Supports [Model Context Protocol](https://modelcontextprotocol.io) (MCP) servers, [Agent Skills](https://agentskills.io), and [Agent Plugins](https://agent-plugins.org).
+A vendor-neutral, federated trust registry for AI artifacts, hosted at the Eclipse Foundation. Supports [Model Context Protocol](https://modelcontextprotocol.io) (MCP) servers, [Agent Skills](https://agentskills.io), [Agent Plugins](https://agent-plugins.org), and [A2A agents](https://a2a-protocol.org).
 
 ## How It Works
 
-The registry follows a federated model: **vendors** maintain their own repositories with approval files for AI artifacts (MCP servers, Agent Skills, and Agent Plugins) they endorse. A **central repository** consolidates all vendor data into a single JSON file that tools can consume.
+The registry follows a federated model: **vendors** maintain their own repositories with approval files for AI artifacts (MCP servers, Agent Skills, Agent Plugins, and A2A agents) they endorse. A **central repository** consolidates all vendor data into a single JSON file that tools can consume.
 
 ```
 Vendor Repos                    Central Repo                    Consumers
@@ -26,6 +26,7 @@ Vendor Repos                    Central Repo                    Consumers
 - `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
 - `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository
 - `plugins/*.json` — one approval file per approved Agent Plugin, pointing to the plugin's source repository
+- `agents/*.json` — one approval file per approved A2A agent, pointing directly at its Agent Card URL
 
 **The central repo** provides:
 
@@ -34,8 +35,9 @@ Vendor Repos                    Central Repo                    Consumers
 - Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
 - Metadata enrichment from skill source repos (name, description, content hash)
 - Metadata enrichment from plugin source repos (name, description, version, author, contained skills/MCP servers, content hash)
+- Metadata enrichment from agent card URLs (name, description, content hash)
 - A static website deployed to GitHub Pages for browsing the registry
-- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md), [skill](skills/create-skill-approval/SKILL.md), and [plugin](skills/create-plugin-approval/SKILL.md) approval files
+- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md), [skill](skills/create-skill-approval/SKILL.md), [plugin](skills/create-plugin-appro...
```

Audit context only — docs after excerpt:

```markdown
<!-- AGENTS.md @ 0ce98c83746e18f948ef1cd2fc7f9c7eb3ab3ec9 -->
# AI Registry — Agent Guide

Vendor-neutral, federated trust registry for MCP servers, Agent Skills, Agent Plugins, and A2A agents, hosted at the Eclipse Foundation. This is the core repo — it contains schemas, validation, consolidation, and the website. Approval files live in separate organization-specific vendor repos (e.g., `ai-registry-theia`).

## Architecture

Four artifact types, same approval model:

- **MCP servers** — referenced by `serverId` in the Anthropic MCP registry. Metadata (name, description, version) enriched during consolidation.
- **Agent Skills** — referenced by `skillId` pointing to a git repo + path. `source.path` can be a single string, an array of paths, or a glob pattern (`"skills/*"`) for batch approvals — consolidation expands these into individual entries. Metadata (name, description) extracted from SKILL.md frontmatter; content hash computed via sparse checkout during consolidation.
- **Agent Plugins** ([agent-plugins.org](https://agent-plugins.org)) — referenced by `pluginId` pointing to a git repo + path (single directory, no glob/array). Consolidation fetches the whole plugin directory via sparse checkout to read `plugin.json` (name, description, version, author, homepage, keywords) and enumerate contents: skills under `skills/*/SKILL.md` and MCP servers in `mcp.json`, surfaced as read-only `containedSkills`/`containedMcpServers` metadata — not as separate standalone entries.
- **A2A agents** — referenced by `agentId` pointing directly at a fetchable `agent_card.json` URL (no repo, no path — a single JSON file). Metadata (name, description) and a content hash are extracted from the fetched card during consolidation.

Organizations can provide tools (with `installConfigs`) or just approve artifacts without tool-specific configuration. All four use the same approval file format — `installConfigs` is optional.

## Data flow

```
Vendor repos → validate → collect → enrich (MCP registry + skill sources + plugin sources + agent card fetches) → write static JSON → deploy website
```

Unreachable MCP servers get `mcpRegistryVerified: false`. Unreachable skill and plugin sources are skipped with a warning. Unreachable agent card URLs are skipped with a warning.

## Key conventions

- **IDs**: Reverse-domain notation with `/` separator (e.g., `io.github.anthropics/code-review`)
- **Filenames**: ID with `/` replaced by `--` + `.json` (e.g., `io.github.anthropics--code-review.json`)
- **Directories**: `mcp/` for server approvals, `skills/` for skill approvals, `plugins/` for plugin approvals, `agents/` for agent approvals
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
  agent-source.ts           Agent enrichment (HTTP fetch, parse, hash)
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

**MANDATORY: run `npm run format` before every commit.** Do not skip this, even for small or "obviously fine" changes — unformatted code must never be committed. After formatting, run `npm run check` (typecheck, lint, format verification, and tests) and confirm it passes before committing.

## When editing

- Schemas are the contract — change schemas first, then update validation and consolidation to match.
- `installConfigs` and `tools` are optional. Handle missing values with `?? []`.
- Validation is split: Phase 1 (schema), Phase 2 (MCP registry verification), Phase 3 (skill source verification), Phase 4 (plugin manifest verification), Phase 5 (agent card verification). Phases 2-5 warn on...
```

### `GH-CAND-0021`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/69
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `69`
- PR title: Add generic MCP server config with cross-vendor derivation and MCP trust delegation
- Language: `typescript`
- Code changed files: `['eslint.config.js', 'package.json', 'schemas/mcp-approval.schema.json', 'schemas/mcp-server-config.schema.json', 'schemas/organization.schema.json', 'src/consolidate.test.ts', 'src/consolidate.ts', 'src/mcp-config-templates/registry.test.ts', 'src/mcp-config-templates/registry.ts', 'src/mcp-config-templates/theia.test.ts', 'src/mcp-config-templates/theia.ts', 'src/mcp-config-templates/types.ts', 'src/validate.test.ts', 'src/validate.ts', 'website/src/components/ServerDetail.tsx', 'website/src/types.ts']`
- Docs changed files: `[]`

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
diff --git a/eslint.config.js b/eslint.config.js
--- a/eslint.config.js
+++ b/eslint.config.js
@@ -4,10 +4,11 @@ export default tseslint.config(
   ...tseslint.configs.recommended,
   {
     rules: {
-      // Allow unused vars prefixed with _
+      // Allow unused vars prefixed with _, and unused rest-destructuring
+      // siblings (e.g. `const { config: _drop, ...rest } = cfg` to omit a key)
       "@typescript-eslint/no-unused-vars": [
         "warn",
-        { argsIgnorePattern: "^_" },
+        { argsIgnorePattern: "^_", ignoreRestSiblings: true },
       ],
     },
   },

diff --git a/package.json b/package.json
--- a/package.json
+++ b/package.json
@@ -13,7 +13,7 @@
     "website:build": "npm run build --prefix website",
     "ci:build": "npm ci && npm run website:install && npm run consolidate && npm run website:prepare && npm run website:build",
     "lint": "eslint src/",
-    "test": "tsx --test src/**/*.test.ts",
+    "test": "tsx --test 'src/**/*.test.ts'",
     "check": "tsc --noEmit && npm run lint && npm run format:check && npm test",
     "format": "prettier --write .",
     "format:check": "prettier --check ."

diff --git a/schemas/mcp-approval.schema.json b/schemas/mcp-approval.schema.json
--- a/schemas/mcp-approval.schema.json
+++ b/schemas/mcp-approval.schema.json
@@ -1,5 +1,6 @@
 {
   "$schema": "http://json-schema.org/draft-07/schema#",
+  "$id": "https://ai.open-vsx.org/schemas/mcp-approval.schema.json",
   "title": "MCP Server Approval",
   "description": "Vendor approval for an MCP server in the AI Registry",
   "type": "object",
@@ -20,6 +21,10 @@
       "type": "string",
       "description": "Pinned server version (e.g., 1.0.1). Omit to use the latest version from the MCP registry."
     },
+    "config": {
+      "$ref": "mcp-server-config.schema.json",
+      "description": "Generic, tool-agnostic connection info for this server. Used to derive installConfigs entries (in this approval or another vendor's) that request derivation."
+    },
     "installConfigs": {
       "type": "array",
       "description": "Tool-specific installation configurations. Omit if no tool-specific configuration is needed.",
@@ -43,8 +48,8 @@
             "description": "Link to an VS Code extension on OpenVSX that installs the MCP server configuration"
           },
           "config": {
-            "type": "object",
-            "description": "Tool-specific configuration object (e.g., MCP server settings)"
+            "description": "Tool-specific configuration object. Set to the literal string \"derived\" to request that this entry's config be automatically derived (from this approval's own root config, or another vendor's approval for the same server) using the tool's registered transform function.",
+            "oneOf": [{ "type": "object" }, { "const": "derived" }]
           },
           "instructions": {
             "type": "string",

diff --git a/schemas/mcp-server-config.schema.json b/schemas/mcp-server-config.schema.json
--- a/schemas/mcp-server-config.schema.json
+++ b/schemas/mcp-server-config.schema.json
@@ -0,0 +1,46 @@
+{
+  "$schema": "http://json-schema.org/draft-07/schema#",
+  "$id": "https://ai.open-vsx.org/schemas/mcp-server-config.schema.json",
+  "title": "MCP Server Config",
+  "description": "Generic, tool-agnostic connection info for an MCP server — a remote URL or a local (stdio) command, with optional auth. Derived from the emerging de-facto standard shape used by mcp.json-style client configs (e.g. Claude Code, VS Code, and similar derivatives), which wrap a per-server entry like this one under an outer \"mcpServers\"/\"servers\" collection keyed by server name — this schema deliberately omits that wrapper; it describes one server, not a wrapped collection. Per-tool derivation (including the outer wrapper) is implemented as a registered transform function, not part of this schema — see ai-registry-core/src/mcp-config-templates/.",
+  "oneOf": [
+    {
+      "type": "object",
+      "required": ["url"],
+      "additionalProperties": false,
+      "properties": {
+        "type": {
+          "type": "string",
+          "enum": ["http", "sse", "ws"],
+          "description": "Remote transport. Matches Claude Code's type values. Defaults to \"http\" (Streamable HTTP) if omitted."
+        },
+        "url": { "type": "string", "format": "uri" },
+        "headers": {
+          "type": "object",
+          "additionalProperties": { "type": "string" },
+          "description": "Static header-based auth, e.g. {\"Authorization\": \"Bearer <token>\"}."
+        },
+        "oauth": {
+          "type": "object",
+          "additionalProperties": false,
+          "properties": {
+            "authServerMetadataUrl": { "type": "string", "format": "uri" },
+            "scopes": { "type": "string" },
+            "clientId": { "type": "string" }
+          }
+        }
+      }
+    },
+    {
+      "type": "object",
+      "required": ["command"],
+      "additionalProperties": false,
+      "properties": {
+        "type": { "const": "stdio" },
+        "command": { "type": "string" },
+        "args": { "type": "array", "items": { "type": "string" } },
+        "env": { "type": "object" }
+      }
+    }
+  ]
+}

diff --git a/schemas/organization.schema.json b/schemas/organization.schema.json
--- a/schemas/organization.schema.json
+++ b/schemas/organization.schema.json
@@ -81,13 +81,18 @@
           },
           "artifactTypes": {
             "type": "object",
-            "description": "Which artifact types this trust entry applies to. Only \"skills\" is supported today.",
+            "description": "Which artifact types this trust entry applies to.",
             "additionalProperties": false,
             "properties": {
               "skills": {
                 "type": "object",
                 "additionalProperties": false,
                 "description": "Trust the organization's skill approvals. Empty today — reserved for future per-type conditions."
+              },
+              "mcp": {
+                "type": "object",
+                "additionalProperties": false,
+                "description": "Trust the organization's MCP server approvals. Empty today — reserved for future per-type conditions."
               }
             }
           }

diff --git a/src/consolidate.test.ts b/src/consolidate.test.ts
--- a/src/consolidate.test.ts
+++ b/src/consolidate.test.ts
@@ -7,16 +7,22 @@ import {
   resolveSkillInstallUrls,
   resolveSkillTrust,
   filterValidSkillTrusts,
+  resolveMcpTrust,
+  filterValidMcpTrusts,
   enrichWithRegistryData,
   resolveVendorMetadata,
+  pickWinningGenericConfig,
+  resolveMcpCrossVendorConfigs,
   buildToolView,
   buildToolSkillView,
   type ConsolidatedOutput,
   type ApprovalData,
   type SkillApprovalData,
+  type Approval,
   type McpEntry,
   type SkillEntry,
   type SkillTrustEntry,
+  type McpTrustEntry,
 } from "./consolidate.js";
 
 function emptyOutput(): ConsolidatedOutput {
@@ -1156,3 +1162,569 @@ describe("buildToolSkillView", () => {
     assert.equal(original[0].approvals[1].installConfigs.length, 1);
   });
 });
+
+describe("addOrganization — mcp trust extraction", () => {
+  it("collects an mcp trust entry", () => {
+    const output = emptyOutput();
+    const skillTrusts: SkillTrustEntry[] = [];
+    const mcpTrusts: McpTrustEntry[] = [];
+    addOrganization(
+      {
+        id: "theia",
+        name: "Theia IDE",
+        description: "IDE",
+        website: "https://theia-ide.org",
+        trusts: [{ org: "eclipsesource", artifactTypes: { mcp: {} } }],
+      },
+      output,
+      skillTrusts,
+      mcpTrusts,
+    );
+    assert.deepEqual(mcpTrusts, [
+      { org: "theia", trustedOrg: "eclipsesource" },
+    ]);
+    assert.deepEqual(skillTrusts, []);
+  });
+
+  it("collects both a skill and an mcp trust entry from the same organization", () => {
+    const output = emptyOutput();
+    const skillTrusts: SkillTrustEntry[] = [];
+    const mcpTrusts: McpTrustEntry[] = [];
+    addOrganization(
+      {
+        id: "theia",
+        name: "Theia IDE",
+        description: "IDE",
+        website: "https://theia-ide.org",
+        trusts: [
+          { org: "anthropic", artifactTypes: { skills: {} } },
+          { org: "eclipsesource", artifactTypes: { mcp: {} } },
+        ],
+      },
+      output,
+      skillTrusts,
+      mcpTrusts,
+    );
+    assert.deepEqual(skillTrusts, [{ org: "theia", trustedOrg: "anthropic" }]);
+    assert.deepEqual(mcpTrusts, [
+      { org: "theia", trustedOrg: "eclipsesource" },
+    ]);
+  });
+});
+
+describe("addApproval — genericConfig", () => {
+  it("populates Approval.genericConfig verbatim from the approval's own root config", () => {
+    const output = emptyOutput();
+    addApproval(
+      {
+        serverId: "io.example/foo",
+        date: "2026-08-05",
+        config: { url: "https://mcp.example.com" },
+      },
+      "eclipsesource",
+...
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ 5702dea961cf461107acfde43dcad953f774b27e -->
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
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Declares your organization and, if applicable, the tools you provide. Organizations that only approve artifacts without providing tools can omit the `tools` field. Set the optional `inferred` field to `true` for organizations pre-seeded from an official public source rather than participating directly in the registry — the website marks them with a distinct "Inferred" badge and a dashed-border treatment, with an explanatory tooltip on hover. See the [organization schema](schemas/organization.schema.json) for the full field reference.

```json
{
  "id": "your-org",
  "name": "Your Organization",
  "description": "Short description",
  "website": "https://example.com",
  "color": "#1a1f71",
  "tools": [
    {
      "id": "your-tool",
      "name": "Your Tool",
      "skillInstallUrlPrefix": "your-tool://install-skill?id=",
      "mcpInstallUrlPrefix": "your-tool://install-mcp?id="
    }
  ]
}
```

When a tool declares `skillInstallUrlPrefix` or `mcpInstallUrlPrefix`, consolidation auto-generates `installUrl` for any approval that targets that tool but omits it — `prefix + a...
```

Audit context only — docs diff excerpt:

```diff

```

Audit context only — docs after excerpt:

```markdown

```

### `GH-CAND-0022`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/72
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `72`
- PR title: Remove homepage preview banner, refresh hero messaging (#68)
- Language: `typescript`
- Code changed files: `['website/src/components/ApiPreviewNotice.tsx', 'website/src/components/InfoCallout.tsx', 'website/src/components/Layout.tsx', 'website/src/components/PreviewBanner.tsx', 'website/src/pages/AboutPage.tsx', 'website/src/pages/ApiDocsPage.tsx', 'website/src/pages/HomePage.tsx']`
- Docs changed files: `['README.md']`

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
diff --git a/website/src/components/ApiPreviewNotice.tsx b/website/src/components/ApiPreviewNotice.tsx
--- a/website/src/components/ApiPreviewNotice.tsx
+++ b/website/src/components/ApiPreviewNotice.tsx
@@ -0,0 +1,30 @@
+import { Link } from "react-router-dom";
+import { InfoCallout } from "./InfoCallout";
+
+/**
+ * Shared "API preview" copy shown on both the About and API-docs pages.
+ * `linkToApiDocs` adds a pointer to /api-docs — omit it on the API-docs page
+ * itself to avoid a self-referential link.
+ */
+export function ApiPreviewNotice({
+  linkToApiDocs = false,
+}: {
+  linkToApiDocs?: boolean;
+}) {
+  return (
+    <InfoCallout>
+      <strong>API preview:</strong> The public catalogue is available for use.
+      The API and metadata schema are still evolving and may change.
+      {linkToApiDocs && (
+        <>
+          {" "}
+          See the{" "}
+          <Link to="/api-docs" className="text-primary hover:underline">
+            API documentation
+          </Link>{" "}
+          for current details.
+        </>
+      )}
+    </InfoCallout>
+  );
+}

diff --git a/website/src/components/InfoCallout.tsx b/website/src/components/InfoCallout.tsx
--- a/website/src/components/InfoCallout.tsx
+++ b/website/src/components/InfoCallout.tsx
@@ -0,0 +1,16 @@
+import { Info } from "lucide-react";
+import type { ReactNode } from "react";
+
+/**
+ * Compact inline informational notice. Unlike a full-width banner, this is
+ * meant to sit within page content and read as a low-key status note rather
+ * than a warning.
+ */
+export function InfoCallout({ children }: { children: ReactNode }) {
+  return (
+    <div className="flex items-start gap-2 rounded-lg border border-primary/20 bg-primary/5 px-4 py-3 text-sm text-card-foreground">
+      <Info className="h-4 w-4 mt-0.5 flex-shrink-0 text-primary" />
+      <p className="leading-relaxed">{children}</p>
+    </div>
+  );
+}

diff --git a/website/src/components/Layout.tsx b/website/src/components/Layout.tsx
--- a/website/src/components/Layout.tsx
+++ b/website/src/components/Layout.tsx
@@ -1,12 +1,10 @@
 import { Outlet } from "react-router-dom";
 import { Header } from "./Header";
 import { Footer } from "./Footer";
-import { PreviewBanner } from "./PreviewBanner";
 
 export function Layout() {
   return (
     <div className="min-h-screen flex flex-col text-foreground">
-      <PreviewBanner />
       <Header />
       <main className="flex-1">
         <Outlet />

diff --git a/website/src/components/PreviewBanner.tsx b/website/src/components/PreviewBanner.tsx
--- a/website/src/components/PreviewBanner.tsx
+++ b/website/src/components/PreviewBanner.tsx
@@ -1,7 +0,0 @@
-export function PreviewBanner() {
-  return (
-    <div className="bg-warning-bg text-warning text-center py-1.5 px-4 text-sm font-medium border-b border-warning/20">
-      This registry is currently in preview. Data and APIs may change.
-    </div>
-  );
-}

diff --git a/website/src/pages/AboutPage.tsx b/website/src/pages/AboutPage.tsx
--- a/website/src/pages/AboutPage.tsx
+++ b/website/src/pages/AboutPage.tsx
@@ -1,4 +1,5 @@
 import { Link } from "react-router-dom";
+import { ApiPreviewNotice } from "../components/ApiPreviewNotice";
 
 export function AboutPage() {
   return (
@@ -38,12 +39,7 @@ export function AboutPage() {
       </section>
 
       <section className="mb-6">
-        <h2 className="text-xl font-semibold mt-8 mb-3">Preview</h2>
-        <p className="mb-3 leading-relaxed text-card-foreground">
-          This registry is currently in <strong>preview</strong>. Data, APIs,
-          and the website may change as we iterate on the concept. Feedback is
-          welcome.
-        </p>
+        <ApiPreviewNotice linkToApiDocs />
       </section>
 
       <section className="mb-6">
@@ -62,6 +58,18 @@ export function AboutPage() {
           </a>{" "}
           on our GitHub repository. We will guide you through the process.
         </p>
+        <p className="mb-3 leading-relaxed text-card-foreground">
+          Ready to register your organization as a tool provider? See{" "}
+          <a
+            href="https://github.com/eclipsefdn-ai-registry/ai-registry-core#becoming-a-vendor"
+            target="_blank"
+            rel="noopener noreferrer"
+            className="text-primary hover:underline"
+          >
+            Becoming a vendor
+          </a>{" "}
+          in the project README for the step-by-step process.
+        </p>
       </section>
 
       <section className="mb-6">

diff --git a/website/src/pages/ApiDocsPage.tsx b/website/src/pages/ApiDocsPage.tsx
--- a/website/src/pages/ApiDocsPage.tsx
+++ b/website/src/pages/ApiDocsPage.tsx
@@ -1,10 +1,16 @@
+import { ApiPreviewNotice } from "../components/ApiPreviewNotice";
+
 const BASE_URL = "https://ai.open-vsx.org/";
 
 export function ApiDocsPage() {
   return (
     <div className="max-w-3xl mx-auto px-4 py-8">
       <h1 className="text-2xl font-bold mb-6">API Documentation</h1>
 
+      <section className="mb-6">
+        <ApiPreviewNotice />
+      </section>
+
       <section className="mb-6">
         <p className="mb-3 leading-relaxed">
           The AI Registry provides a public JSON API. No authentication is

diff --git a/website/src/pages/HomePage.tsx b/website/src/pages/HomePage.tsx
--- a/website/src/pages/HomePage.tsx
+++ b/website/src/pages/HomePage.tsx
@@ -1,5 +1,5 @@
 import { useState, useMemo } from "react";
-import { useSearchParams } from "react-router-dom";
+import { Link, useSearchParams } from "react-router-dom";
 import { Search, ShieldCheck } from "lucide-react";
 import { useAllRegistryData } from "../hooks/useRegistryData";
 import { ServerList } from "../components/ServerList";
@@ -13,7 +13,7 @@ type Tab = "servers" | "skills" | "tools" | "organizations";
 
 const SEARCH_PLACEHOLDERS: Record<Tab, string> = {
   servers: "Search MCP servers...",
-  skills: "Search skills...",
+  skills: "Search agent skills...",
   tools: "Search tools...",
   organizations: "Search organizations...",
 };
@@ -144,11 +144,12 @@ export function HomePage() {
           </span>
 
           <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-foreground mb-6">
-            Find trusted AI artifacts.
+            Find AI tools you can trust.
           </h1>
 
           <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10 leading-relaxed">
-            Currently MCP servers and skills. More artifact types coming soon.
+            Discover MCP servers and agent skills, with transparent provenance
+            and approval signals from participating tool providers.
           </p>
 
           <div className="w-full max-w-2xl mb-3">
@@ -164,9 +165,16 @@ export function HomePage() {
             </div>
           </div>
 
-          <p className="text-sm text-muted-foreground mb-2">
-            Open governance. Free to use. No single vendor controls the catalog.
+          <p className="text-sm text-muted-foreground mb-6">
+            Open source. Open governance. Built for interoperability.
           </p>
+
+          <Link
+            to="/about"
+            className="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg border border-primary/20 bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
+          >
+            Join as a tool provider
+          </Link>
         </div>
       </section>
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ b8d9ed0d605099ce7ecf956c1cf63371acd45f15 -->
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
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Declares your organization and, if applicable, the tools you provide. Organizations that only approve artifacts without providing tools can omit the `tools` field. Set the optional `inferred` field to `true` for organizations pre-seeded from an official public source rather than participating directly in the registry — the website marks them with a distinct "Inferred" badge and a dashed-border treatment, with an explanatory tooltip on hover. See the [organization schema](schemas/organization.schema.json) for the full field reference.

```json
{
  "id": "your-org",
  "name": "Your Organization",
  "description": "Short description",
  "website": "https://example.com",
  "color": "#1a1f71",
  "tools": [
    {
      "id": "your-tool",
      "name": "Your Tool",
      "skillInstallUrlPrefix": "your-tool://install-skill?id=",
      "mcpInstallUrlPrefix": "your-tool://install-mcp?id="
    }
  ]
}
```

When a tool declares `skillInstallUrlPrefix` or `mcpInstallUrlPrefix`, consolidation auto-generates `installUrl` for any approval that targets that tool but omits it — `prefix + a...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -213,10 +213,9 @@ See the [Theia vendor repo](https://github.com/eclipsefdn-ai-registry/ai-registr
 
 ### Becoming a vendor
 
-1. Create a new repository following the structure above
-2. Add your `organization.json` and approval files in `mcp/` and/or `skills/`
-3. Set up CI using the [validate workflow](https://github.com/eclipsefdn-ai-registry/ai-registry-theia/blob/main/.github/workflows/validate.yml) from the Theia repo as a template
-4. Request registration by opening a PR on this repo that adds your entry to `vendors.json`
+1. Request a vendor repository by [opening an issue](https://github.com/eclipsefdn-ai-registry/ai-registry-core/issues) on this repo describing your organization and the artifacts you plan to approve
+2. We create a new repository for you from a template, with the structure above and CI (the [validate workflow](https://github.com/eclipsefdn-ai-registry/ai-registry-theia/blob/main/.github/workflows/validate.yml)) already set up — you only need to fill in your `organization.json` and add approval files in `mcp/` and/or `skills/`
+3. Request registration by opening a PR on this repo that adds your entry to `vendors.json`
 
 ## API
```

Audit context only — docs after excerpt:

```markdown
<!-- README.md @ 7f260049a0ead12f12981842e344f08d95ebb3e0 -->
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
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Declares your organization and, if applicable, the tools you provide. Organizations that only approve artifacts without providing tools can omit the `tools` field. Set the optional `inferred` field to `true` for organizations pre-seeded from an official public source rather than participating directly in the registry — the website marks them with a distinct "Inferred" badge and a dashed-border treatment, with an explanatory tooltip on hover. See the [organization schema](schemas/organization.schema.json) for the full field reference.

```json
{
  "id": "your-org",
  "name": "Your Organization",
  "description": "Short description",
  "website": "https://example.com",
  "color": "#1a1f71",
  "tools": [
    {
      "id": "your-tool",
      "name": "Your Tool",
      "skillInstallUrlPrefix": "your-tool://install-skill?id=",
      "mcpInstallUrlPrefix": "your-tool://install-mcp?id="
    }
  ]
}
```

When a tool declares `skillInstallUrlPrefix` or `mcpInstallUrlPrefix`, consolidation auto-generates `installUrl` for any approval that targets that tool but omits it — `prefix + a...
```

### `GH-CAND-0023`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/70
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `70`
- PR title: Bump fast-uri from 3.1.2 to 3.1.5
- Language: `typescript`
- Code changed files: `['package-lock.json']`
- Docs changed files: `[]`

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
diff --git a/package-lock.json b/package-lock.json
--- a/package-lock.json
+++ b/package-lock.json
@@ -1296,9 +1296,9 @@
       "license": "MIT"
     },
     "node_modules/fast-uri": {
-      "version": "3.1.2",
-      "resolved": "https://registry.npmjs.org/fast-uri/-/fast-uri-3.1.2.tgz",
-      "integrity": "sha512-rVjf7ArG3LTk+FS6Yw81V1DLuZl1bRbNrev6Tmd/9RaroeeRRJhAt7jg/6YFxbvAQXUCavSoZhPPj6oOx+5KjQ==",
+      "version": "3.1.5",
+      "resolved": "https://registry.npmjs.org/fast-uri/-/fast-uri-3.1.5.tgz",
+      "integrity": "sha512-gHwA1O9LDIcKunMKhObS/HimwtehO1nPUECKAu5TpKgaO19fcWEl4bliWe1jWxVFvIXztJjjQ4L8XQ1EU9f7Jw==",
       "funding": [
         {
           "type": "github",
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ 5702dea961cf461107acfde43dcad953f774b27e -->
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
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Declares your organization and, if applicable, the tools you provide. Organizations that only approve artifacts without providing tools can omit the `tools` field. Set the optional `inferred` field to `true` for organizations pre-seeded from an official public source rather than participating directly in the registry — the website marks them with a distinct "Inferred" badge and a dashed-border treatment, with an explanatory tooltip on hover. See the [organization schema](schemas/organization.schema.json) for the full field reference.

```json
{
  "id": "your-org",
  "name": "Your Organization",
  "description": "Short description",
  "website": "https://example.com",
  "color": "#1a1f71",
  "tools": [
    {
      "id": "your-tool",
      "name": "Your Tool",
      "skillInstallUrlPrefix": "your-tool://install-skill?id=",
      "mcpInstallUrlPrefix": "your-tool://install-mcp?id="
    }
  ]
}
```

When a tool declares `skillInstallUrlPrefix` or `mcpInstallUrlPrefix`, consolidation auto-generates `installUrl` for any approval that targets that tool but omits it — `prefix + a...
```

Audit context only — docs diff excerpt:

```diff

```

Audit context only — docs after excerpt:

```markdown

```

### `GH-CAND-0024`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/63
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `63`
- PR title: Rename "verified by publisher" to "Publisher claimed"
- Language: `typescript`
- Code changed files: `['src/consolidate.test.ts', 'src/consolidate.ts', 'website/src/components/McpVerificationBadge.tsx', 'website/src/types.ts']`
- Docs changed files: `['README.md', 'skills/create-mcp-approval/SKILL.md']`

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
diff --git a/src/consolidate.test.ts b/src/consolidate.test.ts
--- a/src/consolidate.test.ts
+++ b/src/consolidate.test.ts
@@ -341,7 +341,7 @@ describe("resolveVendorMetadata", () => {
     assert.equal(entry.name, "Acme Server");
     assert.equal(entry.description, "Suggested by Acme");
     assert.equal(entry.mcpRegistryVerified, false);
-    assert.equal(entry.vendorVerifiedBy, undefined);
+    assert.equal(entry.publisherClaimedBy, undefined);
   });
 
   it("prefers the earliest-dated metadata when two vendors disagree", () => {
@@ -399,7 +399,7 @@ describe("resolveVendorMetadata", () => {
     assert.equal(entry.description, "Acme description");
   });
 
-  it("sets vendorVerifiedBy and fills metadata for a self-published approval", () => {
+  it("sets publisherClaimedBy and fills metadata for a publisher-claimed approval", () => {
     const entry = baseEntry({
       approvals: [
         {
@@ -415,7 +415,7 @@ describe("resolveVendorMetadata", () => {
 
     resolveVendorMetadata(entry);
 
-    assert.equal(entry.vendorVerifiedBy, "acme");
+    assert.equal(entry.publisherClaimedBy, "acme");
     assert.equal(entry.name, "Acme Server");
     assert.equal(entry.description, "We built this");
   });
@@ -445,7 +445,7 @@ describe("resolveVendorMetadata", () => {
     }, /io\.example\/server/);
   });
 
-  it("does not overwrite registry-verified name/description with vendor metadata, but still marks vendorVerifiedBy", () => {
+  it("does not overwrite registry-verified name/description with vendor metadata, but still marks publisherClaimedBy", () => {
     const entry = baseEntry({
       name: "Registry Name",
       description: "Registry description",
@@ -466,7 +466,7 @@ describe("resolveVendorMetadata", () => {
 
     assert.equal(entry.name, "Registry Name");
     assert.equal(entry.description, "Registry description");
-    assert.equal(entry.vendorVerifiedBy, "acme");
+    assert.equal(entry.publisherClaimedBy, "acme");
   });
 });

diff --git a/src/consolidate.ts b/src/consolidate.ts
--- a/src/consolidate.ts
+++ b/src/consolidate.ts
@@ -95,8 +95,8 @@ export interface McpEntry {
   latestVersion?: string;
   mcpRegistryVerified: boolean;
   approvals: Approval[];
-  vendorVerifiedBy?: string;
-  // organization id of the single approval that self-attests as publisher
+  publisherClaimedBy?: string;
+  // organization id of the single approval claiming to be the publisher
 }
 
 export interface SkillInstallConfig {
@@ -226,31 +226,31 @@ export function enrichWithRegistryData(
 
 /**
  * Resolve vendor-supplied fallback metadata (name/description) and publisher
- * self-attestation for an MCP entry.
+ * claim status for an MCP entry.
  *
  * Precedence: Anthropic registry (already applied via enrichWithRegistryData)
- * > self-attested publisher metadata > earliest-dated vendor-suggested metadata.
+ * > publisher-claimed metadata > earliest-dated vendor-suggested metadata.
  *
- * Throws if two different organizations both self-attest as publisher for the
+ * Throws if two different organizations both claim to be the publisher of the
  * same server — that's a genuine contradiction, not a matter of opinion.
  */
 export function resolveVendorMetadata(entry: McpEntry): void {
-  const selfPublishedOrgs = [
+  const claimingOrgs = [
     ...new Set(
       entry.approvals
         .filter((a) => a.selfPublished)
         .map((a) => a.organizationId),
     ),
   ];
 
-  if (selfPublishedOrgs.length > 1) {
+  if (claimingOrgs.length > 1) {
     throw new Error(
-      `Conflicting self-attestation for MCP server "${entry.serverId}": ${selfPublishedOrgs.join(", ")}`,
+      `Conflicting publisher claim for MCP server "${entry.serverId}": ${claimingOrgs.join(", ")}`,
     );
   }
 
-  if (selfPublishedOrgs.length === 1) {
-    entry.vendorVerifiedBy = selfPublishedOrgs[0];
+  if (claimingOrgs.length === 1) {
+    entry.publisherClaimedBy = claimingOrgs[0];
   }
 
   if (entry.mcpRegistryVerified) {
@@ -262,9 +262,9 @@ export function resolveVendorMetadata(entry: McpEntry): void {
     return;
   }
 
-  const selfPublishedWithMetadata = withMetadata.find((a) => a.selfPublished);
+  const claimantWithMetadata = withMetadata.find((a) => a.selfPublished);
   const winner =
-    selfPublishedWithMetadata ??
+    claimantWithMetadata ??
     [...withMetadata].sort(
       (a, b) =>
         a.date.localeCompare(b.date) ||
@@ -564,8 +564,8 @@ export async function main(): Promise<void> {
   // Step 2a: Enrich MCP with Anthropic registry (fails build on registry errors)
   await enrichRegistryMetadata(output);
 
-  // Step 2a2: Resolve vendor-supplied fallback metadata + publisher self-attestation
-  // (fails build on conflicting self-attestation for the same server)
+  // Step 2a2: Resolve vendor-supplied fallback metadata + publisher claim
+  // (fails build on conflicting publisher claims for the same server)
   for (const entry of output.mcp) {
     resolveVendorMetadata(entry);
   }

diff --git a/website/src/components/McpVerificationBadge.tsx b/website/src/components/McpVerificationBadge.tsx
--- a/website/src/components/McpVerificationBadge.tsx
+++ b/website/src/components/McpVerificationBadge.tsx
@@ -4,9 +4,11 @@ import type { McpServer, Organization } from "../types";
 /**
  * Three-way verification badge for an MCP server:
  *  - mcpRegistryVerified: found in the Anthropic MCP registry (purple).
- *  - vendorVerifiedBy: no registry entry, but a vendor self-attested as the
- *    publisher/maintainer (blue) — distinct from registry verification.
- *  - otherwise: not found in the registry and no publisher attestation (amber).
+ *  - publisherClaimedBy: no registry entry, but a vendor claims to be the
+ *    publisher/maintainer (blue) — a self-attested claim, not third-party
+ *    registry verification. The claiming org's name is surfaced only in the
+ *    tooltip, not the badge text.
+ *  - otherwise: not found in the registry and no publisher claim (amber).
  *
  * `interactive` controls the hover/cursor-help affordance used on card
  * layouts (ServerList, ToolServerCard); detail views omit it.
@@ -38,16 +40,16 @@ export function McpVerificationBadge({
     );
   }
 
-  if (server.vendorVerifiedBy) {
-    const org = getOrg(server.vendorVerifiedBy);
-    const orgName = org ? org.name : server.vendorVerifiedBy;
+  if (server.publisherClaimedBy) {
+    const org = getOrg(server.publisherClaimedBy);
+    const orgName = org ? org.name : server.publisherClaimedBy;
     return (
       <span
         className={`inline-flex items-center gap-1 text-xs font-normal px-2 py-0.5 rounded-full bg-vendor-verified-bg text-vendor-verified border border-vendor-verified/20 ${interactiveClasses}`}
-        title={`Not in the Anthropic MCP registry. ${orgName} has self-attested that they publish/maintain this server — this is not an Anthropic-registry verification.`}
+        title={`Not in the Anthropic MCP registry. ${orgName} claims to be the publisher/maintainer of this server — this is not an Anthropic-registry verification.`}
       >
         <BadgeCheck className="h-3 w-3" />
-        Verified by {orgName}
+        Publisher claim
       </span>
     );
   }

diff --git a/website/src/types.ts b/website/src/types.ts
--- a/website/src/types.ts
+++ b/website/src/types.ts
@@ -36,7 +36,7 @@ export interface McpServer {
   latestVersion?: string;
   mcpRegistryVerified: boolean;
   approvals: Approval[];
-  vendorVerifiedBy?: string;
+  publisherClaimedBy?: string;
 }
 
 export interface SkillInstallConfig {
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ a3027443638de0865fc455a0abf84a2f99ed41b5 -->
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
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Declares your organization and, if applicable, the tools you provide. Organizations that only approve artifacts without providing tools can omit the `tools` field. Set the optional `inferred` field to `true` for organizations pre-seeded from an official public source rather than participating directly in the registry — the website marks them with a distinct "Inferred" badge and a dashed-border treatment, with an explanatory tooltip on hover. See the [organization schema](schemas/organization.schema.json) for the full field reference.

```json
{
  "id": "your-org",
  "name": "Your Organization",
  "description": "Short description",
  "website": "https://example.com",
  "color": "#1a1f71",
  "tools": [
    {
      "id": "your-tool",
      "name": "Your Tool",
      "skillInstallUrlPrefix": "your-tool://install-skill?id=",
      "mcpInstallUrlPrefix": "your-tool://install-mcp?id="
    }
  ]
}
```

When a tool declares `skillInstallUrlPrefix` or `mcpInstallUrlPrefix`, consolidation auto-generates `installUrl` for any approval that targets that tool but omits it — `prefix + a...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -137,13 +137,13 @@ Not every MCP server a vendor wants to approve is registered with Anthropic yet.
 ```
 
 - **`metadata`** (`{ name, description }`) — a fallback name/description used only while the server is absent from the Anthropic registry. Once the server appears there, registry data always takes precedence and `metadata` is ignored.
-- **`selfPublished`** (boolean) — set this only if your organization actually publishes/maintains the server (not merely approves or recommends it). It renders a distinct "Verified by {vendor}" badge on the website, separate from Anthropic-registry verification.
+- **`selfPublished`** (boolean) — set this only if your organization actually publishes/maintains the server (not merely approves or recommends it). It renders a distinct "Publisher claim" badge on the website, separate from Anthropic-registry verification; the claiming organization's name appears in the badge's tooltip, not the badge text itself.
 
 These two fields are independent: any approving vendor may supply `metadata` as a suggestion without self-attesting, and self-attestation implies stronger trust in that vendor's `metadata` if supplied.
 
 Resolution when a server has no registry entry:
 
-1. If exactly one vendor set `selfPublished: true`, that vendor's `metadata` (if present) wins, and the website shows "Verified by {vendor}". **Two different vendors self-attesting for the same server is a contradiction and fails the shared consolidation build** — a server can only have one publisher.
+1. If exactly one vendor set `selfPublished: true`, that vendor's `metadata` (if present) wins, and the website shows a "Publisher claim" badge (the claiming vendor's name is in the tooltip). **Two different vendors self-attesting for the same server is a contradiction and fails the shared consolidation build** — a server can only have one publisher.
 2. Otherwise, among vendors that supplied plain `metadata`, the earliest-`date` approval wins (organization ID alphabetically as a tie-break on an exact date match). This is a deterministic, non-fatal fallback — vendors can't see each other's data before filing, so disagreement here is expected and only logged as a warning, not a build failure.
 
 ### Skill approval files

diff --git a/skills/create-mcp-approval/SKILL.md b/skills/create-mcp-approval/SKILL.md
--- a/skills/create-mcp-approval/SKILL.md
+++ b/skills/create-mcp-approval/SKILL.md
@@ -44,7 +44,7 @@ Example: Server ID `io.github.ChromeDevTools/chrome-devtools-mcp` becomes filena
   - **installUrl**: Deep-link URL for one-click install (optional). **Omit if the tool declares `mcpInstallUrlPrefix` in `organization.json`** — consolidation generates it automatically as `prefix + serverId`. Set it explicitly only when the tool has no prefix or you need a non-standard URL.
   - **openVsxUrl**: Link to an Open VSX extension (optional).
 - **metadata** (optional): `{ "name": "...", "description": "..." }` — only relevant when the server was not found in the Anthropic MCP registry (step 2). Provides a fallback name/description so the server doesn't show up as a raw serverId with no description. Ignored once the server appears in the registry.
-- **selfPublished** (optional, boolean): Set to `true` only when the vendor filing this approval is the actual publisher/maintainer of the MCP server — never set this on behalf of a server you merely use or recommend. Do not set it just because you're supplying `metadata`. It drives a distinct "Verified by {vendor}" badge on the website. Two different vendors self-attesting for the same server fails the shared consolidation build, so only set this when you're confident it's accurate.
+- **selfPublished** (optional, boolean): Set to `true` only when the vendor filing this approval is the actual publisher/maintainer of the MCP server — never set this on behalf of a server you merely use or recommend. Do not set it just because you're supplying `metadata`. It drives a distinct "Publisher claim" badge on the website (the claiming vendor's name appears in the tooltip, not the badge text). Two different vendors self-attesting for the same server fails the shared consolidation build, so only set this when you're confident it's accurate.
 
 ## Remote Servers and OAuth
```

Audit context only — docs after excerpt:

```markdown
<!-- README.md @ ad52c9ea4aabf574da9d66aa496112f023486278 -->
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
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Declares your organization and, if applicable, the tools you provide. Organizations that only approve artifacts without providing tools can omit the `tools` field. Set the optional `inferred` field to `true` for organizations pre-seeded from an official public source rather than participating directly in the registry — the website marks them with a distinct "Inferred" badge and a dashed-border treatment, with an explanatory tooltip on hover. See the [organization schema](schemas/organization.schema.json) for the full field reference.

```json
{
  "id": "your-org",
  "name": "Your Organization",
  "description": "Short description",
  "website": "https://example.com",
  "color": "#1a1f71",
  "tools": [
    {
      "id": "your-tool",
      "name": "Your Tool",
      "skillInstallUrlPrefix": "your-tool://install-skill?id=",
      "mcpInstallUrlPrefix": "your-tool://install-mcp?id="
    }
  ]
}
```

When a tool declares `skillInstallUrlPrefix` or `mcpInstallUrlPrefix`, consolidation auto-generates `installUrl` for any approval that targets that tool but omits it — `prefix + a...
```

### `GH-CAND-0025`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/64
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `64`
- PR title: Adapt inferred badge
- Language: `typescript`
- Code changed files: `['website/src/orgBadge.ts']`
- Docs changed files: `[]`

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
diff --git a/website/src/orgBadge.ts b/website/src/orgBadge.ts
--- a/website/src/orgBadge.ts
+++ b/website/src/orgBadge.ts
@@ -5,7 +5,7 @@ import type { Organization } from "./types";
  * public source rather than participating directly in the registry.
  */
 export const INFERRED_DISCLAIMER =
-  "Based on an official public source. This does not indicate direct participation by the organisation in the AI Registry.";
+  "This entry is based solely on information published through the organisation's official public channels. The organisation has not endorsed, approved or validated this listing, and is not necessarily participating in the AI Registry.";
 
 export interface OrgBadge {
   inferred: boolean;
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ 8e24c4a2f3c1a5f8379a1a024823cbfc767802e3 -->
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
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Declares your organization and, if applicable, the tools you provide. Organizations that only approve artifacts without providing tools can omit the `tools` field. Set the optional `inferred` field to `true` for organizations pre-seeded from an official public source rather than participating directly in the registry — the website marks them with a distinct "Inferred" badge and a dashed-border treatment, with an explanatory tooltip on hover. See the [organization schema](schemas/organization.schema.json) for the full field reference.

```json
{
  "id": "your-org",
  "name": "Your Organization",
  "description": "Short description",
  "website": "https://example.com",
  "color": "#1a1f71",
  "tools": [
    {
      "id": "your-tool",
      "name": "Your Tool",
      "skillInstallUrlPrefix": "your-tool://install-skill?id=",
      "mcpInstallUrlPrefix": "your-tool://install-mcp?id="
    }
  ]
}
```

When a tool declares `skillInstallUrlPrefix` or `mcpInstallUrlPrefix`, consolidation auto-generates `installUrl` for any approval that targets that tool but omits it — `prefix + a...
```

Audit context only — docs diff excerpt:

```diff

```

Audit context only — docs after excerpt:

```markdown

```

### `GH-CAND-0026`

- Source URL: https://github.com/eclipsefdn-ai-registry/ai-registry-core/pull/62
- Repository: `eclipsefdn-ai-registry/ai-registry-core`
- PR number: `62`
- PR title: Add vendor-supplied fallback metadata and publisher self-attestation of MCP servers
- Language: `typescript`
- Code changed files: `['schemas/mcp-approval.schema.json', 'src/consolidate.test.ts', 'src/consolidate.ts', 'website/src/components/McpVerificationBadge.tsx', 'website/src/components/ServerDetail.tsx', 'website/src/components/ServerList.tsx', 'website/src/pages/ToolPage.tsx', 'website/src/types.ts']`
- Docs changed files: `['README.md', 'skills/create-mcp-approval/SKILL.md']`

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
diff --git a/schemas/mcp-approval.schema.json b/schemas/mcp-approval.schema.json
--- a/schemas/mcp-approval.schema.json
+++ b/schemas/mcp-approval.schema.json
@@ -52,6 +52,26 @@
           }
         }
       }
+    },
+    "metadata": {
+      "type": "object",
+      "required": ["name", "description"],
+      "additionalProperties": false,
+      "description": "Vendor-supplied fallback metadata, used only when the server is not found in the Anthropic MCP registry.",
+      "properties": {
+        "name": {
+          "type": "string",
+          "minLength": 1
+        },
+        "description": {
+          "type": "string",
+          "minLength": 1
+        }
+      }
+    },
+    "selfPublished": {
+      "type": "boolean",
+      "description": "Attest that this organization publishes/maintains this MCP server. Renders a 'Verified by <org>' badge. Two organizations self-attesting for the same server fails consolidation."
     }
   }
 }

diff --git a/src/consolidate.test.ts b/src/consolidate.test.ts
--- a/src/consolidate.test.ts
+++ b/src/consolidate.test.ts
@@ -6,6 +6,7 @@ import {
   addSkillApproval,
   resolveSkillInstallUrls,
   enrichWithRegistryData,
+  resolveVendorMetadata,
   buildToolView,
   buildToolSkillView,
   type ConsolidatedOutput,
@@ -310,6 +311,165 @@ describe("enrichWithRegistryData", () => {
   });
 });
 
+describe("resolveVendorMetadata", () => {
+  function baseEntry(overrides: Partial<McpEntry> = {}): McpEntry {
+    return {
+      serverId: "io.example/server",
+      name: "io.example/server",
+      description: "",
+      mcpRegistryVerified: false,
+      approvals: [],
+      ...overrides,
+    };
+  }
+
+  it("fills name/description from a single vendor-suggested metadata", () => {
+    const entry = baseEntry({
+      approvals: [
+        {
+          organizationId: "acme",
+          date: "2026-05-01",
+          configHash: "abc",
+          installConfigs: [],
+          metadata: { name: "Acme Server", description: "Suggested by Acme" },
+        },
+      ],
+    });
+
+    resolveVendorMetadata(entry);
+
+    assert.equal(entry.name, "Acme Server");
+    assert.equal(entry.description, "Suggested by Acme");
+    assert.equal(entry.mcpRegistryVerified, false);
+    assert.equal(entry.vendorVerifiedBy, undefined);
+  });
+
+  it("prefers the earliest-dated metadata when two vendors disagree", () => {
+    const entry = baseEntry({
+      approvals: [
+        {
+          organizationId: "later-org",
+          date: "2026-05-10",
+          configHash: "abc",
+          installConfigs: [],
+          metadata: { name: "Later Name", description: "Later description" },
+        },
+        {
+          organizationId: "earlier-org",
+          date: "2026-05-01",
+          configHash: "def",
+          installConfigs: [],
+          metadata: {
+            name: "Earlier Name",
+            description: "Earlier description",
+          },
+        },
+      ],
+    });
+
+    resolveVendorMetadata(entry);
+
+    assert.equal(entry.name, "Earlier Name");
+    assert.equal(entry.description, "Earlier description");
+  });
+
+  it("breaks an exact date tie alphabetically by org id", () => {
+    const entry = baseEntry({
+      approvals: [
+        {
+          organizationId: "zebra-org",
+          date: "2026-05-01",
+          configHash: "abc",
+          installConfigs: [],
+          metadata: { name: "Zebra Name", description: "Zebra description" },
+        },
+        {
+          organizationId: "acme",
+          date: "2026-05-01",
+          configHash: "def",
+          installConfigs: [],
+          metadata: { name: "Acme Name", description: "Acme description" },
+        },
+      ],
+    });
+
+    resolveVendorMetadata(entry);
+
+    assert.equal(entry.name, "Acme Name");
+    assert.equal(entry.description, "Acme description");
+  });
+
+  it("sets vendorVerifiedBy and fills metadata for a self-published approval", () => {
+    const entry = baseEntry({
+      approvals: [
+        {
+          organizationId: "acme",
+          date: "2026-05-01",
+          configHash: "abc",
+          installConfigs: [],
+          selfPublished: true,
+          metadata: { name: "Acme Server", description: "We built this" },
+        },
+      ],
+    });
+
+    resolveVendorMetadata(entry);
+
+    assert.equal(entry.vendorVerifiedBy, "acme");
+    assert.equal(entry.name, "Acme Server");
+    assert.equal(entry.description, "We built this");
+  });
+
+  it("throws when two different organizations both self-publish the same server", () => {
+    const entry = baseEntry({
+      approvals: [
+        {
+          organizationId: "acme",
+          date: "2026-05-01",
+          configHash: "abc",
+          installConfigs: [],
+          selfPublished: true,
+        },
+        {
+          organizationId: "other-org",
+          date: "2026-05-02",
+          configHash: "def",
+          installConfigs: [],
+          selfPublished: true,
+        },
+      ],
+    });
+
+    assert.throws(() => {
+      resolveVendorMetadata(entry);
+    }, /io\.example\/server/);
+  });
+
+  it("does not overwrite registry-verified name/description with vendor metadata, but still marks vendorVerifiedBy", () => {
+    const entry = baseEntry({
+      name: "Registry Name",
+      description: "Registry description",
+      mcpRegistryVerified: true,
+      approvals: [
+        {
+          organizationId: "acme",
+          date: "2026-05-01",
+          configHash: "abc",
+          installConfigs: [],
+          selfPublished: true,
+          metadata: { name: "Vendor Name", description: "Vendor description" },
+        },
+      ],
+    });
+
+    resolveVendorMetadata(entry);
+
+    assert.equal(entry.name, "Registry Name");
+    assert.equal(entry.description, "Registry description");
+    assert.equal(entry.vendorVerifiedBy, "acme");
+  });
+});
+
 describe("buildToolView", () => {
   function servers(): McpEntry[] {
     return [

diff --git a/src/consolidate.ts b/src/consolidate.ts
--- a/src/consolidate.ts
+++ b/src/consolidate.ts
@@ -63,11 +63,18 @@ export interface InstallConfig {
   instructions?: string;
 }
 
+export interface VendorMcpMetadata {
+  name: string;
+  description: string;
+}
+
 export interface ApprovalData {
   serverId: string;
   date: string;
   version?: string;
   installConfigs?: InstallConfig[];
+  metadata?: VendorMcpMetadata;
+  selfPublished?: boolean;
 }
 
 export interface Approval {
@@ -77,6 +84,8 @@ export interface Approval {
   configHash: string;
   installConfigs: InstallConfig[];
   // installConfigs is always present in output (defaults to [])
+  metadata?: VendorMcpMetadata;
+  selfPublished?: boolean;
 }
 
 export interface McpEntry {
@@ -86,6 +95,8 @@ export interface McpEntry {
   latestVersion?: string;
   mcpRegistryVerified: boolean;
   approvals: Approval[];
+  vendorVerifiedBy?: string;
+  // organization id of the single approval that self-attests as publisher
 }
 
 export interface SkillInstallConfig {
@@ -187,6 +198,12 @@ export function addApproval(
   if (approvalData.version) {
     approval.version = approvalData.version;
   }
+  if (approvalData.metadata) {
+    approval.metadata = approvalData.metadata;
+  }
+  if (approvalData.selfPublished) {
+    approval.selfPublished = approvalData.selfPublished;
+  }
   mcpEntry.approvals.push(approval);
 }
 
@@ -207,6 +224,67 @@ export function enrichWithRegistryData(
   }
 }
 
+/**
+ * Resolve vendor-supplied fallback metadata (name/description) and publisher
+ * self-attestation for an MCP entry.
+ *
+ * Precedence: Anthropic registry (already applied via enrichWithRegistryData)
+ * > self-attested publisher metadata > earliest-dated vendor-suggested metadata.
+ *
+ * Throws if two different organizations both self-attest as publisher for the
+ * same server — that's a genuine contradiction, not a matter of opinion.
+ */
+export function resolveVendorMetadata(entry: McpEntry): void {
+  const selfPublishedOrgs = [
+    ...new Set(
+      entry.approvals
+        .filter((a) => a.selfPublished)
+        .map((a) => a.organizationId),
+    ),
+  ];
+
+  if (selfPublishedOrgs.length > 1) {
+    throw new Error(
+      `Conflicting self-attestation for MCP server "${entry.serverId}": ${selfPublishedOrgs.join(", ")}`,
+    );
+  }
+
+  if (selfPublishedOrgs.length === 1) {
+    entry.vendorVerifiedBy = selfPublishedOrgs[0];
+  }
+
+  if (entry.mcpRegistryVerified) {
+    return;
+  }
+
+  const withMetadata = entry.approvals.filter((a) => a.metadata);
+  if (withMetadata.length === 0) {
+    return;
+  }
+
+  const selfPublishedWithMetadata = withMetadata.find((a) => a.selfPublished);
+  const winner =
+    selfPublishedWithMetadata ??
+    [...withMetadata].sort(
+      (a, b) =>
+        a.date.localeCompare(b.date) ||
+        a.organizationId.localeCompare(b.organizationId),
+    )[0];
+
+  entry.name = winner.metadata!.name;
+  entry.description = winner.metadata!.descri...
```

Allowed model input — docs before excerpt:

```markdown
<!-- README.md @ 813b6b597cdacdff54ac0c08c068d6fe2c46b4d5 -->
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
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Declares your organization and, if applicable, the tools you provide. Organizations that only approve artifacts without providing tools can omit the `tools` field. Set the optional `inferred` field to `true` for organizations pre-seeded from an official public source rather than participating directly in the registry — the website marks them with a distinct "Inferred" badge and a dashed-border treatment, with an explanatory tooltip on hover. See the [organization schema](schemas/organization.schema.json) for the full field reference.

```json
{
  "id": "your-org",
  "name": "Your Organization",
  "description": "Short description",
  "website": "https://example.com",
  "color": "#1a1f71",
  "tools": [
    {
      "id": "your-tool",
      "name": "Your Tool",
      "skillInstallUrlPrefix": "your-tool://install-skill?id=",
      "mcpInstallUrlPrefix": "your-tool://install-mcp?id="
    }
  ]
}
```

When a tool declares `skillInstallUrlPrefix` or `mcpInstallUrlPrefix`, consolidation auto-generates `installUrl` for any approval that targets that tool but omits it — `prefix + a...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -120,6 +120,32 @@ Example: `mcp/io.github.ChromeDevTools--chrome-devtools-mcp.json`
 
 The `serverId` must reference a server in the [Anthropic MCP registry](https://registry.modelcontextprotocol.io). Server metadata (name, description) is retrieved automatically during consolidation — you only supply the ID and optionally install configurations. Approvals without `installConfigs` are valid and indicate the organization approves the server without providing tool-specific configuration.
 
+#### Vendor-supplied metadata for servers not in the Anthropic registry
+
+Not every MCP server a vendor wants to approve is registered with Anthropic yet. For these, an approval can optionally include `metadata` and `selfPublished`:
+
+```json
+{
+  "serverId": "io.github.some-org/not-yet-registered-server",
+  "date": "2026-07-01",
+  "metadata": {
+    "name": "Not Yet Registered Server",
+    "description": "Does something useful, pending registration with the Anthropic MCP registry."
+  },
+  "selfPublished": true
+}
+```
+
+- **`metadata`** (`{ name, description }`) — a fallback name/description used only while the server is absent from the Anthropic registry. Once the server appears there, registry data always takes precedence and `metadata` is ignored.
+- **`selfPublished`** (boolean) — set this only if your organization actually publishes/maintains the server (not merely approves or recommends it). It renders a distinct "Verified by {vendor}" badge on the website, separate from Anthropic-registry verification.
+
+These two fields are independent: any approving vendor may supply `metadata` as a suggestion without self-attesting, and self-attestation implies stronger trust in that vendor's `metadata` if supplied.
+
+Resolution when a server has no registry entry:
+
+1. If exactly one vendor set `selfPublished: true`, that vendor's `metadata` (if present) wins, and the website shows "Verified by {vendor}". **Two different vendors self-attesting for the same server is a contradiction and fails the shared consolidation build** — a server can only have one publisher.
+2. Otherwise, among vendors that supplied plain `metadata`, the earliest-`date` approval wins (organization ID alphabetically as a tie-break on an exact date match). This is a deterministic, non-fatal fallback — vendors can't see each other's data before filing, so disagreement here is expected and only logged as a warning, not a build failure.
+
 ### Skill approval files
 
 One JSON file per approved Agent Skill (or group of skills from the same repo), stored in `skills/`. The filename must be `<skillId>.json` with `/` replaced by `--`. See the [skill approval schema](schemas/skill-approval.schema.json) for the full field reference.
@@ -200,7 +226,7 @@ A tool integration typically fetches `organizations.json` + its own `tools/<tool
 The consolidation pipeline follows a build-or-nothing approach:
 
 1. **Collect** — Clone all vendor repos and validate their data. Any failure (repo unreachable, invalid data) fails the build.
-2. **Enrich MCP** — Look up each server in the Anthropic MCP registry. Registry errors (down, rate-limited, etc.) fail the build. A server not found in the registry is fine — it's included with `mcpRegistryVerified: false`.
+2. **Enrich MCP** — Look up each server in the Anthropic MCP registry. Registry errors (down, rate-limited, etc.) fail the build. A server not found in the registry is fine — it's included with `mcpRegistryVerified: false`, then falls back to any vendor-supplied `metadata`/`selfPublished` (see [Vendor-supplied metadata](#vendor-supplied-metadata-for-servers-not-in-the-anthropic-registry)). Two different vendors self-attesting as publisher for the same server is treated the same as a registry error — it fails the build.
 3. **Enrich Skills** — Fetch each skill's source via sparse git checkout to extract metadata and compute a content hash. Unreachable sources are skipped with a warning — the skill is omitted from the output until its source is reachable again.
 4. **Write & Deploy** — Only reached if the previous steps succeed.

diff --git a/skills/create-mcp-approval/SKILL.md b/skills/create-mcp-approval/SKILL.md
--- a/skills/create-mcp-approval/SKILL.md
+++ b/skills/create-mcp-approval/SKILL.md
@@ -18,7 +18,7 @@ Vendors maintain their own repositories with approval files for MCP servers they
 ## Your Workflow
 
 1. **Identify the MCP server** — The user provides a server ID (e.g., `io.github.ChromeDevTools/chrome-devtools-mcp`).
-2. **Verify the server exists** — Fetch `https://registry.modelcontextprotocol.io/v0.1/servers/<serverId>/versions` (URL-encode the serverId). If the server is not found (404), warn the user but allow them to proceed.
+2. **Verify the server exists** — Fetch `https://registry.modelcontextprotocol.io/v0.1/servers/<serverId>/versions` (URL-encode the serverId). If the server is not found (404), warn the user but allow them to proceed. In this case, offer to add `metadata` (see below) so the server shows a real name/description instead of the raw serverId.
 3. **Read the vendor's organization.json** — Find `organization.json` in the repo root to determine the vendor ID and available tools.
 4. **Read the approval schema** — Fetch the schema from `https://ai.open-vsx.org/schemas/mcp-approval.schema.json` to ensure you follow the current contract.
 5. **Read tool-specific config docs** — Check `ai-docs/mcp-approval.md` in the repo. If it exists, read it to understand how to construct the `config` and `installUrl` for this vendor's tools.
@@ -43,6 +43,8 @@ Example: Server ID `io.github.ChromeDevTools/chrome-devtools-mcp` becomes filena
   - **instructions**: Human-readable setup instructions.
   - **installUrl**: Deep-link URL for one-click install (optional). **Omit if the tool declares `mcpInstallUrlPrefix` in `organization.json`** — consolidation generates it automatically as `prefix + serverId`. Set it explicitly only when the tool has no prefix or you need a non-standard URL.
   - **openVsxUrl**: Link to an Open VSX extension (optional).
+- **metadata** (optional): `{ "name": "...", "description": "..." }` — only relevant when the server was not found in the Anthropic MCP registry (step 2). Provides a fallback name/description so the server doesn't show up as a raw serverId with no description. Ignored once the server appears in the registry.
+- **selfPublished** (optional, boolean): Set to `true` only when the vendor filing this approval is the actual publisher/maintainer of the MCP server — never set this on behalf of a server you merely use or recommend. Do not set it just because you're supplying `metadata`. It drives a distinct "Verified by {vendor}" badge on the website. Two different vendors self-attesting for the same server fails the shared consolidation build, so only set this when you're confident it's accurate.
 
 ## Remote Servers and OAuth
```

Audit context only — docs after excerpt:

```markdown
<!-- README.md @ e417e66d357b8dd4bce6a0d2b073541ba88f587b -->
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
│ Vendor B     │──┘         │  + Metadata     │          │  Tools/IDEs  │
│ (approvals)  │            └─────────────────┘          └──────────────┘
└──────────────┘
```

**Vendor repos** contain:

- `organization.json` — organization identity and (optionally) tools
- `mcp/*.json` — one approval file per approved MCP server, with optional tool-specific install configurations
- `skills/*.json` — one approval file per approved Agent Skill, pointing to the skill's source repository

**The central repo** provides:

- JSON schemas that define the contract for all participants
- A consolidation pipeline that pulls, validates, and merges vendor data
- Metadata enrichment from the Anthropic MCP registry (server names, descriptions, verification status)
- Metadata enrichment from skill source repos (name, description, content hash)
- A static website deployed to GitHub Pages for browsing the registry
- Claude Code skills for generating [MCP](skills/create-mcp-approval/SKILL.md) and [skill](skills/create-skill-approval/SKILL.md) approval files

## Repositories

| Repository                                                                       | Purpose                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| [ai-registry-core](https://github.com/eclipsefdn-ai-registry/ai-registry-core)   | Central repo — schemas, consolidation, website, AI skill ([development guide](DEVELOPMENT.md)) |
| [ai-registry-theia](https://github.com/eclipsefdn-ai-registry/ai-registry-theia) | Theia IDE vendor repo — serves as the reference implementation for vendor repositories         |

## Data Flow

1. A vendor creates approval files (manually or using the Claude Code skills for [MCP](skills/create-mcp-approval/SKILL.md) or [skills](skills/create-skill-approval/SKILL.md))
2. Vendor commits and pushes — CI validates against the central schemas
3. On successful push to main, the vendor CI triggers the central consolidation workflow
4. Consolidation pulls all registered vendor repos, validates, enriches with MCP registry metadata and skill source metadata
5. The website and consolidated JSON are built and deployed to GitHub Pages
6. Tools (e.g., Theia IDE) consume the consolidated JSON at a stable URL

## Vendor Guide

### Repository structure

A vendor repo is a pure data repository — no dependencies, no build steps. It contains:

```
organization.json          # vendor identity and tools
mcp/
  <server-id>.json         # one file per approved MCP server
skills/
  <skill-id>.json          # one file per approved Agent Skill
.github/workflows/
  validate.yml             # CI that runs the central validation
```

### organization.json

Declares your organization and, if applicable, the tools you provide. Organizations that only approve artifacts without providing tools can omit the `tools` field. Set the optional `inferred` field to `true` for organizations pre-seeded from an official public source rather than participating directly in the registry — the website marks them with a distinct "Inferred" badge and a dashed-border treatment, with an explanatory tooltip on hover. See the [organization schema](schemas/organization.schema.json) for the full field reference.

```json
{
  "id": "your-org",
  "name": "Your Organization",
  "description": "Short description",
  "website": "https://example.com",
  "color": "#1a1f71",
  "tools": [
    {
      "id": "your-tool",
      "name": "Your Tool",
      "skillInstallUrlPrefix": "your-tool://install-skill?id=",
      "mcpInstallUrlPrefix": "your-tool://install-mcp?id="
    }
  ]
}
```

When a tool declares `skillInstallUrlPrefix` or `mcpInstallUrlPrefix`, consolidation auto-generates `installUrl` for any approval that targets that tool but omits it — `prefix + a...
```

### `GH-CAND-0027`

- Source URL: https://github.com/torbido-hq/cicerone/pull/112
- Repository: `torbido-hq/cicerone`
- PR number: `112`
- PR title: fix: load Google Analytics only after Accept
- Language: `python`
- Code changed files: `['website/src/env.d.ts']`
- Docs changed files: `['website/README.md', 'website/src/content/docs/privacy.md']`

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
diff --git a/website/src/env.d.ts b/website/src/env.d.ts
--- a/website/src/env.d.ts
+++ b/website/src/env.d.ts
@@ -3,6 +3,8 @@
 interface Window {
 	gtag?: (...args: unknown[]) => void;
 	dataLayer?: unknown[];
+	__CICERONE_GA_ID?: string;
+	__ciceroneGtagLoaded?: boolean;
 }
 
 interface ImportMetaEnv {
```

Allowed model input — docs before excerpt:

```markdown
<!-- website/README.md @ 8b9a2fad3909013ac8521bf2bf889560b4c8d8de -->
# Cicerone website (Astro Starlight)

Docs site for [cicerone.dev](https://cicerone.dev). Built with
[Starlight](https://starlight.astro.build/); markdown under repo `docs/` is
synced into the Starlight content collection at build time. Articles are the
same static build (no CMS): posts live under `src/content/docs/articles/`.
With no published post, the articles plugin is off — no header link, RSS, or
`/articles/` route.

## Commands

```sh
cd website
npm ci
npm run dev      # sync docs/ + local preview
npm run build    # sync docs/ + production build → dist/
npm run preview  # serve dist/
```

## Layout

| Path | Role |
| --- | --- |
| `src/content/docs/index.mdx` | Landing (Starlight splash) |
| `src/content/docs/articles/` | Articles (`title` + `date` frontmatter) → `/articles/` |
| `scripts/sync-docs.mjs` | Copies `../docs/*.md` → `src/content/docs/` with frontmatter |
| `astro.config.mjs` | Site URL, sidebar, logo, social, articles plugin |
| `src/lib/consent.mjs` | Cookie banner + Consent Mode v2 (`G-E38EP8PJSR`) |
| `public/CNAME` | Custom domain (`cicerone.dev`) |
| `public/images/` | Site diagrams (`flow.svg`) |
| `public/images/docs/` | Copied from `../docs/images/` at build time (gitignored) |

Generated `src/content/docs/how-it-works.md`, `tutorial.md`,
`architecture.md`, `incremental-events.md`, `src/generated/latest-release.json`,
and `public/images/docs/` are gitignored; they are created at build/dev time. CI and local builds always
sync from `docs/`. Articles are **not** synced from `docs/` — add Markdown
under `src/content/docs/articles/` (see below).

## Articles

Jekyll-style: a `.md` file with YAML frontmatter, HTML at build time, nothing
dynamic. Author globally is `nicholas` (`astro.config.mjs`). Until a
non-draft post exists, Articles is omitted from the build.

```md
---
title: Post title
description: One-line summary for search results and Open Graph.
date: 2026-08-19
excerpt: Listing blurb (falls back to description / body).
authors:
  - nicholas
---

Body…
```

Drafts (`draft: true`, or YAML 1.1 `yes` / `on`) are omitted from
production builds; `astro dev` still loads them so `/articles/` can be
previewed. Frontmatter is parsed as YAML. RSS is
`/articles/rss.xml` once a post is published. Article pages use IBM Plex
Serif at ~65ch; chrome stays IBM Plex Sans, dates IBM Plex Mono.

## Publishing

[`.github/workflows/pages.yml`](../.github/workflows/pages.yml) builds
`website/` on PRs and on pushes to `main` that touch `website/**` or
`docs/**`. Only `main` deploys. Website-only PRs skip Docker lint/pytest;
the `ci` job still succeeds so a required check is not left pending.

Google Analytics is `G-E38EP8PJSR` in `src/lib/consent.mjs`. Override with
`PUBLIC_GA_MEASUREMENT_ID` at build time if needed.

**One-time:** Settings → Pages → Source = **GitHub Actions**, custom domain
`cicerone.dev`. DNS notes for Gandi apex records are below.

### DNS (apex `cicerone.dev`)

| Type | Name | Value |
| --- | --- | --- |
| `A` | `@` | `185.199.108.153` |
| `A` | `@` | `185.199.109.153` |
| `A` | `@` | `185.199.110.153` |
| `A` | `@` | `185.199.111.153` |
| `AAAA` | `@` | `2606:50c0:8000::153` |
| `AAAA` | `@` | `2606:50c0:8001::153` |
| `AAAA` | `@` | `2606:50c0:8002::153` |
| `AAAA` | `@` | `2606:50c0:8003::153` |
| `CNAME` | `www` | `torbido-hq.github.io` |

Remove Gandi web-forward / `webredir` records first.

<!-- website/src/content/docs/privacy.md @ 8b9a2fad3909013ac8521bf2bf889560b4c8d8de -->
---
title: Privacy
description: How cicerone.dev handles analytics cookies and Google Consent Mode.
---

cicerone.dev is a static docs site. There are no accounts, checkouts, or server-side sessions.

## Analytics

Google Analytics 4 runs only after you accept the banner. Advertising storage, ad user data, and ad personalization stay denied. Until you choose, or if you reject, Analytics cookies are not set.

Your choice is stored in this browser (`localStorage`, key `cicerone-consent`). Use **Cookie settings** in the footer to change it.

## Other third parties

Pages load IBM Plex from Google Fonts and are served through GitHub Pages and Cloudflare.

<!-- README.md @ 8b9a2fad3909013ac8521bf2bf889560b4c8d8de -->
<img src="https://raw.githubusercontent.com/torbido-hq/cicerone/main/src/cicerone/static/cicerone-logo.svg" alt="Cicerone" width="200">

# Cicerone

[![CI](https://github.com/torbido-hq/cicerone/actions/workflows/ci.yml/badge.svg)](https://github.com/torbido-hq/cicerone/actions/workflows/ci.yml)
[![CodeQL](https://github.com/torbido-hq/cicerone/actions/workflows/codeql.yml/badge.svg)](https://github.com/torbido-hq/cicerone/actions/workflows/codeql.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: Beerware](https://img.shields.io/badge/license-Beerware%20🍺-f28e1c.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/docs-cice...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/website/README.md b/website/README.md
--- a/website/README.md
+++ b/website/README.md
@@ -68,8 +68,8 @@ Serif at ~65ch; chrome stays IBM Plex Sans, dates IBM Plex Mono.
 `docs/**`. Only `main` deploys. Website-only PRs skip Docker lint/pytest;
 the `ci` job still succeeds so a required check is not left pending.
 
-Google Analytics is `G-E38EP8PJSR` in `src/lib/consent.mjs`. Override with
-`PUBLIC_GA_MEASUREMENT_ID` at build time if needed.
+Google Analytics is `G-E38EP8PJSR` in `src/lib/consent.mjs` and loads only after
+Accept. Override with `PUBLIC_GA_MEASUREMENT_ID` at build time if needed.
 
 **One-time:** Settings → Pages → Source = **GitHub Actions**, custom domain
 `cicerone.dev`. DNS notes for Gandi apex records are below.

diff --git a/website/src/content/docs/privacy.md b/website/src/content/docs/privacy.md
--- a/website/src/content/docs/privacy.md
+++ b/website/src/content/docs/privacy.md
@@ -7,7 +7,7 @@ cicerone.dev is a static docs site. There are no accounts, checkouts, or server-
 
 ## Analytics
 
-Google Analytics 4 runs only after you accept the banner. Advertising storage, ad user data, and ad personalization stay denied. Until you choose, or if you reject, Analytics cookies are not set.
+Google Analytics 4 runs only after you accept the banner. Advertising storage, ad user data, and ad personalization stay denied. Until you choose, or if you reject, the Google tag is not loaded and Analytics cookies are not set.
 
 Your choice is stored in this browser (`localStorage`, key `cicerone-consent`). Use **Cookie settings** in the footer to change it.
```

Audit context only — docs after excerpt:

```markdown
<!-- website/README.md @ 868c613957a116f7080fde01d226cae067089a94 -->
# Cicerone website (Astro Starlight)

Docs site for [cicerone.dev](https://cicerone.dev). Built with
[Starlight](https://starlight.astro.build/); markdown under repo `docs/` is
synced into the Starlight content collection at build time. Articles are the
same static build (no CMS): posts live under `src/content/docs/articles/`.
With no published post, the articles plugin is off — no header link, RSS, or
`/articles/` route.

## Commands

```sh
cd website
npm ci
npm run dev      # sync docs/ + local preview
npm run build    # sync docs/ + production build → dist/
npm run preview  # serve dist/
```

## Layout

| Path | Role |
| --- | --- |
| `src/content/docs/index.mdx` | Landing (Starlight splash) |
| `src/content/docs/articles/` | Articles (`title` + `date` frontmatter) → `/articles/` |
| `scripts/sync-docs.mjs` | Copies `../docs/*.md` → `src/content/docs/` with frontmatter |
| `astro.config.mjs` | Site URL, sidebar, logo, social, articles plugin |
| `src/lib/consent.mjs` | Cookie banner + Consent Mode v2 (`G-E38EP8PJSR`) |
| `public/CNAME` | Custom domain (`cicerone.dev`) |
| `public/images/` | Site diagrams (`flow.svg`) |
| `public/images/docs/` | Copied from `../docs/images/` at build time (gitignored) |

Generated `src/content/docs/how-it-works.md`, `tutorial.md`,
`architecture.md`, `incremental-events.md`, `src/generated/latest-release.json`,
and `public/images/docs/` are gitignored; they are created at build/dev time. CI and local builds always
sync from `docs/`. Articles are **not** synced from `docs/` — add Markdown
under `src/content/docs/articles/` (see below).

## Articles

Jekyll-style: a `.md` file with YAML frontmatter, HTML at build time, nothing
dynamic. Author globally is `nicholas` (`astro.config.mjs`). Until a
non-draft post exists, Articles is omitted from the build.

```md
---
title: Post title
description: One-line summary for search results and Open Graph.
date: 2026-08-19
excerpt: Listing blurb (falls back to description / body).
authors:
  - nicholas
---

Body…
```

Drafts (`draft: true`, or YAML 1.1 `yes` / `on`) are omitted from
production builds; `astro dev` still loads them so `/articles/` can be
previewed. Frontmatter is parsed as YAML. RSS is
`/articles/rss.xml` once a post is published. Article pages use IBM Plex
Serif at ~65ch; chrome stays IBM Plex Sans, dates IBM Plex Mono.

## Publishing

[`.github/workflows/pages.yml`](../.github/workflows/pages.yml) builds
`website/` on PRs and on pushes to `main` that touch `website/**` or
`docs/**`. Only `main` deploys. Website-only PRs skip Docker lint/pytest;
the `ci` job still succeeds so a required check is not left pending.

Google Analytics is `G-E38EP8PJSR` in `src/lib/consent.mjs` and loads only after
Accept. Override with `PUBLIC_GA_MEASUREMENT_ID` at build time if needed.

**One-time:** Settings → Pages → Source = **GitHub Actions**, custom domain
`cicerone.dev`. DNS notes for Gandi apex records are below.

### DNS (apex `cicerone.dev`)

| Type | Name | Value |
| --- | --- | --- |
| `A` | `@` | `185.199.108.153` |
| `A` | `@` | `185.199.109.153` |
| `A` | `@` | `185.199.110.153` |
| `A` | `@` | `185.199.111.153` |
| `AAAA` | `@` | `2606:50c0:8000::153` |
| `AAAA` | `@` | `2606:50c0:8001::153` |
| `AAAA` | `@` | `2606:50c0:8002::153` |
| `AAAA` | `@` | `2606:50c0:8003::153` |
| `CNAME` | `www` | `torbido-hq.github.io` |

Remove Gandi web-forward / `webredir` records first.

<!-- website/src/content/docs/privacy.md @ 868c613957a116f7080fde01d226cae067089a94 -->
---
title: Privacy
description: How cicerone.dev handles analytics cookies and Google Consent Mode.
---

cicerone.dev is a static docs site. There are no accounts, checkouts, or server-side sessions.

## Analytics

Google Analytics 4 runs only after you accept the banner. Advertising storage, ad user data, and ad personalization stay denied. Until you choose, or if you reject, the Google tag is not loaded and Analytics cookies are not set.

Your choice is stored in this browser (`localStorage`, key `cicerone-consent`). Use **Cookie settings** in the footer to change it.

## Other third parties

Pages load IBM Plex from Google Fonts and are served through GitHub Pages and Cloudflare.

<!-- README.md @ 868c613957a116f7080fde01d226cae067089a94 -->
<img src="https://raw.githubusercontent.com/torbido-hq/cicerone/main/src/cicerone/static/cicerone-logo.svg" alt="Cicerone" width="200">

# Cicerone

[![CI](https://github.com/torbido-hq/cicerone/actions/workflows/ci.yml/badge.svg)](https://github.com/torbido-hq/cicerone/actions/workflows/ci.yml)
[![CodeQL](https://github.com/torbido-hq/cicerone/actions/workflows/codeql.yml/badge.svg)](https://github.com/torbido-hq/cicerone/actions/workflows/codeql.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: Beerware](https://img.shields.io/badge/license-Beerware%20🍺-f28e1c.svg)](LIC...
```

### `GH-CAND-0028`

- Source URL: https://github.com/torbido-hq/cicerone/pull/107
- Repository: `torbido-hq/cicerone`
- PR number: `107`
- PR title: Add custom consent banner and Consent Mode v2 on cicerone.dev
- Language: `python`
- Code changed files: `['.github/workflows/pages.yml', 'website/src/env.d.ts']`
- Docs changed files: `['website/README.md', 'website/src/content/docs/privacy.md']`

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
diff --git a/.github/workflows/pages.yml b/.github/workflows/pages.yml
--- a/.github/workflows/pages.yml
+++ b/.github/workflows/pages.yml
@@ -39,6 +39,8 @@ jobs:
 
       - name: Install and build
         working-directory: website
+        env:
+          PUBLIC_GA_MEASUREMENT_ID: ${{ vars.PUBLIC_GA_MEASUREMENT_ID }}
         run: |
           npm ci
           npm test

diff --git a/website/src/env.d.ts b/website/src/env.d.ts
--- a/website/src/env.d.ts
+++ b/website/src/env.d.ts
@@ -0,0 +1,10 @@
+/// <reference types="astro/client" />
+
+interface Window {
+	gtag?: (...args: unknown[]) => void;
+	dataLayer?: unknown[];
+}
+
+interface ImportMetaEnv {
+	readonly PUBLIC_GA_MEASUREMENT_ID?: string;
+}
```

Allowed model input — docs before excerpt:

```markdown
<!-- website/README.md @ 9a387b565aa94de4e85e0d8296a211ec92a98367 -->
# Cicerone website (Astro Starlight)

Docs site for [cicerone.dev](https://cicerone.dev). Built with
[Starlight](https://starlight.astro.build/); markdown under repo `docs/` is
synced into the Starlight content collection at build time. Articles are the
same static build (no CMS): posts live under `src/content/docs/articles/`.
With no published post, the articles plugin is off — no header link, RSS, or
`/articles/` route.

## Commands

```sh
cd website
npm ci
npm run dev      # sync docs/ + local preview
npm run build    # sync docs/ + production build → dist/
npm run preview  # serve dist/
```

## Layout

| Path | Role |
| --- | --- |
| `src/content/docs/index.mdx` | Landing (Starlight splash) |
| `src/content/docs/articles/` | Articles (`title` + `date` frontmatter) → `/articles/` |
| `scripts/sync-docs.mjs` | Copies `../docs/*.md` → `src/content/docs/` with frontmatter |
| `astro.config.mjs` | Site URL, sidebar, logo, social, articles plugin |
| `public/CNAME` | Custom domain (`cicerone.dev`) |
| `public/images/` | Site diagrams (`flow.svg`) |
| `public/images/docs/` | Copied from `../docs/images/` at build time (gitignored) |

Generated `src/content/docs/how-it-works.md`, `tutorial.md`,
`architecture.md`, `incremental-events.md`, `src/generated/latest-release.json`,
and `public/images/docs/` are gitignored; they are created at build/dev time. CI and local builds always
sync from `docs/`. Articles are **not** synced from `docs/` — add Markdown
under `src/content/docs/articles/` (see below).

## Articles

Jekyll-style: a `.md` file with YAML frontmatter, HTML at build time, nothing
dynamic. Author globally is `nicholas` (`astro.config.mjs`). Until a
non-draft post exists, Articles is omitted from the build.

```md
---
title: Post title
description: One-line summary for search results and Open Graph.
date: 2026-08-19
excerpt: Listing blurb (falls back to description / body).
authors:
  - nicholas
---

Body…
```

Drafts (`draft: true`, or YAML 1.1 `yes` / `on`) are omitted from
production builds; `astro dev` still loads them so `/articles/` can be
previewed. Frontmatter is parsed as YAML. RSS is
`/articles/rss.xml` once a post is published. Article pages use IBM Plex
Serif at ~65ch; chrome stays IBM Plex Sans, dates IBM Plex Mono.

## Publishing

[`.github/workflows/pages.yml`](../.github/workflows/pages.yml) builds
`website/` on PRs and on pushes to `main` that touch `website/**` or
`docs/**`. Only `main` deploys. Website-only PRs skip Docker lint/pytest;
the `ci` job still succeeds so a required check is not left pending.

**One-time:** Settings → Pages → Source = **GitHub Actions**, custom domain
`cicerone.dev`. DNS notes for Gandi apex records are below.

### DNS (apex `cicerone.dev`)

| Type | Name | Value |
| --- | --- | --- |
| `A` | `@` | `185.199.108.153` |
| `A` | `@` | `185.199.109.153` |
| `A` | `@` | `185.199.110.153` |
| `A` | `@` | `185.199.111.153` |
| `AAAA` | `@` | `2606:50c0:8000::153` |
| `AAAA` | `@` | `2606:50c0:8001::153` |
| `AAAA` | `@` | `2606:50c0:8002::153` |
| `AAAA` | `@` | `2606:50c0:8003::153` |
| `CNAME` | `www` | `torbido-hq.github.io` |

Remove Gandi web-forward / `webredir` records first.

<!-- README.md @ 9a387b565aa94de4e85e0d8296a211ec92a98367 -->
<img src="https://raw.githubusercontent.com/torbido-hq/cicerone/main/src/cicerone/static/cicerone-logo.svg" alt="Cicerone" width="200">

# Cicerone

[![CI](https://github.com/torbido-hq/cicerone/actions/workflows/ci.yml/badge.svg)](https://github.com/torbido-hq/cicerone/actions/workflows/ci.yml)
[![CodeQL](https://github.com/torbido-hq/cicerone/actions/workflows/codeql.yml/badge.svg)](https://github.com/torbido-hq/cicerone/actions/workflows/codeql.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: Beerware](https://img.shields.io/badge/license-Beerware%20🍺-f28e1c.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/docs-cicerone.dev-004B75.svg)](https://cicerone.dev)
[![PyPI](https://img.shields.io/pypi/v/cicerone-recommender.svg)](https://pypi.org/project/cicerone-recommender/)

**Site:** [cicerone.dev](https://cicerone.dev)
([Starlight](https://starlight.astro.build/) docs site; source in [`website/`](website/),
guides synced from [`docs/`](docs/). [Articles](https://cicerone.dev/articles/).)

A generic, self-hosted batch recommender system. It reads your interaction
data, trains a hybrid [rectools](https://github.com/MobileTeleSystems/RecTools)
+ LightFM model (optional item-KNN, SASRec/BERT4Rec, popular/latest), and
writes out top-K recommendations per user. An optional lightweight "serve"
mode can then expose those precomputed recommendations over a small
read-only HTTP API — there's still no live inference, no model loaded in the
request path. Optional `[events]` ingest can refresh popular/latest rows
between full retrains; that is still write-through,...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/website/README.md b/website/README.md
--- a/website/README.md
+++ b/website/README.md
@@ -25,6 +25,7 @@ npm run preview  # serve dist/
 | `src/content/docs/articles/` | Articles (`title` + `date` frontmatter) → `/articles/` |
 | `scripts/sync-docs.mjs` | Copies `../docs/*.md` → `src/content/docs/` with frontmatter |
 | `astro.config.mjs` | Site URL, sidebar, logo, social, articles plugin |
+| `src/lib/consent.mjs` | Cookie banner + Consent Mode v2 (`G-E38EP8PJSR`) |
 | `public/CNAME` | Custom domain (`cicerone.dev`) |
 | `public/images/` | Site diagrams (`flow.svg`) |
 | `public/images/docs/` | Copied from `../docs/images/` at build time (gitignored) |
@@ -67,6 +68,9 @@ Serif at ~65ch; chrome stays IBM Plex Sans, dates IBM Plex Mono.
 `docs/**`. Only `main` deploys. Website-only PRs skip Docker lint/pytest;
 the `ci` job still succeeds so a required check is not left pending.
 
+Google Analytics is `G-E38EP8PJSR` in `src/lib/consent.mjs`. Override with
+`PUBLIC_GA_MEASUREMENT_ID` at build time if needed.
+
 **One-time:** Settings → Pages → Source = **GitHub Actions**, custom domain
 `cicerone.dev`. DNS notes for Gandi apex records are below.

diff --git a/website/src/content/docs/privacy.md b/website/src/content/docs/privacy.md
--- a/website/src/content/docs/privacy.md
+++ b/website/src/content/docs/privacy.md
@@ -0,0 +1,16 @@
+---
+title: Privacy
+description: How cicerone.dev handles analytics cookies and Google Consent Mode.
+---
+
+cicerone.dev is a static docs site. There are no accounts, checkouts, or server-side sessions.
+
+## Analytics
+
+Google Analytics 4 runs only after you accept the banner. Advertising storage, ad user data, and ad personalization stay denied. Until you choose, or if you reject, Analytics cookies are not set.
+
+Your choice is stored in this browser (`localStorage`, key `cicerone-consent`). Use **Cookie settings** in the footer to change it.
+
+## Other third parties
+
+Pages load IBM Plex from Google Fonts and are served through GitHub Pages and Cloudflare.
```

Audit context only — docs after excerpt:

```markdown
<!-- website/README.md @ a036b540a9cb2957d51c2a7d114f8223b54fc602 -->
# Cicerone website (Astro Starlight)

Docs site for [cicerone.dev](https://cicerone.dev). Built with
[Starlight](https://starlight.astro.build/); markdown under repo `docs/` is
synced into the Starlight content collection at build time. Articles are the
same static build (no CMS): posts live under `src/content/docs/articles/`.
With no published post, the articles plugin is off — no header link, RSS, or
`/articles/` route.

## Commands

```sh
cd website
npm ci
npm run dev      # sync docs/ + local preview
npm run build    # sync docs/ + production build → dist/
npm run preview  # serve dist/
```

## Layout

| Path | Role |
| --- | --- |
| `src/content/docs/index.mdx` | Landing (Starlight splash) |
| `src/content/docs/articles/` | Articles (`title` + `date` frontmatter) → `/articles/` |
| `scripts/sync-docs.mjs` | Copies `../docs/*.md` → `src/content/docs/` with frontmatter |
| `astro.config.mjs` | Site URL, sidebar, logo, social, articles plugin |
| `src/lib/consent.mjs` | Cookie banner + Consent Mode v2 (`G-E38EP8PJSR`) |
| `public/CNAME` | Custom domain (`cicerone.dev`) |
| `public/images/` | Site diagrams (`flow.svg`) |
| `public/images/docs/` | Copied from `../docs/images/` at build time (gitignored) |

Generated `src/content/docs/how-it-works.md`, `tutorial.md`,
`architecture.md`, `incremental-events.md`, `src/generated/latest-release.json`,
and `public/images/docs/` are gitignored; they are created at build/dev time. CI and local builds always
sync from `docs/`. Articles are **not** synced from `docs/` — add Markdown
under `src/content/docs/articles/` (see below).

## Articles

Jekyll-style: a `.md` file with YAML frontmatter, HTML at build time, nothing
dynamic. Author globally is `nicholas` (`astro.config.mjs`). Until a
non-draft post exists, Articles is omitted from the build.

```md
---
title: Post title
description: One-line summary for search results and Open Graph.
date: 2026-08-19
excerpt: Listing blurb (falls back to description / body).
authors:
  - nicholas
---

Body…
```

Drafts (`draft: true`, or YAML 1.1 `yes` / `on`) are omitted from
production builds; `astro dev` still loads them so `/articles/` can be
previewed. Frontmatter is parsed as YAML. RSS is
`/articles/rss.xml` once a post is published. Article pages use IBM Plex
Serif at ~65ch; chrome stays IBM Plex Sans, dates IBM Plex Mono.

## Publishing

[`.github/workflows/pages.yml`](../.github/workflows/pages.yml) builds
`website/` on PRs and on pushes to `main` that touch `website/**` or
`docs/**`. Only `main` deploys. Website-only PRs skip Docker lint/pytest;
the `ci` job still succeeds so a required check is not left pending.

Google Analytics is `G-E38EP8PJSR` in `src/lib/consent.mjs`. Override with
`PUBLIC_GA_MEASUREMENT_ID` at build time if needed.

**One-time:** Settings → Pages → Source = **GitHub Actions**, custom domain
`cicerone.dev`. DNS notes for Gandi apex records are below.

### DNS (apex `cicerone.dev`)

| Type | Name | Value |
| --- | --- | --- |
| `A` | `@` | `185.199.108.153` |
| `A` | `@` | `185.199.109.153` |
| `A` | `@` | `185.199.110.153` |
| `A` | `@` | `185.199.111.153` |
| `AAAA` | `@` | `2606:50c0:8000::153` |
| `AAAA` | `@` | `2606:50c0:8001::153` |
| `AAAA` | `@` | `2606:50c0:8002::153` |
| `AAAA` | `@` | `2606:50c0:8003::153` |
| `CNAME` | `www` | `torbido-hq.github.io` |

Remove Gandi web-forward / `webredir` records first.

<!-- website/src/content/docs/privacy.md @ a036b540a9cb2957d51c2a7d114f8223b54fc602 -->
---
title: Privacy
description: How cicerone.dev handles analytics cookies and Google Consent Mode.
---

cicerone.dev is a static docs site. There are no accounts, checkouts, or server-side sessions.

## Analytics

Google Analytics 4 runs only after you accept the banner. Advertising storage, ad user data, and ad personalization stay denied. Until you choose, or if you reject, Analytics cookies are not set.

Your choice is stored in this browser (`localStorage`, key `cicerone-consent`). Use **Cookie settings** in the footer to change it.

## Other third parties

Pages load IBM Plex from Google Fonts and are served through GitHub Pages and Cloudflare.

<!-- README.md @ a036b540a9cb2957d51c2a7d114f8223b54fc602 -->
<img src="https://raw.githubusercontent.com/torbido-hq/cicerone/main/src/cicerone/static/cicerone-logo.svg" alt="Cicerone" width="200">

# Cicerone

[![CI](https://github.com/torbido-hq/cicerone/actions/workflows/ci.yml/badge.svg)](https://github.com/torbido-hq/cicerone/actions/workflows/ci.yml)
[![CodeQL](https://github.com/torbido-hq/cicerone/actions/workflows/codeql.yml/badge.svg)](https://github.com/torbido-hq/cicerone/actions/workflows/codeql.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: Beerware](https://img.shields.io/badge/license-Beerware%20🍺-f28e1c.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/docs-cice...
```

### `GH-CAND-0029`

- Source URL: https://github.com/torbido-hq/cicerone/pull/97
- Repository: `torbido-hq/cicerone`
- PR number: `97`
- PR title: Add PyPI package and cicerone CLI
- Language: `python`
- Code changed files: `['.github/workflows/ci.yml', '.github/workflows/publish.yml', 'config/cicerone.dashboard.toml', 'config/cicerone.serve.toml', 'docker-compose.yml', 'docker/Dockerfile', 'pyproject.toml', 'src/cicerone/__main__.py', 'src/cicerone/cli.py', 'src/cicerone/dashboard.py', 'src/cicerone/dashboard_users.py', 'src/cicerone/export_serve_openapi.py', 'src/cicerone/manage_dashboard_users.py', 'src/cicerone/packaging.py', 'src/cicerone/serve/app.py', 'tests/test_cli.py', 'tests/test_packaging.py', 'tests/test_serve_openapi_client.py']`
- Docs changed files: `['CHANGELOG.md', 'CONTRIBUTING.md', 'README.md', 'docs/architecture.md', 'docs/tutorial.md']`

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
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -46,6 +46,9 @@ jobs:
       - name: pip-audit (dependency vulnerability scan)
         run: docker run --rm cicerone-test pip-audit -r requirements.txt -r requirements-dev.txt
 
+      - name: Build sdist and wheel
+        run: docker build --target package -t cicerone-package -f docker/Dockerfile .
+
   test:
     needs: scope
     if: needs.scope.outputs.python == 'true'

diff --git a/.github/workflows/publish.yml b/.github/workflows/publish.yml
--- a/.github/workflows/publish.yml
+++ b/.github/workflows/publish.yml
@@ -0,0 +1,50 @@
+name: Publish to PyPI
+
+# Uploads sdist + wheel when a GitHub release is published.
+# One-time: GitHub Environment `pypi`, and a PyPI trusted publisher for
+# `cicerone-recommender` (repo torbido-hq/cicerone, workflow publish.yml,
+# environment pypi). The PyPI name `cicerone` is a different project.
+
+on:
+  release:
+    types: [published]
+  workflow_dispatch:
+
+permissions:
+  contents: read
+
+jobs:
+  build:
+    runs-on: ubuntu-latest
+    steps:
+      - uses: actions/checkout@v7
+
+      - name: Build sdist and wheel
+        run: docker build --target package -t cicerone-package -f docker/Dockerfile .
+
+      - name: Extract dist/
+        run: |
+          cid="$(docker create cicerone-package)"
+          docker cp "$cid":/app/dist dist
+          docker rm "$cid"
+
+      - uses: actions/upload-artifact@v4
+        with:
+          name: python-package-distributions
+          path: dist/
+
+  publish:
+    needs: build
+    runs-on: ubuntu-latest
+    environment:
+      name: pypi
+      url: https://pypi.org/p/cicerone-recommender
+    permissions:
+      id-token: write
+    steps:
+      - uses: actions/download-artifact@v4
+        with:
+          name: python-package-distributions
+          path: dist/
+
+      - uses: pypa/gh-action-pypi-publish@release/v1

diff --git a/config/cicerone.dashboard.toml b/config/cicerone.dashboard.toml
--- a/config/cicerone.dashboard.toml
+++ b/config/cicerone.dashboard.toml
@@ -1,9 +1,9 @@
 # Example "dashboard" configuration -- a small read-only status page over
 # the job run history the batch job already writes (job runs on cron, see
 # config/cicerone.toml). Deploy it as a separate container from the same
-# image, pointed at this file via CICERONE_CONFIG_PATH (see the "dashboard"
-# service in docker-compose.yml). Always its own process
-# (`python -m cicerone.dashboard`), independent of [job].mode -- it never
+# image, pointed at this file via `--config` / CICERONE_CONFIG_PATH (see the
+# "dashboard" service in docker-compose.yml). Always its own process
+# (`cicerone dashboard`), independent of [job].mode -- it never
 # imports cicerone.model/dataset/automl (no rectools/lightfm/implicit
 # needed here), same as serve mode.
 #
@@ -27,7 +27,7 @@ enabled = true
 host = "0.0.0.0"
 port = 8090
 # HTTP Basic Auth users (username -> bcrypt hash), managed with:
-#   docker compose run --rm dashboard python -m cicerone.manage_dashboard_users add <username>
+#   docker compose run --rm dashboard users add <username>
 # Meant for a handful of named people, not machine-to-machine access
 # (compare to [serve].auth_token / [job.trigger].auth_token, a single
 # shared bearer token for that use case).

diff --git a/config/cicerone.serve.toml b/config/cicerone.serve.toml
--- a/config/cicerone.serve.toml
+++ b/config/cicerone.serve.toml
@@ -2,7 +2,7 @@
 # that only exposes the read API (cicerone.serve) over the recommendations
 # the batch job (using config/cicerone.toml) already wrote out. Deploy it
 # as a separate container from the same image, pointed at this file via
-# CICERONE_CONFIG_PATH (see the "serve" service in docker-compose.yml).
+# `--config` / CICERONE_CONFIG_PATH (see the "serve" service in docker-compose.yml).
 #
 # [output] here MUST point at the exact same store the batch job writes to
 # -- everything else in this file is independent of the batch config.

diff --git a/docker-compose.yml b/docker-compose.yml
--- a/docker-compose.yml
+++ b/docker-compose.yml
@@ -21,8 +21,7 @@ version: "3.9"
 #   dashboard   — a small status page over job run history
 #                 (config/cicerone.dashboard.toml). Optional: comment it out
 #                 if you don't need it. Manage its login users with:
-#                   docker compose run --rm dashboard \
-#                     python -m cicerone.manage_dashboard_users add <username>
+#                   docker compose run --rm dashboard users add <username>
 #
 # Postgres is opt-in via --profile db so a host already using :5432 (or an
 # S3/dataset-only setup) can still `docker compose up` without waiting on DB.
@@ -79,6 +78,7 @@ services:
 
       # Only used if config/cicerone.toml sets [job.trigger].enabled = true.
       TRIGGER_AUTH_TOKEN: ${TRIGGER_AUTH_TOKEN:-}
+    command: ["start", "--config", "/app/config/cicerone.toml"]
     ports:
       - "8080:8080" # only listens if [job.trigger].enabled = true
     volumes:
@@ -101,6 +101,7 @@ services:
       # Unset by default — set in .env when serve reads a kind = "db" output.
       OUTPUT_DATABASE_URL: ${OUTPUT_DATABASE_URL:-}
       SERVE_AUTH_TOKEN: ${SERVE_AUTH_TOKEN:-}
+    command: ["start", "--config", "/app/config/cicerone.serve.toml"]
     ports:
       - "8000:8000"
     volumes:
@@ -111,7 +112,6 @@ services:
     build:
       context: .
       dockerfile: docker/Dockerfile
-    entrypoint: ["python", "-m", "cicerone.dashboard"]
     environment:
       PYTHONUNBUFFERED: "1"
       TZ: "Europe/Rome"
@@ -123,13 +123,13 @@ services:
       OUTPUT_S3_BUCKET: ${OUTPUT_S3_BUCKET:-}
       # Unset by default — set in .env when the dashboard reads a kind = "db" output.
       OUTPUT_DATABASE_URL: ${OUTPUT_DATABASE_URL:-}
+    command: ["dashboard", "--config", "/app/config/cicerone.dashboard.toml"]
     ports:
       - "8090:8090"
     volumes:
-      # Read-write (unlike recommender/serve above): `manage_dashboard_users`
-      # (run via `docker compose run --rm dashboard python -m
-      # cicerone.manage_dashboard_users add <username>`) writes
-      # config/dashboard_users.toml here.
+      # Read-write (unlike recommender/serve above): `cicerone users`
+      # (run via `docker compose run --rm dashboard users add <username>`)
+      # writes config/dashboard_users.toml here.
       - ./config:/app/config
     restart: unless-stopped

diff --git a/docker/Dockerfile b/docker/Dockerfile
--- a/docker/Dockerfile
+++ b/docker/Dockerfile
@@ -40,6 +40,23 @@ COPY src/cicerone/static/dashboard.js ./src/cicerone/static/dashboard.js
 COPY src/cicerone/static/tailwind.input.css ./tailwind.input.css
 RUN npx tailwindcss -i ./tailwind.input.css -o ./tailwind.css --minify
 
+# --- package ---------------------------------------------------------------
+# sdist + wheel for PyPI and the runtime image. Reuses the frontend CSS
+# artifact; does not install the ML stack.
+FROM python:3.11-slim-bookworm AS package
+
+WORKDIR /app
+RUN pip install --no-cache-dir build==1.5.0 twine==7.0.0
+
+COPY pyproject.toml MANIFEST.in LICENSE README.md CHANGELOG.md ./
+COPY requirements.txt requirements-redis.txt requirements-sequential.txt ./
+COPY src/ ./src/
+COPY --from=frontend /build/tailwind.css ./src/cicerone/static/tailwind.css
+
+RUN python -m build \
+    && python -m twine check dist/* \
+    && PYTHONPATH=src python -m cicerone.packaging
+
 # --- runtime -----------------------------------------------------------------
 FROM python:3.11-slim-bookworm AS runtime
 
@@ -55,33 +72,27 @@ RUN groupadd --gid 1000 cicerone && \
 WORKDIR /app
 
 COPY --from=builder /wheels /wheels
+COPY --from=package /app/dist /dist
 COPY requirements.txt ./
 RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
-    && rm -rf /wheels
+    && pip install --no-cache-dir --no-index --find-links=/dist cicerone-recommender \
+    && rm -rf /wheels /dist \
+    && cicerone --help >/dev/null
 
-COPY src/ ./src/
-COPY --from=frontend /build/tailwind.css ./src/cicerone/static/tailwind.css
 COPY config/ ./config/
-COPY docker/entrypoint.sh ./docker/entrypoint.sh
-RUN chmod +x ./docker/entrypoint.sh
 
-ENV PYTHONPATH=/app/src \
-    PYTHONDONTWRITEBYTECODE=1 \
+ENV PYTHONDONTWRITEBYTECODE=1 \
     PYTHONUNBUFFERED=1
 
 RUN mkdir -p /tmp/cicerone && chown -R cicerone:cicerone /app /tmp/cicerone
 USER cicerone
 
-# Batch mode (default): no HTTP surface, just a scheduled job (R2 in ->
-# train -> R2 out), plus an optional event-driven trigger listener on 8080
-# (see [job.trigger] in cicerone.toml). Serve mode (job.mode = "serve")
-# instead exposes the read API on 8000. entrypoint.sh picks the right one
-# based on the loaded config. The dashboard (cicerone.dashboard, port 8090)
-# is always its own separate entrypoint/container -- see the "dashboard"
-# service in docker-compose.yml, which overrides ENTRYPOINT di...
```

Allowed model input — docs before excerpt:

```markdown
<!-- CHANGELOG.md @ cc82eb89bba772e34e3452f90cd1d81165a98476 -->
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Dashboard user lookup: inspect a `user_id`'s current precomputed top-K
  (rank, item, score, source, optional category) from the job output store,
  with cold-start fallback, on the Basic-Auth status page.
  `GET /dashboard?user_id=` fills the lookup on load.

- Optional project-site articles at `/articles/` (static Markdown under
  `website/src/content/docs/articles/`). No nav, RSS, or index until a
  published post exists. Article pages use IBM Plex Serif and a ~65ch
  measure. Brand accents invert for dark theme. Listing keeps an h1;
  posts use `description` for meta. Website-only PRs skip Docker lint/test
  jobs; the `ci` job still succeeds.

- Optional **sequential** strategy (`SASRecModel` / `BERT4RecModel`) via
  `[model.sequential]` (`architecture = "sasrec"` or `"bert4rec"`). Requires
  `pip install -r requirements-sequential.txt` (`rectools[torch]`); serve
  mode never imports torch. AutoML drops it from the candidate pool when
  the extra is missing or median distinct items/user is below
  `[job.sequential].min_median_interactions` (default 5), and logs the skip.

- Incremental events horizontal HA: leader-only apply lease
  (`{lock_key}:events:apply`) when `events.ha = true` with
  `job.trigger.lock_backend` postgres/redis. Fan-out sources acquire the
  lease only when a micro-batch is ready. Metrics:
  `cicerone_events_lock_total`, `cicerone_events_leader`,
  `cicerone_events_apply_busy_total`.

- Redis Streams EventSource (`events.kind = "redis_streams"`): consumer-group
  poll via `XREADGROUP` / `XACK`, idle PEL recovery with `XAUTOCLAIM`, and
  stream entry id fallback when `event_id` is omitted. Requires
  `requirements-redis.txt` (same optional `redis` pin as the lock backend).
- User-scoped incremental write-through: load/replace only affected users
  (plus `__cold_start__`) via `OutputSink.replace_recommendations_for_users`
  (returns post-write distinct user count) instead of full-frame overwrite.
  Updater keeps an LRU-bounded per-user cache (default 2048); dataset
  `count_recommendation_users` projects only `user_id` from parquet, and
  `load_recommendations_for_users` uses parquet `filters` for `user_id` when
  the engine supports predicate pushdown.
- Incremental events Prometheus metrics on serve `/metrics` (source lag /
  connected, flush counters, last success timestamp, tick errors) and an
  incremental-events panel on the Basic-Auth dashboard (from manifests).
- Incremental events between full retrains: internal `EventSource` surface,
  webhook `POST /events`, micro-batch buffer/worker, and write-through
  updater for popular/latest slices (`[events]` config). Design:
  `docs/incremental-events.md`. Webhook `occurred_at` requires an explicit
  timezone (`Z` / offset) or Unix epoch seconds (UTC).
- DB event source (`events.kind = "db"`): watermark poll over
  `events_table` / `events_query`, durable optional `watermark_path`,
  watermark advances only on successful flush ack.
- S3-compatible event source (`events.kind = "s3"`), R2-first: list/marker
  poll via the same `build_s3_client` / `endpoint_url` options as dataset
  I/O; optional AWS-only SQS mode (rejected with `endpoint_url`). JSON
  object/array payloads; ack advances marker or deletes the SQS message.

### Changed

- Parse article `draft` from YAML frontmatter; article layout CSS keys off
  `data-cicerone-articles` rather than starlight-blog class names.
- Share the articles URL prefix between the Starlight plugin and layout
  classifier; `robots.txt` allows the site and disallows `/pagefind/`.
- Article plugin gating passes `{ production }` explicitly; layout kind
  matches starlight-blog listing routes and ignores a missing route id.
- Drop the Starlight “Edit page” footer; site content is edited in git.
- README and docs-site dashboard screenshot include the user recommendation lookup.
- Docs site copies `docs/images/` into `website/public/images/docs/` at build time.
- Dashboard lookup form is labeled, results are announced, and job-run
  tables expose captions / column headers; helper text contrast is higher.
- Dashboard inspector k is `min(job.top_k, dashboard.lookup_k)` (default 20).

- Bump `pyarrow` 25.0.0 → 25.0.1 (#85), `SQLAlchemy` 2.0.51 → 2.0.52 (#86),
  `uvicorn` 0.52.1 → 0.52.3 (#87), `ruff` 0.16.2 → 0.16.3 (#88).
- Bump GitHub Actions Pages deploy helpers: `actions/upload-pages-artifact`
  v3 → v5 (Dependabot #79), `actions/deploy-pages` v4 → v5 (#80).
- Bump `fastapi` 0.140.13 → 0.141.1 (Dependabot #69).
- Dependabot: ignore `numpy` major bumps (Python 3.11 CI) and `boto3>=1.43.57`
  (aiobotocore botocore pin).
- Project docs site (not part of the runtime product): Starlight under
  `website/`, synced from `docs/`, published at [cicerone.dev](...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/CHANGELOG.md b/CHANGELOG.md
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -12,6 +12,13 @@ The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
   (rank, item, score, source, optional category) from the job output store,
   with cold-start fallback, on the Basic-Auth status page.
   `GET /dashboard?user_id=` fills the lookup on load.
+- PyPI distribution `cicerone-recommender` (`import cicerone`; the name
+  `cicerone` is taken). Wheel includes compiled dashboard CSS. A GitHub
+  Release publishes via trusted publishing (`.github/workflows/publish.yml`).
+- `cicerone` CLI (`start`/`job`/`serve`/`dashboard`/`scheduler`/`users`) with
+  `--config` for a TOML path, plus `--log-level` / `--log-format` (or
+  `CICERONE_LOG_LEVEL` / `CICERONE_LOG_FORMAT`). Runtime image pip-installs
+  the wheel; entrypoint is `cicerone start`.
 
 - Optional project-site articles at `/articles/` (static Markdown under
   `website/src/content/docs/articles/`). No nav, RSS, or index until a
@@ -70,6 +77,10 @@ The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
 - Article plugin gating passes `{ production }` explicitly; layout kind
   matches starlight-blog listing routes and ignores a missing route id.
 - Drop the Starlight “Edit page” footer; site content is edited in git.
+- Docker `package` stage validates the wheel via `python -m cicerone.packaging`
+  (selects `cicerone_recommender-<version>` including PEP 440 local versions
+  and numeric wheel build tags).
+
 - README and docs-site dashboard screenshot include the user recommendation lookup.
 - Docs site copies `docs/images/` into `website/public/images/docs/` at build time.
 - Dashboard lookup form is labeled, results are announced, and job-run
@@ -88,6 +99,10 @@ The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
 
 ### Fixed
 
+- `cicerone users` with a config path requires enabled `dashboard.users_path`
+  (or an explicit `--users-path`); the error names the loaded config and the
+  dashboard settings that were resolved.
+
 - Dashboard still starts if the recommendation store cannot be opened (lookup disabled).
 - Dashboard lookup errors show a generic message; details stay in the logs.
 - Dashboard lookup URL updates keep the hash fragment.

diff --git a/CONTRIBUTING.md b/CONTRIBUTING.md
--- a/CONTRIBUTING.md
+++ b/CONTRIBUTING.md
@@ -134,7 +134,7 @@ client in sync:
 
 ```sh
 docker run --rm -v "$PWD":/app -w /app -e PYTHONPATH=/app/src cicerone-test \
-  python -m cicerone.export_serve_openapi -o docs/openapi/serve.openapi.json
+  cicerone export-openapi -o docs/openapi/serve.openapi.json
 ```
 
 `tests/test_serve_openapi_client.py` asserts the committed file matches
@@ -167,17 +167,27 @@ and/or `examples/serve/` when request/response fields change.
 Do **not** open a follow-up PR that only dates `CHANGELOG.md` — it still
 needs that approval and is pure process drag.
 
-1. On the feature PR that completes the version, change
-   `## [X.Y.Z] - Unreleased` to `## [X.Y.Z] - YYYY-MM-DD` (today's date)
-   in the same branch before merge, and set `cicerone.__version__`
+The PyPI project is **`cicerone-recommender`** (`pip install
+cicerone-recommender`; `import cicerone`). The name `cicerone` is a
+different package.
+
+One-time PyPI setup (before the first upload): create a GitHub Environment
+named `pypi`, then a [pending trusted publisher](https://docs.pypi.org/trusted-publishers/)
+for `cicerone-recommender` — owner `torbido-hq`, repo `cicerone`, workflow
+`publish.yml`, environment `pypi`. No API token.
+
+1. On the feature PR that completes the version, move `## [Unreleased]`
+   notes into `## [X.Y.Z] - YYYY-MM-DD` (today's date) in the same branch
+   before merge, and set `cicerone.__version__`
    (`src/cicerone/__init__.py`) to the same `X.Y.Z` (serve OpenAPI
    metadata uses it via `SERVE_API_VERSION` — regenerate
    `docs/openapi/serve.openapi.json` if the version string changed).
 2. Merge that PR to `main`.
 3. Tag the merge commit: `git tag -a vX.Y.Z <sha> -m "…"` and
    `git push origin vX.Y.Z`.
 4. Publish the GitHub release from that tag (notes can mirror the
-   changelog section).
+   changelog section). `.github/workflows/publish.yml` builds the sdist and
+   wheel (including dashboard CSS) and uploads them to PyPI.
 
 If the version was already tagged while the changelog still said
 Unreleased, fold the date fix into the next real PR — never a dating-only

diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1,4 +1,4 @@
-<img src="src/cicerone/static/cicerone-logo.svg" alt="Cicerone" width="200">
+<img src="https://raw.githubusercontent.com/torbido-hq/cicerone/main/src/cicerone/static/cicerone-logo.svg" alt="Cicerone" width="200">
 
 # Cicerone
 
@@ -7,6 +7,7 @@
 [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
 [![License: Beerware](https://img.shields.io/badge/license-Beerware%20🍺-f28e1c.svg)](LICENSE)
 [![GitHub Pages](https://img.shields.io/badge/docs-cicerone.dev-004B75.svg)](https://cicerone.dev)
+[![PyPI](https://img.shields.io/pypi/v/cicerone-recommender.svg)](https://pypi.org/project/cicerone-recommender/)
 
 **Site:** [cicerone.dev](https://cicerone.dev)
 ([Starlight](https://starlight.astro.build/) docs site; source in [`website/`](website/),
@@ -20,9 +21,9 @@ lightweight "serve" mode can then expose those precomputed recommendations
 over a small read-only HTTP API — there's still no live inference, no
 model loaded in the request path. Optionally (`[job].save_model_artifact`),
 the batch job can also write a versioned fitted-model artifact for offline
-reload / future thin inference without redesigning training. Everything
-runs in Docker (Python 3.11 only lives inside the image, nothing to install
-on the host).
+reload / future thin inference without redesigning training. The supported
+deploy path is Docker (Python 3.11 lives inside the image). A PyPI package
+is also published for Python 3.11 hosts — see Installation.
 
 Cicerone isn't tied to any particular product, shop, or domain — it works
 for any catalog of "users" and "items" with interaction events (purchases,
@@ -78,7 +79,7 @@ at boot, then again on `[job].cron_schedule` in `config/cicerone.toml`
 
 By default (`[job].mode = "batch"`), the container only runs the batch job
 on its cron schedule — no HTTP surface at all. Setting `[job].mode = "serve"`
-switches `python -m cicerone.serve` to instead run a small FastAPI **read**
+switches `cicerone start` / `cicerone serve` to instead run a small FastAPI **read**
 API over the lookup table the batch job already wrote (never loads
 lightfm/rectools/implicit/torch, never trains or imports):
 
@@ -146,7 +147,7 @@ it with:
 
 ```sh
 docker run --rm -v "$PWD":/app -w /app -e PYTHONPATH=/app/src cicerone-test \
-  python -m cicerone.export_serve_openapi -o docs/openapi/serve.openapi.json
+  cicerone export-openapi -o docs/openapi/serve.openapi.json
 ```
 
 Thin clients (no generated SDK package — copy or import as needed). ReDoc
@@ -227,13 +228,14 @@ serve). Like serve mode, it never loads lightfm/rectools/implicit.
   users, not a shared token) with:
 
   ```
-  python -m cicerone.manage_dashboard_users --users-path <path> add <username>
-  python -m cicerone.manage_dashboard_users --users-path <path> remove <username>
-  python -m cicerone.manage_dashboard_users --users-path <path> list
+  cicerone users --users-path <path> add <username>
+  cicerone users --users-path <path> remove <username>
+  cicerone users --users-path <path> list
   ```
 
-  (note `--users-path` comes *before* the subcommand). Passwords are hashed
-  with bcrypt; the file is plain TOML (`username = "<bcrypt hash>"`).
+  (`--users-path` is optional when `--config` points at a dashboard TOML).
+  Passwords are hashed with bcrypt; the file is plain TOML
+  (`username = "<bcrypt hash>"`).
 - Enable it via `[dashboard].enabled = true` in `config/cicerone.toml` (or
   use the standalone `config/cicerone.dashboard.toml` example config). See
   the `dashboard` service in `docker-compose.yml` for how it's wired up
@@ -248,7 +250,8 @@ serve). Like serve mode, it never loads lightfm/rectools/implicit.
 All structural configuration — which backend to use for input/output,
 bucket/table names, scheduling, tuning — lives in one version-controlled
 TOML file, `config/cicerone.toml` (mounted read-only, see
-`docker-compose.yml`; override the path with `CICERONE_CONFIG_PATH`).
+`docker-compose.yml`; override the path with `cicerone --config PATH` or
+`CICERONE_CONFIG_PATH`).
 Secrets are never written into it directly: reference them with
 `${ENV_VAR_NAME}` placeholders, resolved from the environment at load time
 (see [.env.example](.env.example)).
@@ -520,6 +523,35 @@ than one source contributed it. Without blending, users without enough
 interactions still get a fallback list from `PopularModel` (rectools)...
```

Audit context only — docs after excerpt:

```markdown
<!-- CHANGELOG.md @ 60e53eefb5046f07e38528b20a41f2993b60b1b5 -->
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Dashboard user lookup: inspect a `user_id`'s current precomputed top-K
  (rank, item, score, source, optional category) from the job output store,
  with cold-start fallback, on the Basic-Auth status page.
  `GET /dashboard?user_id=` fills the lookup on load.
- PyPI distribution `cicerone-recommender` (`import cicerone`; the name
  `cicerone` is taken). Wheel includes compiled dashboard CSS. A GitHub
  Release publishes via trusted publishing (`.github/workflows/publish.yml`).
- `cicerone` CLI (`start`/`job`/`serve`/`dashboard`/`scheduler`/`users`) with
  `--config` for a TOML path, plus `--log-level` / `--log-format` (or
  `CICERONE_LOG_LEVEL` / `CICERONE_LOG_FORMAT`). Runtime image pip-installs
  the wheel; entrypoint is `cicerone start`.

- Optional project-site articles at `/articles/` (static Markdown under
  `website/src/content/docs/articles/`). No nav, RSS, or index until a
  published post exists. Article pages use IBM Plex Serif and a ~65ch
  measure. Brand accents invert for dark theme. Listing keeps an h1;
  posts use `description` for meta. Website-only PRs skip Docker lint/test
  jobs; the `ci` job still succeeds.

- Optional **sequential** strategy (`SASRecModel` / `BERT4RecModel`) via
  `[model.sequential]` (`architecture = "sasrec"` or `"bert4rec"`). Requires
  `pip install -r requirements-sequential.txt` (`rectools[torch]`); serve
  mode never imports torch. AutoML drops it from the candidate pool when
  the extra is missing or median distinct items/user is below
  `[job.sequential].min_median_interactions` (default 5), and logs the skip.

- Incremental events horizontal HA: leader-only apply lease
  (`{lock_key}:events:apply`) when `events.ha = true` with
  `job.trigger.lock_backend` postgres/redis. Fan-out sources acquire the
  lease only when a micro-batch is ready. Metrics:
  `cicerone_events_lock_total`, `cicerone_events_leader`,
  `cicerone_events_apply_busy_total`.

- Redis Streams EventSource (`events.kind = "redis_streams"`): consumer-group
  poll via `XREADGROUP` / `XACK`, idle PEL recovery with `XAUTOCLAIM`, and
  stream entry id fallback when `event_id` is omitted. Requires
  `requirements-redis.txt` (same optional `redis` pin as the lock backend).
- User-scoped incremental write-through: load/replace only affected users
  (plus `__cold_start__`) via `OutputSink.replace_recommendations_for_users`
  (returns post-write distinct user count) instead of full-frame overwrite.
  Updater keeps an LRU-bounded per-user cache (default 2048); dataset
  `count_recommendation_users` projects only `user_id` from parquet, and
  `load_recommendations_for_users` uses parquet `filters` for `user_id` when
  the engine supports predicate pushdown.
- Incremental events Prometheus metrics on serve `/metrics` (source lag /
  connected, flush counters, last success timestamp, tick errors) and an
  incremental-events panel on the Basic-Auth dashboard (from manifests).
- Incremental events between full retrains: internal `EventSource` surface,
  webhook `POST /events`, micro-batch buffer/worker, and write-through
  updater for popular/latest slices (`[events]` config). Design:
  `docs/incremental-events.md`. Webhook `occurred_at` requires an explicit
  timezone (`Z` / offset) or Unix epoch seconds (UTC).
- DB event source (`events.kind = "db"`): watermark poll over
  `events_table` / `events_query`, durable optional `watermark_path`,
  watermark advances only on successful flush ack.
- S3-compatible event source (`events.kind = "s3"`), R2-first: list/marker
  poll via the same `build_s3_client` / `endpoint_url` options as dataset
  I/O; optional AWS-only SQS mode (rejected with `endpoint_url`). JSON
  object/array payloads; ack advances marker or deletes the SQS message.

### Changed

- Parse article `draft` from YAML frontmatter; article layout CSS keys off
  `data-cicerone-articles` rather than starlight-blog class names.
- Share the articles URL prefix between the Starlight plugin and layout
  classifier; `robots.txt` allows the site and disallows `/pagefind/`.
- Article plugin gating passes `{ production }` explicitly; layout kind
  matches starlight-blog listing routes and ignores a missing route id.
- Drop the Starlight “Edit page” footer; site content is edited in git.
- Docker `package` stage validates the wheel via `python -m cicerone.packaging`
  (selects `cicerone_recommender-<version>` including PEP 440 local versions
  and numeric wheel build tags).

- README and docs-site dashboard screenshot include the user recommendation lookup.
- Docs site copies `docs/images/` into `website/public/images/docs/` at build time.
- Dashboard lookup form is labeled, results are announced, and job-run
  tables expose captions / column headers; helper te...
```

### `GH-CAND-0030`

- Source URL: https://github.com/torbido-hq/cicerone/pull/101
- Repository: `torbido-hq/cicerone`
- PR number: `101`
- PR title: feat(website): static articles at /articles/, hidden until a post exists
- Language: `python`
- Code changed files: `['.github/workflows/ci.yml', '.github/workflows/pages.yml', 'website/package-lock.json', 'website/package.json', 'website/src/content.config.ts']`
- Docs changed files: `['CHANGELOG.md', 'CONTRIBUTING.md', 'README.md', 'website/README.md', 'website/src/content/docs/index.mdx']`

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
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -6,7 +6,24 @@ on:
     branches: [main]
 
 jobs:
+  scope:
+    runs-on: ubuntu-latest
+    outputs:
+      python: ${{ steps.filter.outputs.python }}
+    steps:
+      - uses: actions/checkout@v7
+      - uses: dorny/paths-filter@v4
+        id: filter
+        with:
+          filters: |
+            python:
+              - "**"
+              - "!website/**"
+              - "!.github/workflows/pages.yml"
+
   lint:
+    needs: scope
+    if: needs.scope.outputs.python == 'true'
     runs-on: ubuntu-latest
     steps:
       - uses: actions/checkout@v7
@@ -30,6 +47,8 @@ jobs:
         run: docker run --rm cicerone-test pip-audit -r requirements.txt -r requirements-dev.txt
 
   test:
+    needs: scope
+    if: needs.scope.outputs.python == 'true'
     runs-on: ubuntu-latest
     steps:
       - uses: actions/checkout@v7
@@ -48,3 +67,25 @@ jobs:
         run: |
           docker compose --env-file docker/postgres/defaults.env \
             -f docker-compose.ci.yml down -v
+
+  # Always reports: website-only PRs skip lint/test (no Docker VMs) without
+  # leaving a required check pending. Require this job name, not lint/test.
+  ci:
+    needs: [scope, lint, test]
+    if: always() && !cancelled()
+    runs-on: ubuntu-latest
+    steps:
+      - name: Python CI
+        run: |
+          if [ "${{ needs.scope.result }}" != "success" ]; then
+            echo "scope=${{ needs.scope.result }}"
+            exit 1
+          fi
+          if [ "${{ needs.scope.outputs.python }}" != "true" ]; then
+            echo "Website-only change; Python lint/test skipped."
+            exit 0
+          fi
+          if [ "${{ needs.lint.result }}" != "success" ] || [ "${{ needs.test.result }}" != "success" ]; then
+            echo "lint=${{ needs.lint.result }} test=${{ needs.test.result }}"
+            exit 1
+          fi

diff --git a/.github/workflows/pages.yml b/.github/workflows/pages.yml
--- a/.github/workflows/pages.yml
+++ b/.github/workflows/pages.yml
@@ -11,15 +11,18 @@ on:
       - "website/**"
       - "docs/**"
       - ".github/workflows/pages.yml"
+  pull_request:
+    paths:
+      - "website/**"
+      - "docs/**"
+      - ".github/workflows/pages.yml"
   workflow_dispatch:
 
 permissions:
   contents: read
-  pages: write
-  id-token: write
 
 concurrency:
-  group: pages
+  group: pages-${{ github.ref }}
   cancel-in-progress: false
 
 jobs:
@@ -40,13 +43,18 @@ jobs:
           npm ci
           npm run build
 
-      - uses: actions/upload-pages-artifact@v5
+      - if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'
+        uses: actions/upload-pages-artifact@v5
         with:
           path: website/dist
 
   deploy:
+    if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'
     needs: build
     runs-on: ubuntu-latest
+    permissions:
+      pages: write
+      id-token: write
     environment:
       name: github-pages
       url: ${{ steps.deployment.outputs.page_url }}

diff --git a/website/package-lock.json b/website/package-lock.json
--- a/website/package-lock.json
+++ b/website/package-lock.json
@@ -1,16 +1,18 @@
 {
-  "name": "website",
+  "name": "cicerone-website",
   "version": "0.0.1",
   "lockfileVersion": 3,
   "requires": true,
   "packages": {
     "": {
-      "name": "website",
+      "name": "cicerone-website",
       "version": "0.0.1",
       "dependencies": {
         "@astrojs/starlight": "^0.41.7",
         "astro": "^7.1.6",
-        "sharp": "^0.35.3"
+        "sharp": "^0.35.3",
+        "starlight-blog": "^0.29.0",
+        "yaml": "^2.8.0"
       }
     },
     "node_modules/@astrojs/compiler-binding": {
@@ -289,6 +291,17 @@
         "node": ">=22.12.0"
       }
     },
+    "node_modules/@astrojs/rss": {
+      "version": "4.0.19",
+      "resolved": "https://registry.npmjs.org/@astrojs/rss/-/rss-4.0.19.tgz",
+      "integrity": "sha512-e+z5wYeYtffQdHQO8c2tkSd2JEBdAuRXJV4ZEU5IxkYeE6e39woDd7nw1PH1Kk2tEYNCYuKdylnnbhGmt61awA==",
+      "license": "MIT",
+      "dependencies": {
+        "fast-xml-parser": "^5.5.7",
+        "piccolore": "^0.1.3",
+        "zod": "^4.3.6"
+      }
+    },
     "node_modules/@astrojs/sitemap": {
       "version": "3.7.3",
       "resolved": "https://registry.npmjs.org/@astrojs/sitemap/-/sitemap-3.7.3.tgz",
@@ -1667,6 +1680,18 @@
         "@emnapi/runtime": "^1.7.1 || ^2.0.0-alpha.4"
       }
     },
+    "node_modules/@nodable/entities": {
+      "version": "3.0.0",
+      "resolved": "https://registry.npmjs.org/@nodable/entities/-/entities-3.0.0.tgz",
+      "integrity": "sha512-8L9xFeTYKhm49xfIypoe2W5wV1m/3Z58kT+7kR9A8OyFxcPduI4VmxaUMQyKYrRjUoLLSXv6EKKID5Tvj9cUVw==",
+      "funding": [
+        {
+          "type": "github",
+          "url": "https://github.com/sponsors/nodable"
+        }
+      ],
+      "license": "MIT"
+    },
     "node_modules/@oslojs/encoding": {
       "version": "1.1.0",
       "resolved": "https://registry.npmjs.org/@oslojs/encoding/-/encoding-1.1.0.tgz",
@@ -2212,6 +2237,346 @@
       "integrity": "sha512-ko/gIFJRv177XgZsZcBwnqJN5x/Gien8qNOn0D5bQU/zAzVf9Zt3BlcUiLqhV9y4ARk0GbT3tnUiPNgnTXzc/Q==",
       "license": "MIT"
     },
+    "node_modules/@typescript/typescript-aix-ppc64": {
+      "version": "7.0.2",
+      "resolved": "https://registry.npmjs.org/@typescript/typescript-aix-ppc64/-/typescript-aix-ppc64-7.0.2.tgz",
+      "integrity": "sha512-MTKKkWB7p/0E9xi1d1tHtZ5PiLkGEMIq88pK2CubZjOsLtYTLqhgIgi6zepFa+9GHZ6h05NMCkQxGKiPXMxXtQ==",
+      "cpu": [
+        "ppc64"
+      ],
+      "license": "Apache-2.0",
+      "optional": true,
+      "os": [
+        "aix"
+      ],
+      "peer": true,
+      "engines": {
+        "node": ">=16.20.0"
+      }
+    },
+    "node_modules/@typescript/typescript-darwin-arm64": {
+      "version": "7.0.2",
+      "resolved": "https://registry.npmjs.org/@typescript/typescript-darwin-arm64/-/typescript-darwin-arm64-7.0.2.tgz",
+      "integrity": "sha512-gowzar9MwS/aRWp6f3a4KUqzRjAZjOsmGNCM6LcTgXum+dBfgsBVMN+AgvOCCbguXyick6LJhpBszxMebJ8syA==",
+      "cpu": [
+        "arm64"
+      ],
+      "license": "Apache-2.0",
+      "optional": true,
+      "os": [
+        "darwin"
+      ],
+      "peer": true,
+      "engines": {
+        "node": ">=16.20.0"
+      }
+    },
+    "node_modules/@typescript/typescript-darwin-x64": {
+      "version": "7.0.2",
+      "resolved": "https://registry.npmjs.org/@typescript/typescript-darwin-x64/-/typescript-darwin-x64-7.0.2.tgz",
+      "integrity": "sha512-SZ9xZInqApNlNGc9s0W1VSsktYSOe9cFqNOIqmN1Gs8SmkjKZYFt017G4VwPxASInODuAdbTW7sXiFUf893RgA==",
+      "cpu": [
+        "x64"
+      ],
+      "license": "Apache-2.0",
+      "optional": true,
+      "os": [
+        "darwin"
+      ],
+      "peer": true,
+      "engines": {
+        "node": ">=16.20.0"
+      }
+    },
+    "node_modules/@typescript/typescript-freebsd-arm64": {
+      "version": "7.0.2",
+      "resolved": "https://registry.npmjs.org/@typescript/typescript-freebsd-arm64/-/typescript-freebsd-arm64-7.0.2.tgz",
+      "integrity": "sha512-W5NH4y/J0plIIS5b2xvTEkU7JFxyqdMAOgf+Ilhl0vHQXKO5dZoxd+C/jEtq56c4F3wk71RB4BMRQ2XdI+bwYQ==",
+      "cpu": [
+        "arm64"
+      ],
+      "license": "Apache-2.0",
+      "optional": true,
+      "os": [
+        "freebsd"
+      ],
+      "peer": true,
+      "engines": {
+        "node": ">=16.20.0"
+      }
+    },
+    "node_modules/@typescript/typescript-freebsd-x64": {
+      "version": "7.0.2",
+      "resolved": "https://registry.npmjs.org/@typescript/typescript-freebsd-x64/-/typescript-freebsd-x64-7.0.2.tgz",
+      "integrity": "sha512-UMGDx5sTpzNw3WiPebH7l90IWfJggEd+egHt/q6p7/Cm3zqoV7VxkGXt+3DxPIw8CcmvAB0j3sVVfbhX+M4Tpw==",
+      "cpu": [
+        "x64"
+      ],
+      "license": "Apache-2.0",
+      "optional": true,
+      "os": [
+        "freebsd"
+      ],
+      "peer": true,
+      "engines": {
+        "node": ">=16.20.0"
+      }
+    },
+    "node_modules/@typescript/typescript-linux-arm": {
+      "version": "7.0.2",
+      "resolved": "https://registry.npmjs.org/@typescript/typescript-linux-arm/-/typescript-linux-arm-7.0.2.tgz",
+      "integrity": "sha512-gffT3xPz9sR7j/YJExkyPntrI0P2EP9XbOyWzth2/Gs0RstK+90RBcO0ncXoXy/beYll1SXw846Nf2zdnEz0QQ==",
+      "cpu": [
+        "arm"
+      ],
+      "license": "Apache-2.0",
+      "optional": true,
+      "os": [
+        "linux"
+      ],
+      "peer": true,
+      "engines": {
+        "node": ">=16.20.0"
+      }
+    },
+    "node_modules/@typescript/typescript-linux-arm64": {
+      "version": "7.0.2",
+      "resolved": "https://registry.npmjs.org/@typescript/typescript-linux-arm64/-/typescript-linux-arm64-7.0.2.tgz",
+      "integrity": "sha512-Qh4eU4/y3yDjnfjjyPYihMj5/ODIlmt+Bzu17OI+fiSRDW57QmU5SiN63exPRNJPKUzcc1INa1NXdrJ+MqHjUQ==",
+      "cpu": [
+        "arm64"
+      ],
+      "license": "Apac...
```

Allowed model input — docs before excerpt:

```markdown
<!-- CHANGELOG.md @ 64eba98e5466d90aa41f76dd3d46cf192f75b3dd -->
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Dashboard user lookup: inspect a `user_id`'s current precomputed top-K
  (rank, item, score, source, optional category) from the job output store,
  with cold-start fallback, on the Basic-Auth status page.
  `GET /dashboard?user_id=` fills the lookup on load.

- Optional **sequential** strategy (`SASRecModel` / `BERT4RecModel`) via
  `[model.sequential]` (`architecture = "sasrec"` or `"bert4rec"`). Requires
  `pip install -r requirements-sequential.txt` (`rectools[torch]`); serve
  mode never imports torch. AutoML drops it from the candidate pool when
  the extra is missing or median distinct items/user is below
  `[job.sequential].min_median_interactions` (default 5), and logs the skip.

- Incremental events horizontal HA: leader-only apply lease
  (`{lock_key}:events:apply`) when `events.ha = true` with
  `job.trigger.lock_backend` postgres/redis. Fan-out sources acquire the
  lease only when a micro-batch is ready. Metrics:
  `cicerone_events_lock_total`, `cicerone_events_leader`,
  `cicerone_events_apply_busy_total`.

- Redis Streams EventSource (`events.kind = "redis_streams"`): consumer-group
  poll via `XREADGROUP` / `XACK`, idle PEL recovery with `XAUTOCLAIM`, and
  stream entry id fallback when `event_id` is omitted. Requires
  `requirements-redis.txt` (same optional `redis` pin as the lock backend).
- User-scoped incremental write-through: load/replace only affected users
  (plus `__cold_start__`) via `OutputSink.replace_recommendations_for_users`
  (returns post-write distinct user count) instead of full-frame overwrite.
  Updater keeps an LRU-bounded per-user cache (default 2048); dataset
  `count_recommendation_users` projects only `user_id` from parquet, and
  `load_recommendations_for_users` uses parquet `filters` for `user_id` when
  the engine supports predicate pushdown.
- Incremental events Prometheus metrics on serve `/metrics` (source lag /
  connected, flush counters, last success timestamp, tick errors) and an
  incremental-events panel on the Basic-Auth dashboard (from manifests).
- Incremental events between full retrains: internal `EventSource` surface,
  webhook `POST /events`, micro-batch buffer/worker, and write-through
  updater for popular/latest slices (`[events]` config). Design:
  `docs/incremental-events.md`. Webhook `occurred_at` requires an explicit
  timezone (`Z` / offset) or Unix epoch seconds (UTC).
- DB event source (`events.kind = "db"`): watermark poll over
  `events_table` / `events_query`, durable optional `watermark_path`,
  watermark advances only on successful flush ack.
- S3-compatible event source (`events.kind = "s3"`), R2-first: list/marker
  poll via the same `build_s3_client` / `endpoint_url` options as dataset
  I/O; optional AWS-only SQS mode (rejected with `endpoint_url`). JSON
  object/array payloads; ack advances marker or deletes the SQS message.

### Changed

- Revert unpublished website articles that landed on `main` in #96.
- README and docs-site dashboard screenshot include the user recommendation lookup.
- Docs site copies `docs/images/` into `website/public/images/docs/` at build time.
- Dashboard lookup form is labeled, results are announced, and job-run
  tables expose captions / column headers; helper text contrast is higher.
- Dashboard inspector k is `min(job.top_k, dashboard.lookup_k)` (default 20).

- Bump `pyarrow` 25.0.0 → 25.0.1 (#85), `SQLAlchemy` 2.0.51 → 2.0.52 (#86),
  `uvicorn` 0.52.1 → 0.52.3 (#87), `ruff` 0.16.2 → 0.16.3 (#88).
- Bump GitHub Actions Pages deploy helpers: `actions/upload-pages-artifact`
  v3 → v5 (Dependabot #79), `actions/deploy-pages` v4 → v5 (#80).
- Bump `fastapi` 0.140.13 → 0.141.1 (Dependabot #69).
- Dependabot: ignore `numpy` major bumps (Python 3.11 CI) and `boto3>=1.43.57`
  (aiobotocore botocore pin).
- Project docs site (not part of the runtime product): Starlight under
  `website/`, synced from `docs/`, published at [cicerone.dev](https://cicerone.dev).

### Fixed

- Dashboard still starts if the recommendation store cannot be opened (lookup disabled).
- Dashboard lookup errors show a generic message; details stay in the logs.
- Dashboard lookup URL updates keep the hash fragment.
- Dashboard lookup disables the Look up button during the htmx request.
- Postgres `is_locked()` logs and re-raises probe failures instead of
  treating a dead database as “lock free”; `owned()` logs before fail-closed.
- S3 EventSource `nack` returns events to the local pending queue (and
  extends SQS visibility) instead of dropping the batch. SQS HA lock-busy
  nacks can retry immediately; list-mode array payloads no longer lose
  sibling events when one id is nacked.
- Event worker ack/nack bookkeeping: buffer duplicates are acked (not left
  in-flight), capacity...
```

Audit context only — docs diff excerpt:

```diff
diff --git a/CHANGELOG.md b/CHANGELOG.md
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -13,6 +13,13 @@ The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
   with cold-start fallback, on the Basic-Auth status page.
   `GET /dashboard?user_id=` fills the lookup on load.
 
+- Optional project-site articles at `/articles/` (static Markdown under
+  `website/src/content/docs/articles/`). No nav, RSS, or index until a
+  published post exists. Article pages use IBM Plex Serif and a ~65ch
+  measure. Brand accents invert for dark theme. Listing keeps an h1;
+  posts use `description` for meta. Website-only PRs skip Docker lint/test
+  jobs; the `ci` job still succeeds.
+
 - Optional **sequential** strategy (`SASRecModel` / `BERT4RecModel`) via
   `[model.sequential]` (`architecture = "sasrec"` or `"bert4rec"`). Requires
   `pip install -r requirements-sequential.txt` (`rectools[torch]`); serve
@@ -56,7 +63,13 @@ The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
 
 ### Changed
 
-- Revert unpublished website articles that landed on `main` in #96.
+- Parse article `draft` from YAML frontmatter; article layout CSS keys off
+  `data-cicerone-articles` rather than starlight-blog class names.
+- Share the articles URL prefix between the Starlight plugin and layout
+  classifier; `robots.txt` allows the site and disallows `/pagefind/`.
+- Article plugin gating passes `{ production }` explicitly; layout kind
+  matches starlight-blog listing routes and ignores a missing route id.
+- Drop the Starlight “Edit page” footer; site content is edited in git.
 - README and docs-site dashboard screenshot include the user recommendation lookup.
 - Docs site copies `docs/images/` into `website/public/images/docs/` at build time.
 - Dashboard lookup form is labeled, results are announced, and job-run

diff --git a/CONTRIBUTING.md b/CONTRIBUTING.md
--- a/CONTRIBUTING.md
+++ b/CONTRIBUTING.md
@@ -156,7 +156,10 @@ and/or `examples/serve/` when request/response fields change.
   notes (not repo policy): Cursor **User Rules** / **Team Rules**.
 - Add/update tests for any behavior change — the coverage gate is enforced
   in CI, not just locally.
-- Make sure both the lint job and the test job pass before requesting review.
+- Make sure the `ci` job passes before requesting review. Python changes
+  also run `lint` and `test`. PRs that only touch `website/**` skip those
+  Docker jobs; `ci` still succeeds. The Pages workflow builds the Starlight
+  site (`cd website && npm ci && npm run build`).
 
 ## Releasing

diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -10,7 +10,8 @@
 
 **Site:** [cicerone.dev](https://cicerone.dev)
 ([Starlight](https://starlight.astro.build/) docs site; source in [`website/`](website/),
-content synced from [`docs/`](docs/)).
+guides synced from [`docs/`](docs/). Articles are static Markdown in
+`website/src/content/docs/articles/` and stay off the site until a post exists).
 
 A generic, self-hosted batch recommender system. It reads your interaction
 data, trains a hybrid [rectools](https://github.com/MobileTeleSystems/RecTools)

diff --git a/website/README.md b/website/README.md
--- a/website/README.md
+++ b/website/README.md
@@ -2,7 +2,10 @@
 
 Docs site for [cicerone.dev](https://cicerone.dev). Built with
 [Starlight](https://starlight.astro.build/); markdown under repo `docs/` is
-synced into the Starlight content collection at build time.
+synced into the Starlight content collection at build time. Articles are the
+same static build (no CMS): posts live under `src/content/docs/articles/`.
+With no published post, the articles plugin is off — no header link, RSS, or
+`/articles/` route.
 
 ## Commands
 
@@ -19,20 +22,50 @@ npm run preview  # serve dist/
 | Path | Role |
 | --- | --- |
 | `src/content/docs/index.mdx` | Landing (Starlight splash) |
+| `src/content/docs/articles/` | Articles (`title` + `date` frontmatter) → `/articles/` |
 | `scripts/sync-docs.mjs` | Copies `../docs/*.md` → `src/content/docs/` with frontmatter |
-| `astro.config.mjs` | Site URL, sidebar, logo, social |
+| `astro.config.mjs` | Site URL, sidebar, logo, social, articles plugin |
 | `public/CNAME` | Custom domain (`cicerone.dev`) |
 | `public/images/` | Site diagrams (`flow.svg`) |
 | `public/images/docs/` | Copied from `../docs/images/` at build time (gitignored) |
 
 Generated `src/content/docs/tutorial.md`, `architecture.md`, and
-`public/images/docs/` are gitignored; CI and local builds always sync from
-`docs/`.
+`incremental-events.md` are gitignored; `public/images/docs/` is copied from
+`docs/images/` at build time. CI and local builds always sync from `docs/`.
+Articles are **not** synced from `docs/` — add Markdown under
+`src/content/docs/articles/` (see below).
+
+## Articles
+
+Jekyll-style: a `.md` file with YAML frontmatter, HTML at build time, nothing
+dynamic. Author globally is `nicholas` (`astro.config.mjs`). Until a
+non-draft post exists, Articles is omitted from the build.
+
+```md
+---
+title: Post title
+description: One-line summary for search results and Open Graph.
+date: 2026-08-19
+excerpt: Listing blurb (falls back to description / body).
+authors:
+  - nicholas
+---
+
+Body…
+```
+
+Drafts (`draft: true`, or YAML 1.1 `yes` / `on`) are omitted from
+production builds; `astro dev` still loads them so `/articles/` can be
+previewed. Frontmatter is parsed as YAML. RSS is
+`/articles/rss.xml` once a post is published. Article pages use IBM Plex
+Serif at ~65ch; chrome stays IBM Plex Sans, dates IBM Plex Mono.
 
 ## Publishing
 
 [`.github/workflows/pages.yml`](../.github/workflows/pages.yml) builds
-`website/` on pushes to `main` that touch `website/**` or `docs/**`.
+`website/` on PRs and on pushes to `main` that touch `website/**` or
+`docs/**`. Only `main` deploys. Website-only PRs skip Docker lint/pytest;
+the `ci` job still succeeds so a required check is not left pending.
 
 **One-time:** Settings → Pages → Source = **GitHub Actions**, custom domain
 `cicerone.dev`. DNS notes for Gandi apex records are below.

diff --git a/website/src/content/docs/index.mdx b/website/src/content/docs/index.mdx
--- a/website/src/content/docs/index.mdx
+++ b/website/src/content/docs/index.mdx
@@ -2,7 +2,6 @@
 title: Home
 description: Self-hosted batch recommender — hybrid models, policies, serve API, and dashboard. No live inference in the request path.
 template: splash
-editUrl: false
 hero:
   title: Cicerone
   tagline: A generic, self-hosted batch recommender. Train offline, write top-K recommendations, optionally serve them over a small read-only HTTP API.
```

Audit context only — docs after excerpt:

```markdown
<!-- CHANGELOG.md @ d90bb0b386eddf250e91e8d7cdbec5f121008752 -->
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Dashboard user lookup: inspect a `user_id`'s current precomputed top-K
  (rank, item, score, source, optional category) from the job output store,
  with cold-start fallback, on the Basic-Auth status page.
  `GET /dashboard?user_id=` fills the lookup on load.

- Optional project-site articles at `/articles/` (static Markdown under
  `website/src/content/docs/articles/`). No nav, RSS, or index until a
  published post exists. Article pages use IBM Plex Serif and a ~65ch
  measure. Brand accents invert for dark theme. Listing keeps an h1;
  posts use `description` for meta. Website-only PRs skip Docker lint/test
  jobs; the `ci` job still succeeds.

- Optional **sequential** strategy (`SASRecModel` / `BERT4RecModel`) via
  `[model.sequential]` (`architecture = "sasrec"` or `"bert4rec"`). Requires
  `pip install -r requirements-sequential.txt` (`rectools[torch]`); serve
  mode never imports torch. AutoML drops it from the candidate pool when
  the extra is missing or median distinct items/user is below
  `[job.sequential].min_median_interactions` (default 5), and logs the skip.

- Incremental events horizontal HA: leader-only apply lease
  (`{lock_key}:events:apply`) when `events.ha = true` with
  `job.trigger.lock_backend` postgres/redis. Fan-out sources acquire the
  lease only when a micro-batch is ready. Metrics:
  `cicerone_events_lock_total`, `cicerone_events_leader`,
  `cicerone_events_apply_busy_total`.

- Redis Streams EventSource (`events.kind = "redis_streams"`): consumer-group
  poll via `XREADGROUP` / `XACK`, idle PEL recovery with `XAUTOCLAIM`, and
  stream entry id fallback when `event_id` is omitted. Requires
  `requirements-redis.txt` (same optional `redis` pin as the lock backend).
- User-scoped incremental write-through: load/replace only affected users
  (plus `__cold_start__`) via `OutputSink.replace_recommendations_for_users`
  (returns post-write distinct user count) instead of full-frame overwrite.
  Updater keeps an LRU-bounded per-user cache (default 2048); dataset
  `count_recommendation_users` projects only `user_id` from parquet, and
  `load_recommendations_for_users` uses parquet `filters` for `user_id` when
  the engine supports predicate pushdown.
- Incremental events Prometheus metrics on serve `/metrics` (source lag /
  connected, flush counters, last success timestamp, tick errors) and an
  incremental-events panel on the Basic-Auth dashboard (from manifests).
- Incremental events between full retrains: internal `EventSource` surface,
  webhook `POST /events`, micro-batch buffer/worker, and write-through
  updater for popular/latest slices (`[events]` config). Design:
  `docs/incremental-events.md`. Webhook `occurred_at` requires an explicit
  timezone (`Z` / offset) or Unix epoch seconds (UTC).
- DB event source (`events.kind = "db"`): watermark poll over
  `events_table` / `events_query`, durable optional `watermark_path`,
  watermark advances only on successful flush ack.
- S3-compatible event source (`events.kind = "s3"`), R2-first: list/marker
  poll via the same `build_s3_client` / `endpoint_url` options as dataset
  I/O; optional AWS-only SQS mode (rejected with `endpoint_url`). JSON
  object/array payloads; ack advances marker or deletes the SQS message.

### Changed

- Parse article `draft` from YAML frontmatter; article layout CSS keys off
  `data-cicerone-articles` rather than starlight-blog class names.
- Share the articles URL prefix between the Starlight plugin and layout
  classifier; `robots.txt` allows the site and disallows `/pagefind/`.
- Article plugin gating passes `{ production }` explicitly; layout kind
  matches starlight-blog listing routes and ignores a missing route id.
- Drop the Starlight “Edit page” footer; site content is edited in git.
- README and docs-site dashboard screenshot include the user recommendation lookup.
- Docs site copies `docs/images/` into `website/public/images/docs/` at build time.
- Dashboard lookup form is labeled, results are announced, and job-run
  tables expose captions / column headers; helper text contrast is higher.
- Dashboard inspector k is `min(job.top_k, dashboard.lookup_k)` (default 20).

- Bump `pyarrow` 25.0.0 → 25.0.1 (#85), `SQLAlchemy` 2.0.51 → 2.0.52 (#86),
  `uvicorn` 0.52.1 → 0.52.3 (#87), `ruff` 0.16.2 → 0.16.3 (#88).
- Bump GitHub Actions Pages deploy helpers: `actions/upload-pages-artifact`
  v3 → v5 (Dependabot #79), `actions/deploy-pages` v4 → v5 (#80).
- Bump `fastapi` 0.140.13 → 0.141.1 (Dependabot #69).
- Dependabot: ignore `numpy` major bumps (Python 3.11 CI) and `boto3>=1.43.57`
  (aiobotocore botocore pin).
- Project docs site (not part of the runtime product): Starlight under
  `website/`, synced from `docs/`, published at [cicerone.dev](...
```
