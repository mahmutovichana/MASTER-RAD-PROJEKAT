from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any


DOC_FILE_BY_CATEGORY = {
    "api_reference": "docs/api.md",
    "model_contract": "docs/models.md",
    "configuration": "docs/configuration.md",
    "testing_instructions": "docs/testing.md",
    "workflow_documentation": "docs/workflows.md",
    "architecture_flow": "docs/architecture.md",
    "developer_setup": "docs/developer-setup.md",
    "changelog": "CHANGELOG.md",
    "no_update": "",
}


SECTION_BY_CATEGORY = {
    "api_reference": "API Reference",
    "model_contract": "Data Models",
    "configuration": "Configuration",
    "testing_instructions": "Testing",
    "workflow_documentation": "Workflows",
    "architecture_flow": "Architecture",
    "developer_setup": "Developer Setup",
    "changelog": "Unreleased",
    "no_update": "Documentation",
}


PUBLIC_CONTRACT_FILE_HINTS = {
    "schema",
    "schemas",
    "dto",
    "types",
    "model",
    "models",
    "prisma",
    "migration",
    "migrations",
    "openapi",
    "api",
    "sdk",
    "config",
    "settings",
    "package.json",
    "requirements.txt",
    "dockerfile",
    "docker-entrypoint",
    "toml",
    "yaml",
    "yml",
}


INTERNAL_ONLY_FILE_HINTS = {
    "test",
    "tests",
    "__tests__",
    "spec",
    "mock",
    "mocks",
}


def _added_lines(diff: str) -> list[str]:
    return [
        line[1:].strip()
        for line in diff.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]


def _removed_lines(diff: str) -> list[str]:
    return [
        line[1:].strip()
        for line in diff.splitlines()
        if line.startswith("-") and not line.startswith("---")
    ]


def _changed_lines(diff: str) -> list[str]:
    return _added_lines(diff) + _removed_lines(diff)


def _norm_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def _path_parts(path: str) -> set[str]:
    normalized = _norm_path(path).lower()
    parts = set(PurePosixPath(normalized).parts)
    parts.update(part for part in re.split(r"[/_.\-]+", normalized) if part)
    return parts


def _files_blob(files: list[str]) -> str:
    return "\n".join(_norm_path(path).lower() for path in files)


def _diff_blob(diff: str) -> str:
    return diff.lower()


def _has_any(text: str, needles: set[str] | list[str] | tuple[str, ...]) -> bool:
    return any(needle.lower() in text for needle in needles)


def _is_comment_or_whitespace_only(diff: str) -> bool:
    changed = _changed_lines(diff)
    if not changed:
        return True

    meaningful: list[str] = []
    for line in changed:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("//", "#", "/*", "*", "<!--")):
            continue
        if stripped in {"{", "}", "};", ")", "(", ",", ";"}:
            continue
        meaningful.append(stripped)

    return not meaningful


def _looks_like_tests_only(files: list[str]) -> bool:
    if not files:
        return False
    for path in files:
        parts = _path_parts(path)
        normalized = _norm_path(path).lower()
        if not (parts & INTERNAL_ONLY_FILE_HINTS or normalized.endswith((".spec.ts", ".test.ts", "_test.py", "test.py"))):
            return False
    return True


def _extract_env_vars(diff: str) -> list[str]:
    vars_: list[str] = []

    patterns = [
        r"\bprocess\.env\.([A-Z][A-Z0-9_]{2,})\b",
        r"\bos\.getenv\(['\"]([A-Z][A-Z0-9_]{2,})['\"]",
        r"\benv\[['\"]([A-Z][A-Z0-9_]{2,})['\"]\]",
        r"^\+\s*([A-Z][A-Z0-9_]{2,})\s*=",
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, diff, flags=re.MULTILINE):
            value = match.group(1)
            if value not in vars_:
                vars_.append(value)

    return vars_


