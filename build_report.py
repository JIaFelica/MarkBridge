"""Build the MarkBridge First Iteration Report.

Reproduces docs/First_Iteration_Report.docx: page geometry, margins, fonts,
sizes, colours, table shading, row heights, bullets and hyperlink fields.
Usage: py build_report.py [output.docx]
"""
import os
import sys
from datetime import datetime

from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from lxml import etree

PANDOC_VERSION = "3.13"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Half-point sizes used in the submitted report.
SZ_BODY = "22"      # 11 pt
SZ_HEADING = "26"   # 13 pt
SZ_TITLE = "36"     # 18 pt
SZ_SMALL = "20"     # 10 pt

BODY_AFTER = "80"    # 4 pt
BLANK_AFTER = "40"   # 2 pt
NAVY = "1F334E"
LINK = "1155CC"
HEADER_FILL = "C7DAF1"

ARIAL = {"ascii": "Arial", "hAnsi": "Arial", "eastAsia": "Arial", "cs": "Arial"}
RTX = {"val": "0"}


def w(tag):
    return "{%s}%s" % (W, tag)


def sub(parent, tag, attrs=None, text=None):
    """Append a WordprocessingML child with optional attributes and text."""
    e = etree.SubElement(parent, w(tag))
    for key, value in (attrs or {}).items():
        e.set(w(key), value)
    if text is not None:
        e.text = text
    return e


def build_rpr(parent, items):
    """Build a w:rPr element from an ordered list of (tag, attrs) pairs."""
    rpr = sub(parent, "rPr")
    for tag, attrs in items:
        sub(rpr, tag, attrs)
    return rpr


RPR_TEXT = [("sz", {"val": SZ_BODY}), ("szCs", {"val": SZ_BODY}), ("rtl", RTX)]
RPR_LEAD = [("b", {}), ("bCs", {})] + RPR_TEXT
RPR_HEADING = [("rFonts", ARIAL), ("sz", {"val": SZ_HEADING}),
               ("szCs", {"val": SZ_HEADING}), ("rtl", RTX)]
RPR_TITLE = [("color", {"val": NAVY}), ("sz", {"val": SZ_TITLE}),
             ("szCs", {"val": SZ_TITLE}), ("rtl", RTX)]
RPR_PLAIN = [("rtl", RTX)]
RPR_LIST = [("rFonts", ARIAL), ("b", {"val": "0"}), ("bCs", {"val": "0"}),
            ("i", {"val": "0"}), ("iCs", {"val": "0"}),
            ("smallCaps", {"val": "0"}), ("strike", {"val": "0"}),
            ("color", {"val": "000000"}), ("sz", {"val": SZ_BODY}),
            ("szCs", {"val": SZ_BODY}), ("u", {"val": "none"}),
            ("shd", {"val": "clear", "fill": "auto"}),
            ("vertAlign", {"val": "baseline"}), ("rtl", RTX)]
RPR_LINK = [("color", {"val": LINK}), ("sz", {"val": SZ_BODY}),
            ("szCs", {"val": SZ_BODY}), ("u", {"val": "single"}), ("rtl", RTX)]
RPR_TBL_HEAD = [("rFonts", ARIAL), ("b", {}), ("bCs", {}),
                ("sz", {"val": SZ_BODY}), ("szCs", {"val": SZ_BODY}), ("rtl", RTX)]
RPR_TBL_BODY = [("rFonts", ARIAL), ("sz", {"val": SZ_BODY}),
                ("szCs", {"val": SZ_BODY}), ("rtl", RTX)]
RPR_MARK = [("sz", {"val": SZ_BODY}), ("szCs", {"val": SZ_BODY})]
RPR_HEADING_MARK = [("rFonts", ARIAL), ("sz", {"val": SZ_HEADING}),
                    ("szCs", {"val": SZ_HEADING}), ("rtl", RTX)]

doc = Document()
body = doc.element.body


# --------------------------------------------------------------------------
# Styles: the three styles the report relies on.
# --------------------------------------------------------------------------
def set_style_rpr(style, items):
    element = style.element
    for existing in element.findall(w("rPr")):
        element.remove(existing)
    ppr = element.find(w("pPr"))
    rpr = etree.SubElement(element, w("rPr"))
    for tag, attrs in items:
        sub(rpr, tag, attrs)
    if ppr is not None:
        ppr.addnext(rpr)
    else:
        element.append(rpr)


