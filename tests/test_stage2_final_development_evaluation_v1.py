from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

from scripts.prepare_stage2_final_development_evaluation_v1 import (
    BASELINE_REPRODUCTION_TOLERANCE,
    CLASS_WEIGHT_GRID,
    COARSE_MAPPING,
    EXPECTED_TRAIN_COUNTS,
    EXPECTED_TRAIN_SHA256,
    EXPECTED_TRAIN_TOTAL,
    EXPECTED_VALIDATION_CASE_IDS_SHA256,
    EXPECTED_VALIDATION_COUNTS,
    EXPECTED_VALIDATION_TOTAL,
    HISTORICAL_BASELINE_MACRO_F1,
    LABELS,
    MINILM_MODEL_NAME,
    MINILM_MODEL_REVISION,
    NOTEBOOK_PATH,
    PRECISION_FLOOR,
    README_PATH,
    SPECIALIST_LABELS,
    THRESHOLD_GRID,
    TRAIN_JSONL,
    VALIDATION_JSONL,
    compile_notebook_code_cells,
    sha256_file,
    stable_json_hash,
)


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def notebook_source() -> str:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def test_exact_train_and_development_validation_artifacts() -> None:
    train_rows = read_jsonl(TRAIN_JSONL)
    validation_rows = read_jsonl(VALIDATION_JSONL)

    assert len(train_rows) == EXPECTED_TRAIN_TOTAL == 1038
    assert Counter(row["gold_doc_category"] for row in train_rows) == EXPECTED_TRAIN_COUNTS == {
        "api_reference": 412,
        "configuration": 277,
        "developer_setup": 88,
        "model_contract": 261,
    }
    assert sha256_file(TRAIN_JSONL) == EXPECTED_TRAIN_SHA256
    assert len(validation_rows) == EXPECTED_VALIDATION_TOTAL == 322
    assert Counter(row["gold_doc_category"] for row in validation_rows) == EXPECTED_VALIDATION_COUNTS == {
        "api_reference": 85,
        "configuration": 154,
        "developer_setup": 19,
        "model_contract": 64,
    }
    assert stable_json_hash([row["case_id"] for row in validation_rows]) == EXPECTED_VALIDATION_CASE_IDS_SHA256
    assert not ({row["repository"] for row in train_rows} & {row["repository"] for row in validation_rows})
    assert set(Counter(row["gold_doc_category"] for row in train_rows)) == set(LABELS)
    assert set(Counter(row["gold_doc_category"] for row in validation_rows)) == set(LABELS)


def test_notebook_uses_development_validation_language_not_final_test_language() -> None:
    source = notebook_source()

    assert "THIS IS DEVELOPMENT VALIDATION, NOT FINAL EXTERNAL TESTING" in source
    assert "development-validation" in source
    assert "final external testing" in source.lower()
    assert "sealed test set" not in source.lower()


def test_no_forbidden_extra_data_sources() -> None:
    source = notebook_source()
    script = (ROOT / "scripts" / "prepare_stage2_final_development_evaluation_v1.py").read_text(encoding="utf-8")

    for forbidden in [
        "confirmation.jsonl",
        "refresh_validation",
        "controlled_synthetic",
        "controlled_positive",
    ]:
        assert forbidden not in source
        assert forbidden not in script
    assert "reject_forbidden_path" in source
    assert '["confirmation", "refresh", "controlled", "synthetic", "no_update", "other_documentation"]' in source


def test_frozen_representation_and_safe_model_input() -> None:
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
    assert "sanitize_repository_identity" in source
    assert "f\"repository:" not in source
    assert "source_url" not in source
    assert "pr_number" not in source
    assert "optimizer" not in source.lower()
    assert "encoder.fit(" not in source


def test_baseline_coarse_and_specialist_train_only_fit_design() -> None:
    source = notebook_source()

    assert "baseline_vectorizer, baseline_train_x = fit_feature_components(train_rows, train_code_embeddings, train_docs_embeddings)" in source
    assert "baseline_clf.fit(baseline_train_x, train_y)" in source
    assert "coarse_vectorizer, coarse_train_x = fit_feature_components(train_rows, train_code_embeddings, train_docs_embeddings)" in source
    assert "coarse_clf.fit(coarse_train_x, train_coarse_y)" in source
    assert COARSE_MAPPING == {
        "api_reference": "api_reference",
        "configuration": "config_setup_family",
        "developer_setup": "config_setup_family",
        "model_contract": "model_contract",
    }
    assert SPECIALIST_LABELS == ["configuration", "developer_setup"]
    assert "specialist_train_indices" in source
    assert "row[\"gold_doc_category\"] in SPECIALIST_LABELS" in source
    assert "Counter(row[\"gold_doc_category\"] for row in specialist_rows) == {\"configuration\": 277, \"developer_setup\": 88}" in source
    assert "specialist_clf.fit(specialist_train_x, specialist_y)" in source
    assert "transform_feature_components(baseline_vectorizer, validation_rows" in source
    assert "transform_feature_components(coarse_vectorizer, validation_rows" in source
    assert "transform_feature_components(specialist_vectorizer, validation_rows" in source


