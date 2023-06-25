"""
Author: Darren
Date: 01/12/2023

Solving https://adventofcode.com/2023/day/1

Part 1:

Part 2:

"""
import logging
from pathlib import Path
import time
import common.type_defs as td

SCRIPT_NAME = Path(__file__).stem
SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
OUTPUT_DIR = Path(SCRIPT_DIR, "output")
# OUTPUT_FILE = Path(OUTPUT_DIR, "output.png")

logger = logging.getLogger(SCRIPT_NAME)
logger.setLevel(logging.DEBUG)
logger.addHandler(td.stream_handler)
# td.setup_file_logging(logger, OUTPUT_DIR, SCRIPT_NAME)

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    logger.debug(data)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
