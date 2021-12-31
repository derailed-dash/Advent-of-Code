"""
Author: Darren
Date: 04/06/2021

Solving https://adventofcode.com/2016/day/8

Overview
    A 50w x 6h grid of pixels, which are all turned off at the beginning.
    Follow instructions to turn on pixels and move pixels.

Part 1:
    Create a zeros np array.
    Apply the instructions.
    Then use ndarray.sum() to sum the lit pixels.

Part 2:
    We can just print the grid as it is, but it's not very readable.
    So, covert to a list.
    For each line in the line, convert 1 to "*" and convert 0 to " ".
    Then concatenate and print the result.
"""
from __future__ import absolute_import
import logging
import os
import time
import re
import numpy as np

# pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

rect_pattern = re.compile(r"rect (\d+)x(\d+)")
shift_pattern = re.compile(r"rotate [a-z]* (.)=(\d+) by (\d+)")

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    # if we want to print the numpy array, we'll need wider rows...
    np.set_printoptions(linewidth=150)
    
    # cols = 7
    # rows = 3
    cols = 50
    rows = 6

    # Part 1
    grid = np.zeros((rows, cols), dtype=np.int8)
    process_instructions(data, grid)
    print("Part 1")
    print("------")
    print(f"Pixels lit: {grid.sum()}")
    
    # Part 2
    print("\nPart 2")
    print("------")
    grid_list = grid.tolist()
    rendered = "\n".join(["".join(["*" if char == 1 else " " for char in line]) 
                          for line in grid_list])
        
    print(rendered)


def process_instructions(data, grid):
    for line in data:
        if "rect" in line:
            # Create a rect of lit pixels, starting top left
            x_size, y_size = rect_pattern.search(line).groups()
            x_size, y_size = map(int, [x_size, y_size])
            
            # Set all the pixels in this rect to 1
            grid[0:y_size, 0:x_size] = 1
        else:
            axis, val, shift = shift_pattern.search(line).groups()
            val, shift = map(int, [val, shift])
            
            # Extract the specified row or column
            # Then shift the row/column the specified number
            # Then replace the np array row/column with the shifted values
            if axis == 'x':
                seq_data = list(grid[:, val])
                shifted = seq_data[-shift:] + seq_data[:-shift]
                grid[:, val] = shifted
            else:
                seq_data = list(grid[val, :])
                shifted = seq_data[-shift:] + seq_data[:-shift]
                grid[val, :] = shifted


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
