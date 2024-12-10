import numpy as np
from aocd import submit, get_data


def clean_data(data):
    cleaned_data = data.split('\n')
    cleaned_data = np.array([list(x) for x in cleaned_data])
    return cleaned_data


# Part A - Solving a word search
test_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
test_data = clean_data(test_data)
print(test_data)
