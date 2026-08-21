import re

from .models import Project, Chapter, Section


CHAPTER_PATTERN = re.compile(
    r"^CHAPTER\s+(\d+)\s*[:\-]?\s*(.*)$",
    re.IGNORECASE
)

SECTION_PATTERN = re.compile(
    r"^(\d+(?:\.\d+)*)\s+(.+)$"
)


def parse_content(text, project_data):
    """
    Convert normal project text into our internal structure.
    """

    project = Project(
        title=project_data.get("title", ""),
        subtitle=project_data.get("subtitle", ""),
        student_name=project_data.get("student_name", ""),
        uid=project_data.get("uid", ""),
        degree=project_data.get("degree", ""),
        guide=project_data.get("guide", ""),
        coordinator=project_data.get("coordinator", ""),
        academic_year=project_data.get("academic_year", "")
    )

    current_chapter = None
    current_section = None

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        chapter_match = CHAPTER_PATTERN.match(line)

        if chapter_match:
            number = int(chapter_match.group(1))
            title = chapter_match.group(2).strip()

            current_chapter = Chapter(
                number=number,
                title=title
            )

            project.chapters.append(current_chapter)
            current_section = None
            continue

        section_match = SECTION_PATTERN.match(line)

        if section_match and current_chapter:

            title = section_match.group(2).strip()

            current_section = Section(title=title)

            current_chapter.sections.append(
                current_section
            )

            continue

        if current_section:
            if current_section.content:
                current_section.content += " "

            current_section.content += line

    return project