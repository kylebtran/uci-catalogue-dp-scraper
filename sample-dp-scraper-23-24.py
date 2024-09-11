from bs4 import BeautifulSoup


import pandas as pd
import requests


URL: str = (
    "https://catalogue.uci.edu/previouseditions/2022-23/thehenrysamuelischoolofengineering/departmentofmechanicalandaerospaceengineering/aerospaceengineering_bs/#sampleprogramtext"
)


def get_soup(url: str) -> BeautifulSoup:
    response: requests.Response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_df(soup: BeautifulSoup) -> pd.DataFrame:
    data: list = []

    table = soup.find("table", class_="sc_plangrid")
    for row in table.find_all("tr"):
        row_data: list = []

        for cell in row.find_all(["td", "th"]):
            anchor = cell.find("a")
            if anchor:
                row_data.append(
                    {cell.text.strip().replace("\xa0", " "): anchor.get("href")}
                )
            else:
                row_data.append(cell.text.strip())
        data.append(row_data)

    return pd.DataFrame(data)


def get_class_info(info: dict) -> dict:
    pass


def main():
    soup = get_soup(URL)
    df = get_df(soup)

    df.to_clipboard(index=False, header=False)


if __name__ == "__main__":
    main()
