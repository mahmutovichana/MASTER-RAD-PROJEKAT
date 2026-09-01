"""Prepare the bounded Stage-2 Jina code-aware frozen hybrid experiment.

This script does not train the final model. It validates the frozen natural
Architecture Challenge V1 export, documents the current hybrid implementation,
and writes the Colab notebook for the one predeclared Jina replacement.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
LABELS = ["api_reference", "configuration", "developer_setup", "model_contract"]
LABEL_SET = set(LABELS)
SEED = 42

JINA_MODEL_NAME = "jinaai/jina-embeddings-v2-base-code"
PRIMARY_MODEL_ID = "jina_code_hybrid__natural_only__multinomial_logreg"
CURRENT_HYBRID_MODEL_ID = "hybrid__natural_only__multinomial_logreg__natural_diversity_expansion_v1"

EXPORT_DIR = ROOT / "data" / "final_v2" / "architecture_challenge_v1"
TRAIN_PATH = EXPORT_DIR / "natural_train_primary_four.jsonl"
VALIDATION_PATH = EXPORT_DIR / "natural_validation_primary_four.jsonl"
MANIFEST_PATH = EXPORT_DIR / "export_manifest.json"

NOTEBOOK_PATH = ROOT / "notebooks" / "category_jina_code_hybrid_architecture_challenge_v3.ipynb"
EXPERIMENT_DIR = ROOT / "experiments" / "category_architecture_challenge_v3" / "jina_code_hybrid"
FIGURES_DIR = EXPERIMENT_DIR / "figures"
AUDIT_PATH = EXPERIMENT_DIR / "CURRENT_HYBRID_IMPLEMENTATION_AUDIT.md"

FROZEN_VALIDATION_CASE_IDS_SHA256 = "aac3384de6d482abefb4201091bf828d6d8c1c91c1ddbdad40a4ec7273051e3e"
FROZEN_TRAIN_SHA256 = "9dc1136f1cf695eb69c70b763ad051898aa5fae351fcf028eed97116c8891f99"
FROZEN_VALIDATION_SHA256 = "1865d6803ac7e57cf38e315789732ee6592ddb6890373afa7fd1f988eb45ba2e"
FROZEN_TRAIN_COUNT = 1038
FROZEN_VALIDATION_COUNT = 322
FROZEN_TRAIN_CATEGORY_COUNTS = {
    "api_reference": 412,
    "configuration": 277,
    "developer_setup": 88,
    "model_contract": 261,
}
FROZEN_VALIDATION_CATEGORY_COUNTS = {
    "api_reference": 85,
    "configuration": 154,
    "developer_setup": 19,
    "model_contract": 64,
}

SAFE_EXPORT_FIELDS = {
    "case_id",
    "repository",
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
    "gold_doc_category",
    "partition",
}
FORBIDDEN_MODEL_FIELDS = {
    "controlled_design_label",
    "controlled_design_supervision",
    "docs_after",
    "docs_after_excerpt",
    "docs_diff",
    "docs_diff_excerpt",
    "human_label_notes",
    "human_docs_update_required",
    "human_doc_category",
    "independent_human_reviewed",
    "label_source",
    "owner_accepted_for_training",
    "pr_number",
    "provenance_tier",
    "repository",
    "repository_full_name_for_model",
    "review_status",
    "suggested_doc_category",
    "suggested_docs_update_required",
    "suggested_notes",
    "supervision_source",
}

CURRENT_HYBRID_IMPLEMENTATION = {
    "source_scripts": [
        "scripts/run_category_semantic_development_v1.py",
        "scripts/run_natural_diversity_refresh_category_v1.py",
    ],
    "current_model": CURRENT_HYBRID_MODEL_ID,
    "semantic_encoder_replaced": "sentence-transformers/all-MiniLM-L6-v2",
    "semantic_encoder_replaced_revision": "1110a243fdf4706b3f48f1d95db1a4f5529b4d41",
    "new_semantic_encoder": JINA_MODEL_NAME,
    "lexical_channel": {
        "field": "code side only: language + code_changed_files + code_diff_excerpt",
        "vectorizer": "TfidfVectorizer",
        "analyzer": "char_wb",
        "ngram_range": [3, 5],
        "min_df": 2,
        "max_features": 20000,
        "sublinear_tf": True,
        "dtype": "np.float32",
        "fit_policy": "fit on training rows only; transform internal eval/development validation",
    },
    "semantic_relational_features": [
        "E_code",
        "E_docs",
        "abs(E_code - E_docs)",
        "E_code * E_docs",
        "cosine(E_code, E_docs)",
    ],
    "lexical_scalar_features": [
        "log1p(shared code/docs token count)",
        "shared / union token ratio",
        "shared / min(code token count, docs token count)",
        "identifier overlap ratio",
        "changed-path token overlap ratio",
        "log1p(code text length)",
        "log1p(docs text length)",
    ],
    "feature_concatenation": [
        "code char_wb TF-IDF sparse matrix",
        "relational semantic dense matrix converted to CSR",
        "7 lexical scalar features converted to CSR",
    ],
    "classifier": {
        "class": "sklearn.linear_model.LogisticRegression",
        "C": 1.0,
        "solver": "lbfgs",
        "max_iter": 2000,
        "random_state": 42,
        "class_weight": None,
        "resampling": None,
        "multiclass_behavior": "scikit-learn lbfgs multinomial behavior for multiclass labels",
    },
    "primary_change": "Only replace frozen MiniLM embeddings with frozen Jina code-aware embeddings; keep lexical and classifier channels matched.",
}

FROZEN_BASELINES = {
    "tfidf_category_v8": {
        "model": "TF-IDF Category V8",
        "macro_f1": 0.3817290905323643,
        "balanced_accuracy": 0.41814481474407944,
        "per_class_f1": {
            "api_reference": None,
            "configuration": None,
            "developer_setup": 0.0,
            "model_contract": None,
        },
    },
    "frozen_minilm_hybrid_natural_only": {
        "model": CURRENT_HYBRID_MODEL_ID,
        "macro_f1": 0.45628987455472775,
        "balanced_accuracy": 0.478023538961039,
        "per_class_f1": {
            "api_reference": 0.5340314136125655,
            "configuration": 0.6824324324324325,
            "developer_setup": 0.0,
            "model_contract": 0.6086956521739131,
        },
        "api_catch_all": {
            "configuration_to_api_reference": 35,
            "developer_setup_to_api_reference": 5,
            "model_contract_to_api_reference": 15,
            "total_api_false_positives": 55,
        },
    },
    "codebert_joint_512": {
        "model": "microsoft/codebert-base joint classifier",
        "macro_f1": 0.2105,
        "balanced_accuracy": 0.2702,
        "per_class_f1": {
            "api_reference": None,
            "configuration": None,
            "developer_setup": 0.0,
            "model_contract": None,
        },
        "api_catch_all": {"total_api_false_positives": 143},
    },
    "modernbert_long_context_2048": {
        "model": "answerdotai/ModernBERT-base joint classifier",
        "macro_f1": 0.39070343714306566,
        "balanced_accuracy": 0.3906347377467733,
        "per_class_f1": {
            "api_reference": 0.4784688995215311,
            "configuration": 0.5816993464052288,
            "developer_setup": 0.09523809523809523,
            "model_contract": 0.4074074074074074,
        },
        "fit_diagnostic": {
            "internal_train_macro_f1": 0.772,
            "internal_eval_macro_f1": 0.406,
            "external_development_validation_macro_f1": 0.39070343714306566,
        },
    },
}

TRUNCATION_REFERENCES = {
    "codebert_v1_512": {
        "train": {
            "average_original_code_tokens": 2701,
            "average_original_diff_tokens": 2591,
            "average_original_docs_tokens": 2191,
            "average_retained_code_tokens": 286,
            "average_retained_diff_tokens": 236,
            "average_retained_docs_tokens": 212,
            "percent_diff_tokens_retained": 9.10,
            "percent_rows_with_any_truncation": 99.9,
        },
        "validation": {
            "average_original_code_tokens": 2961,
            "average_original_diff_tokens": 2824,
            "average_original_docs_tokens": 1836,
            "average_retained_diff_tokens": 232,
            "percent_diff_tokens_retained": 8.23,
            "percent_rows_with_any_truncation": 100.0,
        },
    },
    "modernbert_v2_2048": {
        "note": "Use exact V2 truncation_report.json if present after Colab; otherwise prompt-level values are not manufactured.",
    },
}


def stable_json_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    reject_confirmation_path(path)
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def reject_confirmation_path(path: Path) -> None:
    text = str(path).replace("\\", "/").lower()
    if "confirmation" in text:
        raise ValueError(f"Confirmation path is forbidden: {path}")


def reject_forbidden_row(row: dict[str, Any], *, source: str) -> None:
    case_id = str(row.get("case_id") or "<missing-case-id>")
    partition = str(row.get("partition") or "").lower()
    if partition == "confirmation":
        raise ValueError(f"{source}:{case_id}: confirmation row is forbidden")
    if row.get("controlled_design_supervision") is True:
        raise ValueError(f"{source}:{case_id}: controlled row is forbidden")
    if "controlled" in str(row.get("label_source") or "").lower():
        raise ValueError(f"{source}:{case_id}: controlled label_source is forbidden")
    if "synthetic" in str(row.get("label_source") or "").lower():
        raise ValueError(f"{source}:{case_id}: synthetic label_source is forbidden")
    if "controlled" in str(row.get("supervision_source") or "").lower():
        raise ValueError(f"{source}:{case_id}: controlled supervision_source is forbidden")
    if "synthetic" in str(row.get("supervision_source") or "").lower():
        raise ValueError(f"{source}:{case_id}: synthetic supervision_source is forbidden")


def validate_training_row(row: dict[str, Any]) -> None:
    reject_forbidden_row(row, source="training")
    if row.get("partition") != "development_train":
        raise ValueError(f"training:{row.get('case_id')}: only development_train rows may be used for training")
    if row.get("gold_doc_category") not in LABEL_SET:
        raise ValueError(f"training:{row.get('case_id')}: primary-four categories only")


def validate_export_row(row: dict[str, Any], *, source: str) -> None:
    reject_forbidden_row(row, source=source)
    extra = set(row) - SAFE_EXPORT_FIELDS
    if extra:
        raise ValueError(f"{source}:{row.get('case_id')}: unexpected export fields: {sorted(extra)}")
    if row.get("gold_doc_category") not in LABEL_SET:
        raise ValueError(f"{source}:{row.get('case_id')}: primary-four categories only")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    reject_confirmation_path(path)
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: row is not an object")
            validate_export_row(row, source=f"{path}:{line_number}")
            rows.append(row)
    return rows


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("["):
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        return [text] if text else []
    return []


def sanitize_repository_identity(text: str, repository: str) -> str:
    repo = repository.strip().strip("/")
    sanitized = str(text)
    if not repo or "/" not in repo:
        return sanitized
    owner, name = repo.split("/", 1)
    patterns = [
        re.escape(repo),
        re.escape(f"github.com/{repo}"),
        re.escape(f"https://github.com/{repo}"),
        re.escape(f"http://github.com/{repo}"),
        re.escape(f"git@github.com:{repo}"),
    ]
    for pattern in patterns:
        sanitized = re.sub(pattern, "[REPOSITORY]", sanitized, flags=re.IGNORECASE)
    return re.sub(
        rf"github\.com/{re.escape(owner)}/{re.escape(name)}(?:\.git)?",
        "[REPOSITORY]",
        sanitized,
        flags=re.IGNORECASE,
    )


def build_code_prefix_text(row: dict[str, Any]) -> str:
    text = "\n".join(
        [
            f"language: {str(row.get('language') or 'unknown').lower()}",
            "changed files:",
            "\n".join(list_value(row.get("code_changed_files"))),
            "code change:",
        ]
    )
    return sanitize_repository_identity(text, str(row.get("repository") or ""))


def build_diff_text(row: dict[str, Any]) -> str:
    return sanitize_repository_identity(str(row.get("code_diff_excerpt") or ""), str(row.get("repository") or ""))


def build_code_text(row: dict[str, Any]) -> str:
    return build_code_prefix_text(row) + "\n" + build_diff_text(row)


def build_docs_text(row: dict[str, Any]) -> str:
    return sanitize_repository_identity(str(row.get("docs_before_excerpt") or ""), str(row.get("repository") or ""))


def head_tail(ids: list[int], budget: int) -> list[int]:
    if budget <= 0:
        return []
    if len(ids) <= budget:
        return list(ids)
    head = max(1, budget // 2)
    tail = budget - head
    return list(ids[:head]) + list(ids[-tail:])


def choose_jina_max_seq_length(total_gpu_memory_gb: float) -> tuple[int, str]:
    if total_gpu_memory_gb >= 35:
        return 8192, "gpu_memory_ge_35gb"
    if total_gpu_memory_gb >= 20:
        return 4096, "gpu_memory_ge_20gb"
    return 2048, "gpu_memory_lt_20gb"


def retained_texts_for_jina(tokenizer: Any, row: dict[str, Any], *, max_seq_length: int) -> tuple[str, str, dict[str, Any]]:
    prefix_text = build_code_prefix_text(row)
    diff_text = build_diff_text(row)
    docs_text = build_docs_text(row)
    prefix_ids = tokenizer.encode(prefix_text, add_special_tokens=False)
    diff_ids = tokenizer.encode(diff_text, add_special_tokens=False)
    docs_ids = tokenizer.encode(docs_text, add_special_tokens=False)
    prefix_cap = max(1, int(max_seq_length * 0.23))
    if diff_ids:
        prefix_budget = min(len(prefix_ids), prefix_cap)
        diff_budget = max(1, max_seq_length - prefix_budget)
    else:
        prefix_budget = min(len(prefix_ids), max_seq_length)
        diff_budget = 0
    kept_prefix = head_tail(prefix_ids, prefix_budget)
    kept_diff = head_tail(diff_ids, diff_budget)
    kept_docs = head_tail(docs_ids, max_seq_length)
    if diff_ids and not kept_diff:
        raise AssertionError("non-empty code_diff_excerpt retained zero tokens")
    if docs_ids and not kept_docs:
        raise AssertionError("non-empty docs_before_excerpt retained zero tokens")
    kept_code = kept_prefix + kept_diff
    code_text = tokenizer.decode(kept_code, skip_special_tokens=True)
    docs_retained_text = tokenizer.decode(kept_docs, skip_special_tokens=True)
    stats = {
        "original_code_tokens": len(prefix_ids) + len(diff_ids),
        "original_prefix_tokens": len(prefix_ids),
        "original_diff_tokens": len(diff_ids),
        "original_docs_tokens": len(docs_ids),
        "retained_code_tokens": len(kept_code),
        "retained_prefix_tokens": len(kept_prefix),
        "retained_diff_tokens": len(kept_diff),
        "retained_docs_tokens": len(kept_docs),
        "code_truncated": len(kept_code) < len(prefix_ids) + len(diff_ids),
        "docs_truncated": len(kept_docs) < len(docs_ids),
    }
    return code_text, docs_retained_text, stats


def summarize_truncation(rows: list[dict[str, Any]], tokenizer: Any, *, max_seq_length: int) -> dict[str, Any]:
    stats = [retained_texts_for_jina(tokenizer, row, max_seq_length=max_seq_length)[2] for row in rows]

    def avg(key: str) -> float:
        return float(np.mean([item[key] for item in stats])) if stats else 0.0

    totals = {
        key: sum(item[key] for item in stats)
        for key in [
            "original_code_tokens",
            "original_diff_tokens",
            "original_docs_tokens",
            "retained_code_tokens",
            "retained_diff_tokens",
            "retained_docs_tokens",
        ]
    }
    rows_with_nonempty_original_diff = sum(item["original_diff_tokens"] > 0 for item in stats)
    rows_with_zero_retained_diff = sum(
        item["original_diff_tokens"] > 0 and item["retained_diff_tokens"] == 0 for item in stats
    )
    rows_with_nonempty_original_docs = sum(item["original_docs_tokens"] > 0 for item in stats)
    rows_with_zero_retained_docs = sum(
        item["original_docs_tokens"] > 0 and item["retained_docs_tokens"] == 0 for item in stats
    )
    if rows_with_zero_retained_diff:
        raise AssertionError("rows_with_zero_retained_diff must be 0")
    if rows_with_zero_retained_docs:
        raise AssertionError("rows_with_zero_retained_docs must be 0")
    return {
        "rows": len(rows),
        "JINA_MAX_SEQ_LENGTH": max_seq_length,
        "average_original_code_tokens": avg("original_code_tokens"),
        "average_original_prefix_tokens": avg("original_prefix_tokens"),
        "average_original_diff_tokens": avg("original_diff_tokens"),
        "average_original_docs_tokens": avg("original_docs_tokens"),
        "average_retained_code_tokens": avg("retained_code_tokens"),
        "average_retained_prefix_tokens": avg("retained_prefix_tokens"),
        "average_retained_diff_tokens": avg("retained_diff_tokens"),
        "average_retained_docs_tokens": avg("retained_docs_tokens"),
        "percent_code_tokens_retained": 100.0 * totals["retained_code_tokens"] / totals["original_code_tokens"]
        if totals["original_code_tokens"]
        else 100.0,
        "percent_diff_tokens_retained": 100.0 * totals["retained_diff_tokens"] / totals["original_diff_tokens"]
        if totals["original_diff_tokens"]
        else 100.0,
        "percent_docs_tokens_retained": 100.0 * totals["retained_docs_tokens"] / totals["original_docs_tokens"]
        if totals["original_docs_tokens"]
        else 100.0,
        "rows_with_nonempty_original_diff": rows_with_nonempty_original_diff,
        "rows_with_zero_retained_diff": rows_with_zero_retained_diff,
        "rows_with_nonempty_original_docs": rows_with_nonempty_original_docs,
        "rows_with_zero_retained_docs": rows_with_zero_retained_docs,
        "rows_with_any_truncation": sum(item["code_truncated"] or item["docs_truncated"] for item in stats),
        "rows_code_fully_preserved": sum(
            item["retained_code_tokens"] == item["original_code_tokens"] for item in stats
        ),
        "rows_docs_fully_preserved": sum(
            item["retained_docs_tokens"] == item["original_docs_tokens"] for item in stats
        ),
    }


def validate_v1_exports() -> dict[str, Any]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    train = read_jsonl(TRAIN_PATH)
    validation = read_jsonl(VALIDATION_PATH)
    for row in train:
        validate_training_row(row)
    for row in validation:
        if row.get("partition") != "development_validation":
            raise ValueError(f"validation:{row.get('case_id')}: expected development_validation")
    audit = {
        "train_rows": len(train),
        "validation_rows": len(validation),
        "train_category_counts": dict(Counter(row["gold_doc_category"] for row in train)),
        "validation_category_counts": dict(Counter(row["gold_doc_category"] for row in validation)),
        "train_validation_repository_overlap": sorted(
            {row["repository"] for row in train} & {row["repository"] for row in validation}
        ),
        "train_sha256": sha256_file(TRAIN_PATH),
        "validation_sha256": sha256_file(VALIDATION_PATH),
        "validation_case_ids_sha256": stable_json_hash([row["case_id"] for row in validation]),
        "manifest_validation_case_ids_sha256": manifest["audit"]["validation_case_ids_sha256"],
        "manifest": manifest,
    }
    if audit["train_rows"] != FROZEN_TRAIN_COUNT:
        raise AssertionError(audit["train_rows"])
    if audit["validation_rows"] != FROZEN_VALIDATION_COUNT:
        raise AssertionError(audit["validation_rows"])
    if audit["train_category_counts"] != FROZEN_TRAIN_CATEGORY_COUNTS:
        raise AssertionError(audit["train_category_counts"])
    if audit["validation_category_counts"] != FROZEN_VALIDATION_CATEGORY_COUNTS:
        raise AssertionError(audit["validation_category_counts"])
    if audit["train_validation_repository_overlap"]:
        raise AssertionError(audit["train_validation_repository_overlap"])
    if audit["train_sha256"] != FROZEN_TRAIN_SHA256:
        raise AssertionError(audit["train_sha256"])
    if audit["validation_sha256"] != FROZEN_VALIDATION_SHA256:
        raise AssertionError(audit["validation_sha256"])
    if audit["validation_case_ids_sha256"] != FROZEN_VALIDATION_CASE_IDS_SHA256:
        raise AssertionError(audit["validation_case_ids_sha256"])
    if audit["validation_case_ids_sha256"] != manifest["audit"]["validation_case_ids_sha256"]:
        raise AssertionError("manifest validation hash mismatch")
    if manifest["audit"]["confirmation_accessed"] is not False:
        raise AssertionError("confirmation access must be false")
    if manifest["controlled_or_synthetic_rows_used"] is not False:
        raise AssertionError("controlled/synthetic rows must not be used")
    if manifest["refresh_validation_used_for_training"] is not False:
        raise AssertionError("refresh validation must not be used for training")
    return audit


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_current_hybrid_audit(audit: dict[str, Any]) -> None:
    lines = [
        "# Current hybrid implementation audit",
        "",
        "This audit documents the frozen Stage-2 hybrid pipeline that V3 must match as closely as possible.",
        "",
        f"- Current frozen model: `{CURRENT_HYBRID_MODEL_ID}`",
        "- Source scripts inspected:",
        "  - `scripts/run_category_semantic_development_v1.py`",
        "  - `scripts/run_natural_diversity_refresh_category_v1.py`",
        f"- Frozen V1 train rows reused for V3: {audit['train_rows']}",
        f"- Frozen V1 validation rows reused for V3: {audit['validation_rows']}",
        f"- Validation case-id SHA256: `{audit['validation_case_ids_sha256']}`",
        "- Train/validation repository overlap: 0",
        "",
        "## Matched lexical channel",
        "",
        "- Input: sanitized code side only (`language`, `code_changed_files`, `code_diff_excerpt`).",
        "- Vectorizer: `TfidfVectorizer(analyzer=\"char_wb\", ngram_range=(3, 5), min_df=2, max_features=20000, sublinear_tf=True, dtype=np.float32)`.",
        "- Fit policy: fit only on training rows; transform internal eval/development validation.",
        "",
        "## Matched semantic relational channel",
        "",
        "- Current encoder being replaced: `sentence-transformers/all-MiniLM-L6-v2` revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.",
        f"- V3 encoder: `{JINA_MODEL_NAME}` frozen, resolved to an exact Hugging Face SHA at Colab runtime.",
        "- Separate embeddings: `E_code = encoder(code_side)`, `E_docs = encoder(docs_before)`.",
        "- Relational features: `E_code`, `E_docs`, `abs(E_code - E_docs)`, `E_code * E_docs`, `cosine(E_code, E_docs)`.",
        "- Embeddings are normalized; cosine is therefore dot product.",
        "",
        "## Matched scalar features",
        "",
        "Seven lexical relational scalars are reused: shared-token log count, shared/union ratio, shared/min-side ratio, identifier overlap ratio, changed-path token overlap ratio, log code length, log docs length.",
        "",
        "## Matched classifier",
        "",
        "- Classifier: `LogisticRegression(C=1.0, solver=\"lbfgs\", max_iter=2000, random_state=42)`.",
        "- Class weights: none.",
        "- Resampling: none.",
        "- No grid search, no threshold tuning, no class balancing.",
        "",
        "## Primary controlled change",
        "",
        "Only the frozen semantic encoder changes from MiniLM to Jina code-aware embeddings. The lexical feature family, relational feature construction, sparse/dense concatenation, and Logistic Regression configuration remain matched.",
        "",
    ]
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text("\n".join(lines), encoding="utf-8")
    write_json(EXPERIMENT_DIR / "current_hybrid_implementation_audit.json", CURRENT_HYBRID_IMPLEMENTATION)


def nb_cell(cell_type: str, source: str) -> dict[str, Any]:
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.strip("\n").splitlines()],
        **({"outputs": [], "execution_count": None} if cell_type == "code" else {}),
    }


def make_notebook() -> dict[str, Any]:
    title = """
# Stage-2 Architecture Challenge V3: Frozen code-aware Jina hybrid

This notebook runs one bounded representation experiment: replace the frozen MiniLM semantic encoder in the current natural-only hybrid with `jinaai/jina-embeddings-v2-base-code`, while keeping the matched code TF-IDF channel, relational feature design, scalar features, and multinomial Logistic Regression classifier. It does not fine-tune Jina, does not acquire data, does not use confirmation, and does not use controlled/synthetic rows.
"""
    deps = """
# Python 3.13 compatible Colab stack. Keep Colab's CUDA torch build.
!python -m pip install -q \\
  "sentence-transformers==6.0.1" \\
  "transformers==4.56.2" \\
  "tokenizers==0.22.0" \\
  "huggingface_hub==0.34.4" \\
  "safetensors==0.6.2" \\
  "accelerate==1.10.1" \\
  "scikit-learn==1.7.2" \\
  "matplotlib==3.10.6" \\
  "scipy"
"""
    imports = """
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import random
import re
import sys
import time
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy
import sklearn
import torch
import transformers
import tokenizers
from huggingface_hub import HfApi, __version__ as hf_hub_version
from scipy import sparse
from sentence_transformers import SentenceTransformer, __version__ as sentence_transformers_version
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import GroupShuffleSplit

