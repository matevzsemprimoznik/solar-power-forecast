from src.config.constants import FETCH_WINDOW_IN_HOURS
from src.data.data_coverter import DataConverter
from src.data.data_saver import DataSaver
from src.data.weather_fetcher import WeatherFetcher


def main() -> None:
    weather_fetcher = WeatherFetcher()
    weather_data = weather_fetcher.fetch_data(None, FETCH_WINDOW_IN_HOURS)

    converter = DataConverter()
    df = converter.basemodel_to_dataframe(weather_data)

    saver = DataSaver("data/raw/fetched/", "weather.csv")
    saver.save_to_csv(df)


if __name__ == "__main__":
    main()
