import pandas as pd


def main():
    df_historical = pd.read_csv("data/processed/data_historical_full_features.csv")
    df_power_plant_production = pd.read_csv("data/raw/fetched/power_plant_production.csv")
    df_weather = pd.read_csv("data/raw/fetched/weather.csv")

    df_power_plant_production['time'] = pd.to_datetime(df_power_plant_production['time'])
    df_power_plant_production['kw'] = df_power_plant_production['power'] * 1000
    df_weather['time'] = pd.to_datetime(df_weather['time'])

    df_historical['timestamp'] = pd.to_datetime(df_historical['timestamp'])
    df_historical.dropna()

    df = pd.merge(df_power_plant_production, df_weather, left_on='time', right_on='time', how='inner')

    for column in df.columns:
        df.rename(columns={column: column.split()[0].lower()}, inplace=True)

    print(df_historical.columns)
    print(df.columns)

    df = df.dropna()
    df['timestamp'] = df['time']

    df = pd.concat([df_historical, df], ignore_index=True)
    df.sort_values(by='timestamp', inplace=True)

    df.dropna(axis=1, inplace=True)
    df.drop(columns=['time'], inplace=True)

    print(df.columns)

    df.to_csv("data/processed/data_full_features.csv", index=False, header=True)


if __name__ == "__main__":
    main()