print("Python:", sys.version)
print("torch:", torch.__version__)
print("CUDA availability:", torch.cuda.is_available())
print("CUDA device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NONE")
print("sentence_transformers:", sentence_transformers_version)
print("transformers:", transformers.__version__)
print("tokenizers:", tokenizers.__version__)
print("huggingface_hub:", hf_hub_version)
print("sklearn:", sklearn.__version__)
assert torch.cuda.is_available(), "CUDA GPU is required for Jina embedding extraction."
"""
    data_import = """
REQUIRED_EXPORT_FILES = ["natural_train_primary_four.jsonl", "natural_validation_primary_four.jsonl", "export_manifest.json"]


def has_frozen_v1_export(root):
    export_dir = Path(root) / "data" / "final_v2" / "architecture_challenge_v1"
    return all((export_dir / name).exists() for name in REQUIRED_EXPORT_FILES)


def locate_frozen_v1_root():
    candidates = [
        Path.cwd(),
        Path("/content/MASTER-RAD-PROJEKAT"),
        Path("/content/MASTER RAD PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER-RAD-PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER RAD PROJEKAT"),
    ]
    for candidate in candidates:
        if has_frozen_v1_export(candidate):
            return candidate
    for manifest in Path("/content").glob("**/export_manifest.json"):
        possible_root = manifest.parent.parent.parent.parent
        if has_frozen_v1_export(possible_root):
            return possible_root
    return None


