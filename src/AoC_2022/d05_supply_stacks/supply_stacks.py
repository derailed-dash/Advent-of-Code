"""
Author: Darren
Date: 05/12/2022

Solving https://adventofcode.com/2022/day/5

We have stacks of crates. First block of input data shows stack configuration, e.g.
            [D]    
        [N] [C]    
        [Z] [M] [P]
         1   2   3

We have instructions for rearranging crates.  E.g. 
move 3 from 1 to 3

Part 1:

Our CrateMover 9000 moves one crate at the time, from the end of one stack to the end of another.
What crates will be at the top of each stack, after following the instructions?

- Solution:
  - Split the instructions into two blocks: crate config, and instructions.
    - For config, first reverse the order, count how many stacks, and then parse with regex.
  - Process each instruction, popping off the end of the source stack as many times as required,
    and appending to the target stack.
  
Part 2:

Our CrateMover 9001 moves multiple crates at a time, 
and puts them in the new stack in the same order that they were lifted.
What crates will be at the top of each stack, after following the instructions?

- Solution:
  - The same, except now we can slice n items off the end of the source stack, 
    rather than popping one at a time.
  - Because we're now adding a list (slice) to the target stack, we need to use extend, not append.
  
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
   
    stacks = process_stack_data(stack_data.splitlines())
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

def process_stack_data(stack_data: list[str]) -> list[list]:
    """ Data looks like... 
            [D]    
        [N] [C]    
        [Z] [M] [P]
         1   2   3
         
    Return: [['Z', 'N'], ['M', 'C', 'D'], ['P']]
    """
    stack_width = 4
    p = re.compile(r"[A-Z]")
    # reverse it, so we've got the stack numbers at the top
    stack_data = stack_data[::-1]
    num_stacks = len(stack_data[0].split())

    stacks = [[] for _ in range(num_stacks)] # empty list for each stack
        
    # proces the stacks
    for stack_row in stack_data[1:]:     # starting at the row of crates
        for stack_num in range(num_stacks):
            match = p.search(stack_row[stack_num * stack_width:(stack_num+1) * stack_width])
            if match:
                stacks[stack_num].append(match.group())
        
    return stacks

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