def set_style_ppr(style, xml_fragment):
    element = style.element
    for existing in element.findall(w("pPr")):
        element.remove(existing)
    ppr = parse_xml(xml_fragment)
    rpr = element.find(w("rPr"))
    if rpr is not None:
        rpr.addprevious(ppr)
    else:
        element.append(ppr)


def set_doc_defaults():
    defaults = doc.styles.element.find(w("docDefaults"))
    rpr_default = defaults.find(w("rPrDefault"))
    for existing in rpr_default.findall(w("rPr")):
        rpr_default.remove(existing)
    rpr = etree.SubElement(rpr_default, w("rPr"))
    sub(rpr, "rFonts", ARIAL)


# Word spells these style ids differently, but they are the ids the submitted
# report references; keeping them makes the two files line up one to one.
STYLE_IDS = {"Normal": "1", "Heading 2": "3", "Title": "10"}
for style_name, style_identifier in STYLE_IDS.items():
    doc.styles[style_name].element.set(qn("w:styleId"), style_identifier)

set_doc_defaults()

normal = doc.styles["Normal"]
set_style_ppr(normal, '<w:pPr %s><w:spacing w:after="200" w:line="276" w:lineRule="auto"/></w:pPr>' % nsdecls("w"))
set_style_rpr(normal, [("rFonts", ARIAL), ("lang", {"val": "en"})])

title = doc.styles["Title"]
set_style_ppr(title, (
    '<w:pPr %s><w:pBdr><w:bottom w:val="single" w:color="4F81BD" w:sz="8" w:space="4"/></w:pBdr>'
    '<w:spacing w:after="300" w:line="240" w:lineRule="auto"/></w:pPr>' % nsdecls("w")))
set_style_rpr(title, [("rFonts", ARIAL), ("color", {"val": NAVY}),
                      ("sz", {"val": "52"}), ("szCs", {"val": "52"})])

heading2 = doc.styles["Heading 2"]
set_style_ppr(heading2, (
    '<w:pPr %s><w:keepNext/><w:keepLines/>'
    '<w:spacing w:before="200" w:after="0"/></w:pPr>' % nsdecls("w")))
set_style_rpr(heading2, [("rFonts", ARIAL), ("b", {}), ("bCs", {}),
                         ("color", {"val": NAVY}),
                         ("sz", {"val": SZ_HEADING}), ("szCs", {"val": SZ_HEADING})])


def add_table_style(table_style_id, style_label):
    """Register the minimal table style the report's tables reference."""
    styles_el = doc.styles.element
    element = etree.SubElement(styles_el, w("style"))
    element.set(w("type"), "table")
    element.set(w("customStyle"), "1")
    element.set(w("styleId"), table_style_id)
    sub(element, "name", {"val": style_label})
    sub(element, "basedOn", {"val": "TableGrid"})
    sub(element, "qFormat")
    sub(element, "uiPriority", {"val": "0"})
    ppr = sub(element, "pPr")
    sub(ppr, "spacing", {"after": "0", "line": "240", "lineRule": "auto"})
    tbl_pr = sub(element, "tblPr")
    margins = sub(tbl_pr, "tblCellMar")
    sub(margins, "top", {"w": "0", "type": "dxa"})
    sub(margins, "left", {"w": "108", "type": "dxa"})
    sub(margins, "bottom", {"w": "0", "type": "dxa"})
    sub(margins, "right", {"w": "108", "type": "dxa"})


add_table_style("14", "_Style 11")
add_table_style("15", "_Style 12")


# --------------------------------------------------------------------------
# Page setup.
# --------------------------------------------------------------------------
# Section geometry is written straight into sectPr, so the page size, margins,
# numbering start and column settings match the submitted report exactly.
sect_pr = body.find(w("sectPr"))
for child in list(sect_pr):
    sect_pr.remove(child)
sub(sect_pr, "pgSz", {"w": "12240", "h": "15840"})
sub(sect_pr, "pgMar", {"top": "1440", "right": "1247", "bottom": "1440",
                       "left": "1247", "header": "720", "footer": "720", "gutter": "0"})
sub(sect_pr, "pgNumType", {"start": "1"})
sub(sect_pr, "cols", {"space": "720", "num": "1"})


