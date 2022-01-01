""" 
Author: Darren
Date: 03/02/2021

Solving https://adventofcode.com/2015/day/10

Read-and-say sequences, generated iteratively. E.g.
    1 = 11
    11 = 21
    21 = 1211

Solution:
    Iterate through input str, char by char.
    Count the number of each repeating char.
    Store the count whenever we find a different char, or at the end.

"""
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()

    print(data)
    iterations = 40

    for _ in range(iterations):
        data = look_and_say(data)

    print(f"After {iterations} iterations, length of result is {len(data)}")


def look_and_say(data):
    digit_counts = []
    digit_count = 0
    last_digit = None
    for digit in data:
        if (last_digit and digit != last_digit):
            # if this digit is different to last digit, store the count of the last digit
            digit_counts.append([last_digit, digit_count])
            digit_count = 0

        digit_count += 1 
        last_digit = digit

    digit_counts.append([last_digit, digit_count])

    new_str = ""
    for digit_count in digit_counts:
        digit, count = digit_count
        new_str += str(count) + digit
    
    return new_str


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
