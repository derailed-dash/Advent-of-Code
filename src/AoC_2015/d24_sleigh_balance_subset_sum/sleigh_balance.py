""" 
Author: Darren
Date: 02/05/2021

Solving https://adventofcode.com/2015/day/24

We require three bags of equal weight. 
   Bag 1 in the passenger compartment, needs to have fewest packages.
   Bags 2 and 3 to either side.
   
Solution:
   Use subset sum function to work out which combinations of packages adds up to 
   total weight / number of bags (compartments).
   The faster subsum is about 3x quicker than the version that uses itertools.combinations.
   Once we have all combinations for the first bag, sort by the number of packages, 
   since we want the first bag to have fewest possible packages.
   
   We don't care about what's in bags 2, 3...
   I.e. because we know we will have valid combinations of packages that will add up to the same weight

"""
from __future__ import absolute_import
import logging
import os
import time
from math import prod
from itertools import combinations

# pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
    
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        package_weights = [int(x) for x in f.read().splitlines()]
    
    logging.info(f"Package weights: {package_weights}")

    # Part 1
    optimum_solution = distribute_packages(package_weights, 3)
    logging.info(f"Solution found with QE {get_quantum_entanglement(optimum_solution)}")
    logging.info(f"First bag: {optimum_solution}")
    
    # Part 2
    optimum_solution = distribute_packages(package_weights, 4)
    logging.info(f"Solution found with QE {get_quantum_entanglement(optimum_solution)}")
    logging.info(f"First bag: {optimum_solution}")


def distribute_packages(package_weights, number_of_bags) -> tuple:
    logging.info(f"Solving for {number_of_bags} bags")
    
    package_count = len(package_weights)
    total_weight = sum(package_weights)
    target_weight_per_bag = total_weight // number_of_bags
    
    logging.debug(f"Total packages: {package_count}, with total weight: {total_weight}")
    logging.debug(f"Target weight per bag: {target_weight_per_bag}")

    # Get all combos for first bag.
    # Sort by bags in the combo, since the first bag should have fewest packages.    
    first_bag_combos = faster_subset_sum(package_weights, target_weight_per_bag)
    first_bag_combos = sorted(first_bag_combos, key=len)
    
    # store first bag of optimum solution
    optimum_solution = tuple()
        
    for first_bag_combo in first_bag_combos:
        # First bag must have smallest number of packages
        # Skip any bag combos that have more packages than a previous solution
        if len(optimum_solution) > 0:
            if len(first_bag_combo) > len(optimum_solution):
                continue
            
            # if quantum entanglement of the first bag is higher than an existing solution,
            # then skip it
            if get_quantum_entanglement(first_bag_combo) >= get_quantum_entanglement(optimum_solution):
                continue
            
        optimum_solution = first_bag_combo
        
    return optimum_solution
            

def get_quantum_entanglement(bag: tuple):
    return prod(bag)


def faster_subset_sum(items: list, target: int, partial=[], results=[]) -> list:
    """
    Determine all combinations of list items that add up to the target
    
    Args:
        numbers (list): A list of values
        target (int): The total that the values need to add up to
        partial (list, optional): Used by the function. Defaults to [].
        results (list, optional): Used by the function. Defaults to [].

    Returns:
        list: The list of valid combinations
    """
    total = sum(partial)

    # check if the partial sum is equals to target, and if so
    # add the current terms to the results list
    if total == target:
        results.append(partial)
        
    # if the partial sum equals or exceed the target, no point in recursing through remaining terms.
    if total >= target:
        return []

    for i, item in enumerate(items):
        remaining_numbers = items[i + 1:]
        faster_subset_sum(remaining_numbers, target, partial + [item], results)

    return results


def simple_subset_sum(items, target: int) -> tuple:
    """ Return a tuple of any combinations of items that adds up to the target

    Args:
        items (Sequence): List/set of items
        target (int): The target sum to achieve

    Yields:
        Iterator[tuple]: Items that achieve the desired sum
    """
    # Iterating through all possible subsets of collection from lengths 0 to n:
    for i in range(len(items)+1):
        for subset in combinations(items, i):
              
            # printing the subset if its sum is x:
            if sum(subset) == target:
                yield subset
                

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
