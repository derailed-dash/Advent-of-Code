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

Solution 1:
    Here we'll use Parsimonious PEG to parse the data and catch validation errors.

Part 1:
    Get syntax error score. 
    I.e. find first invalid char on each corrupted line, and get score for that character.
    Sum all the invalid character scores.
    
    We need to distinguish between:
    - IncompleteParseError - got to the end of the line, some rules passed, but incomplete
    - ParseError, pos == len(line) - got to the end, but no rules passed, therefore incomplete
    - ParseError, pos < len(line) - corrupted

Part 2:
    Get completion scores, by completing incomplete lines.
    We want the median score of the sorted scores.
    
    Strip out corrupted lines to leave only incomplete lines.
    For each line...
    - Count from right hand end
    - Use DefaultDict to count each type of closing bracket as we go
    - If we come across an opening bracket, we decrement the matching closer.
    - If there's no matching closer, then the closer is missing, so append it.
    - Finally, score up the appended chars (trivial).
"""
from collections import defaultdict
import logging
import os
import time
from parsimonious import Grammar, ParseError
from parsimonious.exceptions import IncompleteParseError

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

# Define our rules for parsing the input
# Each row (expr) must contain one or more chunks (any)
# Each chunk (any) can be of type 'normal', 'angle', 'square', or 'curly'
# Each type is composed of a bracket pair, and 0 or more inner chunks (any)
grammar = Grammar(r"""
    expr = any+
    any = (normal / angle / square / curly)
    normal = "(" any* ")"
    angle = "<" any* ">"
    square = "[" any* "]"
    curly = "{" any* "}"
""")

OPENERS = ["(", "[", "{", "<"]
CLOSERS = [")", "]", "}", ">"]
OPEN_TO_CLOSE = dict(zip(OPENERS, CLOSERS))  # {'(': ')', ...}
CLOSE_TO_OPEN = dict(zip(CLOSERS, OPENERS))  # {')': '(', ...}

COMPLETION_CHAR_SCORES = dict(zip(CLOSERS, (1, 2, 3, 4)))  # {')': 1, ...}
INVALID_CHAR_SCORES = dict(zip(CLOSERS, (3, 57, 1197, 25137))) # {')': 3, ...}

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    # Part 1 - Looking for corrupted lines only
    incomplete_lines = []
    invalid_chars = []
    for line_num, line in enumerate(data):
        try:
            grammar.parse(line)
        except IncompleteParseError:    # valid, but incomplete
            incomplete_lines.append(line)
        except ParseError as err:
            if err.pos == len(line):    # valid, but incomplete
                incomplete_lines.append(line)
            else:                       # corrupted
                logger.debug("%d: %s", line_num, line)
                logger.debug("Found %s", line[err.pos])
                invalid_chars.append(line[err.pos])

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
    close_counters = defaultdict(int)
    for char in line[::-1]:     # process chars from the end
        if char in CLOSERS:
            close_counters[char] += 1
        else:  # opener
            matching_closer = OPEN_TO_CLOSE[char]
            if close_counters[matching_closer] > 0:    # opener for existing closer
                close_counters[matching_closer] -= 1
            else:    # opener, but missing closer
                to_complete += matching_closer
                
    return to_complete

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
