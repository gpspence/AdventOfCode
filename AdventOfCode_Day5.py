import numpy as np
import math
import matplotlib.pyplot as plt
import networkx as nx
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
        Rules are pipe delimited strings e.g. "10|12".
        Updates are list of lists of ints.
    """
    split_data = data.split("\n\n")
    rules = split_data[0].split('\n')
    rules = np.array([x.split('|') for x in rules]).astype(int).tolist()
    updates = [
        np.array(x.split(','))
        .astype(int)
        .tolist() for x in split_data[1].split('\n')
    ]
    return (rules, updates)


def order_numbers(update: List, rules: List) -> List:
    """
    Topological sorting using Kahn's algorithm (BFS). Sort using rules.
    0. Build the graph - assign each node a list of destination nodes.
    Calculate the in-degree for each node (each incoming edge).
    1. Add all nodes with in-degree 0 to a queue.
    2. For each outgoing edge from the removed node, decrement
    3. If the in-degree for any child node becomes 0, add it to the queue
    If the queue is empty and there are still nodes in graph at end, there is
    a cycle.
    Args:
        update (list): list of numbers to be sorted
        rules (list): list of rules (pairs of numbers) to use to sort update
    Returns:
        [list]: update sorted by rules
    """
    # 0. Build graph - initialise in-degree counter and in-degree
    graph = defaultdict(list)  # collection default list on KeyError
    in_degree = defaultdict(int)  # collection default int on KeyError

    for num in update:
        in_degree[num] = 0  # Number of incoming edges, initially 0

    # 0. Build graph - Add edges to the graph based on rules
    for left, right in rules:
        # Only consider numbers in the given update
        if left in update and right in update:
            graph[left].append(right)  # outgoing higher nodes to list lower
            in_degree[right] += 1  # increment incoming edges for lower nodes

    # 1. Add nodes with no incoming edges (in-degree = 0 to the queue
    queue = deque()  # list like container with fast appends and pops at ends

    for num in update:
        if in_degree[num] == 0:
            queue.append(num)

    ordered_numbers = []

    # 2. and 3. from docstring
    while queue:
        node = queue.popleft()
        ordered_numbers.append(node)

        # Reduce in-degree for neighbors, add to queue if in-degree becomes 0
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # plot_dag(graph)

    # Check if topological sort is possible (i.e., no cycle)
    if len(ordered_numbers) != len(update):
        raise ValueError("A cycle was found in rules - ordering not possible.")

    return ordered_numbers


def plot_dag(graph):
    # Create a directed graph and add edges
    G = nx.DiGraph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Use networkx util to check if valid DAG
    if nx.is_directed_acyclic_graph(G):
        print("The graph is a valid Directed Acyclic Graph (DAG).")
    else:
        print("Warning: The graph has a cycle.")

    # Plot the graph
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, node_size=300, arrows=True)
    plt.title("Directed Acyclic Graph (DAG)")
    plt.show()


def main(data: AnyStr) -> int:
    """
    Calculate the total middle value of the ordered lists.
    """
    rules, updates = clean_data(data)
    total_a = 0
    total_b = 0
    failed_updates = []

    for update in updates:
        update_ordered = order_numbers(update, rules)
        # print(f"Try Update: {update}, Ranking: {update_ordered}")
        if update == update_ordered:
            # print(f"Succeed Update: {update}, Ranking: {update_ordered}")
            # print(f"Adding {update[math.floor(len(update)/2)]}")
            total_a += update[math.floor(len(update)/2)]
        else:
            failed_updates.append(update)

    for update in failed_updates:
        failed_update_ordered = order_numbers(update, rules)
        total_b += failed_update_ordered[math.floor(len(update)/2)]

    return (total_a, total_b)


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

test_answer = main(data=test_data)
print(test_answer)

# Use the real data
data = get_data(day=5, year=2024)
rules, updates = clean_data(data)
answer_a, answer_b = main(data=data)
print(answer_a)
submit(answer_a, part='a', day=5, year=2024)

# Part B - repeat for updates which failed, but reorder
submit(answer_b, part='b', day=5, year=2024)
