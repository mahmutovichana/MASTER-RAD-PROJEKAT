# Manual Audit Template

The automatic validator checks schema and consistency constraints, but it does not replace human quality review.

Use this checklist for each record in `reports/manual_audit_sample.jsonl`.

## Record Review Checklist

Record id:

Scenario type:

1. Is `code_diff` meaningful and realistic?
2. Does `docs_before_excerpt` really represent missing or outdated documentation?
3. Are `expected_facts` correct and grounded in the `code_diff`?
4. Does `gold_doc_patch` match the actual code change?
5. Is the patch minimal and specific?
6. Is `target_doc_file` correct?
7. Is `target_section` correct?
8. For negative records, is `negative_reason` logical?
9. Would a developer realistically expect documentation to be updated for this change?
10. Notes / decision:

Decision:

- accepted
- needs correction
- unclear

Notes:
