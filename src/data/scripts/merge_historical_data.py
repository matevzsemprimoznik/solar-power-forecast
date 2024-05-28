import pandas as pd


def main():
    df_2016 = pd.read_csv("data/raw/historical/BS_2016.csv")
    df_2017 = pd.read_csv("data/raw/historical/BS_2017.csv")
    df_2018 = pd.read_csv("data/raw/historical/BS_2018.csv")
    df_2019 = pd.read_csv("data/raw/historical/BS_2019.csv")
    df_2020 = pd.read_csv("data/raw/historical/BS_2020.csv")
    df_2021 = pd.read_csv("data/raw/historical/BS_2021.csv")
    df_2022 = pd.read_csv("data/raw/historical/BS_2022.csv")

    df = pd.concat([df_2016, df_2017, df_2018, df_2019, df_2020, df_2021, df_2022])

    df.sort_values(by="Timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)

    df.to_csv("data/raw/historical/power_plant_production.csv", index=False, header=True)


if __name__ == "__main__":
    main()