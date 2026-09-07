from __future__ import annotations

import numpy as np
import pytest

from docguard_eval_v2.gate5_bootstrap import (
    draw_repository_cluster_indices,
    repository_cluster_bootstrap,
    repository_groups,
)


def synthetic_rows():
    return [
        {"case_id": "a1", "repository": "Org/A"},
        {"case_id": "a2", "repository": "org/a"},
        {"case_id": "b1", "repository": "org/b"},
        {"case_id": "c1", "repository": "org/c"},
        {"case_id": "c2", "repository": "org/c"},
        {"case_id": "c3", "repository": "org/c"},
    ]


def test_repository_groups_normalize_and_keep_full_clusters():
    groups = repository_groups(synthetic_rows())

    assert groups == {
        "org/a": [0, 1],
        "org/b": [2],
        "org/c": [3, 4, 5],
    }


def test_cluster_draw_repeats_entire_repository_cluster():
    rows = synthetic_rows()
    rng = np.random.default_rng(7)

    indexes = draw_repository_cluster_indices(
        rows,
        rng,
    )

    groups = repository_groups(rows)

    for repository, group_indexes in groups.items():
        count = sum(
            1
            for index in indexes
            if index in group_indexes
        )

        # A sampled repository contributes either zero or an
        # integer number of complete copies of its full cluster.
        assert count % len(group_indexes) == 0


def test_repository_bootstrap_is_seed42_deterministic():
    rows = synthetic_rows()

    y_true = [1, 1, 0, 0, 1, 1]
    y_pred = [1, 0, 0, 0, 1, 0]

    metric = lambda yt, yp: sum(
        int(a == b)
        for a, b in zip(yt, yp)
    ) / len(yt)

    first = repository_cluster_bootstrap(
        metric,
        rows,
        y_true,
        y_pred,
        seed=42,
        n_bootstrap=2000,
        alpha=0.05,
    )

    second = repository_cluster_bootstrap(
        metric,
        rows,
        y_true,
        y_pred,
        seed=42,
        n_bootstrap=2000,
        alpha=0.05,
    )

    assert first == second
    assert first["sampling_unit"] == "repository"
    assert first["requested_replicates"] == 2000
    assert first["valid_replicates"] == 2000
    assert first["seed"] == 42
    assert first["alpha"] == 0.05


def test_two_class_metric_skips_invalid_cluster_replicates():
    rows = [
        {"repository": "positive"},
        {"repository": "negative"},
    ]

    y_true = [1, 0]
    scores = [0.9, 0.1]

    def two_class_metric(yt, values):
        if len(set(yt)) < 2:
            raise ValueError("one class")
        return 1.0

    result = repository_cluster_bootstrap(
        two_class_metric,
        rows,
        y_true,
        scores,
        seed=42,
        n_bootstrap=2000,
        require_two_classes=True,
    )

    assert 0 < result["valid_replicates"] < 2000
    assert result["low"] == pytest.approx(1.0)
    assert result["high"] == pytest.approx(1.0)


def test_missing_repository_fails_closed():
    with pytest.raises(
        ValueError,
        match="non-empty repository",
    ):
        repository_cluster_bootstrap(
            lambda yt, yp: 1.0,
            [{"case_id": "x"}],
            [1],
            [1],
        )
