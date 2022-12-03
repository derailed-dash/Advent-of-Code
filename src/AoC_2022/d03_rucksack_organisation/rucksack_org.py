"""
Author: Darren
Date: 03/12/2022

Solving https://adventofcode.com/2022/day/3

Input lines each represent a rucksack full of items. Lines look like:
vJrwpWtwJgWrhcsFMMfFFhFp
- Each letter represents an item. 
- 1st half is compartment 1. 2nd half is compartment 2.
- Letterz a-z are priorities 1-26. Letterz A-Z are priorities 27-52.

Part 1:

Find the item type that appears in both compartments of each rucksack. 
What is the sum of the priorities of those item types?

- Solution:
  - Build a dict that maps all chars to their priority values.
  - Split the rucksack into two compartments. 
  - Turn each compartment to a set to remove duplicates.
  - Use the set intersection to return the items that are common to both compartments.
  - Convert the common items to their priorities and sum them.

Part 2:

Find the item type that corresponds to the badges of each three-Elf group. 
What is the sum of the priorities of those item types?

- Solution:
  - Use a defaultdict[list] to store rucksack items for each group of 3 elves.
    The key of the dict is the group number.
  - Iterate through the group values. Each value is a list of rucksacks.
    - Convert each rucksack to a set.
    - Find the intersection of the three sets in this group.
    - Convert the intersection items to priorities and sum them
"""
from collections import defaultdict
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

GRP_SZ = 3

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    item_to_priority = {} # a:1, b:2... Y:51, Z:52
    for i, ordinal in enumerate(range(ord('a'), ord('z')+1), start=1):
        item_to_priority[chr(ordinal)] = i
    for i, ordinal in enumerate(range(ord('A'), ord('Z')+1), start=27):
        item_to_priority[chr(ordinal)] = i
    
    priorities = []
    for rucksack in data:
        compartment_1 = set(rucksack[0:len(rucksack)//2])
        compartment_2 = set(rucksack[len(rucksack)//2:])
        common = compartment_1 & compartment_2 # intersection
        for item in common:
            priorities.append(item_to_priority[item])
    
    print(f"Part 1: Sum of priorities = {sum(priorities)}")
    
    # Goal is # {1: ['vJrw...', 'jqHR...', 'Pmmd...'], 2: [...], ...} etc
    groups = defaultdict(list) 
    group_num = 1
    for line_num, rucksack in enumerate(data):
        if line_num > 0 and line_num % GRP_SZ == 0:
            group_num += 1
        
        groups[group_num] += [rucksack]
    
    priorities = []
    for rucksacks in groups.values():
        rucksack_sets = [set(sack) for sack in rucksacks]
        common = set.intersection(*rucksack_sets)
        for item in common:
            priorities.append(item_to_priority[item])        
        
    print(f"Part 2: Sum of priorities = {sum(priorities)}")
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
