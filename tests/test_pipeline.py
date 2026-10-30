"""Automated tests for the Iteration 1 MarkBridge prototype pipeline.

Covers AST parsing, heading preservation on round trip, report metadata,
profile validation and the CLI end-to-end flow. Dialect adaptation rules are
not tested here; they belong to later iterations.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from markbridge.pipeline import convert, PANDOC_VERSION
from markbridge.cli import main


FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_parse_ast_contains_blocks():
    """The parsed AST must contain non-empty top-level blocks."""
    text = (FIXTURES / "commonmark_basic.md").read_text(encoding="utf-8")
    _, ast, report = convert(text, "commonmark", "commonmark")

    assert ast["blocks"], "AST blocks should not be empty."
    assert report.statistics["source_block_count"] == len(ast["blocks"])


def test_round_trip_preserves_heading_text():
    """A heading survives the parse -> write round trip."""
    text = "# Demo Title\n\nSome body text.\n"
    output, _, report = convert(text, "commonmark", "commonmark")

    assert "Demo Title" in output
    assert report.statistics["source_block_count"] >= 1


def test_report_records_pandoc_version_and_profiles():
    """Report metadata records the Pandoc version and source/target profiles."""
    text = "# Sample\n"
    _, _, report = convert(text, "gfm", "commonmark")
    summary = report.summary()

    assert summary["pandoc_version"] == PANDOC_VERSION
    assert summary["source_profile"] == "gfm"
    assert summary["target_profile"] == "commonmark"
    assert summary["event_counts"].get("info", 0) >= 1


def test_unknown_profile_raises():
    """An unsupported profile must raise a clear ValueError."""
    with pytest.raises(ValueError):
        convert("# X\n", "markdown-it", "commonmark")


def test_cli_end_to_end(tmp_path: Path):
    """CLI writes the output Markdown, AST JSON and report files."""
    input_file = tmp_path / "input.md"
    output_file = tmp_path / "output.md"
    ast_file = tmp_path / "ast.json"
    report_file = tmp_path / "report.json"

    input_file.write_text("# CLI Demo\n\nBody paragraph.\n", encoding="utf-8")

    exit_code = main(
        [
            "--input", str(input_file),
            "--output", str(output_file),
            "--from", "commonmark",
            "--to", "commonmark",
            "--ast-out", str(ast_file),
            "--report", str(report_file),
        ]
    )

    assert exit_code == 0
    assert output_file.exists() and "CLI Demo" in output_file.read_text(encoding="utf-8")
    assert ast_file.exists()
    assert report_file.exists()

    report_text = report_file.read_text(encoding="utf-8")
    assert PANDOC_VERSION in report_text
