"""
Author: Darren
Date: 06/12/2021

Solving https://adventofcode.com/2021/day/6

Solution 1 of 4.

We have a school of lanternfish. Each fish is immortal.
A new lanternfish spawns a new lanternfish after 9 days, and thereafter, every 7 days.
We start with a list of fish with timers (t) until spawn day, e.g. 3,4,3,1,2.
How many fish will we have after d days?

We're getting exponential growth every ~7 days, 
so with f initial fish and d days, expect n = f*(d/7)

Part 1:
    Iterate through each fish.  
    If t=0, reset this timer and add a new fish with t=8.
    Else t=t-1.
    Works pretty well.

Part 2:
    We're seeing exponential growth every ~7 days.  I.e. we double our processing time every ~7.
    With 120 days, ~9s.  So with 150 days, expect 9*2^(30/7) = ~140s.  
    With 256 days, we'd be running for several days!
    We need a better solution!
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()
        
    fish_timers = list(map(int, data.split(",")))
    logger.debug(fish_timers)   # E.g. [3,4,3,1,2]
    
    t1 = time.perf_counter()
    fish_timers_copy = fish_timers.copy()
    days = 80
    for _ in range(1, days+1):
        # we can't enumerate since we don't extra iterations when we spawn
        for i in range(len(fish_timers_copy)):
            if fish_timers_copy[i] == 0:
                fish_timers_copy[i] = 6     # reset this fish timer
                fish_timers_copy.append(8)  # spawn a new fish
            else:
                fish_timers_copy[i] -= 1    # decrement this fish timer
    
    logger.info("After %d days, there are %d fish", days, len(fish_timers_copy))
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)      

    t1 = time.perf_counter()
    fish_timers_copy = fish_timers.copy()
    days = 120
    for _ in range(1, days+1):
        # we can't enumerate since we don't extra iterations when we spawn
        for i in range(len(fish_timers_copy)):
            if fish_timers_copy[i] == 0:
                fish_timers_copy[i] = 6     # reset this fish timer
                fish_timers_copy.append(8)  # spawn a new fish
            else:
                fish_timers_copy[i] -= 1    # decrement this fish timer
    
    logger.info("After %d days, there are %d fish", days, len(fish_timers_copy))
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)          
    

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
