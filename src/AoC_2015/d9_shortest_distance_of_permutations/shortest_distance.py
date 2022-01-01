""" 
Author: Darren
Date: 01/02/2021

Solving https://adventofcode.com/2015/day/9

Read a bunch of location pairs and distances between them.  E.g.
London to Dublin = 464

We must visit all the locations once and only once.

Solution:
    Use regex to create a [(location_1, location_2), distance] list for each distance.
    Use a set to store unique locations.
    Use itertools.permutations to obtain all possible location permutations.
    Iterate through each permutation, and determine distances between each location pair in that perm.
    Thus, we create a total distance for each perm.

Part 1:
    Minimum distance to visit all locations. I.e. min of all the total distances.

Part 2:
    Maximum distance to visit all locations. I.e. max of all the total distances.
"""
import os
import time
import re
from itertools import permutations

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    locations = set()
    distances = get_distances(data)
    for distance in distances:
        # update our set of unique locations
        locations.add(distance[0][0])
        locations.add(distance[0][1])

    journey_distances = []

    # create permutations of all possible combinations of locations
    for perm in permutations(locations):
        journey_dist = 0
        for i in range(len(perm)-1):
            # iterate through location pairs i, i+1, for all locations in this permutation
            start = perm[i]
            end = perm [i+1]
            dist_index = next(index for index, distance in enumerate(distances) if distance[0] == tuple([start, end]))
            journey_dist += distances[dist_index][1]
        
        journey_distances.append(journey_dist)

    print(f"Shortest journey: {min(journey_distances)}")
    print(f"Longest journey: {max(journey_distances)}")


def get_distances(data):
    distances = []
    distance_match = re.compile(r"^(\w+) to (\w+) = (\d+)")
    
    for line in data:
        start, end, dist = distance_match.match(line).groups()
        dist = int(dist)

        # create a distance record in the form: [(loc_1, loc_2), dist]
        # And also store it in reverse, so that when we look it up, 
        # it doesn't matter which order the locations come in the journey.
        distances.append([tuple([start, end]), dist])
        distances.append([tuple([end, start]), dist])

    return distances


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
