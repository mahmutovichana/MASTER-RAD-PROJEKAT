from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

from scripts.prepare_stage2_hierarchy_integration_pilot_v1 import (
    CLASS_WEIGHT_GRID,
    EXPECTED_COUNTS,
    EXPECTED_TOTAL,
    EXPECTED_TRAIN_SHA256,
    LABELS,
    MINILM_MODEL_NAME,
    MINILM_MODEL_REVISION,
    NOTEBOOK_PATH,
    PRECISION_FLOOR,
    README_PATH,
    SAFE_FIELDS,
    SPECIALIST_LABELS,
    THRESHOLD_GRID,
    TRAIN_JSONL,
    compile_notebook_code_cells,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def notebook_source() -> str:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def test_hierarchy_pilot_uses_exact_frozen_primary_four_train_export() -> None:
    rows = read_jsonl(TRAIN_JSONL)

    assert len(rows) == EXPECTED_TOTAL == 1038
    assert Counter(row["gold_doc_category"] for row in rows) == EXPECTED_COUNTS == {
        "api_reference": 412,
        "configuration": 277,
        "developer_setup": 88,
        "model_contract": 261,
    }
    assert sha256_file(TRAIN_JSONL) == EXPECTED_TRAIN_SHA256
    assert set(row["partition"] for row in rows) == {"development_train"}
    assert set(Counter(row["gold_doc_category"] for row in rows)) == set(LABELS)
    assert set(LABELS) == {"api_reference", "configuration", "developer_setup", "model_contract"}
    assert SPECIALIST_LABELS == ["configuration", "developer_setup"]


def test_hierarchy_pilot_has_no_forbidden_data_sources_or_extra_labels() -> None:
    source = notebook_source()
    script = (ROOT / "scripts" / "prepare_stage2_hierarchy_integration_pilot_v1.py").read_text(encoding="utf-8")

    for forbidden in [
        "natural_validation_primary_four.jsonl",
        "VALIDATION_PATH",
        "confirmation.jsonl",
        "refresh_validation",
        "controlled_synthetic",
        "controlled_positive",
        "other_documentation",
        "no_update",
    ]:
        assert forbidden not in source
        assert forbidden not in script
    assert "reject_supplied_path" in source
    assert '["validation", "confirmation", "refresh"]' in source


def test_repository_identity_is_audit_only_and_not_model_text() -> None:
    source = notebook_source()

    assert "sanitize_repository_identity" in source
    assert "build_code_text" in source
    assert "build_docs_text" in source
    assert "row.get(\"repository\")" in source
    assert "f\"repository:" not in source
    assert "repository:" not in source.lower()
    assert set(SAFE_FIELDS) == {
        "case_id",
        "repository",
        "language",
        "code_changed_files",
        "code_diff_excerpt",
        "docs_before_excerpt",
        "gold_doc_category",
        "partition",
    }


def test_frozen_minilm_hybrid_representation_is_unchanged() -> None:
    source = notebook_source()

    assert f'MINILM_MODEL_NAME = "{MINILM_MODEL_NAME}"' in source
    assert f'MINILM_MODEL_REVISION = "{MINILM_MODEL_REVISION}"' in source
    assert "SentenceTransformer(MINILM_MODEL_NAME, revision=MINILM_MODEL_REVISION, device=\"cuda\")" in source
    assert "encoder.eval()" in source
    assert "parameter.requires_grad_(False)" in source
    assert "torch.inference_mode()" in source
    assert "CHUNK_CHARS = 1000" in source
    assert "MAX_CHUNKS = 2" in source
    assert "normalize_embeddings=True" in source
    assert "np.hstack([code, docs, np.abs(code - docs), code * docs, cosine])" in source
    assert 'analyzer="char_wb"' in source
    assert "ngram_range=(3, 5)" in source
    assert "min_df=2" in source
    assert "max_features=20000" in source
    assert "sublinear_tf=True" in source
    assert "dtype=np.float32" in source
    assert "code_vectorizer.fit_transform" in source
    assert "code_vectorizer.transform" in source
    assert "optimizer" not in source.lower()
    assert "encoder.fit(" not in source


def test_outer_general_model_and_specialist_nested_cv_are_repository_grouped() -> None:
    source = notebook_source()

    assert "StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)" in source
    assert "for n_splits in [5, 4, 3]" in source
    assert "set(labels_for(train_rows)) == set(LABELS)" in source
    assert "set(labels_for(eval_rows)) == set(LABELS)" in source
    assert "choose_inner_splits" in source
    assert "for n_splits in [4, 3]" in source
    assert "SEED + outer_fold_id" in source
    assert "labels=SPECIALIST_LABELS" in source
    assert "specialist_outer_train_idx" in source
    assert "rows[int(i)][\"gold_doc_category\"] in SPECIALIST_LABELS" in source
    assert "general_clf.fit(x_general_train, y_general_train)" in source
    assert "selected_clf" not in source
    assert "specialist_clf.fit(x_spec_train, y_spec_train)" in source
    assert "eval_enters_tfidf_fit" in source


def test_exact_routing_rule_and_no_routing_search() -> None:
    source = notebook_source()

    assert "def apply_routing_rule(general_prediction, specialist_prediction):" in source
    assert 'if general_prediction in {"configuration", "developer_setup"}:' in source
    assert "return specialist_prediction" in source
    assert "return general_prediction" in source
    assert 'should_route = str(general_pred[local_pos]) in {"configuration", "developer_setup"}' in source
    assert "if should_route:" in source
    assert "else:" in source
    assert "final = str(general_pred[local_pos])" in source
    assert "routing threshold" not in source.lower()
    assert "top-2" not in source.lower()
    assert "confidence routing" not in source.lower()
    assert "learned router" not in source.lower()


def test_specialist_v2_decision_grid_and_precision_floor_are_fixed() -> None:
    source = notebook_source()

    assert CLASS_WEIGHT_GRID == [
        {"name": "none", "value": None, "rank": 0},
        {"name": "developer_1_5", "value": {"configuration": 1.0, "developer_setup": 1.5}, "rank": 1},
        {"name": "developer_2_0", "value": {"configuration": 1.0, "developer_setup": 2.0}, "rank": 2},
        {"name": "developer_3_0", "value": {"configuration": 1.0, "developer_setup": 3.0}, "rank": 3},
        {"name": "balanced", "value": "balanced", "rank": 4},
    ]
    assert THRESHOLD_GRID == [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
    assert PRECISION_FLOOR == 0.30
    assert "for weight_spec in CLASS_WEIGHT_GRID" in source
    assert "for threshold in THRESHOLD_GRID" in source
    assert "PRECISION_FLOOR = 0.3" in source
    assert "precision_floor_satisfied" in source
    assert "candidate_sort_key" in source
    assert "class_weight=weight_spec[\"value\"]" in source
    assert "class_weight=selected[\"class_weight_value\"]" in source
    assert "SMOTE" not in source
    assert "oversampl" not in source.lower()
    assert "undersampl" not in source.lower()
    assert "RandomForest" not in source
    assert "XGB" not in source
    assert "SVC(" not in source
    assert "MLP" not in source


def test_required_outputs_figures_and_go_gates_are_present() -> None:
    source = notebook_source()

    for artifact in [
        "RESULTS.md",
        "experiment_manifest.json",
        "outer_fold_manifest.json",
        "outer_fold_metrics.json",
        "baseline_oof_metrics.json",
        "hierarchy_oof_metrics.json",
        "paired_oof_predictions.jsonl",
        "hierarchy_comparison.json",
        "routing_diagnostics.json",
        "developer_setup_rescue_analysis.json",
        "damage_analysis.json",
        "specialist_selection_by_fold.json",
        "selection_stability.json",
        "repository_diagnostics.json",
        "repository_cluster_bootstrap.json",
        "hierarchy_rescued_errors.jsonl",
        "hierarchy_new_errors.jsonl",
        "decision.json",
        "baseline_confusion_matrix.png",
        "hierarchy_confusion_matrix.png",
        "hierarchy_normalized_confusion_matrix.png",
        "baseline_vs_hierarchy_macro_f1.png",
        "baseline_vs_hierarchy_balanced_accuracy.png",
        "baseline_vs_hierarchy_per_class_f1.png",
        "baseline_vs_hierarchy_setup_f1.png",
        "baseline_vs_hierarchy_setup_recall.png",
        "outer_fold_macro_f1_delta.png",
        "outer_fold_setup_f1_delta.png",
        "routing_breakdown.png",
    ]:
        assert artifact in source

    for gate in [
        "macro_f1_delta_ge_0_02",
        "balanced_accuracy_not_worse",
        "developer_setup_f1_ge_0_25",
        "developer_setup_f1_delta_ge_0_15",
        "developer_setup_recall_ge_0_25",
        "api_configuration_model_contract_f1_safety",
        "setup_improves_across_at_least_3_repositories",
        "setup_gain_not_only_one_repository",
        "bootstrap_macro_delta_probability_ge_0_90",
        "no_leakage_or_partition_integrity_issue",
    ]:
        assert gate in source
    assert "stage2_hierarchy_integration_pilot_v1_results.zip" in source
    assert "2000" in source


def test_notebook_compiles_and_has_no_bare_json_null() -> None:
    assert compile_notebook_code_cells(NOTEBOOK_PATH) == []
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        executable = [line.strip() for line in source.splitlines() if line.strip() and not line.strip().startswith("#")]
        if executable and executable[0].startswith("!"):
            continue
        ast.parse(source)
        assert not re.search(r"(?<![A-Za-z_])null(?![A-Za-z_])", source)


def test_readme_and_gitignore_document_hierarchy_pilot() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "Stage-2 hierarchical integration pilot V1" in readme
    assert EXPECTED_TRAIN_SHA256 in readme
    assert MINILM_MODEL_NAME in readme
    assert MINILM_MODEL_REVISION in readme
    assert "Route iff the general four-class prediction" in readme
    assert "experiments/category_hierarchy_integration_pilot_v1/cache/" in gitignore
    assert "experiments/category_hierarchy_integration_pilot_v1/**/*.npy" in gitignore