ROOT = locate_frozen_v1_root()
if ROOT is None:
    print("Frozen V1 export nije pronađen. Uploaduj ZIP repozitorija ili direktno 3 V1 export fajla.")
    for name in REQUIRED_EXPORT_FILES:
        print("-", name)
    from google.colab import files

    uploaded = files.upload()
    upload_root = Path("/content/MASTER-RAD-PROJEKAT")
    export_dir = upload_root / "data" / "final_v2" / "architecture_challenge_v1"
    export_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in uploaded.items():
        base = Path(name).name
        if base.lower().endswith(".zip"):
            zip_path = upload_root / base
            zip_path.write_bytes(payload)
            with zipfile.ZipFile(zip_path) as archive:
                archive.extractall(upload_root)
        elif base in REQUIRED_EXPORT_FILES:
            (export_dir / base).write_bytes(payload)
    ROOT = locate_frozen_v1_root()
assert ROOT is not None and has_frozen_v1_export(ROOT), "Missing frozen V1 export files."
print("Using repository/data root:", ROOT)
"""
    config = f"""
EXPORT_DIR = ROOT / "data" / "final_v2" / "architecture_challenge_v1"
TRAIN_PATH = EXPORT_DIR / "natural_train_primary_four.jsonl"
VALIDATION_PATH = EXPORT_DIR / "natural_validation_primary_four.jsonl"
MANIFEST_PATH = EXPORT_DIR / "export_manifest.json"
OUTPUT_DIR = ROOT / "experiments" / "category_architecture_challenge_v3" / "jina_code_hybrid"
FIGURES_DIR = OUTPUT_DIR / "figures"
CACHE_DIR = OUTPUT_DIR / "cache"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

LABELS = {LABELS!r}
LABEL_TO_ID = {{label: index for index, label in enumerate(LABELS)}}
SEED = 42
JINA_MODEL_NAME = "{JINA_MODEL_NAME}"
PRIMARY_MODEL_ID = "{PRIMARY_MODEL_ID}"
CURRENT_HYBRID_MODEL_ID = "{CURRENT_HYBRID_MODEL_ID}"
FROZEN_VALIDATION_CASE_IDS_SHA256 = "{FROZEN_VALIDATION_CASE_IDS_SHA256}"
FROZEN_BASELINES = {json.dumps(FROZEN_BASELINES, indent=2)}
TRUNCATION_REFERENCES = {json.dumps(TRUNCATION_REFERENCES, indent=2)}

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
"""
    helpers = r'''
def stable_json_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def reject_confirmation_path(path):
    if "confirmation" in str(path).replace("\\", "/").lower():
        raise ValueError(f"Confirmation path is forbidden: {path}")


def read_jsonl(path):
    reject_confirmation_path(path)
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("partition") == "confirmation":
                raise ValueError(f"{path}:{line_number}: confirmation row is forbidden")
            rows.append(row)
    return rows


def list_value(value):
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("["):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except json.JSONDecodeError:
                pass
        return [text] if text else []
    return []


def sanitize_repository_identity(text, repository):
    repo = str(repository or "").strip().strip("/")
    sanitized = str(text)
    if not repo or "/" not in repo:
        return sanitized
    owner, name = repo.split("/", 1)
    patterns = [
        re.escape(repo),
        re.escape(f"github.com/{repo}"),
        re.escape(f"https://github.com/{repo}"),
        re.escape(f"http://github.com/{repo}"),
        re.escape(f"git@github.com:{repo}"),
    ]
    for pattern in patterns:
        sanitized = re.sub(pattern, "[REPOSITORY]", sanitized, flags=re.IGNORECASE)
    return re.sub(rf"github\.com/{re.escape(owner)}/{re.escape(name)}(?:\.git)?", "[REPOSITORY]", sanitized, flags=re.IGNORECASE)


def build_code_prefix_text(row):
    text = "\n".join([
        f"language: {str(row.get('language') or 'unknown').lower()}",
        "changed files:",
        "\n".join(list_value(row.get("code_changed_files"))),
        "code change:",
    ])
    return sanitize_repository_identity(text, row.get("repository") or "")


def build_diff_text(row):
    return sanitize_repository_identity(row.get("code_diff_excerpt") or "", row.get("repository") or "")


def build_code_text(row):
    return build_code_prefix_text(row) + "\n" + build_diff_text(row)


def build_docs_text(row):
    return sanitize_repository_identity(row.get("docs_before_excerpt") or "", row.get("repository") or "")


def head_tail(ids, budget):
    if budget <= 0:
        return []
    if len(ids) <= budget:
        return list(ids)
    head = max(1, budget // 2)
    tail = budget - head
    return list(ids[:head]) + list(ids[-tail:])


def choose_jina_max_seq_length(total_gpu_memory_gb):
    if total_gpu_memory_gb >= 35:
        return 8192, "gpu_memory_ge_35gb"
    if total_gpu_memory_gb >= 20:
        return 4096, "gpu_memory_ge_20gb"
    return 2048, "gpu_memory_lt_20gb"


def choose_encode_batch_size(total_gpu_memory_gb):
    return 2


def retained_texts_for_jina(tokenizer, row, max_seq_length):
    prefix_ids = tokenizer.encode(build_code_prefix_text(row), add_special_tokens=False)
    diff_ids = tokenizer.encode(build_diff_text(row), add_special_tokens=False)
    docs_ids = tokenizer.encode(build_docs_text(row), add_special_tokens=False)
    prefix_cap = max(1, int(max_seq_length * 0.23))
    if diff_ids:
        prefix_budget = min(len(prefix_ids), prefix_cap)
        diff_budget = max(1, max_seq_length - prefix_budget)
    else:
        prefix_budget = min(len(prefix_ids), max_seq_length)
        diff_budget = 0
    kept_prefix = head_tail(prefix_ids, prefix_budget)
    kept_diff = head_tail(diff_ids, diff_budget)
    kept_docs = head_tail(docs_ids, max_seq_length)
    assert not (diff_ids and not kept_diff), "non-empty diff retained zero tokens"
    assert not (docs_ids and not kept_docs), "non-empty docs retained zero tokens"
    kept_code = kept_prefix + kept_diff
    return (
        tokenizer.decode(kept_code, skip_special_tokens=True),
        tokenizer.decode(kept_docs, skip_special_tokens=True),
        {
            "original_code_tokens": len(prefix_ids) + len(diff_ids),
            "original_prefix_tokens": len(prefix_ids),
            "original_diff_tokens": len(diff_ids),
            "original_docs_tokens": len(docs_ids),
            "retained_code_tokens": len(kept_code),
            "retained_prefix_tokens": len(kept_prefix),
            "retained_diff_tokens": len(kept_diff),
            "retained_docs_tokens": len(kept_docs),
            "code_truncated": len(kept_code) < len(prefix_ids) + len(diff_ids),
            "docs_truncated": len(kept_docs) < len(docs_ids),
        },
    )


def summarize_truncation(rows, tokenizer, max_seq_length):
    stats = [retained_texts_for_jina(tokenizer, row, max_seq_length)[2] for row in rows]
    def avg(key):
        return float(np.mean([s[key] for s in stats]))
    totals = {key: sum(s[key] for s in stats) for key in ["original_code_tokens", "original_diff_tokens", "original_docs_tokens", "retained_code_tokens", "retained_diff_tokens", "retained_docs_tokens"]}
    rows_with_zero_retained_diff = sum(s["original_diff_tokens"] > 0 and s["retained_diff_tokens"] == 0 for s in stats)
    rows_with_zero_retained_docs = sum(s["original_docs_tokens"] > 0 and s["retained_docs_tokens"] == 0 for s in stats)
    assert rows_with_zero_retained_diff == 0
    assert rows_with_zero_retained_docs == 0
    return {
        "rows": len(rows),
        "JINA_MAX_SEQ_LENGTH": max_seq_length,
        "average_original_code_tokens": avg("original_code_tokens"),
        "average_original_prefix_tokens": avg("original_prefix_tokens"),
        "average_original_diff_tokens": avg("original_diff_tokens"),
        "average_original_docs_tokens": avg("original_docs_tokens"),
        "average_retained_code_tokens": avg("retained_code_tokens"),
        "average_retained_prefix_tokens": avg("retained_prefix_tokens"),
        "average_retained_diff_tokens": avg("retained_diff_tokens"),
        "average_retained_docs_tokens": avg("retained_docs_tokens"),
        "percent_code_tokens_retained": 100.0 * totals["retained_code_tokens"] / totals["original_code_tokens"] if totals["original_code_tokens"] else 100.0,
        "percent_diff_tokens_retained": 100.0 * totals["retained_diff_tokens"] / totals["original_diff_tokens"] if totals["original_diff_tokens"] else 100.0,
        "percent_docs_tokens_retained": 100.0 * totals["retained_docs_tokens"] / totals["original_docs_tokens"] if totals["original_docs_tokens"] else 100.0,
        "rows_with_nonempty_original_diff": sum(s["original_diff_tokens"] > 0 for s in stats),
        "rows_with_zero_retained_diff": rows_with_zero_retained_diff,
        "rows_with_nonempty_original_docs": sum(s["original_docs_tokens"] > 0 for s in stats),
        "rows_with_zero_retained_docs": rows_with_zero_retained_docs,
        "rows_with_any_truncation": sum(s["code_truncated"] or s["docs_truncated"] for s in stats),
        "rows_code_fully_preserved": sum(s["retained_code_tokens"] == s["original_code_tokens"] for s in stats),
        "rows_docs_fully_preserved": sum(s["retained_docs_tokens"] == s["original_docs_tokens"] for s in stats),
    }


TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{1,}")


def token_set(text):
    return {token.lower() for token in TOKEN_RE.findall(text)}


def lexical_relational_scalars(rows):
    values = []
    for row in rows:
        code_text = build_code_text(row)
        docs_text = build_docs_text(row)
        code_tokens = token_set(code_text)
        docs_tokens = token_set(docs_text)
        shared = code_tokens & docs_tokens
        union = code_tokens | docs_tokens
        identifiers = {token for token in code_tokens if "_" in token or any(char.isupper() for char in token)}
        path_tokens = token_set(" ".join(list_value(row.get("code_changed_files"))))
        values.append([
            math.log1p(len(shared)),
            len(shared) / max(1, len(union)),
            len(shared) / max(1, min(len(code_tokens), len(docs_tokens))),
            len(identifiers & docs_tokens) / max(1, len(identifiers)),
            len(path_tokens & docs_tokens) / max(1, len(path_tokens)),
            math.log1p(len(code_text)),
            math.log1p(len(docs_text)),
        ])
    return np.asarray(values, dtype=np.float32)


def relational_semantic_features(code, docs):
    if code.shape != docs.shape:
        raise ValueError(f"Embedding shape mismatch: {code.shape} vs {docs.shape}")
    cosine = np.sum(code * docs, axis=1, keepdims=True)
    return np.hstack([code, docs, np.abs(code - docs), code * docs, cosine]).astype(np.float32)


def make_classifier():
    return LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED)


def labels_for(rows):
    return np.asarray([row["gold_doc_category"] for row in rows])


def metric_bundle(y_true, y_pred):
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=LABELS, zero_division=0)
    matrix = confusion_matrix(y_true, y_pred, labels=LABELS)
    normalized = matrix.astype(float) / np.maximum(matrix.sum(axis=1, keepdims=True), 1)
    return {
        "support": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="weighted", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "per_class": {label: {"precision": float(precision[i]), "recall": float(recall[i]), "f1": float(f1[i]), "support": int(support[i])} for i, label in enumerate(LABELS)},
        "confusion_matrix": matrix.tolist(),
        "normalized_confusion_matrix": normalized.tolist(),
        "predicted_class_counts": dict(sorted(Counter(map(str, y_pred)).items())),
    }


def probabilities(model, features):
    raw = np.asarray(model.predict_proba(features), dtype=float)
    out = np.zeros((raw.shape[0], len(LABELS)), dtype=float)
    for source_index, label in enumerate(map(str, model.classes_)):
        out[:, LABELS.index(label)] = raw[:, source_index]
    return out


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
'''
    audit_load = """
manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
train_rows = read_jsonl(TRAIN_PATH)
validation_rows = read_jsonl(VALIDATION_PATH)
assert len(train_rows) == 1038
assert len(validation_rows) == 322
assert Counter(row["gold_doc_category"] for row in train_rows) == {"api_reference": 412, "configuration": 277, "developer_setup": 88, "model_contract": 261}
assert Counter(row["gold_doc_category"] for row in validation_rows) == {"api_reference": 85, "configuration": 154, "developer_setup": 19, "model_contract": 64}
assert set(row["partition"] for row in train_rows) == {"development_train"}
assert set(row["partition"] for row in validation_rows) == {"development_validation"}
assert not ({row["repository"] for row in train_rows} & {row["repository"] for row in validation_rows})
assert sha256_file(TRAIN_PATH) == manifest["artifacts"]["natural_train_primary_four.jsonl"]["sha256"]
assert sha256_file(VALIDATION_PATH) == manifest["artifacts"]["natural_validation_primary_four.jsonl"]["sha256"]
validation_case_hash = stable_json_hash([row["case_id"] for row in validation_rows])
assert validation_case_hash == manifest["audit"]["validation_case_ids_sha256"] == FROZEN_VALIDATION_CASE_IDS_SHA256
assert manifest["audit"]["confirmation_accessed"] is False
assert manifest["controlled_or_synthetic_rows_used"] is False
assert manifest["refresh_validation_used_for_training"] is False
print("Frozen V1 natural export verified.")
"""
    model_smoke = """
gpu_props = torch.cuda.get_device_properties(0)
total_gpu_memory_gb = gpu_props.total_memory / (1024 ** 3)
JINA_MAX_SEQ_LENGTH, max_length_branch = choose_jina_max_seq_length(total_gpu_memory_gb)
ENCODE_BATCH_SIZE = choose_encode_batch_size(total_gpu_memory_gb)
print({"gpu_memory_gb": total_gpu_memory_gb, "JINA_MAX_SEQ_LENGTH": JINA_MAX_SEQ_LENGTH, "batch_size": ENCODE_BATCH_SIZE, "branch": max_length_branch})

api = HfApi()
jina_info = api.model_info(JINA_MODEL_NAME)
JINA_MODEL_REVISION_SHA = jina_info.sha
print("Resolved Jina revision:", JINA_MODEL_REVISION_SHA)

device = "cuda"
load_started = time.time()
jina_model = SentenceTransformer(
    JINA_MODEL_NAME,
    revision=JINA_MODEL_REVISION_SHA,
    trust_remote_code=True,
    device=device,
)
jina_model.max_seq_length = JINA_MAX_SEQ_LENGTH
jina_model.eval()
if hasattr(jina_model, "parameters"):
    for parameter in jina_model.parameters():
        parameter.requires_grad_(False)

tokenizer = getattr(jina_model, "tokenizer", None)
assert tokenizer is not None, "Jina tokenizer is required for deterministic head/tail retention."

code_sample, docs_sample, sample_stats = retained_texts_for_jina(tokenizer, train_rows[0], JINA_MAX_SEQ_LENGTH)
smoke_started = time.time()
with torch.inference_mode():
    emb1 = jina_model.encode([code_sample, docs_sample], batch_size=1, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False, device=device)
    duplicate_a = jina_model.encode(["deterministic duplicate smoke"], batch_size=1, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False, device=device)
    duplicate_b = jina_model.encode(["deterministic duplicate smoke"], batch_size=1, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False, device=device)
assert np.all(np.isfinite(emb1))
assert emb1.ndim == 2 and emb1.shape[0] == 2 and emb1.shape[1] > 0
assert np.all(np.linalg.norm(emb1, axis=1) > 0)
assert np.allclose(np.linalg.norm(emb1, axis=1), 1.0, atol=1e-3)
assert np.allclose(duplicate_a, duplicate_b, atol=1e-5)
print({"embedding_dim": int(emb1.shape[1]), "sample_stats": sample_stats, "smoke_seconds": time.time() - smoke_started})
"""
    truncation_embeddings = """
truncation_report = {
    "train": summarize_truncation(train_rows, tokenizer, JINA_MAX_SEQ_LENGTH),
    "validation": summarize_truncation(validation_rows, tokenizer, JINA_MAX_SEQ_LENGTH),
    "references": TRUNCATION_REFERENCES,
}
assert truncation_report["train"]["rows_with_zero_retained_diff"] == 0
assert truncation_report["validation"]["rows_with_zero_retained_diff"] == 0
assert truncation_report["train"]["rows_with_zero_retained_docs"] == 0
assert truncation_report["validation"]["rows_with_zero_retained_docs"] == 0
write_json(OUTPUT_DIR / "truncation_report.json", truncation_report)
print(json.dumps(truncation_report, indent=2))


def prepare_retained_texts(rows):
    code_texts, docs_texts = [], []
    for row in rows:
        code_text, docs_text, _stats = retained_texts_for_jina(tokenizer, row, JINA_MAX_SEQ_LENGTH)
        code_texts.append(code_text)
        docs_texts.append(docs_text)
    return code_texts, docs_texts


train_code_texts, train_docs_texts = prepare_retained_texts(train_rows)
validation_code_texts, validation_docs_texts = prepare_retained_texts(validation_rows)


