from pathlib import Path
from docx import Document


def load_text_file(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    return path.read_text(encoding="utf-8")


def load_docx_file(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    document = Document(path)

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n\n".join(paragraphs)


def load_content(path):
    path = Path(path)

    if path.suffix.lower() == ".txt":
        return load_text_file(path)

    if path.suffix.lower() == ".docx":
        return load_docx_file(path)

    raise ValueError(
        "Supported formats: .txt and .docx"
    )