# --------------------------------------------------------------------------
# Bullet numbering for the plan list (one level, circular bullet).
# --------------------------------------------------------------------------
numbering = doc.part.numbering_part.element
NUM_ID = "1"
abstract = etree.SubElement(numbering, w("abstractNum"))
abstract.set(w("abstractNumId"), "100")
first_num = numbering.find(w("num"))
if first_num is not None:
    first_num.addprevious(abstract)
sub(abstract, "multiLevelType", {"val": "singleLevel"})
lvl = sub(abstract, "lvl", {"ilvl": "0"})
sub(lvl, "start", {"val": "1"})
sub(lvl, "numFmt", {"val": "bullet"})
sub(lvl, "lvlText", {"val": "\u25cf"})
sub(lvl, "lvlJc", {"val": "left"})
lvl_ppr = sub(lvl, "pPr")
sub(lvl_ppr, "ind", {"left": "360", "hanging": "360"})
num = None
for candidate in numbering.findall(w("num")):
    if candidate.get(w("numId")) == NUM_ID:
        num = candidate
        break
if num is None:
    num = etree.SubElement(numbering, w("num"))
    num.set(w("numId"), NUM_ID)
for existing in num.findall(w("abstractNumId")):
    num.remove(existing)
sub(num, "abstractNumId", {"val": "100"})


# --------------------------------------------------------------------------
# Paragraph and run helpers.
# --------------------------------------------------------------------------
def new_para(ppr_items):
    """Append a paragraph whose pPr is built from the given ordered items."""
    p = etree.SubElement(body, w("p"))
    ppr = etree.SubElement(p, w("pPr"))
    for tag, attrs in ppr_items:
        sub(ppr, tag, attrs)
    return p, ppr


def add_run(p, rpr_items, text):
    r = sub(p, "r")
    if rpr_items is not None:
        build_rpr(r, rpr_items)
    sub(r, "t", text=text)
    return r


def add_field_run(p, kind, rpr_items):
    """Field character or instruction run used for the hyperlink fields."""
    r = sub(p, "r")
    build_rpr(r, rpr_items or RPR_TEXT[:2])
    if kind == "begin":
        sub(r, "fldChar", {"fldCharType": "begin"})
    elif kind == "separate":
        sub(r, "fldChar", {"fldCharType": "separate"})
    elif kind == "end":
        sub(r, "fldChar", {"fldCharType": "end"})
    return r


def add_instr(p, instruction):
    r = sub(p, "r")
    build_rpr(r, RPR_TEXT[:2])
    instr = sub(r, "instrText")
    instr.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    instr.text = " %s " % instruction
    return r


def heading(text):
    p, ppr = new_para([("pStyle", {"val": "3"})])
    mark = sub(ppr, "rPr")
    for tag, attrs in RPR_HEADING_MARK:
        sub(mark, tag, attrs)
    add_run(p, RPR_HEADING, text)
    return p


def para(text, lead=None):
    """A body paragraph, 11 pt; an optional lead-in phrase is set in bold."""
    p, ppr = new_para([("spacing", {"after": BODY_AFTER})])
    mark = sub(ppr, "rPr")
    for tag, attrs in RPR_MARK:
        sub(mark, tag, attrs)
    if lead:
        add_run(p, RPR_LEAD, lead)
    add_run(p, RPR_TEXT, text)
    return p


def header_line(text):
    """A cover line: 10 pt and no colour, inherited from the document default."""
    p, _ = new_para([("spacing", {"after": BODY_AFTER})])
    add_run(p, RPR_PLAIN, text)
    return p


def blank():
    """The empty 2 pt paragraph that follows each table."""
    p, _ = new_para([("spacing", {"after": BLANK_AFTER})])
    return p


def bullet(text, after="0", tail=None):
    ppr_items = [
        ("keepNext", {"val": "0"}),
        ("keepLines", {"val": "0"}),
        ("pageBreakBefore", {"val": "0"}),
        ("widowControl", {}),
        ("numPr", None),
        ("pBdr", None),
        ("shd", {"val": "clear", "fill": "auto"}),
        ("spacing", {"before": "0", "after": after, "line": "276", "lineRule": "auto"}),
        ("ind", {"left": "360", "right": "0", "hanging": "360"}),
        ("jc", {"val": "left"}),
        ("rPr", None),
    ]
    p = etree.SubElement(body, w("p"))
    ppr = etree.SubElement(p, w("pPr"))
    for tag, attrs in ppr_items:
        if tag == "numPr":
            num_pr = sub(ppr, "numPr")
            sub(num_pr, "ilvl", {"val": "0"})
            sub(num_pr, "numId", {"val": NUM_ID})
        elif tag == "pBdr":
            bdr = sub(ppr, "pBdr")
            for side in ("top", "left", "bottom", "right", "between"):
                sub(bdr, side, {"val": "none", "color": "auto", "sz": "0", "space": "0"})
        elif tag == "rPr":
            if after != BLANK_AFTER:
                mark = sub(ppr, "rPr")
                for t, a in RPR_MARK:
                    sub(mark, t, a)
        else:
            sub(ppr, tag, attrs)
    add_run(p, RPR_LIST, text)
    if tail:
        add_run(p, RPR_LIST_SHORT, tail)
    return p


