import pandas as pd
from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset, NoTargetPerformanceTestPreset
from evidently.tests import TestNumberOfColumnsWithMissingValues, TestNumberOfRowsWithMissingValues, TestNumberOfConstantColumns, TestNumberOfDuplicatedRows, TestNumberOfDuplicatedColumns, TestColumnsType, TestNumberOfDriftedColumns


def stability():
    tests = TestSuite(tests=[
        TestNumberOfColumnsWithMissingValues(),
        TestNumberOfRowsWithMissingValues(),
        TestNumberOfConstantColumns(),
        TestNumberOfDuplicatedRows(),
        TestNumberOfDuplicatedColumns(),
        TestColumnsType(),
        TestNumberOfDriftedColumns(),
        NoTargetPerformanceTestPreset(),
        DataStabilityTestPreset()
    ])

    current_data = pd.read_csv("data/validation/current.csv")
    reference_data = pd.read_csv("data/validation/reference.csv")

    tests.run(reference_data=reference_data, current_data=current_data)

    tests.save_html("reports/data_stability.html")


if __name__ == "__main__":
    stability()
