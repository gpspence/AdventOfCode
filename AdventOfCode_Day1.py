import numpy as np
from aocd import get_data, submit

# Get the data
data = get_data(day=1, year=2024)
data = data.split("\n")  # split on each newline, to get pairs of values
data = [x.split("   ") for x in data]  # nested rows as list
col_1, col_2 = np.array(list(zip(*data))).astype(int)

# Part A - Comparing sorted arrays
assert len(col_1) == len(col_2)
diff = np.abs(np.sort(col_1) - np.sort(col_2))
total_diff = diff.sum()
submit(total_diff, part='a', day=1, year=2024)

# Part B - Comparing the mode of a given value
value, counts = np.unique(col_2, return_counts=True)
mapping = {x[0]: x[1] for x in zip(value, counts)}
total = 0
for row in col_1:
    if row in mapping.keys():
        total += row * mapping[row]  # could use .count instead of mapping
submit(total, part='B', day=1, year=2024)
