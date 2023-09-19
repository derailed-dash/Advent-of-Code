"""
Author: Darren
Date: 01/12/2022

Solving https://adventofcode.com/2022/day/1

Our input data contains lines of numbers, with occasional empty lines.
- Each line is a number, representing the calories for an elf meal.
- Each contiguous block of lines represents the meals for a given elf.
- The empty lines separate one elf from the next.

Part 1:

How many calories in total, for the elf with the most calories?

Solution:
- Read the data, and split by empty lines, to return a list of str.
- Each element is a str containing all the numbers for a given elf.
- Split these numbers, convert them to int with map(), and then sum them.

Part 2:

How many calories in total for the top three elves?

Solution:
- Sort the list.
- Add up the last three.
"""
import logging
from pathlib import Path
import time
import aoc_common.aoc_commons as ac

SCRIPT_NAME = Path(__file__).stem
SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

logger = logging.getLogger(SCRIPT_NAME)
logger.setLevel(logging.DEBUG)
logger.addHandler(ac.stream_handler)

def main():
    with open(INPUT_FILE, mode="rt") as f:
        elf_meals = f.read().split("\n\n") # split on empty lines
    
    elf_calories = [] # store total calories for each elf
    for elf in elf_meals:
        calories = sum(map(int, elf.splitlines()))
        elf_calories.append(calories)
        
    logger.info("Part 1: %d", max(elf_calories))
    
    elf_calories = sorted(elf_calories)
    logger.info("Part 2: %d", sum(elf_calories[-3:]))

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
