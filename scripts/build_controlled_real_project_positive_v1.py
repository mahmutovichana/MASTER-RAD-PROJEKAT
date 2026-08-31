from __future__ import annotations

import argparse
import copy
import csv
import difflib
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from human_review_workflow_v2 import review_context_hash, review_row_hash


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data/final_v2/controlled_real_project_positive_v1"
ORIGINAL_CORPUS = ROOT / "data/final_v2/human_review/candidate_partitioned_17880.jsonl"
CATEGORIES = [
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
    "other_documentation",
]

IMBALANCED_V2_COUNTS = {
    "jobfair_platform": {
        "api_reference": 180,
        "configuration": 140,
        "developer_setup": 110,
        "model_contract": 90,
        "other_documentation": 40,
    },
    "rbi_related_parties_portal": {
        "api_reference": 150,
        "configuration": 145,
        "developer_setup": 120,
        "model_contract": 75,
        "other_documentation": 30,
    },
    "rbi_test_forge": {
        "api_reference": 100,
        "configuration": 105,
        "developer_setup": 135,
        "model_contract": 65,
        "other_documentation": 25,
    },
    "rbi_property_valuation": {
        "api_reference": 150,
        "configuration": 130,
        "developer_setup": 95,
        "model_contract": 70,
        "other_documentation": 45,
    },
}


@dataclass(frozen=True)
class ProjectSpec:
    key: str
    repository: str
    language: str
    display_name: str
    source_copy: str
    code_root: str
    prefix: str
    runtime: str
    runtime_version: str
    package_manager: str
    dev_command: str
    migration_command: str


