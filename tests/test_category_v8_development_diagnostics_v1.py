from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.run_category_v8_development_diagnostics_v1 import FieldText, load_jsonl, metrics_report


def test_diagnostic_loader_rejects_confirmation_path(tmp_path: Path) -> None:
    path = tmp_path / "confirmation.jsonl"
    path.write_text(json.dumps({"partition": "confirmation"}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Confirmation path"):
        load_jsonl(path)


def test_diagnostic_loader_rejects_confirmation_row(tmp_path: Path) -> None:
    path = tmp_path / "development.jsonl"
    path.write_text(json.dumps({"partition": "confirmation"}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Confirmation row"):
        load_jsonl(path)


def test_ablation_text_uses_only_requested_fields() -> None:
    rows = [{"code_diff_excerpt": "+changed", "docs_before_excerpt": "old docs", "docs_after_excerpt": "forbidden"}]
    assert FieldText(("code_diff_excerpt",)).transform(rows) == ["code_diff_excerpt: +changed"]


def test_metrics_report_has_all_primary_classes() -> None:
    result = metrics_report(["api_reference", "configuration"], ["api_reference", "api_reference"], ["api_reference", "configuration", "developer_setup", "model_contract"])
    assert set(result["per_class"]) == {"api_reference", "configuration", "developer_setup", "model_contract"}
    assert result["support"] == 2
