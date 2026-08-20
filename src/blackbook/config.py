from dataclasses import dataclass
@dataclass
class BlackbookConfig:

    # -------------------------
    # DOCUMENT
    # -------------------------
    page_width_cm: float = 21.0
    page_height_cm: float = 29.7

    # Margins
    top_margin_cm: float = 1.5
    bottom_margin_cm: float = 1.5
    left_margin_cm: float = 1.5
    right_margin_cm: float = 1.5

    # -------------------------
    # FONT
    # -------------------------
    font_name: str = "Times New Roman"

    body_font_size: int = 12
    heading_font_size: int = 16
    subheading_font_size: int = 14

    # -------------------------
    # SPACING
    # -------------------------
    body_line_spacing: float = 1.15
    paragraph_spacing_after_pt: int = 8

    # -------------------------
    # PAGE BORDER
    # -------------------------
    border_enabled: bool = True
    border_size: int = 10
    border_color: str = "000000"

    # -------------------------
    # PAGE LIMIT
    # -------------------------
    minimum_pages: int = 80
    maximum_pages: int = 90

    # -------------------------
    # PROJECT SCHEDULE
    # -------------------------
    gantt_start_month: str = "May"
    gantt_end_month: str = "September"

    # -------------------------
    # NUMBERING
    # -------------------------
    figure_numbering: bool = True
    table_numbering: bool = True
    section_numbering: bool = True
    automatic_index: bool = True