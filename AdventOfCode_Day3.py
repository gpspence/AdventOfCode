import re
from aocd import submit, get_data
from typing import List, Match, Iterable


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


def get_new_state(
    match: Match,
    list_do: List,
    list_dont: List,
    state: bool,
) -> bool:
    """
    Get the state (True or False) for the given match.
    If do() is most recent command, return True, if don't() return False.
    Args:(
        match: re match object for the mul(x,y) match
        list_do: re match list of all do() occurences
        list_dont: re match list of all dont() occurences
    Returns:
        [bool]: current state, where to execute mul(x,y) command.
    """
    start_of_mul = match.start()
    last_do = max([x.end() for x in list_do if x.end() <= start_of_mul], default=-1)
    last_dont = max([x.end() for x in list_dont if x.end() <= start_of_mul], default=-1)

    if last_do == -1 and last_dont == -1:  # If both are -1
        return state  # Keep previous state

    if last_do > last_dont:  # Make state true
        print(f"Enabled {match.group(0)}")
        return True
    elif last_dont > last_do:  # Make state false
        print(f"Disabled {match.group(0)}")
        return False
    else:
        raise ValueError("No state could be determined.")


def main(
    list_matches: List[Match], list_do: List[Match], list_dont: List[Match]
) -> int:
    """
    Given a list of matches, calculate the output of the string computation.
    Args:
        list_matches: list of match objects for main pattern "mul(x,y)"
        list_do: list of match objects for pattern "do()"
        list_dont: list of match objects for pattern "don't()"
    Returns:
        [int]: numeric output of the computation
    """
    total = 0
    state = True

    for match in list_matches:
        state = get_new_state(match, list_do, list_dont, state)
        if state:
            print(f"Adding {match.group(0)}")
            total += calculate_product(match)
    return total


# Part A - Multiplications from corrupted data
# Working with test data
test_str = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
main_pattern = r'mul\((\d+),(\d+)\)'  # pattern to match "mul(#,#)"
test_extracted = list(re.finditer(main_pattern, test_str))  # find all occurences
test_sum_prod = sum(list(map(calculate_product, test_extracted)))

# Get the puzzle
data = get_data(day=3, year=2024)
extracted = list(re.finditer(main_pattern, data))
sum_prod = sum(list(map(calculate_product, extracted)))
# submit(sum_prod, part='a', day=3, year=2024)

# Part B - Activate and deactivate statements
test_str_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()mul(8,5))"
dont_pattern = r"don't\(\)"
do_pattern = r"do\(\)"
test_extracted_2 = list(re.finditer(main_pattern, test_str_2))
test_extract_do = list(re.finditer(do_pattern, test_str_2))
test_extract_dont = list(re.finditer(dont_pattern, test_str_2))
test_sum_prod_2 = main(test_extracted_2, test_extract_do, test_extract_dont)
print(test_sum_prod_2)

extract_do = list(re.finditer(do_pattern, data))
extract_dont = list(re.finditer(dont_pattern, data))
sum_prod_2 = main(extracted, extract_do, extract_dont)
print(sum_prod_2)
submit(sum_prod_2, part='b', day=3, year=2024)
