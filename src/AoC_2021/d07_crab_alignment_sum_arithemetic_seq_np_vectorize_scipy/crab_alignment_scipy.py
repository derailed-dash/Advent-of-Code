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

Solution 3:
    Use numpy to read in the csv and store as an array.
    Then use scipy optimize.minimum_scaler to obtain the minimum value.
    This solution is REALLY fast.

Part 1:
    Read in csv as numpy array.determine the (abs) horizontal diff for each crab.
    Provide a cost function that determines cost to get to a given position.
    Then pass the cost function to optimize.minimize_scalar, 
    to determine the best possible findal position that minimises the result.

Part 2:
    Same, as before, but change the cost_func to use the sum of arithmetic progression,
    with a (1st term)=1 and d (diff)=1:
    s(a->n) = n/2*(2a+(n-1)d) = n/2*(n+1)    
"""
import logging
import os
import time
import numpy as np
from scipy import optimize

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    data: np.ndarray = np.loadtxt(input_file, delimiter=",", dtype=np.int32)
    
    # minimize_scaler expects the function as first param, 
    # and args are any additional params the func requires
    cost_part_1 = optimize.minimize_scalar(cost, args=(data))
    logger.info("Part 1 min cost: %s", round(cost_part_1.fun))
    
    cost_part_2 = optimize.minimize_scalar(cost, args=(data, lambda n: n*(n+1)/2))
    logger.info("Part 2 min cost: %s", round(cost_part_2.fun)) 
        
def cost(posn: int, data: np.ndarray, cost_func=lambda n: n) -> int:
    """ Return the sum of applying the cost_func to get to position n, for every item in the array.

    Args:
        posn (int): The position we need each crab to get to
        data (ndarray): The initial crab positions
        cost_func (func, optional): Determines the cost for a given distance.
                                    Defaults to a cost of 1 per unit distance. """
    return cost_func(np.abs(posn-data)).sum()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
