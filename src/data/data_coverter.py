from typing import List
import pandas as pd
from pydantic import BaseModel


class DataConverter:

    @staticmethod
    def basemodel_to_dataframe(basemodel: List[BaseModel]):
        return pd.DataFrame([item.dict() for item in basemodel])