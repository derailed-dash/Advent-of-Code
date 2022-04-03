""" 
Author: Darren
Date: 14/01/2021

Solving https://adventofcode.com/2015/day/6

Configure 1m lights in a 1000x1000 grid, by following a set of instructions.
Lights begin turned off.
Coords are 0-indexed

Solution 2 of 3:
    Uses a list of lists to represent a 2D array.  Easy to index.
    Each element initialised to False.
    This is quite slow.  Twice as fast as dict of dicts.  Takes about 5s for both parts.

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
from pathlib import Path
import time
import re

SCRIPT_DIR = Path(__file__).parent 
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    width = height = 1000

    # Part 1
    # Create a list of lists
    light_rows = [[False for light in range(width)] for row in range(height)]
    process_instructions(data, light_rows)
    lights = [light_rows[y][x] for x in range(width) for y in range(height)]
    assert len(lights) == width*height
    print(f"Part 1, lights on: {sum(lights)}")

    # Part 2
    # Re-initialise our grid
    light_rows = [[0 for light in range(width)] for row in range(height)]
    process_variable_brightness_instructions(data, light_rows)
    lights = [light_rows[y][x] for x in range(width) for y in range(height)]
    print(f"Part 2, brightness: {sum(lights)}")

def process_variable_brightness_instructions(data, lights):
    p = re.compile(r"(\d+),(\d+) through (\d+),(\d+)")

    for line in data:
        match = p.search(line)
        assert match, "All instruction lines are expected to match"
        tl_x, tl_y, br_x, br_y = map(int, match.groups())

        for y in range(tl_y, br_y + 1):
            for x in range(tl_x, br_x + 1):
                if "toggle" in line:
                    lights[y][x] += 2
                elif "on" in line:
                    lights[y][x] += 1
                elif "off" in line:
                    if lights[y][x] > 0:
                        lights[y][x] -= 1

def process_instructions(data, lights):
    p = re.compile(r"(\d+),(\d+) through (\d+),(\d+)")

    for line in data:
        match = p.search(line)
        assert match, "All instruction lines are expected to match"
        tl_x, tl_y, br_x, br_y = map(int, match.groups())

        for y in range(tl_y, br_y + 1):
            for x in range(tl_x, br_x + 1):
                if "toggle" in line:
                    lights[y][x] = not lights[y][x]
                elif "on" in line:
                    lights[y][x] = True
                elif "off" in line:
                    lights[y][x] = False

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
