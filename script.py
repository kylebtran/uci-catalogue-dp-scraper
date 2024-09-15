from sample_dp_scrapers import sample_dp_scraper_2020_24


import pandas as pd
import os


# TODO:
# Search second layer course results by their h2 course name before reading paragraph details.


URLS: list = [
    "https://catalogue.uci.edu/previouseditions/2022-23/thehenrysamuelischoolofengineering/departmentofmechanicalandaerospaceengineering/aerospaceengineering_bs/#sampleprogramtext",
    "https://catalogue.uci.edu/previouseditions/2023-24/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/computerscience_bs/",

]


def main():
    for idx, url in enumerate(URLS):
        try:
            df: pd.DataFrame = sample_dp_scraper_2020_24.scrape(url)

            file_name: str = df.iloc[1, 3].split(" ", 1)[1].replace(" ", "_")
            subdir_name: str = f"sample_dp_exports/{df.iloc[1, 2].replace(" ", "_")}"

            os.makedirs(subdir_name, exist_ok=True)

            df.to_csv(
                os.path.join(subdir_name, f"UCI_DegreePlan_{file_name}.csv"),
                index=False,
            )

            print(f"({idx + 1}/{len(URLS)}) Success")

        except Exception as e:
            print(f"({idx + 1}/{len(URLS)}) Failure ({url}: {e})")


if __name__ == "__main__":
    main()
