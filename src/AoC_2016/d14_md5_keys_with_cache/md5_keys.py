"""
Author: Darren
Date: 26/07/2021

Solving https://adventofcode.com/2016/day/14

Solution:
    Trivial md5 hashing problem.
    However, because we have to generate the next 1000 hashes for each successful hash,
    and because those 1000 hashes are typically overlapping, 
    it's much more efficient if we store previously calculated hashes in a dict against the index.
"""
import hashlib
import logging
import os
import time
import re

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
    logging.info(f"Part 1: 64th key produced at index {index-1}")
    
    index, keys = find_keys(salt, MD5_REPEATS)   
    logging.info(f"Part 2: 64th key produced at index {index-1}")

def find_keys(salt, repeats=0):
    keys = []
    index = 0
    
    hashes_by_index = {}
    while len(keys) < KEYS_TO_FIND:
        if index in hashes_by_index:
            hash_hex = hashes_by_index[index]
        else:
            hash_hex = hash_method(salt, index, hashes_by_index, repeats)
        
        if match := triple_chars_match.search(hash_hex):
            five_char_seq = 5*match.group()[0]
            for i in range(1, 1001):
                if index+i in hashes_by_index:
                    subsequent_hash = hashes_by_index[index+i]
                else:
                    subsequent_hash = hash_method(salt, index+i, hashes_by_index, repeats)
                
                if five_char_seq in subsequent_hash:
                    keys.append(hash_hex)
                    break
            
        index += 1
    return index, keys

def hash_method(salt, index, hashes_by_index: dict, md5_repeats):
    result = hashlib.md5((salt+str(index)).encode()).hexdigest()
    for _ in range(md5_repeats):
        result = hashlib.md5(result.encode()).hexdigest()
    
    hashes_by_index[index] = result
    
    return result

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
