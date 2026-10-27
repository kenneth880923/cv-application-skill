#!/usr/bin/env python3
"""Build an ATS-safe A4 CV (.docx) from a JSON content file.

Usage:
    python build_cv.py content.json "Output Name.docx" [--compact]

Formatting follows references/formatting-standard.md.
JSON shape: see examples/cv_example.json.
"""
import argparse
import json
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Twips

FONT = "Calibri"


def spacing(compact):
    """Spacing values in points (dxa / 20)."""
    if compact:
        return dict(head_before=2.2, head_after=1, co_before=2.9, co_after=0.7,
                    bullet_line=10.5, bullet_after=0.9, summary_line=10.6,
                    top=420, bottom=400)
    return dict(head_before=7, head_after=3, co_before=4, co_after=1,
                bullet_line=11.5, bullet_after=2, summary_line=11.5,
                top=620, bottom=620)


def set_run(run, size, bold=False, italic=False, colour=None, small_caps=False):
    run.font.name = FONT
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.small_caps = small_caps
    if colour:
        run.font.color.rgb = RGBColor.from_string(colour)


def para(doc_or_cell, text="", size=10, bold=False, italic=False, align=None,
         before=0, after=0, line=None, style=None):
    p = doc_or_cell.add_paragraph(style=style) if style else doc_or_cell.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line:
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(line)
    if align is not None:
        p.alignment = align
    if text:
        set_run(p.add_run(text), size, bold, italic)
    return p


def bottom_border(p):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "1"), ("w:color", "auto")):
        bottom.set(qn(k), v)
    pbdr.append(bottom)
    pPr.append(pbdr)


def heading(doc, text, sp):
    p = para(doc, before=sp["head_before"], after=sp["head_after"])
    set_run(p.add_run(text), 12, bold=True, small_caps=True)
    bottom_border(p)


def bullet(container, text, size, sp, colour=None):
    p = container.add_paragraph(style="List Bullet")
    pf = p.paragraph_format
    pf.left_indent = Twips(220 if colour is None else 200)
    pf.first_line_indent = Twips(-180)
    pf.space_before = Pt(0)
    pf.space_after = Pt(sp["bullet_after"] if colour is None else 0)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(sp["bullet_line"] if colour is None else 11)
    set_run(p.add_run(text), size, colour=colour)
    return p


def table_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "0"), ("w:color", "auto")):
            el.set(qn(k), v)
        borders.append(el)
    tblPr.append(borders)


def skills_table(doc, skills):
    skills = list(skills)[:9]
    per_col = -(-len(skills) // 3)  # fill column by column, 3 per column
    cols = [skills[i * per_col:(i + 1) * per_col] for i in range(3)]
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table_borders(table)
    for i, cell in enumerate(table.rows[0].cells):
        cell.width = Twips(3502)
        cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)
        items = cols[i]
        if not items:
            cell.add_paragraph()
        for s in items:
            bullet(cell, s, 9, None, colour="333333")


def build(data, out, compact=False):
    sp = spacing(compact)
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Twips(11906), Twips(16838)  # A4
    sec.top_margin, sec.bottom_margin = Twips(sp["top"]), Twips(sp["bottom"])
    sec.left_margin = sec.right_margin = Twips(700)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(10)

    para(doc, data["name"], 15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, data["title"], 10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    for line in data.get("contact", []):
        para(doc, line, 9, align=WD_ALIGN_PARAGRAPH.CENTER)

    heading(doc, "Summary", sp)
    para(doc, data["summary"], 10, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line=sp["summary_line"])

    if data.get("skills"):
        heading(doc, "Skills & Tools", sp)
        skills_table(doc, data["skills"])

    heading(doc, "Experience", sp)
    for job in data.get("experience", []):
        p = para(doc, before=sp["co_before"], after=sp["co_after"])
        set_run(p.add_run(f"{job['company']} - {job['title']}"), 10, bold=True)
        meta = "  |  ".join(x for x in (job.get("location"), job.get("dates")) if x)
        if meta:
            set_run(p.add_run(f"  |  {meta}"), 10, italic=True)
        if job.get("scope"):
            para(doc, job["scope"], 10, italic=True, after=1)
        for b in job.get("bullets", []):
            bullet(doc, b, 10, sp)

    if data.get("education"):
        heading(doc, "Education", sp)
        for ed in data["education"]:
            p = para(doc, after=1)
            set_run(p.add_run(f"{ed['degree']}, {ed['institution']}"), 10, bold=True)
            meta = "  |  ".join(x for x in (ed.get("location"), ed.get("dates")) if x)
            if meta:
                set_run(p.add_run(f"  |  {meta}"), 10, italic=True)

    if data.get("training"):
        heading(doc, "Training", sp)
        for t in data["training"]:
            bullet(doc, t, 10, sp)

    doc.save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("content")
    ap.add_argument("output")
    ap.add_argument("--compact", action="store_true", help="tighter spacing to fit one page")
    args = ap.parse_args()
    with open(args.content, encoding="utf-8") as f:
        data = json.load(f)
    text = json.dumps(data, ensure_ascii=False)
    if "—" in text:
        sys.exit("Em dash found in content. Replace it before building.")
    build(data, args.output, args.compact)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
