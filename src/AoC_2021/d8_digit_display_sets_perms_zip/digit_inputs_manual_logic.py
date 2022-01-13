"""
Author: Darren
Date: 08/12/2021

Solving https://adventofcode.com/2021/day/8

  0:      1:      2:      3:      4:      5:      6:      7:      8:      9:
 aaaa    ....    aaaa    aaaa    ....    aaaa    aaaa    aaaa    aaaa    aaaa
b    c  .    c  .    c  .    c  b    c  b    .  b    .  .    c  b    c  b    c
b    c  .    c  .    c  .    c  b    c  b    .  b    .  .    c  b    c  b    c
 ....    ....    dddd    dddd    dddd    dddd    dddd    ....    dddd    dddd
e    f  .    f  e    .  .    f  .    f  .    f  e    f  .    f  e    f  .    f
e    f  .    f  e    .  .    f  .    f  .    f  e    f  .    f  e    f  .    f
 gggg    ....    gggg    gggg    ....    gggg    gggg    ....    gggg    gggg 
 
Data input is in the format: 
    ten unique signal patterns | four digit output value
    E.g. be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    
Note that the following digits are rendered by the following segment counts:
0: 6, 1: 2*, 2: 5, 3: 5, 4: 4*, 5: 5, 6: 6, 7: 3*, 8: 7*, 9: 6

Solution 1:
    Here we use set algebra against numbers and segments, 
    making use of our knowledge of how many segments are required for each number.

Part 1:
    Counting digits in output values only, how many times to 1, 4, 7 and 8 appear?
    
    Read in signals and outputs into two lists of sorted strings.
    Only digits 1, 4, 7 and 8 are rendered by unique counts of segments.
    Work out which digits corresponds to these unique counts for each row of output.
    Then count the total of all the digits.  Easy!

Part 2:
    Not so easy.
    The goal is to map each of the unique digit inputs (0-9) to an input str (for each line).
    Then we can use the map to look the 4-digit output value for each line (for each line).
    
    We already have 1, 4, 7, and 8 mapped.
    We can work out segment a, since it's in 7 but not 1.
    We can propose candidates for c/f, since they're in 1.
    We can propose candidates for b/d, since they're in 4, but not 7.
    We can determine 3, since it's the only 5-segment digit that contains 1. (Leaving 2, 5.)
    We can determine d, since it's the intersection of 3 and b+d.  Now we know b also.
    5 is the intersection of digits 2,5 and segment b.  Now we know 2 also, since it's the only 5 segment left.
    We can determine 9, since it's the only 6-segment digit that contains 4. (Leaving 0, 6.)
    We can determine 0, since it's the only one of 0,9 that contains d.  Now we also know 6.
    
    Finally, return the map of str to digit values, and use to lookup, 
    for the outputs of each matching row.
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

unique_segment_counts = {2: 1, 4: 4, 3: 7, 7: 8}   # {count: digit}

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    signals = []      # list of lists of sorted segment signals for all digits
    outputs = []      # list of lists of sorted output values
    for line in data:
        digit_signals, four_digit_outputs = line.split("|")
        signals.append(["".join(sorted(signal)) for signal in digit_signals.split()])
        outputs.append(["".join(sorted(signal)) for signal in four_digit_outputs.split()])
    
    # Part 1
    all_easy_digits = []
    for output_line in outputs:
        # Determine which digits in the output are in 1, 4, 7, 8
        easy_digits = [output for output in output_line if len(output) in unique_segment_counts]
        all_easy_digits.append(easy_digits)  # append, e.g. ['bcg', 'abcdefg', 'cg']
        
    sum_of_easy_digits = sum([len(digits) for digits in all_easy_digits])   # count all
    logger.info("Sum of easy digits: %d", sum_of_easy_digits)
    
    # Part 2
    outs = []
    for i, input_line in enumerate(signals):
        signal_map = determine_signal_map(input_line)       
        
        outs.append(int("".join([str(signal_map[output]) for output in outputs[i]])))

    logger.info("Sum of outputs: %d", sum(outs))

def determine_signal_map(input_line):
    """ Return a dict that maps the str representation of the segments to the digit they produce """
    segments = {}        # {segment: set(inputs)}
    seg_candidates = {}  # {segment: set(inputs)}
    
    # create a list, containing a set of signals for each (unknown) unique digit
    digit_signals = [set(input) for input in input_line] 
        
    # First let's map the easy digits to segment sets, in the form {digit: set(signals)}
    # We know 1, 4, 7, 8.  E.g. {1: {'g', 'c'}, ...}
    known_digits = {unique_segment_counts[len(input)]: set(input) 
                  for input in input_line if len(input) in unique_segment_counts}
    
    segments["a"] = known_digits[7] - known_digits[1] # a is in 7, but not in 1
    seg_candidates["b"] = seg_candidates["d"] = known_digits[4] - known_digits[7] # b, d are in 4 but not in 7
    seg_candidates["c"] = seg_candidates["f"] = known_digits[1] # c, f are in 1        
        
    unknown_digits_with_five_segments = [digit for digit in digit_signals if len(digit)==5] # 2, 3, 5
    known_digits[3] = [digit for digit in unknown_digits_with_five_segments 
                           if digit > known_digits[1]][0]       # Only digit 3 contains digit 1
    unknown_digits_with_five_segments.remove(known_digits[3])   # Leaving 2, 5
        
    segments["d"] = seg_candidates.pop("d") & known_digits[3]
    segments["b"] = seg_candidates.pop("b") - segments["d"]

    # 5 contains b (known); whilst 2 doesn't. 5 contains f (unknown)
    known_digits[5] = [digit for digit in unknown_digits_with_five_segments 
                           if digit > segments["b"]][0]
    unknown_digits_with_five_segments.remove(known_digits[5])  # Leaving 2.
    known_digits[2] = unknown_digits_with_five_segments[0]

    unknown_digits_with_six_segments = [digit for digit in digit_signals if len(digit)==6] # 0, 6, 9
    known_digits[9] = [digit for digit in unknown_digits_with_six_segments 
                           if digit > known_digits[4]][0]    # 9 is the only one that contains 4
    unknown_digits_with_six_segments.remove(known_digits[9]) # 0, 6 remaining

    known_digits[6] = [digit for digit in unknown_digits_with_six_segments 
                           if digit > segments['d']][0]      # 6 is the only one that contains segment d
    unknown_digits_with_six_segments.remove(known_digits[6]) # 0 remaining
    known_digits[0] = unknown_digits_with_six_segments[0]                          
        
    # convert back to strings and transpose to {str: digit}
    return {"".join(sorted(input)): digit for digit, input in known_digits.items()}

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
