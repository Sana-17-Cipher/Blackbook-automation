from pathlib import Path

from .config import BlackbookConfig
from .document import create_document
from .styles import add_heading, add_subheading, add_body_paragraph
from .content.models import Project


def generate_blackbook(project: Project, output_path):
    config = BlackbookConfig()
    document = create_document(config)

    for chapter in project.chapters:
        document.add_page_break()

        add_heading(
            document,
            f"CHAPTER {chapter.number}"
        )

        add_heading(
            document,
            chapter.title
        )

        for section in chapter.sections:
            add_subheading(document, section.title)

            if section.content:
                add_body_paragraph(
                    document,
                    section.content
                )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    document.save(output_path)

    return output_path