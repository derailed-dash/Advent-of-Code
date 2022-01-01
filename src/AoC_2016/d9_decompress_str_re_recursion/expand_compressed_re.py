"""
Author: Darren
Date: 11/06/2021

Solving https://adventofcode.com/2016/day/9

Solution 1 of 2:
    X(8x2)(3x3)ABCY
    
    Uses regex to identify (nxm).
    Then expands subsequent text according to (nxm) rules.
    Create a new str based on expanded text.
    
Part 1:
    Build expanded str by expanding src str.

    While more str:
        Find next (nxm), expand, and move src_str pointer to char+n posn.
        Copy any chars before the match to the expanded_str.
        Then expand according to nxm.
        Move char pointer to char+n.
        Ignore any (nxm) within the expanding segment.
        
    Runs in about 5ms.

Part 2:
    As Part 1, but now expand all (nxm) within the expanding segment.
    I.e. wrap in another while loop that continues until there are
    no remaining (nxm).
    
    This solution is going to take hours to complete!
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
            
    # Part 1
    char_posn = 0
    expanded_str = ""
    while char_posn < len(src_str):
        match = expand_pattern.search(src_str, char_posn)
        if match:
            match_start = match.start()
            match_end = match.end()
            extent, repeat = [int(x) for x in match.groups()]
            
            expanded_str += src_str[char_posn:match_start]
            for _ in range(repeat):
                expanded_str += src_str[match_end:match_end+extent]
            
            char_posn = match_end+extent
        else:
            expanded_str += src_str[char_posn:]
            char_posn = len(src_str)
            
    # logging.debug(expanded_str)
    logging.info(f"Part 1: Expanded str length = {len(expanded_str)}")

    # Part 2
    char_posn = 0
    expanded_str = ""
    
    while expand_pattern.search(src_str):
        while char_posn < len(src_str):
            match = expand_pattern.search(src_str, char_posn)
            if match:
                match_start = match.start()
                match_end = match.end()
                extent, repeat = [int(x) for x in match.groups()]
                
                expanded_str += src_str[char_posn:match_start]
                for _ in range(repeat):
                    expanded_str += src_str[match_end:match_end+extent]
                
                char_posn = match_end+extent
            else:
                expanded_str += src_str[char_posn:]
                char_posn = len(src_str)
        
        logging.debug(f"Part 2: Expanded str length = {len(expanded_str)}")
        src_str = expanded_str
    
    logging.info(f"Part 2: Expanded str length = {len(expanded_str)}")
    

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
