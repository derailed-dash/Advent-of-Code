""" 
Author: Darren
Date: 03/05/2021

Solving https://adventofcode.com/2015/day/25

Enter the code at row 2947, column 3029.

Solution:
    Create a 2D list of lists.
    Then use a generate to allocate values.

"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")

    code_generator = get_next_code()
    
    target_row = 2947
    target_col = 3029
    
    coord_max = target_row + target_col   
    rows = []
    
    # initialise the 2D array.  Fill it with zeroes.
    for row in range(coord_max):
        column = []
        for col in range(coord_max):
            column.append(0)
        
        rows.append(column)
    
    # now use the generator to fill the values.
    for row in range(coord_max):
        # the sequence is... 0,0 | 1,0 0,1 | 2,0 1,1 0,2 | 3,0 2,1 1,2 0,3...
        for col in range(row+1):
            rows[row-col][col] = next(code_generator)   
        
    print(f"Value at row {target_row}, col {target_col} is: {rows[target_row-1][target_col-1]}")
    

def get_next_code():
    current_code = 20151125
    yield current_code
    
    multiplier = 252533
    dividend = 33554393
    
    while True:
        current_code = (current_code * multiplier) % dividend
        yield current_code


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
