import pandas as pd


def main():
    df_power_plant_production = pd.read_csv("data/raw/historical/power_plant_production.csv")
    df_weather = pd.read_csv("data/raw/historical/weather.csv")

    df_power_plant_production['Timestamp'] = pd.to_datetime(df_power_plant_production['Timestamp'])
    df_weather['time'] = pd.to_datetime(df_weather['time'])

    df = pd.merge(df_power_plant_production, df_weather, left_on='Timestamp', right_on='time', how='inner')

    for column in df.columns:
        df.rename(columns={column: column.split()[0].lower()}, inplace=True)

    df = df.dropna()

    df.to_csv("data/processed/data_historical_full_features.csv", index=False, header=True)


if __name__ == "__main__":
    main()
