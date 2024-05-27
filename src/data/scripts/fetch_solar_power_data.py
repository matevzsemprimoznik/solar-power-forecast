from src.data.solar_production_fetcher import ProductionFetcher


def main() -> None:
    production_fetcher = ProductionFetcher()
    solar_production_data = production_fetcher.fetch_n_last()

    print(solar_production_data)


if __name__ == "__main__":
    main()
