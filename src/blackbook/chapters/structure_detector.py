"""
structure_detector.py

Detects blackbook document structure directly from plain,
unformatted text -- no Markdown (#, ##, ###) required.

Numbering conventions detected:

    1.1 Background              -> SECTION       (2 number groups)
    1.3.1 Purpose                -> SUBSECTION    (3 number groups)
    INTRODUCTION                  -> CHAPTER       (short, ALL CAPS)
    CHAPTER 2: SURVEY OF TECH     -> CHAPTER       (starts with "CHAPTER")
    2. SURVEY OF TECHNOLOGIES     -> CHAPTER       (single number, ALL CAPS)
    1. Frontend Technologies      -> SUBHEADING    (single number, mixed case)
    Functional Requirements       -> SUBHEADING    (short Title Case, no number)
    1. Automated profiling        -> NUMBERED      (follows a ':' intro line)
    I. User Authentication ...      -> REQUIREMENT   (roman numeral, label auto-
                                                     detected up to a sentence-
                                                     starter word like "The"/"Users")
    - some point / * some point      -> BULLET
    Term: description                  -> BULLET / REQUIREMENT with the term bolded
    tab-separated rows (2+ in a row)    -> TABLE (first row = header)
    anything else                       -> BODY text (merged into paragraphs)

Disambiguating "1. Heading" from "1. list item" -- both use the same
"digit + period" pattern:

    - If the text right before it ends with ':', or we're already
      mid-list, it's a numbered list item.
    - Otherwise ALL CAPS content -> CHAPTER heading.
    - Otherwise -> SUBHEADING.

Roman-numeral requirement lines (e.g. "I. User Authentication The
system must allow...") have no punctuation separating the label from
the description. The label is taken as the words up to the first
sentence-starter word (STOP_WORDS below), which reliably matches
"Label Word Word The/Users/... rest of sentence" phrasing.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional

# --- token types -----------------------------------------------------

CHAPTER = "chapter"
SECTION = "section"
SUBSECTION = "subsection"
SUBHEADING = "subheading"
BULLET = "bullet"
NUMBERED = "numbered"
REQUIREMENT = "requirement"
TABLE = "table"
BODY = "body"


@dataclass
class Token:
    type: str
    text: str
    # For BULLET / REQUIREMENT tokens: the leading label to bold,
    # e.g. "React.js" or "I. User Authentication".
    bold_prefix: Optional[str] = None
    # For TABLE tokens: list of rows, each a list of cell strings.
    # rows[0] is treated as the header row.
    rows: Optional[List[List[str]]] = field(default=None)


# --- line-level patterns ----------------------------------------------

SUBSECTION_RE = re.compile(r"^\d+\.\d+\.\d+\s+\S.*$")     # 1.3.1 Purpose
SECTION_RE = re.compile(r"^\d+\.\d+\s+\S.*$")              # 1.1 Background
SINGLE_NUM_RE = re.compile(r"^(\d+)\.\s+(\S.*)$")           # 1. <text>
BULLET_RE = re.compile(r"^[-*\u2022]\s+\S.*$")              # - item / * item
CHAPTER_WORD_RE = re.compile(r"^CHAPTER\s+\d+", re.IGNORECASE)

# I. / II. / III. / IV. ... up to a generous roman numeral length
ROMAN_RE = re.compile(r"^([IVXLCDM]{1,6})\.\s+(\S.*)$")

# Words that typically start the sentence part of a requirement line,
# used to find where the bold label ends.
REQUIREMENT_STOP_WORDS = {
    "The", "A", "An", "This", "That", "These", "Those", "Users",
    "It", "Non-technical", "All", "Each", "Every",
}


def _uppercase_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if c.isupper()) / len(letters)


def _looks_like_chapter_text(text: str) -> bool:
    """Heuristic: short line, mostly uppercase letters."""
    words = text.split()
    if not (1 <= len(words) <= 10):
        return False
    return _uppercase_ratio(text) > 0.9


def _looks_like_plain_subheading(line: str) -> bool:
    """
    A short Title Case line with no trailing punctuation and no
    numbering at all, e.g. "Functional Requirements". Used for
    sub-headings that aren't numbered.
    """
    if line.endswith((".", ":", ";", ",")):
        return False
    words = line.split()
    if not (1 <= len(words) <= 6):
        return False
    # Every word should start with a capital letter (Title Case).
    return all(w[0].isupper() for w in words if w[0].isalpha())


def _split_bold_prefix(text: str):
    """
    Split "Term: description" -> ("Term", "description") for bolding
    the leading term. Only splits on the FIRST colon, and only if the
    term itself looks like a short label (not a full clause).
    """
    if ":" not in text:
        return None, text

    term, _, rest = text.partition(":")
    term = term.strip()
    rest = rest.strip()

    if 0 < len(term.split()) <= 6 and rest:
        return term, rest

    return None, text


def _split_requirement_label(numeral: str, content: str):
    """
    Split "User Authentication The system must allow..." into
    ("User Authentication", "The system must allow...") by scanning
    for the first REQUIREMENT_STOP_WORDS word.
    """
    words = content.split()
    label_words = []

    for i, w in enumerate(words):
        if w in REQUIREMENT_STOP_WORDS:
            break
        label_words.append(w)
    else:
        # No stop word found -- treat the whole line as body-like,
        # nothing to bold.
        return None, content

    if not label_words:
        return None, content

    label = " ".join(label_words)
    rest = " ".join(words[len(label_words):])
    return f"{numeral}. {label}", rest


def _split_table_row(line: str):
    """
    Return a list of cells if this line looks like a table row
    (tab-separated, 2+ columns), else None.
    """
    if "\t" in line:
        cells = [c.strip() for c in line.split("\t") if c.strip() != ""]
        if len(cells) >= 2:
            return cells
    return None


def detect_structure(text: str) -> List[Token]:
    """Convert raw plain text into a list of typed Tokens."""
    tokens: List[Token] = []
    body_buffer: List[str] = []
    table_buffer: List[List[str]] = []
    last_meaningful_line = ""
    in_numbered_list = False

    def flush_body():
        if body_buffer:
            paragraph = " ".join(s.strip() for s in body_buffer).strip()
            if paragraph:
                tokens.append(Token(BODY, paragraph))
            body_buffer.clear()

    def flush_table():
        if table_buffer:
            tokens.append(Token(TABLE, "", rows=[row[:] for row in table_buffer]))
            table_buffer.clear()

    for raw_line in text.splitlines():
        line = raw_line.strip("\n")
        stripped = line.strip()

        if not stripped:
            flush_body()
            flush_table()
            continue

        # --- table row (check BEFORE .strip() collapses tabs at edges) ---
        row_cells = _split_table_row(line.strip())
        if row_cells is not None:
            flush_body()
            table_buffer.append(row_cells)
            last_meaningful_line = stripped
            in_numbered_list = False
            continue
        else:
            flush_table()

        line = stripped

        # --- subsection (X.Y.Z) ---
        if SUBSECTION_RE.match(line):
            flush_body()
            number = re.match(r"^(\d+\.\d+\.\d+)\s+", line).group(1)
            heading_text = line[len(number):].strip()
            tokens.append(Token(SUBSECTION, f"{number} {heading_text}"))
            last_meaningful_line = line
            in_numbered_list = False
            continue

        # --- section (X.Y) ---
        if SECTION_RE.match(line):
            flush_body()
            number = re.match(r"^(\d+\.\d+)\s+", line).group(1)
            heading_text = line[len(number):].strip()
            tokens.append(Token(SECTION, f"{number} {heading_text}"))
            last_meaningful_line = line
            in_numbered_list = False
            continue

        # --- "CHAPTER N: ..." explicit form ---
        if CHAPTER_WORD_RE.match(line):
            flush_body()
            tokens.append(Token(CHAPTER, line))
            last_meaningful_line = line
            in_numbered_list = False
            continue

        # --- bullet ---
        if BULLET_RE.match(line):
            flush_body()
            item_text = re.sub(r"^[-*\u2022]\s+", "", line).strip()
            bold_prefix, rest = _split_bold_prefix(item_text)
            display_text = f"{bold_prefix}: {rest}" if bold_prefix else item_text
            tokens.append(Token(BULLET, display_text, bold_prefix=bold_prefix))
            last_meaningful_line = line
            in_numbered_list = False
            continue

        # --- roman numeral requirement ("I. Label ... The system must ...") ---
        roman_match = ROMAN_RE.match(line)
        if roman_match:
            flush_body()
            numeral, content = roman_match.groups()
            bold_prefix, rest = _split_requirement_label(numeral, content)
            display_text = f"{bold_prefix} {rest}" if bold_prefix else line
            tokens.append(Token(REQUIREMENT, display_text, bold_prefix=bold_prefix))
            last_meaningful_line = line
            in_numbered_list = False
            continue

        # --- single number + period: chapter / subheading / numbered ---
        single_match = SINGLE_NUM_RE.match(line)
        if single_match:
            flush_body()
            number, content = single_match.groups()

            if in_numbered_list or last_meaningful_line.endswith(":"):
                tokens.append(Token(NUMBERED, content.strip()))
                in_numbered_list = True
            elif _looks_like_chapter_text(content):
                tokens.append(Token(CHAPTER, line))
                in_numbered_list = False
            else:
                tokens.append(Token(SUBHEADING, line))
                in_numbered_list = False

            last_meaningful_line = line
            continue

        # --- plain ALL CAPS chapter line, no numbering ---
        if _looks_like_chapter_text(line):
            flush_body()
            tokens.append(Token(CHAPTER, line))
            last_meaningful_line = line
            in_numbered_list = False
            continue

        # --- plain Title Case sub-heading, no numbering ---
        if _looks_like_plain_subheading(line):
            flush_body()
            tokens.append(Token(SUBHEADING, line))
            last_meaningful_line = line
            in_numbered_list = False
            continue

        # --- body text ---
        body_buffer.append(line)
        last_meaningful_line = line
        in_numbered_list = False

    flush_body()
    flush_table()
    return tokens