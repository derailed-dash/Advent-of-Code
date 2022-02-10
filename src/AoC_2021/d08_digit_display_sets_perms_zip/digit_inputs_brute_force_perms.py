"""
Author: Darren
Date: 08/12/2021

Solving https://adventofcode.com/2021/day/8

The sub has a four-digit display, with each digit generated from the use of seven segments.
Input wires have been scambled, so we do not know which input wires
correspond to which segment in the display.
E.g. wires c, f should be used to generate digit 1.

  0:      1:      2:      3:      4:      5:      6:      7:      8:      9:
 aaaa    ....    aaaa    aaaa    ....    aaaa    aaaa    aaaa    aaaa    aaaa
b    c  .    c  .    c  .    c  b    c  b    .  b    .  .    c  b    c  b    c
b    c  .    c  .    c  .    c  b    c  b    .  b    .  .    c  b    c  b    c
 ....    ....    dddd    dddd    dddd    dddd    dddd    ....    dddd    dddd
e    f  .    f  e    .  .    f  .    f  .    f  e    f  .    f  e    f  .    f
e    f  .    f  e    .  .    f  .    f  .    f  e    f  .    f  e    f  .    f
 gggg    ....    gggg    gggg    ....    gggg    gggg    ....    gggg    gggg 

Data example is in the format: 
    All signal patterns for ten digits, 0-9 | Four digit output (using four of the input patterns)
    E.g. be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    
In this first sample row, digit 1 would be generated from wires b,e.
    
Note that the following digits are rendered by the following segment counts:
0: 6, 1: 2*, 2: 5, 3: 5, 4: 4*, 5: 5, 6: 6, 7: 3*, 8: 7*, 9: 6

Solution 2:
    Here we use brute force to look at all possible permutations of segments, 
    and determine which permutation works for a given input-to-output line.

Part 1:
    Counting digits in output values only, how many times do digits 1, 4, 7 and 8 appear?
    
    Read in signals and outputs into two lists of sorted strings.
    Only digits 1, 4, 7 and 8 are rendered by unique counts of segments.
    Work out which digits corresponds to these unique counts for each row of output.
    Then count the total of all the digits.  Easy!

Part 2:
    We need the sum of all the output digits.

    The goal is to map each of the unique digit inputs (0-9) to an input str (for each line).
    Then we can use the map to look the 4-digit output value for each line (for each line).
    There are 7! (5040) permutations of segments. 
    So we can map each permutation to the input strings, and see which produces valid output.
"""
from collections import defaultdict
import logging
import os
import time
from itertools import permutations

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

SEGMENTS = "abcdefg"

# These are the output signal segment combinations that are valid
VALID_DIGITS = {
    "abcefg": 0,
    "cf": 1,    
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    signals = []      # list of lists of sorted segment signals for all digits
    outputs = []      # list of lists of 4 * sorted output values
    for line in data:
        digit_signals, four_digit_outputs = line.split("|")
        signals.append(["".join(sorted(signal)) for signal in digit_signals.split()])
        outputs.append(["".join(sorted(signal)) for signal in four_digit_outputs.split()])
    
    # Count how many segments are used for each digit      
    digit_counts = defaultdict(list)
    for digit_segments in VALID_DIGITS:
        # store as {count: [digit_segments]}, e.g. 2: ['cf'], 5: ['acdeg', 'acdfg', 'abdfg']
        digit_counts[len(digit_segments)].append(digit_segments)
    
    # filter simple_digits to include only ["cf", "bcdf", "acf", "abcdefg"]:
    simple_digits = [v[0] for k, v in digit_counts.items() if len(v) == 1]  
    
    count_simple_digits_in_output = 0
    numeric_outputs = []
    
    # process each row of data; different rows require different perms
    for row_num, input_row in enumerate(signals): 
        
        # There are 5040 (7!) permutations of input signals (segments)
        # Only one will be valid for any given line
        for perm in permutations(SEGMENTS): # e.g. ('c', 'a', 'b', 'f', 'e', 'g', 'd')
            # Now we need to map input char to a char in the perm
            # E.g. {'a': 'c', 'b': 'a', 'c': 'b', 'd': 'f', 'e': 'e', 'f': 'g', 'g': 'd'}
            # We can zip the 7-char SEGMENTS with the current 7-char perm
            # This is much neater than: 
            # unscramble_map = {SEGMENTS[i]: perm[i] for i, char in enumerate(SEGMENTS)}
            unscramble_map = dict(zip(SEGMENTS, perm))
            
            try:    # use try-except pattern for continuing outer loop
                for word in input_row:
                    unscrambled_word = unscramble(word, unscramble_map)
                    if unscrambled_word not in VALID_DIGITS:
                        raise StopIteration     # if any unscrambled not in valid
            except StopIteration:
                continue    # continue to next permutation
            
            # If we're here, then we've got a permutation that maps to valid digits
            numeric_output = []
            for word in outputs[row_num]:
                unscrambled_word = unscramble(word, unscramble_map)
                # check if in ("cf", "bcdf", "acf", "abcdefg"):
                if unscrambled_word in simple_digits:
                    count_simple_digits_in_output += 1
                
                # convert from segments to digit, and append the digit
                numeric_output.append(VALID_DIGITS[unscrambled_word])

            numeric_outputs.append(int("".join(map(str, numeric_output)))) # convert to 4-digit int
            break   # If we've got here, we've got everything we need. No more perms needed.
                 
    logger.info("Part 1 - Sum of easy digits: %d", count_simple_digits_in_output)
    logger.info("Part 2 - Sum of numeric outputs=%d", sum(numeric_outputs))
    
def unscramble(word, unscramble_map: dict) -> str:
    """ Takes a scrambled input word, and converts to unscrambled.
    
    Args:
        word (str): Scrambled input
        unscramble_map (dict): Map of scrambled char->unscrambled char """
    return "".join(sorted([unscramble_map[char] for char in word]))

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
