"""
Author: Darren
Date: 06/12/2021

Solving https://adventofcode.com/2021/day/6

Solution 2 of 4.

We have a school of lanternfish. Each fish is immortal.
A new lanternfish spawns a new lanternfish after 9 days, and thereafter, every 7 days.
We start with a list of fish with timers (t) until spawn day, e.g. 3,4,3,1,2.
How many fish will we have after d days?

My first attempt simply iterated through each timer, 
and grew the school with each iteration.  That's far too inefficient when d is large.

Part 1:
    We don't need to iterate through each fish.
    We just need to count the timers for all the fish timer types. E.g.
    Counter({1: 162, 4: 47, 2: 36, 5: 28, 3: 27})
    
    Now we can simply update the counters according to the rules, i.e.
        When 0: add this count to 6 (reset), and add this count to 8 (spawn)
        Else: add this count to t-1.

Part 2:
    No changes required.  This runs really quickly!
"""
import logging
import os
import time
from collections import defaultdict, Counter 

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()
        
    data = list(map(int, data.split(",")))
    
    # count the timers for each fish
    fish_timer_counts = Counter(data)
    for days in (80, 256):
        logger.info("Fish at day %d: %d", days, get_fish_count(fish_timer_counts, days))

def get_fish_count(fish_timer_counts, days):
    for _ in range(days):
        # so we can create new counts without key errors
        new_fish_timer_counts = defaultdict(int)
        
        # loop through timers.  
        # There will only ever be a max of 9 different timers, i.e. 0-8.
        for timer, count in fish_timer_counts.items():
            if timer == 0:     # reset timer and spawn a new fish
                new_fish_timer_counts[6] += count   # reset this fish timer
                new_fish_timer_counts[8] += count   # spawn new fish
            else:       # All t should now become t-1
                # E.g. count-of-fish-0 += count-of-fish-1
                new_fish_timer_counts[timer-1] += count
        
        fish_timer_counts = new_fish_timer_counts
        
    return sum(fish_timer_counts.values())
        

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
