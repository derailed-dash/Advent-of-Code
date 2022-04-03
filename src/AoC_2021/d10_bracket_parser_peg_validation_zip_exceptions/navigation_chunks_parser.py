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

Solution 3:
    Create our own parser, based on a stack.
    
Part 1:
    Maintain a stack (deque) where the last item is the corresponding right bracket
    for any left bracket just read.
    If we read a right bracket that isn't at the top of the stack, 
    then raise a ParseException (custom exception). The ParseException contains the invalid char.
    
Part 2:
    Add a ParseIncompleteException. 
    This is raised whenever the stack has any remaining items after reading in all the characters.
    We reverse the stack, to obtain all the closing brackets required, in order.
"""
import logging
import os
import time
from collections import deque
from dataclasses import dataclass

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

OPENERS = ["(", "[", "{", "<"]
CLOSERS = [")", "]", "}", ">"]
OPEN_TO_CLOSE = dict(zip(OPENERS, CLOSERS))  # {'(': ')', ...}

COMPLETION_CHAR_SCORES = dict(zip(CLOSERS, (1, 2, 3, 4)))
INVALID_CHAR_SCORES = dict(zip(CLOSERS, (3, 57, 1197, 25137)))

@dataclass
class ParseException(Exception):
    """ Data parsed and found to be invalid """
    expected: str
    actual: str
  
@dataclass          
class ParseIncompleteException(Exception):
    """ Data parsed and found to be incomplete """
    remaining: str

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    # Part 1 - Looking for corrupted lines only
    invalid_chars = []
    completion_scores = []
    for line in data:
        try:
            parse(line)
        except ParseException as p_e:
            invalid_chars.append(p_e.actual)
        except ParseIncompleteException as pie:
            completion_scores.append(score_for_completion(pie.remaining))

    logger.info("Part 1: There are %d corrupted lines", len(invalid_chars))                
    score = sum([INVALID_CHAR_SCORES[char] for char in invalid_chars])
    logger.info("Syntax error score=%d\n", score)
    
    # Part 2
    completion_scores.sort()
    logger.info("Part 2: Completion score=%d", completion_scores[len(completion_scores)//2])

def parse(line: str):
    """ Parse the navigation instructions, line-by-line.
    If we read any right bracket that does not match an existing left bracket, raise ParseException.
    If we read all the data but still have closing brackets left on the stack, raise ParseIncompleteException.
    """
    stack = deque()
    
    for char in line:        
        if char in OPENERS:
            stack.append(OPEN_TO_CLOSE[char])
            continue    # Move on to the next char
        
        assert char in CLOSERS, "Must be right bracket"
        popped = stack.pop()    # Pop the required right bracket
        if char == popped:
            continue    # This was the right bracket we needed
    
        raise ParseException(expected=popped, actual=char)  # Wrong right bracket - invalid line
    
    if stack:   # There were more left brackets than right, so this line is incomplete
        raise ParseIncompleteException(remaining="".join(reversed(stack)))
    
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
