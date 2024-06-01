import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


def drift():
    report = Report(metrics=[DataDriftPreset()])

    current_data = pd.read_csv("data/validation/current.csv")
    reference_data = pd.read_csv("data/validation/reference.csv")

    report.run(reference_data=reference_data, current_data=current_data)

    report.save_html("reports/data_drift.html")


if __name__ == "__main__":
    drift()
