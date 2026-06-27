# Real LLM Manual Review Template

Use this checklist for each real Hugging Face LLM prediction before trusting aggregate metrics.

1. Is `docs_update_required` correct?
2. Is `scenario_type` correct or at least semantically close?
3. Is `doc_category` correct?
4. Is `target_doc_file` correct?
5. Is `generated_doc_patch` grounded in `code_diff`?
6. Does the patch cover important expected facts?
7. Does it hallucinate implementation details?
8. Is confidence reasonable?
9. Decision: accepted / partially correct / incorrect / hallucinated
10. Notes:
