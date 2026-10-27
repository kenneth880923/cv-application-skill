# CV Application Skill for Claude

A Claude skill that turns a job description into a tailored UK application:

1. **Stage 1** - JD analysis, gap check against your experience, CV drafting
2. **Stage 2** - ATS scoring and a recruiter-style review, with a pass/fail gate
3. **Stage 3** - Cover letter (on request)
4. **Stage 4** - Interview preparation (on request)

CVs are written in British English, avoid AI-sounding phrasing, and are built as an ATS-safe A4 `.docx`.

## Install

1. On this page, click **Code > Download ZIP** and unzip it.
2. Zip the `cv-application-skill` folder on its own (the folder that contains `SKILL.md`).
3. In Claude, open the Skills section of your settings and upload that zip.

## Use

Start a chat (a Project works best, so your facts persist) and say something like:

> Here is my CV and a job description. Please run the CV application workflow.

On first use Claude asks for your name, contact details, right-to-work status and current CV. It never invents experience: anything it cannot find, it asks you about.

Tip: keep a short "facts" note in your Project with verified numbers and things you have never done (tools, responsibilities). Claude will check it before writing.

## Folder

```
cv-application-skill/
├── SKILL.md                         # the workflow Claude follows
├── references/formatting-standard.md
├── scripts/build_cv.py              # builds the .docx from JSON
└── examples/cv_example.json         # fictional example content
```

Try the builder yourself:

```bash
pip install python-docx
python cv-application-skill/scripts/build_cv.py cv-application-skill/examples/cv_example.json "Example CV.docx"
```

## Updating

Edit the files here and re-upload the zip in Claude. Changes to the workflow go in `SKILL.md`; layout changes go in `references/formatting-standard.md` and `scripts/build_cv.py`.
