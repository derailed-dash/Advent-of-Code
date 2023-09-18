""" 
Author: Darren
Date: 02/05/2021

Solving https://adventofcode.com/2015/day/24

We require three bags of equal weight. 
    3 groups: one in the middle, and on on each side.
    We are given a list of package weights.
    We must distribute packages across the 3 groups, such that each group has the same weight.
    The central group needs to have the fewest packages.
    If there is more than one solution with equal minimum number of packages,
    then return the group of packages with the lowest QE, where QE = product of package weights
   
Solution for Part 1:
  - Add up the package weights and divide by 3. This is our required weight for each group.
  - We only care about the middle group. The configurations of the other two groups are irrelevant.
  - So, try combinations of packages that sum to the required weight.
    Start with 1 package, then 2, then 3, etc. 
  - The first returned valid combinations will be of the fewest number of packages.
  - If more than one valid combo is returned, find the minimum based on QE.
  
Solution for Part 2:
  - Same as before, but use 4 instead of 3. Easy!
  
This solution works pretty well... About 0.2s for both parts.
"""
from __future__ import absolute_import
import logging
import time
from math import prod
from itertools import combinations
import aoc_commons as ac

YEAR = 2015
DAY = 24

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
ac.write_puzzle_input_file(YEAR, DAY, locations)

def main():
    # with open(locations.sample_input_file, mode="rt") as f:
    with open(locations.input_file, mode="rt") as f:
        package_weights = [int(x) for x in f.read().splitlines()]
    
    logger.debug(f"Package weights: {package_weights}")

    run_part(1, package_weights, 3)
    run_part(2, package_weights, 4)
    
def run_part(part: int, package_weights, number_of_groups: int):
    optimum_solution = distribute_packages(package_weights, number_of_groups)
    logger.info("Part %d:", part)
    logger.info(f"First group: {optimum_solution}")
    logger.info(f"QE: {get_quantum_entanglement(optimum_solution)}")
    logger.info(".")

def distribute_packages(package_weights, number_of_groups) -> tuple:
    logger.info(f"Solving for {number_of_groups} groups")
    
    package_count = len(package_weights)
    total_weight = sum(package_weights)
    target_weight_per_group = total_weight // number_of_groups
    
    logger.info(f"Total packages: {package_count}, with total weight: {total_weight}")
    logger.info(f"Target weight per bag: {target_weight_per_group}")

    # Get all combos for first group.
    # Try any single package, then any two packages, then any three, etc
    # Since we need fewest packages that add up to target weight,
    # there's no point trying more than package_count // number_of_groups
    valid_combos = None
    for num_packages in range(1, (package_count // number_of_groups) +1):
        logger.debug("Trying %d packages...", num_packages)
        valid_combos = [combo for combo in list(combinations(package_weights, num_packages))
                              if sum(combo) == target_weight_per_group]
        if valid_combos: # we've found a solution
            break
    
    assert valid_combos, "There should be a matching combo"
    logger.debug(valid_combos)

    return min(valid_combos, key=get_quantum_entanglement)
            
def get_quantum_entanglement(bag: tuple):
    """ QE = the product of the values in the tuple """
    return prod(bag)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
