import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np

from src.config.constants import POWER_PLANT_PRODUCTION_TARGET


def main():
    df = pd.read_csv("data/processed/data_full_features.csv")

    X = df.drop(columns=[POWER_PLANT_PRODUCTION_TARGET, 'timestamp'])
    y = df[POWER_PLANT_PRODUCTION_TARGET]

    model = RandomForestRegressor()
    model.fit(X, y)

    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")

    for f in range(X.shape[1]):
        print("%d. feature %s (%f)" % (f + 1, X.columns[indices[f]], importances[indices[f]]))

    X = X[X.columns[indices[:10]]]
    X[POWER_PLANT_PRODUCTION_TARGET] = y

    X.to_csv("data/processed/data_selected_features.csv", index=False, header=True)


if __name__ == "__main__":
    main()
