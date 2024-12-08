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
        Rules are pipe delimited strings.
        Updates are list of lists.
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
    Sort nums using rules - uses Kahn's algorithm for topological sorting:
    1.
    2.
    3.
    Args:
        update (list):
    Returns:

    """
    # Build graph and in-degree counter
    graph = defaultdict(list)  # collection default list on KeyError
    in_degree = defaultdict(int)  # collection default int on KeyError

    # Initialize in-degree for all nodes (numbers)
    for num in update:
        in_degree[num] = 0  # Number of nodes which feed node, init unknown

    # Add edges to the graph based on instructions
    for higher, lower in rules:
        # Only consider numbers in the update
        if higher in in_degree and lower in update:
            graph[higher].append(lower)  # add outgoing nodes to list in dict
            in_degree[lower] += 1  # add to lower "in degree" i.e. feeds in

    # Topological sorting using Kahn's algorithm (BFS)
    queue = deque()  # list like container with fast appends and pops at ends

    # Add nodes with no incoming edges (in-degree = 0) to the queue
    for num in update:
        if in_degree[num] == 0:
            queue.append(num)

    ordered_numbers = []

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
    # Create a directed graph from the dictionary
    G = nx.DiGraph()

    # Add edges to the graph
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
    total = 0

    for update in updates:
        update_ordered = order_numbers(update, rules)
        # print(f"Try Update: {update}, Ranking: {update_ordered}")
        if update == update_ordered:
            # print(f"Succeed Update: {update}, Ranking: {update_ordered}")
            # print(f"Adding {update[math.floor(len(update)/2)]}")
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

test_answer = main(data=test_data)
print(test_answer)

# Use the real data
data = get_data(day=5, year=2024)
rules, updates = clean_data(data)
answer = main(data=data)
print(answer)
submit(answer, part='a', day=5, year=2024)
