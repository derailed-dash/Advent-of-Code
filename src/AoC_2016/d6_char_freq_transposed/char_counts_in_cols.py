"""
Author: Darren
Date: 30/05/2021

Solving https://adventofcode.com/2016/day/6

Part 1:
    Need to get most frequent char in each column, given many rows of data.
    Transpose columns to rows.
    Find the Counter d:v that has the max value, keyed using v from the k,v tuple.
    
Part 2:
    As part 1, but using min instead of max.

"""
import logging
import os
import time
from collections import Counter

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
        
    # First, we need to transpose columns to rows
    transposed = list(zip(*data))
    
    most_common_chars = [] # Part 1
    least_common_chars = [] # Part 2
        
    for line in transposed:
        char_counts = Counter(line)
        # Get the least / most frequent char
        most_common_chars.append(max(char_counts.items(), key=lambda x: x[1])[0])
        least_common_chars.append(min(char_counts.items(), key=lambda x: x[1])[0])
    
    # Convert to str representation
    least_common = "".join(str(char) for char in least_common_chars)
    most_common = "".join(str(char) for char in most_common_chars)
    
    logging.info(f"Part 1 message: {most_common}")
    logging.info(f"Part 2 message: {least_common}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
