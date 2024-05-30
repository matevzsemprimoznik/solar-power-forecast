import pandas as pd
from src.config.constants import POWER_PLANT_PRODUCTION_TARGET, SEED
from sklearn.model_selection import train_test_split


def prepare_data():
    df = pd.read_csv("data/processed/data_selected_features.csv")
    X = df.drop(columns=[POWER_PLANT_PRODUCTION_TARGET])
    y = df[POWER_PLANT_PRODUCTION_TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=SEED)

    print('Splitted data shapes:')
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"y_test shape: {y_test.shape}\n")

    return X_train, X_test, y_train, y_test
