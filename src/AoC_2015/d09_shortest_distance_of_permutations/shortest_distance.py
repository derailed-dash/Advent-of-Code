""" 
Author: Darren
Date: 01/02/2021

Solving https://adventofcode.com/2015/day/9

Read a bunch of location pairs and distances between them.  E.g.
London to Dublin = 464

We must visit all the locations once and only once.

Solution:
    Use regex to create a (location_1, location_2):distance dict for each distance.
    Also store the locations in reverse, so we can lookup either way.
    Use a set to store unique locations.
    Use itertools.permutations to obtain all possible location permutations (order of) cities.
    For each permutation:
        Check if perm[0] < perm[-1], since this allows us to ignore reverse journeys. If so...
            Iterate through each pair of locations in the permutation.
            Lookup the distance for that pair.
            Add that distance to the overall journey.
    Thus, we end up with total distance for each permutation.

Part 1:
    Minimum distance to visit all locations. I.e. min of all the total distances.

Part 2:
    Maximum distance to visit all locations. I.e. max of all the total distances.
"""
from pathlib import Path
import time
import re
from itertools import permutations

SCRIPT_DIR = Path(__file__).parent 
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    locs_to_distances = get_distances(data) # E.g. (A, B) = n
    
    # build our set of unique locations
    locations = set()
    for loc_pair in locs_to_distances:
        locations.add(loc_pair[0]) # place_a
        locations.add(loc_pair[1]) # place_b

    journey_distances = []

    # Create permutations of all possible combinations of locations
    # I.e. all possible ways of ordering the locations we must visit.
    # E.g. if we have to visit places A, B and C, there would be 3! perms:
    # ABC, ACB, BAC, BCA, CAB, CBA
    for loc_perm in permutations(locations):
        # For efficiency: filter out inverse routes. E.g. we want ABC, but not CBA; they are the same
        if loc_perm[0] < loc_perm[-1]: 
            journey_dist = 0
            for i in range(len(loc_perm)-1):
                # iterate through location pairs i, i+1, for all locations in this permutation
                # E.g. for A, B, C, we would have pairs: A-B, and B-C.
                pair_a = loc_perm[i]
                pair_b = loc_perm[i+1]
                dist = locs_to_distances[(pair_a, pair_b)]
                journey_dist += dist
            
            # Just store the total distance for this journey.
            # If we cared about the order of places, we could use a dict and store those too
            journey_distances.append(journey_dist)

    print(f"Shortest journey: {min(journey_distances)}")
    print(f"Longest journey: {max(journey_distances)}")

def get_distances(data) -> dict:
    """ Read list of distances between place_a and place_b.
    Return each as a list, with each element a unique two-place tuple, and a distance.

    Args:
        data (list[str]): distances, in the form "London to Dublin = 464"

    Returns:
        dict: (start, end) = distance
    """
    distances = {}
    distance_match = re.compile(r"^(\w+) to (\w+) = (\d+)")
    
    for line in data:
        start, end, dist = distance_match.findall(line)[0]
        dist = int(dist)

        # create a distance record in the form: [(loc_1, loc_2), dist]
        # And also store it in reverse, so that when we look it up, 
        # it doesn't matter which order the locations come in the journey.
        distances[(start, end)] = dist
        distances[(end, start)] = dist

    return distances

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
