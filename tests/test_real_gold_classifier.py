from __future__ import annotations

from docguard_external.real_gold_classifier import build_text, compute_metrics, make_pipeline


def test_build_text_uses_safe_fields_only() -> None:
    row = {
        "language": "typescript",
        "code_changed_files": ["src/api.ts"],
        "code_diff_excerpt": "+export type UserDto = { id: string }",
        "docs_before_excerpt": "# API",
        "docs_after_excerpt": "SHOULD_NOT_APPEAR",
        "manual_label_notes": "SHOULD_NOT_APPEAR",
        "source_url": "https://github.com/example/repo/pull/1",
    }

    text = build_text(row)

    assert "typescript" in text
    assert "src/api.ts" in text
    assert "UserDto" in text
    assert "SHOULD_NOT_APPEAR" not in text
    assert "github.com" not in text


def test_compute_metrics() -> None:
    metrics = compute_metrics(
        gold=[1, 1, 0, 0],
        pred=[1, 0, 1, 0],
    )

    assert metrics["true_positives"] == 1
    assert metrics["false_negatives"] == 1
    assert metrics["false_positives"] == 1
    assert metrics["true_negatives"] == 1
    assert metrics["accuracy"] == 0.5


def test_make_pipeline_can_fit_small_dataset() -> None:
    rows = [
        "api endpoint added request response schema",
        "test fixture mock only",
        "configuration option environment variable",
        "internal refactor rename imports",
    ]
    labels = [1, 0, 1, 0]

    model = make_pipeline()
    model.fit(rows, labels)

    preds = model.predict(rows)

    assert len(preds) == 4