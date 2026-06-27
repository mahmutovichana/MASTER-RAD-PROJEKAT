from __future__ import annotations

import re
from dataclasses import dataclass, field


HTTP_METHODS = {"get", "post", "put", "patch", "delete"}
ENDPOINT_SUFFIX_DESCRIPTIONS = {
    "": "Returns a single {item} by id",
    "audit": "Returns audit details for a single {item}",
    "summary": "Returns a compact summary for a single {item}",
    "history": "Returns change history for a single {item}",
    "status": "Returns current status details for a single {item}",
    "metrics": "Returns usage metrics for a single {item}",
    "owner": "Returns owner details for a single {item}",
    "timeline": "Returns timeline events for a single {item}",
    "attachments": "Returns attachments for a single {item}",
    "eligibility": "Returns eligibility checks for a single {item}",
}


@dataclass
class DiffFacts:
    scenario_signals: set[str] = field(default_factory=set)
    method: str | None = None
    route_path: str | None = None
    full_path: str | None = None
    response_status: str | None = None
    endpoint_description: str | None = None
    field: str | None = None
    old_min: int | None = None
    new_min: int | None = None
    middleware: str | None = None
    auth_description: str | None = None
    module: str | None = None
    target_section: str | None = None
    target_doc_file: str = "docs/api.md"


def extract_module(record: dict) -> str | None:
    for changed_file in record.get("changed_files", []):
        match = re.search(r"src/modules/([^/\\]+)/", changed_file)
        if match:
            return match.group(1)
    return None


def title_from_module(module: str | None) -> str | None:
    if not module:
        return None
    return module.replace("-", " ").replace("_", " ").title()


def split_camel(value: str) -> list[str]:
    return re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)", value)


def item_from_handler(handler: str | None, module: str | None) -> str:
    if handler and handler.startswith("get"):
        name = handler[3:]
        for suffix in [
            "Eligibility",
            "Attachments",
            "Timeline",
            "Metrics",
            "History",
            "Summary",
            "Status",
            "Audit",
            "Owner",
        ]:
            if name.endswith(suffix):
                name = name[: -len(suffix)]
                break
        words = split_camel(name)
        if words:
            return " ".join(word.lower() for word in words)
    if module:
        return module[:-1] if module.endswith("s") else module
    return "resource"


def full_path(module: str | None, route_path: str) -> str:
    if not module:
        return route_path
    if route_path == "/":
        return f"/{module}"
    return f"/{module}{route_path}"


def describe_endpoint(route_path: str, item: str) -> str:
    suffix = route_path.removeprefix("/:id").strip("/")
    template = ENDPOINT_SUFFIX_DESCRIPTIONS.get(suffix, "Returns {item} details")
    return template.format(item=item)


def describe_middleware(middleware: str | None) -> str | None:
    if not middleware:
        return None
    words = split_camel(middleware.removeprefix("require").removesuffix("Access"))
    if not words:
        return f"{middleware} middleware"
    return f"{' '.join(word.lower() for word in words)} access middleware"


def analyze_record(record: dict) -> DiffFacts:
    diff = record.get("code_diff", "")
    module = extract_module(record)
    facts = DiffFacts(
        module=module,
        target_section=record.get("target_section") or title_from_module(module),
        target_doc_file="docs/api.md",
    )

    auth_match = re.search(
        r"-(\w+Router)\.(get|post|put|patch|delete)\(\"([^\"]+)\",\s*(\w+)\);\n"
        r"\+(\w+Router)\.(get|post|put|patch|delete)\(\"([^\"]+)\",\s*(\w+),\s*(\w+)\);",
        diff,
    )
    if auth_match:
        facts.scenario_signals.add("changed_auth_requirement")
        facts.method = auth_match.group(6).upper()
        facts.route_path = auth_match.group(7)
        facts.full_path = full_path(module, facts.route_path)
        facts.middleware = auth_match.group(8)
        facts.auth_description = describe_middleware(facts.middleware)
        return facts

    validation_match = re.search(
        r"-\s+([A-Za-z_][A-Za-z0-9_]*):\s*z\.[^\n]*\.min\((\d+)\)[^\n]*\n"
        r"\+\s+\1:\s*z\.[^\n]*\.min\((\d+)\)",
        diff,
    )
    if validation_match:
        facts.scenario_signals.add("changed_validation_min")
        facts.field = validation_match.group(1)
        facts.old_min = int(validation_match.group(2))
        facts.new_min = int(validation_match.group(3))
        facts.method = "POST"
        facts.full_path = f"/{module}" if module else None
        return facts

    response_field_match = re.search(r"\+\s+([A-Za-z_][A-Za-z0-9_]*):\s*string;", diff)
    if response_field_match and "const saved" in diff:
        facts.scenario_signals.add("added_response_field")
        facts.field = response_field_match.group(1)
        facts.method = "POST"
        facts.full_path = f"/{module}" if module else None
        return facts

    route_match = re.search(r"\+(\w+Router)\.(get|post|put|patch|delete)\(\"([^\"]+)\",\s*(\w+)\);", diff)
    if route_match and route_match.group(2) in HTTP_METHODS:
        facts.scenario_signals.add("new_endpoint")
        facts.method = route_match.group(2).upper()
        facts.route_path = route_match.group(3)
        facts.full_path = full_path(module, facts.route_path)
        facts.response_status = "200 OK"
        status_match = re.search(r"\+\s*res\.status\((\d+)\)", diff)
        if status_match:
            status = status_match.group(1)
            facts.response_status = "201 Created" if status == "201" else f"{status} OK"
        handler = route_match.group(4)
        facts.endpoint_description = describe_endpoint(facts.route_path, item_from_handler(handler, module))
        return facts

    if re.search(r"-\s+const\s+\w+\s*=.+\n\+\s+const\s+\w+\s*=", diff):
        facts.scenario_signals.add("internal_refactor")

    return facts
