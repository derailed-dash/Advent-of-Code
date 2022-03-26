""" 
Author: Darren
Date: 14/01/2021

Solving https://adventofcode.com/2015/day/6

Configure 1m lights in a 1000x1000 grid, by following a set of instructions.
Lights begin turned off.
Coords are 0-indexed

Solution 1 of 3:
    Uses a defaultdict to create a dict of dicts, to represent a 2D array.
    Each element initialised to False.
    This is quite slow.  Takes about 7s for both parts.

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
import os
import time
import re
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    dim_length = 1000

    # Part 1
    lights = defaultdict(dict)
    # create a dict for every lights[i]
    for i in range(dim_length):
        for j in range(dim_length):
            lights[i][j] = False

    process_instructions(data, lights)

    count_lights_on = sum(1 if lights[i][j] else 0 for j in range(dim_length) for i in range(dim_length))
    print(f"Part 1, lights on: {count_lights_on}")

    # Part 2
    lights = defaultdict(dict)
    # create a dict for every lights[i]
    for i in range(dim_length):
        for j in range(dim_length):
            lights[i][j] = 0

    process_variable_brightness_instructions(data, lights)
    total_brightness = sum(lights[i][j] for j in range(dim_length) for i in range(dim_length))
    print(f"Part 2, brightness: {total_brightness}")

def process_variable_brightness_instructions(data, lights):
    p = re.compile(r"(\D+) (\d+),(\d+) through (\d+),(\d+)")

    for line in data:
        _, tl_x, tl_y, br_x, br_y = p.search(line).groups()
        tl_x, tl_y, br_x, br_y = map(int, (tl_x, tl_y, br_x, br_y))

        for i in range(tl_x, br_x + 1):
            for j in range(tl_y, br_y + 1):
                if "toggle" in line:
                    lights[i][j] += 2
                elif "on" in line:
                    lights[i][j] += 1
                elif "off" in line:
                    if lights[i][j] > 0:
                        lights[i][j] -= 1


def process_instructions(data, lights):
    p = re.compile(r"(\D+) (\d+),(\d+) through (\d+),(\d+)")

    for line in data:
        _, tl_x, tl_y, br_x, br_y = p.search(line).groups()
        tl_x, tl_y, br_x, br_y = map(int, (tl_x, tl_y, br_x, br_y))

        for i in range(tl_x, br_x + 1):
            for j in range(tl_y, br_y + 1):
                if "toggle" in line:
                    lights[i][j] = not lights[i][j]
                elif "on" in line:
                    lights[i][j] = True
                elif "off" in line:
                    lights[i][j] = False


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")