def embedding_cache_key(side, texts):
    return stable_json_hash({
        "model": JINA_MODEL_NAME,
        "revision": JINA_MODEL_REVISION_SHA,
        "side": side,
        "max_seq_length": JINA_MAX_SEQ_LENGTH,
        "normalize_embeddings": True,
        "content_hash": stable_json_hash(texts),
    })


def encode_cached(side, texts):
    key = embedding_cache_key(side, texts)
    npy_path = CACHE_DIR / f"{side}_{key}.npy"
    meta_path = CACHE_DIR / f"{side}_{key}.json"
    if npy_path.exists() and meta_path.exists():
        return np.load(npy_path), json.loads(meta_path.read_text(encoding="utf-8")) | {"cache_hit": True}
    started = time.time()
    try:
        with torch.inference_mode():
            embeddings = jina_model.encode(texts, batch_size=ENCODE_BATCH_SIZE, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=True, device=device).astype(np.float32)
    except torch.cuda.OutOfMemoryError:
        if ENCODE_BATCH_SIZE != 1:
            torch.cuda.empty_cache()
            print("OOM at batch_size=2; retrying once at batch_size=1 with unchanged context length.")
            with torch.inference_mode():
                embeddings = jina_model.encode(texts, batch_size=1, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=True, device=device).astype(np.float32)
        else:
            raise RuntimeError("OOM at batch_size=1 and JINA_MAX_SEQ_LENGTH unchanged; stop and report.")
    np.save(npy_path, embeddings)
    meta = {
        "side": side,
        "row_count": len(texts),
        "embedding_dimension": int(embeddings.shape[1]),
        "cache_key": key,
        "cache_hit": False,
        "npy_path": str(npy_path),
        "bytes": int(npy_path.stat().st_size),
        "elapsed_seconds": time.time() - started,
        "content_hash": stable_json_hash(texts),
    }
    write_json(meta_path, meta)
    return embeddings, meta


train_code_embeddings, train_code_cache = encode_cached("train_code", train_code_texts)
train_docs_embeddings, train_docs_cache = encode_cached("train_docs", train_docs_texts)
validation_code_embeddings, validation_code_cache = encode_cached("validation_code", validation_code_texts)
validation_docs_embeddings, validation_docs_cache = encode_cached("validation_docs", validation_docs_texts)
"""
    feature_fit = """
def select_internal_split(rows):
    y = labels_for(rows)
    groups = np.asarray([row["repository"] for row in rows])
    indices = np.arange(len(rows))
    for split_seed in [42, 43, 44, 45, 46]:
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=split_seed)
        train_idx, eval_idx = next(splitter.split(indices, y, groups))
        if set(groups[train_idx]) & set(groups[eval_idx]):
            continue
        if set(y[train_idx]) == set(LABELS) and set(y[eval_idx]) == set(LABELS):
            return train_idx, eval_idx, split_seed
    raise RuntimeError("No valid internal grouped split in predefined seeds.")


def build_features(train_subset_rows, eval_subset_rows, train_subset_code_emb, train_subset_docs_emb, eval_code_emb, eval_docs_emb):
    code_vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=20000,
        sublinear_tf=True,
        dtype=np.float32,
    )
    code_train = code_vectorizer.fit_transform([build_code_text(row) for row in train_subset_rows])
    code_eval = code_vectorizer.transform([build_code_text(row) for row in eval_subset_rows])
    train_semantic = relational_semantic_features(train_subset_code_emb, train_subset_docs_emb)
    eval_semantic = relational_semantic_features(eval_code_emb, eval_docs_emb)
    train_features = sparse.hstack([code_train, sparse.csr_matrix(train_semantic), sparse.csr_matrix(lexical_relational_scalars(train_subset_rows))], format="csr")
    eval_features = sparse.hstack([code_eval, sparse.csr_matrix(eval_semantic), sparse.csr_matrix(lexical_relational_scalars(eval_subset_rows))], format="csr")
    return train_features, eval_features, {
        "code_vocabulary_size": len(code_vectorizer.vocabulary_),
        "vectorizer_fit_rows": len(train_subset_rows),
        "validation_never_enters_vectorizer_fit": True,
        "lexical_vectorizer": {
            "class": "TfidfVectorizer",
            "analyzer": "char_wb",
            "ngram_range": [3, 5],
            "min_df": 2,
            "max_features": 20000,
            "sublinear_tf": True,
            "dtype": "np.float32",
        },
    }


def fit_and_predict(train_subset_rows, eval_subset_rows, train_subset_code_emb, train_subset_docs_emb, eval_code_emb, eval_docs_emb):
    x_train, x_eval, feature_meta = build_features(train_subset_rows, eval_subset_rows, train_subset_code_emb, train_subset_docs_emb, eval_code_emb, eval_docs_emb)
    y_train = labels_for(train_subset_rows)
    y_eval = labels_for(eval_subset_rows)
    model = make_classifier()
    model.fit(x_train, y_train)
    train_pred = model.predict(x_train)
    eval_pred = model.predict(x_eval)
    eval_probs = probabilities(model, x_eval)
    records = []
    for row, gold, pred, prob in zip(eval_subset_rows, y_eval, eval_pred, eval_probs):
        records.append({
            "case_id": row["case_id"],
            "gold": str(gold),
            "prediction": str(pred),
            "correct": str(gold) == str(pred),
            "probabilities": {label: float(prob[LABELS.index(label)]) for label in LABELS},
        })
    return {
        "model": model,
        "train_metrics": metric_bundle(y_train, train_pred),
        "eval_metrics": metric_bundle(y_eval, eval_pred),
        "eval_predictions": records,
        "eval_probabilities": eval_probs,
        "feature_meta": feature_meta,
    }


internal_train_idx, internal_eval_idx, internal_split_seed = select_internal_split(train_rows)
internal_result = fit_and_predict(
    [train_rows[i] for i in internal_train_idx],
    [train_rows[i] for i in internal_eval_idx],
    train_code_embeddings[internal_train_idx],
    train_docs_embeddings[internal_train_idx],
    train_code_embeddings[internal_eval_idx],
    train_docs_embeddings[internal_eval_idx],
)
internal_train_metrics = internal_result["train_metrics"]
internal_eval_metrics = internal_result["eval_metrics"]
write_json(OUTPUT_DIR / "internal_train_metrics.json", internal_train_metrics)
write_json(OUTPUT_DIR / "internal_eval_metrics.json", internal_eval_metrics)
print("Internal split seed:", internal_split_seed)
print("Internal train/eval Macro-F1:", internal_train_metrics["macro_f1"], internal_eval_metrics["macro_f1"])

final_result = fit_and_predict(
    train_rows,
    validation_rows,
    train_code_embeddings,
    train_docs_embeddings,
    validation_code_embeddings,
    validation_docs_embeddings,
)
metrics = final_result["eval_metrics"]
validation_predictions = final_result["eval_predictions"]
validation_probabilities = final_result["eval_probabilities"]
write_json(OUTPUT_DIR / "metrics.json", metrics)
with open(OUTPUT_DIR / "validation_predictions.jsonl", "w", encoding="utf-8", newline="\\n") as handle:
    for record in validation_predictions:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\\n")
print(json.dumps(metrics, indent=2))
"""
    diagnostics = """
dev_rows = []
dev_id = LABELS.index("developer_setup")
rank_counts = Counter()
for row, record, prob in zip(validation_rows, validation_predictions, validation_probabilities):
    ranked = list(np.argsort(prob)[::-1])
    dev_rank = ranked.index(dev_id) + 1
    if row["gold_doc_category"] == "developer_setup":
        rank_counts[dev_rank] += 1
        dev_rows.append({
            "case_id": row["case_id"],
            "prediction": record["prediction"],
            "probabilities": record["probabilities"],
            "decision_scores": record["probabilities"],
            "developer_setup_rank": dev_rank,
            "developer_setup_probability": float(prob[dev_id]),
            "top_2_classes": [LABELS[int(i)] for i in ranked[:2]],
        })
dev_true_probs = [float(prob[dev_id]) for row, prob in zip(validation_rows, validation_probabilities) if row["gold_doc_category"] == "developer_setup"]
dev_other_probs = [float(prob[dev_id]) for row, prob in zip(validation_rows, validation_probabilities) if row["gold_doc_category"] != "developer_setup"]
developer_setup_predictions = {
    "rows": dev_rows,
    "correct_out_of_19": sum(item["prediction"] == "developer_setup" for item in dev_rows),
    "support": len(dev_rows),
    "precision": metrics["per_class"]["developer_setup"]["precision"],
    "recall": metrics["per_class"]["developer_setup"]["recall"],
    "f1": metrics["per_class"]["developer_setup"]["f1"],
    "rank_counts": {str(rank): rank_counts.get(rank, 0) for rank in [1, 2, 3, 4]},
    "mean_developer_setup_probability_for_true_setup": float(np.mean(dev_true_probs)),
    "mean_developer_setup_probability_for_non_setup": float(np.mean(dev_other_probs)),
}
write_json(OUTPUT_DIR / "developer_setup_predictions.json", developer_setup_predictions)

