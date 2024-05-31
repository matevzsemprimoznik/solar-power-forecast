import os.path

from pandas import DataFrame


class DataSaver:

    def __init__(self, path: str, file_name: str):
        self.path = path
        self.file_name = file_name

    def save_to_csv(self, data: DataFrame):
        full_path = self.path + self.file_name

        if os.path.exists(full_path):
            data.to_csv(full_path, mode='a', header=False, index=False)
        else:
            data.to_csv(full_path, index=False)