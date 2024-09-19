from sample_dp_scrapers.sample_dp_scraper_2020_24 import Scraper
from typing import Generator


import pandas as pd
import os


# TODO:
# 1. Search second layer course results by their h2 course name before reading paragraph details.


YEARS = ["2020-21", "2021-22", "2022-23", "2023-24"]


def process_urls(file_path: str) -> list:
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines() if line.startswith("https://catalogue.uci.edu")]
    

def apply_year_range(urls: list) -> Generator[str, None, None]:
    global YEARS

    for url in urls:
        for year in YEARS:
            yield url.replace(url.split('/')[4], year) 


def main():
    global YEARS

    urls = process_urls("urls.txt")

    os.makedirs("sample_dp_exports", exist_ok=True)

    for idx, url in enumerate(apply_year_range(urls)):
        try:
            scraper = Scraper(url)
            df: pd.DataFrame = scraper.scrape()

            file_name: str = df.iloc[1, 3].split(" ", 1)[1].replace(" ", "_").replace(":", "").replace("/", "")
            subdir_name: str = f"sample_dp_exports/{df.iloc[1, 2].replace(" ", "_")}"

            os.makedirs(subdir_name, exist_ok=True)

            df.to_csv(
                os.path.join(subdir_name, f"UCI_DegreePlan_{file_name}.csv"),
                index=False,
            )

            print(f"({idx + 1}/{len(urls * len(YEARS))}) Success")

        except Exception as e:
            print(f"({idx + 1}/{len(urls * len(YEARS))}) Failure ({url}: {e})")


if __name__ == "__main__":
    main()
