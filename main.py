#!/usr/bin/env python3
"""
Convert a Markdown file to PDF using ReportLab + markdown2.

Usage:
    python md2pdf.py input.md output.pdf
"""

import sys
from markdown2 import markdown
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def convert(md_path: str, pdf_path: str):
    # Read MD and convert to basic HTML
    with open(md_path, 'r', encoding='utf-8') as f:
        html = markdown(f.read(), extras=["fenced-code-blocks", "tables"])

    # Strip tags to plain text with minimal formatting
    # (ReportLab doesn’t render full HTML—so we’ll drop tags)
    # A quick hack: remove all HTML tags
    import re
    text = re.sub(r'<[^>]+>', '', html)

    # Build PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph(line, styles['Normal']))
            story.append(Spacer(1, 4))
    doc.build(story)
    print(f"[✓] Converted {md_path} → {pdf_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python md2pdf.py <input.md> <output.pdf>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