pairs = [(record["gold"], record["prediction"]) for record in validation_predictions]
configuration_setup_diagnostics = {
    "developer_setup_to_configuration": sum(g == "developer_setup" and p == "configuration" for g, p in pairs),
    "configuration_to_developer_setup": sum(g == "configuration" and p == "developer_setup" for g, p in pairs),
}
write_json(OUTPUT_DIR / "configuration_setup_diagnostics.json", configuration_setup_diagnostics)

api_catch_all = {
    "configuration_to_api_reference": sum(g == "configuration" and p == "api_reference" for g, p in pairs),
    "developer_setup_to_api_reference": sum(g == "developer_setup" and p == "api_reference" for g, p in pairs),
    "model_contract_to_api_reference": sum(g == "model_contract" and p == "api_reference" for g, p in pairs),
}
api_catch_all["total_api_false_positives"] = sum(api_catch_all.values())
api_catch_all["prior_references"] = {
    "current_hybrid": FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"].get("api_catch_all"),
    "codebert_joint_512": FROZEN_BASELINES["codebert_joint_512"].get("api_catch_all"),
}
write_json(OUTPUT_DIR / "api_catch_all_diagnostics.json", api_catch_all)
"""
    bootstrap_figures = """
def plot_matrix(matrix, path, title, normalized=False):
    matrix = np.asarray(matrix)
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(matrix, cmap="Blues", vmin=0 if normalized else None, vmax=1 if normalized else None)
    ax.set_title(title)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Gold")
    ax.set_xticks(range(len(LABELS)), LABELS, rotation=30, ha="right")
    ax.set_yticks(range(len(LABELS)), LABELS)
    for i in range(len(LABELS)):
        for j in range(len(LABELS)):
            ax.text(j, i, f"{matrix[i, j]:.2f}" if normalized else str(int(matrix[i, j])), ha="center", va="center")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


plot_matrix(metrics["confusion_matrix"], FIGURES_DIR / "jina_confusion_matrix.png", "Jina hybrid confusion matrix")
plot_matrix(metrics["normalized_confusion_matrix"], FIGURES_DIR / "jina_normalized_confusion_matrix.png", "Jina hybrid row-normalized confusion matrix", normalized=True)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(LABELS, [metrics["per_class"][label]["f1"] for label in LABELS])
ax.set_ylim(0, 1)
ax.set_title("Jina hybrid per-class F1")
ax.tick_params(axis="x", rotation=25)
fig.tight_layout()
fig.savefig(FIGURES_DIR / "jina_per_class_f1.png", dpi=180)
plt.close(fig)

comparison = {
    "tfidf_category_v8": FROZEN_BASELINES["tfidf_category_v8"],
    "frozen_minilm_hybrid_natural_only": FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"],
    "codebert_joint_512": FROZEN_BASELINES["codebert_joint_512"],
    "modernbert_long_context_2048": FROZEN_BASELINES["modernbert_long_context_2048"],
    "jina_code_hybrid": {
        "model": PRIMARY_MODEL_ID,
        "macro_f1": metrics["macro_f1"],
        "balanced_accuracy": metrics["balanced_accuracy"],
        "per_class_f1": {label: metrics["per_class"][label]["f1"] for label in LABELS},
    },
}
write_json(OUTPUT_DIR / "comparison_with_prior_models.json", comparison)

model_order = ["tfidf_category_v8", "frozen_minilm_hybrid_natural_only", "codebert_joint_512", "modernbert_long_context_2048", "jina_code_hybrid"]
names = ["TF-IDF V8", "MiniLM hybrid", "CodeBERT 512", "ModernBERT 2048", "Jina hybrid"]
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(names, [comparison[key]["macro_f1"] for key in model_order])
ax.set_ylim(0, 1)
ax.set_ylabel("Macro-F1")
ax.tick_params(axis="x", rotation=25)
fig.tight_layout()
fig.savefig(FIGURES_DIR / "architecture_comparison_macro_f1.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(names, [comparison[key]["balanced_accuracy"] for key in model_order])
ax.set_ylim(0, 1)
ax.set_ylabel("Balanced accuracy")
ax.tick_params(axis="x", rotation=25)
fig.tight_layout()
fig.savefig(FIGURES_DIR / "architecture_comparison_balanced_accuracy.png", dpi=180)
plt.close(fig)

hybrid_f1 = comparison["frozen_minilm_hybrid_natural_only"]["per_class_f1"]
jina_f1 = comparison["jina_code_hybrid"]["per_class_f1"]
x = np.arange(len(LABELS))
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - 0.18, [hybrid_f1[label] for label in LABELS], width=0.36, label="MiniLM hybrid")
ax.bar(x + 0.18, [jina_f1[label] for label in LABELS], width=0.36, label="Jina hybrid")
ax.set_xticks(x, LABELS, rotation=25)
ax.set_ylim(0, 1)
ax.set_ylabel("F1")
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES_DIR / "hybrid_vs_jina_per_class_f1.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(["internal train", "internal repo eval", "external validation"], [internal_train_metrics["macro_f1"], internal_eval_metrics["macro_f1"], metrics["macro_f1"]])
ax.set_ylim(0, 1)
ax.set_ylabel("Macro-F1")
ax.set_title("Jina hybrid train/eval gap")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "jina_internal_train_eval_gap.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(["code retained %", "diff retained %", "docs retained %"], [
    truncation_report["validation"]["percent_code_tokens_retained"],
    truncation_report["validation"]["percent_diff_tokens_retained"],
    truncation_report["validation"]["percent_docs_tokens_retained"],
])
ax.set_ylim(0, 100)
ax.set_ylabel("Percent retained")
ax.set_title("Jina validation evidence retention")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "jina_truncation_retention.png", dpi=180)
plt.close(fig)


def load_hybrid_predictions_if_valid():
    path = ROOT / "experiments" / "natural_diversity_refresh_category_v1" / "old_development_validation_predictions.jsonl"
    if not path.exists():
        return None
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    validation_ids = [row["case_id"] for row in validation_rows]
    if [row.get("case_id") for row in rows] != validation_ids:
        return None
    if stable_json_hash(validation_ids) != FROZEN_VALIDATION_CASE_IDS_SHA256:
        return None
    return rows


def paired_bootstrap(hybrid_records):
    rng = np.random.default_rng(SEED)
    gold = np.asarray([record["gold"] for record in validation_predictions])
    jina_pred = np.asarray([record["prediction"] for record in validation_predictions])
    hybrid_pred = np.asarray([record["prediction"] for record in hybrid_records])
    n = len(gold)
    deltas = {"macro_f1": [], "balanced_accuracy": []}
    per_class = {label: [] for label in LABELS}
    for _ in range(2000):
        idx = rng.integers(0, n, size=n)
        deltas["macro_f1"].append(f1_score(gold[idx], jina_pred[idx], labels=LABELS, average="macro", zero_division=0) - f1_score(gold[idx], hybrid_pred[idx], labels=LABELS, average="macro", zero_division=0))
        deltas["balanced_accuracy"].append(balanced_accuracy_score(gold[idx], jina_pred[idx]) - balanced_accuracy_score(gold[idx], hybrid_pred[idx]))
        hybrid_cls = precision_recall_fscore_support(gold[idx], hybrid_pred[idx], labels=LABELS, zero_division=0)[2]
        jina_cls = precision_recall_fscore_support(gold[idx], jina_pred[idx], labels=LABELS, zero_division=0)[2]
        for i, label in enumerate(LABELS):
            per_class[label].append(float(jina_cls[i] - hybrid_cls[i]))
    def summarize(values):
        arr = np.asarray(values)
        return {"mean_delta": float(np.mean(arr)), "ci_2_5": float(np.percentile(arr, 2.5)), "ci_97_5": float(np.percentile(arr, 97.5)), "probability_delta_gt_zero": float(np.mean(arr > 0))}
    return {"iterations": 2000, "seed": SEED, "macro_f1": summarize(deltas["macro_f1"]), "balanced_accuracy": summarize(deltas["balanced_accuracy"]), "per_class_f1": {label: summarize(values) for label, values in per_class.items()}, "paired_same_validation_cases": True}


hybrid_records = load_hybrid_predictions_if_valid()
bootstrap_result = None
if hybrid_records is not None:
    bootstrap_result = paired_bootstrap(hybrid_records)
    write_json(OUTPUT_DIR / "paired_bootstrap_vs_hybrid.json", bootstrap_result)
    fig, ax = plt.subplots(figsize=(7, 4))
    mean = bootstrap_result["macro_f1"]["mean_delta"]
    lo = bootstrap_result["macro_f1"]["ci_2_5"]
    hi = bootstrap_result["macro_f1"]["ci_97_5"]
    ax.errorbar([0], [mean], yerr=[[mean - lo], [hi - mean]], fmt="o")
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xticks([0], ["Jina - MiniLM hybrid"])
    ax.set_ylabel("Macro-F1 delta")
    ax.set_title("Paired bootstrap Macro-F1 delta")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "paired_bootstrap_macro_f1_delta.png", dpi=180)
    plt.close(fig)
