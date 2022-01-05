"""
Author: Darren
Date: 01/12/2021

Solving https://adventofcode.com/2021/day/1

Input looks like:
199
200
208
210
200

Part 1:
    From a list of depth figures, count how many times the depth increases.

Part 2:
    Now count how many times a sliding window of the sum of three depths increases.
    Let's use a deque (stack) with a window size of three.

"""
import logging
import os
import time
from collections import deque

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        depths = f.read().splitlines()
    
    depths = list(map(int, depths))
    
    # Part 1
    increase_counter = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i-1]:
            increase_counter += 1
    
    logger.info("There are %d measurements", len(depths))
    logger.info("Depth increases %d times", increase_counter)
    
    # Part 2
    measurements_window_sz = 3
    three_measurements = deque(depths[0:measurements_window_sz], maxlen=measurements_window_sz)
    last_three_sum = sum(three_measurements)
    
    increase_counter = 0
    for i in range(measurements_window_sz, len(depths)):
        three_measurements.append(depths[i])
        current_three_sum = sum(three_measurements)
        if current_three_sum > last_three_sum:
            increase_counter += 1
            
        last_three_sum = current_three_sum
    
    logger.info("Depth increases %d times", increase_counter)

t1 = time.perf_counter()
main()
t2 = time.perf_counter()
logger.info("Execution time: %0.4f seconds", t2 - t1)
