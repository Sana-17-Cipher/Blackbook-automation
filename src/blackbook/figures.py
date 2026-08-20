from pathlib import Path
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_logo(document, logo_path, width_cm=3.2):
    """Add the institutional logo centered on the page."""

    logo_path = Path(logo_path)

    if not logo_path.exists():
        raise FileNotFoundError(f"Logo not found: {logo_path}")

    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = paragraph.add_run()
    run.add_picture(
        str(logo_path),
        width=Cm(width_cm)
    )

    return paragraph