else:
    print("Skipping paired bootstrap; exact hybrid predictions not proven.")
"""
    manifests_results = """
if bootstrap_result and bootstrap_result["macro_f1"]["ci_2_5"] > 0 and metrics["macro_f1"] > FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"]["macro_f1"]:
    decision = "A. CLEAR REPRESENTATION IMPROVEMENT"
elif metrics["macro_f1"] > FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"]["macro_f1"]:
    decision = "B. PROMISING BUT UNCERTAIN"
elif abs(metrics["macro_f1"] - FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"]["macro_f1"]) <= 0.02 and metrics["per_class"]["developer_setup"]["f1"] > 0:
    decision = "C. CLASS TRADE-OFF"
else:
    decision = "D. NO REPRESENTATION SIGNAL"

representation_manifest = {
    "model_identifier": JINA_MODEL_NAME,
    "model_revision_sha": JINA_MODEL_REVISION_SHA,
    "tokenizer_revision_sha": JINA_MODEL_REVISION_SHA,
    "embedding_dimension": int(train_code_embeddings.shape[1]),
    "max_sequence_length_per_side": JINA_MAX_SEQ_LENGTH,
    "sentence_transformers_version": sentence_transformers_version,
    "transformers_version": transformers.__version__,
    "torch_version": torch.__version__,
    "python_version": sys.version,
    "cuda_device": torch.cuda.get_device_name(0),
    "normalize_embeddings": True,
    "encoder_frozen": True,
    "jina_fit_called": False,
}
write_json(OUTPUT_DIR / "representation_manifest.json", representation_manifest)

training_manifest = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "primary_model_id": PRIMARY_MODEL_ID,
    "current_hybrid_model_id": CURRENT_HYBRID_MODEL_ID,
    "seed": SEED,
    "internal_split_seed": int(internal_split_seed),
    "classifier": {
        "class": "LogisticRegression",
        "C": 1.0,
        "solver": "lbfgs",
        "max_iter": 2000,
        "random_state": 42,
        "class_weight": None,
        "resampling": None,
    },
    "feature_meta": final_result["feature_meta"],
    "v1_export_manifest": manifest,
    "embedding_caches": [train_code_cache, train_docs_cache, validation_code_cache, validation_docs_cache],
    "no_confirmation_access": True,
    "no_controlled_or_synthetic_data": True,
    "no_class_balancing": True,
    "no_general_model_search": True,
}
write_json(OUTPUT_DIR / "training_manifest.json", training_manifest)

results_md = f'''# Jina code-aware frozen hybrid architecture challenge V3

Decision: **{decision}**

## Main result

- Model: `{PRIMARY_MODEL_ID}`
- Frozen encoder: `{JINA_MODEL_NAME}`
- Resolved revision SHA: `{JINA_MODEL_REVISION_SHA}`
- Jina max sequence length per side: **{JINA_MAX_SEQ_LENGTH}**
- Validation Macro-F1: **{metrics["macro_f1"]:.4f}**
- Validation balanced accuracy: **{metrics["balanced_accuracy"]:.4f}**
- developer_setup F1: **{metrics["per_class"]["developer_setup"]["f1"]:.4f}**

## Internal fit diagnostic

- Internal train Macro-F1: **{internal_train_metrics["macro_f1"]:.4f}**
- Internal repository-grouped eval Macro-F1: **{internal_eval_metrics["macro_f1"]:.4f}**
- Gap: **{internal_train_metrics["macro_f1"] - internal_eval_metrics["macro_f1"]:.4f}**

## Frozen comparison

| Model | Macro-F1 | Balanced accuracy | API F1 | Configuration F1 | Developer setup F1 | Model contract F1 |
|---|---:|---:|---:|---:|---:|---:|
| TF-IDF Category V8 | {FROZEN_BASELINES["tfidf_category_v8"]["macro_f1"]:.4f} | {FROZEN_BASELINES["tfidf_category_v8"]["balanced_accuracy"]:.4f} | n/a | n/a | 0.0000 | n/a |
| Frozen MiniLM Hybrid Natural-Only | {FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"]["macro_f1"]:.4f} | {FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"]["balanced_accuracy"]:.4f} | {FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"]["per_class_f1"]["api_reference"]:.4f} | {FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"]["per_class_f1"]["configuration"]:.4f} | 0.0000 | {FROZEN_BASELINES["frozen_minilm_hybrid_natural_only"]["per_class_f1"]["model_contract"]:.4f} |
| CodeBERT Joint 512 | {FROZEN_BASELINES["codebert_joint_512"]["macro_f1"]:.4f} | {FROZEN_BASELINES["codebert_joint_512"]["balanced_accuracy"]:.4f} | n/a | n/a | 0.0000 | n/a |
| ModernBERT Long Context 2048 | {FROZEN_BASELINES["modernbert_long_context_2048"]["macro_f1"]:.4f} | {FROZEN_BASELINES["modernbert_long_context_2048"]["balanced_accuracy"]:.4f} | {FROZEN_BASELINES["modernbert_long_context_2048"]["per_class_f1"]["api_reference"]:.4f} | {FROZEN_BASELINES["modernbert_long_context_2048"]["per_class_f1"]["configuration"]:.4f} | {FROZEN_BASELINES["modernbert_long_context_2048"]["per_class_f1"]["developer_setup"]:.4f} | {FROZEN_BASELINES["modernbert_long_context_2048"]["per_class_f1"]["model_contract"]:.4f} |
| Jina Code-Aware Frozen Hybrid | {metrics["macro_f1"]:.4f} | {metrics["balanced_accuracy"]:.4f} | {metrics["per_class"]["api_reference"]["f1"]:.4f} | {metrics["per_class"]["configuration"]["f1"]:.4f} | {metrics["per_class"]["developer_setup"]["f1"]:.4f} | {metrics["per_class"]["model_contract"]["f1"]:.4f} |

The 322-row split is frozen development validation, not a test set. It is evaluated once after the predeclared full development-train fit.
'''
Path(OUTPUT_DIR / "RESULTS.md").write_text(results_md, encoding="utf-8")
print(results_md)
"""
    return {
        "cells": [
            nb_cell("markdown", title),
            nb_cell("code", deps),
            nb_cell("code", imports),
            nb_cell("code", data_import),
            nb_cell("code", config),
            nb_cell("code", helpers),
            nb_cell("code", audit_load),
            nb_cell("code", model_smoke),
            nb_cell("code", truncation_embeddings),
            nb_cell("code", feature_fit),
            nb_cell("code", diagnostics),
            nb_cell("code", bootstrap_figures),
            nb_cell("code", manifests_results),
        ],
        "metadata": {
            "accelerator": "GPU",
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebook() -> None:
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(json.dumps(make_notebook(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def write_readme(audit: dict[str, Any]) -> None:
    EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    readme = f"""# Stage-2 Architecture Challenge V3: Jina code-aware frozen hybrid

Prepared notebook: `notebooks/category_jina_code_hybrid_architecture_challenge_v3.ipynb`

This is the final planned general representation experiment for the Stage-2
four-class category classifier. It tests one change: replace the frozen MiniLM
semantic encoder in the current natural-only hybrid with frozen code-aware
Jina embeddings from `{JINA_MODEL_NAME}`.

Frozen data reused exactly from Architecture Challenge V1:

- `data/final_v2/architecture_challenge_v1/natural_train_primary_four.jsonl` ({audit['train_rows']} rows)
- `data/final_v2/architecture_challenge_v1/natural_validation_primary_four.jsonl` ({audit['validation_rows']} rows)
- validation case-id SHA256: `{audit['validation_case_ids_sha256']}`

The notebook resolves the exact Hugging Face model revision at runtime, keeps
Jina frozen, uses repository only for grouping/audit, and writes lightweight
outputs to this directory. Large embedding caches under `cache/` are
regenerable and ignored by Git.
"""
    (EXPERIMENT_DIR / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    audit = validate_v1_exports()
    write_current_hybrid_audit(audit)
    write_notebook()
    write_readme(audit)
    print(
        json.dumps(
            {
                "status": "prepared",
                "notebook": str(NOTEBOOK_PATH.relative_to(ROOT)),
                "output_dir": str(EXPERIMENT_DIR.relative_to(ROOT)),
                "audit": str(AUDIT_PATH.relative_to(ROOT)),
                "validation_case_ids_sha256": audit["validation_case_ids_sha256"],
                "created_at": datetime.now(UTC).isoformat(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
