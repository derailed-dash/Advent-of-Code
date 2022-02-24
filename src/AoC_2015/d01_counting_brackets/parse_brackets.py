""" 
Author: Darren
Date: 11/01/2021

Solving https://adventofcode.com/2015/day/1

( = up a floor; ) = down a floor

Part 2: after how many instructions are we in the basement (-1)
"""
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"

UP = "("
DOWN = ")"

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()

    up_count = data.count(UP)
    down_count = data.count(DOWN)

    print(f"Final floor: {up_count-down_count}")

    floor = 0
    for i, char in enumerate(data, 1):
        if char == UP:
            floor += 1
        else:
            floor -= 1

        if floor == -1:
            print(f"Basement reached at instruction {i}")
            break

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
