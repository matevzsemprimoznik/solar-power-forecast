from datetime import datetime, timezone
import requests
import time
from src.data.models.production import Production
from src.config.settings import settings


class ProductionFetcher:
    data_uri = settings.POWER_PLANT_API_URI

    def fetch_n_last(self, n: int = 1, step: int = 60):
        attempts = 0
        response = None
        retries = 3
        delay = 5

        while attempts < retries:
            try:
                response = requests.get(self.data_uri)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                print(f"Attempt {attempts + 1} failed: {e}")
                attempts += 1
                if attempts < retries:
                    time.sleep(delay)
                else:
                    raise Exception("Failed to fetch data after multiple attempts")

        raw_data_full = response.json()

        raw_data = raw_data_full[0].get('args')[1][0].get('results')
        raw_data['timestamp'] = raw_data['timestamp'][::-1]
        raw_data['mw'] = raw_data['mw'][::-1]

        results = []

        first_date = datetime.fromtimestamp(raw_data['timestamp'][0], timezone.utc).replace(tzinfo=None)
        offset = (first_date.hour * step + first_date.minute) % step
        raw_data['timestamp'] = raw_data['timestamp'][offset:]
        raw_data['mw'] = raw_data['mw'][offset:]

        for i, date in enumerate(raw_data['timestamp']):
            if i % step != 0:
                continue

            results.append(
                Production(
                    time=datetime.fromtimestamp(date, timezone.utc).replace(tzinfo=None),
                    power=raw_data['mw'][i] * 1000000
                )
            )
            if len(results) == n:
                break

        return results
