from __future__ import annotations


DATASET_CANDIDATES = {
    "codocbench": {
        "name": "CoDocBench",
        "url": "https://github.com/kunpai/codocbench",
        "paper": "https://arxiv.org/html/2502.00519v1",
        "task_type": "code-documentation alignment during maintenance",
        "priority": "high",
        "notes": "Most promising first external benchmark candidate for real code/docstring co-changes.",
    },
    "comment_update": {
        "name": "Learning to Update Natural Language Comments Based on Code Changes",
        "url": "https://github.com/panthap2/LearningToUpdateNLComments",
        "paper": "https://aclanthology.org/2020.acl-main.168/",
        "task_type": "comment update generation from code changes",
        "priority": "high",
        "notes": "Real commit-derived code/comment update pairs; focused on comments/docstrings.",
        "expected_label_type": "positive update pairs unless local downloaded data shows explicit non-update labels",
        "docguard_mapping_notes": "Map as external positive comment-update records when code/comment before-after fields are available.",
        "limitations": "Likely not sufficient for external precision/F1 unless non-update examples are present.",
    },
    "panthaplackel_comment_update": {
        "name": "Learning to Update Natural Language Comments Based on Code Changes",
        "url": "https://github.com/panthap2/LearningToUpdateNLComments",
        "paper": "https://aclanthology.org/2020.acl-main.168/",
        "task_type": "comment update generation from code changes",
        "priority": "medium-high",
        "expected_label_type": "comment update pairs; binary negatives not confirmed",
        "docguard_mapping_notes": "Candidate second positive external benchmark for code/comment maintenance; inspect downloaded data for old/new code and old/new comment fields.",
        "limitations": "Repository points to Google Drive data; local format must be inspected before mapping. If only update pairs exist, it cannot support precision/F1.",
        "notes": "Use this id for explicit external adapter scaffolding; `comment_update` is retained as a legacy alias.",
    },
    "codesearchnet": {
        "name": "CodeSearchNet",
        "url": "https://github.com/github/CodeSearchNet",
        "paper": "https://arxiv.org/pdf/1909.09436",
        "task_type": "static code-comment retrieval",
        "priority": "auxiliary",
        "notes": "Useful for embeddings/retrieval, not a code-change update benchmark.",
    },
    "docchecker": {
        "name": "DocChecker / code-comment inconsistency datasets",
        "url": "https://github.com/FSoft-AI4Code/DocChecker",
        "paper": "https://aclanthology.org/2024.eacl-demo.20/",
        "task_type": "code-comment inconsistency detection/rectification",
        "priority": "high",
        "expected_label_type": "explicit consistent/inconsistent labels for ICCD / Just-In-Time-style task if dataset is obtained",
        "docguard_mapping_notes": "Map inconsistent examples to docs_update_required=true and consistent examples to docs_update_required=false as an external binary proxy.",
        "limitations": "DocChecker repo references CodeXGLUE for pre-training and Google Drive Just-In-Time data for fine-tuning; local dataset format must be inspected before mapping.",
        "notes": "Best current candidate family for an explicit external binary sanity/evaluation set.",
    },
}


def list_candidates() -> list[dict]:
    return [{"id": key, **value} for key, value in DATASET_CANDIDATES.items()]


def describe_candidate(dataset: str) -> dict:
    if dataset not in DATASET_CANDIDATES:
        raise KeyError(f"Unknown dataset candidate: {dataset}")
    return {"id": dataset, **DATASET_CANDIDATES[dataset]}
