"""
Author: Darren
Date: 10/12/2021

Solving https://adventofcode.com/2021/day/10

Process navigation data line-by-line. Navigation lines look like:
[({(<(())[]>[[{[]{<()<>>
    - Each line contains one or more navigation 'chunks'. 
    - Chunks open and close with matching brackets.
      Valid brackets = (), <>, {}, []
    - Each chunk contains zero or more inner chunks.

Some lines are incomplete, whilst some are corrupted.
    - Corrupted = bracket present which invalidates the rules, i.e. wrong closer 
      E.g. {()()()>
    - Incomplete = valid, but not yet closed. 

Solution 2:
    Strip out complete sets of brackets, until only incomplete and corrupted remain.
    This is much faster than parsing with Parsimonious.

Part 1:
    Get syntax error score. 
    I.e. find first invalid char on each corrupted line, and get score for that character.
    Sum all the invalid character scores.
    
    Just use str replace to iteratively remove any pairs of brackets until nothing left to remove.
    At this point, incomplete lines will have no closing brackets,
    but corrupt lines will have closing brackets, and no matching opener.
    
Part 2:
    Get completion scores, by completing incomplete lines.
    We want the median score of the sorted scores.
    
    Strip out corrupted lines to leave only incomplete lines.
    Each incomplete line is now a set of opening brackets with no matching closer.
    So simply go through the openers in reverse, adding the correspnding closer.
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

OPENERS = ["(", "[", "{", "<"]
CLOSERS = [")", "]", "}", ">"]
PAIRS = ["".join(item) for item in zip(OPENERS, CLOSERS)] # ['()', '[]', ...]
OPEN_TO_CLOSE = dict(zip(OPENERS, CLOSERS))  # {'(': ')', ...}

INVALID_CHAR_SCORES = dict(zip(CLOSERS, (3, 57, 1197, 25137)))
COMPLETION_CHAR_SCORES = dict(zip(CLOSERS, (1, 2, 3, 4)))

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    # Part 1 - Looking for corrupted lines only
    incomplete_lines = []
    invalid_chars = []
    trimmed_lines = [trim_brackets(line) for line in data]
    for line in trimmed_lines:
        # corrupt lines will have closing brackets, whilst incomplete lines will not
        if any(char in CLOSERS for char in line):   # corrupt
            for char in line:
                if char in CLOSERS:
                    invalid_chars.append(char)  # find first closer
                    break
        else:
            incomplete_lines.append(line)

    logger.info("Part 1: There are %d corrupted lines", len(invalid_chars))                
    score = sum([INVALID_CHAR_SCORES[char] for char in invalid_chars])
    logger.info("Syntax error score=%d\n", score)
        
    # Part 2
    logger.info("Part 2: There are %d remaining incomplete lines", len(incomplete_lines))
    completion_scores = []
    for line in incomplete_lines:
        to_complete = get_completion_for_line(line)
        completion_scores.append(score := score_for_completion(to_complete))
        logger.debug("To complete: %s with score %d", to_complete, score)
    
    completion_scores.sort()
    logger.info("Completion score=%d", completion_scores[len(completion_scores)//2])

def get_completion_for_line(line: str) -> str:
    """ Determine which closing brackets need to be added to complete this incomplete line. """
    
    to_complete = ""
    for opener in line[::-1]:
        to_complete += OPEN_TO_CLOSE[opener]
                
    return to_complete

def trim_brackets(line: str) -> str:
    """ Iteratively strip out pairs of brackets from this line, until none remain """
    stripped = True
    while stripped:         # Continue until no more stripping
        stripped = False
        for bracket_pair in PAIRS:
            if bracket_pair in line:
                line = line.replace(bracket_pair, "")   # Strip out all occurences of this pair
                stripped = True

    return line

def score_for_completion(completion_str: str) -> int:
    """ Arbitrary rules for calculating a score for a str of completion chars """
    score = 0
    
    for char in completion_str:
        score *= 5
        score += COMPLETION_CHAR_SCORES[char]
        
    return score          

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
