"""MarkBridge: AST-based CommonMark <-> GFM conversion pipeline.

Iteration 1 scope: parse Markdown into the Pandoc JSON AST, serialise it back,
and record diagnostics. Dialect-specific adaptation rules are added in later
iterations.
"""

__version__ = "0.1.0"
