"""
Author: Darren
Date: 01/12/2023

Solving https://adventofcode.com/2023/day/1

Part 1:

Part 2:

"""
import logging
import time
import aoc_common.aoc_commons as ac

YEAR = 2017
DAY = 1

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)
try:
    ac.write_puzzle_input_file(YEAR, DAY, locations)
except ValueError as e:
    logger.error(e)
    
with open(locations.input_file, mode="rt") as f:        
    input_data = f.read().splitlines()
    logger.debug(input_data)

def part1(data):
    return "uvwxyz"

def part2(data):
    return "uvwxyz"

def main(data):
    part1(data)
    part2(data)

if __name__ == "__main__":
    ac.validate(part1("abcdef"), "uvwxyz")
    ac.validate(part2("abcdef"), "uvwxyz")    
    
    t1 = time.perf_counter()
    main(input_data)
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
