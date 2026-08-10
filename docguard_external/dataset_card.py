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
        "paper": "https://arxiv.org/html/2306.06347v3",
        "task_type": "code-comment inconsistency detection/rectification",
        "priority": "auxiliary",
        "notes": "Relevant related work and possible consistency baseline.",
    },
}


def list_candidates() -> list[dict]:
    return [{"id": key, **value} for key, value in DATASET_CANDIDATES.items()]


def describe_candidate(dataset: str) -> dict:
    if dataset not in DATASET_CANDIDATES:
        raise KeyError(f"Unknown dataset candidate: {dataset}")
    return {"id": dataset, **DATASET_CANDIDATES[dataset]}

