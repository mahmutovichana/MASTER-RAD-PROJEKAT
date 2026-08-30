from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import pytest

from docguard_ml_v2.data_contract import (
    PRIMARY_STAGE2_LABELS,
    binary_eligible_rows,
    binary_labels,
    category_eligible_rows,
    category_labels,
    category_scope_counts,
    serialize_model_row,
)
from docguard_ml_v2.metrics import bootstrap_ci, majority_binary_baseline, majority_category_baseline
from docguard_ml_v2.model_manifest import sha256_file
from scripts.evaluate_binary_v4_confirmation import run as run_binary_confirmation
from scripts.freeze_final_model_v2 import run as run_freeze
from scripts.train_binary_classifier_v4 import run as run_binary_train
from scripts.train_category_classifier_v8 import run as run_category_train


ROOT = Path(__file__).resolve().parents[1]


def row(case_id: str, repo: str, language: str, label: bool, category: str, text: str) -> dict:
    return {
        "case_id": case_id,
        "repository": repo,
        "partition": "development_train",
        "language": language,
        "code_changed_files": [f"src/{text}.py"],
        "code_diff_excerpt": f"+def {text}_feature(): return '{text}' common shared token",
        "docs_before_excerpt": f"# Docs\ncommon shared documentation {text}",
        "gold_docs_update_required": label,
        "gold_doc_category": category,
        "human_review_complete": True,
        "review_status": "approved",
        "label_source": "human_reviewed_final_v2",
        "source_url": f"https://example.invalid/{case_id}",
        "pr_title": "must not enter model",
        "docs_after_excerpt": "must not enter model",
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")


def train_rows() -> list[dict]:
    rows = [
        row("t1", "org/a", "python", True, "api_reference", "reviews"),
        row("t2", "org/b", "python", True, "configuration", "config"),
        row("t3", "org/c", "typescript", True, "developer_setup", "setup"),
        row("t4", "org/d", "typescript", True, "model_contract", "schema"),
        row("t5", "org/e", "python", False, "no_update", "internal"),
        row("t6", "org/f", "typescript", False, "no_update", "refactor"),
        row("t7", "org/g", "python", True, "other_documentation", "guide"),
        row("t8", "org/h", "go", False, "no_update", "cleanup"),
    ]
    return rows


def validation_rows() -> list[dict]:
    rows = [
        row("v1", "org/i", "python", True, "api_reference", "reviews"),
        row("v2", "org/j", "typescript", True, "configuration", "config"),
        row("v3", "org/k", "python", True, "developer_setup", "setup"),
        row("v4", "org/l", "typescript", True, "model_contract", "schema"),
        row("v5", "org/m", "python", False, "no_update", "internal"),
        row("v6", "org/n", "ruby", False, "no_update", "refactor"),
        row("v7", "org/o", "typescript", True, "other_documentation", "guide"),
        row("v8", "org/p", "python", False, "no_update", "cleanup"),
    ]
    return [dict(item, partition="development_validation") for item in rows]


def confirmation_rows() -> list[dict]:
    return [dict(item, partition="confirmation") for item in validation_rows()]


def tiny_config(path: Path, *, category: bool = False) -> None:
    payload = {
        "pipeline_version": "category_classifier_v8" if category else "binary_classifier_v4",
        "seed": 7,
        "safe_fields": ["language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt"],
        "candidate_models": ["word_tfidf_logistic_regression"],
        "hyperparameter_grid": {"C": [0.5], "min_df": [1]},
        "threshold_policy": {"grid": [0.4, 0.5, 0.6]},
        "selection_metric": "macro_f1" if category else "mcc",
        "class_balancing": False,
        "confirmation_access": "forbidden",
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_trainer_cli_has_no_confirmation_or_test_arguments():
    for script in ["scripts/train_binary_classifier_v4.py", "scripts/train_category_classifier_v8.py"]:
        result = subprocess.run([sys.executable, script, "--help"], cwd=ROOT, text=True, capture_output=True)
        assert result.returncode == 0
        assert "--confirmation" not in result.stdout
        assert "--locked-test" not in result.stdout
        assert "--test" not in result.stdout


def test_safe_serializer_uses_only_canonical_fields():
    serialized = serialize_model_row(train_rows()[0])
    assert "source_url" not in serialized
    assert "pr_title" not in serialized
    assert "docs_after_excerpt" not in serialized
    assert "gold_docs_update_required" not in serialized
    assert "src/reviews.py" in serialized


def test_no_forbidden_balancing_or_manual_path_flags_in_final_sources():
    source = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in [
        "docguard_ml_v2/data_contract.py",
        "docguard_ml_v2/features.py",
        "scripts/train_binary_classifier_v4.py",
        "scripts/train_category_classifier_v8.py",
    ])
    assert 'class_weight="balanced"' not in source
    assert "oversampling" not in source.lower()
    assert "undersampling" not in source.lower()
    assert "path_has_api" not in source
    assert "path_has_config" not in source
    assert "CATEGORY_ALIASES" not in source


def test_binary_policy_preserves_natural_counts_and_other_documentation_positive():
    rows = train_rows()
    eligible = binary_eligible_rows(rows)
    labels = binary_labels(eligible)
    assert len(eligible) == len(rows)
    assert labels.count(1) == 5
    assert labels.count(0) == 3
    assert any(item["gold_doc_category"] == "other_documentation" and label == 1 for item, label in zip(eligible, labels))


def test_category_policy_excludes_other_documentation_and_aliases():
    rows = train_rows()
    eligible = category_eligible_rows(rows)
    assert [item["gold_doc_category"] for item in eligible] == PRIMARY_STAGE2_LABELS
    assert category_scope_counts(rows)["stage2_coverage_ratio"] == pytest.approx(4 / 5)
    bad = [dict(eligible[0], gold_doc_category="security")]
    with pytest.raises(ValueError):
        category_labels(bad)


def test_binary_training_uses_validation_selection_only_and_writes_manifest(tmp_path: Path):
    train_path = tmp_path / "train.jsonl"
    val_path = tmp_path / "validation.jsonl"
    config_path = tmp_path / "binary_config.json"
    write_jsonl(train_path, train_rows())
    write_jsonl(val_path, validation_rows())
    tiny_config(config_path)
    summary = run_binary_train(train=train_path, validation=val_path, output_dir=tmp_path / "binary_out", model_output=tmp_path / "binary.joblib", config_path=config_path)
    assert summary["row_counts"]["train_used"] == 8
    assert summary["class_counts"]["development_train"] == {1: 5, 0: 3}
    assert summary["model_results"][0]["model_selection_split"] == "development_validation"
    assert summary["model_results"][0]["threshold_selection_split"] == "development_validation"


def test_category_training_reports_stage2_coverage_and_validation_selection(tmp_path: Path):
    train_path = tmp_path / "train.jsonl"
    val_path = tmp_path / "validation.jsonl"
    config_path = tmp_path / "category_config.json"
    write_jsonl(train_path, train_rows())
    write_jsonl(val_path, validation_rows())
    tiny_config(config_path, category=True)
    summary = run_category_train(train=train_path, validation=val_path, output_dir=tmp_path / "category_out", model_output=tmp_path / "category.joblib", config_path=config_path)
    assert summary["scope_counts"]["development_train"]["primary_stage2_eligible_rows"] == 4
    assert summary["scope_counts"]["development_train"]["other_documentation_rows"] == 1
    assert summary["model_results"][0]["model_selection_split"] == "development_validation"


def test_freeze_manifest_does_not_read_confirmation_and_hashes_files(tmp_path: Path):
    model = tmp_path / "model.joblib"
    summary = tmp_path / "summary.json"
    config = tmp_path / "config.json"
    dataset_manifest = tmp_path / "dataset_manifest.json"
    partition_manifest = tmp_path / "partition_manifest.json"
    output = tmp_path / "freeze.json"
    model.write_bytes(b"model")
    summary.write_text(json.dumps({"model_version": "binary_v4", "selected_model": "x", "selected_threshold": 0.5, "best_metrics": {}, "config": {"seed": 7}}), encoding="utf-8")
    config.write_text("{}", encoding="utf-8")
    dataset_manifest.write_text("{}", encoding="utf-8")
    partition_manifest.write_text("{}", encoding="utf-8")
    manifest = run_freeze(model_file=model, training_summary=summary, config=config, dataset_manifest=dataset_manifest, repository_partition_manifest=partition_manifest, output=output)
    assert manifest["confirmation_accessed"] is False
    assert manifest["hashes"]["model"] == sha256_file(model)


def test_confirmation_evaluator_requires_freeze_manifest(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        run_binary_confirmation(model_path=tmp_path / "missing.joblib", confirmation=tmp_path / "confirmation.jsonl", freeze_manifest=tmp_path / "missing_freeze.json", output_dir=tmp_path / "out")


def test_one_shot_guard_refuses_repeat_for_same_model_and_confirmation(tmp_path: Path):
    train_path = tmp_path / "train.jsonl"
    val_path = tmp_path / "validation.jsonl"
    config_path = tmp_path / "binary_config.json"
    write_jsonl(train_path, train_rows())
    write_jsonl(val_path, validation_rows())
    tiny_config(config_path)
    run_binary_train(train=train_path, validation=val_path, output_dir=tmp_path / "binary_out", model_output=tmp_path / "binary.joblib", config_path=config_path)
    freeze = run_freeze(model_file=tmp_path / "binary.joblib", training_summary=tmp_path / "binary_out" / "training_summary.json", config=config_path, dataset_manifest=config_path, repository_partition_manifest=config_path, output=tmp_path / "freeze.json")
    assert freeze["confirmation_accessed"] is False
    out = tmp_path / "confirm"
    confirmation_path = tmp_path / "confirmation.jsonl"
    write_jsonl(confirmation_path, confirmation_rows())
    run_binary_confirmation(model_path=tmp_path / "binary.joblib", confirmation=confirmation_path, freeze_manifest=tmp_path / "freeze.json", output_dir=out, enforce_one_shot=True)
    with pytest.raises(ValueError):
        run_binary_confirmation(model_path=tmp_path / "binary.joblib", confirmation=confirmation_path, freeze_manifest=tmp_path / "freeze.json", output_dir=out, enforce_one_shot=True)


def test_runtime_source_contains_no_document_routing_or_gold_consumption():
    source = (ROOT / "docguard_ml_v2/runtime.py").read_text(encoding="utf-8")
    assert "target_document_path" not in source
    assert "gold_doc" not in source
    assert "route" not in source.lower()


def test_majority_baselines_and_bootstrap_are_deterministic():
    binary = majority_binary_baseline([1, 1, 0])
    category = majority_category_baseline(["api_reference", "api_reference", "configuration"], PRIMARY_STAGE2_LABELS)
    assert binary["majority_label"] == 1
    assert category["majority_label"] == "api_reference"
    first = bootstrap_ci(lambda yt, yp: sum(int(a == b) for a, b in zip(yt, yp)) / len(yt), [1, 0, 1], [1, 0, 0], seed=3)
    second = bootstrap_ci(lambda yt, yp: sum(int(a == b) for a, b in zip(yt, yp)) / len(yt), [1, 0, 1], [1, 0, 0], seed=3)
    assert first == second


def test_configuration_hash_is_deterministic(tmp_path: Path):
    config = tmp_path / "config.json"
    config.write_text('{"a": 1}', encoding="utf-8")
    assert sha256_file(config) == sha256_file(config)
