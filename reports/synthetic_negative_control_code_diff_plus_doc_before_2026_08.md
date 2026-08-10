# Synthetic Negative Sanity Control 2026-08

- Input mode: `code_diff_plus_doc_before`
- Control type: `synthetic negatives`, not an external negative set
- Total negative records evaluated: `500`
- Predicted update-required count: `0`
- False positive count: `0`
- Negative accuracy: `100.00%`
- False positive rate: `0.00%`
- Median confidence: `0.1325`
- Low confidence <0.25: `270`
- Min confidence: `0.1296`
- Max confidence: `0.9059`

## Dataset Paths Searched

- `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\validation.jsonl`

## Important Limitation

This is a sanity control using existing synthetic negatives. It is useful for checking constant-positive behavior, but it is not a real external negative set and cannot support final external precision/F1.

## Predicted Doc Category Distribution

- `no_update`: 500

## Predicted Scenario Type Distribution

- `internal_variable_rename_no_behavior_change`: 82
- `internal_performance_refactor_no_documented_behavior_change`: 80
- `helper_extraction_no_behavior_change`: 55
- `docs_already_updated`: 39
- `config_refactor_no_new_env_var`: 39
- `test_assertion_refactor_no_behavior_change`: 38
- `dev_dependency_patch_no_command_change`: 38
- `route_implementation_refactor_no_contract_change`: 38
- `type_alias_rename_no_contract_change`: 38
- `comments_reworded_no_contract_change`: 35
- `log_message_change_no_user_visible_behavior`: 15
- `private_helper_refactor_no_flow_change`: 3

## Top False-Positive Examples

None.

## 10 Low-Confidence Examples

### docguard-v04-project-27-api-186

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `private_helper_refactor_no_flow_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_variable_rename_no_behavior_change`
- confidence: `0.1296`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName27186 = compute();\n+const renamedInternalName27186 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-184

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `internal_variable_rename_no_behavior_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_performance_refactor_no_documented_behavior_change`
- confidence: `0.1296`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName27184 = compute();\n+const renamedInternalName27184 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-186

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `log_message_change_no_user_visible_behavior`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_variable_rename_no_behavior_change`
- confidence: `0.1299`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29186 = compute();\n+const renamedInternalName29186 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-196

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `log_message_change_no_user_visible_behavior`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `log_message_change_no_user_visible_behavior`
- confidence: `0.1300`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName27196 = compute();\n+const renamedInternalName27196 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-016

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `internal_performance_refactor_no_documented_behavior_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_performance_refactor_no_documented_behavior_change`
- confidence: `0.1300`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName27016 = compute();\n+const renamedInternalName27016 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-188

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `formatting_only_in_docs_or_code`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_variable_rename_no_behavior_change`
- confidence: `0.1300`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName27188 = compute();\n+const renamedInternalName27188 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-198

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `internal_performance_refactor_no_documented_behavior_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `log_message_change_no_user_visible_behavior`
- confidence: `0.1301`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName27198 = compute();\n+const renamedInternalName27198 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-30-api-074

- project: `docguard-v04-project-30-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `helper_extraction_no_behavior_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `comments_reworded_no_contract_change`
- confidence: `0.1301`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName30074 = compute();\n+const renamedInternalName30074 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-068

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `internal_performance_refactor_no_documented_behavior_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_performance_refactor_no_documented_behavior_change`
- confidence: `0.1301`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName27068 = compute();\n+const renamedInternalName27068 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-066

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `log_message_change_no_user_visible_behavior`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `helper_extraction_no_behavior_change`
- confidence: `0.1302`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName27066 = compute();\n+const renamedInternalName27066 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.


## 10 High-Confidence Examples

### docguard-v04-project-29-api-086

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9059`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName29086 = compute();\n+const renamedInternalName29086 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-018

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9041`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName27018 = compute();\n+const renamedInternalName27018 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-008

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9041`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName29008 = compute();\n+const renamedInternalName29008 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-28-api-078

- project: `docguard-v04-project-28-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9033`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName28078 = compute();\n+const renamedInternalName28078 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-28-api-052

- project: `docguard-v04-project-28-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9027`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName28052 = compute();\n+const renamedInternalName28052 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-30-api-016

- project: `docguard-v04-project-30-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9026`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName30016 = compute();\n+const renamedInternalName30016 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-28-api-026

- project: `docguard-v04-project-28-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9017`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName28026 = compute();\n+const renamedInternalName28026 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-28-api-104

- project: `docguard-v04-project-28-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9016`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName28104 = compute();\n+const renamedInternalName28104 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-30-api-042

- project: `docguard-v04-project-30-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9015`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName30042 = compute();\n+const renamedInternalName30042 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-28-api-156

- project: `docguard-v04-project-28-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.9015`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName28156 = compute();\n+const renamedInternalName28156 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

