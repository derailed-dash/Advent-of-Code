""" 
Author: Darren
Date: 27/02/2021

Solving https://adventofcode.com/2015/day/17

Find all combinations of containers that can store 150L

Part 1:
    Use recursive sub sum pattern.

Part 2:
    Determine the minimum number of containers to achieve the target.
    Determine how many combinations there are, using this minimum number of containers.
"""
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

TARGET = 150

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    containers = process_input(data)

    # part 1
    valid_combos = subset_sum(containers, TARGET)
    print(f"Part 1 valid_combos to contain {TARGET}l: {len(valid_combos)}")

    # part 2
    min_containers = min(len(combo) for combo in valid_combos)
    print(f"Minimum number of containers for {TARGET}l: {min_containers}")

    min_container_combos = [combo for combo in valid_combos if len(combo) == min_containers]
    print(f"Number of combos only using the minimum number of containers: {len(min_container_combos)}")


# pylint: disable=dangerous-default-value
def subset_sum(numbers: list, target: int, partial=[], results=[]) -> list:
    """
    Determine all combinations of list items that add up to the target

    :param numbers: A list of values
    :type numbers: list
    :param target: The total that the values need to add up to
    :type target: int
    :param partial: Used by the function, defaults to []
    :type partial: list, optional
    :param results: Used by the function, defaults to []
    :type results: list, optional
    :return: The list of valid combinations
    :rtype: list
    """
    s = sum(partial)

    # Determine all combinations of list items that add up to the target.
    
    # Args:
    #     numbers (list): A list of values
    #     target (int): The total that the values need to add up to
    #     partial (list, optional): Used by the function. Defaults to [].
    #     results (list, optional): Used by the function. Defaults to [].

    # Returns:
    #     [list]: The list of valid combinations


    # check if the partial sum is equals to target, and if so
    # add the current terms to the results list
    if s == target:
        results.append(partial)
    # if the partial sum equals or exceed the target, 
    # no point in recursing through remaining terms.
    if s >= target:
        return []

    for i, n in enumerate(numbers):
        remaining_numbers = numbers[i + 1:]
        subset_sum(remaining_numbers, target, partial + [n], results)

    return results


def process_input(data):
    return [int(x) for x in data]

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
