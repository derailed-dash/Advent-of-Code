"""
Author: Darren
Date: 28/05/2021

Solving https://adventofcode.com/2016/day/5

Solution:
    Find 8 char password.
    Compute hashes from input data + incrementing seq
    Find first valid hex repr of hash starting with 00000

Part 1:
    Take 6th char of hash as next char of password.
    Keep incrementing until we have 8 valid hashes, and thus, 8 chars of the password.

Part 2:
    6th char represents position in the password (0-7)
    7th char is the char to put in that position.
    Use only the first result for that position.
    Ignore invalid positions.
    So trivial, no explanation necessary.

"""
import logging
import os
import time
import hashlib

# pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        door_id = f.read()
    
    logging.info(f"Door ID: {door_id}")

    # Part 1
    pwd = ""
    nonce = 0
    while len(pwd) < 8:
        data = door_id + str(nonce)
        # Create byte equivalent of input string, then generate md5 hexdigest.
        hash_hex = hashlib.md5(data.encode()).hexdigest()
        
        if hash_hex.startswith("00000"):
            pwd = pwd + hash_hex[5]
            logging.debug(f"Found {hash_hex} with data {data}.")
            logging.info(f"Pwd is: {pwd}")
            
        nonce += 1
    
    # Part 2
    pwd = "________"
    nonce = 0
    while "_" in pwd:
        data = door_id + str(nonce)
        # Create byte equivalent of input string, then generate md5 hexdigest.
        hash_hex = hashlib.md5(data.encode()).hexdigest()
        
        if hash_hex.startswith("00000"):
            position = hash_hex[5]
            if position in "01234567":
                position = int(position)
                # Check we haven't already filled this position
                if pwd[position] == "_":
                    pwd = pwd[:position] + hash_hex[6] + pwd[position+1:]
                    
                    logging.debug(f"Found {hash_hex} with data {data}.")
                    logging.info(f"{pwd}")
        
        nonce += 1


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
