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

This is solution v2. No numpy for this one.

Part 1:
    For each horizontal position available, determine the (abs) horizontal diff for each crab.
    Sum up all these horizontal diffs, and store in a dict against the position.
    Then return the minimum diff sum (and its position)

Part 2:
    Same, but now add a function that changes the fuel cost per unit moved by each crab.
    Move 1 costs 1 unit, move 2 costs 2 units, etc.  Thus, cost is simply sum(range).
    However, sum of range (1..n) is slow.  Much quicker to use sum of arithmetic progression:
    s(a -> n) = n/2*(2a+(n-1)d)
    where a is 1st term, n is last term, and d is diff.
    With a=1 and d=1: s(1->n) = n/2*(n+1)
"""
import logging
import os
import time

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
        data = [int(x) for x in f.read().split(",")]
    
    logger.info("Part 1 min cost: %s", get_min_cost(data))
    logger.info("Part 2 min cost: %s", get_min_cost(data, lambda n: n*(n+1)/2)) 

def get_min_cost(data, cost_func=lambda x: x) -> tuple:
    """ Function that determines the minimum total cost to arrange our crabs

    Args:
        data (array): The initial crab positions
        cost_func (func, optional): Determines the cost for a given distance.
                                    Defaults to a cost of 1 per unit distance.

    Returns:
        tuple: Alignment position, cost
    """
    max_horizontal = max(data)
    
    costs = {}
    for i in range(max_horizontal+1):
        individual_costs = []
        for posn in data:
            individual_costs.append(cost_func(abs(posn - i)))
        
        costs[i] = int(sum(individual_costs))    # sun of all the costs to reach this position

    min_cost = min(costs.items(), key=lambda x: x[1])
    return min_cost   

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
