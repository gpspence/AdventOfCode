import numpy as np
import math
from numpy.typing import NDArray
from typing import Tuple, List, AnyStr
from aocd import get_data, submit


def clean_data(data: str) -> Tuple[NDArray]:
    """
    Clean the input puzzle into NDArray.
    Args:
        data (str): input string, raw puzzle.
    Returns:
        [Tuple[NDArray]]: Tuple of cleaned arrays
        Rules are pipe delimited strings.
        Updates are list of lists.
    """
    split_data = data.split("\n\n")
    rules = split_data[0].split('\n')
    updates = [np.array(x.split(',')).astype(int).tolist() for x in split_data[1].split('\n')]
    return (rules, updates)


def rank_nums(rules: List, all_nums: List) -> List:
    """
    Take all of the rules and create a dict, where each number has a power score.
    Return a list ordered by the rules.
    Args:
        rules (list): list of rules each a pipe delimited str
        all_nums (list): list of all nums contained in the rules
    Returns:
        [list]: list of numbers, ordered by rules
    """
    num_ranking = {num: 0 for num in all_nums}

    for rule in rules:
        winning_num = int(rule.split('|')[0])
        num_ranking[winning_num] = num_ranking[winning_num] + 1

    num_ranking = dict(
        sorted(num_ranking.items(), key=lambda item: item[1], reverse=True)
    )
    return list(num_ranking.keys())


def filter_ranking(update: List[int], num_ranking: List[int]) -> List:
    """
    Filter num_ranking based on which numbers are in the update.
    Args:
        update (List): list of updates
    Returns:
        [List]: filtered list containing only nums which are in update
    """
    return list(filter(lambda x: x in update, num_ranking.copy()))


def main(data: AnyStr) -> int:
    """
    Calculate the total middle value of the ordered lists.
    """
    rules, updates = clean_data(data)
    all_nums = np.array([x.split('|') for x in rules]).flatten().astype(int).tolist()
    num_ranking = rank_nums(rules, all_nums)
    total = 0

    for update in updates:
        new_ranking = filter_ranking(update, num_ranking)
        print(f"Try Update: {update}, Ranking: {new_ranking}")
        if update == new_ranking:
            print(f"Succeed Update: {update}, Ranking: {new_ranking}")
            print(f"Adding {update[math.floor(len(update)/2)]}")
            total += update[math.floor(len(update)/2)]

    return total


# Part A - Check valid updates, sum the middle number
# Develop with the test data
test_data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

# test_answer = main(data=test_data)

# Use the real data
data = get_data(day=5, year=2024)
rules, updates = clean_data(data)
rules_all_nums = np.array([x.split('|') for x in rules]).flatten().astype(int).tolist()
# updates_all_nums = [val for sublist in updates for val in sublist]
# answer = main(data=data)
# print(answer)

