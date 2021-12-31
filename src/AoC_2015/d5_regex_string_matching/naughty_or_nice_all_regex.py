""" 
Author: Darren
Date: 14/01/2021

Solving https://adventofcode.com/2015/day/5

Determine if a string is naughty or nice.

Solution 2 of 2:
    All rules done in regex.
    Quite a bit faster than iterating through strings looking for repeating chars.

Part 1:
Nice includes ALL of: 3 vowels, a letter that appears twice in a row, and NOT ab, cd, pq, or xy

Part 2:
Nice includes ALL of:
    Any two chars that repeat anywhere in the remaining string.
    Any two chars that repeat, with a single char between them.
"""
import sys
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

# part 1 rules
three_vowels_match = re.compile(r"([aeiou].*){3}")
# \1 means: repeat what we matched before
double_chars_match = re.compile(r"(.)\1")
bad_chars_match = re.compile(r"ab|cd|pq|xy")

# part 2 rules
char_pair_repeats_match = re.compile(r"(..).*\1")
xwx_match = re.compile(r"(.).\1")


def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    nice_lines_count = sum(1 for line in data if part_1_rules_match(line))
    print(f"Part 1: there are {nice_lines_count} nice strings.")

    nice_lines_count = sum(1 for line in data if part_2_rules_match(line))
    print(f"Part 2: there are {nice_lines_count} nice strings.")


def part_2_rules_match(input):
    return (char_pair_repeats_match.search(input)
        and xwx_match.search(input))


def part_1_rules_match(input):
    return (three_vowels_match.search(input) 
        and double_chars_match.search(input) 
        and not bad_chars_match.search(input))


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")