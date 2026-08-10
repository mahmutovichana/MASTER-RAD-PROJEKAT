from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ExternalDocGuardRecord:
    record_id: str
    source_dataset: str
    repository: str | None
    commit_hash: str | None
    language: str | None
    code_before: str | None
    code_after: str | None
    code_diff: str | None
    doc_before: str | None
    doc_after: str | None
    doc_diff: str | None
    docs_update_required: bool | None
    label_source: str
    target_kind: str | None
    target_path: str | None
    scenario_type: str
    split: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


REQUIRED_FIELDS = set(ExternalDocGuardRecord.__dataclass_fields__)


def validate_record(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(row))
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if row.get("docs_update_required") not in {True, False, None}:
        errors.append("docs_update_required must be true, false, or null")
    if row.get("label_source") not in {
        "strong_paired_code_doc_change",
        "strong_positive_code_doc_cochange",
        "strong_external_inconsistent_comment",
        "strong_external_consistent_comment",
        "incomplete_mapping",
        "strong_dataset_negative",
        "weak_negative_sampling",
        "unknown",
    }:
        errors.append("label_source should explicitly distinguish strong and weak labels")
    return errors
