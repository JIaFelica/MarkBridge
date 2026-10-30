"""Core MarkBridge pipeline (Iteration 1 prototype).

Flow for this iteration:
    Markdown text -> Pandoc JSON AST -> Pandoc writer -> Markdown text

Dialect adaptation rules (task lists, tables, strikethrough, autolinks) are
not applied yet; they are implemented in Iteration 2 and 3. This prototype
establishes the parse / AST / write boundary, records Pandoc metadata and
structural statistics, and produces the conversion report.

本迭代流程：Markdown 文本 -> Pandoc JSON AST -> Pandoc writer -> Markdown 文本。
方言转换规则尚未接入（留待第 2、3 轮）；本原型先打通解析 / AST / 回写边界，
记录 Pandoc 元数据、结构统计并生成转换报告。
"""

from __future__ import annotations

import json
from typing import Any

import pypandoc

from .profiles import get_profile
from .diagnostics import ConversionReport, LEVEL_INFO

# Pin and expose the Pandoc version used by this environment.
# 记录当前环境使用的 Pandoc 版本，便于规格书与报告锁定版本。
PANDOC_VERSION = pypandoc.get_pandoc_version()


def parse_to_ast(markdown_text: str, source_profile: str, report: ConversionReport) -> dict[str, Any]:
    """Parse Markdown into the Pandoc JSON AST.

    用源配置对应的 reader 把 Markdown 解析为 Pandoc JSON AST（字典形式）。
    """
    profile = get_profile(source_profile)
    report.add(
        stage="parsing",
        message=f"Parsing input with reader '{profile.reader}'.",
        level=LEVEL_INFO,
    )

    ast_json = pypandoc.convert_text(
        markdown_text,
        to="json",
        format=profile.reader,
    )
    ast: dict[str, Any] = json.loads(ast_json)

    block_count = len(ast.get("blocks", []))
    report.set_statistic("source_block_count", block_count)
    report.add(
        stage="parsing",
        message=f"AST contains {block_count} top-level block(s).",
        level=LEVEL_INFO,
    )
    return ast


def ast_to_markdown(ast: dict[str, Any], target_profile: str, report: ConversionReport) -> str:
    """Serialise the AST back into target-profile Markdown.

    用目标配置对应的 writer 把 AST 回写为目标方言的 Markdown。
    """
    profile = get_profile(target_profile)
    report.add(
        stage="writing",
        message=f"Serialising AST with writer '{profile.writer}'.",
        level=LEVEL_INFO,
    )

    ast_json = json.dumps(ast, ensure_ascii=False)
    output = pypandoc.convert_text(ast_json, to=profile.writer, format="json")
    report.set_statistic("target_block_count", len(ast.get("blocks", [])))
    return output


def convert(
    markdown_text: str,
    source_profile: str,
    target_profile: str,
    policy: str = "fallback",
) -> tuple[str, dict[str, Any], ConversionReport]:
    """Run the prototype pipeline and return output Markdown, AST and report.

    运行原型管线，返回转换后的 Markdown、AST 字典与转换报告。
    Iteration 1: no dialect rules are applied yet; the AST is parsed and written
    through the selected readers/writers.
    """
    source = get_profile(source_profile)
    target = get_profile(target_profile)

    report = ConversionReport(
        source_profile=source.key,
        target_profile=target.key,
        pandoc_version=PANDOC_VERSION,
    )
    report.add(
        stage="configuration",
        message=f"Source='{source.key}', target='{target.key}', policy='{policy}'.",
        level=LEVEL_INFO,
    )
    report.add(
        stage="configuration",
        message="Prototype pipeline: dialect adaptation rules are deferred to later iterations.",
        level=LEVEL_INFO,
    )

    ast = parse_to_ast(markdown_text, source.key, report)
    output = ast_to_markdown(ast, target.key, report)

    report.add(
        stage="complete",
        message="Prototype parse/write cycle finished.",
        level=LEVEL_INFO,
    )
    return output, ast, report
