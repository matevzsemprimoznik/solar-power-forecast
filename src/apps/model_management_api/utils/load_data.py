import os
import dvc.api

from src.config.settings import settings


def download_data_for_model_train():
    print("Downloading data for model training")

    try:
        os.environ["GIT_PYTHON_REFRESH"] = "quiet"
        with dvc.api.open(
                'data/processed/data_selected_features.csv',
                repo=settings.DAGSHUB_REPO_URI,
                mode='r',
                remote_config={
                    "access_key_id": settings.DAGSHUB_ACCESS_KEY_ID,
                    "secret_access_key": settings.DAGSHUB_ACCESS_SECRET_KEY
                }
        ) as f:
            print("Data downloaded successfully")
            if not os.path.exists('data/processed'):
                os.makedirs('data/processed')
            with open('data/processed/data_selected_features.csv', 'w') as file:
                file.write(f.read())

    except Exception as e:
        print("An error occurred while downloading data:", e)


if __name__ == "__main__":
    download_data_for_model_train()
