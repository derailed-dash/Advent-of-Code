"""
Author: Darren
Date: 02/12/2021

Solving https://adventofcode.com/2021/day/2

Part 1:
    Given forward, up and down instructions like: down 5, forward 8, up 3
    - Determine final position as horizontal, depth.
    - Return the product of horizontal and depth.

Part 2:
    Now, up and down simply change inclination and change the depth change for each unit of horizontal.
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

VECTORS = {     # using complex numbers means we can track horizontal (real) and depth (imag) in one variable
    'forward': 1+0j,    # increase horizontal
    'down': 0+1j,       # increase depth (vertical)
    'up': 0-1j,         # decrease depth
}

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt", encoding="utf-8") as f:
        data = [line.split() for line in f.read().splitlines()]
    
    # Let's get tuples of instruction:str, instruction_magnitude:int
    instructions = [(instr[0], int(instr[1])) for instr in data]
    
    # Part 1
    current_location = 0+0j
    for instruction in instructions:
        current_location += instruction[1]*VECTORS[instruction[0]]
        
    logger.info("Part 1: Final location=%s", current_location)
    logger.info("Location product = %d", current_location.real*current_location.imag)
    
    # Part 2
    aim = 0 # track the inclination of the sub, in terms of depth change per unit horizontal
    current_location = 0+0j
    for instr, instr_mag in instructions:
        if instr == 'down':
            aim += instr_mag
        elif instr == 'up':
            aim -= instr_mag
        else:
            current_location += complex(instr_mag, instr_mag*aim)
    
    logger.info("Part 2: Final location=%s", current_location)
    logger.info("Location product = %d", current_location.real*current_location.imag)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
