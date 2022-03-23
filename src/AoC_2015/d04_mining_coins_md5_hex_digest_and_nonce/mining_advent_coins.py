""" 
Author: Darren
Date: 13/01/2021

Solving https://adventofcode.com/2015/day/4

Determine first MD5 hex digest of seed + str representation of a number n,
where the resulting hex digest starts with 5, 6 zeroes.
What is the value of n?

This is simulating creating a block on the blockchain.
I.e. the hex digest is equivalent to the block hash.
The number of leading zeros is equivalent to the difficulty of the proof of work.
The number n, is equivalent to the nonce.
"""
from pathlib import Path
import time
import hashlib

SCRIPT_DIR = Path(__file__).parent 
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        hash_seed = f.read()
    
    # counter is the nonce
    counter = 0
    part1_solved = part2_solved = False
    while not (part1_solved and part2_solved):
        data = hash_seed + str(counter)
        # Create byte equivalent of input string, then generate md5 hexdigest.
        hash_hex = hashlib.md5(data.encode()).hexdigest()
        
        if hash_hex.startswith(5*"0") and not part1_solved:
            print(f"Part 1. With input {data}, hash = {hash_hex}")
            part1_solved = True

        if hash_hex.startswith(6*"0") and not part2_solved:
            print(f"Part 2. With input {data}, hash = {hash_hex}")
            part2_solved = True

        counter += 1  # increment the nonce

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
