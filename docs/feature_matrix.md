# Feature Matrix

Supported and planned Markdown features across the four iterations. The Pandoc version used for this project is recorded in the conversion report and pinned through `pypandoc-binary`.

| Feature / capability | Iteration 1 | Iteration 2 | Iteration 3 | Iteration 4 |
| -------------------- | ----------- | ----------- | ----------- | ----------- |
| Markdown -> Pandoc JSON AST parse | Done | - | - | - |
| AST -> Markdown serialise | Done | - | - | - |
| Pandoc version / profile metadata in report | Done | - | - | - |
| Diagnostic event schema | Done | Extended | Extended | Extended |
| Task-list adaptation | - | Planned | - | - |
| Strikethrough adaptation | - | Planned | - | - |
| Pipe-table adaptation | - | - | Planned | - |
| Autolink adaptation | - | - | Planned | - |
| Configurable downgrade policies | Placeholder | Partial | Full | - |
| Unit / integration / regression tests | Unit | Expanded | Expanded | Full |
| Round-trip tests | Basic | Expanded | Expanded | Full |
| Direct Pandoc baseline comparison | - | - | - | Planned |
| Additional dialect / UI (optional) | - | - | - | Optional |

## Notes

- Iteration 1 is a prototype: it establishes the parse / AST / write boundary and diagnostics but does not yet apply dialect-specific adaptation rules.
- The GFM fixture already contains task lists, tables, strikethrough and autolinks so that later iterations can build rules against real Pandoc AST structures.
- Byte-identical round trips are not guaranteed; Pandoc writers normalise whitespace, list markers and escaping.
