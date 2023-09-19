""" 
Author: Darren
Date: 19/03/2021

Solving https://adventofcode.com/2015/day/20

Infinite elves deliver to infinite houses numbered sequentially.
Each elf is assigned a number and a progression.
Elf e visits houses eh. E.g.
    elf 1 visits 1, 2, 3, 4, 5, 6, 7, 8, 9 ...
    elf 2 visits    2     4     6     8    ...
    elf 3 visits       3        6        9 ...

At each house h, elf e delivers 10e presents.  Thus:
house 1 gets 10, house 2 gets 30, house 3 gets 40...

Solution:
    My approach seems inefficient.  It takes ~30s for both parts.
    I'm using a cache with my get_factors() function,
    since the 2nd part calcualtes mostly calculates the same factors.

Part 1:
    E.g. for house 6, we must determine all factors of 6.  Why?
    Because the factors are the elves that will visit this house.
    Thus, house 6 is visted by elves 1, 2, 3, and 6.
    
    Use a generator to get factors for next house.
    Use a map to multiply each factor by the per_elf number.

Part 2:
    Elves now have a limit on the number of houses they visit. (50.)
    So, we need to count the occurences of each factor (i.e. each elf visit).
    When each elf reaches its limit of visits, exclude this elf.
"""
import time
from collections import defaultdict
import logging
import aoc_common.aoc_commons as ac

locations = ac.get_locations(__file__)
logger = ac.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)

TARGET = 36000000
MAX_HOUSES_PER_ELF = 50

# TARGET = 200
# MAX_HOUSES_PER_ELF = 5

def main():

    # Part 1
    presents_dropped, house_num = 0, 0
    while presents_dropped < TARGET:
        house_num += 1
        presents_dropped = sum(factor * 10 for factor in ac.get_factors(house_num))   

    logger.info("Part 1: House=%d, presents dropped=%d", house_num, presents_dropped)
    
    # Part 2
    gen = generate_presents_for_house(11, MAX_HOUSES_PER_ELF)
    presents_dropped, house_num = 0, 0
    while presents_dropped < TARGET:
        house_num, presents_dropped = next(gen)
    
    logger.info("Part 2: House=%d, presents dropped=%d", house_num, presents_dropped)

def generate_presents_for_house(per_elf_multiplier: int, elf_visit_limit: int = 0):
    """ Generator function that returns the number of presents dropped at a given house.

    Yields:
        [tuple]: Current house number, total presents dropped at this house
    """
    house_num = 0
    elf_visits = defaultdict(int)

    while True: # iterate for each house, yielding each time
        house_num += 1
        presents_dropped = 0
        factors_for_house = ac.get_factors(house_num)
        
        # iterate through all the factors for this house
        for factor in factors_for_house:
            if elf_visit_limit and elf_visits[factor] >= elf_visit_limit:
                pass
            else:
                elf_visits[factor] += 1
                presents_dropped += factor * per_elf_multiplier
      
        if logger.isEnabledFor(logging.DEBUG): # avoid expensive sorting
            logger.debug("House %d visited by: %s", house_num, sorted(factors_for_house))
            logger.debug("Presents dropped: %d", presents_dropped)
        
            # convert defaultdict to dict so we don't print out the default factory information
            logger.debug("Factors counter: %s", dict(elf_visits)) 
        
        yield house_num, presents_dropped

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
