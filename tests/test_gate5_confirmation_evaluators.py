from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.evaluate_binary_v4_confirmation import (
    EXPECTED_BOOTSTRAP as BINARY_BOOTSTRAP,
    repository_bootstrap_binary,
    validate_freeze as validate_binary_freeze,
)
from scripts.evaluate_category_v8_confirmation import (
    EXPECTED_BOOTSTRAP as CATEGORY_BOOTSTRAP,
    repository_bootstrap_category,
    validate_freeze as validate_category_freeze,
)


def write_manifest(
    path: Path,
    *,
    task: str,
    model_sha256: str | None,
    confirmation_accessed=False,
):
    payload = {
        "schema_version":
            "gate3_classifier_freeze_manifest_v1",
        "status":
            "FROZEN",
        "task":
            task,
        "confirmation_accessed":
            confirmation_accessed,
    }

    if model_sha256 is not None:
        payload[
            "model_sha256"
        ] = model_sha256

    path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )


def test_binary_freeze_requires_current_model_sha256(
    tmp_path: Path,
):
    model = tmp_path / "model.bin"
    model.write_bytes(
        b"binary-model"
    )

    manifest = (
        tmp_path
        / "manifest.json"
    )

    write_manifest(
        manifest,
        task="binary",
        model_sha256=None,
    )

    with pytest.raises(
        ValueError,
        match="missing model_sha256",
    ):
        validate_binary_freeze(
            model,
            manifest,
        )


def test_binary_freeze_rejects_hash_mismatch(
    tmp_path: Path,
):
    model = tmp_path / "model.bin"

    model.write_bytes(
        b"binary-model"
    )

    manifest = (
        tmp_path
        / "manifest.json"
    )

    write_manifest(
        manifest,
        task="binary",
        model_sha256="bad",
    )

    with pytest.raises(
        ValueError,
        match="hash",
    ):
        validate_binary_freeze(
            model,
            manifest,
        )


def test_category_freeze_rejects_confirmation_accessed(
    tmp_path: Path,
):
    import hashlib

    model = tmp_path / "model.bin"

    model.write_bytes(
        b"category-model"
    )

    digest = hashlib.sha256(
        model.read_bytes()
    ).hexdigest()

    manifest = (
        tmp_path
        / "manifest.json"
    )

    write_manifest(
        manifest,
        task="category",
        model_sha256=digest,
        confirmation_accessed=True,
    )

    with pytest.raises(
        ValueError,
        match="confirmation_accessed",
    ):
        validate_category_freeze(
            model,
            manifest,
        )


def test_preregistered_bootstrap_policy_is_exact():
    expected = {
        "method":
            "repository_cluster_bootstrap",
        "sampling_unit":
            "repository",
        "n_bootstrap":
            2000,
        "seed":
            42,
        "alpha":
            0.05,
    }

    assert BINARY_BOOTSTRAP == expected
    assert CATEGORY_BOOTSTRAP == expected


def test_binary_repository_bootstrap_returns_brier():
    rows = [
        {
            "repository":
                "org/a",
        },
        {
            "repository":
                "org/a",
        },
        {
            "repository":
                "org/b",
        },
        {
            "repository":
                "org/c",
        },
    ]

    result = repository_bootstrap_binary(
        rows,
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0.9, 0.2, 0.1, 0.8],
    )

    assert result[
        "n_bootstrap"
    ] == 2000

    assert result[
        "seed"
    ] == 42

    assert result[
        "sampling_unit"
    ] == "repository"

    assert "mcc" in result[
        "metrics"
    ]

    assert "brier_score" in result[
        "metrics"
    ]


def test_category_repository_bootstrap_is_preregistered():
    rows = [
        {
            "repository":
                "org/a",
        },
        {
            "repository":
                "org/a",
        },
        {
            "repository":
                "org/b",
        },
        {
            "repository":
                "org/c",
        },
    ]

    y_true = [
        "api_reference",
        "configuration",
        "developer_setup",
        "model_contract",
    ]

    result = repository_bootstrap_category(
        rows,
        y_true,
        list(y_true),
    )

    assert result[
        "n_bootstrap"
    ] == 2000

    assert result[
        "seed"
    ] == 42

    assert result[
        "sampling_unit"
    ] == "repository"

    assert "macro_f1" in result[
        "metrics"
    ]

    assert "weighted_f1" in result[
        "metrics"
    ]
