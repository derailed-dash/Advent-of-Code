""" 
Author: Darren
Date: 12/02/2021

Solving https://adventofcode.com/2015/day/13

A list of people sat around the table.
Happiness scores depend on who sets next to whom. E.g.
    Alice would gain 54 happiness units by sitting next to Bob.

Solution:
    Use a defaultdict to store happiness scores each person.  E.g.
        happiness[Alice][Bob] = 54
    
    Use a set to store all people.
    Find all permutations of people around the table using itertools.permutations().
    Create a dict happiness_for_perms
    For each perm:
        We don't want to process reverse order of perms, so check using <= vs last element
        For each person around the table clockwise:
            Add up the happiness of the adjacent people
        Store happiness for this perm

Part 1:
    Find happiness of optimal seating arrangement

Part 2:
    Add myself, and assume that all happiness relationships are 0, wherever I go.
    
    Add myself to the dict for every other person in the set.
    Add me to the set.
    Repeat Part 1.
"""
import os
import time
import re
from itertools import permutations
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    print("Part 1")
    # build up a dict of hapiness scores for each person
    happiness_by_person = get_happiness_by_person(data)

    # create a set of all the people
    people = set(happiness_by_person.keys())

    # we don't care where the first person sits, since it's a circle.  
    # So let's just make person_1 the 'head' of the table
    person_1 = people.pop()

    # get all permutations for remaining people around the table, as list of tuples
    # We expect n! perms
    happiness_for_perm, optimum_happiness_perm = find_optimum_happiness(happiness_by_person, person_1, people)
    print(f"Optimum happiness = {happiness_for_perm[optimum_happiness_perm]} with seating: {optimum_happiness_perm}")

    print("\nPart 2")
    # Need to add person_1 back in, so that we can add values for Me sitting next to Person_1
    people.add(person_1)
    add_me_to_happiness_by_person(happiness_by_person, people)
    people.remove(person_1)
    people.add('Me')

    happiness_for_perm, optimum_happiness_perm = find_optimum_happiness(happiness_by_person, person_1, people)
    print(f"Optimum happiness = {happiness_for_perm[optimum_happiness_perm]} with seating: {optimum_happiness_perm}")

def find_optimum_happiness(happiness_by_person, person_1, people):
    """ Determine all permutations of seating.
    Reduce number of perms by removing person_1.
    Compute happiness score for each permutation.
    Determine the permutation with the greatest happiness score.

    Args:
        happiness_by_person (dict): Happiness adjacency map
        person_1 (str): Arbitrary head of the table
        people (set): The people to seat around the table

    Returns:
        tuple: (score, optimum_seating_permutation)
    """
    perms = list(permutations(people))
    happiness_for_perm = {}
    for perm in perms:
        # this allows us to remove reverse permutations
        if perm <= perm[::-1]:
            perm = list(perm)  # convert perm from tuple to list, to make it mutable
            perm.insert(0, person_1) # such that we can insert the head of the table
            happiness_for_perm[tuple(perm)] = compute_happiness_for_perm(perm, happiness_by_person)
    
    optimum_happiness_perm = max(happiness_for_perm.items(), key=lambda x: x[1])[0]
    return happiness_for_perm, optimum_happiness_perm

def add_me_to_happiness_by_person(happiness_by_person: dict, people):
    for person in people:
        happiness_by_person[person]['Me'] = 0
        happiness_by_person['Me'][person] = 0

def compute_happiness_for_perm(seating_arrangement, happiness_by_person):
    happiness = 0

    for i, current_person in enumerate(seating_arrangement):
        if i < len(seating_arrangement) - 1:
            current_next_person = seating_arrangement[i+1]
        else:
            current_next_person = seating_arrangement[0]

        happiness += happiness_by_person[current_person][current_next_person]
        happiness += happiness_by_person[current_next_person][current_person]

    return happiness

def get_happiness_by_person(data) -> dict[str, dict[str, int]]:
    """ Here we build an adjacency list.
    We will map each person to every other person.
    Since this is a directed graph, we'll use a defaultdict(dict).

    Args:
        data (list): A list of happiness statements

    Returns:
        dict: dict[person_x][person_y: happiness]
    """
    # Alice would gain 54 happiness units by sitting next to Bob.
    happiness = defaultdict(dict)
    happiness_pattern = re.compile(r"^(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+)")
    
    for line in data:
        person_1, gain_or_lose, value, person_2 = happiness_pattern.findall(line)[0]
        if gain_or_lose == "gain":
            value = int(value)
        else:
            value = -(int(value))
    
        happiness[person_1][person_2] = value

    return happiness

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
