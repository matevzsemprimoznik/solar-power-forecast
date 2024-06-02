from datetime import datetime
from typing import List

import numpy as np
import pandas as pd
from pandas import NaT

from src.apps.api.models.predictions import PredictionMultipleOutput
from src.apps.api.utils.utils import convert_to_datetime
from src.config.constants import POWER_PRODUCTION_MODEL_NAME, SOLAR_RADIATION_MODEL_NAME
from src.data.solar_production_fetcher import ProductionFetcher
from src.data.time_fetcher import TimeFetcher
from src.data.weather_fetcher import WeatherFetcher
from src.models.common.model_registry import get_artifact


class ProductionService:
    def __init__(self):
        self.power_production_artifact = get_artifact(POWER_PRODUCTION_MODEL_NAME, "production")
        self.solar_radiation_artifact = get_artifact(SOLAR_RADIATION_MODEL_NAME, "production")

    def predict(self):
        return self.predict_n_next(n_next=1)[0]

    def predict_n_next(self, n_next: int):
        weather_data = WeatherFetcher().fetch_data(n_next=n_next)
        weather_data = weather_data[1:]

        df = pd.DataFrame.from_records([item.dict() for item in weather_data])

        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['day'] = df['time'].dt.day
        df['hour'] = df['time'].dt.hour

        solar_radiation_model_input = []

        for i, row in df.iterrows():
            element = {}

            for item in self.solar_radiation_artifact.get('metadata'):
                element[item.value] = row[item.key]

            solar_radiation_model_input.append(element)

        solar_radiation_model_input = pd.DataFrame(solar_radiation_model_input)

        solar_radiation_model = self.solar_radiation_artifact.get('model')

        model_predictions = \
        solar_radiation_model.run(None, {'input': solar_radiation_model_input.values.astype(np.float32)})[0]

        print(model_predictions)

        df['solar_radiation_predicted'] = model_predictions

        print(df.head())

        power_production_model_input = []

        for i, row in df.iterrows():
            element = {}

            for item in self.power_production_artifact.get('metadata'):
                element[item.value] = row[item.key]

            power_production_model_input.append(element)

        power_production_model_input = pd.DataFrame(power_production_model_input)

        power_production_model = self.power_production_artifact.get('model')

        model_predictions = \
        power_production_model.run(None, {'input': power_production_model_input.values.astype(np.float32)})[0]

        df['power_production_predicted'] = model_predictions

        df_predictions = df[['time', 'power_production_predicted']].copy(deep=True)
        df_predictions.rename(columns={'power_production_predicted': 'power'}, inplace=True)
        df_predictions.rename(columns={'time': 'date'}, inplace=True)

        return df_predictions.to_dict(orient='records')

    def history(self, start_date_str, end_date_str):
        try:
            start_date = convert_to_datetime(start_date_str)
            end_date = convert_to_datetime(end_date_str)
        except ValueError as e:
            raise ValueError(e)

        if start_date is None or start_date is NaT:
            start_date = pd.Timestamp.now() - pd.DateOffset(weeks=1)

        if end_date is None or end_date is NaT:
            end_date = pd.Timestamp.now()

        if start_date > end_date:
            raise ValueError("Start date cannot be greater than end date")

        if start_date == end_date:
            end_date = end_date + pd.DateOffset(days=1) - pd.DateOffset(hours=1)

        current_date = TimeFetcher().fetch_gtm_time()

        difference_in_hours = int((current_date - start_date).total_seconds() / 3600) + 1

        production_fetcher = ProductionFetcher()
        production_data = production_fetcher.fetch_n_last(difference_in_hours)

        production_data = [data.dict() for data in production_data if start_date <= data.time <= end_date]

        return production_data[::-1]
