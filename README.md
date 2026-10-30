# MarkBridge

AST-based bidirectional conversion between CommonMark and GitHub Flavoured Markdown (GFM).

MarkBridge uses Pandoc to parse Markdown into a structured **Abstract Syntax Tree (AST)**, applies explicit AST-level adaptation rules, and serialises the result in the target Markdown profile. Conversions operate on semantic AST nodes rather than raw string replacement, so document structure and content are preserved while syntax differences between Markdown flavours are handled.

## Iteration 1 status

This iteration establishes the foundation and prototype pipeline:

- Parse Markdown into the Pandoc JSON AST (CommonMark and GFM readers).
- Serialise the AST back into Markdown through the selected writer.
- Record Pandoc version, source/target profiles, structural statistics and diagnostic events.
- Automated pytest suite covering parsing, round-trip behaviour, report metadata and the CLI.

Dialect adaptation rules (task lists, tables, strikethrough, autolinks) are added in later iterations.

## Requirements

- Python 3.10+
- Pandoc is provided through the `pypandoc-binary` package (no separate system installation required).
- See `requirements.txt` for pinned dependency versions.

## Installation

Install the pinned dependencies:

```bash
python -m pip install -r requirements.txt
```

On Windows, if `python` opens the Microsoft Store or returns no output, use the Python launcher (`py`) instead:

```powershell
py -m pip install -r requirements.txt
```

## Usage

Run the command-line prototype from the project root:

```bash
python -m markbridge.cli --input fixtures/gfm_basic.md --from gfm --to commonmark --output output/output.md --ast-out output/ast.json --report output/report.json
```

Windows equivalent with the Python launcher:

```powershell
New-Item -ItemType Directory -Force -Path output
py -m markbridge.cli --input fixtures/gfm_basic.md --from gfm --to commonmark --output output/output.md --ast-out output/ast.json --report output/report.json
```

CLI options:

- `--input`: path to the source Markdown file.
- `--from`: source profile (`commonmark` or `gfm`).
- `--to`: target profile (`commonmark` or `gfm`).
- `--output`: path for the converted Markdown file.
- `--ast-out`: optional path to save the Pandoc JSON AST.
- `--report`: optional path for the conversion report (`.json` suffix selects JSON output).
- `--policy`: downgrade policy placeholder (`fallback`, `approximate`, `strict`).

## Running the tests

```bash
python -m pytest
```

Windows equivalent:

```powershell
py -m pytest
```

## Project structure

```
MarkBridge/
├── markbridge/
│   ├── __init__.py
│   ├── profiles.py        # Markdown profiles and reader/writer settings
│   ├── diagnostics.py     # Diagnostic events and conversion report
│   ├── pipeline.py        # Markdown -> AST -> Markdown pipeline
│   └── cli.py             # Command-line interface
├── fixtures/              # Curated CommonMark and GFM sample documents
├── tests/                 # Automated pytest suite
├── docs/                  # Feature matrix and supporting documentation
├── requirements.txt
└── README.md
```

## Iteration roadmap

1. **Iteration 1** – Analysis and prototype: parse-to-JSON and JSON-to-output pipeline.
2. **Iteration 2** – Core rules: task-list and strikethrough handling, diagnostics, unit tests.
3. **Iteration 3** – Required coverage: table and autolink rules, fallbacks and reports.
4. **Iteration 4** – Evaluation and release: regression/round-trip tests, baseline comparison, final release.

## References and AI usage

External sources are listed in the project specification and iteration report. AI tools are used only for drafting, proofreading and conceptual explanation; all design decisions and code are reviewed, understood and tested by the student.
