from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib

from docguard_eval_v2.gate5_bootstrap import (
    DEFAULT_ALPHA,
    DEFAULT_N_BOOTSTRAP,
    DEFAULT_SEED,
    repository_cluster_bootstrap,
)
from docguard_ml_v2.data_contract import (
    PRIMARY_STAGE2_LABELS,
    category_eligible_rows,
    category_labels,
    load_jsonl,
    write_json,
    write_jsonl,
)
from docguard_ml_v2.metrics import (
    category_metrics,
    per_language_category_metrics,
)
from docguard_ml_v2.model_manifest import (
    sha256_file,
    utc_now,
)


EXPECTED_BOOTSTRAP = {
    "method": "repository_cluster_bootstrap",
    "sampling_unit": "repository",
    "n_bootstrap": 2000,
    "seed": 42,
    "alpha": 0.05,
}


def load_manifest(
    path: Path,
) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            "Freeze manifest is required before confirmation evaluation."
        )

    payload = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(
        payload,
        dict,
    ):
        raise ValueError(
            "Freeze manifest must be a JSON object."
        )

    return payload


def validate_freeze(
    model: Path,
    freeze_manifest: Path,
) -> dict[str, Any]:
    manifest = load_manifest(
        freeze_manifest
    )

    if (
        manifest.get("schema_version")
        != "gate3_classifier_freeze_manifest_v1"
    ):
        raise ValueError(
            "Unexpected Gate 3 freeze manifest schema."
        )

    if manifest.get("status") != "FROZEN":
        raise ValueError(
            "Category freeze manifest must have status=FROZEN."
        )

    if manifest.get("task") != "category":
        raise ValueError(
            "Category evaluator received a non-category freeze manifest."
        )

    if (
        manifest.get(
            "confirmation_accessed"
        )
        is not False
    ):
        raise ValueError(
            "Freeze manifest must state confirmation_accessed=false."
        )

    expected = manifest.get(
        "model_sha256"
    )

    if not expected:
        raise ValueError(
            "Category freeze manifest is missing model_sha256."
        )

    actual = sha256_file(
        model
    )

    if expected != actual:
        raise ValueError(
            "Model hash does not match category freeze manifest."
        )

    return manifest


def validate_confirmation_partitions(
    rows: list[dict[str, Any]],
    partition_manifest: Path | None,
) -> dict[str, Any]:
    if partition_manifest is None:
        return {
            "partition_manifest_supplied":
                False,
        }

    payload = json.loads(
        partition_manifest.read_text(
            encoding="utf-8"
        )
    )

    if (
        payload.get(
            "confirmation_sealed"
        )
        is not True
    ):
        raise ValueError(
            "Partition manifest must have confirmation_sealed=true"
        )

    manifest_hash = sha256_file(
        partition_manifest
    )

    # --------------------------------------------------------
    # Canonical Final V2 gold-manifest contract.
    #
    # The Final V2 consolidation superseded the older
    # repository-assignment manifest as the Gate 5
    # confirmation-boundary source of truth.
    # --------------------------------------------------------
    if (
        payload.get("version")
        == "consolidated_enriched_training_v2_gold"
    ):
        expected_rows = (
            payload.get(
                "partition_row_counts",
                {},
            ).get(
                "confirmation"
            )
        )

        expected_repositories = (
            payload.get(
                "partition_repository_counts",
                {},
            ).get(
                "confirmation"
            )
        )

        expected_confirmation_sha = (
            payload.get(
                "sha256",
                {},
            ).get(
                "confirmation.jsonl"
            )
        )

        if (
            expected_rows != 3747
            or expected_repositories != 52
            or payload.get(
                "repository_overlap_count"
            ) != 0
            or expected_confirmation_sha
            != "e73caca3b9ef46de284c4755127e3d7cfc0b5db9f3d1c8cd2b85be80b2c6d01b"
        ):
            raise ValueError(
                "Final V2 gold manifest confirmation boundary mismatch."
            )

        if len(rows) != expected_rows:
            raise ValueError(
                "Final V2 confirmation row-count mismatch."
            )

        repositories: set[str] = set()

        for row in rows:
            if (
                row.get("partition")
                != "confirmation"
            ):
                raise ValueError(
                    "Non-confirmation row detected."
                )

            repository = str(
                row.get("repository")
                or ""
            ).strip().lower()

            if not repository:
                raise ValueError(
                    "Confirmation row is missing repository identity."
                )

            repositories.add(
                repository
            )

        if (
            len(repositories)
            != expected_repositories
        ):
            raise ValueError(
                "Final V2 confirmation repository-count mismatch."
            )

        return {
            "partition_manifest_supplied":
                True,
            "manifest_mode":
                "final_v2_gold_manifest",
            "partition_manifest_hash":
                manifest_hash,
            "repository_partition_manifest_hash":
                manifest_hash,
            "expected_confirmation_sha256":
                expected_confirmation_sha,
            "confirmation_rows":
                len(rows),
            "confirmation_repositories":
                len(repositories),
            "repository_overlap_count":
                0,
        }

    # --------------------------------------------------------
    # Legacy compatibility path.
    # Not used by canonical Gate 5 after incident 002.
    # --------------------------------------------------------
    assignments = {
        str(repo).lower(): part
        for repo, part in (
            payload.get(
                "repository_assignments"
            )
            or {}
        ).items()
    }

    for row in rows:
        repo = str(
            row.get("repository")
            or ""
        ).lower()

        if (
            row.get("partition")
            != "confirmation"
            or assignments.get(repo)
            != "confirmation"
        ):
            raise ValueError(
                "Non-confirmation row detected."
            )

    return {
        "partition_manifest_supplied":
            True,
        "manifest_mode":
            "legacy_repository_assignments",
        "partition_manifest_hash":
            manifest_hash,
        "repository_partition_manifest_hash":
            manifest_hash,
    }


