""" Add_to_2020.py
Author: Darren
Date: 05/12/2020

Solving https://adventofcode.com/2020/day/1

Solution 1 of 2:

Process a list of numbers, and determine which two numbers add up to 2020.
Process a list of numbers and determine which three numbers add up to 2020.
"""

import sys
import os
import time


def read_input(a_file):
    with open(a_file, mode="rt") as f:

        # list comprehension to convert each line to an int
        entries = [int(x) for x in f.read().splitlines()]

    return entries


def total_of_two(entries, target):
    iterations = 0
    for i, num1 in enumerate(entries):
        for num2 in entries[i+1:]:
            iterations += 1
            the_sum = num1 + num2
            if (the_sum == target):
                print(f"The sum of {num1} and {num2} is: " + str(target))
                print(f"And the product is: " + str(num1 * num2))
                print(f"{iterations} iterations required.")


def total_of_three(entries, target):
    iterations = 0
    for i, num1 in enumerate(entries):
        for j, num2 in enumerate(entries[i+1:]):
            iterations += 1
            sum_so_far = num1 + num2
            if (sum_so_far >=target):
                # we've already exceeded target with just two numbers
                continue
            
            for num3 in entries[j+1:]:
                iterations += 1
                the_sum = sum_so_far + num3
                if (the_sum == target):
                    print(f"The sum of {num1} and {num2} and {num3} is: " + str(the_sum))
                    print(f"And the product is: " + str(num1*num2*num3))
                    print(f"{iterations} iterations required.")
                    return


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 

    # path of input file
    input_file = os.path.join(script_dir, "input/expenses.txt")
    print("Input file is: " + input_file)
    entries = read_input(input_file)
    print("File read.")

    target = 2020

    # print(entries)
    print("Looking for two numbers that total " + str(target))
    total_of_two(entries, target)

    print("Looking for three numbers that total " + str(target))
    total_of_three(entries, target)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

