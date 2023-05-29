""" 
Author: Darren
Date: 13/01/2021

Solving https://adventofcode.com/2015/day/3

Solution 2 of 3:
    Same as solution 1, but let's use a Point class to store the x, y coordinates, rather than lists/tuples.
    That way, we only have to store one thing for each move.
    This removes a load of code duplicaton, and over half the time!

Part 1:
    Given input of directions in >^<v format, count how many locations were visited.
    Each location is represented using a complex number.
    Store each visited location in a set.

Part 2:
    Santa and Robosanta alternate to follow the directions given.
    Count how many locations were visited by either Santa or Robosanta.
    Here, we use %2 to send alternate directions to each of Santa and Robosanta.    
"""
from pathlib import Path
import time
from src.common.type_defs import Point, ARROW_VECTORS

SCRIPT_DIR = Path(__file__).parent 
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()

    current_location = Point(0, 0)
    visited_locations = set()
    visited_locations.add(current_location)

    for vector in data: # read char by char
        current_location += ARROW_VECTORS[vector]
        visited_locations.add(current_location)

    print(f"Santa visited {len(visited_locations)} locations.")

    santa_location = robosanta_location = Point(0,0)

    santa_visited_locations = set()
    santa_visited_locations.add(santa_location)
    robosanta_visited_locations = set()
    robosanta_visited_locations.add(robosanta_location)

    for i, vector in enumerate(data):
        if i % 2 == 1:
            santa_location += ARROW_VECTORS[vector]
            santa_visited_locations.add(santa_location)
        else:
            robosanta_location += ARROW_VECTORS[vector]
            robosanta_visited_locations.add(robosanta_location)

    visited_locations = santa_visited_locations | robosanta_visited_locations
    print(f"Santa and Robosanta visited {len(visited_locations)} locations.")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
