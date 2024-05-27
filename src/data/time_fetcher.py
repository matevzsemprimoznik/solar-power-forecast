from datetime import datetime
import requests
from src.config.settings import settings


class TimeFetcher:
    time_api_uri = settings.TIME_API_URI

    def fetch_gtm_time(self):
        current_gtm_time_response = requests.get(self.time_api_uri)
        if current_gtm_time_response.status_code != 200:
            raise Exception('Problems fetching GTM time')

        current_gtm_time = current_gtm_time_response.json()['dateTime']
        current_gtm_time = current_gtm_time.split('.')[0]

        current_gtm_time = datetime.strptime(current_gtm_time, "%Y-%m-%dT%H:%M:%S")
        return current_gtm_time
