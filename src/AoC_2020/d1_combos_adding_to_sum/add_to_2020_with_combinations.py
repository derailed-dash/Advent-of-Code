""" Add_to_2020.py
Author: Darren
Date: 05/12/2020

Solving https://adventofcode.com/2020/day/1

Process a list of numbers, and determine which two numbers add up to 2020.
Process a list of numbers and determine which three numbers add up to 2020.

Solution 2 of 2:

This program uses itertools.combinations() to return all the combinations from n numbers.
Thus, we can generically use the function to any n numbers.
It is brute force, so not particularly fast.
"""

import sys
import os
import time
import re
from typing import List, Tuple
from itertools import combinations
from math import prod as prod

INPUT_FILE = "input/expenses.txt"

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    print("Input file is: " + input_file)
    entries = read_input(input_file)
    # print(entries)

    target = 2020
    terms = determine_terms(entries, target, 2)
    print(f"Terms: {terms}.")
    print(f"And the product is: " + str(prod(terms)))
    
    terms = determine_terms(entries, target, 3)
    print(f"Terms: {terms}.")
    print(f"And the product is: " + str(prod(terms)))


def determine_terms(entries: List[int], target: int, num_terms: int) -> tuple:
    """ Determine combination of terms that add up to the target

    Args:
        entries ([list]): List of int values
        target ([int]): The target sum of any n terms
        num_terms ([int]): The number of terms, n, that must add up to the target

    Returns:
        [type]: [description]
    """
    for num_list in combinations(entries, num_terms):
        the_sum = sum(num_list)
        if the_sum == target:
            return num_list

    return ()


def read_input(a_file) -> List[int]:
    with open(a_file, mode="rt") as f:
        entries_list = [int(x) for x in f.read().splitlines()]

    return entries_list


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")