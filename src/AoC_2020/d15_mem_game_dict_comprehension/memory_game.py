"""
Author: Darren
Date: 15/12/2020

Solving: https://adventofcode.com/2020/day/15

Read from list of starting numbers.
If that was the first time the number has been spoken, the current player says 0.
Otherwise, announce how many turns apart the number is from when it was previously spoken.

For part 1, it is possible to simply store all the previous numbers in a list, 
and check the list with each iteration.  However, this does not scale for Part 2,
when there are millions of iterations.  
Instead, store the last position of each occurence of a number.
The dict ends up being ~1/10 the size of the data.
"""
import os
import time
from pprint import pprint as pp

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/starting_numbers.txt"
SAMPLE_INPUT_FILE = "input/sample_starting_numbers.txt"


def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    game_seed = convert_input_to_list(read_input(input_file))
    pp(game_seed)

    for i, iterations in enumerate([2020, 30000000]):
        last_val = play_game(iterations, game_seed)
        print(f"Part {i+1}, value of iteration {iterations} = {last_val}")
    

def play_game(iterations, seed):
    # We need a ditionary to store last position of any given value.
    # Dict comprehension to seed a dictionary that 
    # stores the last position of each number in the sequence
    # e.g. {1: 0, 2: 1, 16: 2, 19: 3 ...}
    last_val_positions = {val: position for position, val in enumerate(seed)}
    last_val = seed[-1]

    for i in range(len(seed), iterations-1):
        # Add seq diff between this number and the last time we saw this number
        if (last_val in last_val_positions.keys()):
            previous_index = last_val_positions[last_val]
            new_val = i - previous_index
           
        # otherwise, we've not seen this number before, add 0 to seq
        else:
            new_val = 0         

        last_val_positions[last_val] = i
        last_val = new_val        
        
    print(f"Size of dict is {len(last_val_positions)}")
    return last_val


def read_input(a_file):
    # input is single line of comma-separated numbers
    with open(a_file, mode="rt") as f:
        data = f.read()
        
    return data


def convert_input_to_list(input_data):
    # convert comma-separated numbers to a list of ints
    return [int(x) for x in input_data.split(",")]


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

