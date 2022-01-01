"""
Author: Darren
Date: 21/02/2021

Solving https://adventofcode.com/2016/day/3

Solution:
    Input file contains many rows, with each row containing three numbers.
    Part 1: 
        Read each row, take the three numbers, and determine how many are 'valid 'triangles.
        Easy to implement using filter.
    
    Part 2:
        Read down, then across, in groups of three.
        The challenge here is first flattening the input data.
        This solution zips all the rows, in order to transpose the rows and cols.
        Then we flatten with itertools.chain().
"""
import logging
import os
from itertools import chain
from util.timer import Timer

# pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

NUMS_PER_ROW = 3

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    # Part 1    
    # Each row of data has three numbers.  These represent the lengths of the triangle.
    triangles = []
    for line in data:
        lengths = [int(x) for x in line.split()]
        triangles.append(lengths)
    
    # apply rules to determine which sets of three numbers are valid triangles    
    valid_triangles = list(filter(is_valid_triangle, triangles))
    
    logging.info("Part 1")
    logging.info(f"We have a total of {len(triangles)} triangles, of which {len(valid_triangles)} are valid.")
    
    # Part 2
    # Here, we need to read down the columns, 3 numbers at a time. Rather than reading rows.
    # First, create a list for each row, and add to all_numbers...
    all_numbers = []
    for line in data:
        # get a list of lists
        nums = [int(x) for x in line.split()]
        all_numbers.append(nums)
    
    # now unpack all these lists into zip, in order to transpose our cols to rows
    transposed_nums = list(zip(*all_numbers))
    
    # now flatten our new rows into one single list.  Put back into all_numbers.
    # Use itertools.chain() to concatenate all items from an arbitrary number of lists 
    all_numbers = list(chain(*transposed_nums))
    
    triangles = []
    for i, _ in enumerate(all_numbers):
        # Read our single list of numbers, 3 at a time
        if i % NUMS_PER_ROW == 0:
            triangles.append([all_numbers[i], all_numbers[i+1], all_numbers[i+2]])

    valid_triangles = list(filter(is_valid_triangle, triangles))
    logging.info("Part 2")
    logging.info(f"We have a total of {len(triangles)} triangles, of which {len(valid_triangles)} are valid.")


def is_valid_triangle(triangle: list) -> bool:
    """ Valid triangles have one length greater than the sum of the two shorter lengths.

    Args:
        triangle (list): side lengths of this triangle

    Returns:
        [bool]: Whether valid, according to the rules
    """
    triangle = sorted(triangle)
    return triangle[0] + triangle[1] > triangle[2]
    
if __name__ == "__main__":
    t1 = Timer(True)
    main()
    print(f"Execution time: {t1():0.4f} seconds")