def test_final_specialist_policy_selected_before_validation_scoring() -> None:
    source = notebook_source()

    freeze_index = source.index("STAGE2_TRAIN_FREEZE_COMPLETE")
    validation_index = source.index("validation_rows = read_rows(VALIDATION_PATH")
    assert freeze_index < validation_index
    assert "stage2_train_freeze_manifest.json" in source[:validation_index]
    assert "final_specialist_selection = max" in source[:validation_index]
    assert "final_specialist_selection[\"threshold\"]" in source[validation_index:]
    assert CLASS_WEIGHT_GRID == [
        {"name": "none", "value": None, "rank": 0},
        {"name": "developer_1_5", "value": {"configuration": 1.0, "developer_setup": 1.5}, "rank": 1},
        {"name": "developer_2_0", "value": {"configuration": 1.0, "developer_setup": 2.0}, "rank": 2},
        {"name": "developer_3_0", "value": {"configuration": 1.0, "developer_setup": 3.0}, "rank": 3},
        {"name": "balanced", "value": "balanced", "rank": 4},
    ]
    assert THRESHOLD_GRID == [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
    assert PRECISION_FLOOR == 0.30
    assert "for threshold in THRESHOLD_GRID" in source[:validation_index]
    assert "PRECISION_FLOOR = 0.3" in source
    assert "SMOTE" not in source
    assert "oversampl" not in source.lower()
    assert "undersampl" not in source.lower()


def test_baseline_reproduction_and_decision_rules_are_hard_coded() -> None:
    source = notebook_source()

    assert HISTORICAL_BASELINE_MACRO_F1 == 0.45628987455472775
    assert BASELINE_REPRODUCTION_TOLERANCE == 0.005
    assert "BASELINE_REPRODUCTION_AUDIT.md" in source
    assert "baseline_reproduction_warning" in source
    assert "hierarchy_macro_f1_gt_baseline_macro_f1" in source
    assert "hierarchy_balanced_accuracy_ge_baseline_minus_0_01" in source
    assert "hierarchy_developer_setup_f1_gt_baseline" in source
    assert "api_configuration_model_contract_no_f1_loss_gt_0_07" in source
    assert "HIERARCHY_SELECTED" in source
    assert "BASELINE_RETAINED" in source
    assert "development_decision.json" in source
    assert "Do NOT" not in (ROOT / "experiments" / "category_stage2_final_development_evaluation_v1" / "README.md").read_text(encoding="utf-8")


def test_required_outputs_and_figures_are_present() -> None:
    source = notebook_source()

    for artifact in [
        "RESULTS.md",
        "stage2_train_freeze_manifest.json",
        "experiment_manifest.json",
        "final_specialist_selection.json",
        "final_specialist_oof_metrics.json",
        "baseline_validation_metrics.json",
        "hierarchy_validation_metrics.json",
        "coarse_validation_metrics.json",
        "paired_validation_predictions.jsonl",
        "hierarchy_validation_comparison.json",
        "setup_validation_path_analysis.json",
        "development_decision.json",
        "BASELINE_REPRODUCTION_AUDIT.md",
        "baseline_validation_confusion_matrix.png",
        "hierarchy_validation_confusion_matrix.png",
        "hierarchy_validation_normalized_confusion_matrix.png",
        "baseline_vs_hierarchy_macro_f1.png",
        "baseline_vs_hierarchy_balanced_accuracy.png",
        "baseline_vs_hierarchy_per_class_f1.png",
        "baseline_vs_hierarchy_setup_f1.png",
        "baseline_vs_hierarchy_setup_recall.png",
        "stage2_final_development_evaluation_v1_results.zip",
    ]:
        assert artifact in source


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

    assert "Final Stage-2 development evaluation V1" in readme
    assert "not final external testing" in readme.lower()
    assert EXPECTED_TRAIN_SHA256 in readme
    assert EXPECTED_VALIDATION_CASE_IDS_SHA256 in readme
    assert MINILM_MODEL_NAME in readme
    assert MINILM_MODEL_REVISION in readme
    assert "experiments/category_stage2_final_development_evaluation_v1/cache/" in gitignore
    assert "experiments/category_stage2_final_development_evaluation_v1/**/*.npy" in gitignore