RPR_LIST_SHORT = [("rFonts", ARIAL), ("b", {"val": "0"}), ("bCs", {"val": "0"}),
                  ("i", {"val": "0"}), ("iCs", {"val": "0"}),
                  ("smallCaps", {"val": "0"}), ("strike", {"val": "0"}),
                  ("color", {"val": "000000"}), ("sz", {"val": SZ_SMALL}),
                  ("szCs", {"val": SZ_SMALL}), ("u", {"val": "none"}),
                  ("shd", {"val": "clear", "fill": "auto"}),
                  ("vertAlign", {"val": "baseline"}), ("rtl", RTX)]


def reference(text, target, display, tail):
    """Reference paragraph with a HYPERLINK field around the URL.

    ``display`` may be a list of strings so the link can keep the leading
    space and the URL in separate runs, as in the submitted report.
    """
    p, ppr = new_para([("spacing", {"after": BODY_AFTER})])
    mark = sub(ppr, "rPr")
    for tag, attrs in RPR_MARK:
        sub(mark, tag, attrs)
    add_run(p, RPR_TEXT, text)
    add_field_run(p, "begin", None)
    add_instr(p, 'HYPERLINK "%s"' % target)
    add_field_run(p, "separate", None)
    for part in (display if isinstance(display, (list, tuple)) else [display]):
        add_run(p, RPR_LINK, part)
    add_field_run(p, "end", RPR_LINK)
    add_run(p, RPR_TEXT, tail)
    return p


BORDER = {"val": "single", "color": "000000", "sz": "4", "space": "0"}


RPR_TBL_HEAD_BOTTOM = [("rFonts", ARIAL), ("b", {}), ("bCs", {}),
                       ("color", {"val": "auto"}), ("sz", {"val": SZ_BODY}),
                       ("szCs", {"val": SZ_BODY}), ("rtl", RTX)]


