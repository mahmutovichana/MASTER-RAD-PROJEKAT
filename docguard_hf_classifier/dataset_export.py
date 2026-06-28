from __future__ import annotations

import json
from pathlib import Path

from docguard_hf_classifier.label_maps import label_for_record, save_label_maps
from docguard_hf_classifier.text_builder import build_input_text

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
HF_DATA_DIR = DATA_DIR / "hf_v0_4"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def export_row(record: dict) -> dict:
    return {
        "id": record["id"],
        "input_text": build_input_text(record),
        "docs_update_required_label": label_for_record(record, "docs_update_required"),
        "doc_category_label": label_for_record(record, "doc_category"),
        "target_doc_file_label": label_for_record(record, "target_doc_file"),
        "scenario_type_label": label_for_record(record, "scenario_type"),
        "split": record["split"],
        "project_id": record.get("project_id"),
        "changed_files": record.get("changed_files", []),
        "code_diff": record.get("code_diff", ""),
        "change_summary": record.get("change_summary"),
        "change_intent_summary": record.get("change_intent_summary"),
        "docs_before_excerpt": record.get("docs_before_excerpt"),
        "docs_after_gold_excerpt": record.get("docs_after_gold_excerpt"),
        "docs_update_required": record.get("docs_update_required"),
        "doc_category": record.get("doc_category"),
        "target_doc_file": record.get("target_doc_file"),
        "target_section": record.get("target_section"),
        "scenario_type": record.get("scenario_type"),
        "expected_facts": record.get("expected_facts", []),
        "gold_doc_patch": record.get("gold_doc_patch"),
        "negative_reason": record.get("negative_reason"),
    }


def export(version: str = "v0_4") -> dict:
    if version != "v0_4":
        raise ValueError("Only v0_4 is supported for HF export.")
    all_records = read_jsonl(DATA_DIR / "docguard_dataset.jsonl")
    save_label_maps(all_records)
    summary = {"version": version, "splits": {}}
    for split in ["train", "validation", "test"]:
        records = read_jsonl(DATA_DIR / f"{split}.jsonl")
        rows = [export_row(record) for record in records]
        write_jsonl(HF_DATA_DIR / f"{split}.jsonl", rows)
        summary["splits"][split] = len(rows)
    return summary
