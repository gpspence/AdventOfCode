import numpy as np
from aocd import get_data, submit


def clean_data(data: str) -> np.array:
    """
    Clean the dirty input string.
    Args:
        data: input raw puzzle
    Returns:
        [np.array]: cleaned array of ints
    """
    data = np.array(data.split("\n"))  # split data
    data = data[~np.isin(data, [''])]
    data = np.char.split(data, sep=' ')
    return [np.array(x).astype(int) for x in data]


def test_asc_desc(report: np.array) -> bool:
    """
    Check whether a report is all increasing or all decreasing.
    Args:
        report: a row of data
    Returns:
        [bool]: True if successful, False if failure 
    """
    asc_report = np.sort(report)
    desc_report = asc_report[::-1]
    if (np.all(report == asc_report)) | np.all(report == desc_report):
        return True
    else:
        return False


def test_step_size(report: np.array) -> bool:
    """
    Check whether the step size within a level is between 1 and 3 (inclusive).
    Args:
        report: a row of data
    Returns:
        [bool]: True if successful, False if failure
    """
    report_rshift = np.insert(report, 0, 0)
    report_rshift = report_rshift[:-1]
    step = np.abs(report - report_rshift)[1:]  # take abs difference, discount first value (no diff)
    if (np.max(step) <= 3) and (np.min(step) > 0):
        return True
    else:
        return False


def run_tests(data: np.array) -> int:
    """
    Run step size and asc/desc tests on the report.
    Args:
        data: puzzle input consisting of many reports.
    Returns:
        [int]: number of safe reports
    """
    safe_reports = 0
    for report in data:
        if test_asc_desc(report) & test_step_size(report):
            safe_reports += 1
    return safe_reports


# Part A - Reactor stability data
# Develop with test data
test_data = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
test_reports = clean_data(test_data)

# Run the tests
safe_test_reports = run_tests(test_reports)
# print(safe_test_reports)

# Get the real data and run tests
data = get_data(day=2, year=2024)
reports = clean_data(data)
safe_reports = run_tests(reports)
submit(safe_reports, part='a', day=2, year=2024)
print(safe_reports)