def _extract_config_keys(diff: str) -> list[str]:
    keys: list[str] = []

    for line in _added_lines(diff):
        for match in re.finditer(r"\b([a-zA-Z_][a-zA-Z0-9_]{2,})\s*[:=]\s*['\"]?([A-Za-z0-9_./:-]+)?", line):
            key = match.group(1)
            if key.lower() in {"const", "let", "var", "return", "import", "export", "from"}:
                continue
            if key not in keys:
                keys.append(key)

    return keys[:20]


def _extract_public_fields(diff: str) -> list[str]:
    fields: list[str] = []

    for line in _added_lines(diff):
        stripped = line.strip()

        # TypeScript / JavaScript exported public contracts:
        # export type AgentNextStep = { ... }
        # export interface AgentSummary { ... }
        # export class PaymentWarning { ... }
        for match in re.finditer(
            r"\bexport\s+(?:type|interface|class|enum)\s+([A-Za-z_][A-Za-z0-9_]*)\b",
            stripped,
        ):
            name = match.group(1)
            if name not in fields:
                fields.append(name)

        # Non-exported public-looking contracts:
        # type AgentNextStep = { ... }
        # interface AgentSummary { ... }
        # class PaymentWarning { ... }
        for match in re.finditer(
            r"^(?:type|interface|class|enum)\s+([A-Za-z_][A-Za-z0-9_]*)\b",
            stripped,
        ):
            name = match.group(1)
            if name not in fields:
                fields.append(name)

        # Object / JSON / DTO fields:
        # nextAction: string
        # "pluginInstallUrlPrefix": { ... }
        # reviewerId?: string
        for match in re.finditer(
            r"^[\"']?([A-Za-z_][A-Za-z0-9_]*)[\"']?\??\s*[:=]\s*[A-Za-z0-9_\"'{\[]",
            stripped,
        ):
            name = match.group(1)
            if name.lower() in {"type", "const", "let", "var", "return", "import", "export", "from"}:
                continue
            if name not in fields:
                fields.append(name)

        # Inline export list:
        # export type { AgentNextStep, AgentSummary }
        export_list = re.search(r"\bexport\s+type\s+\{([^}]+)\}", stripped)
        if export_list:
            for part in re.split(r"[, ]+", export_list.group(1)):
                cleaned = part.strip().strip("{}").strip()
                if not cleaned:
                    continue
                if cleaned not in fields:
                    fields.append(cleaned)

    return fields[:30]

def _extract_routes_or_endpoints(diff: str) -> list[str]:
    endpoints: list[str] = []

    route_patterns = [
        r"\b(?:router|app)\.(get|post|put|patch|delete)\(['\"]([^'\"]+)",
        r"@\w+\.(get|post|put|patch|delete)\(['\"]([^'\"]+)",
        r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[A-Za-z0-9_./{}:-]+)",
        r"['\"](/[A-Za-z0-9_./{}:-]+)['\"]",
    ]

    for pattern in route_patterns:
        for match in re.finditer(pattern, diff, flags=re.IGNORECASE):
            if len(match.groups()) >= 2:
                method_or_path = match.group(1)
                path = match.group(2)
                if path.startswith("/"):
                    value = f"{method_or_path.upper()} {path}" if method_or_path.lower() in {"get", "post", "put", "patch", "delete"} else path
                else:
                    value = path
            else:
                value = match.group(1)
            if value.startswith("/") or re.match(r"^(GET|POST|PUT|PATCH|DELETE)\s+/", value):
                if value not in endpoints:
                    endpoints.append(value)

    if "/metrics" in diff and "GET /metrics" not in endpoints:
        endpoints.append("GET /metrics")

    return endpoints[:20]


