from src.blackbook.config import BlackbookConfig
from src.blackbook.document import create_document
from src.blackbook.preliminary.cover import add_cover_page
from src.blackbook.preliminary.certificate import add_certificate_page
from src.blackbook.preliminary.declaration import add_declaration_page
from src.blackbook.preliminary.acknowledgement import add_acknowledgement_page
from src.blackbook.preliminary.abstract import add_abstract_page
from src.blackbook.preliminary.index import add_index_page
from src.blackbook.chapters.renderer import render_markdown
from src.blackbook.chapters.renderer import render_plain_text_file
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
        "acknowledgement": """
I would like to express my sincere gratitude to all the people who have helped me throughout the completion of this project. I am grateful to my project guide for the continuous support, guidance and encouragement provided throughout the development of the project.

I would also like to express my deep gratitude to the Head of the Department and all the faculty members of the Department of Information Technology for their valuable guidance and support.

I would like to thank my friends and classmates for their valuable suggestions, ideas and assistance during the development of the project.

Finally, I would like to thank my parents and family for their constant support, encouragement and motivation throughout the completion of this project.
""",
"abstract": """
Cleanlytics is a web-based data analytics and cleaning platform that provides data preparation, analysis, 
and visualization through a single interface. It supports CSV, Excel, JSON and automatically profiles uploaded data 
to identify its structure, data types, missing values, and quality issues.

The platform provides features such as missing-value handling, duplicate
removal, data standardization, column transformation, filtering, sorting and
group-based analysis. It also incorporates an analytics and semantic layer
that helps represent business-oriented measures and relationships within
datasets. Users can create interactive dashboards using different
visualization techniques and generate reports for further use.

The platform uses DuckDB as its server-side analytical engine for profiling, cleaning, joining, and aggregation. 
Its quality engine identifies issues such as missing values, duplicates, outliers, and type inconsistencies 
and provides suitable corrective actions. Cleanlytics also detects relationships between multiple tables 
and uses approved relationships to perform cross-table analysis through a semantic model.

CLEANYTICS aims to reduce the complexity of traditional data preparation and
Business Intelligence workflows by bringing data processing, visualization,
analytics and reporting into a single platform. The system includes interactive dashboards, 
automatic dashboard generation, data export, and operation history with undo support. 
It is developed using Next.js 16, React 19, FastAPI, Python, and DuckDB, providing an 
integrated workflow from raw data to meaningful insights.
 The proposed system provides a practical, scalable and user-friendly
approach to transforming raw data into actionable information.
""",
"index": [

    {"sr": "1", "title": "Introduction", "bold": True},

    {"level1": "1.1", "title": "Background"},

    {"level1": "1.2", "title": "Objectives"},

    {"level1": "1.3", "title": "Purpose, Scope, and Applicability"},

    {"level2": "1.3.1", "title": "Purpose"},

    {"level2": "1.3.2", "title": "Scope"},

    {"level2": "1.3.3", "title": "Applicability"},

    {"level1": "1.4", "title": "Achievements"},

    {"level1": "1.5", "title": "Organization of Report"},

    {
        "sr": "2",
        "title": "Survey Of Technologies",
        "bold": True
    },

    {
        "sr": "3",
        "title": "Requirement And Analysis",
        "bold": True
    },

    {"level1": "3.1", "title": "Problem Definition"},

    {"level1": "3.2", "title": "Requirement Specification"},

    {"level1": "3.3", "title": "Planning and Scheduling"},

    {
        "level1": "3.4",
        "title": "Software and Hardware Requirements"
    },

    {
        "level1": "3.5",
        "title": "Preliminary Product Description"
    },

    {
        "level1": "3.6",
        "title": "Conceptual Models"
    },

    {"level2": "3.6.1", "title": "Event Table"},

    {"level2": "3.6.2", "title": "Use Case Diagram"},

    {"level2": "3.6.3", "title": "Entity Relationship Diagram"},

    {"level2": "3.6.4", "title": "Class Diagram"},

    {"level2": "3.6.5", "title": "Object Diagram"},

    {"level2": "3.6.6", "title": "Activity Diagram"},

    {"level2": "3.6.7", "title": "Sequence Diagram"},

    {"level2": "3.6.8", "title": "State Flow Diagram"},

    {"level2": "3.6.9", "title": "Context Diagram"},

    {"level2": "3.6.10", "title": "Data Flow Diagram"},

    {"level2": "3.6.11", "title": "Component Diagram"},

    {"level2": "3.6.12", "title": "Package Diagram"},

    {"level2": "3.6.13", "title": "Deployment Diagram"},

    {
        "sr": "4",
        "title": "System Coding",
        "bold": True
    },

    {"level1": "4.1", "title": "Code"},
    {"level1": "4.2", "title": "Data Dictionary"},
    {"level1": "4.3", "title": "Program Description"},
    {"level1": "4.4", "title": "Naming Conventions"},
    {"level1": "4.5", "title": "Validations"},

    {
        "sr": "5",
        "title": "Program Listing",
        "bold": True
    },

    {"level1": "5.1", "title": "Cost Estimation"},
    {"level1": "5.2", "title": "Schema Design"},
    {"level1": "5.3", "title": "User Manual With Screenshots"},
    {"level1": "5.4", "title": "Test Cases Design"},

    {
        "sr": "6",
        "title": "Conclusion",
        "bold": True
    },

    {"level1": "6.1", "title": "Conclusion"},
    {"level1": "6.2", "title": "Limitations of the System"},
    {"level1": "6.3", "title": "Future Scope of the Project"},

    {
        "sr": "7",
        "title": "Bibliography",
        "bold": True
    },
]
    }

    add_cover_page(document, data)
    add_certificate_page(document, data)
    add_declaration_page(document, data)
    add_acknowledgement_page(document, data)
    add_abstract_page(document, data)
    add_index_page(document, data)
    document.add_page_break()
    render_markdown(
    document,
    "src/blackbook/chapters/introduction.md")
    document.add_page_break()
    render_plain_text_file(
       document,
       "src/blackbook/chapters/survey_of_technologies.txt"
   )
    document.add_page_break()
    render_plain_text_file(
           document,
           "src/blackbook/chapters/requirement_analysis.txt"
       )
    
    
    
    



    document.save("output/cover_test.docx")

    print("Cover page generated successfully!")


if __name__ == "__main__":
    main()