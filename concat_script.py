import pandas as pd
import glob


MAJORS = ["Aerospace Engineering"]


def main() -> None:
    for idx, major in enumerate(MAJORS):
        try:
            dps: list[str] = sorted(
                glob.glob(
                    f"sample_dp_exports/**/UCI_DegreePlan_{major.replace(' ', '_')}.csv",
                    recursive=True,
                )
            )
            dfs: list[pd.Dataframe] = [pd.read_csv(dp) for dp in dps]
            df: pd.DataFrame = pd.concat(dfs, ignore_index=True)

            df.to_csv(f"sample_dp_exports/UCI_DegreePlan_{major.replace(' ', '_')}.csv")

            print(f"({idx + 1}/{len(MAJORS)}) Success ({major})")

        except Exception as e:
            print(f"({idx + 1}/{len(MAJORS)}) Failure ({major}: {e})")


if __name__ == "__main__":
    main()
