""" 
Author: Darren
Date: 01/02/2021

Solving https://adventofcode.com/2015/day/12

Extract all numbers from JSON input.
The json data contains lists, dicts, numbers and strings.
These may be nested.

Solution:
    Recursively process the json.  
    Identify whether the current element is a dict, a list, a str or an int.
    If an int, just add it to the running total.
    If a str, ignore.
    If a dict, recursively call this method against all values for this dict.
    If a list, recurisvely call for all elements in this list.

Part 1:
    Sum of all integers stored anywhere in the json.

Part 2:
    Ignore any object (and all of its children) which has any property with the value "red".
    Ignore objects (dicts), but not lists.
    E.g. [1,{"c":"red","b":2},3] has the sum of 4, because the middle object (dict) is ignored.
    We do this by adding a second parameter to the process_json method, which takes a value to ignore.
    If this value is specified, and if its found in any values of the current dict, 
    then return 0 and do not recurse this dict.
"""
import os
import time
import json

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.json"
SAMPLE_INPUT_FILE = "input/sample_input.json"

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        j = json.load(f)

    result = process_json(j)
    print(f"Total of all numbers: {result}")
    
    result = process_json(j, "red")
    print(f"Total of all numbers: {result}")


def process_json(input, ignore=None):
    num_total = 0

    if type(input) is dict:
        if ignore is not None:
            if ignore in input.values():
                return 0

        for key in input:
            num_total += process_json(input[key], ignore)
    elif type(input) is list:
        for element in input:
            num_total += process_json(element, ignore) 
    elif type(input) is int:
        num_total += input

    return num_total


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