def _extract_commands(diff: str) -> list[str]:
    commands: list[str] = []

    patterns = [
        r"\b(npm run [A-Za-z0-9:_-]+)\b",
        r"\b(pnpm [A-Za-z0-9:_-]+)\b",
        r"\b(yarn [A-Za-z0-9:_-]+)\b",
        r"\b(pytest(?: [A-Za-z0-9_./:-]+)*)",
        r"\b(jest(?: [A-Za-z0-9_./:-]+)*)",
        r"\b(vitest(?: run)?(?: [A-Za-z0-9_./:-]+)*)",
        r"\b(docker compose [A-Za-z0-9_./:-]+)",
        r"\b(omind doctor)\b",
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, diff):
            command = match.group(1).strip()
            if command not in commands:
                commands.append(command)

    return commands[:20]


def _extract_defaults(diff: str) -> list[str]:
    defaults: list[str] = []

    for line in _added_lines(diff):
        patterns = [
            r"\|\|\s*['\"]([^'\"]+)['\"]",
            r"\?\?\s*['\"]([^'\"]+)['\"]",
            r"default\s*[:=]\s*['\"]?([A-Za-z0-9_./:-]+)",
            r"=\s*['\"]?([A-Za-z0-9_./:-]+)['\"]?\s*(?:#|//|$)",
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, line, flags=re.IGNORECASE):
                value = match.group(1)
                if len(value) <= 1:
                    continue
                if value not in defaults:
                    defaults.append(value)

    return defaults[:20]


def extract_real_case_signals(record: dict[str, Any]) -> dict[str, Any]:
    files = [str(path) for path in record.get("changed_files") or record.get("code_changed_files") or []]
    diff = str(record.get("code_diff") or "")
    docs_before = str(record.get("docs_before") or record.get("docs_before_excerpt") or "")

    files_text = _files_blob(files)
    diff_text = _diff_blob(diff)
    docs_text = docs_before.lower()

    env_vars = _extract_env_vars(diff)
    config_keys = _extract_config_keys(diff)
    public_fields = _extract_public_fields(diff)
    endpoints = _extract_routes_or_endpoints(diff)
    commands = _extract_commands(diff)
    defaults = _extract_defaults(diff)

    file_parts: set[str] = set()
    for path in files:
        file_parts.update(_path_parts(path))

    schema_or_model_change = bool(
        file_parts & {"schema", "schemas", "dto", "types", "model", "models", "prisma", "migration", "migrations", "openapi", "sdk"}
        or public_fields
        or _has_any(diff_text, {"json schema", "z.object", "pydantic", "dataclass", "interface ", "type ", "export type", "export interface"})
    )

    endpoint_change = bool(
        endpoints
        or _has_any(diff_text, {"openapi", "swagger", "/metrics", "fastapi", "flask", "express", "router.", "app.get", "app.post"})
    )

    configuration_change = bool(
        env_vars
        or file_parts & {"config", "configuration", "settings", "toml", "yaml", "yml", "env"}
        or files_text.endswith(".env")
        or _has_any(diff_text, {"process.env", "os.getenv", "config.", "settings.", "metrics_enabled", "metrics_token"})
    )

    testing_or_verification_change = bool(
        commands
        or file_parts & {"test", "tests", "spec"}
        and _has_any(diff_text, {"doctor", "verification", "acceptance", "canonical", "install", "pytest", "jest", "vitest"})
    )

    workflow_change = bool(
        file_parts & {"workflow", "workflows", ".github", "systemd", "docker", "dockerfile"}
        or _has_any(diff_text, {"cron", "schedule", "timer", "systemd", "docker compose", "dockerfile", "entrypoint", "workflow"})
    )

    developer_setup_change = bool(
        file_parts & {"package", "requirements", "dockerfile", "docker-entrypoint", "setup", "install"}
        or "package.json" in files_text
        or "requirements.txt" in files_text
        or _has_any(diff_text, {"npm run", "pip install", "docker compose", "requirements.txt", "entrypoint"})
    )

    architecture_change = bool(
        file_parts & {"architecture", "orchestrator", "imports", "service"}
        or _has_any(diff_text, {"orchestrator", "pipeline", "service", "payment", "signer", "runtime", "compatibility"})
    )

    comments_or_formatting_only = _is_comment_or_whitespace_only(diff)
    tests_only = _looks_like_tests_only(files)

    public_signal_count = sum(
        bool(value)
        for value in [
            schema_or_model_change,
            endpoint_change,
            configuration_change,
            testing_or_verification_change,
            workflow_change,
            developer_setup_change,
            architecture_change,
        ]
    )

    likely_no_update = bool(
        comments_or_formatting_only
        or (tests_only and not testing_or_verification_change and not schema_or_model_change)
    )

    docs_already_cover_change = False
    visible_tokens = env_vars + public_fields + endpoints + commands + defaults
    if visible_tokens:
        docs_already_cover_change = all(str(token).lower() in docs_text for token in visible_tokens[:5])

    return {
        "env_vars": env_vars,
        "config_keys": config_keys,
        "public_fields": public_fields,
        "endpoints": endpoints,
        "commands": commands,
        "defaults": defaults,
        "schema_or_model_change": schema_or_model_change,
        "endpoint_change": endpoint_change,
        "configuration_change": configuration_change,
        "testing_or_verification_change": testing_or_verification_change,
        "workflow_change": workflow_change,
        "developer_setup_change": developer_setup_change,
        "architecture_change": architecture_change,
        "comments_or_formatting_only": comments_or_formatting_only,
        "tests_only": tests_only,
        "likely_no_update": likely_no_update,
        "docs_already_cover_change": docs_already_cover_change,
        "public_signal_count": public_signal_count,
        "visible_tokens": visible_tokens[:30],
    }