def one_shot_guard(
    output_dir: Path,
    model_hash: str,
    confirmation_hash: str,
    *,
    enforce: bool,
    allow_repeat: bool,
) -> None:
    receipt = (
        output_dir
        / "confirmation_evaluation_receipt.json"
    )

    if (
        enforce
        and receipt.exists()
    ):
        existing = json.loads(
            receipt.read_text(
                encoding="utf-8"
            )
        )

        if (
            existing.get(
                "model_hash"
            )
            == model_hash
            and existing.get(
                "confirmation_dataset_sha256"
            )
            == confirmation_hash
            and not allow_repeat
        ):
            raise ValueError(
                "Confirmation already evaluated for "
                "this model and dataset."
            )


def _category_metric(
    name: str,
):
    def metric(
        yt: list[str],
        yp: list[str],
    ) -> float:
        return float(
            category_metrics(
                yt,
                yp,
                PRIMARY_STAGE2_LABELS,
            )[name]
        )

    return metric


def repository_bootstrap_category(
    rows: list[dict[str, Any]],
    y_true: list[str],
    y_pred: list[str],
) -> dict[str, Any]:
    output = {
        "method":
            "repository_cluster_bootstrap",
        "sampling_unit":
            "repository",
        "seed":
            DEFAULT_SEED,
        "n_bootstrap":
            DEFAULT_N_BOOTSTRAP,
        "alpha":
            DEFAULT_ALPHA,
        "metrics": {},
    }

    for metric_name in (
        "macro_f1",
        "accuracy",
        "weighted_f1",
        "balanced_accuracy",
    ):
        output[
            "metrics"
        ][
            metric_name
        ] = repository_cluster_bootstrap(
            _category_metric(
                metric_name
            ),
            rows,
            y_true,
            y_pred,
            seed=DEFAULT_SEED,
            n_bootstrap=
                DEFAULT_N_BOOTSTRAP,
            alpha=
                DEFAULT_ALPHA,
        )

    return output


