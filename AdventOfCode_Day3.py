import numpy as np
import re
from aocd import submit, get_data
from typing import List, Match


def calculate_product(match: Match) -> int:
    """
    Given a match object, calculate multiplication of first and second
    capture groups.
    Args:
        match: re match object
    Returns:
        [int]: multiplication of first and second capture groups
    """
    return int(match.group(1)) * int(match.group(2))


# Part A - Multiplications from corrupted data
# Working with test data
test_str = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
main_pattern = r'mul\((\d+),(\d+)\)'  # pattern to match "mul(#,#)"
test_extracted = re.finditer(main_pattern, test_str)  # find all occurences
test_sum_prod = sum(list(map(calculate_product, test_extracted)))

# Get the puzzle
data = get_data(day=3, year=2024)
extracted = re.finditer(main_pattern, data)
sum_prod = sum(list(map(calculate_product, extracted)))
# submit(sum_prod, part='a', day=3, year=2024)

# Part B - Activate and deactivate statements
test_str_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
dont_pattern = r'don\'t\(\)'
do_pattern = r'do\(\)'
test_extracted_2 = re.finditer(main_pattern, test_str_2)
test_extract_do = re.finditer(do_pattern, test_str_2)
test_extract_dont = re.finditer(dont_pattern, test_extracted_2)
state = True
