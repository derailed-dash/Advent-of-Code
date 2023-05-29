""" 
Author: Darren
Date: 03/02/2021

Solving https://adventofcode.com/2015/day/10

Read-and-say sequences, generated iteratively. E.g. if we start with input of just 1:
    Iteration 1: 11
    Iteration 2: 21
    Iteration 3: 1211
    Iteration 4: 111221

Solution:
    Iterate through input str, char by char.
    Count the number of each repeating char.
    Store the count of previous chars, whenever we find a different char, or at the end.
    
Part 1: 40 iterations. Takes about 0.5s.
Part 2: 50 iterations. Takes about 7s. Not terrible. Not great.
"""
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

ITERATIONS = 50

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()

    print(f"Input data: {data}")

    for _ in range(ITERATIONS):
        data = look_and_say(data)

    print(f"After {ITERATIONS} iterations, length of result is {len(data)}")

def look_and_say(data: str) -> str:
    """ Perform a single look_and_say iteration

    Args:
        data (str): The input string, which is a seequence of numbers

    Returns:
        str: The resulting look-and-say string
    """
    digit_counts = []   # store each count as a (count, digit) tuple, e.g. [(3, 1), (2, 2), (1, 1)]
    digit_count = 0
    prev_digit = None
    for digit in data:
        if (prev_digit and digit != prev_digit):
            # if this digit is different to last digit, store the count of the last digit, and reset the count
            digit_counts.append([digit_count, prev_digit])
            digit_count = 0

        digit_count += 1
        prev_digit = digit

    digit_counts.append([digit_count, prev_digit])
    
    return "".join(str(count) + str(digit) for count, digit in digit_counts)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
