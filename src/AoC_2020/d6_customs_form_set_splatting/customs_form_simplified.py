""" customs_form.py
Author: Darren
Date: 07/12/2020

Solving: https://adventofcode.com/2020/day/6

Solution 2 of 2:
    Each input group is stored as a list.  Thus, a list of lists.
    Use set union, splatted with each group list item, to get unique responses.
    Use set intersection, splatted with each group list item, to get common responses.
"""

import sys
import os
import time
from pprint import pprint as pp

CUSTOMS_FORM_INPUT_FILE = "input/customs_answers.txt"


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, CUSTOMS_FORM_INPUT_FILE)
    print("Input file is: " + input_file)
    
    group_responses = read_input(input_file)

    # unique responses per group_response
    unique_responses = []
    all_yes_responses = []
    for group_response in group_responses:
        # identify all the unique responses from the whole group
        unique_responses.append(set.union(*[set(entry) for entry in group_response]))
        
        # identify the responses that are common to all members of the group
        all_yes_responses.append(set.intersection(*[set(entry) for entry in group_response])) 
    
    count_unique_responses = sum(len(unique_response) for unique_response in unique_responses)
    print(f"For any yes responses in each group, the sum is {count_unique_responses}.")

    count_all_yes_responses = sum(len(all_yes) for all_yes in all_yes_responses)
    print(f"For all yes responses in each group, the sum is {count_all_yes_responses}.") 


def read_input(a_file):
    # Each row are responses from an individual.
    # A group of individuals is separated by a blank line.

    with open(a_file, mode="rt") as f:
        group_responses = [group_entry.split() for group_entry in f.read().split("\n\n")]

    # return a list of lists
    # e.g. ['icb', 'xqhf']
    return group_responses


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
