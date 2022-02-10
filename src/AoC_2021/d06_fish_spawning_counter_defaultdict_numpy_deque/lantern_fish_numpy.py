"""
Author: Darren
Date: 06/12/2021

Solving https://adventofcode.com/2021/day/6

Solution 3 of 4: Using numpy.

Numpy has the advantages that:
    - We can read in the csv into an array directly.
    - We can initialise a bunch of fish timers to 0.
    - We can set initial fish timer counts based on a count array.
    - We can roll the array. 

We have a school of lanternfish. Each fish is immortal.
A new lanternfish spawns a new lanternfish after 9 days, and thereafter, every 7 days.
We start with a list of fish with timers (t) until spawn day, e.g. 3,4,3,1,2.
How many fish will we have after d days?

Part 1:
    Use numpy to count the number of fish with a given timer, using np.unique().
    There are only ever 9 generations of timer: [0 1 2 3 4 5 6 7 8]
    For each day, roll the current ndarray.
    Since 0 becomes 8, this automatically handles spawns.
    And then add the previous day 0 count to day 6, for spawners.

Part 2:
    No changes required.
"""
import logging
import os
import time
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    
    # read input, which is csv of ints
    # Each value is a fish timer, i.e. days until spawning another fish  
    data = np.loadtxt(input_file, delimiter=",", dtype=np.int8) # [3 4 3 1 2]  
 
    # np.unique() returns ordered unique items.  With return_counts=True, it includes counts.
    # Timers [1 2 3 4], counts [1 1 2 1]
    init_fish_timers, counts = np.unique(data, return_counts=True)

    # Initialise fish timers, by setting index positions to the counts in the array  
    fish_timers = np.zeros(9, dtype=np.uint64)     # [0 0 0 0 0 0 0 0 0]
    fish_timers[init_fish_timers] = counts         # [0 1 1 2 1 0 0 0 0]
    
    for day in (80, 256):
        logger.info("At day %d, count=%d", day, get_fish_count(fish_timers, day))

def get_fish_count(fish_timers: np.ndarray, day_num: int) -> int:
    fish = np.copy(fish_timers)    # create a new copy so we don't mutate the original fish
    for _ in range(day_num):
        fish = np.roll(fish, -1)  # Roll: 2 becomes 1, 1 becomes 0, 0 becomes 8 (spawned fish)  
        fish[6] += fish[8]    # Add fish that were 0 are now reset to 6.
    
    return sum(fish)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
