"""Automated tests for the Iteration 1 MarkBridge prototype pipeline.

测试覆盖：AST 解析、往返保留标题文本、报告元数据、配置校验与 CLI 端到端流程。
Dialect adaptation rules are not tested here; they belong to later iterations.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from markbridge.pipeline import convert, PANDOC_VERSION
from markbridge.cli import main


FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_parse_ast_contains_blocks():
    """The parsed AST must contain non-empty top-level blocks. 解析后的 AST 必须含块。"""
    text = (FIXTURES / "commonmark_basic.md").read_text(encoding="utf-8")
    _, ast, report = convert(text, "commonmark", "commonmark")

    assert ast["blocks"], "AST blocks should not be empty."
    assert report.statistics["source_block_count"] == len(ast["blocks"])


def test_round_trip_preserves_heading_text():
    """A heading survives parse -> write round trip. 标题文本在往返后保留。"""
    text = "# Demo Title\n\nSome body text.\n"
    output, _, report = convert(text, "commonmark", "commonmark")

    assert "Demo Title" in output
    assert report.statistics["source_block_count"] >= 1


def test_report_records_pandoc_version_and_profiles():
    """Report metadata records Pandoc version and source/target profiles. 报告记录版本与配置。"""
    text = "# Sample\n"
    _, _, report = convert(text, "gfm", "commonmark")
    summary = report.summary()

    assert summary["pandoc_version"] == PANDOC_VERSION
    assert summary["source_profile"] == "gfm"
    assert summary["target_profile"] == "commonmark"
    assert summary["event_counts"].get("info", 0) >= 1


def test_unknown_profile_raises():
    """An unsupported profile must raise a clear ValueError. 不支持的配置应抛出明确错误。"""
    with pytest.raises(ValueError):
        convert("# X\n", "markdown-it", "commonmark")


def test_cli_end_to_end(tmp_path: Path):
    """CLI writes output Markdown, AST JSON and report files. CLI 端到端生成三类文件。"""
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