def table(grid, rows, header_valign="center", header_after="20",
          header_line="240", table_style_id="14", header_rpr=RPR_TBL_HEAD):
    """Two-column table built to the submitted report's exact geometry."""
    tbl = etree.SubElement(body, w("tbl"))
    tbl_pr = sub(tbl, "tblPr")
    sub(tbl_pr, "tblStyle", {"val": table_style_id})
    sub(tbl_pr, "tblW", {"w": str(sum(grid)), "type": "dxa"})
    # Centre the table between the left and right margins.
    sub(tbl_pr, "jc", {"val": "center"})
    sub(tbl_pr, "tblInd", {"w": "0", "type": "dxa"})
    borders = sub(tbl_pr, "tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        sub(borders, side, BORDER)
    sub(tbl_pr, "tblLayout", {"type": "fixed"})
    margins = sub(tbl_pr, "tblCellMar")
    sub(margins, "top", {"w": "0", "type": "dxa"})
    sub(margins, "left", {"w": "108", "type": "dxa"})
    sub(margins, "bottom", {"w": "0", "type": "dxa"})
    sub(margins, "right", {"w": "108", "type": "dxa"})

    grid_el = sub(tbl, "tblGrid")
    for width in grid:
        sub(grid_el, "gridCol", {"w": str(width)})

    header_rpr = header_rpr or RPR_TBL_HEAD
    for index, row in enumerate(rows):
        tr = sub(tbl, "tr")
        tr_pr = sub(tr, "trPr")
        if row["height"]:
            sub(tr_pr, "trHeight", {"val": str(row["height"]), "hRule": "atLeast"})
        if index == 0:
            sub(tr_pr, "tblHeader")
        for col, text in enumerate(row["cells"]):
            tc = sub(tr, "tc")
            tc_pr = sub(tc, "tcPr")
            if index == 0:
                sub(tc_pr, "shd", {"val": "clear", "color": "auto", "fill": HEADER_FILL,
                                   "themeFill": "text2", "themeFillTint": "32"})
            sub(tc_pr, "vAlign", {"val": header_valign if index == 0 else "center"})
            p = sub(tc, "p")
            ppr = sub(p, "pPr")
            if index == 0 and header_line:
                sub(ppr, "spacing", {"after": header_after, "line": header_line,
                                     "lineRule": "auto"})
            elif index == 0:
                sub(ppr, "spacing", {"after": header_after})
            else:
                sub(ppr, "spacing", {"after": "20", "line": "240", "lineRule": "auto"})
            # Header cells are centred; body rows centre the left column and
            # justify the right column.
            sub(ppr, "jc", {"val": "center" if (index == 0 or col == 0) else "both"})
            mark = sub(ppr, "rPr")
            if index == 0 and header_valign == "bottom":
                for tag, attrs in RPR_TBL_HEAD_BOTTOM[:-1]:
                    sub(mark, tag, attrs)
            else:
                for tag, attrs in RPR_MARK:
                    sub(mark, tag, attrs)
            add_run(p, header_rpr if index == 0 else RPR_TBL_BODY, text)
    return tbl


# --------------------------------------------------------------------------
# Document content.
# --------------------------------------------------------------------------
def title_block():
    p, _ = new_para([("pStyle", {"val": "10"})])
    add_run(p, RPR_TITLE, "MarkBridge \u2014 First Iteration Report")


def header_lines():
    header_line("AST-based conversion between CommonMark and GitHub Flavoured Markdown (GFM)")
    header_line("Student: Xinyu Jia  |  Student ID: C00304524  |  "
                "Supervisor: Tom Corcoran  |  Pandoc version: " + PANDOC_VERSION)
    header_line("Iteration period: Iteration 1 ")


title_block()
header_lines()

heading("1. Iteration goal")
para('The goal of Iteration 1 ("Analysis and prototype" in the specification work plan) '
     "was to establish a runnable conversion pipeline and to check the core design "
     "assumption that the Pandoc JSON AST can serve as the process boundary. This iteration "
     "set up the Python project and dependency environment, pinned the Pandoc version for "
     "reproducibility, implemented parsing and serialisation for the CommonMark and GFM "
     "profiles, and added a diagnostic report and an automated test foundation.")
para("Dialect adaptation rules (task lists, strikethrough, tables and autolinks) were "
     "deliberately not implemented. They are the core-rule work of Iterations 2 and 3 "
     "(specification Section 9). Iteration 1 delivers only the parsing-and-serialisation "
     "prototype, which gives the rule layer a stable base.")
para("the pipeline runs end to end, the AST process boundary works for the tested "
     "documents, and results are reproducible through a pinned Pandoc version. Policy "
     "behaviour and the dialect rule layer have not started and are the main work of "
     "Iteration 2.", lead="Iteration 1 conclusion: ")

heading("2. Completed functionality and what it adds to the project")
para("The table lists each function delivered and what it gives the project. Source files "
     "are shown in brackets for reference only.")
table(
    [2948, 6463],
    [
        {"height": 454, "cells": ("Function delivered", "What it adds to the project")},
        {"height": 1938, "cells": (
            "Conversion between the two profiles from the command line (pipeline.py, cli.py)",
            "A user can convert a Markdown file between CommonMark and GFM with one command; "
            "at present the conversion uses Pandoc's default behaviour, and explicit "
            "adaptation policies will be added in Iterations 2 and 3. The user obtains the "
            "converted file, the report and, optionally, the intermediate AST. The source "
            "file is never modified. The JSON AST is now the main point at which later "
            "adaptation rules will operate.")},
        {"height": 989, "cells": (
            "Explicit CommonMark and GFM profiles (profiles.py)",
            "The project states exactly which two dialects it supports and which Pandoc "
            "reader and writer each uses. An unsupported profile is rejected with a clear "
            "error instead of silently falling back.")},
        {"height": None, "cells": (
            "Reproducible Pandoc environment (pypandoc-binary, requirements.txt)",
            "All runs use Pandoc " + PANDOC_VERSION + ", supplied by the pinned "
            "pypandoc-binary package, whether or not Pandoc is installed on the machine, and "
            "the version is recorded in every report. The baseline comparison with direct "
            "Pandoc depends on this. Panflute, click and PyYAML are declared as dependencies "
            "for the rule layer and later CLI work; this prototype calls pypandoc directly "
            "and does not use them.")},
        {"height": 1663, "cells": (
            "Conversion report (diagnostics.py)",
            "Each run records the Pandoc version, source and target profiles, block counts "
            "and a log of events by stage. It prints to the terminal and is saved as text, "
            "or as JSON when the path ends in .json. The report format already defines "
            "fallback, loss and warning levels for later iterations; at present only info "
            "events are produced.")},
        {"height": 1506, "cells": (
            "Policy option (--policy)",
            "The option is accepted and echoed in the report's event log, which confirms "
            "that the setting reaches the pipeline; the structured policy field on each "
            "event is reserved and remains null in this iteration. The three values "
            "(fallback, approximate, strict) do not yet change the output; the behaviour is "
            "built in Iteration 2.")},
        {"height": 1400, "cells": (
            "Initial fixtures and automated tests (fixtures/, tests/)",
            "Two sample documents and five passing tests check parsing, heading preservation "
            "on a same-profile parse-and-write cycle, report metadata, rejection of an "
            "unknown profile and the full command-line run. They are the regression base for "
            "the rules that follow.")},
    ],
)
blank()

heading("3. How Iteration 1 reduces risk for later work")
para("The results support the layered design in Section 5 of the specification, check two "
     "of its key design decisions, record one baseline observation, and state what remains "
     "unverified.")
para("The specification requires Python AST transformation with Pandoc JSON as the process "
     "boundary. In this iteration Pandoc parsed the Markdown into its JSON AST, which was "
     "held in memory, written to a JSON file when --ast-out was supplied, and passed back "
     "to the target writer as JSON. The same-profile parse-and-write cycle preserved the "
     "heading text asserted in the test suite, and later adaptation rules can therefore be "
     "written against AST nodes rather than against raw Markdown text. Preservation has so "
     "far been asserted on heading text only, and byte-level equality with the input is not "
     "claimed; wider preservation is evaluated in Iteration 4.",
     lead="The AST process boundary works. ")
para("Section 6 of the specification requires the Pandoc version and options to be pinned "
     "and reported. Using the Pandoc " + PANDOC_VERSION + " bundled with pypandoc-binary and "
     "recording it in each report removes the question of which Pandoc a machine has. This "
     "is a prerequisite for the baseline comparison in Section 7.",
     lead="Reproducibility is in place. ")
para("With no adaptation rules applied, a GFM document written directly as CommonMark is "
     "changed by Pandoc's defaults: strikethrough becomes <s> HTML, task boxes become glyphs "
     "and tables become HTML tables. This was observed by inspecting the output and is not "
     "yet an automated test. It set the improvement target for the rule layer, which is to "
     "replace these defaults with explicit policies and reports, and it feeds the systematic "
     "baseline comparison in Iteration 4.",
     lead="Baseline behaviour was observed manually. ")
para("How GFM-specific constructs are written out has been observed but not asserted in "
     "tests. Strict mode and real loss events can only be tested once the rule layer exists. "
     "These are goals of the later iterations, not defects of Iteration 1.",
     lead="Limitation: not yet validated. ")

heading("4. Specification requirements and Iteration 1 status")
para("The table maps the main requirements of the specification to their status at the end "
     "of Iteration 1.")
table(
    [3969, 5443],
    [
        {"height": 454, "cells": ("Specification requirement", "Iteration 1 status")},
        {"height": None, "cells": (
            "Supported profiles, Pandoc version and reader/writer settings recorded.",
            "Partly implemented: the two profiles are defined with fixed Pandoc reader and "
            "writer names in profiles.py, and Pandoc " + PANDOC_VERSION + " is pinned through "
            "pypandoc-binary. Every report records the Pandoc version, the profile names and, "
            "in its event log, the reader and writer used. No further reader/writer options "
            "are set yet; any options added later will be itemised in the report from "
            "Iteration 2.")},
        {"height": 1242, "cells": (
            "CLI handling of input, source, target, policy and report.",
            "Implemented: the user selects input and output paths, source and target "
            "profile, policy and report path. The policy value is recorded; its downgrade "
            "behaviour is deferred to Iteration 2.")},
        {"height": None, "cells": (
            "Result presentation: converted Markdown plus a human-readable or JSON report.",
            "Implemented: output Markdown, AST JSON and a report are each written when the "
            "corresponding output path is supplied; the report also prints to the terminal, "
            "and its file is saved as plain text or JSON depending on the file suffix.")},
        {"height": 852, "cells": (
            "Source-versus-target comparison: source never modified, outputs kept separate.",
            "Basis implemented: the source is read-only and output goes to a separate file. "
            "The structural change report depends on the rules of Iterations 2 and 3.")},
        {"height": 1063, "cells": (
            "Information-loss reporting and strict mode.",
            "Report format reserved: fallback, loss and warning levels and construct/policy "
            "fields are defined (see Section 2). Real loss events and strict-mode stopping "
            "are deferred to Iteration 2.")},
        {"height": 2149, "cells": (
            "Compatibility checking through the report.",
            "Baseline implemented: the report records version, profiles and block counts. "
            "Source and target block counts are identical by construction: the target count "
            "is read from the same AST object before writing, so the equality only confirms "
            "that the write step did not fail and is not yet an independent check of the "
            "produced output. Re-parsing output with the matching reader is planned.")},
        {"height": 768, "cells": (
            "Adaptation of task lists, strikethrough, tables and autolinks, with fallbacks.",
            "Not started, as planned: task lists and strikethrough in Iteration 2; tables and "
            "autolinks in Iteration 3.")},
        {"height": 999, "cells": (
            "Fixture corpus of at least 40 cases; unit, integration, regression and "
            "round-trip tests.",
            "Started: 2 fixtures and 5 tests. The corpus grows with each rule from Iteration "
            "2; regression and round-trip testing are completed in Iteration 4.")},
        {"height": 1062, "cells": (
            "Baseline comparison with direct Pandoc conversion.",
            "Initial manual observation recorded (Section 3). The systematic comparison is "
            "planned for Iteration 4.")},
    ],
    header_valign="bottom",
    header_after="80",
    header_line="",
    table_style_id="15",
    header_rpr=RPR_TBL_HEAD_BOTTOM,
)
blank()

heading("5. Next iteration plan")
para("Following the work plan in Section 9 of the specification, Iteration 2 focuses on "
     "the core rules:")
bullet("Implement AST adaptation rules for task lists and strikethrough, so that these GFM "
       "constructs follow an explicit policy instead of Pandoc's default fallback when "
       "converting to CommonMark.")
bullet("Introduce the first configurable downgrade policy (fallback, approximate, strict) "
       "and produce real fallback and loss events in the report.")
bullet('Write unit tests for the new rules, including features nested in lists and block '
       'quotes (the "Nested structures" challenge in Section 6 of the specification), and '
       "extend the fixtures.")
bullet("Commit work in small steps per feature throughout Iteration 2, so the repository "
       "history reflects the actual development", after=BLANK_AFTER, tail=".")

heading("References")
reference("CommonMark. (2021) CommonMark Specification 0.30. Available at:",
          "https://spec.commonmark.org/0.30/",
          " https://spec.commonmark.org/0.30/ ", "(Accessed: 30 October 2026).")
reference("GitHub. (n.d.) GitHub Flavoured Markdown Spec. Available at:",
          "https://github.github.com/gfm/",
          " https://github.github.com/gfm/", " (Accessed: 26 October 2026).")
reference("Krewinkel, A. (n.d.) Panflute: Pythonic Pandoc Filters. Available at: ",
          "https://panflute.readthedocs.io/",
          "https://panflute.readthedocs.io/", " (Accessed: 28 October 2026).")
reference("MacFarlane, J. (n.d.) Pandoc User's Guide. Available at:",
          "https://pandoc.org/MANUAL.html",
          [" ", "https://pandoc.org/MANUAL.html"], " (Accessed: 30 October 2026).")

heading("AI usage statement")
para("AI tools were used only for drafting, proofreading and conceptual explanation. All "
     "design decisions and code were reviewed, understood and tested by the student, in "
     "accordance with course rules. No unexplained black-box code was included.")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "docs", "First_Iteration_Report_generated.docx")
PARENT = os.path.dirname(OUT)
if PARENT:
    os.makedirs(PARENT, exist_ok=True)


def save_report(path):
    """Save the document, stepping aside if the target is open in another program."""
    try:
        doc.save(path)
        return path
    except PermissionError:
        root, ext = os.path.splitext(path)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        fallback = root + "_" + stamp + ext
        doc.save(fallback)
        print("target file is open in another program; wrote %s instead" % fallback)
        return fallback


print("saved", save_report(OUT))
