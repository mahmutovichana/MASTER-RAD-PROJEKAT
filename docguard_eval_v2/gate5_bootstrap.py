from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, Sequence

import numpy as np


DEFAULT_SEED = 42
DEFAULT_N_BOOTSTRAP = 2000
DEFAULT_ALPHA = 0.05


def normalized_repository(row: dict[str, Any]) -> str:
    repository = str(row.get("repository") or "").strip().lower()

    if not repository:
        raise ValueError(
            "Repository-cluster bootstrap requires a non-empty repository."
        )

    return repository


def repository_groups(
    rows: Sequence[dict[str, Any]],
) -> dict[str, list[int]]:
    groups: dict[str, list[int]] = defaultdict(list)

    for index, row in enumerate(rows):
        groups[normalized_repository(row)].append(index)

    if not groups:
        raise ValueError(
            "Repository-cluster bootstrap requires at least one row."
        )

    return dict(sorted(groups.items()))


def draw_repository_cluster_indices(
    rows: Sequence[dict[str, Any]],
    rng: np.random.Generator,
) -> list[int]:
    groups = repository_groups(rows)
    repositories = list(groups)

    sampled = rng.choice(
        repositories,
        size=len(repositories),
        replace=True,
    )

    indexes: list[int] = []

    for repository in sampled:
        indexes.extend(groups[str(repository)])

    return indexes


def repository_cluster_bootstrap(
    metric_fn: Callable[[list[Any], list[Any]], float],
    rows: Sequence[dict[str, Any]],
    y_true: Sequence[Any],
    values: Sequence[Any],
    *,
    seed: int = DEFAULT_SEED,
    n_bootstrap: int = DEFAULT_N_BOOTSTRAP,
    alpha: float = DEFAULT_ALPHA,
    require_two_classes: bool = False,
) -> dict[str, Any]:
    if len(rows) != len(y_true) or len(rows) != len(values):
        raise ValueError(
            "rows, y_true and values must have identical lengths."
        )

    if not rows:
        return {
            "low": 0.0,
            "high": 0.0,
            "valid_replicates": 0,
            "requested_replicates": int(n_bootstrap),
            "seed": int(seed),
            "alpha": float(alpha),
            "sampling_unit": "repository",
        }

    if n_bootstrap <= 0:
        raise ValueError("n_bootstrap must be positive.")

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")

    # Validate cluster identity before the first draw.
    repository_groups(rows)

    rng = np.random.default_rng(seed)
    metric_values: list[float] = []

    for _ in range(n_bootstrap):
        indexes = draw_repository_cluster_indices(
            rows,
            rng,
        )

        sampled_true = [
            y_true[index]
            for index in indexes
        ]

        sampled_values = [
            values[index]
            for index in indexes
        ]

        if (
            require_two_classes
            and len(set(sampled_true)) < 2
        ):
            continue

        try:
            value = float(
                metric_fn(
                    sampled_true,
                    sampled_values,
                )
            )
        except Exception:
            continue

        if np.isfinite(value):
            metric_values.append(value)

    if not metric_values:
        return {
            "low": 0.0,
            "high": 0.0,
            "valid_replicates": 0,
            "requested_replicates": int(n_bootstrap),
            "seed": int(seed),
            "alpha": float(alpha),
            "sampling_unit": "repository",
        }

    return {
        "low": float(
            np.quantile(
                metric_values,
                alpha / 2,
            )
        ),
        "high": float(
            np.quantile(
                metric_values,
                1 - alpha / 2,
            )
        ),
        "valid_replicates": len(metric_values),
        "requested_replicates": int(n_bootstrap),
        "seed": int(seed),
        "alpha": float(alpha),
        "sampling_unit": "repository",
    }
