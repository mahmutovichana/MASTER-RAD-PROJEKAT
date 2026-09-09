from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path.cwd()

FINAL = (
    ROOT
    / "reports/final_v2/gate5/final_results"
)

FIGURES = FINAL / "figures"

SUMMARY_PATH = (
    FINAL
    / "gate5_final_summary.json"
)

FIGURES_MANIFEST_PATH = (
    FINAL
    / "figures_manifest.json"
)

REPORT_PATH = (
    FINAL
    / "GATE5_FINAL_REPORT.md"
)

EVIDENCE_PATH = (
    FINAL
    / "GATE5_GENERALIZATION_GAP_EVIDENCE.json"
)


def load_json(path: Path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def write_json(path: Path, payload) -> None:
    with path.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        json.dump(
            payload,
            handle,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        handle.write("\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


summary = load_json(
    SUMMARY_PATH
)

# ------------------------------------------------------------
# Frozen Gate 2 M1 development-only OOF evidence.
# Source:
# reports/final_v2/gate2/final_results/GATE2_FINAL_REPORT.md
# ------------------------------------------------------------

development = {
    "binary_mcc": 0.832147,
    "binary_mcc_ci_95": {
        "low": 0.699005,
        "high": 0.898874,
    },
    "category_macro_f1": 0.860982,
    "category_macro_f1_ci_95": {
        "low": 0.736054,
        "high": 0.925118,
    },
}

confirmation = {
    "binary_mcc":
        summary["binary"]["mcc"],

    "binary_mcc_ci_95":
        summary["binary"]["mcc_ci_95"],

    "category_macro_f1":
        summary["category"]["macro_f1"],

    "category_macro_f1_ci_95":
        summary["category"]["macro_f1_ci_95"],
}

assert abs(
    confirmation["binary_mcc"]
    - 0.5381511839614936
) < 1e-12

assert abs(
    confirmation["category_macro_f1"]
    - 0.40318848348589814
) < 1e-12


# ------------------------------------------------------------
# Build comparison figure.
# ------------------------------------------------------------

labels = [
    "Binary\nMCC",
    "Category\nMacro-F1",
]

dev_values = np.array(
    [
        development["binary_mcc"],
        development["category_macro_f1"],
    ]
)

conf_values = np.array(
    [
        confirmation["binary_mcc"],
        confirmation["category_macro_f1"],
    ]
)

dev_low = np.array(
    [
        development[
            "binary_mcc_ci_95"
        ]["low"],
        development[
            "category_macro_f1_ci_95"
        ]["low"],
    ]
)

dev_high = np.array(
    [
        development[
            "binary_mcc_ci_95"
        ]["high"],
        development[
            "category_macro_f1_ci_95"
        ]["high"],
    ]
)

conf_low = np.array(
    [
        confirmation[
            "binary_mcc_ci_95"
        ]["low"],
        confirmation[
            "category_macro_f1_ci_95"
        ]["low"],
    ]
)

conf_high = np.array(
    [
        confirmation[
            "binary_mcc_ci_95"
        ]["high"],
        confirmation[
            "category_macro_f1_ci_95"
        ]["high"],
    ]
)

dev_err = np.vstack(
    [
        dev_values - dev_low,
        dev_high - dev_values,
    ]
)

conf_err = np.vstack(
    [
        conf_values - conf_low,
        conf_high - conf_values,
    ]
)

x = np.arange(
    len(labels)
)

width = 0.32

fig, ax = plt.subplots(
    figsize=(8.4, 6.0)
)

dev_bars = ax.bar(
    x - width / 2,
    dev_values,
    width,
    yerr=dev_err,
    capsize=5,
    label="Development OOF (Gate 2)",
)

conf_bars = ax.bar(
    x + width / 2,
    conf_values,
    width,
    yerr=conf_err,
    capsize=5,
    label="Sealed confirmation (Gate 5)",
)

ax.set_ylim(
    0,
    1.05,
)

ax.set_ylabel(
    "Primary metric value"
)

ax.set_xticks(
    x,
    labels=labels,
)

ax.set_title(
    "Development vs. Sealed Confirmation Performance"
)

ax.legend()

ax.grid(
    axis="y",
    alpha=0.25,
)

for bars, values in (
    (dev_bars, dev_values),
    (conf_bars, conf_values),
):
    for bar, value in zip(
        bars,
        values,
    ):
        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            bar.get_height() + 0.025,
            f"{value:.3f}",
            ha="center",
            va="bottom",
        )


# Absolute generalization drops.
binary_drop = (
    development["binary_mcc"]
    - confirmation["binary_mcc"]
)

category_drop = (
    development["category_macro_f1"]
    - confirmation["category_macro_f1"]
)

ax.text(
    x[0],
    0.08,
    f"Δ = −{binary_drop:.3f}",
    ha="center",
    va="center",
)

ax.text(
    x[1],
    0.08,
    f"Δ = −{category_drop:.3f}",
    ha="center",
    va="center",
)

fig.tight_layout()

png = (
    FIGURES
    / "gate5_development_vs_confirmation_headline.png"
)

pdf = (
    FIGURES
    / "gate5_development_vs_confirmation_headline.pdf"
)

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


# ------------------------------------------------------------
# Evidence object.
# ------------------------------------------------------------

evidence = {
    "schema_version":
        "gate5_generalization_gap_evidence_v1",

    "status":
        "PASS",

    "comparison_type":
        "development_oof_vs_sealed_confirmation",

    "development_source":
        "reports/final_v2/gate2/final_results/GATE2_FINAL_REPORT.md",

    "confirmation_source":
        "reports/final_v2/gate5/final_results/gate5_final_summary.json",

    "development": development,

    "confirmation": confirmation,

    "absolute_change": {
        "binary_mcc":
            -binary_drop,

        "category_macro_f1":
            -category_drop,
    },

    "interpretation_boundary": (
        "Gate 2 values are repository-grouped development-only "
        "OOF estimates, while Gate 5 values are one-shot sealed "
        "confirmation estimates. The comparison quantifies observed "
        "generalization shift and must not be used for post-confirmation "
        "model tuning."
    ),

    "scientific_content_changed":
        False,

    "post_confirmation_tuning":
        False,
}

write_json(
    EVIDENCE_PATH,
    evidence,
)


# ------------------------------------------------------------
# Update final summary.
# ------------------------------------------------------------

summary[
    "development_vs_confirmation"
] = {
    "binary": {
        "metric":
            "mcc",

        "development_oof":
            development[
                "binary_mcc"
            ],

        "confirmation":
            confirmation[
                "binary_mcc"
            ],

        "absolute_change":
            -binary_drop,
    },

    "category": {
        "metric":
            "macro_f1",

        "development_oof":
            development[
                "category_macro_f1"
            ],

        "confirmation":
            confirmation[
                "category_macro_f1"
            ],

        "absolute_change":
            -category_drop,
    },

    "comparison_is_descriptive_only":
        True,

    "post_confirmation_tuning":
        False,
}

new_figure_paths = [
    str(
        png.relative_to(ROOT)
    ).replace("\\", "/"),

    str(
        pdf.relative_to(ROOT)
    ).replace("\\", "/"),
]

for rel in new_figure_paths:
    if rel not in summary["figures"]:
        summary["figures"].append(
            rel
        )

write_json(
    SUMMARY_PATH,
    summary,
)


# ------------------------------------------------------------
# Update figures manifest.
# ------------------------------------------------------------

manifest = load_json(
    FIGURES_MANIFEST_PATH
)

existing = {
    item["path"]
    for item in manifest[
        "figures"
    ]
}

for path in (
    png,
    pdf,
):
    rel = str(
        path.relative_to(ROOT)
    ).replace("\\", "/")

    if rel not in existing:
        manifest[
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
    FIGURES_MANIFEST_PATH,
    manifest,
)


# ------------------------------------------------------------
# Add section to final report once.
# ------------------------------------------------------------

report = REPORT_PATH.read_text(
    encoding="utf-8"
)

heading = (
    "## Development-to-confirmation generalization gap"
)

section = f"""
## Development-to-confirmation generalization gap

The selected M1 classifier families showed substantially stronger
development-only repository-grouped OOF performance than on the sealed
one-shot confirmation set.

| Task | Development OOF | Sealed confirmation | Absolute change |
|---|---:|---:|---:|
| Binary MCC | {development['binary_mcc']:.4f} | {confirmation['binary_mcc']:.4f} | {-binary_drop:.4f} |
| Category Macro-F1 | {development['category_macro_f1']:.4f} | {confirmation['category_macro_f1']:.4f} | {-category_drop:.4f} |

The observed change is **descriptive evidence of a generalization/domain
shift**, not a basis for further model selection or tuning. Gate 2 already
showed that aggregate development performance was materially influenced by
controlled-design examples and that natural-case slices were substantially
harder.

![Development versus sealed confirmation performance](figures/gate5_development_vs_confirmation_headline.png)

"""

if heading not in report:
    marker = "## Interpretation"

    assert marker in report

    report = report.replace(
        marker,
        section + marker,
        1,
    )

    REPORT_PATH.write_text(
        report,
        encoding="utf-8",
        newline="\n",
    )


# ------------------------------------------------------------
# Final verification.
# ------------------------------------------------------------

assert png.is_file()
assert pdf.is_file()

assert (
    load_json(
        EVIDENCE_PATH
    )["status"]
    == "PASS"
)

print()
print(
    "GATE5_GENERALIZATION_GAP_FIGURE = PASS"
)

print(
    "Binary development OOF MCC =",
    f"{development['binary_mcc']:.6f}",
)

print(
    "Binary confirmation MCC =",
    f"{confirmation['binary_mcc']:.6f}",
)

print(
    "Binary absolute change =",
    f"{-binary_drop:.6f}",
)

print(
    "Category development OOF Macro-F1 =",
    f"{development['category_macro_f1']:.6f}",
)

print(
    "Category confirmation Macro-F1 =",
    f"{confirmation['category_macro_f1']:.6f}",
)

print(
    "Category absolute change =",
    f"{-category_drop:.6f}",
)

print(
    "PNG =",
    png,
)

print(
    "PDF =",
    pdf,
)
