from src.blackbook.config import BlackbookConfig
from src.blackbook.document import create_document


def main():
    config = BlackbookConfig()
    document = create_document(config)

    document.save("output/test_document.docx")

    print("Blackbook base document created successfully!")


if __name__ == "__main__":
    main()