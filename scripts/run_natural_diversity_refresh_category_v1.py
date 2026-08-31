"""Retrain the fixed natural-only hybrid Category model after expansion review.

This is deliberately not a model search.  It keeps the previously selected
hybrid representation and multinomial logistic regression, adds only approved
primary-four expansion-train examples, and evaluates on the unchanged old
development validation.  The frozen refresh partition is evaluated only when
it contains primary-four positives.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import joblib
import matplotlib
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scripts.run_category_semantic_development_v1 import (
    LABELS,
    MODEL_LICENSE,
    MODEL_NAME,
    MODEL_REVISION,
    SEED,
    bootstrap_delta,
    build_code_text,
    build_docs_text,
    classifier,
    encode_texts_cached,
    labels_for,
    lexical_relational_scalars,
    load_development_jsonl,
    metric_bundle,
    probabilities,
    reject_confirmation_path,
    relational_semantic_features,
    select_training_rows,
    sha256_path,
    source_distribution,
    stable_json_hash,
    validate_validation_rows,
    write_json,
    write_jsonl,
)


MODEL_ID = "hybrid__natural_only__multinomial_logreg"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    reject_confirmation_path(path)
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: row is not an object")
            if str(row.get("partition") or "").lower() == "confirmation":
                raise ValueError(f"Confirmation row is forbidden: {row.get('case_id')}")
            rows.append(row)
    return rows


def primary_expansion(rows: list[dict[str, Any]], partition: str) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for row in rows:
        if row.get("partition") != partition:
            raise ValueError(f"{row.get('case_id')}: expected partition {partition}")
        if row.get("review_status") != "approved" or row.get("independent_human_reviewed") is not True:
            continue
        if row.get("gold_docs_update_required") is True and str(row.get("gold_doc_category")) in LABELS:
            selected.append(row)
    return selected


def repo_pr_key(row: dict[str, Any]) -> tuple[str, int]:
    return str(row.get("repository") or "").strip().lower(), int(row.get("pr_number") or 0)


def audit_membership(
    old_train: list[dict[str, Any]],
    old_validation: list[dict[str, Any]],
    expansion_train: list[dict[str, Any]],
    refresh_all: list[dict[str, Any]],
) -> dict[str, Any]:
    old_train_repos = {repo_pr_key(row)[0] for row in old_train}
    old_validation_repos = {repo_pr_key(row)[0] for row in old_validation}
    expansion_train_repos = {repo_pr_key(row)[0] for row in expansion_train}
    refresh_repos = {repo_pr_key(row)[0] for row in refresh_all}
    all_rows = old_train + old_validation + expansion_train + refresh_all
    keys = [repo_pr_key(row) for row in all_rows]
    overlaps = {
        "expansion_train_vs_old_train": sorted(expansion_train_repos & old_train_repos),
        "expansion_train_vs_old_validation": sorted(expansion_train_repos & old_validation_repos),
        "refresh_vs_old_train": sorted(refresh_repos & old_train_repos),
        "refresh_vs_old_validation": sorted(refresh_repos & old_validation_repos),
        "expansion_train_vs_refresh": sorted(expansion_train_repos & refresh_repos),
    }
    errors = [f"{name}: {values}" for name, values in overlaps.items() if values]
    if len(keys) != len(set(keys)):
        errors.append("duplicate repository/PR keys across compared datasets")
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "repository_overlaps": overlaps,
        "duplicate_repository_pr_count": len(keys) - len(set(keys)),
        "confirmation_accessed": False,
    }


def fit_hybrid(
    train_rows: list[dict[str, Any]],
    evaluation_rows: list[dict[str, Any]],
    *,
    encoder: Any,
    embedding_cache_dir: Path,
) -> tuple[Any, dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    all_rows = train_rows + evaluation_rows
    code_texts = [build_code_text(row) for row in all_rows]
    docs_texts = [build_docs_text(row) for row in all_rows]
    code_embeddings, code_cache = encode_texts_cached(
        code_texts, side="code", model=encoder, cache_dir=embedding_cache_dir
    )
    docs_embeddings, docs_cache = encode_texts_cached(
        docs_texts, side="docs", model=encoder, cache_dir=embedding_cache_dir
    )
    semantic = relational_semantic_features(code_embeddings, docs_embeddings)
    train_count = len(train_rows)

    code_vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=20_000,
        sublinear_tf=True,
        dtype=np.float32,
    )
    code_train = code_vectorizer.fit_transform(code_texts[:train_count])
    code_eval = code_vectorizer.transform(code_texts[train_count:])
    train_features = sparse.hstack(
        [
            code_train,
            sparse.csr_matrix(semantic[:train_count]),
            sparse.csr_matrix(lexical_relational_scalars(train_rows)),
        ],
        format="csr",
    )
    eval_features = sparse.hstack(
        [
            code_eval,
            sparse.csr_matrix(semantic[train_count:]),
            sparse.csr_matrix(lexical_relational_scalars(evaluation_rows)),
        ],
        format="csr",
    )
    y_train = labels_for(train_rows)
    y_eval = labels_for(evaluation_rows)
    model = classifier("multinomial_logreg")
    model.fit(train_features, y_train)
    train_pred = model.predict(train_features)
    eval_pred = model.predict(eval_features)
    eval_prob = probabilities(model, eval_features)
    metrics = {
        "train": metric_bundle(y_train, train_pred),
        "evaluation": metric_bundle(y_eval, eval_pred),
    }
    predictions: list[dict[str, Any]] = []
    for row, gold, predicted, scores in zip(evaluation_rows, y_eval, eval_pred, eval_prob):
        predictions.append({
            "case_id": str(row["case_id"]),
            "gold": str(gold),
            "prediction": str(predicted),
            "correct": str(gold) == str(predicted),
            "probabilities": {label: float(scores[index]) for index, label in enumerate(LABELS)},
        })
    bundle = {
        "model": model,
        "code_vectorizer": code_vectorizer,
        "labels": LABELS,
        "representation": "code_char_tfidf_plus_relational_minilm_plus_lexical_scalars",
        "embedding_model_name": MODEL_NAME,
        "embedding_model_revision": MODEL_REVISION,
    }
    return bundle, metrics, predictions, code_cache, docs_cache


def load_prior_predictions(path: Path, case_ids: list[str]) -> np.ndarray:
    reject_confirmation_path(path)
    mapping: dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("model") == MODEL_ID:
                mapping[str(row["case_id"])] = str(row["prediction"])
    missing = sorted(set(case_ids) - set(mapping))
    if missing:
        raise ValueError(f"Prior predictions missing {len(missing)} unchanged validation cases")
    return np.asarray([mapping[case_id] for case_id in case_ids])


def plot_confusion(metrics: dict[str, Any], output: Path) -> None:
    matrix = np.asarray(metrics["normalized_confusion_matrix"], dtype=float)
    plt.figure(figsize=(7.5, 6.5))
    plt.imshow(matrix, vmin=0, vmax=1, cmap="Blues")
    plt.colorbar(label="Row-normalized proportion")
    plt.xticks(range(len(LABELS)), LABELS, rotation=25, ha="right")
    plt.yticks(range(len(LABELS)), LABELS)
    for i in range(len(LABELS)):
        for j in range(len(LABELS)):
            plt.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="white" if matrix[i, j] > 0.5 else "black")
    plt.xlabel("Predicted")
    plt.ylabel("Gold")
    plt.title("Refreshed natural-only hybrid Category model")
    plt.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=180)
    plt.close()


def plot_before_after(prior: dict[str, Any], current: dict[str, Any], output: Path) -> None:
    x = np.arange(len(LABELS))
    width = 0.36
    before = [prior["per_class"][label]["f1"] for label in LABELS]
    after = [current["per_class"][label]["f1"] for label in LABELS]
    plt.figure(figsize=(10, 6))
    plt.bar(x - width / 2, before, width, label="Before expansion")
    plt.bar(x + width / 2, after, width, label="After expansion")
    plt.xticks(x, LABELS, rotation=18)
    plt.ylabel("F1 on unchanged development validation")
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=180)
    plt.close()


def run(args: argparse.Namespace) -> dict[str, Any]:
    for path in (
        args.old_train,
        args.old_validation,
        args.expansion_train,
        args.refresh_validation,
        args.prior_predictions,
    ):
        reject_confirmation_path(path)
    old_train_all = load_development_jsonl(args.old_train, "development_train")
    old_validation_all = load_development_jsonl(args.old_validation, "development_validation")
    old_train = select_training_rows(old_train_all, controlled_enabled=False)
    old_validation = validate_validation_rows(old_validation_all)
    expansion_train_all = load_jsonl(args.expansion_train)
    refresh_all = load_jsonl(args.refresh_validation)
    expansion_train = primary_expansion(expansion_train_all, "development_train")
    refresh_primary = primary_expansion(refresh_all, "refresh_validation")
    audit = audit_membership(old_train_all, old_validation_all, expansion_train_all, refresh_all)
    if audit["errors"]:
        raise ValueError("Membership audit failed: " + "; ".join(audit["errors"]))
    combined_train = old_train + expansion_train

    from sentence_transformers import SentenceTransformer

    started = time.perf_counter()
    encoder = SentenceTransformer(
        MODEL_NAME,
        revision=MODEL_REVISION,
        cache_folder=str(args.model_cache_dir),
        device="cpu",
    )
    bundle, metrics, predictions, code_cache, docs_cache = fit_hybrid(
        combined_train,
        old_validation,
        encoder=encoder,
        embedding_cache_dir=args.embedding_cache_dir,
    )
    old_ids = [str(row["case_id"]) for row in old_validation]
    prior_pred = load_prior_predictions(args.prior_predictions, old_ids)
    current_pred = np.asarray([row["prediction"] for row in predictions])
    gold = labels_for(old_validation)
    prior_metrics = metric_bundle(gold, prior_pred)
    comparison = {
        "prior_model": MODEL_ID,
        "refreshed_model": f"{MODEL_ID}__natural_diversity_expansion_v1",
        "same_unchanged_validation_membership": True,
        "validation_case_ids_sha256": stable_json_hash(old_ids),
        "prior": prior_metrics,
        "refreshed": metrics["evaluation"],
        "delta": {
            "macro_f1": metrics["evaluation"]["macro_f1"] - prior_metrics["macro_f1"],
            "balanced_accuracy": metrics["evaluation"]["balanced_accuracy"] - prior_metrics["balanced_accuracy"],
            "per_class_f1": {
                label: metrics["evaluation"]["per_class"][label]["f1"] - prior_metrics["per_class"][label]["f1"]
                for label in LABELS
            },
        },
        "paired_bootstrap_refreshed_minus_prior": bootstrap_delta(gold, prior_pred, current_pred),
    }
    refresh_evaluation = {
        "status": "not_evaluable",
        "reason": "frozen refresh validation contains zero primary-four Stage-2 positives",
        "all_reviewed_rows": len(refresh_all),
        "primary_four_positive_rows": len(refresh_primary),
        "other_documentation_positive_rows": sum(
            row.get("gold_docs_update_required") is True and row.get("gold_doc_category") == "other_documentation"
            for row in refresh_all
        ),
        "no_update_rows": sum(row.get("gold_doc_category") == "no_update" for row in refresh_all),
        "repository_count": len({str(row.get("repository") or "") for row in refresh_all}),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    model_path = args.output_dir / "model" / "category_hybrid_natural_refresh_v1.joblib"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, model_path)
    write_jsonl(args.output_dir / "old_development_validation_predictions.jsonl", predictions)
    write_json(args.output_dir / "old_development_validation_comparison.json", comparison)
    write_json(args.output_dir / "refresh_validation_evaluation.json", refresh_evaluation)
    plot_confusion(metrics["evaluation"], args.output_dir / "figures" / "refreshed_normalized_confusion_matrix.png")
    plot_before_after(prior_metrics, metrics["evaluation"], args.output_dir / "figures" / "before_after_per_class_f1.png")

    manifest = {
        "schema": "natural_diversity_refresh_category_v1",
        "model": f"{MODEL_ID}__natural_diversity_expansion_v1",
        "fixed_model_no_search": True,
        "controlled_data_used": False,
        "confirmation_accessed": False,
        "training": {
            "old_natural_primary_four": source_distribution(old_train),
            "new_natural_primary_four": source_distribution(expansion_train),
            "combined_natural_primary_four": source_distribution(combined_train),
        },
        "old_development_validation": source_distribution(old_validation),
        "refresh_validation": refresh_evaluation,
        "membership_audit": audit,
        "source_hashes": {
            str(path): sha256_path(path)
            for path in (
                args.old_train,
                args.old_validation,
                args.expansion_train,
                args.refresh_validation,
                args.prior_predictions,
            )
        },
        "model_sha256": sha256_path(model_path),
        "embedding": {
            "model_name": MODEL_NAME,
            "revision": MODEL_REVISION,
            "license": MODEL_LICENSE,
            "code_cache": code_cache,
            "docs_cache": docs_cache,
        },
        "runtime": {
            "seconds": time.perf_counter() - started,
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
    }
    write_json(args.output_dir / "experiment_manifest.json", manifest)
    report = [
        "# Natural Diversity Expansion V1 — fixed Category refresh",
        "",
        "No model search was performed. The fixed natural-only hybrid multinomial logistic regression was retrained.",
        "",
        f"- Old natural training positives: **{len(old_train)}**",
        f"- New expansion-train primary-four positives: **{len(expansion_train)}**",
        f"- Combined natural training positives: **{len(combined_train)}**",
        f"- Old validation Macro-F1 before / after: **{prior_metrics['macro_f1']:.4f} / {metrics['evaluation']['macro_f1']:.4f}**",
        f"- Delta Macro-F1: **{comparison['delta']['macro_f1']:+.4f}**",
        f"- Balanced accuracy before / after: **{prior_metrics['balanced_accuracy']:.4f} / {metrics['evaluation']['balanced_accuracy']:.4f}**",
        f"- Delta balanced accuracy: **{comparison['delta']['balanced_accuracy']:+.4f}**",
        f"- developer_setup F1 before / after: **{prior_metrics['per_class']['developer_setup']['f1']:.4f} / {metrics['evaluation']['per_class']['developer_setup']['f1']:.4f}**",
        f"- Refresh Category evaluation: **not evaluable** ({refresh_evaluation['primary_four_positive_rows']} primary-four positives)",
        "- Confirmation accessed: **no**",
    ]
    (args.output_dir / "FINAL_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return {"comparison": comparison, "refresh_validation": refresh_evaluation, "manifest": manifest}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-train", type=Path, required=True)
    parser.add_argument("--old-validation", type=Path, required=True)
    parser.add_argument("--expansion-train", type=Path, required=True)
    parser.add_argument("--refresh-validation", type=Path, required=True)
    parser.add_argument("--prior-predictions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--embedding-cache-dir", type=Path, required=True)
    parser.add_argument("--model-cache-dir", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(json.dumps({
        "status": "ok",
        "macro_f1_before": result["comparison"]["prior"]["macro_f1"],
        "macro_f1_after": result["comparison"]["refreshed"]["macro_f1"],
        "refresh_status": result["refresh_validation"]["status"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
