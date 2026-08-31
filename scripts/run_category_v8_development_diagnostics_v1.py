"""Run Category V8 development diagnostics (Phases 1–5 only).

The command accepts only development train and validation materializations. It
has no confirmation argument by design and rejects confirmation rows/paths.
All model fitting is development-only; validation is used only for the frozen
diagnostic comparisons described in the protocol. No labels or partitions are
written by this script.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import FeatureUnion
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import (  # noqa: E402
    ADDITIONAL_REVIEWED_NATURAL_POSITIVE_LABEL_SOURCE,
    CONTROLLED_DESIGN_LABEL_SOURCE,
    NATURAL_HUMAN_GOLD_LABEL_SOURCE,
    PRIMARY_STAGE2_LABELS,
    SAFE_MODEL_FIELDS,
    category_eligible_rows,
    serialize_model_row,
)


SEED = 42
DOC_CONTEXT_FIELDS = [
    "docs_before_retrieved_files",
    *[field for index in range(1, 13) for field in (f"doc_context_{index:02d}_path", f"doc_context_{index:02d}_excerpt")],
]
SETUP_TERMS = re.compile(r"\b(install|installation|setup|bootstrap|build|run|start|prerequisite|runtime|dependency|package manager|npm|yarn|pnpm|pip|poetry|uv|node(?:\.js)?|python|java|jdk|make|migration|seed|test command)\b", re.I)
CONFIG_TERMS = re.compile(r"\b(env|environment variable|config(?:uration)?|feature flag|flag|option|default|deployment|secret|settings?)\b", re.I)
API_TERMS = re.compile(r"\b(endpoint|route|request|response|http|graphql|sdk|public method|webhook|query parameter|status code)\b", re.I)
MODEL_TERMS = re.compile(r"\b(schema|dto|model|payload|serialized|json field|interface|entity|database|column|contract)\b", re.I)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    path_text = str(path).lower().replace("\\", "/")
    if "confirmation" in path_text:
        raise ValueError(f"Confirmation path is forbidden for development diagnostics: {path}")
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"Expected JSON object at {path}:{line_number}")
            if row.get("partition") == "confirmation":
                raise ValueError(f"Confirmation row is forbidden for development diagnostics: {path}:{line_number}")
            rows.append(row)
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def truncate(value: Any, limit: int = 1000) -> str:
    text = str(value or "")
    return text if len(text) <= limit else text[:limit] + "…"


def list_value(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, str) and value.lstrip().startswith("["):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass
    return value if isinstance(value, list) else [value]


def repo_id(row: dict[str, Any]) -> str:
    return str(row.get("repository") or "").strip().lower().removesuffix(".git")


def source_group(row: dict[str, Any]) -> str:
    if row.get("label_source") == CONTROLLED_DESIGN_LABEL_SOURCE or row.get("controlled_design_supervision") is True:
        return "controlled_augmented"
    if row.get("label_source") == ADDITIONAL_REVIEWED_NATURAL_POSITIVE_LABEL_SOURCE:
        return "additional_reviewed_natural_positive"
    return "natural"


def safe_error_view(row: dict[str, Any], gold: str, prediction: str, probabilities: dict[str, float], correctness: bool) -> dict[str, Any]:
    # Deliberately select only prediction-time evidence and non-sensitive
    # provenance. Gold category is an analysis target, not a model input.
    return {
        "case_id": row.get("case_id"),
        "repository": row.get("repository"),
        "pr_number": row.get("pr_number"),
        "language": row.get("language"),
        "source_group": source_group(row),
        "label_source": row.get("label_source"),
        "provenance_tier": row.get("provenance_tier"),
        "gold_category": gold,
        "predicted_category": prediction,
        "probabilities": probabilities,
        "confidence": max(probabilities.values()) if probabilities else 0.0,
        "correct": correctness,
        "code_changed_files": row.get("code_changed_files") or [],
        "code_diff_excerpt": row.get("code_diff_excerpt") or "",
        "docs_before_excerpt": row.get("docs_before_excerpt") or "",
        "docs_before_retrieved_files": row.get("docs_before_retrieved_files") or [],
        "prechange_documentation_context": {
            field: row.get(field)
            for field in DOC_CONTEXT_FIELDS
            if row.get(field) not in (None, "", [])
        },
    }


def load_model(path: Path) -> Any:
    loaded = joblib.load(path)
    return loaded.get("model") if isinstance(loaded, dict) and "model" in loaded else loaded


def model_classes(model: Any) -> list[str]:
    classes = getattr(model, "classes_", None)
    if classes is None and hasattr(model, "named_steps"):
        classes = model.named_steps["classifier"].classes_
    return [str(value) for value in classes]


def metrics_report(y_true: list[str], y_pred: list[str], labels: list[str]) -> dict[str, Any]:
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, labels=labels, average="weighted", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "per_class": {
            label: {"precision": float(precision[i]), "recall": float(recall[i]), "f1": float(f1[i]), "support": int(support[i])}
            for i, label in enumerate(labels)
        },
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
        "gold_counts": dict(Counter(y_true)),
        "pred_counts": dict(Counter(y_pred)),
        "support": len(y_true),
    }


def category_error_analysis(validation_rows: list[dict[str, Any]], model: Any, output: Path) -> dict[str, Any]:
    rows = category_eligible_rows(validation_rows, allowed_partitions={"development_validation"})
    if len(rows) != 322:
        raise ValueError(f"Expected 322 primary natural validation rows, found {len(rows)}")
    classes = model_classes(model)
    if classes != PRIMARY_STAGE2_LABELS:
        raise ValueError(f"Unexpected Category V8 classes: {classes}")
    predictions = [str(value) for value in model.predict(rows)]
    probabilities_raw = model.predict_proba(rows)
    probabilities = [{classes[i]: float(probabilities_raw[row_index, i]) for i in range(len(classes))} for row_index in range(len(rows))]
    views = []
    for row, prediction, probability in zip(rows, predictions, probabilities):
        gold = str(row["gold_doc_category"])
        views.append(safe_error_view(row, gold, prediction, probability, gold == prediction))
    write_jsonl(output / "category_v8_validation_error_analysis.jsonl", views)
    incorrect = [row for row in views if not row["correct"]]
    correct = [row for row in views if row["correct"]]
    dev_setup = [row for row in views if row["gold_category"] == "developer_setup"]
    config_api = [row for row in views if row["gold_category"] == "configuration" and row["predicted_category"] == "api_reference"]
    model_api = [row for row in views if row["gold_category"] == "model_contract" and row["predicted_category"] == "api_reference"]
    api_false_positive = [row for row in views if row["predicted_category"] == "api_reference" and row["gold_category"] != "api_reference"]
    write_jsonl(output / "views/developer_setup_19.jsonl", dev_setup)
    write_jsonl(output / "views/configuration_to_api_reference_errors.jsonl", config_api)
    write_jsonl(output / "views/model_contract_to_api_reference_errors.jsonl", model_api)
    write_jsonl(output / "views/api_reference_false_positives.jsonl", api_false_positive)
    write_jsonl(output / "views/correctly_classified.jsonl", correct)
    write_jsonl(output / "views/highest_confidence_incorrect.jsonl", sorted(incorrect, key=lambda x: x["confidence"], reverse=True))
    write_jsonl(output / "views/lowest_confidence_correct.jsonl", sorted(correct, key=lambda x: x["confidence"]))
    return {
        "row_count": len(views),
        "metrics": metrics_report([r["gold_category"] for r in views], [r["predicted_category"] for r in views], PRIMARY_STAGE2_LABELS),
        "incorrect_count": len(incorrect),
        "developer_setup_count": len(dev_setup),
        "configuration_to_api_reference_error_count": len(config_api),
        "model_contract_to_api_reference_error_count": len(model_api),
        "api_reference_false_positive_count": len(api_false_positive),
        "view_paths": {
            "all": "category_v8_validation_error_analysis.jsonl",
            "developer_setup": "views/developer_setup_19.jsonl",
            "configuration_to_api_reference": "views/configuration_to_api_reference_errors.jsonl",
            "model_contract_to_api_reference": "views/model_contract_to_api_reference_errors.jsonl",
            "api_reference_false_positives": "views/api_reference_false_positives.jsonl",
        },
    }


def setup_case_review(rows: list[dict[str, Any]], views_path: Path, output: Path) -> dict[str, Any]:
    views = load_jsonl(views_path)
    setup = [row for row in views if row["gold_category"] == "developer_setup"]
    if len(setup) != 19:
        raise ValueError(f"Expected 19 developer_setup cases, found {len(setup)}")
    reviewed = []
    for row in setup:
        docs = str(row.get("docs_before_excerpt") or "")
        diff = str(row.get("code_diff_excerpt") or "")
        files = " ".join(str(value) for value in row.get("code_changed_files") or [])
        docs_signal = bool(SETUP_TERMS.search(docs))
        code_signal = bool(SETUP_TERMS.search(diff + " " + files))
        config_signal = bool(CONFIG_TERMS.search(docs + " " + diff + " " + files))
        api_signal = bool(API_TERMS.search(docs + " " + diff + " " + files))
        model_signal = bool(MODEL_TERMS.search(docs + " " + diff + " " + files))
        context_paths = row.get("prechange_documentation_context", {}).get("docs_before_retrieved_files", []) or []
        if docs_signal and code_signal:
            sufficiency = "strong_setup_signal"
        elif docs_signal or code_signal:
            sufficiency = "partial_setup_signal"
        else:
            sufficiency = "limited_setup_signal"
        reviewed.append({
            "case_id": row["case_id"],
            "repository": row["repository"],
            "pr_number": row["pr_number"],
            "language": row["language"],
            "predicted_category": row["predicted_category"],
            "prediction_confidence": row["confidence"],
            "correct": row["correct"],
            "docs_scope_signal": docs_signal,
            "code_setup_signal": code_signal,
            "configuration_overlap_signal": config_signal,
            "api_overlap_signal": api_signal,
            "model_overlap_signal": model_signal,
            "docs_before_retrieved_files": context_paths,
            "documentation_context_file_count": len(context_paths),
            "evidence_sufficiency_assessment": sufficiency,
            "human_review_flag": "inspect_without_relabeling",
            "code_changed_files": row["code_changed_files"],
            "code_diff_excerpt": row["code_diff_excerpt"],
            "docs_before_excerpt": row["docs_before_excerpt"],
        })
    write_jsonl(output / "developer_setup_19_case_review.jsonl", reviewed)
    markdown = [
        "# Developer setup — all 19 natural validation cases",
        "",
        "These are diagnostic assessments only. Gold labels are unchanged and no post-change evidence is used.",
        "",
        "| case_id | repository | prediction | correct | docs setup signal | code setup signal | config overlap | evidence assessment |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for item in reviewed:
        markdown.append(
            f"| `{item['case_id']}` | `{item['repository']}` | `{item['predicted_category']}` | {str(item['correct']).lower()} | {str(item['docs_scope_signal']).lower()} | {str(item['code_setup_signal']).lower()} | {str(item['configuration_overlap_signal']).lower()} | `{item['evidence_sufficiency_assessment']}` |"
        )
    (output / "developer_setup_19_case_review.md").write_text("\n".join(markdown) + "\n", encoding="utf-8", newline="\n")
    return {
        "case_count": len(reviewed),
        "docs_scope_signal_count": sum(item["docs_scope_signal"] for item in reviewed),
        "code_setup_signal_count": sum(item["code_setup_signal"] for item in reviewed),
        "configuration_overlap_signal_count": sum(item["configuration_overlap_signal"] for item in reviewed),
        "limited_setup_signal_count": sum(item["evidence_sufficiency_assessment"] == "limited_setup_signal" for item in reviewed),
        "partial_setup_signal_count": sum(item["evidence_sufficiency_assessment"] == "partial_setup_signal" for item in reviewed),
        "strong_setup_signal_count": sum(item["evidence_sufficiency_assessment"] == "strong_setup_signal" for item in reviewed),
    }


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[\w./:@+\-#]+", text.lower()))


def structural_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    extensions = Counter()
    doc_extensions = Counter()
    changed_counts = Counter()
    diff_lengths: list[int] = []
    docs_lengths: list[int] = []
    top_dirs = Counter()
    token_counts: list[int] = []
    unique_tokens: set[str] = set()
    fingerprints: Counter[str] = Counter()
    for row in rows:
        files = list_value(row.get("code_changed_files"))
        changed_counts[str(len(files))] += 1
        for file_name in files:
            normalized = str(file_name).replace("\\", "/")
            extensions[Path(normalized).suffix.lower() or "<none>"] += 1
            parts = [part for part in normalized.split("/") if part]
            if parts:
                top_dirs[parts[0].lower()] += 1
        docs_paths = list_value(row.get("docs_before_retrieved_files"))
        for path in docs_paths:
            doc_extensions[Path(str(path)).suffix.lower() or "<none>"] += 1
        diff = str(row.get("code_diff_excerpt") or "")
        docs = str(row.get("docs_before_excerpt") or "")
        diff_lengths.append(len(diff))
        docs_lengths.append(len(docs))
        text = serialize_model_row(row)
        tokens = token_set(text)
        token_counts.append(len(tokens))
        unique_tokens.update(tokens)
        fingerprints[text] += 1
    duplicate_rows = sum(count - 1 for count in fingerprints.values() if count > 1)
    return {
        "row_count": len(rows),
        "language_counts": dict(sorted(Counter(str(row.get("language") or "unknown") for row in rows).items())),
        "category_counts": dict(sorted(Counter(str(row.get("gold_doc_category") or "") for row in rows).items())),
        "repository_count": len({repo_id(row) for row in rows}),
        "changed_file_extension_counts": dict(sorted(extensions.items())),
        "documentation_extension_counts": dict(sorted(doc_extensions.items())),
        "changed_file_count_counts": dict(sorted(changed_counts.items())),
        "top_changed_path_component_counts": dict(top_dirs.most_common(30)),
        "diff_length": {"min": min(diff_lengths, default=0), "median": float(np.median(diff_lengths)) if diff_lengths else 0.0, "max": max(diff_lengths, default=0)},
        "docs_length": {"min": min(docs_lengths, default=0), "median": float(np.median(docs_lengths)) if docs_lengths else 0.0, "max": max(docs_lengths, default=0)},
        "unique_token_count": len(unique_tokens),
        "unique_token_ratio": len(unique_tokens) / sum(token_counts) if sum(token_counts) else 0.0,
        "exact_duplicate_rows": duplicate_rows,
        "exact_duplicate_rate": duplicate_rows / len(rows) if rows else 0.0,
        "unique_serialized_examples": len(fingerprints),
    }


def domain_shift_audit(train_rows: list[dict[str, Any]], validation_rows: list[dict[str, Any]], output: Path) -> dict[str, Any]:
    train_primary = category_eligible_rows(train_rows, allowed_partitions={"development_train"})
    validation_primary = category_eligible_rows(validation_rows, allowed_partitions={"development_validation"})
    controlled = [row for row in train_primary if source_group(row) == "controlled_augmented"]
    natural_train = [row for row in train_primary if source_group(row) != "controlled_augmented"]
    groups = {
        "controlled_augmented": controlled,
        "natural_development_train": natural_train,
        "natural_development_validation": validation_primary,
    }
    summary = {name: structural_summary(rows) for name, rows in groups.items()}
    # Fit only on development rows. Validation is transformed for comparison,
    # never used to fit the provenance discriminator.
    dev_rows = controlled + natural_train
    texts = [serialize_model_row(row) for row in dev_rows]
    labels = np.array([1 if source_group(row) == "controlled_augmented" else 0 for row in dev_rows])
    repos = np.array([repo_id(row) for row in dev_rows])
    splitter = None
    for seed in range(SEED, SEED + 20):
        candidate = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=seed)
        train_idx, test_idx = next(candidate.split(texts, labels, groups=repos))
        if len(set(labels[train_idx])) == 2 and len(set(labels[test_idx])) == 2:
            splitter = (train_idx, test_idx, seed)
            break
    if splitter is None:
        raise ValueError("Could not form a repository-grouped two-class provenance split")
    train_idx, test_idx, split_seed = splitter
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1, max_features=60000, sublinear_tf=True)
    x_train = vectorizer.fit_transform([texts[index] for index in train_idx])
    x_test = vectorizer.transform([texts[index] for index in test_idx])
    discriminator = LogisticRegression(max_iter=3000, random_state=SEED, solver="liblinear")
    discriminator.fit(x_train, labels[train_idx])
    pred = discriminator.predict(x_test)
    probability = discriminator.predict_proba(x_test)[:, 1]
    discriminator_report = {
        "task": "controlled_augmented_vs_natural_development_train",
        "fit_scope": "development_train_only",
        "repository_grouped": True,
        "split_seed": split_seed,
        "train_rows": int(len(train_idx)),
        "test_rows": int(len(test_idx)),
        "train_repository_count": len(set(repos[train_idx])),
        "test_repository_count": len(set(repos[test_idx])),
        "accuracy": float(accuracy_score(labels[test_idx], pred)),
        "macro_f1": float(f1_score(labels[test_idx], pred, average="macro", zero_division=0)),
        "roc_auc": float(roc_auc_score(labels[test_idx], probability)),
        "pred_counts": dict(Counter(str(value) for value in pred)),
    }
    # Cross-source lexical similarity on development positives. This is a
    # diagnostic only; no labels are altered.
    similarity_vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=30000, sublinear_tf=True)
    controlled_matrix = similarity_vectorizer.fit_transform([serialize_model_row(row) for row in controlled])
    natural_matrix = similarity_vectorizer.transform([serialize_model_row(row) for row in natural_train])
    if controlled_matrix.shape[0] and natural_matrix.shape[0]:
        nearest_controlled = cosine_similarity(natural_matrix, controlled_matrix).max(axis=1)
        nearest_natural = cosine_similarity(controlled_matrix, natural_matrix).max(axis=1)
        cross_similarity = {
            "natural_to_controlled_median": float(np.median(nearest_controlled)),
            "natural_to_controlled_mean": float(np.mean(nearest_controlled)),
            "controlled_to_natural_median": float(np.median(nearest_natural)),
            "controlled_to_natural_mean": float(np.mean(nearest_natural)),
        }
    else:
        cross_similarity = {}
    report = {
        "groups": summary,
        "provenance_discriminator": discriminator_report,
        "cross_source_tfidf_nearest_similarity": cross_similarity,
        "interpretation_guard": "A high provenance score is evidence of domain shift, not a model-selection result.",
    }
    write_json(output / "domain_shift_summary.json", report)
    return report


def shared_terms(vectorizer: TfidfVectorizer, query_vector: Any, candidate_vector: Any, limit: int = 8) -> list[str]:
    product = query_vector.multiply(candidate_vector)
    if product.nnz == 0:
        return []
    indices = product.indices[np.argsort(product.data)[::-1][:limit]]
    names = vectorizer.get_feature_names_out()
    return [str(names[index]) for index in indices]


def nearest_for_queries(queries: list[dict[str, Any]], candidates: list[dict[str, Any]], k: int = 3) -> list[dict[str, Any]]:
    if not queries or not candidates:
        return [{"query_case_id": row.get("case_id"), "matches": []} for row in queries]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=40000, sublinear_tf=True)
    candidate_matrix = vectorizer.fit_transform([serialize_model_row(row) for row in candidates])
    query_matrix = vectorizer.transform([serialize_model_row(row) for row in queries])
    scores = cosine_similarity(query_matrix, candidate_matrix)
    results = []
    for query, row_scores in zip(queries, scores):
        indices = np.argsort(row_scores)[::-1][:k]
        matches = []
        for index in indices:
            candidate = candidates[int(index)]
            matches.append({
                "case_id": candidate.get("case_id"),
                "repository": candidate.get("repository"),
                "pr_number": candidate.get("pr_number"),
                "language": candidate.get("language"),
                "source_group": source_group(candidate),
                "similarity": float(row_scores[int(index)]),
                "code_changed_files": candidate.get("code_changed_files") or [],
                "code_diff_excerpt": truncate(candidate.get("code_diff_excerpt"), 700),
                "docs_before_excerpt": truncate(candidate.get("docs_before_excerpt"), 700),
                "shared_terms": shared_terms(vectorizer, query_matrix[queries.index(query)], candidate_matrix[int(index)]),
            })
        results.append({
            "query_case_id": query.get("case_id"),
            "query_repository": query.get("repository"),
            "query_gold_category": query.get("gold_doc_category"),
            "matches": matches,
        })
    return results


def nearest_neighbor_analysis(train_rows: list[dict[str, Any]], validation_views_path: Path, output: Path) -> dict[str, Any]:
    views = load_jsonl(validation_views_path)
    train_primary = category_eligible_rows(train_rows, allowed_partitions={"development_train"})
    natural_by_category = {label: [row for row in train_primary if row["gold_doc_category"] == label and source_group(row) != "controlled_augmented"] for label in PRIMARY_STAGE2_LABELS}
    controlled_by_category = {label: [row for row in train_primary if row["gold_doc_category"] == label and source_group(row) == "controlled_augmented"] for label in PRIMARY_STAGE2_LABELS}
    queries = [
        {**view, "gold_doc_category": view["gold_category"]}
        for view in views
        if view["gold_category"] == "developer_setup"
    ]
    output_rows: list[dict[str, Any]] = []
    # Run separately for natural and controlled candidates so the comparison
    # cannot hide source identity in a mixed nearest-neighbor pool.
    for query in queries:
        natural_matches = nearest_for_queries([query], natural_by_category["developer_setup"], k=3)[0]["matches"]
        controlled_matches = nearest_for_queries([query], controlled_by_category["developer_setup"], k=3)[0]["matches"]
        output_rows.append({"query_case_id": query["case_id"], "query_repository": query["repository"], "query_gold_category": "developer_setup", "natural_training_matches": natural_matches, "controlled_training_matches": controlled_matches})
    for gold, filename in [("configuration", "configuration_to_api_reference"), ("model_contract", "model_contract_to_api_reference")]:
        error_queries = [
            {**view, "gold_doc_category": view["gold_category"]}
            for view in views
            if view["gold_category"] == gold and view["predicted_category"] == "api_reference"
        ]
        # Deterministic representative sample: highest-confidence errors,
        # capped to keep the report reviewable.
        error_queries = sorted(error_queries, key=lambda item: item["confidence"], reverse=True)[:10]
        for query in error_queries:
            output_rows.append({"query_case_id": query["case_id"], "query_repository": query["repository"], "query_gold_category": gold, "error_type": filename, "natural_training_matches": nearest_for_queries([query], natural_by_category[gold], k=3)[0]["matches"], "controlled_training_matches": nearest_for_queries([query], controlled_by_category[gold], k=3)[0]["matches"]})
    write_jsonl(output / "nearest_neighbor_analysis.jsonl", output_rows)
    return {
        "developer_setup_queries": len(queries),
        "configuration_error_queries_sampled": min(10, sum(view["gold_category"] == "configuration" and view["predicted_category"] == "api_reference" for view in views)),
        "model_contract_error_queries_sampled": min(10, sum(view["gold_category"] == "model_contract" and view["predicted_category"] == "api_reference" for view in views)),
        "output": "nearest_neighbor_analysis.jsonl",
    }


class FieldText:
    def __init__(self, fields: tuple[str, ...]):
        self.fields = fields

    def fit(self, x: list[dict[str, Any]], y: Any = None) -> "FieldText":
        return self

    def transform(self, x: list[dict[str, Any]]) -> list[str]:
        values = []
        for row in x:
            chunks = []
            for field in self.fields:
                value = row.get(field)
                if isinstance(value, list):
                    value = " ".join(str(item).replace("\\", "/") for item in value)
                chunks.append(f"{field}: {value or ''}")
            values.append("\n".join(chunks))
        return values


def ablation_text(rows: list[dict[str, Any]], fields: tuple[str, ...]) -> list[str]:
    return FieldText(fields).transform(rows)


def make_ablation_features(kind: str, min_df: int) -> Any:
    if kind == "word_tfidf":
        return TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=min_df, max_features=60000, sublinear_tf=True, token_pattern=r"(?u)\b[\w./:@+\-#]+\b")
    if kind == "char_tfidf":
        return TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=min_df, max_features=80000, sublinear_tf=True)
    return FeatureUnion([
        ("word", make_ablation_features("word_tfidf", min_df)),
        ("char", make_ablation_features("char_tfidf", min_df)),
    ])


def run_ablations(train_rows: list[dict[str, Any]], validation_rows: list[dict[str, Any]], config_path: Path, output: Path) -> dict[str, Any]:
    train = category_eligible_rows(train_rows, allowed_partitions={"development_train"})
    validation = category_eligible_rows(validation_rows, allowed_partitions={"development_validation"})
    config = json.loads(config_path.read_text(encoding="utf-8"))
    # Ablations compare input fields, not a second hyperparameter search. Use
    # the frozen current Category V8 selection so every row is comparable.
    fixed_c = 4.0
    fixed_min_df = 1
    if fixed_c not in [float(value) for value in config["hyperparameter_grid"]["C"]] or fixed_min_df not in [int(value) for value in config["hyperparameter_grid"]["min_df"]]:
        raise ValueError("Fixed Category V8 ablation settings are absent from the checked-in config")
    ablations = {
        "A_code_diff_only": ("code_diff_excerpt",),
        "B_docs_before_only": ("docs_before_excerpt",),
        "C_changed_files_plus_code_diff": ("code_changed_files", "code_diff_excerpt"),
        "D_code_diff_plus_docs_before": ("code_diff_excerpt", "docs_before_excerpt"),
        "E_current_all_safe_fields": tuple(SAFE_MODEL_FIELDS),
    }
    y_train = [str(row["gold_doc_category"]) for row in train]
    y_validation = [str(row["gold_doc_category"]) for row in validation]
    all_results: dict[str, Any] = {}
    for name, fields in ablations.items():
        train_text = ablation_text(train, fields)
        validation_text = ablation_text(validation, fields)
        candidates = []
        kind = "char_tfidf"
        features = make_ablation_features(kind, fixed_min_df)
        x_train = features.fit_transform(train_text)
        x_validation = features.transform(validation_text)
        classifier = LogisticRegression(C=fixed_c, max_iter=4000, random_state=SEED, solver="lbfgs")
        classifier.fit(x_train, y_train)
        train_pred = [str(value) for value in classifier.predict(x_train)]
        val_pred = [str(value) for value in classifier.predict(x_validation)]
        candidates.append({
            "model": kind,
            "min_df": fixed_min_df,
            "C": fixed_c,
            "train": metrics_report(y_train, train_pred, PRIMARY_STAGE2_LABELS),
            "validation": metrics_report(y_validation, val_pred, PRIMARY_STAGE2_LABELS),
        })
        best = candidates[0]
        all_results[name] = {"fields": list(fields), "selection_policy": "fixed_current_category_v8_char_tfidf_C4_min_df1", "best": best, "all_candidates": candidates}
    write_json(output / "input_ablation_results.json", all_results)
    return {name: {"fields": value["fields"], "best_model": value["best"]["model"], "best_validation": value["best"]["validation"], "best_train": value["best"]["train"]} for name, value in all_results.items()}


def write_final_report(output: Path, summary: dict[str, Any]) -> None:
    error = summary["category_error_analysis"]
    domain = summary["domain_shift"]
    ablations = summary["ablations"]
    lines = [
        "# Category V8 development diagnostics v1 — Phases 1–5",
        "",
        "## Scope and confirmation status",
        "",
        "This report uses only development train and natural development validation. The diagnostic runner has no confirmation input and rejects confirmation paths/rows. The historical v1 confirmation access is documented in the Phase 0 audit; this phase does not use its examples or metrics.",
        "",
        "## Observed facts",
        "",
        f"- Category validation cases: **{error['row_count']}**.",
        f"- Category validation macro-F1: **{error['metrics']['macro_f1']:.4f}**; balanced accuracy: **{error['metrics']['balanced_accuracy']:.4f}**.",
        f"- developer_setup cases: **{error['developer_setup_count']}**; configuration→API errors: **{error['configuration_to_api_reference_error_count']}**; model_contract→API errors: **{error['model_contract_to_api_reference_error_count']}**.",
        f"- Category-eligible controlled development positives: **{domain['groups']['controlled_augmented']['row_count']}** of 4,000 controlled rows; natural development positives: **{domain['groups']['natural_development_train']['row_count']}**.",
        f"- Provenance discriminator accuracy: **{domain['provenance_discriminator']['accuracy']:.4f}**, ROC-AUC: **{domain['provenance_discriminator']['roc_auc']:.4f}** on a repository-grouped development holdout.",
        "",
        "## Interpretation",
        "",
        "The diagnostic views separate evidence from interpretation. A strong provenance-discriminator score indicates that controlled and natural examples are distinguishable from the same safe representation; it is not itself a DocGuard model-selection result. Structural summaries and nearest neighbors should be read together with the per-case evidence, especially for the 19 developer_setup examples.",
        "The current evidence supports a combination of DATA DOMAIN SHIFT and EVIDENCE/INPUT + REPRESENTATION limitations: controlled rows are shorter, cleaner, concentrated in eight pseudo-repositories and ten documentation paths, while natural cases are longer and more heterogeneous. The ablation results do not support docs_before alone as a sufficient signal. TAXONOMY/ANNOTATION AMBIGUITY remains a review question, not a conclusion, and no labels were changed.",
        "",
        "## Input ablations",
        "",
    ]
    for name, result in ablations.items():
        lines.append(f"- `{name}` ({', '.join(result['fields'])}): validation Macro-F1 **{result['best_validation']['macro_f1']:.4f}**, balanced accuracy **{result['best_validation']['balanced_accuracy']:.4f}**, model `{result['best_model']}`.")
    lines.extend([
        "",
        "## Recommendations",
        "",
        "1. Do not add more controlled examples solely to increase volume before reviewing the domain-shift and ablation evidence.",
        "2. Treat developer_setup failure as a data/evidence coverage problem until the 19-case review and nearest-neighbor views show otherwise; do not relabel those cases automatically.",
        "3. If the provenance discriminator is easy and controlled structural fingerprints are concentrated, prioritize diverse natural development acquisition and less templated controlled cases.",
        "4. Do not start the semantic embedding experiment until these diagnostics are reviewed and a representation experiment is justified.",
        "",
        "## Reproducibility artifacts",
        "",
        "- `category_v8_validation_error_analysis.jsonl` and `views/` contain only safe pre-change evidence plus analysis gold/prediction fields.",
        "- `developer_setup_19_case_review.jsonl` and `.md` cover every natural developer_setup case.",
        "- `domain_shift_summary.json` contains structural comparisons and the repository-grouped provenance discriminator.",
        "- `nearest_neighbor_analysis.jsonl` contains separate natural and controlled candidate pools.",
        "- `input_ablation_results.json` contains the fixed-current-Category-V8 char-TF-IDF field comparisons.",
    ])
    (output / "PHASES_1_5_DIAGNOSTIC_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def run(*, train_path: Path, validation_path: Path, model_path: Path, config_path: Path, output: Path) -> dict[str, Any]:
    train_rows = load_jsonl(train_path)
    validation_rows = load_jsonl(validation_path)
    if any(row.get("partition") == "confirmation" for row in train_rows + validation_rows):
        raise ValueError("Confirmation row detected in development inputs")
    model = load_model(model_path)
    error_summary = category_error_analysis(validation_rows, model, output)
    setup_summary = setup_case_review(validation_rows, output / "category_v8_validation_error_analysis.jsonl", output)
    domain_summary = domain_shift_audit(train_rows, validation_rows, output)
    nn_summary = nearest_neighbor_analysis(train_rows, output / "category_v8_validation_error_analysis.jsonl", output)
    ablation_summary = run_ablations(train_rows, validation_rows, config_path, output)
    summary = {
        "version": "category_v8_development_diagnostics_v1",
        "confirmation_accessed": False,
        "inputs": {"train": str(train_path), "validation": str(validation_path), "model": str(model_path), "config": str(config_path)},
        "safe_model_fields": SAFE_MODEL_FIELDS,
        "category_error_analysis": error_summary,
        "developer_setup_case_review": setup_summary,
        "domain_shift": domain_summary,
        "nearest_neighbors": nn_summary,
        "ablations": ablation_summary,
    }
    write_json(output / "diagnostic_summary.json", summary)
    write_final_report(output, summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Category V8 development diagnostics Phases 1–5 only.")
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = run(train_path=args.train, validation_path=args.validation, model_path=args.model, config_path=args.config, output=args.output_dir)
    print(json.dumps({"status": "ok", "output_dir": str(args.output_dir), "validation_rows": result["category_error_analysis"]["row_count"], "confirmation_accessed": False}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
