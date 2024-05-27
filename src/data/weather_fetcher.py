from datetime import datetime, timezone, timedelta
import requests
from dateutil import parser
from src.data.models.weather import Weather
from src.config.settings import settings
from src.data.time_fetcher import TimeFetcher


class WeatherFetcher:
    data_uri = settings.WEATHER_API_URI

    def fetch_data(self, n_next = None):
        response = requests.get(self.data_uri)
        raw_data = response.json()
        hourly_data = raw_data['hourly']

        results = []

        time_fetcher = TimeFetcher()
        target_date = time_fetcher.fetch_gtm_time()
        if n_next is None:
            target_date = target_date - timedelta(hours=1)

        for i, date in enumerate(hourly_data['time']):
            date = parser.parse(date)
            if date < target_date:
                continue
            results.append(
                Weather(
                    time=date,
                    temperature_2m=hourly_data['temperature_2m'][i],
                    relative_humidity_2m=hourly_data['relative_humidity_2m'][i],
                    dew_point_2m=hourly_data['dew_point_2m'][i],
                    apparent_temperature=hourly_data['apparent_temperature'][i],
                    rain=hourly_data['rain'][i],
                    pressure_msl=hourly_data['pressure_msl'][i],
                    cloud_cover=hourly_data['cloud_cover'][i],
                    cloud_cover_low=hourly_data['cloud_cover_low'][i],
                    cloud_cover_mid=hourly_data['cloud_cover_mid'][i],
                    cloud_cover_high=hourly_data['cloud_cover_high'][i],
                    wind_speed_10m=hourly_data['wind_speed_10m'][i],
                    wind_direction_10m=hourly_data['wind_direction_10m'][i],
                    wind_gusts_10m=hourly_data['wind_gusts_10m'][i],
                    shortwave_radiation_instant=hourly_data['shortwave_radiation_instant'][i],
                    direct_radiation_instant=hourly_data['direct_radiation_instant'][i],
                    diffuse_radiation_instant=hourly_data['diffuse_radiation_instant'][i],
                    direct_normal_irradiance_instant=hourly_data['direct_normal_irradiance_instant'][i],
                    terrestrial_radiation_instant=hourly_data['terrestrial_radiation_instant'][i]
                )
            )
            if len(results) == n_next or n_next is None:
                break

        return results

    def fetch_next_n_hours(self, n: int):
        return self.fetch_data(n)
