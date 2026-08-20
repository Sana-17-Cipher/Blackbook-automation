from src.blackbook.config import BlackbookConfig
from src.blackbook.document import create_document
from src.blackbook.preliminary.cover import add_cover_page


def main():
    config = BlackbookConfig()
    document = create_document(config)

    data = {
        "project_title": "PROJECT TITLE",
        "project_subtitle": "(Project Subtitle)",
        "semester_requirement": "Requirements for completion of Semester V of",
        "degree": "BACHELOR OF VOCATION (SOFTWARE DEVELOPMENT)",
        "student_name": "STUDENT NAME",
        "uid": "STUDENT UID",
        "guide": "Prof. GUIDE NAME",
        "coordinator": "Ms. COORDINATOR NAME",
        "academic_year": "2026-27",
    }

    add_cover_page(document, data)

    document.save("output/cover_test.docx")

    print("Cover page generated successfully!")


if __name__ == "__main__":
    main()