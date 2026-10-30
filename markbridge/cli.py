"""MarkBridge command-line interface (Iteration 1 prototype).

Example:
    python -m markbridge.cli --input sample.md --from gfm --to commonmark \
        --output out.md --ast-out ast.json --report report.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .pipeline import convert
from .profiles import supported_profiles


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="markbridge",
        description="AST-based CommonMark <-> GFM conversion prototype.",
    )
    parser.add_argument("--input", required=True, help="Path to the source Markdown file.")
    parser.add_argument(
        "--output",
        help="Path where the converted Markdown file is written.",
    )
    parser.add_argument(
        "--from",
        dest="source",
        required=True,
        choices=supported_profiles(),
        help="Source Markdown profile.",
    )
    parser.add_argument(
        "--to",
        dest="target",
        required=True,
        choices=supported_profiles(),
        help="Target Markdown profile.",
    )
    parser.add_argument(
        "--policy",
        default="fallback",
        choices=["fallback", "approximate", "strict"],
        help="Downgrade policy (reserved for later iterations).",
    )
    parser.add_argument(
        "--ast-out",
        help="Optional path to save the Pandoc JSON AST.",
    )
    parser.add_argument(
        "--report",
        help="Optional path for the conversion report; .json suffix selects JSON output.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    """Execute the CLI workflow and return the exit code."""
    source_path = Path(args.input)
    if not source_path.exists():
        print(f"Error: input file not found: {source_path}", file=sys.stderr)
        return 1

    markdown_text = source_path.read_text(encoding="utf-8")

    # 为所有输出文件自动创建父目录；目录已存在时不报错，
    # 这样用户不需要先手动新建 output 文件夹。
    for output_path in (args.output, args.ast_out, args.report):
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    output, ast, report = convert(
        markdown_text,
        source_profile=args.source,
        target_profile=args.target,
        policy=args.policy,
    )

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Converted Markdown written to: {args.output}")

    if args.ast_out:
        import json

        Path(args.ast_out).write_text(
            json.dumps(ast, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"AST JSON written to: {args.ast_out}")

    if args.report:
        report_text = report.to_json() if args.report.endswith(".json") else report.to_text()
        Path(args.report).write_text(report_text, encoding="utf-8")
        print(f"Conversion report written to: {args.report}")

    # Print a short human-readable summary to the terminal as well.
    print("\n" + report.to_text())
    return 0


def main(argv: list[str] | None = None) -> int:
    """Entry point used by `python -m markbridge.cli`."""
    args = build_parser().parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
