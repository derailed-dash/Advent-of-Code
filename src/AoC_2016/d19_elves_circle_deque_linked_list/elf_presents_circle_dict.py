"""
Author: Darren
Date: 10/09/2021

Solving https://adventofcode.com/2016/day/19

Solution #2.  (#1 was better.)

Part 1:
    Elves sat in a circle.  Each elf brings 1 present.
    Start at elf 1, each elf steals all the presents from the elf to their left (CW).
    Remove elves that have no presents.
    Stop when one elf has all the presents.
    
    Tried to implement using a dict, and then a list of the dict for quickly obtaining positions.
    This performs even worse than the deque. :(
    
    Slow: t(n) = O(n**2)
    Takes too way too long!!

Part 2:
    Slow, as above.
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

NUMBER_OF_ELVES = 1000
# NUMBER_OF_ELVES = 3012210

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")

    # Part 1    
    elves = {}
    for elf_posn in range(1, NUMBER_OF_ELVES+1):
        elves[elf_posn] = 1
        
    logging.debug(elves)
        
    elf_posn = 0
    while len(elves) > 1:   # Loop until only one elf left
        elf_num_list = list(elves)[elf_posn:] + list(elves)[0:elf_posn]  # list of keys (elf numbers)
        taker = elf_num_list[0]
        giver = elf_num_list[1]
        elves[taker] = elves[taker] + elves[giver]
        elves.pop(giver)
        
        # new giver could be back at posn 0
        elf_posn = elf_posn + 1 if elf_posn < (len(elves)-1) else 0
        
    logging.info(f"Part 1: Winning elf is {elves}")
    
    # Part 2
    elves = {}
    for elf_posn in range(1, NUMBER_OF_ELVES+1):
        elves[elf_posn] = 1
        
    elf_posn = 0
    while len(elves) > 1:   # Loop until only one elf left
        
        # This list creation is killing the performance, I think
        elf_num_list = list(elves)[elf_posn:] + list(elves)[0:elf_posn]  # list of keys (elf numbers)
        
        taker = elf_num_list[0]
        giver = elf_num_list[len(elves)//2]
        elves[taker] = elves[taker] + elves[giver]
        elves.pop(giver)
        if giver >= elf_num_list[0]:    # only increment position if we haven't taken away a lower elf
            if giver > elf_num_list[0]:
                elf_posn = elf_posn + 1 if elf_posn < (len(elves)-1) else 0
            else:   # giver removed at our current position
                if elf_posn == (len(elves)-1):
                    elf_posn = 0
        else:
            if elf_posn == len(elves):
                elf_posn = 0
        
    logging.info(f"Part 2: Winning elf is {elves}")
       

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
