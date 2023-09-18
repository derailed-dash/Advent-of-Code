"""
Author: Darren
Date: 01/12/2023

Solving https://adventofcode.com/2023/day/1

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as td

YEAR = 2017
DAY = 1

locations = td.get_locations(__file__)
logger = td.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
td.write_puzzle_input_file(YEAR, DAY, locations)

def main():
    with open(locations.sample_input_file, mode="rt") as f:
    # with open(locations.input_file, mode="rt") as f:        
        data = f.read().splitlines()
        
    logger.debug(data)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
