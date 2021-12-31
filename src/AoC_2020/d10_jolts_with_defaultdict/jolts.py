"""
Author: Darren
Date: 11/12/2020

Solving: https://adventofcode.com/2020/day/10

The initial output from the console is 0 jolts. 
We have a bag of joltage adapters.
Any adapter can take input of 1, 2 or 3 jolts lower than its rated joltage.
Our device is rated 3 jolts higher than any adapter in the bag.

Part 1: create a chain of all joltage adapters, and determine jolt differences.
Part 2: find all combinations where the difference between adapters is 3 jolts or less
"""
import os
import time
from collections import defaultdict
from pprint import pprint as pp

INPUT_FILE = "input/jolts.txt"
SAMPLE_INPUT_FILE = "input/sample_jolts.txt"
PREAMBLE_SIZE = 25

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)
    joltages = read_input(input_file)

    # add source charging point at 0 jolts and target at max+3
    joltages.append(0)
    joltages.append(max(joltages)+3)

    joltages.sort()
    pp(joltages)

    diffs = process_differences(joltages)
    print(f"1 jolt diffs: {diffs[1]} and 3 jolt diffs: {diffs[3]}")
    print(f"Product: {diffs[1]*diffs[3]}")

    adapter_permutations = find_adapter_permutations(joltages)
    print(f"Max permutations: {adapter_permutations}")


def find_adapter_permutations(seq: list):
    # seed with entry for 0 permutations that only includes the charging point
    solutions = {0: 1}

    # iterate through all sorted adapter ratings, after 0
    # e.g. [1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22]
    for i in range(1, len(seq)):
        # E.g. when i = 1, adapter_jolts = 4
        adapter_jolts = seq[i]
        
        # create new dict entry for this adapter
        # e.g. {4: 0}
        solutions[adapter_jolts] = 0

        # look for adapters rated 1-3 lower than this adapter
        # when we find one, increment the count of permutations with this adapter
        # E.g. if adapter_jolts is 4, then we will have a matching solution includings adapter_volts = 1, resulting in {4: 1}
        # if adapter_jolts is 5, then we will have a matching solution includings adapter_volts = 4, resulting in {5: 1}
        # if adapter_jolts is 6, then we will have matching solutions 4, 5, resulting in {6: (1+1)} = {6: 2}
        # if adapter_jolts is 7, then we will have matching solutions 4, 5, 6 resulting in {7: (1+1+2)} = {7: 4}
        MAX_JOLTS = 3
        for j in range(1, MAX_JOLTS+1):
            if adapter_jolts - j in solutions.keys():
                solutions[adapter_jolts] += solutions[adapter_jolts - j]
    
    return solutions[max(seq)]


def process_differences(seq: list) -> defaultdict:
    """
    Build a dict that maps jolt differences to the number of occurences of that difference
    """
    diffs = defaultdict(int)
    for i in range(0, len(seq) - 1):
        diff = seq[i+1]-seq[i]
        diffs[diff] = diffs[diff] + 1

    return diffs


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        return [int(line) for line in f.read().splitlines()]


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

