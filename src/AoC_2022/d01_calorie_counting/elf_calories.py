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
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        elf_meals = f.read().split("\n\n") # split on empty lines
    
    elf_calories = [] # store total calories for each elf
    for elf in elf_meals:
        calories = sum(map(int, elf.splitlines()))
        elf_calories.append(calories)
        
    print(f"Part 1: {max(elf_calories)}")
    
    elf_calories = sorted(elf_calories)
    print(f"Part 2: {sum(elf_calories[-3:])}")
    

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
