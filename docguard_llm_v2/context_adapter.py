from __future__ import annotations

from typing import Any, Iterable


FORBIDDEN_GENERATION_KEYS = {
    "confirmation",
    "docs_after",
    "docs_after_excerpt",
    "docs_diff",
    "docs_diff_excerpt",
    "gold_docs_update_required",
    "gold_doc_category",
    "gold_patch_summary",
    "gold_target_doc_file",
    "gold_target_section",
    "human_docs_update_required",
    "human_doc_category",
    "human_label_notes",
    "manual_label_notes",
    "suggested_docs_update_required",
    "suggested_doc_category",
    "suggested_notes",
    "label_source",
    "provenance_tier",
    "supervision_source",
    "controlled_design_supervision",
    "independent_human_reviewed",
    "review_status",
    "review_row_hash",
    "review_context_hash",
}


def _candidate(item: Any) -> dict[str, str] | None:
    if not isinstance(item, dict):
        return None
    path = str(item.get("path") or "").strip().replace("\\", "/")
    excerpt = str(item.get("excerpt") or "").strip()
    source_ref = str(item.get("source_ref") or "").strip()
    if not path or not excerpt:
        return None
    return {"path": path, "excerpt": excerpt, "source_ref": source_ref}


def _legacy_lists(row: dict[str, Any]) -> Iterable[list[Any]]:
    direct = row.get("documentation_context_candidates")
    if isinstance(direct, list):
        yield direct
    for parent_key in ("generator_context", "retrieval_context"):
        parent = row.get(parent_key)
        if isinstance(parent, dict):
            nested = parent.get("documentation_context_candidates")
            if isinstance(nested, list):
                yield nested


def normalize_documentation_context(row: dict[str, Any]) -> list[dict[str, str]]:
    """Return only canonical pre-change retrieval candidates.

    The adapter deliberately reads an exact allowlist. It never promotes
    ``docs_before_excerpt`` into a target because that excerpt has no canonical
    document path.
    """
    candidates: list[dict[str, str]] = []
    for index in range(1, 13):
        prefix = f"doc_context_{index:02d}"
        item = _candidate(
            {
                "path": row.get(f"{prefix}_path"),
                "excerpt": row.get(f"{prefix}_excerpt"),
                "source_ref": row.get(f"{prefix}_source_ref"),
            }
        )
        if item is not None:
            candidates.append(item)
    for items in _legacy_lists(row):
        for raw in items:
            item = _candidate(raw)
            if item is not None:
                candidates.append(item)

    # Sorting before deduplication makes the result independent of legacy-list
    # order. Exact canonical triples are the deduplication identity.
    ordered = sorted(candidates, key=lambda item: (item["path"].casefold(), item["path"], item["excerpt"], item["source_ref"]))
    unique: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for item in ordered:
        key = (item["path"], item["excerpt"], item["source_ref"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def assert_generation_payload_safe(value: Any, *, location: str = "generation_payload") -> None:
    if isinstance(value, dict):
        leaked = FORBIDDEN_GENERATION_KEYS & set(value)
        if leaked:
            raise ValueError(f"Forbidden fields in {location}: {sorted(leaked)}")
        for key, nested in value.items():
            assert_generation_payload_safe(nested, location=f"{location}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            assert_generation_payload_safe(nested, location=f"{location}[{index}]")
