# Synthetic Negative Sanity Control 2026-08

- Input mode: `code_diff_only`
- Control type: `synthetic negatives`, not an external negative set
- Total negative records evaluated: `500`
- Predicted update-required count: `0`
- False positive count: `0`
- Negative accuracy: `100.00%`
- False positive rate: `0.00%`
- Median confidence: `0.1360`
- Low confidence <0.25: `270`
- Min confidence: `0.1329`
- Max confidence: `0.8928`

## Dataset Paths Searched

- `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\validation.jsonl`

## Important Limitation

This is a sanity control using existing synthetic negatives. It is useful for checking constant-positive behavior, but it is not a real external negative set and cannot support final external precision/F1.

## Predicted Doc Category Distribution

- `no_update`: 500

## Predicted Scenario Type Distribution

- `internal_variable_rename_no_behavior_change`: 189
- `helper_extraction_no_behavior_change`: 75
- `docs_already_updated`: 39
- `config_refactor_no_new_env_var`: 39
- `test_assertion_refactor_no_behavior_change`: 38
- `dev_dependency_patch_no_command_change`: 38
- `route_implementation_refactor_no_contract_change`: 38
- `type_alias_rename_no_contract_change`: 38
- `internal_performance_refactor_no_documented_behavior_change`: 3
- `comments_reworded_no_contract_change`: 2
- `log_message_change_no_user_visible_behavior`: 1

## Top False-Positive Examples

None.

## 10 Low-Confidence Examples

### docguard-v04-project-29-api-176

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `private_helper_refactor_no_flow_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_performance_refactor_no_documented_behavior_change`
- confidence: `0.1329`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29176 = compute();\n+const renamedInternalName29176 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-108

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `log_message_change_no_user_visible_behavior`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_variable_rename_no_behavior_change`
- confidence: `0.1330`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29108 = compute();\n+const renamedInternalName29108 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-170

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `helper_extraction_no_behavior_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_performance_refactor_no_documented_behavior_change`
- confidence: `0.1330`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29170 = compute();\n+const renamedInternalName29170 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-076

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `comments_reworded_no_contract_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_variable_rename_no_behavior_change`
- confidence: `0.1330`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29076 = compute();\n+const renamedInternalName29076 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-154

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `comments_reworded_no_contract_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_variable_rename_no_behavior_change`
- confidence: `0.1331`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29154 = compute();\n+const renamedInternalName29154 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-174

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `internal_variable_rename_no_behavior_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_performance_refactor_no_documented_behavior_change`
- confidence: `0.1332`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29174 = compute();\n+const renamedInternalName29174 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-074

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `formatting_only_in_docs_or_code`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `comments_reworded_no_contract_change`
- confidence: `0.1332`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29074 = compute();\n+const renamedInternalName29074 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-178

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `formatting_only_in_docs_or_code`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_variable_rename_no_behavior_change`
- confidence: `0.1332`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29178 = compute();\n+const renamedInternalName29178 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-076

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `helper_extraction_no_behavior_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_variable_rename_no_behavior_change`
- confidence: `0.1333`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName27076 = compute();\n+const renamedInternalName27076 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-014

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `helper_extraction_no_behavior_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `internal_variable_rename_no_behavior_change`
- confidence: `0.1333`
- code_diff: diff --git a/src/modules/tickets/tickets.service.ts b/src/modules/tickets/tickets.service.ts\n@@\n-const internalName29014 = compute();\n+const renamedInternalName29014 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.


## 10 High-Confidence Examples

### docguard-v04-project-29-api-086

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.8928`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName29086 = compute();\n+const renamedInternalName29086 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-080

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `dev_dependency_patch_no_command_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `dev_dependency_patch_no_command_change`
- confidence: `0.8918`
- code_diff: diff --git a/package.json b/package.json\n@@\n-const internalName29080 = compute();\n+const renamedInternalName29080 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-018

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.8897`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName27018 = compute();\n+const renamedInternalName27018 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-168

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `dev_dependency_patch_no_command_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `dev_dependency_patch_no_command_change`
- confidence: `0.8897`
- code_diff: diff --git a/package.json b/package.json\n@@\n-const internalName27168 = compute();\n+const renamedInternalName27168 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-064

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `dev_dependency_patch_no_command_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `dev_dependency_patch_no_command_change`
- confidence: `0.8894`
- code_diff: diff --git a/package.json b/package.json\n@@\n-const internalName27064 = compute();\n+const renamedInternalName27064 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-30-api-016

- project: `docguard-v04-project-30-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `docs_already_updated`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `docs_already_updated`
- confidence: `0.8892`
- code_diff: diff --git a/docs/api.md b/docs/api.md\n@@\n-const internalName30016 = compute();\n+const renamedInternalName30016 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-142

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `dev_dependency_patch_no_command_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `dev_dependency_patch_no_command_change`
- confidence: `0.8892`
- code_diff: diff --git a/package.json b/package.json\n@@\n-const internalName27142 = compute();\n+const renamedInternalName27142 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-184

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `dev_dependency_patch_no_command_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `dev_dependency_patch_no_command_change`
- confidence: `0.8890`
- code_diff: diff --git a/package.json b/package.json\n@@\n-const internalName29184 = compute();\n+const renamedInternalName29184 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-29-api-002

- project: `docguard-v04-project-29-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `dev_dependency_patch_no_command_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `dev_dependency_patch_no_command_change`
- confidence: `0.8887`
- code_diff: diff --git a/package.json b/package.json\n@@\n-const internalName29002 = compute();\n+const renamedInternalName29002 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

### docguard-v04-project-27-api-012

- project: `docguard-v04-project-27-api`
- source path: `C:\Users\mahmu\Desktop\MASTER RAD PROJEKAT\data\test.jsonl`
- gold scenario: `dev_dependency_patch_no_command_change`
- predicted docs_update_required: `False`
- predicted doc category: `no_update`
- predicted scenario: `dev_dependency_patch_no_command_change`
- confidence: `0.8886`
- code_diff: diff --git a/package.json b/package.json\n@@\n-const internalName27012 = compute();\n+const renamedInternalName27012 = compute();
- docs_before_excerpt: No documentation-relevant behavior changed.

