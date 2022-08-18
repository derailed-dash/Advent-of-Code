"""
Author: Darren
Date: 28/01/2021

Solving https://adventofcode.com/2015/day/8

Part 1:
    Parse lengths of strings, with and without quotes+escapes.
    Solution is the sum of lengths of raw strings - sum of lengths of evaluated strings
    Use literal_eval() to convert raw to evaluated strings.
    E.g. "aaa\"aaa" becomes aaa"aaa

Part 2:
    Convert raw strings into the escaped format that would be required to express them in Python. 
    I.e. escape all chars that need escaping, and wrap in additional quotes.
    E.g. "aaa\"aaa" becomes \"aaa\\\"aaa\", all wrapped in another pair of quotes
"""
from pathlib import Path
import time
import re
from ast import literal_eval

SCRIPT_DIR = Path(__file__).parent 
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    raw_lengths = []
    evaluated_lengths = []
    encoded_lengths = []
    for line in data:
        line = line.strip()
        raw_lengths.append(len(line))
        
        # Use literal_eval to take the raw string, and evaluate it as a Python expression
        str_repr = literal_eval(line)

        # Part 1
        evaluated_lengths.append(len(str_repr))

        # Part 2
        # replace any " with \" and any \ with \\
        # we do this by just inserting a \ before each matching \1.
        encoded_str = r'"' + re.sub(r'(["\\])', r'\\\1', line) + r'"'
        encoded_lengths.append(len(encoded_str))

    sum_raw_lengths = sum(raw_lengths)
    sum_eval_lengths = sum(evaluated_lengths)
    sum_encoded_lengths = sum(encoded_lengths)
    print(f"Sum of raw strings: {sum_raw_lengths}") 
    print(f"Sum of evaluated strings: {sum_eval_lengths}") 
    print(f"Diff: {sum_raw_lengths-sum_eval_lengths}") 

    print(f"Sum of encoded strings: {sum_encoded_lengths}") 
    print(f"Diff: {sum_encoded_lengths-sum_raw_lengths}") 

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
