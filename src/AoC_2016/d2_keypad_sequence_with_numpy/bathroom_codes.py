"""
Author: Darren
Date: 01/02/2021

Solving https://adventofcode.com/2016/day/2

Solution:
    Use numpy array to represent the buttons in the keypad.
"""
import logging
import os
import time
import numpy as np

# pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

class NavigationConstants:
    """ Navigation Constants """
    U = 'U'
    D = 'D'
    L = 'L'
    R = 'R'

    VECTORS = {
        U: [0, -1],
        D: [0, 1],
        L: [-1, 0],
        R: [1, 0]
    }

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    # Part 1
    # initialise the array in the form of a numeric keypad, with digits 1-9
    keypad = np.arange(1, 10).reshape(3, 3)
    
    # set starting position to be digit 5
    row = col = 1
    keypresses = get_combo(keypad, data, row, col)
    logging.info("".join(keypresses))
    
    # Part 2
    # initialise the array with the weird keypad
    # Spaces represent invalid locations
    keypad = np.array([[" ", " ", "1", " ", " "],
                       [" ", "2", "3", "4", " "],
                       ["5", "6", "7", "8", "9"],
                       [" ", "A", "B", "C", " "],
                       [" ", " ", "D", " ", " "]])
    row = 2
    col = 0
    keypresses = get_combo(keypad, data, row, col)
    logging.info("".join(keypresses))


def get_combo(keypad: np.ndarray, instructions: list, row: int, col: int) -> list:
    """ Process a list of keypad navigation instructions.
    At the end of each line, store the current button position.

    Args:
        keypad (np.ndarray): The 2D array that represents the keypad
        instructions (list): List of navigation instructions, in the format U, D, L, R
        row (int): The starting row.
        col (int): The starting col.

    Returns:
        list: The sequence of keypresses.
    """
    rows, cols = keypad.shape
    logging.debug(f"\n{keypad}")
    logging.debug(f"Starting button: {keypad[row, col]}")
    keypresses = []
    
    for line in instructions:
        for char in line:
            col += NavigationConstants.VECTORS[char][0]
            row += NavigationConstants.VECTORS[char][1]
            
            # if we've gone off the edge, then set the col and row to edge
            if col < 0: 
                col = 0
            if col > cols-1: 
                col = cols-1
            if row < 0: 
                row  = 0
            if row > rows-1: 
                row = rows-1
            
            # if current array position is ' ', then reverse (ignore) last instruction
            if str(keypad[row][col]) == ' ':
                col -= NavigationConstants.VECTORS[char][0]
                row -= NavigationConstants.VECTORS[char][1]
            
        keypresses.append(str(keypad[row][col]))
        
    return keypresses
    

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
