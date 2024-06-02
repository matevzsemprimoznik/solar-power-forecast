import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.config.column_names_serializer import serialize_column_names
from src.config.constants import POWER_PLANT_PRODUCTION_TARGET, SEED, SOLAR_RADIATION_MODEL_NAME
from src.models.common.model_registry import get_artifact
from src.models.solar_radiation_model.prepare_data import prepare_solar_radiation_model_data


def prepare_power_production_model_data():
    X_train, X_test, y_train, y_test, _ = prepare_solar_radiation_model_data()
    X = pd.concat([X_train, X_test], axis=0)

    model = get_artifact(SOLAR_RADIATION_MODEL_NAME, "production").get('model')

    model_predictions = model.run(None, {'input': X.values.astype(np.float32)})[0]

    df = pd.read_csv("data/processed/data_selected_features.csv")

    df['solar_radiation_predicted'] = model_predictions

    X = df.drop(columns=[POWER_PLANT_PRODUCTION_TARGET])
    column_names_map = serialize_column_names(X.columns)
    X.columns = column_names_map.values()

    y = df[POWER_PLANT_PRODUCTION_TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=SEED)

    return X_train, X_test, y_train, y_test, column_names_map