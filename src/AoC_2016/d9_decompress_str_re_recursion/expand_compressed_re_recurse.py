"""
Author: Darren
Date: 11/06/2021

Solving https://adventofcode.com/2016/day/9

Solution 2 of 2:
    X(8x2)(3x3)ABCY
    
    Original solution replaced src str with target str, i.e. by expanding.
    However, part 2 was taking too long.  Probably would have taken several hours.
    
    This solution doesn't create the expanded str.  
    It simply calculates the lenths of segments that would be in the expanded str.
    
Part 1:
    Calculate length of str segment, by multiplying n*m.
    Then recursively call for the rest of the str, until no more segments.

Part 2:
    As with Part 1, but now we want to replace the call to len to instead
    be a call to recursive_len().  I.e. we now recurse into each segment, 
    not just to retrieve the rest of the str.
    This is flippin' fast at returning a count of 10bn+.

"""
import logging
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

expand_pattern = re.compile(r"\((\d+)x(\d+)\)")

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        src_str = f.read()
            
    # Part 1 - Uses the default len_func=len(), so (nxm) segments are only expanded once
    result = decompressed_len(src_str=src_str)
    logging.info(f"Part 1: Expanded str length = {result}")
    
    # Part 2 - Recurses into each segment
    result = recursive_len(src_str=src_str)
    logging.info(f"Part 2: Expanded str length = {result}")


def recursive_len(src_str: str) -> int:
    """Recursively calls decompressed_len

    Args:
        src_str (str): Source str to expand

    Returns:
        [int]: Length of th expanded str
    """
    return decompressed_len(src_str=src_str, len_func=recursive_len)

    
def decompressed_len(src_str: str, len_func=len) -> int:
    """ Process src_str one char at a time, looking for (nxm) using re.
    
    We can supply any function to len_func.  If we use len(), 
    then when we expand the segment, it returns the length after a single nxm expansion.
    If we use recurive_len(), then we recursively expand the segment.
    
    Args:
        src_str (str): The compressed str we want to determine expanded length for
        len_func (callable): A function that returns an int
                E.g. len() or recursive_len()

    Returns:
        [int]: The length of the expanded str
    """
    # If there's no more src_str left...
    if not src_str:
        return 0

    # See if we've found (nxm) at the BEGINNING of the str
    match = expand_pattern.match(src_str)
    if match:
        extent, repeat = map(int, match.groups())
        
        # determine positions of the segments we need to amplify
        start = match.end()
        end = match.end() + extent
        
        # return the length of this repeated segment
        # + recurse to get the expanded lenght of the rest of the src str
        return (repeat * len_func(src_str[start:end]) 
                + decompressed_len(src_str[end:], len_func))

    # If we're here, then no (nxm) found at beginning
    # Return length of this first char (1) and move on to the rest of the str
    return 1 + decompressed_len(src_str[1:], len_func)


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
