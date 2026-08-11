from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_patch_backend_comparison_skips_hf_without_flag(tmp_path: Path) -> None:
    output_dir = tmp_path / "comparison"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/compare_patch_backends.py",
            "--case-limit",
            "2",
            "--hf-model",
            "fake/model",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    report = output_dir / "docguard_patch_backend_comparison_2026_08.md"
    assert result.returncode == 0
    assert report.exists()
    text = report.read_text(encoding="utf-8")
    assert "HF backend was not run" in text
    assert not (output_dir / "llm_hf").exists()


def test_patch_backend_comparison_without_hf_writes_quality_columns(tmp_path: Path) -> None:
    output_dir = tmp_path / "comparison"
    subprocess.run(
        [sys.executable, "scripts/compare_patch_backends.py", "--case-limit", "2", "--output-dir", str(output_dir)],
        check=True,
        capture_output=True,
        text=True,
    )
    text = (output_dir / "docguard_patch_backend_comparison_2026_08.md").read_text(encoding="utf-8")
    assert "Quality" in text
    assert "Groundedness" in text
    assert "Hallucination risk" in text
