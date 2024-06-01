from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score


def evaluate_model_performance(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    evs = explained_variance_score(y_true, y_pred)

    return mse, mae, evs
