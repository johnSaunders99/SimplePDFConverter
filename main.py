#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re
from pathlib import Path
from markdown2 import markdown
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1. 注册一个支持中文的 TrueType 字体（比如 SimHei 或者 Noto Sans CJK）
#    把 SimHei.ttf 放在项目同级目录，或者给出绝对路径。
pdfmetrics.registerFont(TTFont('SimHei', './font/simhei.ttf'))

# 2. 基于默认样式，创建一个中文样式，指定 fontName="SimHei"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='Chinese',
    parent=styles['Normal'],
    fontName='SimHei',
    fontSize=12,
    leading=16,
))

def convert(md_path: Path, pdf_path: Path):
    # 读取 Markdown，转成 HTML，再剥标签成纯文本
    text_md = md_path.read_text(encoding='utf-8')
    html = markdown(text_md, extras=["fenced-code-blocks", "tables"])
    plain = re.sub(r'<[^>]+>', '', html)

    # 构建 PDF，所有段落都用 "Chinese" 样式
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    story = []
    for line in plain.splitlines():
        line = line.strip()
        if line:
            story.append(Paragraph(line, styles['Chinese']))
        else:
            story.append(Spacer(1, 8))
    doc.build(story)
    print(f"[✓] 已生成 PDF：{pdf_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python md2pdf.py <input.md> <output.pdf>")
        sys.exit(1)

    md_file = Path(sys.argv[1])
    pdf_file = Path(sys.argv[2])
    convert(md_file, pdf_file)