from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

import pytest

from scripts.prepare_configuration_setup_specialist_v1 import (
    CURRENT_HYBRID_CONFIG,
    EXPORT_JSONL,
    EXPORT_MANIFEST,
    LABELS,
    MINILM_MODEL_NAME,
    MINILM_MODEL_REVISION,
    NOTEBOOK_PATH,
    SAFE_FIELDS,
    SENTENCE_TRANSFORMERS_VERSION,
    SOURCE_TRAIN_PATH,
    compile_notebook_code_cells,
    export_row,
    reject_forbidden_path,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def safe_source_row(*, category: str = "configuration", partition: str = "development_train") -> dict:
    return {
        "case_id": "DGPR-specialist-safe",
        "repository": "org/private-repo",
        "language": "python",
        "code_changed_files": ["src/config.py"],
        "code_diff_excerpt": "+ CONFIG_TIMEOUT = 30",
        "docs_before_excerpt": "Configuration docs mention CONFIG_TIMEOUT.",
        "gold_doc_category": category,
        "partition": partition,
        "independent_human_reviewed": True,
    }


def test_specialist_export_is_train_only_and_small() -> None:
    manifest = json.loads(EXPORT_MANIFEST.read_text(encoding="utf-8"))
    rows = read_jsonl(EXPORT_JSONL)

    assert len(rows) == 365
    assert Counter(row["gold_doc_category"] for row in rows) == {"configuration": 277, "developer_setup": 88}
    assert set(row["partition"] for row in rows) == {"development_train"}
    assert all(set(row) == set(SAFE_FIELDS) for row in rows)
    assert manifest["row_count"] == 365
    assert manifest["category_counts"] == {"configuration": 277, "developer_setup": 88}
    assert manifest["confirmation_accessed"] is False
    assert manifest["frozen_322_validation_accessed"] is False
    assert manifest["development_validation_rows_used"] is False
    assert manifest["refresh_validation_rows_used"] is False
    assert manifest["controlled_or_synthetic_rows_used"] is False
    assert manifest["artifacts"]["natural_train_configuration_setup.jsonl"]["sha256"] == sha256_file(EXPORT_JSONL)


def test_export_does_not_load_or_require_frozen_322_validation() -> None:
    script = (ROOT / "scripts" / "prepare_configuration_setup_specialist_v1.py").read_text(encoding="utf-8")
    notebook = NOTEBOOK_PATH.read_text(encoding="utf-8")

    assert "natural_validation_primary_four" not in script
    assert "natural_validation_primary_four" not in notebook
    assert "VALIDATION_PATH" not in script
    assert "VALIDATION_PATH" not in notebook
    assert "SOURCE_TRAIN_PATH" in script
    assert SOURCE_TRAIN_PATH.name in script


def test_forbidden_paths_are_rejected_for_manual_upload() -> None:
    for path in [
        Path("natural_validation_primary_four.jsonl"),
        Path("refresh_validation.jsonl"),
        Path("historical_confirmation.jsonl"),
        Path("nested/development_validation/export_manifest.json"),
    ]:
        with pytest.raises(ValueError, match="Forbidden"):
            reject_forbidden_path(path)


def test_export_row_rejects_non_specialist_or_non_train_rows() -> None:
    with pytest.raises(ValueError, match="only"):
        export_row(safe_source_row(category="api_reference"))
    with pytest.raises(ValueError, match="only"):
        export_row(safe_source_row(category="model_contract"))
    with pytest.raises(ValueError, match="validation|forbidden"):
        export_row(safe_source_row(partition="development_validation"))
    with pytest.raises(ValueError, match="controlled"):
        export_row({**safe_source_row(), "controlled_design_supervision": True})
    with pytest.raises(ValueError, match="controlled/synthetic"):
        export_row({**safe_source_row(), "label_source": "controlled_synthetic_positive"})


def test_current_minilm_hybrid_configuration_is_reused() -> None:
    assert CURRENT_HYBRID_CONFIG["semantic_encoder"]["model_name"] == MINILM_MODEL_NAME
    assert CURRENT_HYBRID_CONFIG["semantic_encoder"]["revision"] == MINILM_MODEL_REVISION
    assert CURRENT_HYBRID_CONFIG["semantic_encoder"]["chunk_chars"] == 1000
    assert CURRENT_HYBRID_CONFIG["semantic_encoder"]["max_chunks_per_side"] == 2
    assert CURRENT_HYBRID_CONFIG["lexical_code_channel"]["analyzer"] == "char_wb"
    assert CURRENT_HYBRID_CONFIG["lexical_code_channel"]["ngram_range"] == [3, 5]
    assert CURRENT_HYBRID_CONFIG["lexical_code_channel"]["min_df"] == 2
    assert CURRENT_HYBRID_CONFIG["lexical_code_channel"]["max_features"] == 20000
    assert CURRENT_HYBRID_CONFIG["classifier"]["class"] == "LogisticRegression"
    assert CURRENT_HYBRID_CONFIG["classifier"]["C"] == 1.0
    assert CURRENT_HYBRID_CONFIG["classifier"]["solver"] == "lbfgs"
    assert CURRENT_HYBRID_CONFIG["classifier"]["max_iter"] == 2000
    assert CURRENT_HYBRID_CONFIG["classifier"]["random_state"] == 42
    assert CURRENT_HYBRID_CONFIG["classifier"]["class_weight"] is None


def test_notebook_python_cells_compile_and_have_no_json_null_source() -> None:
    assert compile_notebook_code_cells(NOTEBOOK_PATH) == []
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        executable_lines = [
            line.strip()
            for line in source.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        if executable_lines and executable_lines[0].startswith("!"):
            continue
        ast.parse(source)
        assert not re.search(r"(?<![A-Za-z_])null(?![A-Za-z_])", source)


def test_notebook_is_colab_first_frozen_minilm_oof_only() -> None:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert f'"sentence-transformers=={SENTENCE_TRANSFORMERS_VERSION}"' in source
    assert '"sentence-transformers==6.0.1"' not in source
    assert f'MINILM_MODEL_NAME = "{MINILM_MODEL_NAME}"' in source
    assert f'MINILM_MODEL_REVISION = "{MINILM_MODEL_REVISION}"' in source
    assert "SentenceTransformer(" in source
    assert "encoder.eval()" in source
    assert "parameter.requires_grad_(False)" in source
    assert "torch.inference_mode()" in source
    assert "optimizer" not in source.lower()
    assert "encoder.fit(" not in source
    assert "StratifiedGroupKFold" in source
    assert "for n_splits in [5, 4, 3]" in source
    assert "code_vectorizer.fit_transform" in source
    assert "code_vectorizer.transform" in source
    assert "fold_eval_never_enters_vectorizer_fit" in source
    assert "LogisticRegression(C=1.0, solver=\"lbfgs\", max_iter=2000, random_state=SEED)" in source
    assert "class_weight=\"balanced\"" not in source
    assert "SMOTE" not in source
    assert "WeightedRandomSampler" not in source
    assert "threshold search" not in source.lower()
    assert "files.download(\"/content/configuration_setup_specialist_v1_results.zip\")" in source


def test_embedding_cache_is_ignored_by_git() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "experiments/category_hierarchy_pilot_v1/configuration_vs_developer_setup/cache/" in gitignore
    assert "experiments/category_hierarchy_pilot_v1/configuration_vs_developer_setup/**/*.npy" in gitignore
