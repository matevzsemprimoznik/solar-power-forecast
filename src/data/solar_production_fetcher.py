from datetime import datetime, timezone
import requests

from src.data.models.production import Production
from src.config.settings import settings


class ProductionFetcher:
    data_uri = settings.POWER_PLANT_API_URI

    def fetch_n_last(self, n: int = 1, step: int = 60):
        response = requests.get(self.data_uri)
        raw_data_full = response.json()

        raw_data = raw_data_full[0].get('args')[1][0].get('results')
        raw_data['timestamp'] = raw_data['timestamp'][::-1]
        raw_data['mw'] = raw_data['mw'][::-1]

        results = []

        first_date = datetime.fromtimestamp(raw_data['timestamp'][0], timezone.utc)
        offset = (first_date.hour * 60 + first_date.minute) % step
        raw_data['timestamp'] = raw_data['timestamp'][offset:]
        raw_data['mw'] = raw_data['mw'][offset:]

        for i, date in enumerate(raw_data['timestamp']):
            if i % step != 0:
                continue

            results.append(
                Production(
                    time=datetime.fromtimestamp(date, timezone.utc).replace(minute=0, second=0, microsecond=0).replace(tzinfo=None),
                    power=raw_data['mw'][i]
                )
            )
            if len(results) == n:
                break

        return results
