from typing import NamedTuple, Optional


import datetime


YEAR_STANDINGS: list = ["Freshman", "Sophomore", "Junior", "Senior"]
TERMS: list = ["Fall", "Winter", "Spring", "Summer"]


class Header(NamedTuple):
    DegreePlanID: str
    Institution: str
    AcademicYear: str
    Curriculum: str
    DegreePlan: str
    DegreeType: str
    SystemType: str
    CIP: str


class Course(NamedTuple):
    CourseSequenceID: str
    CourseName: str
    Prefix: str
    Number: str
    Prerequisites: Optional[str]
    Corequisites: Optional[str]
    Strict_Corequisites: Optional[str]
    CreditHours: str
    CanonicalName: Optional[str]
    TermNumber: str
    Course_URL: Optional[str]
    Plan_URL: str
    Notes: Optional[str]
    ExtractDate: datetime.datetime
