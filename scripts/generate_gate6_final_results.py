from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


DIMENSIONS = [
    ("human_factual_correctness", "Factual\ncorrectness"),
    ("human_semantic_completeness", "Semantic\ncompleteness"),
    ("human_developer_usefulness", "Developer\nusefulness"),
    ("human_readability", "Readability"),
    ("human_style_fit", "Style fit"),
]
EXPECTED_MEANS = {
    "human_factual_correctness": 4.142857142857143,
    "human_semantic_completeness": 4.357142857142857,
    "human_developer_usefulness": 2.0,
    "human_readability": 4.714285714285714,
    "human_style_fit": 2.0714285714285716,
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_figure(fig: plt.Figure, figure_dir: Path, stem: str) -> list[Path]:
    outputs = [figure_dir / f"{stem}.png", figure_dir / f"{stem}.pdf"]
    fig.savefig(outputs[0], dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(outputs[1], bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return outputs


def style_axis(ax: plt.Axes) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#D8DEE9", linewidth=0.7, alpha=0.75)
    ax.set_axisbelow(True)


def run(root: Path) -> dict:
    gate6 = root / "reports/final_v2/gate6"
    final_dir = gate6 / "final_results"
    pipeline = final_dir / "pipeline"
    figure_dir = final_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)

    validation = load_json(pipeline / "completed_review_validation.json")
    human = load_json(pipeline / "human/human_review_summary.json")
    aggregate = load_json(pipeline / "aggregate/stage3_final_evaluation_summary.json")
    reference_raw = load_json(pipeline / "reference/reference_metrics.json")
    safety = load_json(pipeline / "diagnostics/primary_safety_diagnostics.json")
    sample_manifest = load_json(gate6 / "samples/sample_manifest.json")
    review_manifest = load_json(gate6 / "review/gate6_primary_blind_review_manifest.json")

    if validation.get("status") != "PASS":
        raise ValueError("Completed review validation did not pass.")
    if (human["total_evaluated"], human["no_output_system_failure_rows"], human["scorable_output_rows"]) != (100, 86, 14):
        raise ValueError("Gate 6 row-count integrity check failed.")
    if human["accepted_output_rows"] != 0:
        raise ValueError("Expected 0 accept-as-is judgments from the completed workbook.")
    for key, expected in EXPECTED_MEANS.items():
        actual = float(human["dimensions"][key]["mean"])
        if not np.isclose(actual, expected, atol=1e-12):
            raise ValueError(f"Workbook-derived mean differs for {key}: {actual} != {expected}")

    cis = aggregate["human_confidence_intervals_95"]
    dimensions: dict[str, dict] = {}
    for key, _ in DIMENSIONS:
        item = human["dimensions"][key]
        dimensions[key] = {
            "n": 14,
            "mean": item["mean"],
            "median": item["median"],
            "distribution_scores_1_to_5": {str(score): int(item["distribution"].get(str(score), 0)) for score in range(1, 6)},
            "bootstrap_ci_95_for_mean": cis[f"mean_{key.removeprefix('human_')}"] ,
        }

    human_metrics = {
        "schema_version": "gate6_human_evaluation_metrics_v1",
        "sample_scope": "primary_natural_distribution",
        "primary_sample_size": 100,
        "generated_scorable_rows": 14,
        "no_output_system_failure_rows": 86,
        "system_coverage": {"numerator": 14, "denominator": 100, "rate": 0.14},
        "no_output_system_failure_rate": {"numerator": 86, "denominator": 100, "rate": 0.86},
        "end_to_end_accept_as_is": {"numerator": 0, "denominator": 100, "rate": 0.0, "bootstrap_ci_95": cis["end_to_end_accept_as_is_rate"]},
        "conditional_output_accept_as_is": {"numerator": 0, "denominator": 14, "rate": 0.0, "bootstrap_ci_95": cis["conditional_output_accept_as_is_rate"]},
        "conditional_on_output_quality": dimensions,
        "no_output_quality_policy": "STRUCTURALLY_NA_NOT_ZERO",
        "review_status_semantics": "approved means completed and schema-valid human review; it is not human_accept_as_is.",
        "excluded_or_incomplete_reviews": human["excluded_or_incomplete_reviews"],
    }
    write_json(final_dir / "human_evaluation_metrics.json", human_metrics)

    reference = {
        "schema_version": "gate6_reference_evaluation_metrics_v1",
        "sample_scope": "primary_generated_output_rows_only",
        "diagnostic_only": True,
        "evaluated_output_rows": 14,
        "reference_available_rows": sum(bool(row["reference_available"]) for row in reference_raw["case_metrics"]),
        "reference_availability_rate": reference_raw["reference_availability_rate"],
        "word_overlap_f1": None if reference_raw["reference_availability_rate"] == 0 else reference_raw["mean_word_overlap_f1"],
        "tfidf_cosine": None if reference_raw["reference_availability_rate"] == 0 else reference_raw["mean_tfidf_cosine"],
        "exact_match": None if reference_raw["reference_availability_rate"] == 0 else sum(row["exact_match"] for row in reference_raw["case_metrics"]) / len(reference_raw["case_metrics"]),
        "implementation_empty_set_sentinel_note": (
            "The frozen evaluator emits numeric zero summaries when no reference text is available. "
            "Gate 6 reports these metrics as not calculated rather than interpreting the sentinel as performance."
        ),
        "interpretation": "Reference similarity is supporting diagnostic evidence only and does not replace human judgment.",
    }
    write_json(final_dir / "reference_evaluation_metrics.json", reference)

    # Figure 1: outcome composition. Quality scores are never attached to no-output rows.
    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    labels = ["No output", "Generated, rejected", "Accepted as-is"]
    values = [86, 14, 0]
    colors = ["#6B7280", "#D97706", "#0F766E"]
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.bar_label(bars, labels=["86 (86%)", "14 (14%)", "0 (0%)"], padding=5, fontsize=11, fontweight="bold")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Primary rows (n=100)")
    ax.set_title("Gate 6 primary outcome composition", loc="left", fontweight="bold", fontsize=15)
    ax.text(0, -0.20, "No-output rows have structural N/A ratings; generated outputs were judged conditionally.", transform=ax.transAxes, fontsize=9, color="#4B5563")
    style_axis(ax)
    figure_paths = save_figure(fig, figure_dir, "gate6_primary_outcome_composition")

    # Figure 2: conditional means with bootstrap intervals.
    labels = [label for _, label in DIMENSIONS]
    means = [dimensions[key]["mean"] for key, _ in DIMENSIONS]
    lows = [dimensions[key]["bootstrap_ci_95_for_mean"]["low"] for key, _ in DIMENSIONS]
    highs = [dimensions[key]["bootstrap_ci_95_for_mean"]["high"] for key, _ in DIMENSIONS]
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    x = np.arange(len(labels))
    bars = ax.bar(x, means, color="#2563A6", width=0.62, yerr=[np.array(means)-np.array(lows), np.array(highs)-np.array(means)], capsize=5, ecolor="#243B53")
    ax.bar_label(bars, labels=[f"{value:.2f}" for value in means], padding=7, fontsize=10, fontweight="bold")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 5.35)
    ax.set_yticks(range(0, 6))
    ax.set_ylabel("Mean human score (1–5)")
    ax.set_title("Conditional human quality of generated outputs", loc="left", fontweight="bold", fontsize=15)
    ax.text(0, -0.22, "Output rows only (n=14); error bars are preregistered 95% bootstrap intervals. No-output rows are excluded, not scored zero.", transform=ax.transAxes, fontsize=9, color="#4B5563")
    style_axis(ax)
    figure_paths += save_figure(fig, figure_dir, "gate6_conditional_human_quality_means")

    # Figure 3: full ordinal distributions.
    fig, ax = plt.subplots(figsize=(10.5, 5.5))
    score_colors = ["#7F1D1D", "#C2410C", "#D97706", "#60A5FA", "#0F766E"]
    left = np.zeros(len(labels))
    for score, color in zip(range(1, 6), score_colors):
        counts = np.array([dimensions[key]["distribution_scores_1_to_5"][str(score)] for key, _ in DIMENSIONS])
        ax.barh(labels, counts, left=left, color=color, label=str(score), height=0.62)
        for idx, count in enumerate(counts):
            if count:
                ax.text(left[idx] + count / 2, idx, str(count), ha="center", va="center", color="white" if score in {1, 2, 5} else "#111827", fontsize=9, fontweight="bold")
        left += counts
    ax.set_xlim(0, 14)
    ax.set_xlabel("Output rows (n=14)")
    ax.set_title("Human score distributions by dimension", loc="left", fontweight="bold", fontsize=15)
    ax.legend(title="Score", ncol=5, loc="lower center", bbox_to_anchor=(0.5, -0.28), frameon=False)
    ax.grid(axis="x", color="#D8DEE9", linewidth=0.7, alpha=0.75)
    ax.spines[["top", "right"]].set_visible(False)
    ax.invert_yaxis()
    figure_paths += save_figure(fig, figure_dir, "gate6_human_score_distributions")

    # Figure 4: rates with explicit denominators.
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    summary_labels = ["System coverage\n14 / 100", "No-output failure\n86 / 100", "End-to-end accepted\n0 / 100", "Conditional accepted\n0 / 14"]
    summary_values = [14, 86, 0, 0]
    bars = ax.bar(summary_labels, summary_values, color=["#2563A6", "#6B7280", "#0F766E", "#0F766E"], width=0.62)
    ax.bar_label(bars, labels=["14%", "86%", "0%", "0%"], padding=5, fontsize=11, fontweight="bold")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Rate (%)")
    ax.set_title("Coverage and acceptance summary", loc="left", fontweight="bold", fontsize=15)
    ax.text(0, -0.22, "Acceptance is human accept-as-is. Pipeline 'approved' status indicates completed review, not acceptance.", transform=ax.transAxes, fontsize=9, color="#4B5563")
    style_axis(ax)
    figure_paths += save_figure(fig, figure_dir, "gate6_coverage_and_acceptance_summary")

    figure_manifest = {
        "schema_version": "gate6_figures_manifest_v1",
        "figures": [
            {"path": path.relative_to(root).as_posix(), "sha256": sha256_file(path), "bytes": path.stat().st_size}
            for path in figure_paths
        ],
        "quality_denominator": 14,
        "no_output_rows_assigned_numeric_scores": False,
    }
    write_json(final_dir / "figures_manifest.json", figure_manifest)

    summary = {
        "schema_version": "gate6_final_summary_v1",
        "status": "COMPLETED_FROZEN_HUMAN_EVALUATION",
        "human_evaluation_primary": human_metrics,
        "reference_diagnostics": reference,
        "safety_diagnostics": safety,
        "secondary_sample": {"rows": 83, "status": "NOT_HUMAN_EVALUATED", "pooled_into_primary": False},
        "separation_policy": "Human evaluation, reference diagnostics, and safety diagnostics are separate; no combined accuracy is computed.",
    }
    write_json(final_dir / "gate6_final_summary.json", summary)

    report_lines = [
        "# Gate 6 Final Human/Reference Evaluation",
        "",
        "**Status:** `COMPLETED_FROZEN_HUMAN_EVALUATION`",
        "",
        "The protocol and blind review template were frozen before scoring at commit `99d6ac11b04e33cd5ddbc5fc11da48388f38cb82`. The completed workbook passed the frozen membership, order, schema, no-output, completeness, and leakage checks. `review_status = approved` means that the human review is completed and valid; it does **not** mean `human_accept_as_is = yes`.",
        "",
        "## Primary outcome",
        "",
        "- System coverage: **14/100 (14.0%)** generated/scorable outputs.",
        "- No-output system failure: **86/100 (86.0%)**.",
        "- End-to-end accept-as-is: **0/100 (0.0%)**.",
        "- Conditional accept-as-is: **0/14 (0.0%)**.",
        "",
        "The 86 no-output rows retain structural `N/A` ratings. They count against end-to-end acceptance but were not assigned synthetic numeric quality scores.",
        "",
        "## Conditional-on-output human quality",
        "",
        "| Dimension | n | Mean | Median | Scores 1/2/3/4/5 | Bootstrap 95% CI for mean |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for key, label in DIMENSIONS:
        item = dimensions[key]
        dist = item["distribution_scores_1_to_5"]
        ci = item["bootstrap_ci_95_for_mean"]
        report_lines.append(f"| {label.replace(chr(10), ' ')} | 14 | {item['mean']:.6f} | {item['median']:.1f} | {dist['1']}/{dist['2']}/{dist['3']}/{dist['4']}/{dist['5']} | [{ci['low']:.6f}, {ci['high']:.6f}] |")
    report_lines += [
        "",
        "## Reference diagnostics",
        "",
        "No eligible post-change reference text was present for the 14 generated-output rows (`0/14`). Word overlap, TF-IDF cosine, and exact match are therefore **not calculated**. The evaluator's zero-valued empty-set sentinel is not interpreted as performance. Reference similarity remains diagnostic only and does not replace human judgment.",
        "",
        "## Safety diagnostics",
        "",
        f"Frozen Stage 3 execution on the primary sample invoked generation for **{safety['stage3_invocation_count']}/100** rows and produced **{safety['generated_output_rows']}/100** accepted pipeline outputs. Final statuses: `{json.dumps(safety['final_status_counts'], sort_keys=True)}`. Verifier violations: `{json.dumps(safety['safety_violation_counts'], sort_keys=True)}`. Execution errors: `{json.dumps(safety['execution_error_counts'], sort_keys=True)}`. These are provenance/safety diagnostics, not human accept-as-is judgments.",
        "",
        "## Secondary sample",
        "",
        "The supplementary category-stress sample contains 83 rows and is `NOT_HUMAN_EVALUATED`. It is not pooled into the primary result.",
        "",
        "## Methodology closure",
        "",
        "Human evaluation, reference diagnostics, and safety diagnostics remain separate. No opaque combined accuracy is computed, no post-review methodology change was made, and no Gate 5 artifact was modified.",
    ]
    (final_dir / "GATE6_FINAL_REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8", newline="\n")

    receipt = {
        "schema_version": "gate6_final_evaluation_receipt_v1",
        "status": "COMPLETE",
        "frozen_protocol_commit": "99d6ac11b04e33cd5ddbc5fc11da48388f38cb82",
        "review_workbook_path": "reports/final_v2/gate6/review/gate6_primary_blind_review.xlsx",
        "review_workbook_sha256": validation["review_workbook_sha256"],
        "frozen_review_template_sha256": validation["frozen_review_template_sha256"],
        "sample_hash": sample_manifest["primary"]["source_hash"],
        "primary_sample_sha256": review_manifest["source_sample_sha256"],
        "primary_rows": 100,
        "no_output_system_failure_rows": 86,
        "scorable_output_rows": 14,
        "completed_scorable_reviews": 14,
        "completion_state": "ALL_PRIMARY_ROWS_COMPLETE_UNDER_FROZEN_POLICY",
        "no_output_policy": "NO_OUTPUT_SYSTEM_FAILURE_COUNTS_AS_END_TO_END_FAILURE_WITH_STRUCTURAL_NA_QUALITY",
        "no_post_review_methodology_changes": True,
        "secondary_status": "NOT_HUMAN_EVALUATED_NOT_POOLED",
        "review_validation_sha256": sha256_file(pipeline / "completed_review_validation.json"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(final_dir / "GATE6_FINAL_EVALUATION_RECEIPT.json", receipt)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate final Gate 6 human/reference evaluation artifacts and figures.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    result = run(Path(args.root))
    print(json.dumps({"status": result["status"], "output": "reports/final_v2/gate6/final_results"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
