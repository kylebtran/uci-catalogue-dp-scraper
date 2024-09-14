from collections import namedtuple
from typing import Optional
from bs4 import BeautifulSoup


import pandas as pd
import datetime
import requests


URL: str = (
    "https://catalogue.uci.edu/previouseditions/2022-23/thehenrysamuelischoolofengineering/departmentofmechanicalandaerospaceengineering/aerospaceengineering_bs/#sampleprogramtext"
)

YEAR_STANDINGS: list = ["Freshman", "Sophomore", "Junior", "Senior"]
TERMS: list = ["Fall", "Winter", "Spring", "Summer"]

curr_course_sequence_id: int = 0
curr_term_number: int = 0
course_id_map: dict = {}


course: namedtuple = namedtuple(
    "course",
    [
        "course_sequence_id",
        "course_name",
        "prefix",
        "number",
        "prerequisites",
        "corequisites",
        "strict_corequisites",
        "credit_hours",
        "canonical_name",
        "term_number",
        "course_url",
        "plan_url",
        "notes",
        "extract_date",
    ],
)


def get_soup(url: str) -> BeautifulSoup:
    response: requests.Response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_df(soup: BeautifulSoup) -> pd.DataFrame:
    global course_id_map
    data: list = []

    table = soup.find("table", class_="sc_plangrid")
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

    return pd.DataFrame(data)


def split_df(df: pd.DataFrame) -> list[pd.DataFrame]:
    idx, dfs = [], []

    for i, value in enumerate(df.iloc[:, 0]):
        if value in YEAR_STANDINGS:
            idx.append(i)
    idx.append(len(df))

    for i in range(len(idx) - 1):
        dfs.append(df.iloc[idx[i] : idx[i + 1]])

    return dfs


def get_class_info(info: Optional[str | dict]) -> list:
    global curr_course_sequence_id, curr_term_number, course_id_map

    if not info:
        return None

    elif info in YEAR_STANDINGS:
        return info

    elif info in TERMS:
        curr_term_number += 1
        return info

    course_sequence_id = (curr_course_sequence_id := curr_course_sequence_id + 1)

    if isinstance(info, str):
        course_name = info
        prefix = "GE"
        number = "999"
        prerequisites = None
        corequisites = None
        credit_hours = 4
        course_url = None

    else:
        course_url = next(iter(info.values()))
        prefix, number = next(iter(info.keys())).split("\xa0")

        soup = get_soup("https://catalogue.uci.edu" + course_url)

        dr = {}
        paragraphs = soup.find("div", class_="courseblockdesc").find_all("p")
        for p in paragraphs:
            for keyword, var in [
                ("Prerequisite:", "prerequisites"),
                ("Corequisite:", "corequisites"),
            ]:
                if keyword in p.get_text():
                    anchors = p.find_all("a")
                    dr[var] = ", ".join(
                        set(
                            anchor.get_text().replace("\xa0", " ") for anchor in anchors
                        )
                    )

        course_name, credit_hours = (
            soup.find("div", class_="search-courseresult")
            .find("h2")
            .text.replace(f"{prefix}\xa0{number}.  ", "")
        ).rsplit(".", 2)[:2]
        prerequisites = ", ".join(
            [
                str(course_id_map[prereq])
                for prereq in dr.get("prerequisites", "").split(", ")
                if prereq in course_id_map.keys()
            ]
        )
        corequisites = ", ".join(
            [
                str(course_id_map[prereq])
                for prereq in dr.get("corequisites", "").split(", ")
                if prereq in course_id_map.keys()
            ]
        )
        credit_hours = credit_hours[2]

        course_id_map[f"{prefix} {number}"] = course_sequence_id

    canonical_name = None
    term_number = curr_term_number
    strict_corequisites = None
    plan_url = URL
    notes = None
    extract_date = datetime.datetime.now(datetime.timezone.utc)

    return course(
        course_sequence_id,
        course_name,
        prefix,
        number,
        prerequisites,
        corequisites,
        strict_corequisites,
        credit_hours,
        canonical_name,
        term_number,
        course_url,
        plan_url,
        notes,
        extract_date,
    )


def format_export(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    rows: list = []

    for df_each in dfs:
        for _, row in df_each.iterrows():
            for cell in row:
                if isinstance(cell, course):
                    rows.append(list(cell))

    return pd.DataFrame(rows, columns=course._fields)


def main() -> None:
    soup = get_soup(URL)
    df = get_df(soup)

    dfs = [df_each.map(get_class_info) for df_each in split_df(df)]
    export = format_export(dfs).sort_values(by="course_sequence_id")

    export.to_clipboard(index=False, header=False)

    print("Tasks Completed Successfully")


if __name__ == "__main__":
    main()
