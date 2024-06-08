import os
import dvc.api
from src.config.settings import setting

def download_data_for_model_train():
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
        if not os.path.exists('data/processed'):
            os.makedirs('data/processed')
        with open('data_selected_features.csv', 'w') as file:
            file.write(f.read())


if __name__ == "__main__":
    download_data_for_model_train()
