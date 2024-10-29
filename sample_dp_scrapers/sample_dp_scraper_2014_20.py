from typing import Generator, NamedTuple, Optional
from bs4 import BeautifulSoup


import pandas as pd
import datetime
import requests
import re


from sample_dp_scrapers.types import Header, Course, YEAR_STANDINGS, TERMS


class Scraper:
    def __init__(self, url: str) -> None:
        self.url = url
        self.curr_course_sequence_id = 0
        self.curr_term_number = 0
        self.course_id_map = {}

    def reset(self) -> None:
        self.curr_course_sequence_id = 0
        self.curr_term_number = 0
        self.course_id_map = {}

    def get_class_info(self, info: Optional[str | dict]) -> list:
        if not info:
            return None

        elif info in YEAR_STANDINGS:
            return info

        elif info in TERMS:
            self.curr_term_number += 1
            return info

        self.curr_course_sequence_id += 1
        self.course_sequence_id = self.curr_course_sequence_id

        if isinstance(info, str):
            course_name = info
            prefix = "GE"
            number = "999"
            prerequisites = None
            corequisites = None
            credit_hours = 4
            course_url = None

        else:
            course_url = "/".join(self.url.split("/")[:5]) + next(iter(info.values()))
            prefix, number = next(iter(info.keys())).rsplit("\xa0", 1)

            soup = get_soup(course_url)

            dr = {}
            try:
                paragraphs = soup.find("div", class_="courseblockdesc").find_all("p")
            except:
                soup = get_soup(re.sub(r"\d{4}-\d{2}", "2019-20", course_url))
                paragraphs = soup.find("div", class_="courseblockdesc").find_all("p")
            for p in paragraphs:
                for keyword, var in [
                    ("Prerequisite:", "Prerequisites"),
                    ("Prerequisite or corequisite:", "Prerequisites"),
                    ("Corequisite:", "Corequisites"),
                ]:
                    if keyword in p.get_text():
                        anchors = p.find_all("a")
                        dr[var] = ", ".join(
                            set(
                                anchor.get_text().replace("\xa0", " ")
                                for anchor in anchors
                            )
                        )

            try:
                course_name, credit_hours = (
                    soup.find("div", class_="searchresult")
                    .find("h2")
                    .text.replace(f"{prefix}\xa0{number}.  ", "")
                ).rsplit(".", 2)[:2]
            except:
                course_name, credit_hours = "ERROR", "ERROR"
            prerequisites = ", ".join(
                sorted(  # Sorted not working
                    str(self.course_id_map[prereq])
                    for prereq in dr.get("Prerequisites", "").split(", ")
                    if prereq in self.course_id_map.keys()
                )
            )
            corequisites = ", ".join(
                sorted(  # Sorted not working
                    str(self.course_id_map[prereq])
                    for prereq in dr.get("Corequisites", "").split(", ")
                    if prereq in self.course_id_map.keys()
                )
            )
            credit_hours = credit_hours[2]

            self.course_id_map[f"{prefix} {number}"] = self.course_sequence_id

        canonical_name = None
        term_number = self.curr_term_number
        strict_corequisites = None
        plan_url = self.url
        notes = None
        extract_date = datetime.datetime.now(datetime.timezone.utc)

        return Course(
            CourseSequenceID=self.course_sequence_id,
            CourseName=course_name,
            Prefix=prefix,
            Number=number,
            Prerequisites=prerequisites,
            Corequisites=corequisites,
            Strict_Corequisites=strict_corequisites,
            CreditHours=credit_hours,
            CanonicalName=canonical_name,
            TermNumber=term_number,
            Course_URL=course_url,
            Plan_URL=plan_url,
            Notes=notes,
            ExtractDate=extract_date,
        )

    def scrape(self) -> list[pd.DataFrame]:
        exports: list = []
        soup = get_soup(self.url)
        row_headers = get_headers(soup)
        dfs = get_dfs(soup)

        for row_header, df in zip(row_headers, dfs):
            mdfs = [
                df_each.map(lambda x: self.get_class_info(x))
                for df_each in split_df(df)
            ]
            exports.append(
                format_export(row_header, mdfs).sort_values(by="CourseSequenceID")
            )

            self.reset()

        return exports


def get_soup(url: str) -> BeautifulSoup:
    response: requests.Response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_dfs(soup: BeautifulSoup) -> list[pd.DataFrame]:
    dfs: list[pd.DataFrame] = []

    tables = soup.find_all("table", class_="sc_plangrid")
    for table in tables:
        data = []

        for row in table.find_all("tr"):
            row_data: list = []

            for cell in row.find_all(["td", "th"]):
                anchor = cell.find("a")
                if anchor:
                    row_data.append(
                        {cell.text.strip().split(" ")[0].strip("*"): anchor.get("href")}
                    )
                else:
                    row_data.append(cell.text.strip())
            data.append(row_data)

        df = pd.DataFrame(data)
        dfs.append(df)

    return dfs


def get_headers(soup: BeautifulSoup) -> list[Header]:
    headers = []

    degree_plan_id = None
    institution = "University of California, Irvine"
    system_type = "Quarter"
    cip = "26.0101"
    header_sections = soup.find_all(
        ["h4", "h3"], string=lambda s: s and "Requirements for the" in s
    )

    for header_section in header_sections:
        if "Minor" in header_section.get_text():
            continue

        academic_year = soup.find("div", id="edition").get_text().strip()[:7]
        degree_type, curriculum = header_section.get_text().rsplit(" in ", 1)
        degree_plan = "Catalogue Sample"
        degree_type = (
            degree_type.replace(".", "")
            .replace("Degree", "")
            .replace("Requirements for the ", "")
            .strip()
        )
        curriculum = f"{degree_type} {curriculum}"

        header = Header(
            DegreePlanID=degree_plan_id,
            Institution=institution,
            AcademicYear=academic_year,
            Curriculum=curriculum,
            DegreePlan=degree_plan,
            DegreeType=degree_type,
            SystemType=system_type,
            CIP=cip,
        )

        headers.append(header)

    return headers


def split_df(df: pd.DataFrame) -> list[pd.DataFrame]:
    idx, dfs = [], []

    for i, value in enumerate(df.iloc[:, 0]):
        if value in YEAR_STANDINGS:
            idx.append(i)
    idx.append(len(df))

    for i in range(len(idx) - 1):
        dfs.append(df.iloc[idx[i] : idx[i + 1]])

    return dfs


def format_export(row_header: Header, dfs: list[pd.DataFrame]) -> pd.DataFrame:
    rows: list = []

    for df_each in dfs:
        for _, row in df_each.iterrows():
            for cell in row:
                if isinstance(cell, Course):
                    rows.append([cell.CourseSequenceID, *row_header[1:], *cell])

    return pd.DataFrame(rows, columns=[*Header._fields, *Course._fields])
