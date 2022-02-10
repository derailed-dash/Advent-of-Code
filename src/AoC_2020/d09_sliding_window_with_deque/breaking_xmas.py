"""
Author: Darren
Date: 10/12/2020

Solving: https://adventofcode.com/2020/day/9

Valid numbers must be the sum of two previous numbers in a sliding window.
User itertools.combinations() to identify any two numbers that add up to latest number.

Part 1 is to find the first invalid number.
Part 2 is to find a contiguous set of numbers that add up to the invalid number.
"""
import os
import time
from collections import deque
from itertools import combinations

SEQUENCE_INPUT_FILE = "input/sequence.txt"
SAMPLE_SEQUENCE_INPUT_FILE = "input/test_sequence.txt"
PREAMBLE_SIZE = 25

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, SEQUENCE_INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_SEQUENCE_INPUT_FILE)
    print("Input file is: " + input_file)

    sequence = read_input(input_file)

    invalid_num = process_seq(sequence)
    print(f"{invalid_num} is invalid.")
    
    limits = find_contiguous_block(invalid_num, sequence)
    if len(limits) > 0:
        contiguous_block = sequence[limits[0]:limits[1]+1]
        print(contiguous_block)
        smallest = min(contiguous_block)
        largest = max(contiguous_block)
        print(f"Sum of {smallest} and {largest} is {smallest+largest}")


def find_contiguous_block(num, seq):
    limits = []

    # define function for inner loop.  Use a function so we can return from it.
    # This allows us to 'continue' outer loop, rather than inner loop.
    def inner(i, the_sum):
        for j in range(i+1, len(seq)):
            the_sum += seq[j]
            if the_sum > num:
                # we've gone bust, so try next outer
                return False
            
            if the_sum == num:
                # store start and end indexes in seq
                limits.append(i)
                limits.append(j)
                # success
                return True

    # try first number in contiguous block
    for i in range(0, len(seq)):
        the_sum = seq[i]
        if inner(i, the_sum):
            # we've found our contiguous numbers.  We can finish now.
            break
    
    return limits


def process_seq(sequence):

    # create a FILO queue to hold our sliding window of numbers
    q = deque()
    seq_ptr = 0

    # buld the pre-amble, if we've got enough items
    if (len(sequence) >= PREAMBLE_SIZE):
        for i in range(PREAMBLE_SIZE):
            q.append(sequence[i])
            seq_ptr += 1

    # go until we get to the end
    while seq_ptr < len(sequence):
        num = sequence[seq_ptr]
        # print(f'Testing {sequence[seq_ptr]} in queue: {q}')
        if check_sum(num, q):
            # this number is valid, so pop the last and add the next
            q.popleft()
            q.append(num)
        else:
            break

        seq_ptr += 1
    
    return num


def check_sum(num, q):
    for num_1, num_2 in combinations(q, 2):
        if num == num_1 + num_2:
            return True
    
    return False


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        return [int(line) for line in f.read().splitlines()]


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

