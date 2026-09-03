from src.blackbook.document import create_document
from src.blackbook.config import BlackbookConfig
from src.blackbook.document import create_document
from src.blackbook.preliminary.cover import add_cover_page
from src.blackbook.preliminary.certificate import add_certificate_page
from src.blackbook.preliminary.declaration import add_declaration_page
from src.blackbook.preliminary.acknowledgement import add_acknowledgement_page
from src.blackbook.preliminary.abstract import add_abstract_page
from src.blackbook.preliminary.index import add_figures_page, add_index_page
from src.blackbook.chapters.renderer import render_markdown
from src.blackbook.chapters.renderer import render_plain_text_file
def main():
    config = BlackbookConfig()
    document = create_document(config)

    data = {
        "project_title": "Enter your Project Name", 
        "project_subtitle": "", 
"semester_requirement": "Submitted in partial fulfillment of the\nRequirements for the award of the Degree of",
"degree": "BACHELOR OF SCIENCE (INFORMATION TECHNOLOGY)",
"student_name": "Name of Student",
"uid": "UID / Roll No.",
"guide": "Mr. Wilson Rao and Ms. Bertilla Fernandes",
"coordinator": "",  
"academic_year": "2026-27",

        "acknowledgement": 
"""I am extremely grateful for the guidance of our Head of Department (Information Technology
& Software Development) Mr. Wilson Rao. Sir had great involvement in making sure my
project is a well-rounded and a flawless system by constantly guiding us till the completion of
our project work by providing all the necessary information for developing a good system.
I would like to express immense gratitude to the people who have helped me throughout the
course of my project. I am grateful to Prof. Ms. Bertilla Fernandes for her constant
encouragement and support.
I would also like to thank all of my friends and my seniors who supported and helped me in
completing the project, where they all had their own interesting takes on the technology stack,
and the own interesting ideas on how to finesse the system even further. I would also like to
thank my family for their constant support and encouragement.""",

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

    {"sr": "2", "title": "Survey Of Technologies", "bold": True},

    {"sr": "3", "title": "Requirement And Analysis", "bold": True},
    {"level1": "3.1", "title": "Problem Definition"},
    {"level1": "3.2", "title": "Requirement Specification"},
    {"level1": "3.3", "title": "Planning and Scheduling"},
    {"level1": "3.4", "title": "Software and Hardware Requirements"},
    {"level1": "3.5", "title": "Preliminary Product Description"},
    {"level1": "3.6", "title": "Conceptual Models"},
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

    {"sr": "4", "title": "System Coding", "bold": True},
    {"level1": "4.1", "title": "Code"},
    {"level1": "4.2", "title": "Data Dictionary"},
    {"level1": "4.3", "title": "Program Description"},
    {"level1": "4.4", "title": "Naming Conventions"},
    {"level1": "4.5", "title": "Validations"},

    {"sr": "5", "title": "Program Listing", "bold": True},
    {"level1": "5.1", "title": "Cost Estimation"},
    {"level1": "5.2", "title": "Schema Design"},
    {"level1": "5.3", "title": "User Manual With Screenshots"},
    {"level1": "5.4", "title": "Test Cases Design"},

    {"sr": "6", "title": "Conclusion", "bold": True},
    {"level1": "6.1", "title": "Conclusion"},
    {"level1": "6.2", "title": "Limitations of the System"},
    {"level1": "6.3", "title": "Future Scope of the Project"},

    {"sr": "7", "title": "Bibliography", "bold": True},
],
"figures_index": [
    {"sr": "1", "title": "Gantt Chart", "page": ""},
    {"sr": "2", "title": "PERT Chart", "page": ""},
    {"sr": "3", "title": "Event Table", "page": ""},
    {"sr": "4", "title": "ER Diagram", "page": ""},
    {"sr": "5", "title": "Class Diagram", "page": ""},
    {"sr": "6", "title": "Object Diagram", "page": ""},
    {"sr": "7", "title": "Use Case Diagram", "page": ""},
    {"sr": "8", "title": "Activity Diagram", "page": ""},
    {"sr": "9", "title": "Sequence Diagram", "page": ""},
    {"sr": "10", "title": "State Diagram", "page": ""},
    {"sr": "11", "title": "Package Diagram", "page": ""},
    {"sr": "12", "title": "Component Diagram", "page": ""},
    {"sr": "13", "title": "Deployment Diagram", "page": ""},
    {"sr": "14", "title": "Data Flow Level 0 Diagram", "page": ""},
    {"sr": "15", "title": "Data Flow Level 1 Diagram", "page": ""},
    {"sr": "16", "title": "Data Flow Level  Diagram", "page": ""},
    {"sr": "17", "title": "Database Schema Design", "page": ""},
],
    }
    add_cover_page(document, data)
    add_certificate_page(document, data)
    add_abstract_page(document, data)
    add_acknowledgement_page(document, data)   # swapped: now after abstract
    add_index_page(document, data)
    add_figures_page(document, data)
    document.add_page_break()
    render_markdown(
        document,
        "src/blackbook/chapters/introduction.md"
    )
    render_plain_text_file(
       document,
       "src/blackbook/chapters/survey_of_technologies.txt"
   )
    render_plain_text_file(
           document,
           "src/blackbook/chapters/requirement_analysis.txt"
       )
    render_plain_text_file(
        document,
        "src/blackbook/chapters/system_design.txt"
    )
    render_plain_text_file(document, "src/blackbook/chapters/implementation_and_testing.txt")
    render_plain_text_file(document, "src/blackbook/chapters/results_and_discussion.txt")
    render_plain_text_file(document, "src/blackbook/chapters/conclusion.txt")
    render_plain_text_file(document, "src/blackbook/chapters/references.txt")
    



    document.save("output/cover_test.docx")


    print("Document generated successfully: output/cover_test.docx")


if __name__ == "__main__":
    main()