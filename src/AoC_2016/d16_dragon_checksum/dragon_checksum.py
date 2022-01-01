"""
Author: Darren
Date: 07/08/2021

Solving https://adventofcode.com/2016/day/16

Part 1:
    So trivial, doesn't really require explaining.
    
Part 2:
    Same as part 1, but with a much longer target.  No changes required.
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

PART_1_TARGET_DATA_SIZE = 272
PART_2_TARGET_DATA_SIZE = 35651584

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()
    
    dragon_data = generate_dragon_data(data, PART_1_TARGET_DATA_SIZE)
    checksum = compute_checksum(dragon_data)
    logging.info(f"Part 1 Checksum: {checksum}")
    
    dragon_data = generate_dragon_data(data, PART_2_TARGET_DATA_SIZE)
    checksum = compute_checksum(dragon_data)
    logging.info(f"Part 2 Checksum: {checksum}")


def compute_checksum(dragon_data: str) -> str:
    checksum = ""   # initialise with even length
    checksum_input = dragon_data     # start by generating checksum from our dragon data
    while len(checksum) % 2 == 0:   # keep generating checksums from last checksum, until checksum is even length
        checksum = ""
        for i in range(0, len(checksum_input), 2):   # increment 2 at a time
            if checksum_input[i] == checksum_input[i+1]:
                checksum += "1"     # if these two adjacent chars are the same
            else:
                checksum += "0"     # if these two adjacent chars are different
        
        checksum_input = checksum
    
    return checksum

def generate_dragon_data(data, target_size):
    """ Runs the source data through dragon encoding, 
    until the resulting data is at least as large as the target size.
    Then return exactly the first target_size chars.

    Args:
        data ([str]): Source data to encode
        target_size ([int]): Target data size required

    Returns:
        [str]: Encoded data
    """
    dragon_data = dragon_encode(data)
    
    # repeat until we have enough characters
    while len(dragon_data) < target_size:
        dragon_data = dragon_encode(dragon_data)
    
    # we only want the specified number of chars
    dragon_data = dragon_data[:target_size]
    
    return dragon_data


def dragon_encode(input_data) -> str:
    """ Takes an initial state (the input_data) and then applies these transformations:
     - Call the data you have at this point "a".
     - Make a copy of "a"; call this copy "b".
     - Reverse the order of the characters in "b".
     - In "b", replace all instances of 0 with 1 and all 1s with 0.
     - The resulting data is "a", then a single 0, then "b".
     
     As a result, each transformation returns a str that is 2n+1 in length """
    part_a = input_data
    part_b = part_a[::-1].replace("0", "x").replace("1", "0").replace("x", "1")
    result = part_a + "0" + part_b
    return result


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
