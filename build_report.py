# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = Document()

THEME_ATTRS = ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme")

def force_arial(style):
    """Force Arial on a style and remove theme-font selectors that shadow it.

    强制样式使用 Arial，并删除会遮蔽显式字体的主题字体属性。
    """
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in THEME_ATTRS:
        if rfonts.get(qn(attr)) is not None:
            del rfonts.attrib[qn(attr)]
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Arial")

# Base font: Arial 10 for normal text, Arial for headings.
normal = doc.styles["Normal"]
force_arial(normal)
normal.font.size = Pt(10)

for name in ("Heading 1", "Heading 2", "Title"):
    st = doc.styles[name]
    force_arial(st)
    st.font.color.rgb = RGBColor(0x1F, 0x33, 0x4E)

def h1(text):
    p = doc.add_heading(text, level=1)
    p.runs[0].font.size = Pt(14)
    return p

def h2(text):
    p = doc.add_heading(text, level=2)
    p.runs[0].font.size = Pt(11)
    return p

def body(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(4)
    return p

def bullet(text):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    return p

# ---- Title block ----
title = doc.add_heading("MarkBridge — First Iteration Report", level=0)
title.runs[0].font.size = Pt(18)
title.runs[0].font.color.rgb = RGBColor(0x1F, 0x33, 0x4E)
body("AST-based conversion between CommonMark and GitHub Flavoured Markdown (GFM)")
body("Student: Xinyu Jia  |  Student ID: C00304524  |  Supervisor: Tom Corcoran  |  Pandoc version: 3.9")

h2("1. What was planned")
bullet("Set up the Python project structure and dependency environment, and pin the Pandoc version.")
bullet("Establish the prototype pipeline: Markdown -> Pandoc JSON AST -> Markdown.")
bullet("Define CommonMark and GFM profiles with explicit reader/writer settings.")
bullet("Build a diagnostic report schema, prepare Markdown fixtures and write an automated test suite.")

h2("2. What work was completed")
bullet("Project structure created: markbridge package, fixtures, tests and docs directories.")
bullet("pipeline.py implements parse_to_ast, ast_to_markdown and convert using pypandoc with bundled Pandoc 3.9.")
bullet("profiles.py defines commonmark and gfm profiles; diagnostics.py records events and emits text/JSON reports.")
bullet("cli.py supports --input, --from, --to, --output, --ast-out, --report and --policy.")
bullet("Two fixtures (CommonMark and GFM) and five automated tests, all passing; the CLI end-to-end run was verified.")
bullet("README, pinned requirements, feature matrix and .gitignore completed.")

h2("3. What worked")
bullet("pypandoc-binary supplied a reproducible Pandoc 3.9 without a separate system installation.")
bullet("The JSON AST acts as a stable process boundary; the parse/serialise round trip works correctly.")
bullet("pytest gives fast feedback, and the end-to-end CLI test confirms output, AST and report files are written.")

h2("4. What did not work / observed limitations")
bullet("The machine initially had no Pandoc, pytest or panflute, so these dependencies had to be installed first.")
bullet("The prototype does not yet apply dialect adaptation rules. A direct GFM-to-CommonMark write shows Pandoc's default fallback: strikethrough becomes <s> HTML, task boxes become glyphs and tables become HTML tables. This is the problem later iterations will address.")

h2("5. Problems encountered")
bullet("Pandoc was not installed; resolved by using the bundled binary through pypandoc-binary.")
bullet("Missing pytest and panflute; installed via pip with versions recorded in requirements.txt.")
bullet("Understanding AST node forms; inspected real Pandoc JSON AST produced from the fixtures.")

h2("6. Changes made")
bullet("Used bundled Pandoc through pypandoc-binary rather than assuming a system installation; panflute is retained for later rule work.")
bullet("Kept Iteration 1 to the parse/write prototype and deferred dialect rules according to the plan.")

h2("7. What is planned for the next iteration")
bullet("Implement AST adaptation rules for task lists and strikethrough.")
bullet("Add the first configurable downgrade policy and expand diagnostics with fallback and loss events.")
bullet("Add unit tests covering the new rules and nested cases.")

h2("References")
body("CommonMark. (2022) CommonMark Specification 0.30. Available at: https://spec.commonmark.org/0.30/ (Accessed: 30 October 2026).")
body("GitHub. (n.d.) GitHub Flavoured Markdown Spec. Available at: https://github.github.com/gfm/ (Accessed: 30 October 2026).")
body("Krewinkel, A. (n.d.) Panflute: Pythonic Pandoc Filters. Available at: https://panflute.readthedocs.io/ (Accessed: 30 October 2026).")
body("MacFarlane, J. (n.d.) Pandoc User's Guide. Available at: https://pandoc.org/MANUAL.html (Accessed: 30 October 2026).")

h2("AI usage statement")
body("AI tools were used only for drafting, proofreading and conceptual explanation. All design decisions and code were reviewed, understood and tested by the student, in accordance with course rules. No unexplained black-box code was included.")

out = r"C:\Users\jxy2004\Doubao\chats\2026-10-30\new-chat\MarkBridge\docs\First_Iteration_Report.docx"
doc.save(out)
print("saved", out)
