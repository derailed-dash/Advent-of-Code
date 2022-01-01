"""
Author: Darren
Date: 10/09/2021

Solving https://adventofcode.com/2016/day/19

Solution #3.  (#1 was better.)

Part 1:
    Tried using a SortedSet, since SortedSet uses binary searching.
    Yet still O(n**2).  Sad times. :(
    Probably due to the list within the SortedSet having to rebuild with every del.

Part 2:
    No point trying.
"""
import logging
import os
import time
from sorted_set import SortedSet

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

NUMBER_OF_ELVES = 20
# NUMBER_OF_ELVES = 3012210

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")

    # Part 1    
    elves = SortedSet(range(1, NUMBER_OF_ELVES+1))
    
    elves_count = len(elves)
    elf_index = 0
    while True:           # Loop until only one elf left
        discard_elf_posn = elf_index+1 if elf_index < (elves_count-1) else 0
        
        # I think the underlying list takes a while to rebuld.  That's why we get O(n**2) performance.
        del elves[discard_elf_posn]
        elves_count -= 1
        
        if elves_count == 1:
            break
        
        if elf_index >= (elves_count-1):
            elf_index = 0
        else:
            elf_index += 1
        
    logging.info(f"Part 1: Winning elf is {elves[0]}")
    
    # Part 2    
    # elves = deque()
    # for elf_num in range(1, NUMBER_OF_ELVES+1):
    #     elves.append([elf_num, 1])  # Initialise all our elves to 1 present
        
    # while len(elves) > 1:           # Loop until only one elf left
    #     elf_opposite = len(elves) // 2
    #     elves[0][1] = elves[0][1] + elves[elf_opposite][1]     # Elf takes all presents from elf on the right
    #     elves[elf_opposite][1] = 0     # Set elf on right to 0 presents
    #     elves.rotate(-elf_opposite)    # Rotate until we reach the elf that was stolen from
    #     elves.popleft()     # Pop the elf on the left, since they have 0 presents
    #     elves.rotate(elf_opposite-1)    # Now rotate back, until we're on the 'next elf
        
    #     # alternatively, we could just delete the one opposite and rotate one.  Same performance...
    #     # del elves[elf_opposite]
    #     # elves.rotate(-1)    # Rotate left.  So the elf that was on the right is now first elf
        
    # logging.info(f"Part 2: Winning elf is {elves[0][0]}")
       

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
