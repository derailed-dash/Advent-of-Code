""" 
Author: Darren
Date: 13/01/2021

Solving https://adventofcode.com/2015/day/3

Solution 1 of 2:
    Create VECTORS dict, where each of >^<v maps to a [x, y] list.
    For each move, store the current x and y as a tuple.
    Use a set to store only unique locations.    

Part 1:
    Given input of directions in >^<v format, count how many locations were visited.

Part 2:
    Santa and Robosanta alternate to follow the directions given.
    Count how many locations were visited by either Santa or Robosanta.
    Here, we use %2 to send alternate directions to each of Santa and Robosanta.
"""
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

VECTORS = {
    '^': [0, 1],
    '>': [1, 0],
    'v': [0, -1],
    '<': [-1, 0]
}

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()

    current_x = current_y = 0
    visited_locations = set()
    visited_locations.add(tuple([current_x, current_y]))

    for vector in data:
        current_x += VECTORS[vector][0]
        current_y += VECTORS[vector][1]
        visited_locations.add(tuple([current_x, current_y]))

    print(f"Santa visited {len(visited_locations)} locations.")

    santa_x = santa_y = 0
    robosanta_x = robosanta_y = 0

    santa_visited_locations = set()
    santa_visited_locations.add(tuple([santa_x, santa_y]))
    robosanta_visited_locations = set()
    robosanta_visited_locations.add(tuple([robosanta_x, robosanta_y]))

    for i, vector in enumerate(data):
        if i % 2 == 1:
            santa_x += VECTORS[vector][0]
            santa_y += VECTORS[vector][1]
            santa_visited_locations.add(tuple([santa_x, santa_y]))
        else:
            robosanta_x += VECTORS[vector][0]
            robosanta_y += VECTORS[vector][1]
            robosanta_visited_locations.add(tuple([robosanta_x, robosanta_y]))

    visited_locations = santa_visited_locations.union(robosanta_visited_locations)
    print(f"Santa and Robosanta visited {len(visited_locations)} locations.")

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
