""" 
Author: Darren
Date: 14/01/2021

Solving https://adventofcode.com/2015/day/6

Configure 1m lights in a 1000x1000 grid, by following a set of instructions.
Lights begin turned off.
Coords are 0-indexed

Solution 3 of 3:
    Use numpy 2D array.  
    This is about 35x faster than using dicts!


Part 1:
    Instructions require lights to be toggled, turned on, or off.
    Calculate total lights turned on.

Part 2:
    Lights have variable brightness.  Instructions have new meanings:
        Turn on = increase by 1
        Turn off = decrease by 1
        Toggle = increase by 2
    Calculate total brightness.

"""
from __future__ import absolute_import
import os
import time
import re
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    dim_size = 1000

    # Part 1
    lights = np.zeros((dim_size,dim_size), dtype=np.int8)
    process_instructions(data, lights)
    print(f"Part 1, lights on: {lights.sum()}")

    # Part 2
    lights = np.zeros((dim_size,dim_size), dtype=np.int8)
    process_variable_brightness_instructions(data, lights)
    print(f"Part 2, brightness: {lights.sum()}")


def process_variable_brightness_instructions(data, lights):
    p = re.compile(r"(\D+) (\d+),(\d+) through (\d+),(\d+)")

    for line in data:
        _, tl_x, tl_y, br_x, br_y = p.search(line).groups()
        tl_x, tl_y, br_x, br_y = map(int, (tl_x, tl_y, br_x, br_y))

        if "toggle" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] += 2
        elif "on" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] += 1
        elif "off" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] -= 1

        lights[lights < 0] = 0


def process_instructions(data, lights):
    p = re.compile(r"(\D+) (\d+),(\d+) through (\d+),(\d+)")

    for line in data:
        _, tl_x, tl_y, br_x, br_y = p.search(line).groups()
        tl_x, tl_y, br_x, br_y = map(int, (tl_x, tl_y, br_x, br_y))

        if "toggle" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] ^= 1
        elif "on" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] = 1
        elif "off" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] = 0


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")