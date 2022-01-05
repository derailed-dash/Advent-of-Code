"""
Author: Darren
Date: 03/12/2021

Solving https://adventofcode.com/2021/day/1

Now a solution using numpy. 
It's slower than solution 1, which iterates over elements and uses a deque for sliding windows.
But this solution is VERY neat!

Part 1:
    From a list of depth figures, count how many times the depth increases.
    Use a numpy array, and compare each element n to n-1, and sum the count of where element n is larger.

Part 2:
    Now count how many times a sliding window of the sum of three depths increases.
    This is the comparison: x[n+3] + x[n+2] + x[n+1] > x[n+2] + x[n+1] + x[n]
    This simplifies to: x[n+3] > x[n]

"""
import logging
import os
import time
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    depths = np.loadtxt(input_file)
    
    # Part 1
    # sum count of where depth n is greater than depth n-1, where n starts at 1, to the last.
    increase_count = (depths[1:] > depths[:-1]).sum()
    logger.info("Part 1: Depth increases %d times", increase_count)
    
    # Part 2
    window_sz = 3
    # sum count of where n > n-3, where n starts at 3, to the last.
    increase_count = (depths[window_sz:] > depths[:-window_sz]).sum()
    logger.info("Part 2:Depth increases %d times", increase_count)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
