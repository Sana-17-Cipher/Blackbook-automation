from pathlib import Path
import re

from docx.enum.text import WD_BREAK
from docx.shared import Pt


def add_page_break(document):
    """Add a page break."""
    paragraph = document.add_paragraph()
    paragraph.add_run().add_break(WD_BREAK.PAGE)


def clean_inline_markdown(text):
    """
    Remove Markdown formatting markers.

    Examples:
        **Cleanlytics** -> Cleanlytics
        *Cleanlytics*   -> Cleanlytics
        __Cleanlytics__ -> Cleanlytics
        `Cleanlytics`   -> Cleanlytics
    """

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)

    return text


def add_heading(document, text, level):
    """
    Blackbook heading hierarchy:

    Level 1 = 16 pt bold
    Level 2 = 14 pt bold
    Level 3 = 12 pt bold
    """

    text = clean_inline_markdown(text)

    paragraph = document.add_paragraph()

    run = paragraph.add_run(text)
    run.bold = True

    if level == 1:
        run.font.size = Pt(16)

    elif level == 2:
        run.font.size = Pt(14)

    elif level == 3:
        run.font.size = Pt(12)

    run.font.name = "Times New Roman"

    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(10)

    return paragraph


def add_body_paragraph(document, text):
    """Add normal 12 pt body text."""

    text = clean_inline_markdown(text)

    paragraph = document.add_paragraph()

    run = paragraph.add_run(text)
    run.font.size = Pt(12)
    run.font.name = "Times New Roman"

    paragraph.paragraph_format.first_line_indent = Pt(18)
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.paragraph_format.line_spacing = 1.15

    return paragraph


def add_bullet(document, text):
    """Add a 12 pt bullet."""

    text = clean_inline_markdown(text)

    paragraph = document.add_paragraph(style="List Bullet")

    run = paragraph.add_run(text)
    run.font.size = Pt(12)
    run.font.name = "Times New Roman"

    paragraph.paragraph_format.space_after = Pt(4)

    return paragraph


def add_numbered_item(document, text):
    """Add a 12 pt numbered item."""

    text = clean_inline_markdown(text)

    paragraph = document.add_paragraph(style="List Number")

    run = paragraph.add_run(text)
    run.font.size = Pt(12)
    run.font.name = "Times New Roman"

    paragraph.paragraph_format.space_after = Pt(4)

    return paragraph


def render_markdown(document, markdown_file):
    """
    Render a blackbook Markdown chapter.

    Formatting:

        # CHAPTER
            16 pt bold

        ## 1.1 SECTION
            14 pt bold
            New page between sections

        ### 1.3.1 SUBSECTION
            12 pt bold
            No page break

        Normal text
            12 pt

    Important:
    The first ## section does NOT receive an additional
    page break because the preliminary/index section has
    already ended on its own page.
    """

    markdown_path = Path(markdown_file)

    if not markdown_path.exists():
        raise FileNotFoundError(
            f"Markdown file not found: {markdown_path}"
        )

    text = markdown_path.read_text(
        encoding="utf-8"
    )

    lines = text.splitlines()

    current_paragraph = []

    # ---------------------------------------------------------
    # Track whether we have already rendered the first section.
    # ---------------------------------------------------------

    first_section = True

    def flush_paragraph():
        if current_paragraph:

            paragraph_text = " ".join(
                line.strip()
                for line in current_paragraph
            ).strip()

            if paragraph_text:
                add_body_paragraph(
                    document,
                    paragraph_text
                )

            current_paragraph.clear()

    for raw_line in lines:

        line = raw_line.strip()

        # -----------------------------------------------------
        # EMPTY LINE
        # -----------------------------------------------------

        if not line:
            flush_paragraph()
            continue

        # -----------------------------------------------------
        # CHAPTER HEADING
        #
        # # INTRODUCTION
        #
        # We don't render this as a separate page.
        # -----------------------------------------------------

        if re.match(r"^#\s+", line):

            flush_paragraph()

            heading_text = re.sub(
                r"^#\s+",
                "",
                line
            ).strip()

            # Don't create a standalone INTRODUCTION page.
            if heading_text.upper() == "INTRODUCTION":
                continue

            add_heading(
                document,
                heading_text,
                1
            )

            continue

        # -----------------------------------------------------
        # LEVEL 2 SECTION
        #
        # ## 1.1 BACKGROUND
        #
        # FIRST SECTION:
        #     no additional page break
        #
        # EVERY FOLLOWING SECTION:
        #     page break
        # -----------------------------------------------------

        if re.match(r"^##\s+", line):

            flush_paragraph()

            if not first_section:
                add_page_break(document)

            first_section = False

            heading_text = re.sub(
                r"^##\s+",
                "",
                line
            ).strip()

            add_heading(
                document,
                heading_text,
                2
            )

            continue

        # -----------------------------------------------------
        # LEVEL 3 SUBSECTION
        #
        # ### 1.3.1 PURPOSE
        #
        # NO page break.
        # -----------------------------------------------------

        if re.match(r"^###\s+", line):

            flush_paragraph()

            heading_text = re.sub(
                r"^###\s+",
                "",
                line
            ).strip()

            add_heading(
                document,
                heading_text,
                3
            )

            continue

        # -----------------------------------------------------
        # BULLET
        # -----------------------------------------------------

        if re.match(r"^[-*]\s+", line):

            flush_paragraph()

            bullet_text = re.sub(
                r"^[-*]\s+",
                "",
                line
            )

            add_bullet(
                document,
                bullet_text
            )

            continue

        # -----------------------------------------------------
        # NUMBERED LIST
        # -----------------------------------------------------

        if re.match(r"^\d+\.\s+", line):

            flush_paragraph()

            numbered_text = re.sub(
                r"^\d+\.\s+",
                "",
                line
            )

            add_numbered_item(
                document,
                numbered_text
            )

            continue

        # -----------------------------------------------------
        # NORMAL BODY TEXT
        # -----------------------------------------------------

        current_paragraph.append(
            clean_inline_markdown(line)
        )

    # ---------------------------------------------------------
    # Remaining paragraph
    # ---------------------------------------------------------

    flush_paragraph()