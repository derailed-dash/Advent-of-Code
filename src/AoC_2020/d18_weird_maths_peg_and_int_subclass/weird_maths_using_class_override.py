"""
Author: Darren
Date: 18/12/2020

Solving: https://adventofcode.com/2020/day/18

Solution 2 of 3:
Override the int class, so - now does multiplication, and * now does addition.

Part 1
------
Rather than evaluating multiplication before addition, 
the operators have the same precedence, and are evaluated left-to-right 
regardless of the order in which they appear.

Part 2
------
Addition is evaluated before multiplication.
"""
import os
import re
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/math_puzzle.txt"
SAMPLE_INPUT_FILE = "input/test_math_puzzle.txt"

# extend the int class
class I(int):
    # override addition (+)
    def __add__(self, other): 
        return I(self.real + other.real)
    
    # override subtraction (-)
    # make subtraction implement multiplication
    def __sub__(self, other): 
        return I(self.real * other.real)
    
    # make * perform addition operator
    __mul__ = __add__


def main():
    # input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input = read_input(input_file)

    # replace every digit n with I(n)
    # replace every * with -; but - will perform multiplication.
    # But because - and + have same precedence, they simply get evaluated left to right
    lines = re.sub(r"(\d+)", r"I(\1)", input).replace("*", "-").splitlines()

    # evalute the input as though code
    print(sum(eval(line) for line in lines))

    # by replacing all + with *, this has the effect of * taking precedence
    # but remember that * will actually perform addition
    print(sum(eval(line.replace("+", "*")) for line in lines))


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read()
        
    return data


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
     