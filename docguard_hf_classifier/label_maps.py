from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models" / "hf_v0_4"

TASKS = ["docs_update_required", "doc_category", "target_doc_file", "scenario_type"]


def normalize_target_doc_file(record: dict) -> str:
    if not record.get("docs_update_required"):
        return "no_update"
    return record.get("target_doc_file") or "no_update"


def labels_for_task(records: list[dict], task: str) -> list[str]:
    if task == "docs_update_required":
        return ["false", "true"]
    if task == "doc_category":
        values = {record["doc_category"] for record in records}
    elif task == "target_doc_file":
        values = {normalize_target_doc_file(record) for record in records}
    elif task == "scenario_type":
        values = {record["scenario_type"] for record in records}
    else:
        raise ValueError(f"Unsupported task: {task}")
    return sorted(values)


def label_for_record(record: dict, task: str) -> str:
    if task == "docs_update_required":
        return "true" if record.get("docs_update_required") else "false"
    if task == "doc_category":
        return record["doc_category"]
    if task == "target_doc_file":
        return normalize_target_doc_file(record)
    if task == "scenario_type":
        return record["scenario_type"]
    raise ValueError(f"Unsupported task: {task}")


def build_label_maps(records: list[dict]) -> dict:
    maps = {}
    for task in TASKS:
        labels = labels_for_task(records, task)
        maps[task] = {
            "labels": labels,
            "label2id": {label: index for index, label in enumerate(labels)},
            "id2label": {str(index): label for index, label in enumerate(labels)},
        }
    return maps


def save_label_maps(records: list[dict], path: Path | None = None) -> dict:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    maps = build_label_maps(records)
    target = path or MODELS_DIR / "label_maps.json"
    target.write_text(json.dumps(maps, indent=2), encoding="utf-8")
    return maps


def load_label_maps(path: Path | None = None) -> dict:
    target = path or MODELS_DIR / "label_maps.json"
    return json.loads(target.read_text(encoding="utf-8"))

