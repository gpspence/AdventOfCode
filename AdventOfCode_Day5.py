import numpy as np
import math
from numpy.typing import NDArray
from typing import Tuple, List, AnyStr
from collections import defaultdict, deque
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


def order_numbers(nums, instructions):
    # Build graph and in-degree counter
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Initialize in-degree for all nodes (numbers)
    for num in nums:
        in_degree[num] = 0
    
    # Add edges to the graph based on instructions
    for higher, lower in instructions:
        graph[higher].append(lower)
        in_degree[lower] += 1
    
    # Topological sorting using Kahn's algorithm (BFS)
    queue = deque()
    
    # Add nodes with no incoming edges (in-degree = 0) to the queue
    for num in nums:
        if in_degree[num] == 0:
            queue.append(num)
  
    ordered_numbers = []
   
    while queue:
        node = queue.popleft()
        ordered_numbers.append(node)
       
        # Reduce in-degree for neighbors and add to queue if in-degree becomes 0
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
   
    # Check if topological sort is possible (i.e., no cycle)
    if len(ordered_numbers) != len(nums):
        raise ValueError("There is a cycle in the instructions, so no valid ordering is possible.")
   
    return ordered_numbers


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

