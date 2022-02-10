""" 
boarding_passes.py
Author: Darren
Date: 07/12/2020

Solving https://adventofcode.com/2020/day/5

Process boarding passes, which can contain seat codes in format RRRRRRRCCC.
Seat code is binary, where R (row) can be F or B and C (column) can be L or R.
"""
import sys
import os
import time
from pprint import pprint as pp

BOARDING_PASS_INPUT_FILE = "input/boarding_passes.txt"

class BoardingPass:

    def __init__(self, seat_code: str):
        """
        Creates a boarding pass for given seat code.
        E.g. seat code "BBFFFFBRLR"
        """
        self._seat_code = seat_code

    def get_seat_code(self):
        return self._seat_code
    
    def get_seat_row(self):
        """
        7-bit row number from 0-127.
        F = 0 and B = 1.
        """
        seat_row = self.get_seat_code()[:7].replace("F", "0").replace("B", "1")
        return int(seat_row, 2)

    def get_seat_col(self):
        """
        3-bit col number from 0-7
        L = 0 and R = 1
        """
        seat_col = self.get_seat_code()[7:].replace("L", "0").replace("R", "1")
        return int(seat_col, 2)

    def get_seat_id(self):
        """
        Seat ID is given by 8*row + col.
        """
        return (self.get_seat_row() * 8) + self.get_seat_col()

    def __str__(self):
        return self.get_seat_code() + " " + str(self.get_seat_id())


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, BOARDING_PASS_INPUT_FILE)
    print("Input file is: " + input_file)
    
    # read in the seat codes
    pass_codes = read_input(input_file)
    
    # get all the allocated seat IDs
    seat_ids = set()
    for pass_code in pass_codes:
        p = BoardingPass(pass_code)
        seat_ids.add(p.get_seat_id())

    min_seat_id = min(seat_ids)
    max_seat_id = max(seat_ids)
    print("Highest seat code from input: " + str(max_seat_id))
    
    possible_seats = set(range(min_seat_id, max_seat_id))
    missing_seats = possible_seats.difference(seat_ids)

    # Our seat is in a non-contiguous block of missing seats...
    print(f"Our seat: {missing_seats}")


def find_noncontiguous_number(numbers): 
    a_list = list(numbers)
    non_contiguous_numbers = set()

    for i in range(1, len(numbers)-1): 
        if ((a_list[i] - a_list[i-1] > 1) and (a_list[i+1] - a_list[i] > 1)): 
            non_contiguous_numbers.add(a_list[i])
        
    return non_contiguous_numbers


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        passes = f.read().splitlines()
        
    return passes


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
