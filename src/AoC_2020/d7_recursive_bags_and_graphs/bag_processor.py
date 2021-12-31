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
How many colors can, eventually, contain at least one shiny gold bag?

Part 2
------
How many bags are required inside the shiny gold bag?

"""
import sys
import os
import time
import re
from collections import defaultdict
from pprint import pprint as pp

bag_example_rules = [
    "light red bags contain 1 bright white bag, 2 muted yellow bags.",
    "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
    "bright white bags contain 1 shiny gold bag.",
    "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
    "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
    "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
    "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
    "faded blue bags contain no other bags.",
    "dotted black bags contain no other bags."
]

BAG_RULES_INPUT_FILE = "input/bag_rules.txt"
SHINY_GOLD = "shiny gold"


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, BAG_RULES_INPUT_FILE)
    print("Input file is: " + input_file)

    rules = process_rules(read_input(input_file))
    #rules = process_rules(bag_example_rules)
    print(f"{len(rules)} rules processed.")

    searching_for = SHINY_GOLD
    print(f"Searching for bags that can contain {searching_for}...")
    container_bags = recursive_search(rules, searching_for)

    # get rid of duplicate bags
    bag_set = set(container_bags)
    print(f"We have found {len(bag_set)} possible bags that can contain {searching_for}.")

    bag_count = recursive_count(rules, searching_for) - 1
    print(f"{searching_for} contains {bag_count} bags.")


def recursive_count(rules, search_bag):
    # count this bag
    count = 1

    # now get the bags that this bag contains as a dict
    # E.g. {'dark lime':3, 'muted violet': 4}
    contained_bags = rules[search_bag]

    # iterate through the contained bag types, e.g. 'muted yellow'
    for contained_bag in contained_bags:
        # e.g. for muted violet, we get 4
        qty_contained = int(rules[search_bag][contained_bag])

        # and now get the bags contained by this contained bag...
        count += qty_contained * recursive_count(rules, contained_bag)
        
    return count


def recursive_search(rules, search_bag):
    contains = []

    # iterate through all the bag types, e.g. 'muted yellow'
    for bag_type in rules.keys():
        
        # let's search for 'shiny gold' in the rule string for this bag
        if search_bag in rules[bag_type]:
            # this bag contains our target, so add it
            contains.append(bag_type)

            # E.g. Found shiny gold in muted yellow: ('2', 'shiny gold')('9', 'faded blue')
            print(f"Found {search_bag} in {bag_type}: {rules[bag_type]}")

            # and now we want to find what type of bags contain this type of bag
            # instead of searching for 'shiny gold', it will search with 'muted yellow'
            contains.extend(recursive_search(rules, bag_type))

    return contains


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

