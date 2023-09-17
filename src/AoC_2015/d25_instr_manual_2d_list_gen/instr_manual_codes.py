""" 
Author: Darren
Date: 03/05/2021

Solving https://adventofcode.com/2015/day/25

- We're given an infinite sequence, where each code is calculated based on the previous code.
- The sequence is populated into a 2D grid diagonally, from bottom left to top right.
  - Starting at location 1,1.
  - Then 1,0 0,1
  - Then 2,0 1,1 0,2
  - Then 3,0 2,1 1,2 0,3, and so on.

Enter the code at row 2947, column 3029.

Solution:
  - Create a 2D list of lists, and fill with zeroes.
    - The row upper bound is row-target + col-target - 1.
    - The col upper bound will be the same value, to complete that diagonal.
  - Then use a generate to allocate values.
"""
import logging
import time
import common.aoc_commons as td

locations = td.get_locations(__file__)
logger = td.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)

TARGET_ROW = 2947
TARGET_COL = 3029

def main():
    code_generator = get_next_code()
        
    coord_max = TARGET_ROW + TARGET_COL - 1 
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
        
    logger.info(f"Value at row {TARGET_ROW}, col {TARGET_COL} is: {rows[TARGET_ROW-1][TARGET_COL-1]}")

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
    logger.info("Execution time: %.3f seconds", t2 - t1)
    logger.info("Execution time: %.3f seconds", t2 - t1)
