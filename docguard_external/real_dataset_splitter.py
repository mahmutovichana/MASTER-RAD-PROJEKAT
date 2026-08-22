from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DEFAULT_SPLITS = {
    "train": 0.70,
    "validation": 0.15,
    "locked_test": 0.15,
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")
            rows.append(value)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def get_case_id(row: dict[str, Any], index: int) -> str:
    return str(row.get("case_id") or f"row-{index}")


def get_repository(row: dict[str, Any]) -> str:
    repo = row.get("repository")
    if repo:
        return str(repo)

    audit = row.get("audit_labeling_context")
    if isinstance(audit, dict) and audit.get("repository"):
        return str(audit["repository"])

    source_url = str(row.get("source_url") or "")
    if "github.com/" in source_url and "/pull/" in source_url:
        part = source_url.split("github.com/", 1)[1].split("/pull/", 1)[0]
        if "/" in part:
            return part

    return "unknown"


def get_language(row: dict[str, Any]) -> str:
    model_input = row.get("model_input")
    if isinstance(model_input, dict):
        return str(model_input.get("language") or "unknown")
    return str(row.get("language") or "unknown")


def get_label_confidence(row: dict[str, Any]) -> str:
    gold = row.get("gold_label_to_fill")
    if isinstance(gold, dict):
        return str(gold.get("label_confidence") or "")
    return str(row.get("label_confidence") or "")


def get_gold_required(row: dict[str, Any]) -> str:
    gold = row.get("gold_label_to_fill")
    if isinstance(gold, dict):
        return str(gold.get("gold_docs_update_required"))
    return str(row.get("gold_docs_update_required"))


def get_candidate_type(row: dict[str, Any]) -> str:
    evidence = row.get("candidate_evidence")
    if isinstance(evidence, dict) and evidence.get("candidate_type"):
        return str(evidence["candidate_type"])

    audit = row.get("audit_labeling_context")
    if isinstance(audit, dict):
        evidence = audit.get("candidate_evidence")
        if isinstance(evidence, dict) and evidence.get("candidate_type"):
            return str(evidence["candidate_type"])

    return "unknown"


def deterministic_hash(value: str, seed: int) -> str:
    raw = f"{seed}:{value}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def parse_split_fractions(raw: str | None) -> dict[str, float]:
    if not raw:
        return dict(DEFAULT_SPLITS)

    result: dict[str, float] = {}
    for part in raw.split(","):
        name, value = part.split("=", 1)
        result[name.strip()] = float(value.strip())

    required = {"train", "validation", "locked_test"}
    if set(result) != required:
        raise ValueError(f"Split fractions must define exactly {sorted(required)}")

    total = sum(result.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"Split fractions must sum to 1.0, got {total}")

    return result


def target_counts(total: int, fractions: dict[str, float]) -> dict[str, int]:
    train = int(round(total * fractions["train"]))
    validation = int(round(total * fractions["validation"]))
    locked_test = total - train - validation

    if locked_test < 0:
        locked_test = 0

    return {
        "train": train,
        "validation": validation,
        "locked_test": locked_test,
    }


def assign_random_splits(rows: list[dict[str, Any]], *, seed: int, fractions: dict[str, float]) -> dict[str, list[dict[str, Any]]]:
    shuffled = list(rows)
    rng = random.Random(seed)
    rng.shuffle(shuffled)

    counts = target_counts(len(shuffled), fractions)
    train_end = counts["train"]
    validation_end = train_end + counts["validation"]

    return {
        "train": shuffled[:train_end],
        "validation": shuffled[train_end:validation_end],
        "locked_test": shuffled[validation_end:],
    }


def assign_repository_group_splits(
    rows: list[dict[str, Any]],
    *,
    seed: int,
    fractions: dict[str, float],
) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[get_repository(row)].append(row)

    group_items = list(groups.items())
    group_items.sort(key=lambda item: deterministic_hash(item[0], seed))

    target = target_counts(len(rows), fractions)
    splits: dict[str, list[dict[str, Any]]] = {
        "train": [],
        "validation": [],
        "locked_test": [],
    }

    # Greedy group assignment to avoid leaking same repository across splits.
    for repo, group_rows in sorted(group_items, key=lambda item: len(item[1]), reverse=True):
        deficits = {
            split: target[split] - len(splits[split])
            for split in splits
        }

        preferred = max(deficits, key=lambda split: (deficits[split], -len(splits[split])))
        splits[preferred].extend(group_rows)

    return splits


def apply_split_metadata(splits: dict[str, list[dict[str, Any]]], *, split_strategy: str, seed: int) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}

    for split_name, rows in splits.items():
        result[split_name] = []
        for row in rows:
            copied = dict(row)
            copied["dataset_split"] = split_name
            copied["split_strategy"] = split_strategy
            copied["split_seed"] = seed
            result[split_name].append(copied)

    return result


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "records": len(rows),
        "repositories": dict(Counter(get_repository(row) for row in rows)),
        "languages": dict(Counter(get_language(row) for row in rows)),
        "candidate_types": dict(Counter(get_candidate_type(row) for row in rows)),
        "label_confidence": dict(Counter(get_label_confidence(row) for row in rows)),
        "gold_docs_update_required": dict(Counter(get_gold_required(row) for row in rows)),
    }


