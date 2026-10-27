# CV Formatting Standard

Every CV produced by this skill follows this standard. `scripts/build_cv.py` applies it automatically from a JSON content file, so no template .docx is needed.

## Page and type

| Item | Specification |
|---|---|
| Font | Calibri throughout |
| Page | A4 portrait; margins top/bottom 620 dxa (~1.09 cm), left/right 700 dxa (~1.23 cm) |
| Name | 15 pt, bold, centred |
| Target job title | 10 pt, bold, centred; must match the JD title |
| Contact lines (2) | 9 pt, centred |
| Section headings | 12 pt, bold, small caps, single bottom border; space before 7 pt / after 3 pt |
| Summary | 10 pt, justified, line spacing 11.5 pt |
| Skills & Tools | Three-column table with borders, bullet list in each cell, 9 pt, colour #333333, total width 10506 dxa (3 x 3502) so it fits inside A4 margins |
| Company / title line | 10 pt bold `Company - Job Title`, then on the same line, italic `City, Country | Mon YYYY - Mon YYYY` |
| Scope line (optional) | 10 pt italic, one line describing team, markets or remit |
| Bullets | 10 pt, left indent 220 dxa / hanging 180 dxa, line spacing 11.5 pt, space after 2 pt |

Section order: SUMMARY, SKILLS & TOOLS, EXPERIENCE, EDUCATION, TRAINING (optional).

## Contact lines

1. `City, Country  |  phone (national format)  |  email`
2. `linkedin.com/in/...  |  right-to-work statement`

## Length

- Two pages maximum.
- If the second page holds only Education / Training, compress spacing to fit one page. Keep font sizes; tighten: heading spacing before 2.2 pt / after 1 pt, company line before 2.9 pt / after 0.7 pt, bullet line spacing 10.5 pt / after 0.9 pt, summary line spacing 10.6 pt, page top 420 / bottom 400 dxa. `build_cv.py --compact` does this.

## ATS rules

- Single-column body. The Skills table is the only table allowed (a deliberate choice: it keeps nine skills compact). Do not use tables anywhere else.
- No text boxes, images, icons, shapes, or content in headers/footers.
- Standard section headings (as above).
- Native Word bullets only, no symbol characters typed as bullets.
- One date format throughout: `Mon YYYY - Mon YYYY` (use `Present` for a current role).
- No em dashes anywhere (also a common AI-writing marker).
- Job title in the header matches the JD title.

## Verification (run every time)

1. Build: `python scripts/build_cv.py content.json "Full Name 2026 CV - Job Title (Company).docx"`
2. Inspect the XML:
   ```bash
   unzip -p out.docx word/document.xml | grep -c "<w:tbl>"     # expect 1 (Skills)
   unzip -p out.docx word/document.xml | grep -cE "txbx|w:drawing"  # expect 0
   unzip -p out.docx word/document.xml | grep -c "—"            # expect 0 (no em dashes)
   ```
3. Render and look at every page:
   ```bash
   soffice --headless --convert-to pdf out.docx
   pdftoppm -png -r 80 out.pdf page
   ```
   Confirm the page count, that nothing overflows the margins, and that the Skills table fits.
