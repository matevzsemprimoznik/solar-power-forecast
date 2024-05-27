from src.data.weather_fetcher import WeatherFetcher


def main() -> None:
    weather_fetcher = WeatherFetcher()
    weather_data = weather_fetcher.fetch_data()

    print(weather_data)


if __name__ == "__main__":
    main()
