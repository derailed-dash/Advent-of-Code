"""
Author: Darren
Date: 04/12/2022

Solving https://adventofcode.com/2022/day/4

The elves have paired up and compared their section assignments, e.g.
2-4,6-8
2-3,4-5
5-7,7-9

Part 1:

How many assignment pairs where one assignment fully contains the other.

- Solution:
  - Read each pair, and turn the x-y to a range.
  - Convert each range to a set, so we can easily perform set algebra.
  - Count where one issubset of the other, or if they are equal.

Part 2:

In how many assignment pairs do the ranges overlap?

- Solution:
  - Count where sets intersect.
"""
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    pairs = process_data(data)
    
    includes_count = sum(1 for assn_1, assn_2 in pairs 
                         if assn_1 == assn_2 or assn_1 < assn_2 or assn_2 < assn_1)
    print(f"Part 1: Assigment inclusions = {includes_count}")
    
    overlap_count = sum(1 for assn_1, assn_2 in pairs if assn_1 & assn_2)
    print(f"Part 2: Assigment overlap = {overlap_count}")    
        
def process_data(data: list[str]) -> list[set]:
    """ Process data pairs.  Each line is a pair, with each item being an x-y range.
    Convert each x-y range to a set, containing an expanded range of int values.
    E.g. 2-4,6-8 -> [{2,3,4}{6,7,8}] """
    
    pairs = [] # We want [[2,3,4][6,7,8]]
    for line in data:
        this_pair = line.split(",") # E.g. ["2-4"]["6-8"]
        assignments = []
        for elf in this_pair:
            start, end = list(map(int, elf.split("-")))  # E.g. 2, 4
            assignments.append(set(range(start, end+1)))   # E.g. {2,3,4}
            
        pairs.append(assignments)

    return pairs
        
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
