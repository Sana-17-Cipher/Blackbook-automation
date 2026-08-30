# Blackbook Automation

A Python-based document generation system that converts plain, unformatted project content into a fully structured, formatted, and editable academic report ("blackbook") in Microsoft Word format.

## Motivation

Academic project documentation at the undergraduate and diploma level typically follows a rigid, prescribed format: consistent heading hierarchies, mandatory page breaks between sections, standardized fonts and sizes, structured indexes, and formal figure and table numbering. In practice, most of the effort in producing this documentation goes not into the content itself, but into manually and repeatedly applying formatting rules across dozens of pages — a process that is tedious, error-prone, and easy to get subtly wrong (inconsistent font sizes, missed page breaks, misaligned indexes).

This project was undertaken with two goals in mind:

1. **To remove the formatting burden from academic report writing.** The underlying idea is that a student should be able to write their project content as plain, unformatted text — the way they would naturally draft it and have the system automatically infer document structure (chapters, sections, subsections, tables, figures, bullet lists) and apply the correct formatting, numbering, and pagination rules without manual intervention.

2. **To deepen my own practical experience with Python**, specifically in the areas of text parsing, regular expressions, document object models (via `python-docx`), modular software architecture, and iterative debugging of a real, non-trivial system as requirements evolved. Rather than working with a toy dataset or a tutorial project, I wanted to solve an actual problem I was personally affected by, and to experience the full lifecycle of building a tool: designing an architecture, discovering edge cases, refactoring based on real output, and correcting course when an initial design decision turned out to be wrong.

## What the System Does

Blackbook Automation accepts plain text files as input - no Markdown syntax, no manual bold/heading markup — and produces a formatted `.docx` document that a student can open directly in Microsoft Word and continue editing.

Given input such as:

```
CHAPTER 3: REQUIREMENTS AND ANALYSIS

3.1 PROBLEM DEFINITION

Organisations and analysts working with data frequently receive raw datasets...

3.1.1 EXISTING SYSTEM

Most data cleaning today is done using spreadsheet applications...
```

the system automatically identifies chapter headings, numbered sections, numbered subsections, bullet lists, numbered lists, tables, and figure placeholders, and renders each with the correct font size, weight, alignment, and pagination behaviour without the author writing a single line of formatting markup.

## Core Design Principle: Structure Detection, Not Markup

The central design decision behind this project is that **structure should be inferred from conventions the author already uses naturally**, rather than requiring the author to learn a markup language. A numbered heading like `3.1.1 Existing System` is unambiguous: the numbering pattern alone (three dot-separated numeric groups) is sufficient to classify it as a subsection, choose its font size, and decide whether it warrants a page break. Similarly, a line beginning with a hyphen is a bullet; a line composed of tab-separated values is a table row; a short, capitalized, unpunctuated line is a heading.

This required building a rule-based text classifier from first principles: a set of regular expressions and heuristics (capitalization ratio, word count, trailing punctuation, numbering depth) that reliably distinguish these categories from one another, including resolving genuine ambiguities — for example, disambiguating `1. Frontend Technologies` (a heading) from `1. Automated profiling` (a list item continuing a numbered list) based on surrounding context.

## Architecture

The system is deliberately separated into three independent layers, so that content changes never require touching formatting code, and formatting changes never require touching content:

```
CONTENT                    ENGINE                      OUTPUT
--------------------       --------------------        --------------------
Plain .txt files per   ->  Structure detection     ->  Editable .docx
chapter, written in        (regex-based parser)        with correct
ordinary prose              |                          fonts, page breaks,
                            Formatting engine             numbering, and
                            (heading levels, bullets,     embedded figures
                            tables, figure insertion)
```

- **`structure_detector.py`** — converts raw text into a typed token stream (chapter, section, subsection, bullet, numbered item, table row, figure reference, plain body text).
- **`renderer.py`** — walks the token stream and applies the correct `python-docx` formatting calls for each token type, including the page-break rules (every chapter and every section after the first begins on a new page; subsections do not force a break).
- **`figures.py`** — resolves figure placeholder tokens (e.g. `[figure: 3.6.2]`) to image files on disk using a chapter-scoped naming convention, inserts and centers the image, and auto-generates a bold, numbered caption from the filename.
- **`preliminary/`** — a self-contained module for the front matter of the report (cover page, certificate, declaration, acknowledgement, abstract, index), kept separate from chapter content so that changing the report body never risks breaking the preliminary pages.

## Technical Stack

- **Python 3.10+**
- **python-docx** for programmatic Word document generation
- **Regular expressions** for structural classification of plain text
- Modular package layout (`chapters/`, `preliminary/`, `assets/`) to keep content, formatting logic, and media assets independently maintainable

## Formatting Rules Enforced

- Times New Roman throughout, with a strict font-size hierarchy: chapter headings (16pt, bold, centered), section headings (14pt, bold), subsection headings (12pt, bold), body text (12pt, justified).
- Every chapter and every section (after the first in a chapter) begins on a new page; subsections continue in the existing flow.
- Table borders rendered at a consistent 0.75pt weight.
- Figures are automatically numbered and captioned based on their filename, removing the need to manually track figure numbers as content is reordered or expanded.
- Inline Markdown artifacts (stray `**`, `##`, backticks) are stripped automatically in case they slip into otherwise plain text, so the final document never exposes formatting syntax to the reader.

## What I Learned

Working through this project surfaced a number of practical software engineering lessons that are easy to state abstractly but are best learned by encountering them directly:

- **Ambiguity in natural text is the hard part, not the formatting.** Deciding whether a numbered line is a heading or a list item, or whether a short capitalized phrase is a title or an acronym-heavy sentence, required building and refining heuristics against real content rather than assuming a single regular expression would suffice.
- **State ownership matters in rendering pipelines.** An early version of the page-break logic tracked a single shared flag across chapter, section, and subsection handling, which caused a subtle bug: the first section immediately following a chapter heading would incorrectly receive an extra page break in some chapters but not others, depending on what happened to appear first. Diagnosing this required tracing execution against multiple real outputs before recognizing that break-ownership needed to belong to a single, narrowly-scoped piece of state.
- **Small path and naming inconsistencies compound quickly.** Several issues over the course of development traced back to mismatches between where files were expected (by code) and where they actually lived (on disk) a reminder that in any system spanning content, code, and assets, keeping naming and path conventions consistent is as important as the logic itself.
- **Iterative, output-driven debugging is effective for this class of problem.** Because the final artifact is a visual document, many defects were only apparent by generating the output and inspecting it directly reinforcing the value of a short feedback loop between a code change and a way to observe its effect.

## Status

The system currently generates a complete draft blackbook covering preliminary pages (cover, certificate, declaration, acknowledgement, abstract, index), and full chapter content through Requirements and Analysis, System Design, Implementation and Testing, Results and Discussion, Conclusion, and References. Development is ongoing, with further refinement planned for dynamic index page-number calculation and expanded table-formatting options.