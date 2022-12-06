"""
Author: Darren
Date: 06/12/2022

Solving https://adventofcode.com/2022/day/6

Part 1:

Read the input stream. Report how many characters have been read when the last four chars are all different.

- Solution
  - Let distinct_chars_required = 4
  - Process the data stream one char at a time and track the slice of the last distinct_chars_required
  - Perform count of all chars in distinct_chars_required. If they are all 1, then we have our goal.

Part 2:

How many characters need to be processed before the first start-of-message marker is detected?

- This is exactly the same as part 1, except distinct_chars_required = 14.

"""
from pathlib import Path
import time
from collections import Counter

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

MARKER_SZ = 4
START_MSG_SZ = 14

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()
        
    distinct_chars, current_posn = process_stream(data, MARKER_SZ)
    print(f"Part 1: {distinct_chars} at {current_posn}")
    
    distinct_chars, current_posn = process_stream(data, START_MSG_SZ)
    print(f"Part 2: {distinct_chars} at {current_posn}")    

def process_stream(data: str, distinct_char_sz: int) -> tuple:
    """ Process a str of data. 
    Report char position when the last distinct_char_sz chars are all different.

    Returns: tuple: (distinct_chars, position) """
    last_sz_chars = ""
    current_posn = 0
    
    stream = data[0:distinct_char_sz]
    for i, char in enumerate(data[distinct_char_sz:]):
        current_posn = i + distinct_char_sz
        last_sz_chars = data[current_posn-distinct_char_sz:current_posn]
        char_counts = Counter(last_sz_chars) # count chars in last four chars
        if all(count == 1 for count in char_counts.values()):
            break

        stream += char
    
    return (last_sz_chars, current_posn)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
