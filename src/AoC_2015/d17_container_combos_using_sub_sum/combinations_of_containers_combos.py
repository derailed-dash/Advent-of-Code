""" 
Author: Darren
Date: 06/12/2022

Solving https://adventofcode.com/2015/day/17

We have a bunch of containers.

Part 1:

We need to store 150L using any combination of our containers.
How many combinations are there?

- Solution:
  - Find all combinations of 1 container, then combinations of 2 containers, etc.
  - Valid combinations are only those that add up to 150L.
  
Part 2:

Determine the minimum number of containers to achieve the target.
Then determine how many combinations there are, using this minimum number of containers.

- Solution:
  - Do the same as Part 1, but break when we first find valid combinations.
    At this point, we're already using the minimum number of containers.
  - Count how many combos there were.
"""
from pathlib import Path
from itertools import combinations
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

TARGET = 150

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    containers = process_input(data)
    print(containers)

    all_valid_combos = []  # all the container combos that add up to TARGET
    
    # Try any single container, then any two containers, then any three, etc
    for num_containers in range(1, len(containers)+1):
        valid_combos = [combo for combo in list(combinations(containers, num_containers))
                              if sum(combo) == TARGET]
        all_valid_combos.extend(valid_combos)

    # part 1
    print(f"Part 1: Valid combos that contain {TARGET}L={len(all_valid_combos)}")

    # part 2
    all_valid_combos = []  # all the container combos that add up to TARGET
    for num_containers in range(1, len(containers)+1):
        valid_combos = [combo for combo in list(combinations(containers, num_containers))
                              if sum(combo) == TARGET]
        all_valid_combos.extend(valid_combos)
        if valid_combos:
            break
    
    print(f"Part 2: Combinations with minimum number of containers={len(all_valid_combos)}")

def process_input(data):
    return [int(x) for x in data]

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
