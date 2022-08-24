""" 
Author: Darren
Date: 22/08/2022

Solving https://adventofcode.com/2015/day/9

Read a bunch of location pairs and distances between them.  E.g.
London to Dublin = 464

We must visit all the locations once and only once.

Solution 2 of 2: Using NetworkX.

Solution:
    Use regex to get all the edges, i.e. location_a, location_b, and the distance between them.
    Use NetworkX to build an undirected weighted graph from the edges.
    As with Solution 1, we need to try all permutations of the locations.
    So, each permutation is a possible route.
    For each route:
      Use nx.path_weight() to determine the overall distance.
      This saves us having to manually obtain all the edge pairs, and adding their distances.
      Store the resulting route distance against the route itself.
    
    Part 1:
      Use min() to get the shortest distance distance, keyed on the value of the route:distance dict.
    
    Part 2:
      Use max() instead.
      
    Optional: render the graph visually.
      Draw all the nodes, except start and end.
      Draw the start and end nodes, in a different colour.
      Draw all the edges between pairs and label them.
      Now draw all the edges that make up the specified route, with arrows and different colour.
"""
from itertools import permutations
from pathlib import Path
import time
import re
import networkx as nx
import matplotlib.pyplot as plt

SCRIPT_DIR = Path(__file__).parent 
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

DISTANCE = "distance"

SHOW_GRAPH = True

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    graph = build_graph(data)

    locations = graph.nodes
    journey_distances = {}

    for route in permutations(locations): # E.g. for route ABC     
        # Use path_weight to get the total of all the edges that make up the route
        route_distance = nx.path_weight(graph, route, weight=DISTANCE)
        journey_distances[route] = route_distance

    # Get (journey, distance) tuples
    min_journey = min(journey_distances.items(), key=lambda x: x[1])
    max_journey = max(journey_distances.items(), key=lambda x: x[1])
    
    print(f"Shortest journey: {min_journey}")
    print(f"Longest journey: {max_journey}")
    
    if SHOW_GRAPH:
        draw_graph(graph, min_journey[0])  
        draw_graph(graph, max_journey[0])
    
def draw_graph(graph, route):
    start_node = route[0]
    end_node = route[-1]
    
    pos = nx.spring_layout(graph) # create a layout for our graph

    # Draw all nodes in the graph
    nx.draw_networkx_nodes(graph, pos, 
                           nodelist=route[1:-1], # exclude start and end
                           node_color="green")
    
    # Draw all the node labels
    nx.draw_networkx_labels(graph, pos, font_size=11)
    
    # Draw start and end nodes
    nx.draw_networkx_nodes(graph, pos, nodelist=[start_node], 
                           node_color="white", edgecolors="green")
    nx.draw_networkx_nodes(graph, pos, nodelist=[end_node], 
                           node_color="orange", edgecolors="green")

    # Draw closest edges for each node only - with thin lines
    nx.draw_networkx_edges(graph, pos, 
                           edge_color="green", width=0.5)
    
    # Draw all the edge labels - i.e. the distances
    nx.draw_networkx_edge_labels(graph, pos, nx.get_edge_attributes(graph, DISTANCE))
    
    # Draw the edges that make up this particular route
    route_edges = list(nx.utils.pairwise(route))
    nx.draw_networkx_edges(graph, pos, edgelist=route_edges,
                           edge_color="red", width=3, arrows=True)
    
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
    
    # Add each edge, in the form of a location pair
    for line in data:
        start, end, distance = distance_match.findall(line)[0]
        distance = int(distance)
        graph.add_edge(start, end, distance=distance)

    return graph

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
