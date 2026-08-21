from __future__ import annotations

import re
from pathlib import Path

from docguard_runtime.schemas import SECTIONS


def _split_words(value: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return [word.lower() for word in re.split(r"[^A-Za-z0-9]+", spaced) if word]


def _property_name_for_env(body: str, env_var: str) -> str | None:
    match = re.search(rf"\b([A-Za-z][A-Za-z0-9_]*)\s*:\s*process\.env\.{re.escape(env_var)}\b", body)
    if match:
        return match.group(1)
    return None


def _humanize_env_var(name: str, body: str = "") -> str:
    property_name = _property_name_for_env(body, name)
    words = _split_words(property_name or name)
    if words:
        if words[-1] in {"flag", "enabled"}:
            return "controls whether " + " ".join(words[:-1] or words) + " is enabled"
        if words[-1] in {"mode", "type", "strategy"}:
            return "sets the " + " ".join(words)
        if words[-1] in {"window", "duration", "timeout", "ttl", "interval"}:
            return "sets the " + " ".join(words)
        if words[-1] in {"port"}:
            return "sets the " + " ".join(words)
        return "configures " + " ".join(words)
    return "configures this runtime setting"


def _extract_env_default(body: str, env_var: str) -> str | None:
    pattern = rf"process\.env\.{re.escape(env_var)}\s*(?:\|\||\?\?)\s*['\"]([^'\"]+)['\"]"
    match = re.search(pattern, body)
    if match:
        return match.group(1)
    assignment = re.search(rf"\b{re.escape(env_var)}\s*=\s*['\"]?([^'\"\s,;]+)", body)
    if assignment:
        return assignment.group(1)
    return None


def _semantic_line(body: str) -> str:
    return body.strip().rstrip(",;").strip()


def _env_fact(env_var: str, body: str) -> str:
    description = _humanize_env_var(env_var, body)
    default = _extract_env_default(body, env_var)
    if default:
        return f"`{env_var}` {description} and defaults to `{default}`."
    return f"`{env_var}` {description}."


def _route_fact(method: str, route_path: str) -> str:
    noun = route_path.strip("/").replace("-", " ")
    if not noun:
        noun = "root endpoint"
    if method == "GET":
        return f"`GET {route_path}` returns {noun} information."
    if method == "POST":
        return f"`POST {route_path}` creates a new {noun.rstrip('s')} resource."
    if method == "PATCH":
        return f"`PATCH {route_path}` updates an existing {noun.rstrip('s')} resource."
    if method == "DELETE":
        return f"`DELETE {route_path}` removes an existing {noun.rstrip('s')} resource."
    return f"`{method} {route_path}` is available."


def extract_facts(code_diff: str, scenario_type: str, docs_text: str = "") -> list[str]:
    facts: list[str] = []
    documented = docs_text.lower()
    removed_semantic_lines = {
        _semantic_line(line.strip()[1:])
        for line in code_diff.splitlines()
        if line.strip().startswith("-") and not line.strip().startswith("---")
    }
    for line in code_diff.splitlines():
        stripped = line.strip()
        if not stripped.startswith("+") or stripped.startswith("+++"):
            continue
        body = stripped[1:].strip()
        if body in {"});", "};", "}", "};,"}:
            continue
        if _semantic_line(body) in removed_semantic_lines:
            continue
        env_matches = re.findall(r"\b([A-Z][A-Z0-9_]{3,})\b", body)
        route_match = re.search(r"(?:router|app)\.(get|post|put|patch|delete)\(['\"]([^'\"]+)", body)
        status_match = re.search(r"res\.status\((\d{3})\)", body)
        if env_matches:
            for env_var in env_matches:
                default = _extract_env_default(body, env_var)
                if env_var.lower() not in documented:
                    facts.append(_env_fact(env_var, body))
                elif default and default.lower() not in documented:
                    facts.append(f"`{env_var}` defaults to `{default}`.")
        elif route_match:
            method = route_match.group(1).upper()
            route_path = route_match.group(2)
            if route_path.lower() not in documented or method.lower() not in documented:
                facts.append(_route_fact(method, route_path))
        elif status_match and status_match.group(1) not in documented:
            facts.append(f"Returns HTTP `{status_match.group(1)}` on success.")
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
    path = workspace / target_file
    docs_text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    facts = extract_facts(code_diff, scenario_type, docs_text)
    text = "\n".join(f"- {fact}" for fact in facts)
    preview = f"## {section_name}\n\n{text}\n"
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
