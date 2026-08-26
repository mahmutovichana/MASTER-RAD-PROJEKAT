from __future__ import annotations

import re
from typing import Any

from docguard_llm_v2.change_analyzer import normalize_text
from docguard_llm_v2.schemas import SafetyResult, SafetyViolation, WriterCandidate


META_RE = re.compile(r"^\s*(?:[-*]\s*)?(?:document|mention|describe|explain|add documentation|update documentation|should document|needs to document|need to document)\b", re.I)
SECURITY_TERMS = {"oauth", "jwt", "bearer", "token", "admin", "permission", "role", "authentication", "authorization"}


def is_meta_instruction(text: str) -> bool:
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text or "")
    return any(META_RE.search(sentence.strip()) for sentence in sentences if sentence.strip())


def extract_atoms(text: str) -> list[str]:
    patterns = [
        r"https?://[^\s)]+",
        r"\b(?:GET|POST|PUT|PATCH|DELETE)\s+/[A-Za-z0-9_./:{}-]+",
        r"\b(?:GET|POST|PUT|PATCH|DELETE)\b",
        r"\b[1-5]\d\d\b",
        r"\b[A-Z][A-Z0-9_]{2,}\b",
        r"\b\d+(?:\.\d+){1,3}\b",
        r"`([^`]+)`",
        r"--[A-Za-z0-9_-]+",
        r"\b[A-Za-z0-9_.-]+\.(?:md|py|ts|tsx|js|json|yml|yaml|toml)\b",
    ]
    atoms: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text or ""):
            atom = match.group(1) if match.lastindex else match.group(0)
            if atom and atom not in atoms:
                atoms.append(atom)
    return atoms


def supported(atom: str, evidence: str) -> bool:
    return normalize_text(atom).lower() in normalize_text(evidence).lower()


def verify_candidate(*, candidate: WriterCandidate, retrieved_paths: list[str], code_diff: str, docs_before: str, validated_inferences: list[dict[str, Any]], forbidden_inputs: dict[str, Any] | None = None) -> SafetyResult:
    violations: list[SafetyViolation] = []
    if forbidden_inputs:
        present = [key for key, value in forbidden_inputs.items() if value]
        if present:
            violations.append(SafetyViolation("forbidden_generation_input", "Outcome or label fields are not allowed in Stage 3 V2 generation.", ", ".join(present)))
    if not candidate.patch_markdown.strip():
        violations.append(SafetyViolation("empty_patch", "Positive prediction requires a non-empty documentation patch.", ""))
    if candidate.target_document_path not in retrieved_paths:
        violations.append(SafetyViolation("target_not_retrieved", "Target document must be one of the retrieved candidates.", candidate.target_document_path))
    if is_meta_instruction(candidate.patch_markdown):
        violations.append(SafetyViolation("meta_instruction", "Patch is an instruction about documentation rather than documentation prose.", candidate.patch_markdown.strip()))
    evidence_quotes = "\n".join(str(item.get("evidence_quote") or "") for item in validated_inferences)
    evidence = "\n".join([code_diff, docs_before, evidence_quotes])
    supported_atoms: list[str] = []
    unsupported_atoms: list[str] = []
    for atom in extract_atoms(candidate.patch_markdown):
        if supported(atom, evidence):
            supported_atoms.append(atom)
        else:
            unsupported_atoms.append(atom)
            violations.append(SafetyViolation("unsupported_fact", "Concrete factual atom is not supported by available evidence.", atom))
    patch_lower = candidate.patch_markdown.lower()
    evidence_lower = evidence.lower()
    for term in sorted(SECURITY_TERMS):
        if term in patch_lower and term not in evidence_lower:
            violations.append(SafetyViolation("unsupported_security_claim", "Security/authentication claim is not supported by evidence.", term))
    return SafetyResult("fail" if violations else "pass", violations, supported_atoms, unsupported_atoms)

