# INTRODUCTION

## 1.1 BACKGROUND OF THE PROJECT

In today's data-driven environment, organizations and individuals use datasets extensively for analysis and decision-making. However, raw data often contains missing values, duplicate records, inconsistent data types, and relationships that are not clearly defined. Preparing such data manually can be time-consuming and may lead to errors.

Existing tools often separate data cleaning, modelling, and visualization into different applications, and many require technical knowledge of SQL or Python. **Cleanlytics** was developed to address this problem by providing a single web-based platform for uploading, profiling, cleaning, modelling, analysing, and visualizing datasets.

The platform uses **DuckDB** as its analytical engine, allowing data to be processed efficiently on the server. With a **Next.js frontend and FastAPI backend**, Cleanlytics provides a simple interface through which users can work with their data without writing code.

## 1.2 OBJECTIVES

1. To provide automated profiling of uploaded datasets, including data types, missing values, distinct values, and semantic column roles.
2. To identify common data quality issues such as duplicates, missing values, inconsistent types, outliers, and constant columns.
3. To provide safe data cleaning and transformation operations with operation history and multi-step undo support.
4. To automatically detect relationships between multiple tables and provide cardinality and confidence information.
5. To develop a semantic model that uses approved relationships for accurate cross-table analytical queries.
6. To provide interactive and automatic dashboards for presenting analytical results.
7. To support exporting cleaned and transformed data in formats such as CSV, Excel, JSON, and Parquet.
8. To use server-side DuckDB-based processing so that larger datasets can be analysed efficiently without loading the complete dataset into the browser.

## 1.3 PURPOSE, SCOPE AND APPLICABILITY

### 1.3.1 PURPOSE

The main purpose of Cleanlytics is to provide a unified platform for data preparation and analysis. It combines data cleaning, quality analysis, relationship modelling, querying, and visualization in one application. The system is designed to make data operations easier to understand, track, and reverse without requiring programming knowledge.

### 1.3.2 SCOPE

Cleanlytics supports the complete data preparation workflow, including:

- CSV, Excel, JSON, and Parquet file ingestion
- Automated data profiling
- Data quality detection
- Data cleaning and transformation
- Multi-table relationship detection
- Semantic data modelling
- Cross-table analytical queries
- Interactive and automatic dashboards
- Data export in multiple formats
- Operation history and undo

Uploaded data is streamed to the server and processed using DuckDB, allowing the system to handle larger datasets more efficiently than browser-based processing.

The current system focuses on uploaded datasets and does not include real-time database connections, scheduled data pipelines, or simultaneous collaborative editing.

### 1.3.3 APPLICABILITY

Cleanlytics can be used by business analysts, students, researchers, data engineers, and other users who work with structured datasets. Business users can analyse sales or inventory data, researchers can examine survey datasets, and students can use the platform to understand data preparation and analytics without writing SQL or Python code.

## 1.4 ACHIEVEMENTS

● The Cleanlytics project was successfully developed as an integrated platform for data
preparation and analysis. The system allows users to upload datasets, analyse their
quality, clean and transform data, identify relationships between tables, and generate
meaningful visualizations through a single interface.
● The major achievements of the project include successful server-side data processing
using DuckDB, allowing the system to handle large datasets efficiently. The platform
also provides automated data profiling and quality detection, along with support for
multiple files and Excel worksheets.
● Cleanlytics successfully detects relationships between tables and provides cardinality
and confidence information, which is further used for cross-table analytical queries
through the semantic model. Users can also generate dashboards, perform reversible data
operations using operation history and undo, and export processed data in formats such as
CSV, Excel, and JSON.
● The system was also tested with a 151 MB dataset containing approximately 2.2
million rows, demonstrating that the platform can handle large datasets while
maintaining efficient data processing.

## 1.5 ORGANIZATION OF REPORT

### 1.5.1 REQUIREMENT AND ANALYSIS

The frontend is developed using Next.js 16, React 19, and Tailwind CSS v4.

The backend uses FastAPI and Python, with DuckDB for analytical processing.

Authentication supports Google OAuth with an optional guest mode.

Uploaded data is streamed to the server and processed using project-specific DuckDB databases.

Application metadata is maintained separately from analytical data.

The system requires Python 3.10+, Node.js 18+, 8 GB RAM, and a modern browser.

### 1.5.2 SYSTEM DESIGN

The system follows the workflow:

Upload → Profiling → Quality Analysis → Cleaning → Relationship Detection → Semantic Modelling → Analytics → Dashboard → Export

The architecture separates analytical data from application metadata. DuckDB handles data processing and SQL-based analysis, while the semantic model manages relationships and enables cross-table queries.

### 1.5.3 IMPLEMENTATION AND TESTING

The major modules implemented include data ingestion, profiling, quality analysis, operations, relationship detection, semantic modelling, analytics, and dashboard generation.

Data operations use an operation history and snapshot-based undo mechanism. The relationship detector identifies possible table relationships, while the semantic model uses approved relationships to generate cross-table SQL queries.

Testing included unit testing, integration testing, and system-level testing to verify individual modules, API communication, and the complete workflow from data upload to export.

### 1.5.4 RESULTS AND DISCUSSION

Cleanlytics successfully processes data through the complete analytics workflow. Testing demonstrated that a 151 MB dataset with approximately 2.2 million rows could be ingested, profiled, and linked in about 17 seconds.

The system also successfully performed cross-table aggregation, processed multiple files in a single request, and converted Excel worksheets into separate tables with relationships detected automatically.

The results demonstrate that the DuckDB-based architecture provides efficient server-side processing while the semantic model enables consistent cross-table analytics.

### 1.5.5 CONCLUSION

Cleanlytics provides an integrated solution for data cleaning, modelling, analysis, and visualization. Its DuckDB-based architecture allows larger datasets to be processed efficiently without loading complete datasets into the browser.

The combination of automated quality analysis, relationship detection, semantic modelling, reversible operations, and interactive dashboards makes the platform suitable for both technical and non-technical users.

The project also provides a strong foundation for future features such as AI-assisted analytics, scheduled data refresh, and collaborative workspaces.