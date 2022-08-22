""" 
Author: Darren
Date: 22/08/2022

Solving https://adventofcode.com/2015/day/9

Read a bunch of location pairs and distances between them.  E.g.
London to Dublin = 464

We must visit all the locations once and only once.

Solution 2 of 2.

Solution:
    Use regex to create a (location_1, location_2):distance dict for each distance.
    Use NetworkX to build an undirected weighted graph.
"""
from pathlib import Path
import time
import re
import networkx as nx
import matplotlib.pyplot as plt

SCRIPT_DIR = Path(__file__).parent 
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    graph = build_graph(data) 
    print(graph)

def draw_graph(graph):
    subax1 = plt.subplot(121)
    nx.draw_spring(graph, with_labels=True)
    plt.show()    
    
def build_graph(data) -> nx.Graph:
    """ Read list of distances between place_a and place_b.
    Return dict that maps (A,B)->dist x, and (B,A)->dist x.

    Args:
        data (list[str]): distances, in the form "London to Dublin = 464"

    Returns:
        dict: (start, end) = distance
    """
    graph = nx.Graph()
    distance_match = re.compile(r"^(\w+) to (\w+) = (\d+)")
    
    for line in data:
        start, end, dist = distance_match.findall(line)[0]
        dist = int(dist)

        graph.add_edge(start, end, weight=dist)

    return graph

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
