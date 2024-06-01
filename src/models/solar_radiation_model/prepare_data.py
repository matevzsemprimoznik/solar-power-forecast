import pandas as pd
from sklearn.model_selection import train_test_split

from src.config.column_names_serializer import serialize_column_names
from src.config.constants import POWER_PLANT_PRODUCTION_TARGET, SOLAR_RADIATION_TARGET, SEED


def prepare_solar_radiation_model_data():
    df = pd.read_csv("data/processed/data_selected_features.csv")

    X = df.drop(columns=[POWER_PLANT_PRODUCTION_TARGET, SOLAR_RADIATION_TARGET])
    column_names_map = serialize_column_names(X.columns)
    X.columns = column_names_map.values()

    y = df[SOLAR_RADIATION_TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=SEED)

    return X_train, X_test, y_train, y_test, column_names_map