def check_repository_overlap(splits: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    repos_by_split = {
        split: set(get_repository(row) for row in rows)
        for split, rows in splits.items()
    }

    overlaps: list[dict[str, Any]] = []
    names = list(repos_by_split)

    for i, left in enumerate(names):
        for right in names[i + 1:]:
            overlap = sorted(repos_by_split[left] & repos_by_split[right])
            if overlap:
                overlaps.append(
                    {
                        "left": left,
                        "right": right,
                        "repositories": overlap,
                    }
                )

    return {
        "has_repository_overlap": bool(overlaps),
        "overlaps": overlaps,
    }


def split_dataset(
    rows: list[dict[str, Any]],
    *,
    seed: int,
    strategy: str,
    fractions: dict[str, float],
) -> dict[str, list[dict[str, Any]]]:
    if strategy == "random":
        raw_splits = assign_random_splits(rows, seed=seed, fractions=fractions)
    elif strategy == "repository_group":
        raw_splits = assign_repository_group_splits(rows, seed=seed, fractions=fractions)
    else:
        raise ValueError(f"Unsupported split strategy: {strategy}")

    return apply_split_metadata(raw_splits, split_strategy=strategy, seed=seed)


def build_manifest(
    *,
    input_path: Path,
    output_dir: Path,
    splits: dict[str, list[dict[str, Any]]],
    seed: int,
    strategy: str,
    fractions: dict[str, float],
) -> dict[str, Any]:
    all_rows = [row for split_rows in splits.values() for row in split_rows]

    return {
        "status": "ok",
        "input": str(input_path),
        "output_dir": str(output_dir),
        "split_strategy": strategy,
        "split_seed": seed,
        "split_fractions": fractions,
        "total_records": len(all_rows),
        "split_summary": {
            split: summarize_rows(rows)
            for split, rows in splits.items()
        },
        "overall_summary": summarize_rows(all_rows),
        "repository_overlap": check_repository_overlap(splits),
        "interpretation": {
            "note": "Splitting candidate/unlabeled records validates infrastructure. Model training/evaluation should use gold-labeled high-confidence records only.",
            "model_input_boundary": "Only language, code_changed_files, code_diff_excerpt, and docs_before_excerpt are model-facing fields.",
        },
    }


def write_markdown_report(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# DocGuard Real Dataset Split Report",
        "",
        f"- Input: `{manifest['input']}`",
        f"- Output directory: `{manifest['output_dir']}`",
        f"- Split strategy: `{manifest['split_strategy']}`",
        f"- Split seed: `{manifest['split_seed']}`",
        f"- Total records: `{manifest['total_records']}`",
        f"- Repository overlap: `{manifest['repository_overlap']['has_repository_overlap']}`",
        "",
        "## Split Summary",
        "",
        "| Split | Records | Repositories | Languages | Candidate types | Label confidence |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]

    for split_name, summary in manifest["split_summary"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{split_name}`",
                    f"`{summary['records']}`",
                    f"`{summary['repositories']}`",
                    f"`{summary['languages']}`",
                    f"`{summary['candidate_types']}`",
                    f"`{summary['label_confidence']}`",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Repository Overlap",
            "",
            "```json",
            json.dumps(manifest["repository_overlap"], ensure_ascii=False, indent=2),
            "```",
            "",
            "## Interpretation Boundary",
            "",
            "- This script does not assign labels.",
            "- For final model training/evaluation, use only high-confidence gold-labeled records.",
            "- Repository-group split is preferred for the final locked test because it reduces repository-pattern leakage.",
            "- Random split may be used only for quick development diagnostics.",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Split DocGuard real PR datasets into train/validation/locked-test files.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--strategy", choices=["repository_group", "random"], default="repository_group")
    parser.add_argument("--fractions", default=None, help='Example: "train=0.7,validation=0.15,locked_test=0.15"')
    parser.add_argument("--prefix", default="real_pr")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    fractions = parse_split_fractions(args.fractions)

    rows = load_jsonl(input_path)
    splits = split_dataset(rows, seed=args.seed, strategy=args.strategy, fractions=fractions)

    output_dir.mkdir(parents=True, exist_ok=True)

    for split_name, split_rows in splits.items():
        write_jsonl(output_dir / f"{args.prefix}_{split_name}.jsonl", split_rows)

    manifest = build_manifest(
        input_path=input_path,
        output_dir=output_dir,
        splits=splits,
        seed=args.seed,
        strategy=args.strategy,
        fractions=fractions,
    )

    write_json(output_dir / f"{args.prefix}_split_manifest.json", manifest)
    write_markdown_report(output_dir / f"{args.prefix}_split_report.md", manifest)

    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())