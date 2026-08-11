from __future__ import annotations

import re
from typing import Any


UNSUPPORTED_CLAIMS = {"oauth", "jwt", "admin"}


def extract_grounding_tokens(code_diff: str) -> list[str]:
    tokens: list[str] = []
    patterns = [
        r"['\"](/[A-Za-z0-9_:{}/-]+)['\"]",
        r"\b([A-Z][A-Z0-9_]{3,})\b",
        r"\b(npm run [A-Za-z0-9:_-]+)\b",
        r"^\+\s*([A-Za-z_][A-Za-z0-9_]*Id)\b",
        r"['\"](\*/\d+ \* \* \* \*)['\"]",
        r"res\.status\((\d{3})\)",
        r"requireRole\(['\"]([^'\"]+)['\"]\)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, code_diff, flags=re.MULTILINE):
            value = match.group(1)
            if value not in tokens:
                tokens.append(value)
    return tokens


def verify_patch(
    patch_text: str | None,
    docs_update_required: bool,
    target_doc_file: str,
    code_diff: str,
    docs_before: str,
) -> dict[str, Any]:
    warnings: list[str] = []
    if not docs_update_required:
        if patch_text:
            return {"verifier_status": "fail", "warnings": ["no-update prediction should not include a patch"], "grounded_tokens_found": []}
        return {"verifier_status": "pass", "warnings": [], "grounded_tokens_found": []}
    if not patch_text:
        return {"verifier_status": "fail", "warnings": ["positive prediction has empty patch"], "grounded_tokens_found": []}
    mentioned_files = {match for match in re.findall(r"(?:docs/[A-Za-z0-9_.-]+\.md|CHANGELOG\.md|README\.md)", patch_text)}
    outside = sorted(path for path in mentioned_files if path != target_doc_file)
    if outside:
        warnings.append(f"patch mentions filenames outside target: {', '.join(outside)}")
    context = f"{code_diff}\n{docs_before}".lower()
    patch_lower = patch_text.lower()
    for claim in sorted(UNSUPPORTED_CLAIMS):
        if claim in patch_lower and claim not in context:
            warnings.append(f"unsupported security/role claim: {claim}")
    tokens = extract_grounding_tokens(code_diff)
    found = [token for token in tokens if token.lower() in patch_lower]
    if tokens and not found:
        warnings.append("patch does not include any concrete token extracted from the diff")
    status = "fail" if any("outside target" in item or "unsupported" in item for item in warnings) else ("warn" if warnings else "pass")
    return {"verifier_status": status, "warnings": warnings, "grounded_tokens_found": found}