def run(
    *,
    model_path: Path,
    confirmation: Path,
    freeze_manifest: Path,
    output_dir: Path,
    partition_manifest: Path | None = None,
    enforce_one_shot: bool = False,
    allow_repeat_for_reproducibility: bool = False,
) -> dict[str, Any]:
    manifest = validate_freeze(
        model_path,
        freeze_manifest,
    )

    model_hash = sha256_file(
        model_path
    )

    confirmation_hash = sha256_file(
        confirmation
    )

    one_shot_guard(
        output_dir,
        model_hash,
        confirmation_hash,
        enforce=enforce_one_shot,
        allow_repeat=
            allow_repeat_for_reproducibility,
    )

    payload = joblib.load(
        model_path
    )

    source_rows = load_jsonl(
        confirmation
    )

    partition_info = (
        validate_confirmation_partitions(
            source_rows,
            partition_manifest,
        )
    )

    if (
        partition_info.get(
            "manifest_mode"
        )
        == "final_v2_gold_manifest"
        and confirmation_hash
        != partition_info[
            "expected_confirmation_sha256"
        ]
    ):
        raise ValueError(
            "Frozen Final V2 confirmation SHA-256 mismatch."
        )

    intrinsic_rows = (
        category_eligible_rows(
            source_rows,
            allowed_partitions={
                "confirmation"
            },
        )
    )

    y_true = category_labels(
        intrinsic_rows
    )

    model = payload["model"]

    y_pred = [
        str(item)
        for item
        in model.predict(
            intrinsic_rows
        )
    ]

    intrinsic = category_metrics(
        y_true,
        y_pred,
        PRIMARY_STAGE2_LABELS,
    )

    intrinsic[
        "repository_bootstrap_ci_95"
    ] = repository_bootstrap_category(
        intrinsic_rows,
        y_true,
        y_pred,
    )

    intrinsic[
        "per_language"
    ] = per_language_category_metrics(
        intrinsic_rows,
        y_true,
        y_pred,
        PRIMARY_STAGE2_LABELS,
    )

    report = {
        "stage2_intrinsic_scope":
            intrinsic,

        "end_to_end_conditional_scope":
            {
                "status":
                    "not_evaluated_here",
                "reason":
                    "Requires Binary predicted-positive "
                    "scope and is reported separately.",
            },
    }

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    write_jsonl(
        output_dir
        / "confirmation_predictions.jsonl",
        [
            {
                "case_id":
                    row.get("case_id"),
                "repository":
                    row.get("repository"),
                "language":
                    row.get("language"),
                "gold":
                    gold,
                "prediction":
                    pred,
            }
            for row, gold, pred
            in zip(
                intrinsic_rows,
                y_true,
                y_pred,
            )
        ],
    )

    write_json(
        output_dir
        / "confirmation_metrics.json",
        report,
    )

    receipt = {
        "confirmation_evaluated": True,
        "evaluation_timestamp":
            utc_now(),
        "model_hash":
            model_hash,
        "confirmation_dataset_sha256":
            confirmation_hash,
        "freeze_manifest_hash":
            sha256_file(
                freeze_manifest
            ),
        "bootstrap_policy":
            EXPECTED_BOOTSTRAP,
        **partition_info,
        "repeat_for_reproducibility":
            bool(
                allow_repeat_for_reproducibility
            ),
    }

    write_json(
        output_dir
        / "confirmation_evaluation_receipt.json",
        receipt,
    )

    (
        output_dir
        / "confirmation_report.md"
    ).write_text(
        "# Category V8 Confirmation Evaluation\n\n"
        f"- Frozen family: "
        f"`{manifest.get('selected_family')}`\n"
        f"- Intrinsic Macro-F1: "
        f"`{intrinsic['macro_f1']:.4f}`\n"
        f"- Intrinsic accuracy: "
        f"`{intrinsic['accuracy']:.4f}`\n\n"
        "End-to-end Binary-conditioned scope is "
        "reported separately.\n",
        encoding="utf-8",
        newline="\n",
    )

    return {
        "status": "ok",
        "metrics": report,
        "receipt": receipt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate frozen Category V8 "
            "on confirmation only."
        )
    )

    parser.add_argument(
        "--model",
        required=True,
    )

    parser.add_argument(
        "--confirmation",
        required=True,
    )

    parser.add_argument(
        "--freeze-manifest",
        required=True,
    )

    parser.add_argument(
        "--output-dir",
        required=True,
    )

    parser.add_argument(
        "--repository-partition-manifest",
    )

    parser.add_argument(
        "--enforce-one-shot",
        action="store_true",
    )

    parser.add_argument(
        "--allow-repeat-for-reproducibility",
        action="store_true",
    )

    args = parser.parse_args()

    result = run(
        model_path=Path(
            args.model
        ),
        confirmation=Path(
            args.confirmation
        ),
        freeze_manifest=Path(
            args.freeze_manifest
        ),
        output_dir=Path(
            args.output_dir
        ),
        partition_manifest=(
            Path(
                args.repository_partition_manifest
            )
            if args.repository_partition_manifest
            else None
        ),
        enforce_one_shot=
            args.enforce_one_shot,
        allow_repeat_for_reproducibility=
            args.allow_repeat_for_reproducibility,
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
