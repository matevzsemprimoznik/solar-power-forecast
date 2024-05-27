from pydantic import BaseModel
from datetime import datetime


class Weather(BaseModel):
    time: datetime
    temperature_2m: float
    relative_humidity_2m: float
    dew_point_2m: float
    apparent_temperature: float
    rain: float
    pressure_msl: float
    cloud_cover: float
    cloud_cover_low: float
    cloud_cover_mid: float
    cloud_cover_high: float
    wind_speed_10m: float
    wind_direction_10m: float
    wind_gusts_10m: float
    shortwave_radiation_instant: float
    direct_radiation_instant: float
    diffuse_radiation_instant: float
    direct_normal_irradiance_instant: float
    terrestrial_radiation_instant: float

    class Config:
        fields = {
            'temperature_2m': 'temperature_2m (°C)',
            'relative_humidity_2m': 'relative_humidity_2m (%)',
            'dew_point_2m': 'dew_point_2m (°C)',
            'apparent_temperature': 'apparent_temperature (°C)',
            'rain': 'rain (mm)',
            'pressure_msl': 'pressure_msl (hPa)',
            'cloud_cover': 'cloud_cover (%)',
            'cloud_cover_low': 'cloud_cover_low (%)',
            'cloud_cover_mid': 'cloud_cover_mid (%)',
            'cloud_cover_high': 'cloud_cover_high (%)',
            'wind_speed_10m': 'wind_speed_10m (km/h)',
            'wind_speed_100m': 'wind_speed_100m (km/h)',
            'wind_direction_10m': 'wind_direction_10m (°)',
            'wind_direction_100m': 'wind_direction_100m (°)',
            'wind_gusts_10m': 'wind_gusts_10m (km/h)',
            'shortwave_radiation_instant': 'shortwave_radiation_instant (W/m²)',
            'direct_radiation_instant': 'direct_radiation_instant (W/m²)',
            'diffuse_radiation_instant': 'diffuse_radiation_instant (W/m²)',
            'direct_normal_irradiance_instant': 'direct_normal_irradiance_instant (W/m²)',
            'terrestrial_radiation_instant': 'terrestrial_radiation_instant (W/m²)',
        }
