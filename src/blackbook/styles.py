from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


def apply_font(run, size=12, bold=False, italic=False, underline=False):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.underline = underline


def add_body_paragraph(document, text):
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    run = paragraph.add_run(text)
    apply_font(run, size=12)

    return paragraph


def add_heading(document, text):
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = paragraph.add_run(text)
    apply_font(run, size=16, bold=True)

    return paragraph


def add_subheading(document, text):
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

    run = paragraph.add_run(text)
    apply_font(run, size=14, bold=True)

    return paragraph


def add_centered_text(document, text, size=12, bold=False):
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = paragraph.add_run(text)
    apply_font(run, size=size, bold=bold)

    return paragraph