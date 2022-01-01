"""
Author: Darren
Date: 10/09/2021

Solving https://adventofcode.com/2016/day/19

Solution 6.
This is BY FAR the best of my six solutions.
This one uses the deque as a ready made linked list, much like solution 1.
But unlike solution 1, we never have to convert to a list to 

Part 1:
    Elves sat in a circle.  Each elf brings 1 present.
    Start at elf 1, each elf steals all the presents from the elf to their left (CW).
    Remove elves that have no presents.
    Stop when one elf has all the presents.
    
    Implement using a deque, since this allows us to efficiently pop "empty" elves
    and supports a rotate method in order to replicate the circular group of elves.
    This way, we don't have to mess about with what happens when we reach the ends.
    Simply start with elf 1, take from elf 2, pop elf 2, 
    then rotate left such that elf 2 is now at the beginning.
    Rinse and repeat until only 1 elf left.
    
    Takes < 2s.
    t(n) = O(n), i.e. linear performance.

Part 2:

"""
import logging
import os
import time
from collections import deque

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

NUMBER_OF_ELVES = 10000
# NUMBER_OF_ELVES = 3012210

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")

    # Part 1    
    elves = deque(range(1, NUMBER_OF_ELVES+1))
    counter = 0    
    while len(elves) > 1:           # Loop until only one elf left
        # We want to pop every other elf
        if counter % 2 != 0:
            elves.popleft()     # Pop this elf, since they have 0 presents
        else:
            elves.rotate(-1)    # Skip this elf. So the elf that was on the right is now first elf
        counter += 1
        
    logging.info(f"Part 1: Winning elf is {elves[0]}")
    
    # Part 2    
    elves = deque(range(1, NUMBER_OF_ELVES+1))
    counter = 0
    elf_opposite = len(elves) // 2     # initial position of elf that is opposite start
    elves.rotate(-elf_opposite)    # Rotate until we reach the elf opposite
    while len(elves) > 1:           # Loop until only one elf left
        elves.popleft()     # Pop this elf (the one opposite)
        
        # Having just popped the elf that *was* opposite
        # we're now positioned at the elf that is now opposite, or the one before.
        # Remember that the elf that is opposite is either next, or next+1, 
        # which alternates as the circle shrinks.
        if counter % 2 != 0:
            elves.rotate(-1)    # Position CW by one additional place, every other pop.
        
        counter += 1
        
    logging.info(f"Part 2: Winning elf is {elves[0]}")

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
