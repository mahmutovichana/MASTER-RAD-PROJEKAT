from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SupportedInference:
    claim: str
    evidence_source: str
    evidence_quote: str
    evidence_valid: bool = False


@dataclass
class ChangeAnalysis:
    change_summary: str
    behavior_before: str
    behavior_after: str
    developer_or_user_impact: str
    documentation_impact: str
    supported_inferences: list[SupportedInference] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)


@dataclass
class DocumentCandidate:
    path: str
    excerpt: str
    source_ref: str = ""
    score: float = 0.0


@dataclass
class WriterCandidate:
    target_document_path: str
    target_section: str
    patch_markdown: str
    writer_confidence: float = 0.0


@dataclass
class SafetyViolation:
    code: str
    message: str
    offending_text: str


@dataclass
class SafetyResult:
    safety_status: str
    violations: list[SafetyViolation]
    supported_atoms: list[str]
    unsupported_atoms: list[str]


def asdict_shallow(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: asdict_shallow(getattr(value, key)) for key in value.__dataclass_fields__}
    if isinstance(value, list):
        return [asdict_shallow(item) for item in value]
    return value

