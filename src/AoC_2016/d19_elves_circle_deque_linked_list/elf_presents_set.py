"""
Author: Darren
Date: 10/09/2021

Solving https://adventofcode.com/2016/day/19

Solution #4.  Good for part 1, but no good for part 2.

Part 1:
    Using sets works pretty well.
    We can use a generator to yield each elf in the range, 
    but filter out any bad_elves using a bad_elves set.
    The beauty of this approach is that bad_elves is updated each time an elf is removed,
    and the generator constantly uses the updated bad_elves when returning the next elf.
    We restart the generator each time we get to the end of the circle and start again.
    
    Performance = O(n).

Part 2:
    Sets aren't going to work for part 2!
    
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

NUMBER_OF_ELVES = 10
# NUMBER_OF_ELVES = 3012210

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")

    # Part 1    
    bad_elves = set()
    
    # generator is cool, because bad_elves is constantly updated by the for loop later
    elves = (elf for elf in range(1, NUMBER_OF_ELVES+1) if elf not in bad_elves)    

    last_elf_good = False
    elves_count = NUMBER_OF_ELVES
    while elves_count > 1:           # Loop until only one elf left
        for elf in elves:
            if last_elf_good:
                bad_elves.add(elf)
                elves_count -= 1
                last_elf_good = False
            else:
                last_elf_good = True
        
        # recreate the generator when we've counted up through all the elves
        elves = (elf for elf in range(1, NUMBER_OF_ELVES+1) if elf not in bad_elves)

    logging.info(f"Part 1: Winning elf is {list(elves)}")
       

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
