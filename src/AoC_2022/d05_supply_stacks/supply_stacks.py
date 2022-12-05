"""
Author: Darren
Date: 01/12/2022

Solving https://adventofcode.com/2022/day/1

Part 1:

Part 2:

"""
from copy import deepcopy
from pathlib import Path
import re
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        stack_data, instructions = f.read().split("\n\n")
    
    # Let's just write out the stacks for now, to save time parsing...
    stacks = [
        ["G", "T", "R", "W"],
        ["G", "C", "H", "P", "M", "S", "V", "W"],
        ["C", "L", "T", "S", "G", "M"],
        ["J", "H", "D", "M", "W", "R", "F"],
        ["P", "Q", "L", "H", "S", "W", "F", "J"],
        ["P", "J", "D", "N", "F", "M", "S"],
        ["Z", "B", "D", "F", "G", "C", "S", "J"],
        ["R", "T", "B"],
        ["H", "N", "W", "L", "C"]
    ]

    movements = read_instructions(instructions.splitlines())
    
    # Part 1
    # make a copy, since we need to reset the stack for Part 2
    part1_stack = deepcopy(stacks)
    for how_many, from_where, to_where in movements:
        # pop items off the end, for how_many times
        for _ in range(how_many):
            part1_stack[to_where].append(part1_stack[from_where].pop())
    
    stack_message = "".join(a_stack[-1] for a_stack in part1_stack)
    print(f"Part 1: {stack_message}")
    
    # Part 2
    for how_many, from_where, to_where in movements:
        # slice items off the end and move to the target stack
        stacks[to_where].extend(stacks[from_where][-how_many:])
        stacks[from_where][-how_many:] = [] # and then delete the items
        
    stack_message = "".join(a_stack[-1] for a_stack in stacks)
    print(f"Part 2: {stack_message}")        

def read_instructions(instructions: list[str]) -> list[tuple[int, int, int]]:
    """ Instructions look like: 'move 3 from 8 to 6' """
    p = re.compile(r"move (\d+) from (\d+) to (\d+)")
    movements = []
    for line in instructions:
        how_many, from_where, to_where = list(map(int, p.findall(line)[0]))
        from_where -= 1 # we need it to be 0-indexed
        to_where -= 1 # we need it to be 0-indexed
        movements.append((how_many, from_where, to_where))

    return movements

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
