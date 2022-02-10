"""
Author: Darren
Date: 07/12/2021

Solving https://adventofcode.com/2021/day/6

Solution 4 of 4.

Having done this with dicts and with numpy, now let's use a circular deque.
Combining the deque with a Counter allows easy replication of numpy rolling.
This is the quickest and simplest solution.

We have a school of lanternfish. Each fish is immortal.
A new lanternfish spawns a new lanternfish after 9 days, and thereafter, every 7 days.
We start with a list of fish with timers (t) until spawn day, e.g. 3,4,3,1,2.
How many fish will we have after d days?

Part 1:
    We don't need to iterate through each fish.
    We just need to count the timers for all the fish. E.g.
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
from collections import Counter, deque 

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()
    
    data = [int(x) for x in data.split(",")]
    fish_timer_counts = Counter(data) # count the timers for each fish
   
    # initialise an array of timer counts, for all timer values 0-8    
    timers = deque()
    for timer in range(9):
        timers.append(fish_timer_counts[timer] if fish_timer_counts[timer] else 0)
    
    for days in (80, 256):
        logger.info("Fish at day %d: %d", days, get_fish_count(timers, days))

def get_fish_count(timers: deque, days: int):
    fish = timers.copy()    # just so we can repeat this method with a different # of days
    
    for _ in range(days):
        fish.rotate(-1)
        fish[6] += fish[8]  # count of newly spawned fish is same as count of fish that need to be reset
        
    return sum(fish)        

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
