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
    Use NetworkX built-in algorithms to approximate shortest distance... Does not provide a good result!!
"""
from itertools import permutations
from pathlib import Path
import time
import re
import networkx as nx
import networkx.algorithms.approximation as nx_app
import matplotlib.pyplot as plt

SCRIPT_DIR = Path(__file__).parent 
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    graph = build_graph(data)

    locations = graph.nodes
    print(locations)
    
    journey_distances = []
    
    for journey_perm in permutations(locations):
        # For efficiency: filter out inverse routes. E.g. we want ABC, but not CBA; they are the same
        if journey_perm[0] < journey_perm[-1]: 
            journey_dist = 0
            for i in range(len(journey_perm)-1):
                # iterate through location pairs i, i+1, for all locations in this permutation
                # E.g. for A, B, C, we would have pairs: A-B, and B-C.
                node_a = journey_perm[i]
                node_b = journey_perm[i+1]
                dist = graph[node_a][node_b]["weight"]
                journey_dist += dist
            
            # Just store the total distance for this journey.
            # If we cared about the order of places, we could use a dict and store those too
            journey_distances.append(journey_dist)

    print(f"Shortest journey: {min(journey_distances)}")
    print(f"Longest journey: {max(journey_distances)}")    

    print(graph)
    draw_graph(graph)
    
def draw_graph(graph):
    pos = nx.spring_layout(graph)
    
    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=300)
    
    # Draw labels
    # nx.draw_networkx_labels(graph, pos, font_size=10, font_family="sans-serif")
    
    # Draw closest edges on each node only
    closest_edges = nx.draw_networkx_edges(graph, 
                           pos, 
                           edge_color="blue", 
                           width=0.5)
    
    # Draw the labels
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels)

    route = nx_app.christofides(graph, weight="weight")[:-1]
    route_edges = list(nx.utils.pairwise(route))
    
    route_distance = nx.path_weight(graph, route, weight="weight")
    print(f"Distance: {route_distance}")
    
    # Draw the route
    nx.draw_networkx(
        graph,
        pos,
        with_labels=True,
        arrows=True,
        edgelist=route_edges,
        edge_color="red",
        node_size=200,
        width=3,
    )
    
    ax = plt.gca()
    plt.axis("off")
    plt.tight_layout()
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
        start, end, distance = distance_match.findall(line)[0]
        distance = int(distance)
        graph.add_edge(start, end, weight=distance)

    return graph

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
