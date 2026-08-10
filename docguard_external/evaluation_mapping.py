from __future__ import annotations


def label_policy_for_dataset(dataset: str) -> dict:
    if dataset == "codocbench":
        return {
            "positive_policy": "code and documentation/docstring changed in same mined commit => strong positive",
            "negative_policy": "do not infer negatives unless CoDocBench provides code-only non-doc-change samples or a conservative paired sampling protocol is defined",
            "target_kind": "docstring_or_documentation",
            "patch_policy": "doc_after/doc_diff can support patch reconstruction when available",
        }
    if dataset == "comment_update":
        return {
            "positive_policy": "code and associated natural language comment changed => strong positive",
            "negative_policy": "avoid automatic negatives without dataset-provided no-update labels",
            "target_kind": "comment",
            "patch_policy": "comment edit sequence or comment_after can support patch-generation evaluation",
        }
    if dataset == "codesearchnet":
        return {
            "positive_policy": "static code-comment pair only; not direct update label",
            "negative_policy": "not suitable for docs_update_required negatives",
            "target_kind": "docstring",
            "patch_policy": "retrieval/embedding auxiliary only",
        }
    return {
        "positive_policy": "dataset-specific",
        "negative_policy": "dataset-specific; keep strong and weak labels separate",
        "target_kind": "comment_or_documentation",
        "patch_policy": "classification first, patch reconstruction only if before/after text exists",
    }

