"""
Author: Darren
Date: 07/12/2021

Solving https://adventofcode.com/2021/day/7

We have a number of crabs aligned in different horizontal positions.
E.g. 16,1,2,0,4,2,7,1,2,14
We need to line them up in a single vertical line, 
i.e. so that they're all at the same horizontal position.
Each move a crab makes takes fuel.  
We need to determine which final horizontal alignment position consumes the least fuel.

Here we use numpy to manipulate the array of input data.

Part 1:
    Read in csv as numpy array.
    For each horizontal position available, determine the (abs) horizontal diff for each crab.
    Sum up all these horizontal diffs, and store in a dict against the position.
    Then return the minimum diff sum (and its position)

Part 2:
    Same, but now add a function that changes the fuel cost per unit moved by each crab.
    Move 1 costs 1 unit, move 2 costs 2 units, etc.  Thus, cost is simply sum(range).
    However, sum of range (1..n) is slow.  Much quicker to use sum of arithmetic progression:
    s(a->n) = n/2*(2a+(n-1)d)
    where a is 1st term, n is last term, and d is the diff.
    With a=1 and d=1: s(1->n) = n/2*(n+1)    
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
    data: np.ndarray = np.loadtxt(input_file, delimiter=",", dtype=np.int32)
    
    logger.info("Part 1 min cost: %s", get_min_cost(data))
    logger.info("Part 2 min cost: %s", get_min_cost(data, lambda n: n*(n+1)//2)) 

def get_min_cost(data: np.ndarray, cost_func=lambda x: 1*x) -> tuple:
    """ Function that determines the minimum total cost to arrange our crabs.

    Args:
        data (ndarray): The initial crab positions
        cost_func (func, optional): Determines the cost for a given distance.
                                    Defaults to a cost of 1 per unit distance.

    Returns:
        tuple: Alignment position, cost
    """
    max_horizontal = max(data)  # i.e. the crab that is furthest out
    
    costs = {}  # Store {position: total-cost-to-get-to-this-position}
    for i in range(max_horizontal+1):
        individual_diffs = (abs(data - i))  # array of steps to reach this horizontal position
        
        # vectorise costs function, i.e. a function that applies to each element
        costs_v = np.vectorize(cost_func)  # bind costs_v variable to the vectorised function
        costs[i] = sum(costs_v(individual_diffs))   # apply cost function to the diffs and sum them
        
        # Or we could have done it by using comprehension, but this is slower than the costs_v
        # costs[i] = sum(cost_func(diff) for diff in individual_diffs)       

    min_cost = min(costs.items(), key=lambda x: x[1])
    return min_cost   

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
