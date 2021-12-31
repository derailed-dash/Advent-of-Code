"""
Author: Darren
Date: 08/12/2020

Solving: https://adventofcode.com/2020/day/7

Rules are like:
    light red bags contain 1 bright white bag, 2 muted yellow bags.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    faded blue bags contain no other bags.

Part 1
------
How many bags can, eventually, contain at least one shiny gold bag?

Part 2
------
How many bags are required inside the shiny gold bag?

Solution 2 of 2:
    Instead of using recursive functions, build a NetworkX graph
    and use this to determine all ancesters.
"""
import os
import time
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx

SCRIPT_DIR = os.path.dirname(__file__) 
BAG_RULES_INPUT_FILE = "input/bag_rules.txt"
SAMPLE_RULES_INPUT_FILE = "input/sample_bag_rules.txt"
SHINY_GOLD = "shiny gold"
DRAW_GRAPH = False

def main():
    input_file = os.path.join(SCRIPT_DIR, BAG_RULES_INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_RULES_INPUT_FILE)
    print("Input file is: " + input_file)

    rules = process_rules(read_input(input_file))
    print(f"{len(rules)} rules processed.")

    graph = build_graph(rules)

    searching_for = SHINY_GOLD
    print(f"Searching for bags that can contain {searching_for}...")
    ancestors = list(nx.ancestors(graph, searching_for))
    print(f"We have found {len(ancestors)} possible bags that can contain {searching_for}.")

    if DRAW_GRAPH:
        draw_graph(graph, searching_for, ancestors)

    bag_count = recursive_graph_count(searching_for, graph)
    print(f"{searching_for} contains {bag_count-1} bags.")


def draw_graph(graph, searching_for, ancestors):
    # Layouts that look okay: spring, random, circular, spiral
    pos = nx.spiral_layout(graph)

    colours = []
    for node in graph.nodes.keys():
        if node == searching_for:
            colours.append("yellow")
        elif node in ancestors:
            colours.append("green")
        else:
            colours.append("purple")

    nx.draw(graph, pos=pos, node_color=colours, edge_color="grey", width=1, with_labels=True)
    ax = plt.gca()
    ax.set_axis_off()
    plt.show()


def build_graph(rules):
    graph = nx.DiGraph()
    for parent, children in rules.items():
        graph.add_node(parent)
        for child, child_count in children.items():
            graph.add_node(child)
            graph.add_edge(parent, child, count=child_count)
    return graph


def recursive_graph_count(parent, graph):
    count = 0
    for child in graph.neighbors(parent):
        count += recursive_graph_count(child, graph) * graph.edges[parent, child]["count"]
    
    return count + 1


def process_rules(bag_rules):
    # match 'light red' at the beginning of the line
    container_bag_pattern = re.compile(r"^[a-z]+\s[a-z]+")

    # match '1 bright white' which will need to repeat x times per line
    contains_bags_pattern = re.compile(r"([0-9]+)\s([a-z]+\s[a-z]+)")

    # let's create a nested dict of this format:
    # rules = { 
    #     'dim silver': {'dull magenta': 4, 'shiny chartreuse': 2}
    #     'shiny cyan:': {'dim coral': 4, 'dull indigo': 4, 'plaid green': 4}
    # }
    # defaultdict, to autocreate a nested dictionary for each assignment 
    rules = defaultdict(dict)
    for rule_line in bag_rules:
        # rule line like: 'light red bags contain 1 bright white bag, 2 muted yellow bags.'
        
        # findall returns 'light red' as a list, so we convert to string
        bag = "".join(container_bag_pattern.findall(rule_line))

        # because we're matching groups, this returns a list of tuples
        # 1st level dict key is the containing bag name
        # 2nd level dict is bag type: count
        for bag_count, bag_contains in contains_bags_pattern.findall(rule_line):
            rules[bag][bag_contains] = int(bag_count)

    return rules


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        rules = f.read().splitlines()
        
    return rules


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")    
