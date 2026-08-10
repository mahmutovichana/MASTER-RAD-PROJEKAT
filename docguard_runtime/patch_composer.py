from __future__ import annotations

import re
from pathlib import Path

from docguard_runtime.schemas import SECTIONS


def extract_facts(code_diff: str, scenario_type: str) -> list[str]:
    facts: list[str] = []
    for line in code_diff.splitlines():
        stripped = line.strip()
        if not stripped.startswith("+") or stripped.startswith("+++"):
            continue
        body = stripped[1:].strip()
        env_match = re.search(r"\b([A-Z][A-Z0-9_]{3,})\b", body)
        route_match = re.search(r"router\.(get|post|put|patch|delete)\(['\"]([^'\"]+)", body)
        if env_match:
            facts.append(f"Document the `{env_match.group(1)}` configuration value.")
        elif route_match:
            facts.append(f"Document `{route_match.group(1).upper()} {route_match.group(2)}`.")
        elif "z." in body or ".min(" in body or ".max(" in body:
            facts.append("Document the updated request validation rule.")
        elif body and len(body) < 160:
            facts.append(f"Reflect code change: `{body}`.")
        if len(facts) >= 3:
            break
    if not facts:
        facts.append(f"Document the `{scenario_type}` behavior change.")
    return facts


def compose_patch(workspace: Path, target_file: str, scenario_type: str, doc_category: str, code_diff: str, section: str | None = None) -> dict:
    section_name = section or SECTIONS.get(target_file, "Documentation")
    facts = extract_facts(code_diff, scenario_type)
    text = "\n".join(f"- {fact}" for fact in facts)
    preview = f"## {section_name}\n\n{text}\n"
    path = workspace / target_file
    if not path.exists():
        mode = "append_to_file"
    elif re.search(rf"^#+\s+{re.escape(section_name)}\s*$", path.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE):
        mode = "append_to_section"
    else:
        mode = "append_to_file"
    return {
        "file": target_file,
        "mode": mode,
        "section": section_name,
        "text": text,
        "preview": preview,
    }


def apply_patch(workspace: Path, patch: dict) -> Path:
    rel = patch["file"]
    path = workspace / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    section = patch.get("section") or "Documentation"
    text = patch.get("text") or ""
    if not path.exists():
        path.write_text(f"# {section}\n\n{text}\n", encoding="utf-8")
        return path
    content = path.read_text(encoding="utf-8", errors="ignore")
    heading = re.compile(rf"^(#+\s+{re.escape(section)}\s*)$", re.MULTILINE)
    match = heading.search(content)
    if not match:
        addition = f"\n\n## {section}\n\n{text}\n"
        path.write_text(content.rstrip() + addition, encoding="utf-8")
        return path
    next_heading = re.search(r"^#{1,6}\s+", content[match.end() :], re.MULTILINE)
    insert_at = len(content) if not next_heading else match.end() + next_heading.start()
    insertion = f"\n{text}\n"
    path.write_text(content[:insert_at].rstrip() + insertion + "\n" + content[insert_at:].lstrip(), encoding="utf-8")
    return path