def choose_real_category(signals: dict[str, Any]) -> tuple[str, str]:
    """
    Return (doc_category, scenario_type).

    Priority is intentionally broad and project-agnostic:
    real GitHub PRs rarely follow the synthetic Express-only route patterns.
    """
    if signals["endpoint_change"]:
        return "api_reference", "real_api_or_endpoint_contract_change"

    if signals["configuration_change"]:
        return "configuration", "real_configuration_or_environment_change"

    if signals["schema_or_model_change"]:
        return "model_contract", "real_schema_or_model_contract_change"

    if signals["testing_or_verification_change"]:
        return "testing_instructions", "real_testing_or_verification_change"

    if signals["workflow_change"]:
        return "workflow_documentation", "real_workflow_or_deployment_change"

    if signals["architecture_change"]:
        return "architecture_flow", "real_architecture_or_service_flow_change"

    if signals["developer_setup_change"]:
        return "developer_setup", "real_developer_setup_change"

    return "no_update", "real_no_documentation_update_detected"


def compose_real_patch(category: str, scenario: str, signals: dict[str, Any]) -> str | None:
    if category == "no_update":
        return None

    section = SECTION_BY_CATEGORY.get(category, "Documentation")
    tokens = signals.get("visible_tokens") or []

    if category == "api_reference":
        endpoints = signals.get("endpoints") or []
        if endpoints:
            return f"@@ {section}\n+Document the public API change for `{endpoints[0]}`."
        return f"@@ {section}\n+Document the public API contract change detected in the code diff."

    if category == "configuration":
        env_vars = signals.get("env_vars") or []
        defaults = signals.get("defaults") or []
        config_keys = signals.get("config_keys") or []
        if env_vars and defaults:
            return f"@@ {section}\n+Document `{env_vars[0]}` and its visible default value `{defaults[0]}`."
        if env_vars:
            return f"@@ {section}\n+Document the new or changed environment variable `{env_vars[0]}`."
        if config_keys:
            return f"@@ {section}\n+Document the changed configuration setting `{config_keys[0]}`."
        return f"@@ {section}\n+Document the configuration behavior changed in the code diff."

    if category == "model_contract":
        fields = signals.get("public_fields") or []
        if fields:
            field_list = ", ".join(f"`{field}`" for field in fields[:6])
            return f"@@ {section}\n+Document the changed public data contract fields: {field_list}."
        if tokens:
            return f"@@ {section}\n+Document the changed public data contract around `{tokens[0]}`."
        return f"@@ {section}\n+Document the changed public data/schema contract."

    if category == "testing_instructions":
        commands = signals.get("commands") or []
        if commands:
            return f"@@ {section}\n+Document the changed verification command `{commands[0]}`."
        return f"@@ {section}\n+Document the changed installation or verification workflow."

    if category == "workflow_documentation":
        if tokens:
            return f"@@ {section}\n+Document the changed workflow behavior around `{tokens[0]}`."
        return f"@@ {section}\n+Document the changed workflow or deployment behavior."

    if category == "architecture_flow":
        if tokens:
            return f"@@ {section}\n+Document the changed service or architecture flow around `{tokens[0]}`."
        return f"@@ {section}\n+Document the changed service or architecture flow."

    if category == "developer_setup":
        commands = signals.get("commands") or []
        if commands:
            return f"@@ {section}\n+Document the changed developer setup command `{commands[0]}`."
        return f"@@ {section}\n+Document the changed developer setup or dependency flow."

    return f"@@ {section}\n+Document the visible project behavior changed in the code diff."


