"""
Author: Darren
Date: 26/07/2021

Solving https://adventofcode.com/2016/day/14

Solution 2 of 2:
    Trivial md5 hashing problem.
    However, because we have to generate the next 1000 hashes for each successful hash,
    and because those 1000 hashes are typically overlapping, 
    it's much more efficient if we store previously calculated hashes in a dict against the index.
    In this solution, we use the LRU_cache to store the previous hashes.
"""
import hashlib
import logging
import os
import time
import re
import functools

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

triple_chars_match = re.compile(r"(.)\1\1")
KEYS_TO_FIND = 64
MD5_REPEATS = 2016

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        salt = f.read()
    
    index, keys = find_keys(salt)   
    logging.info("Part 1: 64th key produced at index %d", index-1)
    
    index, keys = find_keys(salt, MD5_REPEATS)   
    logging.info("Part 2: 64th key produced at index %d", index-1)

def find_keys(salt, repeats=0):
    keys = []
    index = 0
    
    while len(keys) < KEYS_TO_FIND:
        to_hash = salt + str(index)
        hash_hex = hash_method(to_hash, repeats)
        
        if match := triple_chars_match.search(hash_hex):
            five_char_seq = 5*match.group()[0]
            for i in range(1, 1001):
                subsequent_hash = hash_method(salt+str(index+i), repeats)
                
                if five_char_seq in subsequent_hash:
                    keys.append(hash_hex)
                    break
            
        index += 1
    return index, keys

@functools.lru_cache(None)
def hash_method(to_hash, repeats):
    result = to_hash
    for _ in range(repeats+1):
        result = hashlib.md5(result.encode()).hexdigest()
    
    return result

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