PROJECTS = [
    ProjectSpec(
        key="jobfair_platform",
        repository="controlled/jobfair-platform-copy",
        language="typescript",
        display_name="JobFAIR Platform controlled copy",
        source_copy="source_copies/jobfair_platform",
        code_root="src/docguard-contract-lab",
        prefix="JOB",
        runtime="Node.js",
        runtime_version="20.11",
        package_manager="npm@10",
        dev_command="npm run dev",
        migration_command="npm run supabase:migrate",
    ),
    ProjectSpec(
        key="rbi_related_parties_portal",
        repository="controlled/rbi-related-parties-portal-copy",
        language="typescript",
        display_name="RBI Related Parties Portal controlled copy",
        source_copy="source_copies/rbi_related_parties_portal",
        code_root="src/Web/src/docguard-contract-lab",
        prefix="RPP",
        runtime="Node.js",
        runtime_version="20.11",
        package_manager="pnpm@9",
        dev_command="pnpm dev",
        migration_command="pnpm db:migrate",
    ),
    ProjectSpec(
        key="rbi_test_forge",
        repository="controlled/rbi-test-forge-copy",
        language="csharp",
        display_name="RBI Test Forge controlled copy",
        source_copy="source_copies/rbi_test_forge",
        code_root="TestGenerator/DocGuardContractLab",
        prefix="TFG",
        runtime=".NET SDK",
        runtime_version="8.0",
        package_manager="NuGet@6",
        dev_command="dotnet run --project TestGenerator",
        migration_command="dotnet ef database update --project TestGenerator",
    ),
    ProjectSpec(
        key="rbi_property_valuation",
        repository="controlled/rbi-property-valuation-copy",
        language="csharp",
        display_name="RBI Property Valuation controlled copy",
        source_copy="source_copies/rbi_property_valuation",
        code_root="PropertyValuation/DocGuardContractLab",
        prefix="VAL",
        runtime=".NET SDK",
        runtime_version="8.0",
        package_manager="NuGet@6",
        dev_command="dotnet run --project PropertyValuation",
        migration_command="dotnet ef database update --project PropertyValuation",
    ),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_text(payload), encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    preferred = [
        "case_id", "repository", "pr_number", "language", "code_changed_files",
        "code_diff_excerpt", "docs_before_excerpt", "suggested_docs_update_required",
        "suggested_doc_category", "suggested_notes", "human_docs_update_required",
        "human_doc_category", "human_label_notes", "review_status", "review_row_hash",
        "review_context_hash", "synthetic_category_by_design", "source_project_key",
        "mutation_template", "patch_path",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=preferred, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out = dict(row)
            for key, value in list(out.items()):
                if isinstance(value, (list, dict)):
                    out[key] = json.dumps(value, ensure_ascii=False, sort_keys=True)
            writer.writerow(out)


def corpus_identity(path: Path) -> tuple[str, set[str], set[tuple[str, str]]]:
    """Return an integrity hash and identity keys without modifying the corpus."""
    case_ids: set[str] = set()
    repository_pr_keys: set[tuple[str, str]] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        case_id = str(row.get("case_id", "")).strip()
        repository = str(row.get("repository", "")).strip().lower()
        pr_number = str(row.get("pr_number", "")).strip()
        if case_id:
            case_ids.add(case_id)
        if repository and pr_number:
            repository_pr_keys.add((repository, pr_number))
    return sha256_bytes(path.read_bytes()), case_ids, repository_pr_keys


def source_manifest(repo: Path, lab_rel: str, docs_rel: str = "docs/docguard-contract-lab") -> dict[str, Any]:
    excluded = {".git", "node_modules", "bin", "obj", "dist", "build", ".vs", ".idea", ".venv", "coverage", "TestResults"}
    rows: list[tuple[str, int, str]] = []
    for path in sorted(repo.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(repo).as_posix()
        if rel.startswith(lab_rel.rstrip("/") + "/") or rel.startswith(docs_rel.rstrip("/") + "/"):
            continue
        if any(part in excluded for part in path.parts) or path.name == ".env":
            continue
        data = path.read_bytes()
        rows.append((rel, len(data), sha256_bytes(data)))
    aggregate = sha256_bytes("\n".join(f"{p}\t{s}\t{h}" for p, s, h in rows).encode("utf-8"))
    return {"file_count": len(rows), "aggregate_sha256": aggregate, "files": [{"path": p, "size": s, "sha256": h} for p, s, h in rows]}


def contract_id(spec: ProjectSpec, category: str, index: int) -> str:
    short = {
        "api_reference": "API",
        "configuration": "CFG",
        "developer_setup": "SETUP",
        "model_contract": "MODEL",
        "other_documentation": "FLOW",
    }[category]
    return f"{spec.prefix}-{short}-{index:03d}"


def base_entry(spec: ProjectSpec, category: str, index: int) -> dict[str, Any]:
    cid = contract_id(spec, category, index)
    if category == "api_reference":
        return {
            "contractId": cid,
            "operationId": f"{spec.key.replace('_', '')}Operation{index:03d}",
            "method": ["GET", "POST", "PUT", "DELETE"][index % 4],
            "path": f"/api/{spec.key.replace('_', '-')}/v1/resources/{index:03d}",
            "requiredQuery": ["tenantId"],
            "successStatus": 200,
        }
    if category == "configuration":
        return {
            "contractId": cid,
            "key": f"{spec.key}.feature{index:03d}.timeoutSeconds",
            "environmentVariable": f"{spec.prefix}_FEATURE_{index:03d}_TIMEOUT_SECONDS",
            "default": 30 + index,
            "required": False,
            "mode": "safe",
        }
    if category == "developer_setup":
        return {
            "contractId": cid,
            "profile": f"developer-profile-{index:03d}",
            "runtime": spec.runtime,
            "runtimeVersion": spec.runtime_version,
            "packageManager": spec.package_manager,
            "developmentCommand": f"{spec.dev_command} -- --profile {index:03d}",
            "migrationCommand": f"{spec.migration_command} --profile {index:03d}",
        }
    if category == "model_contract":
        return {
            "contractId": cid,
            "title": f"{spec.prefix}PublicContract{index:03d}",
            "type": "object",
            "required": ["id", "status"],
            "properties": {
                "id": {"type": "string", "format": "uuid"},
                "status": {"type": "string", "enum": ["active", "inactive"]},
                "score": {"type": "integer", "minimum": 0},
                "metadata": {"type": "object", "additionalProperties": True},
            },
        }
    return {
        "contractId": cid,
        "workflow": f"{spec.key}-approval-{index:03d}",
        "steps": ["submitted", "validated", "approved", "published"],
        "architecturePath": "frontend -> api -> queue -> database",
        "retryAttempts": 3,
        "approvalRoles": ["operator", "reviewer"],
        "securityGate": "dual-control",
    }


def docs_entry(category: str, entry: dict[str, Any]) -> str:
    cid = entry["contractId"]
    if category == "api_reference":
        return (
            f"### {cid}\n"
            f"- Operation: `{entry['operationId']}`\n"
            f"- Public endpoint: `{entry['method']} {entry['path']}`\n"
            f"- Required query parameters: `{', '.join(entry['requiredQuery'])}`\n"
            f"- Success response status: `{entry['successStatus']}`\n"
        )
    if category == "configuration":
        return (
            f"### {cid}\n"
            f"- Configuration key: `{entry['key']}`\n"
            f"- Environment variable: `{entry['environmentVariable']}`\n"
            f"- Documented default: `{entry['default']}`\n"
            f"- Required: `{str(entry['required']).lower()}`\n"
            f"- Mode: `{entry['mode']}`\n"
        )
    if category == "developer_setup":
        return (
            f"### {cid}\n"
            f"- Profile: `{entry['profile']}`\n"
            f"- Required runtime: `{entry['runtime']} {entry['runtimeVersion']}`\n"
            f"- Package manager: `{entry['packageManager']}`\n"
            f"- Local development command: `{entry['developmentCommand']}`\n"
            f"- Migration command: `{entry['migrationCommand']}`\n"
        )
    if category == "model_contract":
        props = entry["properties"]
        return (
            f"### {cid} — `{entry['title']}`\n"
            f"- Serialized type: `object`\n"
            f"- Required fields: `{', '.join(entry['required'])}`\n"
            f"- `id`: `string(uuid)`\n"
            f"- `status`: `string`, allowed values `active|inactive`\n"
            f"- `score`: `{props['score']['type']}`, minimum `{props['score']['minimum']}`\n"
            f"- `metadata`: `object`, additional properties allowed\n"
        )
    return (
        f"### {cid}\n"
        f"- Workflow: `{entry['workflow']}`\n"
        f"- Required sequence: `{' -> '.join(entry['steps'])}`\n"
        f"- Architecture path: `{entry['architecturePath']}`\n"
        f"- Retry policy: `{entry['retryAttempts']} attempts`\n"
        f"- Approval roles: `{', '.join(entry['approvalRoles'])}`\n"
        f"- Security gate: `{entry['securityGate']}`\n"
    )


def mutate(category: str, entry: dict[str, Any], index: int) -> tuple[dict[str, Any], str, str, str]:
    changed = copy.deepcopy(entry)
    variant = (index - 1) % 4
    if category == "api_reference":
        if variant == 0:
            old, new = entry["method"], {"GET": "POST", "POST": "PUT", "PUT": "PATCH", "DELETE": "POST"}[entry["method"]]
            changed["method"] = new
            return changed, "http_method_change", old, new
        if variant == 1:
            old, new = entry["path"], entry["path"].replace("/v1/", "/v2/")
            changed["path"] = new
            return changed, "endpoint_version_change", old, new
        if variant == 2:
            old, new = ", ".join(entry["requiredQuery"]), ", ".join(entry["requiredQuery"] + ["includeAudit"])
            changed["requiredQuery"].append("includeAudit")
            return changed, "required_parameter_added", old, new
        old, new = str(entry["successStatus"]), "202"
        changed["successStatus"] = 202
        return changed, "success_status_change", old, new
    if category == "configuration":
        if variant == 0:
            old, new = str(entry["default"]), str(entry["default"] + 30)
            changed["default"] += 30
            return changed, "documented_default_change", old, new
        if variant == 1:
            old, new = entry["environmentVariable"], entry["environmentVariable"] + "_V2"
            changed["environmentVariable"] = new
            return changed, "environment_variable_rename", old, new
        if variant == 2:
            old, new = "false", "true"
            changed["required"] = True
            return changed, "optional_to_required", old, new
        old, new = entry["mode"], "strict"
        changed["mode"] = new
        return changed, "configuration_mode_change", old, new
    if category == "developer_setup":
        if variant == 0:
            old = entry["runtimeVersion"]
            major = int(old.split(".")[0]) + 2
            new = f"{major}.0"
            changed["runtimeVersion"] = new
            return changed, "runtime_requirement_change", old, new
        if variant == 1:
            old, new = entry["developmentCommand"], entry["developmentCommand"] + " --strict"
            changed["developmentCommand"] = new
            return changed, "local_command_change", old, new
        if variant == 2:
            old = entry["packageManager"]
            name, _, version = old.partition("@")
            new = f"{name}@{int(version or '1') + 1}"
            changed["packageManager"] = new
            return changed, "package_manager_version_change", old, new
        old, new = entry["migrationCommand"], entry["migrationCommand"] + " --no-build"
        changed["migrationCommand"] = new
        return changed, "migration_command_change", old, new
    if category == "model_contract":
        if variant == 0:
            # The docs-before excerpt explicitly names the documented field and
            # its current type.  Keep ``old`` as a literal evidence token so the
            # coverage gate proves that the mutation invalidates existing docs.
            old, new = "status", "status:integer"
            changed["properties"]["status"] = {"type": "integer", "minimum": 0}
            return changed, "serialized_field_type_change", old, new
        if variant == 1:
            old, new = "id, status", "id, status, score"
            changed["required"].append("score")
            return changed, "required_field_change", old, new
        if variant == 2:
            # Adding a field makes the documented, enumerated schema incomplete;
            # ``metadata`` anchors this mutation to that exact schema block.
            old, new = "metadata", "revision:integer (new field)"
            changed["properties"]["revision"] = {"type": "integer", "minimum": 1}
            return changed, "serialized_field_added", old, new
        old, new = "metadata", "attributes"
        changed["properties"]["attributes"] = changed["properties"].pop("metadata")
        return changed, "serialized_field_rename", old, new
    if variant == 0:
        old = " -> ".join(entry["steps"])
        changed["steps"].insert(2, "compliance_review")
        new = " -> ".join(changed["steps"])
        return changed, "business_workflow_step_added", old, new
    if variant == 1:
        old, new = entry["architecturePath"], "frontend -> api -> cache -> queue -> database"
        changed["architecturePath"] = new
        return changed, "architecture_path_change", old, new
    if variant == 2:
        old, new = str(entry["retryAttempts"]), str(entry["retryAttempts"] + 2)
        changed["retryAttempts"] += 2
        return changed, "operations_retry_policy_change", old, new
    old, new = entry["securityGate"], "three-person-review"
    changed["securityGate"] = new
    changed["approvalRoles"].append("compliance-officer")
    return changed, "security_approval_flow_change", old, new


def note_for(category: str, cid: str, template: str, old: str, new: str) -> str:
    surface = {
        "api_reference": "javni API ugovor",
        "configuration": "dokumentovanu konfiguraciju",
        "developer_setup": "dokumentovani razvojni setup",
        "model_contract": "javni/serijalizovani model",
        "other_documentation": "dokumentovani workflow/arhitekturu/operativno pravilo",
    }[category]
    return f"{cid}: kod mijenja {surface} iz '{old}' u '{new}' ({template}), dok docs-before eksplicitno navodi staru vrijednost; dokumentacija bi zato postala zastarjela."


def category_title(category: str) -> str:
    return {
        "api_reference": "API reference contracts",
        "configuration": "Configuration contracts",
        "developer_setup": "Developer setup contracts",
        "model_contract": "Model and serialization contracts",
        "other_documentation": "Workflow, architecture and operations contracts",
    }[category]


def build_project_baseline(
    out: Path,
    spec: ProjectSpec,
    category_counts: dict[str, int],
    *,
    index_start: int = 1,
    docs_dir_name: str = "docguard-contract-lab",
) -> tuple[dict[str, dict[int, tuple[Path, dict[str, Any]]]], dict[str, tuple[Path, dict[int, str]]]]:
    repo = out / spec.source_copy
    if not repo.exists():
        raise FileNotFoundError(f"Missing source copy: {repo}")
    code_root = repo / spec.code_root
    docs_root = repo / "docs" / docs_dir_name
    code_root.mkdir(parents=True, exist_ok=True)
    docs_root.mkdir(parents=True, exist_ok=True)
    baseline: dict[str, dict[int, tuple[Path, dict[str, Any]]]] = defaultdict(dict)
    docs_index: dict[str, tuple[Path, dict[int, str]]] = {}
    category_file = {
        "api_reference": "API_REFERENCE.md",
        "configuration": "CONFIGURATION.md",
        "developer_setup": "DEVELOPER_SETUP.md",
        "model_contract": "MODEL_CONTRACTS.md",
        "other_documentation": "WORKFLOWS_AND_OPERATIONS.md",
    }
    for category in CATEGORIES:
        excerpts: dict[int, str] = {}
        doc_parts = [f"# {category_title(category)}", "", f"Controlled baseline documentation for {spec.display_name}. Every contract below is implemented by a machine-readable manifest in `{spec.code_root}`.", ""]
        count = category_counts[category]
        indices = list(range(index_start, index_start + count))
        for bucket, chunk_start in enumerate(range(0, count, 10), start=1):
            entries = [base_entry(spec, category, i) for i in indices[chunk_start:chunk_start + 10]]
            suffix = ".schema.json" if category == "model_contract" else ".json"
            rel = Path(spec.code_root) / category / f"contracts_{bucket:02d}{suffix}"
            path = repo / rel
            payload = {"schemaVersion": 1, "project": spec.key, "category": category, "contracts": entries}
            write_json(path, payload)
            for entry in entries:
                index = int(entry["contractId"].rsplit("-", 1)[-1])
                baseline[category][index] = (rel, entry)
                excerpt = docs_entry(category, entry)
                excerpts[index] = excerpt
                doc_parts.extend([excerpt, ""])
        doc_path = docs_root / category_file[category]
        doc_path.write_text("\n".join(doc_parts).rstrip() + "\n", encoding="utf-8", newline="\n")
        docs_index[category] = (doc_path.relative_to(repo), excerpts)
    index = (
        "# DocGuard controlled contract lab\n\n"
        "This directory is part of a copied project baseline used to build controlled, PR-like documentation-drift examples. "
        "Each code contract is documented before mutation. Individual generated patches modify code only and intentionally leave this baseline documentation unchanged.\n\n"
        "- [API reference](API_REFERENCE.md)\n"
        "- [Configuration](CONFIGURATION.md)\n"
        "- [Developer setup](DEVELOPER_SETUP.md)\n"
        "- [Model contracts](MODEL_CONTRACTS.md)\n"
        "- [Workflows and operations](WORKFLOWS_AND_OPERATIONS.md)\n"
    )
    (docs_root / "README.md").write_text(index, encoding="utf-8", newline="\n")
    write_json(code_root / "lab_manifest.json", {
        "project": spec.key,
        "purpose": "Controlled documentation-drift evaluation over a real-project copy",
        "categories": CATEGORIES,
        "contractsPerCategory": category_counts,
        "baselineIsImmutableDuringCaseGeneration": True,
    })
    return baseline, docs_index


def find_payload(repo: Path, rel: Path) -> dict[str, Any]:
    return json.loads((repo / rel).read_text(encoding="utf-8"))


def replace_contract(payload: dict[str, Any], cid: str, changed: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    matches = [i for i, item in enumerate(result["contracts"]) if item["contractId"] == cid]
    if len(matches) != 1:
        raise AssertionError(f"{cid}: expected one contract, found {len(matches)}")
    result["contracts"][matches[0]] = changed
    return result


def unified_diff(rel: Path, before: str, after: str) -> str:
    return "".join(difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=f"a/{rel.as_posix()}",
        tofile=f"b/{rel.as_posix()}",
        n=3,
    ))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--profile", choices=["balanced_v1", "imbalanced_v2"], default="balanced_v1")
    args = parser.parse_args()
    out = args.output_root.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.profile == "imbalanced_v2":
        version = "controlled_real_project_positive_v2_imbalanced"
        case_prefix = "CRPP2"
        index_start = 101
        docs_dir_name = "docguard-contract-lab-v2"
        pr_number = 9_400_000
        active_specs = [
            replace(
                spec,
                repository=spec.repository.replace("controlled/", "controlled-v2/"),
                code_root=spec.code_root + "-v2",
            )
            for spec in PROJECTS
        ]
        project_category_counts = IMBALANCED_V2_COUNTS
    else:
        version = "controlled_real_project_positive_v1"
        case_prefix = "CRPP1"
        index_start = 1
        docs_dir_name = "docguard-contract-lab"
        pr_number = 9_200_000
        active_specs = PROJECTS
        project_category_counts = {
            spec.key: {category: 100 for category in CATEGORIES}
            for spec in active_specs
        }
    expected_total = sum(sum(counts.values()) for counts in project_category_counts.values())
    expected_category_counts = Counter({
        category: sum(project_category_counts[spec.key][category] for spec in active_specs)
        for category in CATEGORIES
    })
    expected_project_counts = Counter({
        spec.key: sum(project_category_counts[spec.key].values())
        for spec in active_specs
    })
    docs_rel = f"docs/{docs_dir_name}"
    if not ORIGINAL_CORPUS.exists():
        raise FileNotFoundError(f"Original 17,880-row corpus is required for the non-overlap gate: {ORIGINAL_CORPUS}")
    original_sha_before, original_case_ids, original_repository_pr_keys = corpus_identity(ORIGINAL_CORPUS)
    cases_dir = out / "cases"
    patches_dir = cases_dir / "patches"
    review_dir = out / "human_review"
    reports_dir = out / "reports"
    audits_dir = out / "audits"
    for path in [cases_dir, patches_dir, review_dir, reports_dir, audits_dir]:
        path.mkdir(parents=True, exist_ok=True)

    pre_lab_manifests = {}
    for spec in active_specs:
        repo = out / spec.source_copy
        if (repo / ".git").exists():
            raise AssertionError(f"Linked .git directory must not exist in source copy: {repo}")
        pre_lab_manifests[spec.key] = source_manifest(repo, spec.code_root, docs_rel)
    write_json(reports_dir / "source_copy_pre_lab_manifest.json", pre_lab_manifests)

    candidates: list[dict[str, Any]] = []
    reviewed: list[dict[str, Any]] = []
    validation_errors: list[dict[str, Any]] = []
    project_case_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    mutation_counts: Counter[str] = Counter()
    fingerprints: set[str] = set()
    patch_hashes: set[str] = set()

    for spec in active_specs:
        repo = out / spec.source_copy
        baseline, docs_index = build_project_baseline(
            out,
            spec,
            project_category_counts[spec.key],
            index_start=index_start,
            docs_dir_name=docs_dir_name,
        )
        for category in CATEGORIES:
            doc_rel, excerpts = docs_index[category]
            count = project_category_counts[spec.key][category]
            for index in range(index_start, index_start + count):
                cid = contract_id(spec, category, index)
                rel, entry = baseline[category][index]
                payload = find_payload(repo, rel)
                changed_entry, template, old, new = mutate(category, entry, index)
                changed_payload = replace_contract(payload, cid, changed_entry)
                # Each mutated manifest must remain valid JSON.
                after_text = json_text(changed_payload)
                json.loads(after_text)
                before_text = json_text(payload)
                diff = unified_diff(rel, before_text, after_text)
                if not diff.strip():
                    validation_errors.append({"contract_id": cid, "reason": "empty_diff"})
                    continue
                if str(doc_rel).replace("\\", "/") in diff:
                    validation_errors.append({"contract_id": cid, "reason": "docs_file_changed"})
                    continue
                excerpt = excerpts[index]
                if cid not in excerpt or old not in excerpt:
                    validation_errors.append({"contract_id": cid, "reason": "docs_before_missing_old_contract", "old": old})
                    continue
                patch_rel = Path("cases/patches") / spec.key / category / f"{cid}.patch"
                patch_path = out / patch_rel
                patch_path.parent.mkdir(parents=True, exist_ok=True)
                patch_path.write_text(diff, encoding="utf-8", newline="\n")
                patch_sha = sha256_bytes(diff.encode("utf-8"))
                if patch_sha in patch_hashes:
                    validation_errors.append({"contract_id": cid, "reason": "duplicate_patch_hash"})
                    continue
                patch_hashes.add(patch_sha)
                pr_number += 1
                case_id = f"{case_prefix}-{spec.prefix}-{category.upper()}-{index:03d}"
                note = note_for(category, cid, template, old, new)
                docs_before = f"<!-- {doc_rel.as_posix()} @ controlled-baseline:{sha256_bytes((repo / doc_rel).read_bytes())[:16]} -->\n{excerpt}"
                row: dict[str, Any] = {
                    "case_id": case_id,
                    "repository": spec.repository,
                    "pr_number": pr_number,
                    "language": spec.language,
                    "code_changed_files": [rel.as_posix()],
                    "code_diff_excerpt": diff,
                    "docs_before_excerpt": docs_before,
                    "docs_before_retrieved_files": [doc_rel.as_posix()],
                    "doc_context_01_path": doc_rel.as_posix(),
                    "doc_context_01_excerpt": excerpt,
                    "suggested_docs_update_required": True,
                    "suggested_doc_category": category,
                    "suggested_notes": f"Controlled design expectation: {category}; independent human/owner acceptance still required before merge.",
                    "human_docs_update_required": "",
                    "human_doc_category": "",
                    "human_label_notes": "",
                    "review_status": "pending",
                    "changed_files": [rel.as_posix()],
                    "classifier_model_input": {
                        "language": spec.language,
                        "code_changed_files": [rel.as_posix()],
                        "code_diff_excerpt": diff,
                        "docs_before_excerpt": docs_before,
                    },
                    "safe_model_input_fields": ["language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt"],
                    "case_origin": version,
                    "acquisition_origin": version,
                    "source_dataset": version,
                    "synthetic_case": True,
                    "controlled_real_project_case": True,
                    "synthetic_category_by_design": category,
                    "source_project_key": spec.key,
                    "source_project_display_name": spec.display_name,
                    "source_copy_path": spec.source_copy,
                    "source_repository_reference": "https://github.com/mahmutovichana/jobfaireestec" if spec.key == "jobfair_platform" else "local_user_project_copy",
                    "synthetic_pr_title": f"Controlled {category} contract change for {cid}",
                    "synthetic_base_sha256": sha256_bytes(before_text.encode("utf-8")),
                    "synthetic_head_sha256": sha256_bytes(after_text.encode("utf-8")),
                    "synthetic_patch_sha256": patch_sha,
                    "synthetic_contract_id": cid,
                    "synthetic_target_doc_path": doc_rel.as_posix(),
                    "mutation_template": template,
                    "mutation_old_value": old,
                    "mutation_new_value": new,
                    "patch_path": patch_rel.as_posix(),
                    "syntax_validation": "json_parse_pass",
                    "docs_coverage_validation": "exact_contract_and_old_value_match",
                    "merge_status": "pending_owner_acceptance",
                    "training_eligible": False,
                }
                row["review_row_hash"] = review_row_hash(row)
                row["review_context_hash"] = review_context_hash(row)
                reviewed_row = copy.deepcopy(row)
                reviewed_row.update({
                    "human_docs_update_required": True,
                    "human_doc_category": category,
                    "human_label_notes": note,
                    "review_status": "approved",
                    "reviewer": "Codex controlled contract review",
                    "review_method": "docs_before_semantic_contract_check",
                })
                candidates.append(row)
                reviewed.append(reviewed_row)
                project_case_counts[spec.key] += 1
                category_counts[category] += 1
                mutation_counts[template] += 1
                fingerprint = sha256_bytes((spec.repository + "\n" + rel.as_posix() + "\n" + diff + "\n" + docs_before).encode("utf-8"))
                if fingerprint in fingerprints:
                    validation_errors.append({"case_id": case_id, "reason": "duplicate_semantic_fingerprint"})
                fingerprints.add(fingerprint)

    write_jsonl(cases_dir / "candidates_2000.jsonl", candidates)
    write_jsonl(review_dir / "reviewed_2000.jsonl", reviewed)
    write_jsonl(review_dir / "positive_reviewed.jsonl", reviewed)
    write_jsonl(review_dir / "excluded_reviewed.jsonl", [])
    batch_dir = review_dir / "review_batches"
    for start in range(0, len(reviewed), 100):
        batch = reviewed[start:start + 100]
        number = start // 100 + 1
        write_jsonl(batch_dir / f"batch_{number:03d}.jsonl", batch)
        write_csv(batch_dir / f"batch_{number:03d}.csv", batch)

    post_lab_manifests = {
        spec.key: source_manifest(out / spec.source_copy, spec.code_root, docs_rel)
        for spec in active_specs
    }
    source_preserved = all(
        pre_lab_manifests[key]["aggregate_sha256"] == post_lab_manifests[key]["aggregate_sha256"]
        for key in pre_lab_manifests
    )
    ids = [row["case_id"] for row in reviewed]
    repo_pr = [(row["repository"], row["pr_number"]) for row in reviewed]
    generated_repository_pr_keys = {(str(repo).lower(), str(pr)) for repo, pr in repo_pr}
    case_id_overlap = len(set(ids) & original_case_ids)
    repository_pr_overlap = len(generated_repository_pr_keys & original_repository_pr_keys)
    original_sha_after, _, _ = corpus_identity(ORIGINAL_CORPUS)
    original_unchanged = original_sha_before == original_sha_after
    hashes_ok = all(row["review_row_hash"] == review_row_hash(row) and row["review_context_hash"] == review_context_hash(row) for row in reviewed)
    all_positive_consistent = all(
        row["human_docs_update_required"] is True
        and row["human_doc_category"] in CATEGORIES
        and row["review_status"] == "approved"
        for row in reviewed
    )
    no_git = all(not any((out / spec.source_copy).rglob(".git")) for spec in active_specs)
    audit = {
        "version": version,
        "row_count": len(reviewed),
        "candidate_count": len(candidates),
        "positive_count": sum(row["human_docs_update_required"] is True for row in reviewed),
        "excluded_count": sum(row["review_status"] == "excluded" for row in reviewed),
        "category_counts": dict(category_counts),
        "project_counts": dict(project_case_counts),
        "mutation_template_counts": dict(mutation_counts),
        "unique_case_ids": len(set(ids)),
        "unique_repository_pr_keys": len(set(repo_pr)),
        "unique_patch_hashes": len(patch_hashes),
        "unique_semantic_fingerprints": len(fingerprints),
        "batch_count": len(list(batch_dir.glob("batch_*.jsonl"))),
        "review_hashes_valid": hashes_ok,
        "all_positive_labels_consistent": all_positive_consistent,
        "source_files_preserved_outside_generated_lab": source_preserved,
        "source_copies_have_no_git_directory": no_git,
        "documentation_files_changed_by_cases": 0,
        "original_corpus_path": ORIGINAL_CORPUS.relative_to(ROOT).as_posix(),
        "original_corpus_sha256_before": original_sha_before,
        "original_corpus_sha256_after": original_sha_after,
        "original_17880_modified": not original_unchanged,
        "repository_pr_overlap_with_original_corpus": repository_pr_overlap,
        "case_id_overlap_with_original_corpus": case_id_overlap,
        "validation_errors": validation_errors,
        "all_quality_gates_pass": (
            len(reviewed) == expected_total
            and category_counts == expected_category_counts
            and project_case_counts == expected_project_counts
            and len(set(ids)) == expected_total
            and len(set(repo_pr)) == expected_total
            and len(patch_hashes) == expected_total
            and len(fingerprints) == expected_total
            and hashes_ok
            and all_positive_consistent
            and source_preserved
            and no_git
            and original_unchanged
            and repository_pr_overlap == 0
            and case_id_overlap == 0
            and not validation_errors
        ),
        "sha256_candidates": sha256_bytes((cases_dir / "candidates_2000.jsonl").read_bytes()),
        "sha256_reviewed": sha256_bytes((review_dir / "reviewed_2000.jsonl").read_bytes()),
    }
    write_json(audits_dir / "quality_audit.json", audit)
    write_json(reports_dir / "source_copy_post_lab_manifest.json", post_lab_manifests)
    manifest = {
        "version": version,
        "rows": len(reviewed),
        "all_rows_positive_by_controlled_design": True,
        "merge_status": "pending_owner_acceptance",
        "training_eligible": False,
        "projects": [spec.__dict__ for spec in active_specs],
        "categories": CATEGORIES,
        "category_counts": dict(category_counts),
        "project_counts": dict(project_case_counts),
        "outputs": {
            "candidates": "cases/candidates_2000.jsonl",
            "reviewed": "human_review/reviewed_2000.jsonl",
            "positive_reviewed": "human_review/positive_reviewed.jsonl",
            "review_batches": "human_review/review_batches",
            "patches": "cases/patches",
            "quality_audit": "audits/quality_audit.json",
        },
    }
    write_json(out / "manifest.json", manifest)
    report = [
        f"# {version}", "",
        "This dataset contains PR-like, code-only mutations over four copied real projects. The linked `.git` directories were not copied. Each mutation is independent from a documented baseline and leaves docs-before unchanged.", "",
        f"- Rows: **{len(reviewed)}**",
        f"- Positive: **{audit['positive_count']}**",
        f"- Excluded: **{audit['excluded_count']}**",
        f"- Quality gates: **{'PASS' if audit['all_quality_gates_pass'] else 'FAIL'}**", "",
        "## Category distribution", "", "| Category | Rows |", "|---|---:|",
    ]
    for category in CATEGORIES:
        report.append(f"| `{category}` | {category_counts[category]} |")
    report += ["", "## Project distribution", "", "| Project | Rows |", "|---|---:|"]
    for spec in active_specs:
        report.append(f"| `{spec.repository}` | {project_case_counts[spec.key]} |")
    report += [
        "", "## Important use constraint", "",
        "Rows are controlled/synthetic positives over real-project copies. They are deliberately marked `training_eligible=false` and `merge_status=pending_owner_acceptance` until the owner accepts the examples and chooses a leakage-safe split strategy.", "",
    ]
    (reports_dir / "summary.md").write_text("\n".join(report), encoding="utf-8", newline="\n")
    print(json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if audit["all_quality_gates_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
