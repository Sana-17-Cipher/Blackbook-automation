"""
structure_detector.py

Detects blackbook document structure directly from plain,
unformatted text -- no Markdown (#, ##, ###) required.

Numbering conventions detected:

    1.1 Background              -> SECTION     (2 number groups)
    1.3.1 Purpose                -> SUBSECTION  (3 number groups)
    INTRODUCTION                  -> CHAPTER     (short, ALL CAPS)
    CHAPTER 2: SURVEY OF TECH     -> CHAPTER     (starts with "CHAPTER", ALL CAPS)
    2. SURVEY OF TECHNOLOGIES     -> CHAPTER     (single number, ALL CAPS content)
    1. Frontend Technologies      -> SUBHEADING  (single number, mixed case, standalone)
    1. Automated profiling        -> NUMBERED    (single number, follows a ':' intro line)
    - some point / * some point    -> BULLET
    Term: description               -> BULLET with the leading term bolded
    anything else                   -> BODY text (merged into paragraphs)

Disambiguating "1. Heading" from "1. list item" -- both use the same
"digit + period" pattern. The rule used to tell them apart:

    - If the text right before it ends with ':', it's the start of
      a real numbered list (an intro like "The objectives are:").
    - Otherwise, if the content is ALL CAPS, it's a CHAPTER heading.
    - Otherwise it's a SUBHEADING (a bold sub-heading, e.g. inside
      a "Survey of Technologies" chapter).
"""

import re
from dataclasses import dataclass
from typing import List, Optional

# --- token types -----------------------------------------------------

CHAPTER = "chapter"
SECTION = "section"
SUBSECTION = "subsection"
SUBHEADING = "subheading"
BULLET = "bullet"
NUMBERED = "numbered"
BODY = "body"


@dataclass
class Token:
    type: str
    text: str
    # For BULLET tokens: if the text has a "Term: description" shape,
    # bold_prefix holds "Term" so the renderer can bold just that part.
    bold_prefix: Optional[str] = None


# --- line-level patterns ----------------------------------------------

SUBSECTION_RE = re.compile(r"^\d+\.\d+\.\d+\s+\S.*$")   # 1.3.1 Purpose
SECTION_RE = re.compile(r"^\d+\.\d+\s+\S.*$")            # 1.1 Background
SINGLE_NUM_RE = re.compile(r"^(\d+)\.\s+(\S.*)$")         # 1. <text>
BULLET_RE = re.compile(r"^[-*\u2022]\s+\S.*$")            # - item / * item

CHAPTER_WORD_RE = re.compile(r"^CHAPTER\s+\d+", re.IGNORECASE)


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


def _split_bold_prefix(text: str):
    """
    Split "Term: description" -> ("Term", "description") for bolding
    the leading term, matching the reference formatting where the
    term before the colon is bold. Only splits on the FIRST colon,
    and only if the term itself looks like a short label (not a full
    sentence containing a colon further in).
    """
    if ":" not in text:
        return None, text

    term, _, rest = text.partition(":")
    term = term.strip()
    rest = rest.strip()

    # Only treat as a bold-term bullet if the term is short (a label,
    # not a full clause) and there's actually a description after it.
    if 0 < len(term.split()) <= 6 and rest:
        return term, rest

    return None, text


def detect_structure(text: str) -> List[Token]:
    """Convert raw plain text into a list of typed Tokens."""
    tokens: List[Token] = []
    body_buffer: List[str] = []
    last_meaningful_line = ""  # last non-empty line seen, for the ':' rule
    in_numbered_list = False   # True while consuming a real numbered list

    def flush_body():
        if body_buffer:
            paragraph = " ".join(s.strip() for s in body_buffer).strip()
            if paragraph:
                tokens.append(Token(BODY, paragraph))
            body_buffer.clear()

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            flush_body()
            continue

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

        # --- single number + period: chapter / subheading / numbered ---
        single_match = SINGLE_NUM_RE.match(line)
        if single_match:
            flush_body()
            number, content = single_match.groups()

            if in_numbered_list or last_meaningful_line.endswith(":"):
                # A real numbered list item -- either the first one,
                # following an intro like "The objectives are:", or a
                # later item continuing that same list.
                tokens.append(Token(NUMBERED, content.strip()))
                in_numbered_list = True
            elif _looks_like_chapter_text(content):
                # e.g. "2. SURVEY OF TECHNOLOGIES"
                tokens.append(Token(CHAPTER, line))
                in_numbered_list = False
            else:
                # e.g. "1. Frontend Technologies" -- a bold sub-heading
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

        # --- body text ---
        body_buffer.append(line)
        last_meaningful_line = line
        in_numbered_list = False

    flush_body()
    return tokens