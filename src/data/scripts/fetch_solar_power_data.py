from src.data.data_coverter import DataConverter
from src.data.data_saver import DataSaver
from src.data.solar_production_fetcher import ProductionFetcher


def main() -> None:
    production_fetcher = ProductionFetcher()
    solar_production_data = production_fetcher.fetch_n_last(168)

    converter = DataConverter()
    df = converter.basemodel_to_dataframe(solar_production_data)

    saver = DataSaver("data/raw/fetched/", "power_plant_production.csv")
    saver.save_to_csv(df)


if __name__ == "__main__":
    main()
