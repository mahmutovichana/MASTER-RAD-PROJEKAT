from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

from scripts.prepare_configuration_setup_specialist_v2 import (
    CLASS_WEIGHT_GRID,
    EXPECTED_COUNTS,
    EXPECTED_EXPORT_SHA256,
    EXPECTED_TOTAL,
    EXPORT_JSONL,
    EXPORT_MANIFEST,
    LABELS,
    MINILM_MODEL_NAME,
    MINILM_MODEL_REVISION,
    NOTEBOOK_PATH,
    PRECISION_FLOOR,
    README_PATH,
    SAFE_FIELDS,
    THRESHOLD_GRID,
    compile_notebook_code_cells,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def notebook_source() -> str:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def test_v2_reuses_exact_v1_specialist_export() -> None:
    manifest = json.loads(EXPORT_MANIFEST.read_text(encoding="utf-8"))
    rows = read_jsonl(EXPORT_JSONL)

    assert len(rows) == EXPECTED_TOTAL == 365
    assert Counter(row["gold_doc_category"] for row in rows) == EXPECTED_COUNTS == {
        "configuration": 277,
        "developer_setup": 88,
    }
    assert sha256_file(EXPORT_JSONL) == EXPECTED_EXPORT_SHA256
    assert manifest["artifacts"]["natural_train_configuration_setup.jsonl"]["sha256"] == EXPECTED_EXPORT_SHA256
    assert set(row["partition"] for row in rows) == {"development_train"}
    assert all(set(row) == set(SAFE_FIELDS) for row in rows)
    assert set(Counter(row["gold_doc_category"] for row in rows)) == set(LABELS)


def test_v2_does_not_reference_forbidden_validation_or_synthetic_sources() -> None:
    source = notebook_source()
    script = (ROOT / "scripts" / "prepare_configuration_setup_specialist_v2.py").read_text(encoding="utf-8")

    forbidden_exact = [
        "natural_validation_primary_four",
        "VALIDATION_PATH",
        "confirmation.jsonl",
        "refresh_validation",
        "controlled_synthetic",
        "controlled_positive",
    ]
    for forbidden in forbidden_exact:
        assert forbidden not in source
        assert forbidden not in script
    assert "reject_supplied_path" in source
    assert '["validation", "confirmation", "refresh"]' in source


def test_v2_keeps_frozen_minilm_hybrid_representation() -> None:
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
    assert "relational_semantic_features" in source
    assert "np.hstack([code, docs, np.abs(code - docs), code * docs, cosine])" in source
    assert 'analyzer="char_wb"' in source
    assert "ngram_range=(3, 5)" in source
    assert "min_df=2" in source
    assert "max_features=20000" in source
    assert "sublinear_tf=True" in source
    assert "dtype=np.float32" in source
    assert "code_vectorizer.fit_transform" in source
    assert "code_vectorizer.transform" in source


def test_v2_only_decision_layer_varies_on_predeclared_grid() -> None:
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
    assert "class_weight=weight_spec[\"value\"]" in source
    assert "class_weight=selected[\"class_weight_value\"]" in source
    assert "predict_from_threshold(prob_setup, threshold)" in source
    assert "for threshold in THRESHOLD_GRID" in source
    assert "PRECISION_FLOOR = 0.3" in source
    assert "C=1.0, solver=\"lbfgs\", max_iter=2000, random_state=SEED" in source
    assert "SMOTE" not in source
    assert "RandomForest" not in source
    assert "XGB" not in source
    assert "SVC(" not in source
    assert "MLP" not in source
    assert "oversampl" not in source.lower()
    assert "undersampl" not in source.lower()


def test_v2_nested_repository_grouped_design_and_no_outer_leakage() -> None:
    source = notebook_source()

    assert "StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)" in source
    assert "deterministic_outer_splits" in source
    assert "load_exact_v1_outer_splits_if_available" in source
    assert '"exact_v1_outer_fold_manifest_reused"' in source
    assert "choose_inner_splits" in source
    assert "for n_splits in [4, 3]" in source
    assert "SEED + outer_fold_id" in source
    assert "assert not set(inner_eval_idx) & set(np.setdiff1d(np.arange(len(rows)), outer_train_idx))" in source
    assert "selected, inner_grid_report, inner_meta = select_inner_candidate" in source
    assert "x_outer_train, x_outer_eval, feature_meta = build_fold_features(outer_train_idx, outer_eval_idx)" in source
    assert "selected_clf.fit(x_outer_train, y_outer_train)" in source
    assert "outer_predictions[outer_eval_idx] = pred" in source
    assert "assert all(item in LABELS for item in outer_predictions)" in source
    assert "eval_enters_tfidf_fit" in source
    assert '"tfidf_fit_rows"' in source


def test_v2_reports_required_diagnostics_outputs_and_go_gates() -> None:
    source = notebook_source()

    required_outputs = [
        "outer_fold_manifest.json",
        "outer_fold_metrics.json",
        "inner_selection_by_outer_fold.json",
        "v2_oof_metrics.json",
        "v1_fixed_baseline_metrics.json",
        "majority_baseline_metrics.json",
        "v1_v2_comparison.json",
        "repository_setup_diagnostics.json",
        "language_diagnostics.json",
        "probability_diagnostics.json",
        "repository_cluster_bootstrap.json",
        "paired_bootstrap_v2_vs_v1.json",
        "v1_to_v2_rescued_setup_cases.jsonl",
        "new_v2_false_positive_cases.jsonl",
        "decision.json",
        "v2_oof_confusion_matrix.png",
        "v2_oof_normalized_confusion_matrix.png",
        "v1_vs_v2_setup_f1.png",
        "v1_vs_v2_setup_recall.png",
        "outer_fold_setup_f1.png",
        "outer_fold_macro_f1.png",
        "selected_thresholds_by_fold.png",
        "selected_weights_by_fold.png",
        "setup_probability_distribution_v2.png",
    ]
    for output in required_outputs:
        assert output in source

    assert "developer_setup_f1_ge_0_30" in source
    assert "balanced_accuracy_ge_0_60" in source
    assert "binary_macro_f1_ge_0_60" in source
    assert "developer_setup_recall_ge_0_25" in source
    assert "setup_detections_across_multiple_repositories" in source
    assert "no_leakage_integrity_issue" in source
    assert "configuration_f1_ge_0_80" in source
    assert "roc_auc_score" in source
    assert "average_precision_score" in source
    assert "2000" in source
    assert "configuration_setup_specialist_v2_results.zip" in source


def test_v2_notebook_python_cells_compile_and_have_no_bare_json_null() -> None:
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


def test_v2_readme_and_gitignore_document_cache_policy() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "final bounded Stage-2 specialist experiment" in readme
    assert EXPECTED_EXPORT_SHA256 in readme
    assert MINILM_MODEL_NAME in readme
    assert MINILM_MODEL_REVISION in readme
    assert "experiments/category_hierarchy_pilot_v2/configuration_vs_developer_setup/cache/" in gitignore
    assert "experiments/category_hierarchy_pilot_v2/configuration_vs_developer_setup/**/*.npy" in gitignore
