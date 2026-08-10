from __future__ import annotations

from pathlib import Path


LIKELY_DOCS = [
    "docs/configuration.md",
    "docs/api.md",
    "docs/developer-setup.md",
    "docs/workflows.md",
    "docs/architecture.md",
    "docs/models.md",
    "docs/testing.md",
    "CHANGELOG.md",
]


def docs_before_excerpt(workspace: Path, max_chars: int = 2400) -> str:
    chunks = []
    for rel in LIKELY_DOCS:
        path = workspace / rel
        if path.exists() and path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            chunks.append(f"--- {rel} ---\n{text[:max_chars // 2]}")
        if sum(len(chunk) for chunk in chunks) >= max_chars:
            break
    return "\n\n".join(chunks)[:max_chars]

