from dataclasses import dataclass, field
from typing import List


@dataclass
class Figure:
    path: str
    caption: str = ""


@dataclass
class Table:
    title: str
    headers: List[str]
    rows: List[List[str]]


@dataclass
class Section:
    title: str
    content: str = ""
    sections: List["Section"] = field(default_factory=list)
    figures: List[Figure] = field(default_factory=list)
    tables: List[Table] = field(default_factory=list)


@dataclass
class Chapter:
    number: int
    title: str
    sections: List[Section] = field(default_factory=list)


@dataclass
class Project:
    title: str
    subtitle: str = ""
    student_name: str = ""
    uid: str = ""
    degree: str = ""
    guide: str = ""
    coordinator: str = ""
    academic_year: str = ""
    abstract: str = ""
    acknowledgement: str = ""
    chapters: List[Chapter] = field(default_factory=list)