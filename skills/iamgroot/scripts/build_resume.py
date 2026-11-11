#!/usr/bin/env python3
"""Build ATS-friendly resume PDFs from the candidate's resume data with LaTeX.

    python3 build_resume.py --data profile/resume.json                 # every variant
    python3 build_resume.py --data profile/resume.json --variant germany
    python3 build_resume.py --data profile/resume.json --tex-only      # write the .tex, do not compile

The data file (see references/resume.example.json) holds the facts once. Each entry under "variants"
overrides top-level keys for one market: normally only "header_line" and "target", so experience,
dates and skills are identical in every version.

The layout is assets/resume-template.tex: one page, two columns, no ligatures and no hyphenation,
so the text a recruiter's parser extracts matches what is printed. A LaTeX engine is needed to
compile: tectonic, pdflatex, xelatex or latexmk, whichever is found first.
After building, read the PDF's extracted text once and check it still fits the intended page count.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(os.path.dirname(HERE), "assets", "resume-template.tex")
SEP = "\n\\enspace|\\enspace\n"
SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
DEFAULT_LAYOUT = {"left": ["summary", "experience", "projects"],
                  "right": ["skills", "education", "languages", "target"]}
TITLES = {"summary": "Summary", "experience": "Work Experience", "projects": "Selected Projects",
          "skills": "Technical Skills", "education": "Education", "languages": "Languages", "target": "Target"}


def esc(text):
    """Escape LaTeX special characters in plain data."""
    return "".join(SPECIAL.get(c, c) for c in str(text))


def href(url, label):
    return "\\href{%s}{%s}" % (str(url).replace("%", r"\%").replace("#", r"\#"), esc(label))


def header(d):
    out = ["{\\Large\\textbf{%s}}\\par" % esc(d["name"]), "\\vspace{1.5pt}"]
    if d.get("headline"):
        out += ["{\\normalsize\\textbf{%s}}\\par" % esc(d["headline"]), "\\vspace{2.5pt}"]
    c = d.get("contact", {})
    row = []
    if c.get("email"):
        row.append(href("mailto:" + c["email"], c["email"]))
    if c.get("phone"):
        row.append(esc(c["phone"]))
    row += [href(x["url"], x.get("label") or re.sub(r"^https?://(www\.)?", "", x["url"])) for x in c.get("links", [])]
    if row:
        out += [SEP.join(row) + "\\par", "\\vspace{1.5pt}"]
    if d.get("header_line"):
        out.append(SEP.join(esc(x) for x in d["header_line"]))
    return "\n\n".join(out)


def section(title, body):
    return "\\section*{%s}\n\n%s" % (esc(title), body)


def render(key, d, titles):
    value = d.get(key)
    if not value:
        return None
    title = titles.get(key, key.replace("_", " ").title())
    if key == "experience":
        blocks = []
        for e in value:
            if e.get("stack"):
                head = "\\entry\n{%s}\n{%s}\n{%s}\n{%s}" % (esc(e["title"]), esc(e.get("dates", "")),
                                                          esc(e.get("employer", "")), esc(e["stack"]))
            else:
                head = "\\entryplain\n{%s}\n{%s}\n{%s}" % (esc(e["title"]), esc(e.get("dates", "")),
                                                         esc(e.get("employer", "")))
            bullets = "".join("  \\item %s\n" % esc(b) for b in e.get("bullets", []))
            blocks.append(head + ("\n\n\\begin{itemize}\n%s\\end{itemize}" % bullets if bullets else ""))
        return section(title, "\n\n".join(blocks))
    if key == "projects":
        return section(title, "\n\n".join(
            "\\project\n{%s}\n{%s}\n{%s}" % (href(p["url"], p["name"]) if p.get("url") else esc(p["name"]),
                                           esc(p.get("stack", "")), esc(p.get("description", ""))) for p in value))
    if key == "skills":
        return section(title, "\n\n".join("\\skill\n{%s}\n{%s}" % (esc(s["group"]), esc(s["items"])) for s in value))
    if key == "education":
        return section(title, "\n\n".join(
            "\\education\n{%s}\n{%s}\n{%s}" % (esc(e["school"]), esc(e.get("degree", "")), esc(e.get("detail", "")))
            for e in value))
    if key == "languages":
        return section(title, "\n\n\\vspace{2.5pt}\n\n".join(
            "\\textbf{%s}\\par\n%s" % (esc(x["language"]), esc(x.get("level", ""))) for x in value))
    if isinstance(value, list):  # any other list becomes bullets
        return section(title, "\\begin{itemize}\n%s\\end{itemize}" % "".join("  \\item %s\n" % esc(x) for x in value))
    return section(title, esc(value))  # summary, target and any other plain-text section


def build_tex(d):
    layout = d.get("layout") or DEFAULT_LAYOUT
    titles = {**TITLES, **d.get("section_titles", {})}
    tex = open(TEMPLATE, encoding="utf-8").read()
    parts = {
        "%%HEADER%%": header(d),
        "%%LEFT%%": "\n\n".join(filter(None, (render(k, d, titles) for k in layout["left"]))),
        "%%RIGHT%%": "\n\n".join(filter(None, (render(k, d, titles) for k in layout["right"]))),
        "%%COLUMN_RATIO%%": str(d.get("column_ratio", 0.67)),
        "%%FONT_SIZE%%": str(d.get("font_size", 8.45)),
        "%%LINE_HEIGHT%%": str(d.get("line_height", 9.45)),
    }
    for marker, text in parts.items():
        tex = tex.replace(marker, text)
    return tex


def compile_pdf(tex_path, out_dir):
    name = os.path.splitext(os.path.basename(tex_path))[0]
    if shutil.which("tectonic"):
        cmd = [["tectonic", "--outdir", out_dir, tex_path]]
    elif shutil.which("latexmk"):
        cmd = [["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-outdir=" + out_dir, tex_path]]
    else:
        engine = shutil.which("pdflatex") or shutil.which("xelatex")
        if not engine:
            sys.exit("No LaTeX engine found. Install one (for example: brew install tectonic), or run with "
                     "--tex-only and compile the .tex on Overleaf.")
        run = [engine, "-interaction=nonstopmode", "-halt-on-error", "-output-directory", out_dir, tex_path]
        cmd = [run, run]
    for c in cmd:
        r = subprocess.run(c, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("LaTeX failed:\n" + (r.stdout + r.stderr)[-2500:])
    for ext in (".aux", ".log", ".out", ".fls", ".fdb_latexmk"):
        junk = os.path.join(out_dir, name + ext)
        if os.path.exists(junk):
            os.remove(junk)
    return os.path.join(out_dir, name + ".pdf")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="resume data JSON")
    ap.add_argument("--variant", action="append", help="variant name; repeat for several; default is all")
    ap.add_argument("--out", help="output directory (default: build/ next to the data file)")
    ap.add_argument("--tex-only", action="store_true", help="write the .tex files and do not compile")
    a = ap.parse_args()
    base = json.load(open(a.data, encoding="utf-8"))
    variants = base.pop("variants", None) or {"default": {}}
    out_dir = os.path.abspath(a.out or os.path.join(os.path.dirname(os.path.abspath(a.data)), "build"))
    os.makedirs(out_dir, exist_ok=True)
    for name in (a.variant or list(variants)):
        if name not in variants:
            sys.exit(f"unknown variant {name!r}; available: {', '.join(variants)}")
        d = {**base, **variants[name]}
        stem = os.path.splitext(d.get("file") or f"{re.sub(r'[^A-Za-z0-9]+', '_', d['name']).strip('_')}_Resume_{name}")[0]
        tex_path = os.path.join(out_dir, stem + ".tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(build_tex(d))
        if a.tex_only:
            print("wrote", tex_path)
            continue
        pdf = compile_pdf(tex_path, out_dir)
        print("built", pdf)
    if not a.tex_only:
        print("Now read each PDF's extracted text once: dates, links and special characters should be plain text, "
              "and the page count should be what you intend.")


if __name__ == "__main__":
    main()
