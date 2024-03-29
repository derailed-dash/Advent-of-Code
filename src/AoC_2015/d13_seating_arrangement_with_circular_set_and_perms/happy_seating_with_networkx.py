""" 
Author: Darren
Date: 15/11/2022

Solving https://adventofcode.com/2015/day/13

A list of people sat around the table.
Happiness scores depend on who sets next to whom. E.g.
    Alice would gain 54 happiness units by sitting next to Bob.

Solution 2 of 2: Using NetworkX.

Solution:
    Use regex to get all the edges, i.e. person_a, person_b, and happiness.
    Use NetworkX to build a directed weighted graph from the edges.
    As with Solution 1, we need to try all permutations, having removed person 1.
    Each permutation is a seating arrangement.
    For each permutation:
      Add person 1 at each end of the path.
      Use nx.path_weight() to determine the overall happiness for the path.
      Then use nx.path.weight() for the path in reverse.
      Why?  Because we need the happiness for A->B and for B->A.
      Store the permutation with the total happiness.

Part 1:
    Find happiness of optimal seating arrangement.
    I.e. the permutation with the highest score.

Part 2:
    Add myself to the graph; happiness relationships are 0, wherever I go.
    Iterate through all the people (nodes) in the current graph. For each:
      - Add "Me" as a new edge in both directions, with happiness of 0.

    Repeat Part 1 with the new graph.
"""
from collections.abc import Iterable
from itertools import permutations
from pathlib import Path
import time
import re
import networkx as nx
import matplotlib.pyplot as plt

SCRIPT_DIR = Path(__file__).parent 
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

HAPPINESS = "happiness"
SHOW_GRAPH = True

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    graph = build_graph(data)

    print("\nPart 1")
    people = set(graph.nodes.keys())
    person_a = people.pop()
    
    max_happiness = get_seating_with_max_happiness(graph, people, person_a)
    print(f"Optimum happiness: {max_happiness}")
    
    print("\nPart 2")
    # Need to add person_a back in, so that we can add values for Me sitting next to person_a
    people.add(person_a)
    graph = add_me_to_happiness_by_person(graph)
    people = set(graph.nodes.keys())
    people.remove(person_a)

    max_happiness = get_seating_with_max_happiness(graph, people, person_a)
    print(f"Optimum happiness: {max_happiness}")
    
    if SHOW_GRAPH:
        draw_graph(graph, max_happiness[0])

def get_seating_with_max_happiness(graph, people, person_a) -> dict:
    happiness_for_perm = {}
    for perm in permutations(people): # E.g. for route ABC     
        # Use path_weight to get the total of all the edges that make up the route
        if perm <= perm[::-1]:
            perm = list(perm)
            perm.insert(0, person_a)
            perm.append(person_a)
            
            # Get happiness in the first direction, e.g. person A -> B
            total_happiness_forward = nx.path_weight(graph, perm, weight=HAPPINESS)
            # Now get happiness in the reverse direction, e.g. person B -> A
            total_happiness_reverse = nx.path_weight(graph, perm[::-1], weight=HAPPINESS)
            
            # For total happiness for this seating arrangement, we need to add forward and reverse
            happiness_for_perm[tuple(perm)] = total_happiness_forward + total_happiness_reverse

    max_journey = max(happiness_for_perm.items(), key=lambda x: x[1])
    return max_journey
    
def build_graph(data: list) -> nx.DiGraph:
    """ 
    Build graph of of all people, including happiness scores between each person.
    """
    graph = nx.DiGraph()
    happiness_pattern = re.compile(r"^(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+)")
    
    # Add each edge, in the form of a location pair
    for line in data:
        person_1, gain_or_lose, value, person_2 = happiness_pattern.findall(line)[0]
        if gain_or_lose == "gain":
            value = int(value)
        else:
            value = -(int(value))
            
        graph.add_edge(person_1, person_2, happiness=value)

    return graph

def add_me_to_happiness_by_person(graph: nx.DiGraph) -> nx.DiGraph:
    """ Extend the graph by adding "Me", 
    with happiness weight of 0 for all pairings that include Me.
    """
    people = list(graph.nodes()) # make a copy of the names
    
    for person in people:
        graph.add_edge(person, "Me", happiness=0)
        graph.add_edge("Me", person, happiness=0)
        
    return graph

def draw_graph(graph: nx.DiGraph, arrangement: Iterable):
    """ Takes the original graph and a seating arrangement, 
    builds a new graph with the nodes in the correct arrangement order, and draws it.
    """
    # Get the edges from only the adjacent people in our seating arrangement
    edges = list(nx.utils.pairwise(arrangement))
    
    # Get dict of {(A, B): happiness} to use as edge labels
    edge_labels = {(person_1, person_2): graph[person_1][person_2][HAPPINESS] 
                        for (person_1, person_2) in edges}
    
    # Get dict of {(B, A): happiness}
    reverse_edges = [(b, a) for a, b in edges] # to use edge labels
    reverse_edge_labels = {(person_2, person_1): graph[person_2][person_1][HAPPINESS] 
                        for (person_1, person_2) in edges}
    
    all_edges = edges + reverse_edges # a single list of all pairs, in both directions
    
    seating_graph = nx.DiGraph() # Create a new graph, to which we will add only relevant edges
    for (person_1, person_2) in all_edges:
        happiness_score = graph[person_1][person_2][HAPPINESS]
        seating_graph.add_edge(person_1, person_2, happiness=happiness_score)

    pos = nx.circular_layout(seating_graph) # arrange our nodes - in the right order - in a circle
   
    # Nodes and node labels
    nx.draw_networkx_nodes(seating_graph, pos, node_color="y")
    nx.draw_networkx_labels(seating_graph, pos, font_family="sans-serif")
    
    # Edges - use arc3 to curve them, otherwise we end up with a double-arrowed line
    nx.draw_networkx_edges(seating_graph, pos, edgelist=edges, # forward edges
                           width=1, edge_color="r", connectionstyle='arc3, rad = 0.3', 
                           min_source_margin=15, min_target_margin=15)
    nx.draw_networkx_edges(seating_graph, pos, edgelist=reverse_edges, # reverse edges
                           width=1, edge_color="b", connectionstyle='arc3, rad = 0.3', 
                           min_source_margin=15, min_target_margin=15)
    
    # Edge weight labels
    nx.draw_networkx_edge_labels(seating_graph, pos, edge_labels, 
                                 font_color="r", verticalalignment="top", horizontalalignment="left")
    nx.draw_networkx_edge_labels(seating_graph, pos, reverse_edge_labels, 
                                 font_color="b", verticalalignment="bottom", horizontalalignment="right")
    
    ax = plt.gca()
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
