""" 
Author: Darren
Date: 14/01/2021

Solving https://adventofcode.com/2015/day/5

Determine if a string is naughty or nice.

Solution 1 of 2:
    Mix of using regex, plus simply matching chars at positions to match repeating chars.

Part 1:
Nice includes ALL of: 3 vowels, a letter that appears twice in a row, and NOT ab, cd, pq, or xy

Part 2:
Nice includes ALL of:
    Any two chars that repeat anywhere in the remaining string.
    Any two chars that repeat, with a single char between them.
"""
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

VOWELS_P = re.compile(r"([aeiou]).*([aeiou]).*([aeiou])")
BAD_CHARS_P = re.compile(r"ab|cd|pq|xy")


def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    nice_lines = []
    for line in data:
        if vowels_rule_match(line) and two_chars_rule_match(line) and no_bad_chars_match(line):
            nice_lines.append(line)

    print(f"Part 1: there are {len(nice_lines)} nice strings.")

    nice_lines = []
    for line in data:
        if two_pairs_match(line) and repeat_with_char_between_match(line):
            nice_lines.append(line)

    print(f"Part 2: there are {len(nice_lines)} nice strings.")


def repeat_with_char_between_match(input):
    ''' Find any two repeated chars, with any char between them '''
    for i in range(len(input) - 2):
        if input[i] == input[i+2]:
            return True

    return False

def two_pairs_match(input):
    ''' Find any two chars that are repeated anywhere in the string '''
    for i in range(len(input) - 1):
        if input[i:i+2] in input[i+2:]:
            return True

    return False


def vowels_rule_match(input):
    ''' Any string containing 3 or more vowels '''
    if VOWELS_P.search(input):
        if len(VOWELS_P.search(input).groups()) >= 3:
            return True

    return False

def no_bad_chars_match(input):
    ''' Must not contain any of the bad char pairs '''
    bad_match = BAD_CHARS_P.search(input)
    if not bad_match:
        return True

    return False


def two_chars_rule_match(input):
    ''' Any two repeating characters '''
    for i in range(len(input) - 1):
        if input[i] == input[i+1]:
            return True

    return False


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
