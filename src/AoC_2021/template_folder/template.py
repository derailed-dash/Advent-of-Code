"""
Author: Darren
Date: 01/12/2021

Solving https://adventofcode.com/2021/day/1

Part 1:

Part 2:

"""
from __future__ import annotations
import logging
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__) 
# INPUT_FILE = "input/input.txt"
INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
