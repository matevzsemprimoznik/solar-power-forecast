import pandas as pd


def main():
    df_power_plant_production = pd.read_csv("data/raw/fetched/power_plant_production.csv")
    df_weather = pd.read_csv("data/raw/fetched/weather.csv")

    df_power_plant_production['time'] = pd.to_datetime(df_power_plant_production['time'])
    df_power_plant_production['power'] = df_power_plant_production['power']
    df_weather['time'] = pd.to_datetime(df_weather['time'])

    df = pd.merge(df_power_plant_production, df_weather, left_on='time', right_on='time', how='inner')

    for column in df.columns:
        df.rename(columns={column: column.split()[0].lower()}, inplace=True)

    df = df.dropna()
    df.rename(columns={'time': 'timestamp'}, inplace=True)

    df.sort_values(by='timestamp', inplace=True)

    df.dropna(axis=1, inplace=True)

    df.drop_duplicates(subset='timestamp', inplace=True)

    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour

    print(df.columns)


    df.to_csv("data/processed/data_full_features.csv", index=False, header=True)


if __name__ == "__main__":
    main()
