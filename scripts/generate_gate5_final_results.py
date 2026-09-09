from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path.cwd()

ONE_SHOT = (
    ROOT
    / "reports/final_v2/gate5/one_shot"
)

OUT = (
    ROOT
    / "reports/final_v2/gate5/final_results"
)

FIGURES = OUT / "figures"

EXPECTED_CONFIRMATION_SHA = (
    "e73caca3b9ef46de284c4755127e3d7cfc0b5db9f3d1c8cd2b85be80b2c6d01b"
)

EXPECTED_BINARY_SHA = (
    "7d6a9263e1262c5c54db3d2e100209707c6a7681133fb1505f44125efa954462"
)

EXPECTED_CATEGORY_SHA = (
    "2d8123ac398568b5c9586b0f8d26d6c4079ddfebd504889b934f77bef65b9f59"
)

EXPECTED_PREREG_SHA = (
    "dd4ed749774c144d3533128e93749fa003925dbdf73b1a121fee1a3fd40dc3b8"
)

RETURN_ARCHIVE_SHA = (
    "bc57c02eba812152713116e978add4c1181d8a741b6a7ed717bd5d4796ea8126"
)

EXECUTION_COMMIT = (
    "88e185a637f11204a1af7b2a6ad2eddc6032e30f"
)


def load_json(path: Path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(
                1024 * 1024
            ),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        json.dump(
            payload,
            handle,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        text,
        encoding="utf-8",
        newline="\n",
    )


def save_figure(fig, stem: str) -> list[str]:
    FIGURES.mkdir(
        parents=True,
        exist_ok=True,
    )

    png = FIGURES / f"{stem}.png"
    pdf = FIGURES / f"{stem}.pdf"

    fig.tight_layout()

    fig.savefig(
        png,
        dpi=300,
        bbox_inches="tight",
    )

    fig.savefig(
        pdf,
        bbox_inches="tight",
    )

    plt.close(fig)

    return [
        str(
            png.relative_to(ROOT)
        ).replace("\\", "/"),
        str(
            pdf.relative_to(ROOT)
        ).replace("\\", "/"),
    ]


# ============================================================
# Load final one-shot evidence.
# ============================================================

receipt = load_json(
    ONE_SHOT
    / "GATE5_MASTER_ONE_SHOT_RECEIPT.json"
)

binary = load_json(
    ONE_SHOT
    / "binary/confirmation_metrics.json"
)

category = load_json(
    ONE_SHOT
    / "category/confirmation_metrics.json"
)

stage3 = load_json(
    ONE_SHOT
    / "stage3/stage3_confirmation_generation_receipt.json"
)


# ============================================================
# Integrity checks.
# ============================================================

assert (
    receipt["status"]
    == "COMPLETED_ONE_SHOT_CONFIRMATION"
)

assert (
    receipt["master_receipt_written_last"]
    is True
)

assert (
    receipt["rerun_allowed"]
    is False
)

assert (
    receipt["confirmation_accessed"]
    is True
)

assert (
    receipt["confirmation_dataset_sha256"]
    == EXPECTED_CONFIRMATION_SHA
)

assert (
    receipt["binary_model_sha256"]
    == EXPECTED_BINARY_SHA
)

assert (
    receipt["category_model_sha256"]
    == EXPECTED_CATEGORY_SHA
)

assert (
    receipt["gate5_preregistration_sha256"]
    == EXPECTED_PREREG_SHA
)

for rel, expected in (
    receipt["output_sha256"].items()
):
    path = ROOT / rel

    assert path.exists(), path

    actual = sha256(
        path
    )

    assert actual == expected, (
        rel,
        expected,
        actual,
    )


# ============================================================
# 1. Binary confusion matrix.
# ============================================================

cm = binary[
    "confusion_matrix"
]

binary_matrix = np.array(
    [
        [
            cm["tn"],
            cm["fp"],
        ],
        [
            cm["fn"],
            cm["tp"],
        ],
    ]
)

fig, ax = plt.subplots(
    figsize=(6.4, 5.2)
)

image = ax.imshow(
    binary_matrix
)

ax.set_title(
    "Gate 5 Binary Confirmation Confusion Matrix"
)

ax.set_xlabel(
    "Predicted label"
)

ax.set_ylabel(
    "Gold label"
)

ax.set_xticks(
    [0, 1],
    labels=[
        "No update",
        "Update required",
    ],
)

ax.set_yticks(
    [0, 1],
    labels=[
        "No update",
        "Update required",
    ],
)

for i in range(2):
    for j in range(2):
        ax.text(
            j,
            i,
            f"{binary_matrix[i, j]:,}",
            ha="center",
            va="center",
        )

fig.colorbar(
    image,
    ax=ax,
    label="Cases",
)

figure_paths = save_figure(
    fig,
    "gate5_binary_confusion_matrix",
)


# ============================================================
# 2. Binary key metrics with bootstrap CIs.
# ============================================================

ci = binary[
    "repository_bootstrap_ci_95"
][
    "metrics"
]

metric_specs = [
    (
        "MCC",
        "mcc",
    ),
    (
        "F1",
        "f1",
    ),
    (
        "Precision",
        "precision",
    ),
    (
        "Recall",
        "recall",
    ),
    (
        "Specificity",
        "specificity",
    ),
    (
        "Accuracy",
        "accuracy",
    ),
    (
        "ROC-AUC",
        "roc_auc",
    ),
    (
        "Average precision",
        "average_precision",
    ),
]

labels = []
points = []
lows = []
highs = []

for label, key in metric_specs:
    labels.append(
        label
    )

    points.append(
        float(
            binary[key]
        )
    )

    lows.append(
        float(
            ci[key]["low"]
        )
    )

    highs.append(
        float(
            ci[key]["high"]
        )
    )

points = np.asarray(
    points
)

lows = np.asarray(
    lows
)

highs = np.asarray(
    highs
)

errors = np.vstack(
    [
        points - lows,
        highs - points,
    ]
)

fig, ax = plt.subplots(
    figsize=(8.5, 5.8)
)

positions = np.arange(
    len(labels)
)

ax.errorbar(
    points,
    positions,
    xerr=errors,
    fmt="o",
    capsize=4,
)

ax.set_yticks(
    positions,
    labels=labels,
)

ax.invert_yaxis()

ax.set_xlim(
    0,
    1.02,
)

ax.set_xlabel(
    "Metric value"
)

ax.set_title(
    "Gate 5 Binary Confirmation Metrics with 95% Repository-Bootstrap CI"
)

ax.grid(
    axis="x",
    alpha=0.25,
)

for y, value in zip(
    positions,
    points,
):
    ax.text(
        min(
            value + 0.025,
            0.98,
        ),
        y,
        f"{value:.3f}",
        va="center",
    )

figure_paths += save_figure(
    fig,
    "gate5_binary_metrics_bootstrap_ci",
)


# ============================================================
# 3. Category confusion matrix.
# ============================================================

cat = category[
    "stage2_intrinsic_scope"
]

class_names = [
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
]

category_matrix = np.asarray(
    cat[
        "confusion_matrix"
    ],
    dtype=int,
)

fig, ax = plt.subplots(
    figsize=(8.0, 6.6)
)

image = ax.imshow(
    category_matrix
)

ax.set_title(
    "Gate 5 Category Confirmation Confusion Matrix"
)

ax.set_xlabel(
    "Predicted category"
)

ax.set_ylabel(
    "Gold category"
)

display_labels = [
    "API reference",
    "Configuration",
    "Developer setup",
    "Model contract",
]

ax.set_xticks(
    range(4),
    labels=display_labels,
    rotation=30,
    ha="right",
)

ax.set_yticks(
    range(4),
    labels=display_labels,
)

for i in range(4):
    for j in range(4):
        ax.text(
            j,
            i,
            str(
                category_matrix[
                    i,
                    j,
                ]
            ),
            ha="center",
            va="center",
        )

fig.colorbar(
    image,
    ax=ax,
    label="Cases",
)

figure_paths += save_figure(
    fig,
    "gate5_category_confusion_matrix",
)


# ============================================================
# 4. Category per-class Precision / Recall / F1.
# ============================================================

precision = []
recall = []
f1 = []

for name in class_names:
    metrics = cat[
        "per_class"
    ][
        name
    ]

    precision.append(
        metrics["precision"]
    )

    recall.append(
        metrics["recall"]
    )

    f1.append(
        metrics["f1"]
    )

x = np.arange(
    len(class_names)
)

width = 0.24

fig, ax = plt.subplots(
    figsize=(9.0, 5.8)
)

ax.bar(
    x - width,
    precision,
    width,
    label="Precision",
)

ax.bar(
    x,
    recall,
    width,
    label="Recall",
)

ax.bar(
    x + width,
    f1,
    width,
    label="F1",
)

ax.set_ylim(
    0,
    1,
)

ax.set_ylabel(
    "Score"
)

ax.set_title(
    "Gate 5 Category Confirmation Performance by Class"
)

ax.set_xticks(
    x,
    labels=display_labels,
    rotation=25,
    ha="right",
)

ax.legend()

ax.grid(
    axis="y",
    alpha=0.25,
)

figure_paths += save_figure(
    fig,
    "gate5_category_per_class_metrics",
)


# ============================================================
# 5. Stage 3 predicted-positive flow.
# ============================================================

stage3_labels = [
    "Retrieval context\nunavailable",
    "Accepted\nfirst pass",
    "Accepted\nafter repair",
    "Human review\nrequired",
]

stage3_values = [
    stage3[
        "retrieval_context_unavailable_count"
    ],
    stage3[
        "final_status_counts"
    ][
        "accepted_first_pass"
    ],
    stage3[
        "final_status_counts"
    ][
        "accepted_after_repair"
    ],
    stage3[
        "final_status_counts"
    ][
        "human_review_required"
    ],
]

assert (
    sum(
        stage3_values
    )
    == stage3[
        "frozen_binary_predicted_positive_count"
    ]
)

fig, ax = plt.subplots(
    figsize=(9.0, 5.8)
)

bars = ax.bar(
    stage3_labels,
    stage3_values,
)

ax.set_ylabel(
    "Cases"
)

ax.set_title(
    "Gate 5 Stage 3 Outcomes for Binary Predicted-Positive Cases"
)

ax.grid(
    axis="y",
    alpha=0.25,
)

for bar, value in zip(
    bars,
    stage3_values,
):
    ax.text(
        bar.get_x()
        + bar.get_width() / 2,
        bar.get_height() + 5,
        str(
            value
        ),
        ha="center",
        va="bottom",
    )

figure_paths += save_figure(
    fig,
    "gate5_stage3_predicted_positive_outcomes",
)


# ============================================================
# Derived summary values.
# ============================================================

mcc_ci = ci[
    "mcc"
]

macro_ci = cat[
    "repository_bootstrap_ci_95"
][
    "metrics"
][
    "macro_f1"
]

predicted_positive = stage3[
    "frozen_binary_predicted_positive_count"
]

context_available = stage3[
    "retrieval_context_available_count"
]

context_unavailable = stage3[
    "retrieval_context_unavailable_count"
]

accepted = (
    stage3[
        "final_status_counts"
    ][
        "accepted_first_pass"
    ]
    +
    stage3[
        "final_status_counts"
    ][
        "accepted_after_repair"
    ]
)

human_review = stage3[
    "final_status_counts"
][
    "human_review_required"
]

context_coverage = (
    context_available
    / predicted_positive
)

conditional_acceptance = (
    accepted
    / context_available
)


summary = {
    "schema_version":
        "gate5_final_summary_v1",

    "status":
        "COMPLETED_ONE_SHOT_CONFIRMATION",

    "execution_commit":
        EXECUTION_COMMIT,

    "return_archive_sha256":
        RETURN_ARCHIVE_SHA,

    "master_receipt_sha256":
        sha256(
            ONE_SHOT
            / "GATE5_MASTER_ONE_SHOT_RECEIPT.json"
        ),

    "confirmation": {
        "rows":
            binary[
                "support"
            ],

        "positive_rows":
            binary[
                "gold_counts"
            ][
                "1"
            ],

        "negative_rows":
            binary[
                "gold_counts"
            ][
                "0"
            ],

        "dataset_sha256":
            EXPECTED_CONFIRMATION_SHA,
    },

    "binary": {
        "primary_metric":
            "mcc",

        "mcc":
            binary["mcc"],

        "mcc_ci_95": {
            "low":
                mcc_ci["low"],
            "high":
                mcc_ci["high"],
        },

        "accuracy":
            binary["accuracy"],

        "balanced_accuracy":
            binary[
                "balanced_accuracy"
            ],

        "precision":
            binary["precision"],

        "recall":
            binary["recall"],

        "f1":
            binary["f1"],

        "specificity":
            binary["specificity"],

        "roc_auc":
            binary["roc_auc"],

        "average_precision":
            binary[
                "average_precision"
            ],

        "confusion_matrix":
            binary[
                "confusion_matrix"
            ],
    },

    "category": {
        "scope":
            "intrinsic_category_eligible_confirmation",

        "support":
            cat["support"],

        "primary_metric":
            "macro_f1",

        "macro_f1":
            cat[
                "macro_f1"
            ],

        "macro_f1_ci_95": {
            "low":
                macro_ci["low"],
            "high":
                macro_ci["high"],
        },

        "accuracy":
            cat["accuracy"],

        "balanced_accuracy":
            cat[
                "balanced_accuracy"
            ],

        "weighted_f1":
            cat[
                "weighted_f1"
            ],

        "per_class":
            cat[
                "per_class"
            ],
    },

    "stage3": {
        "processed_confirmation_rows":
            stage3[
                "processed_row_count"
            ],

        "binary_predicted_positive":
            predicted_positive,

        "retrieval_context_available":
            context_available,

        "retrieval_context_unavailable":
            context_unavailable,

        "retrieval_context_coverage_rate":
            context_coverage,

        "accepted_first_pass":
            stage3[
                "final_status_counts"
            ][
                "accepted_first_pass"
            ],

        "accepted_after_repair":
            stage3[
                "final_status_counts"
            ][
                "accepted_after_repair"
            ],

        "accepted_total":
            accepted,

        "human_review_required":
            human_review,

        "conditional_acceptance_given_context":
            conditional_acceptance,

        "llm_call_count":
            stage3[
                "llm_call_count"
            ],

        "execution_error_counts":
            stage3[
                "execution_error_counts"
            ],

        "safety_violation_counts":
            stage3[
                "safety_violation_counts"
            ],

        "note":
            (
                "Stage 3 acceptance is pipeline-level structured/safety "
                "acceptance, not human semantic-quality validation. "
                "Human/reference evaluation is deferred to Gate 6."
            ),
    },

    "methodology": {
        "post_confirmation_tuning":
            False,

        "rerun_allowed":
            False,

        "gate6_human_evaluation_pending":
            True,
    },

    "figures":
        figure_paths,
}


OUT.mkdir(
    parents=True,
    exist_ok=True,
)

write_json(
    OUT
    / "gate5_final_summary.json",
    summary,
)


# ============================================================
# Figures manifest with hashes.
# ============================================================

figure_manifest = {
    "schema_version":
        "gate5_figures_manifest_v1",

    "source":
        "Gate 5 completed one-shot confirmation outputs",

    "confirmation_dataset_sha256":
        EXPECTED_CONFIRMATION_SHA,

    "scientific_content_changed":
        False,

    "figures": [],
}

for rel in figure_paths:
    path = ROOT / rel

    figure_manifest[
        "figures"
    ].append(
        {
            "path":
                rel,

            "sha256":
                sha256(
                    path
                ),

            "bytes":
                path.stat().st_size,
        }
    )

write_json(
    OUT
    / "figures_manifest.json",
    figure_manifest,
)


# ============================================================
# Final Markdown report.
# ============================================================

report = f"""# Gate 5 — One-Shot Confirmation Final Report

## Status

**COMPLETED — ONE SHOT ONLY.**

The frozen confirmation dataset was evaluated exactly under the preregistered
Gate 5 protocol. The master receipt was written last and explicitly records
`rerun_allowed=false`. No post-confirmation tuning is permitted.

- Execution commit: `{EXECUTION_COMMIT}`
- Confirmation rows: `{binary['support']}`
- Confirmation SHA-256: `{EXPECTED_CONFIRMATION_SHA}`
- Return archive SHA-256: `{RETURN_ARCHIVE_SHA}`

## Binary classifier

Primary preregistered confirmation metric:

- **MCC: {binary['mcc']:.4f}**
- Repository-bootstrap 95% CI:
  **[{mcc_ci['low']:.4f}, {mcc_ci['high']:.4f}]**

Additional metrics:

| Metric | Value |
|---|---:|
| Accuracy | {binary['accuracy']:.4f} |
| Balanced accuracy | {binary['balanced_accuracy']:.4f} |
| Precision | {binary['precision']:.4f} |
| Recall | {binary['recall']:.4f} |
| F1 | {binary['f1']:.4f} |
| Specificity | {binary['specificity']:.4f} |
| ROC-AUC | {binary['roc_auc']:.4f} |
| Average precision | {binary['average_precision']:.4f} |

Confusion matrix:

- TN = {cm['tn']}
- FP = {cm['fp']}
- FN = {cm['fn']}
- TP = {cm['tp']}

![Binary confusion matrix](figures/gate5_binary_confusion_matrix.png)

![Binary metrics and bootstrap confidence intervals](figures/gate5_binary_metrics_bootstrap_ci.png)

## Category classifier

The intrinsic category evaluation contains **{cat['support']}**
category-eligible confirmation examples.

Primary preregistered metric:

- **Macro-F1: {cat['macro_f1']:.4f}**
- Repository-bootstrap 95% CI:
  **[{macro_ci['low']:.4f}, {macro_ci['high']:.4f}]**

Additional metrics:

| Metric | Value |
|---|---:|
| Accuracy | {cat['accuracy']:.4f} |
| Balanced accuracy | {cat['balanced_accuracy']:.4f} |
| Weighted F1 | {cat['weighted_f1']:.4f} |

Per-class F1:

| Category | F1 |
|---|---:|
| API reference | {cat['per_class']['api_reference']['f1']:.4f} |
| Configuration | {cat['per_class']['configuration']['f1']:.4f} |
| Developer setup | {cat['per_class']['developer_setup']['f1']:.4f} |
| Model contract | {cat['per_class']['model_contract']['f1']:.4f} |

![Category confusion matrix](figures/gate5_category_confusion_matrix.png)

![Category per-class metrics](figures/gate5_category_per_class_metrics.png)

## Stage 3 confirmation execution

The frozen Binary model predicted **{predicted_positive}** of
{stage3['processed_row_count']} confirmation cases as positive.

- Retrieval context available: **{context_available}**
  ({context_coverage:.1%} of predicted positives)
- Retrieval context unavailable: **{context_unavailable}**
- Accepted first pass: **{stage3['final_status_counts']['accepted_first_pass']}**
- Accepted after repair: **{stage3['final_status_counts']['accepted_after_repair']}**
- Total pipeline-accepted with context: **{accepted}/{context_available}**
  ({conditional_acceptance:.1%})
- Human review required: **{human_review}**
- LLM calls: **{stage3['llm_call_count']}**

Execution errors:

- Input token budget exceeded:
  **{stage3['execution_error_counts']['input_token_budget_exceeded']}**
- Invalid structured LLM output:
  **{stage3['execution_error_counts']['invalid_structured_llm_output']}**

Safety violations:

- Empty patch:
  **{stage3['safety_violation_counts']['empty_patch']}**
- Target not retrieved:
  **{stage3['safety_violation_counts']['target_not_retrieved']}**
- Unsupported fact:
  **{stage3['safety_violation_counts']['unsupported_fact']}**

![Stage 3 predicted-positive outcomes](figures/gate5_stage3_predicted_positive_outcomes.png)

## Interpretation

The confirmation results demonstrate a meaningful generalization gap relative
to development-only model-selection evidence. The Binary classifier retains
useful discrimination on the sealed confirmation set, but performance is
materially lower than development estimates. Category classification shows a
larger drop, with especially weak performance for `developer_setup`.

These confirmation results are final evidence and **must not be used to
re-tune or re-select the frozen models**.

Stage 3 results above describe retrieval availability and automatic
structured/safety acceptance. They are **not a human semantic-quality score**.
The preregistered post-confirmation human/reference evaluation is performed
separately in Gate 6.

## Gate 5 disposition

- Confirmation evaluated: **yes**
- Master receipt present: **yes**
- Rerun permitted: **no**
- Post-confirmation tuning: **no**
- Gate 6 human/reference evaluation still required: **yes**
"""

write_text(
    OUT
    / "GATE5_FINAL_REPORT.md",
    report,
)


# ============================================================
# Final self-check.
# ============================================================

assert (
    summary[
        "binary"
    ][
        "mcc"
    ]
    == binary[
        "mcc"
    ]
)

assert (
    summary[
        "category"
    ][
        "macro_f1"
    ]
    == cat[
        "macro_f1"
    ]
)

assert (
    summary[
        "stage3"
    ][
        "binary_predicted_positive"
    ]
    == 454
)

assert len(
    figure_paths
) == 10


print()
print("GATE5_FINAL_RESULTS_AND_FIGURES = PASS")
print(
    "Binary MCC =",
    f"{binary['mcc']:.6f}",
)
print(
    "Binary MCC 95% CI =",
    f"[{mcc_ci['low']:.6f}, {mcc_ci['high']:.6f}]",
)
print(
    "Category Macro-F1 =",
    f"{cat['macro_f1']:.6f}",
)
print(
    "Category Macro-F1 95% CI =",
    f"[{macro_ci['low']:.6f}, {macro_ci['high']:.6f}]",
)
print(
    "Stage3 predicted positives =",
    predicted_positive,
)
print(
    "Stage3 context available =",
    context_available,
)
print(
    "Stage3 accepted =",
    accepted,
)
print(
    "Figures generated =",
    len(figure_paths),
    "(5 PNG + 5 PDF)",
)
print(
    "Output =",
    OUT,
)