def predict_real_case_runtime(record: dict[str, Any]) -> dict[str, Any]:
    signals = extract_real_case_signals(record)

    if signals["likely_no_update"]:
        docs_required = False
        category = "no_update"
        scenario = "real_no_documentation_update_detected"
        confidence = 0.72
    elif signals["docs_already_cover_change"] and signals["public_signal_count"] <= 1:
        docs_required = False
        category = "no_update"
        scenario = "real_docs_already_cover_visible_change"
        confidence = 0.74
    elif signals["public_signal_count"] > 0:
        docs_required = True
        category, scenario = choose_real_category(signals)
        confidence = min(0.9, 0.58 + (0.08 * signals["public_signal_count"]))
    else:
        docs_required = False
        category = "no_update"
        scenario = "real_unknown_or_internal_change"
        confidence = 0.55

    target_file = DOC_FILE_BY_CATEGORY.get(category, "")
    patch = compose_real_patch(category, scenario, signals) if docs_required else None

    enabled_signal_names = [
        name
        for name in [
            "schema_or_model_change",
            "endpoint_change",
            "configuration_change",
            "testing_or_verification_change",
            "workflow_change",
            "developer_setup_change",
            "architecture_change",
            "comments_or_formatting_only",
            "tests_only",
            "docs_already_cover_change",
        ]
        if signals.get(name)
    ]

    return {
        "record_id": record["id"],
        "docs_update_required": docs_required,
        "scenario_type": scenario,
        "doc_category": category,
        "target_doc_file": target_file,
        "generated_doc_patch": patch,
        "router_output": {
            "docs_update_required": docs_required,
            "candidate_doc_categories": [category],
            "candidate_target_doc_files": [target_file] if target_file else [],
            "candidate_scenario_types": [scenario],
            "router_confidence": confidence,
            "router_reason": (
                "Real-case detector used only code_changed_files, code_diff_excerpt, "
                "docs_before_excerpt, and language. "
                f"Signals: {', '.join(enabled_signal_names) or 'none'}."
            ),
            "signals": enabled_signal_names,
            "real_case_visible_tokens": signals.get("visible_tokens") or [],
        },
        "router_ml_agree": False,
        "router_llm_agree": False,
        "deterministic_patch_used": bool(patch),
        "llm_patch_rewrite_used": False,
        "corrected_target_doc_file": False,
        "invalid_source_file_target": False,
        "latency_seconds": 0.0,
        "decision_source": "real_case_detector",
        "real_case_signals": signals,
    }