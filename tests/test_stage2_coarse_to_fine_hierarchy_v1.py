from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

from scripts.prepare_stage2_coarse_to_fine_hierarchy_v1 import (
    CLASS_WEIGHT_GRID,
    COARSE_LABELS,
    COARSE_MAPPING,
    EXPECTED_COARSE_COUNTS,
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


def test_exact_frozen_natural_primary_four_train_export() -> None:
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


def test_exact_coarse_taxonomy_and_canonical_labels_unchanged() -> None:
    rows = read_jsonl(TRAIN_JSONL)
    coarse_counts = Counter(COARSE_MAPPING[row["gold_doc_category"]] for row in rows)

    assert LABELS == ["api_reference", "configuration", "developer_setup", "model_contract"]
    assert COARSE_LABELS == ["api_reference", "config_setup_family", "model_contract"]
    assert SPECIALIST_LABELS == ["configuration", "developer_setup"]
    assert COARSE_MAPPING == {
        "api_reference": "api_reference",
        "configuration": "config_setup_family",
        "developer_setup": "config_setup_family",
        "model_contract": "model_contract",
    }
    assert coarse_counts == EXPECTED_COARSE_COUNTS == {
        "api_reference": 412,
        "config_setup_family": 365,
        "model_contract": 261,
    }


def test_no_forbidden_data_sources_or_extra_training_rows() -> None:
    source = notebook_source()
    script = (ROOT / "scripts" / "prepare_stage2_coarse_to_fine_hierarchy_v1.py").read_text(encoding="utf-8")

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


def test_repository_identity_is_grouping_audit_only_not_model_text() -> None:
    source = notebook_source()

    assert "sanitize_repository_identity" in source
    assert "build_code_text" in source
    assert "build_docs_text" in source
    assert "row.get(\"repository\")" in source
    assert "f\"repository:" not in source
    assert "source_url" not in source
    assert "pr_number" not in source


def test_frozen_minilm_hybrid_representation_and_lr_configs() -> None:
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
    assert "coarse_clf = LogisticRegression(C=1.0, solver=\"lbfgs\", max_iter=2000, random_state=SEED)" in source
    assert "baseline_clf = LogisticRegression(C=1.0, solver=\"lbfgs\", max_iter=2000, random_state=SEED)" in source
    assert "optimizer" not in source.lower()
    assert "encoder.fit(" not in source


def test_outer_cv_and_train_fitting_are_fold_local() -> None:
    source = notebook_source()

    assert "StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)" in source
    assert "for n_splits in [5, 4, 3]" in source
    assert "outer_split_valid" in source
    assert "set(labels_for(train_rows)) == set(LABELS)" in source
    assert "set(labels_for(eval_rows)) == set(LABELS)" in source
    assert "set(coarse_labels_for(train_rows)) == set(COARSE_LABELS)" in source
    assert "set(coarse_labels_for(eval_rows)) == set(COARSE_LABELS)" in source
    assert "code_vectorizer.fit_transform" in source
    assert "code_vectorizer.transform" in source
    assert "eval_enters_tfidf_fit" in source
    assert "feature_context=\"baseline_four_class_outer_train_only\"" in source
    assert "feature_context=\"coarse_three_class_outer_train_only\"" in source


def test_specialist_v2_nested_selection_is_config_setup_outer_train_only() -> None:
    source = notebook_source()

    assert "specialist_outer_train_idx" in source
    assert "rows[int(i)][\"gold_doc_category\"] in SPECIALIST_LABELS" in source
    assert "choose_inner_splits" in source
    assert "for n_splits in [4, 3]" in source
    assert "SEED + outer_fold_id" in source
    assert "required_labels=SPECIALIST_LABELS" in source
    assert "feature_context=\"specialist_inner_train_only\"" in source
    assert "feature_context=\"specialist_final_outer_train_config_setup_only\"" in source
    assert "specialist_clf.fit(x_spec_train, y_spec_train)" in source
    assert CLASS_WEIGHT_GRID == [
        {"name": "none", "value": None, "rank": 0},
        {"name": "developer_1_5", "value": {"configuration": 1.0, "developer_setup": 1.5}, "rank": 1},
        {"name": "developer_2_0", "value": {"configuration": 1.0, "developer_setup": 2.0}, "rank": 2},
        {"name": "developer_3_0", "value": {"configuration": 1.0, "developer_setup": 3.0}, "rank": 3},
        {"name": "balanced", "value": "balanced", "rank": 4},
    ]
    assert THRESHOLD_GRID == [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
    assert PRECISION_FLOOR == 0.30
    assert "for threshold in THRESHOLD_GRID" in source
    assert "PRECISION_FLOOR = 0.3" in source
    assert "SMOTE" not in source
    assert "oversampl" not in source.lower()
    assert "undersampl" not in source.lower()


def test_inference_is_single_coarse_to_fine_rule_without_router_search() -> None:
    source = notebook_source()

    assert 'if str(coarse_pred[local_pos]) == "config_setup_family":' in source
    assert 'elif str(coarse_pred[local_pos]) == "api_reference":' in source
    assert 'final = "api_reference"' in source
    assert 'elif str(coarse_pred[local_pos]) == "model_contract":' in source
    assert 'final = "model_contract"' in source
    assert "specialist_predictions_if_applicable" in source
    assert "post-hoc router" not in source.lower()
    assert "routing threshold" not in source.lower()
    assert "top-2" not in source.lower()
    assert "confidence routing" not in source.lower()
    assert "learned router" not in source.lower()


def test_required_outputs_figures_primary_table_and_go_gates() -> None:
    source = notebook_source()

    for artifact in [
        "RESULTS.md",
        "experiment_manifest.json",
        "outer_fold_manifest.json",
        "outer_fold_metrics.json",
        "coarse_oof_metrics.json",
        "baseline_oof_metrics.json",
        "hierarchy_oof_metrics.json",
        "paired_oof_predictions.jsonl",
        "hierarchy_comparison.json",
        "coarse_diagnostics.json",
        "developer_setup_path_analysis.json",
        "configuration_path_analysis.json",
        "api_model_contract_damage_analysis.json",
        "specialist_selection_by_fold.json",
        "selection_stability.json",
        "repository_diagnostics.json",
        "repository_cluster_bootstrap.json",
        "decision.json",
        "coarse_confusion_matrix.png",
        "coarse_normalized_confusion_matrix.png",
        "baseline_confusion_matrix.png",
        "hierarchy_confusion_matrix.png",
        "hierarchy_normalized_confusion_matrix.png",
        "baseline_vs_hierarchy_macro_f1.png",
        "baseline_vs_hierarchy_balanced_accuracy.png",
        "baseline_vs_hierarchy_per_class_f1.png",
        "baseline_vs_hierarchy_setup_f1.png",
        "baseline_vs_hierarchy_setup_recall.png",
        "setup_family_routing_recall_by_fold.png",
        "outer_fold_macro_f1_delta.png",
        "outer_fold_setup_f1_delta.png",
    ]:
        assert artifact in source

    for gate in [
        "macro_f1_delta_ge_0_02",
        "balanced_accuracy_not_worse",
        "developer_setup_f1_ge_0_25",
        "developer_setup_f1_delta_ge_0_10",
        "developer_setup_recall_ge_0_25",
        "setup_family_routing_recall_ge_0_50",
        "api_configuration_model_contract_f1_safety",
        "setup_improves_across_at_least_3_repositories",
        "setup_gain_not_majority_from_one_repository",
        "bootstrap_macro_delta_probability_ge_0_90",
        "no_leakage_repository_overlap_or_forbidden_evidence_violation",
    ]:
        assert gate in source

    assert "Metric | Original 4-class MiniLM | Coarse-to-fine hierarchy | Delta" in source
    assert "stage2_coarse_to_fine_hierarchy_v1_results.zip" in source
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


def test_readme_and_gitignore_document_cache_policy() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "Stage-2 coarse-to-fine hierarchy V1" in readme
    assert EXPECTED_TRAIN_SHA256 in readme
    assert MINILM_MODEL_NAME in readme
    assert MINILM_MODEL_REVISION in readme
    assert "api_reference -> api_reference" in readme
    assert "developer_setup -> config_setup_family" in readme
    assert "experiments/category_stage2_coarse_to_fine_hierarchy_v1/cache/" in gitignore
    assert "experiments/category_stage2_coarse_to_fine_hierarchy_v1/**/*.npy" in gitignore
