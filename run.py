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
    {"sr": "1", "title": "Introduction", "bold": True, "page": ""},
    {"level1": "1.1", "title": "Background", "page": ""},
    {"level1": "1.2", "title": "Objectives", "page": ""},
    {"level1": "1.3", "title": "Purpose, Scope, and Applicability", "page": ""},
    {"level2": "1.3.1", "title": "Purpose", "page": ""},
    {"level2": "1.3.2", "title": "Scope", "page": ""},
    {"level2": "1.3.3", "title": "Applicability", "page": ""},
    {"level1": "1.4", "title": "Achievements", "page": ""},
    {"level1": "1.5", "title": "Organisation of Report", "page": ""},

    {"sr": "2", "title": "Survey Of Technologies", "bold": True, "page": ""},

    {"sr": "3", "title": "Requirements And Analysis", "bold": True, "page": ""},
    {"level1": "3.1", "title": "Problem Definition", "page": ""},
    {"level1": "3.2", "title": "Requirements Specification", "page": ""},
    {"level1": "3.3", "title": "Planning and Scheduling", "page": ""},
    {"level1": "3.4", "title": "Software and Hardware Requirements", "page": ""},
    {"level1": "3.5", "title": "Preliminary Product Description", "page": ""},
    {"level1": "3.6", "title": "Conceptual Models", "page": ""},

    {"sr": "4", "title": "System Design", "bold": True, "page": ""},
    {"level1": "4.1", "title": "Basic Modules", "page": ""},
    {"level1": "4.2", "title": "Data Design", "page": ""},
    {"level2": "4.2.1", "title": "Schema Design", "page": ""},
    {"level2": "4.2.2", "title": "Data Integrity and Constraints", "page": ""},
    {"level1": "4.3", "title": "Procedural Design", "page": ""},
    {"level2": "4.3.1", "title": "Logic Diagrams", "page": ""},
    {"level2": "4.3.2", "title": "Data Structures", "page": ""},
    {"level2": "4.3.3", "title": "Algorithms Design", "page": ""},
    {"level1": "4.4", "title": "User Interface Design", "page": ""},
    {"level1": "4.5", "title": "Security Issues", "page": ""},
    {"level1": "4.6", "title": "Test Cases Design", "page": ""},

    {"sr": "5", "title": "Implementation And Testing", "bold": True, "page": ""},
    {"level1": "5.1", "title": "Implementation Approaches", "page": ""},
    {"level1": "5.2", "title": "Coding Details and Code Efficiency", "page": ""},
    {"level2": "5.2.1", "title": "Code Efficiency", "page": ""},
    {"level1": "5.3", "title": "Testing Approach", "page": ""},
    {"level2": "5.3.1", "title": "Unit Testing", "page": ""},
    {"level2": "5.3.2", "title": "Integrated Testing", "page": ""},
    {"level2": "5.3.3", "title": "Beta Testing", "page": ""},
    {"level1": "5.4", "title": "Modifications and Improvements", "page": ""},
    {"level1": "5.5", "title": "Test Cases", "page": ""},

    {"sr": "6", "title": "Results And Discussion", "bold": True, "page": ""},
    {"level1": "6.1", "title": "Test Reports", "page": ""},
    {"level1": "6.2", "title": "User Documentation", "page": ""},

    {"sr": "7", "title": "Conclusions", "bold": True, "page": ""},
    {"level1": "7.1", "title": "Conclusion", "page": ""},
    {"level2": "7.1.1", "title": "Significance of the System", "page": ""},
    {"level1": "7.2", "title": "Limitations of the System", "page": ""},
    {"level1": "7.3", "title": "Future Scope of the Project", "page": ""},

    {"sr": "", "title": "References", "bold": True, "page": ""},
    {"sr": "", "title": "Glossary", "bold": True, "page": ""},
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
# add_proforma_page(document, data)      # NEW — pending your answer below
    add_certificate_page(document, data)
# add_role_responsibility_page(document, data)  # NEW — pending your answer below
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