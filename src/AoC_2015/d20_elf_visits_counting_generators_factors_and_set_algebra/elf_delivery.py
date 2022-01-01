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

At each house h, elf e delivers 10x presents.  Thus:
house 1 gets 10, house 2 gets 30, house 3 gets 40...

Solution:
    My approach seems inefficient.  It takes ~30s for both parts.

Part 1:
    E.g. for house 6, we must determine all factors of 6.  Why?
    Because the factors are the elves that will visit this house.
    Thus, house 6 is visted by elves 1, 2, 3, and 6.
    
    Use a generator to get factors for next house.
    Use a map to multiply each factor by the per_elf number.

Part 2:
    Elves now have a limit on the number of houses they visit. (50.)
    So, we need to count the occurences of each factor (i.e. each elf visit).
    When each elf reaches its limit of visits, add them to an exclude list.
    Use set difference to remove these from factors returned.
    (Having the exclude list as a set rather than a list is MUCH faster!)
"""
import os
import time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

TARGET = 36000000
MAX_HOUSES_PER_ELF = 50

def main():

    # Part 1
    gen = generate_presents_for_house(10)
    presents_dropped = 0
    house = 0
    while presents_dropped < TARGET:
        house, presents_dropped = next(gen)

    print(f"Part 1: House {house} = {presents_dropped}")
    
    # Part 2
    gen = generate_presents_for_house(11, MAX_HOUSES_PER_ELF)
    presents_dropped = 0
    house = 0
    while presents_dropped < TARGET:
        house, presents_dropped = next(gen)
    
    print(f"Part 2: House {house} = {presents_dropped}")


def generate_presents_for_house(per_elf_multiplier: int, elf_visit_limit: int = 0):
    """ 
    Generator function that returns the number of presents dropped at a given house.
    Each elf drops a certain number of presents at each house

    Args:
        per_elf_multiplier (int): Elves drop e*q presents per house, where e is elf number and q is the multiplier

    Yields:
        [tuple]: Current house number, total presents dropped at this house
    """
    house_num = 1
    factors_for_house = set()
    factors_counter = defaultdict(int)
    factors_to_exclude = set()

    while True:
        factors_for_house = get_factors(house_num)
        factors_for_house.difference_update(factors_to_exclude)

        for factor in factors_for_house:
            factors_counter[factor] += 1

            # if an elf has reached the limit, it won't do any more drops
            if elf_visit_limit and factors_counter[factor] >= elf_visit_limit:
                factors_to_exclude.add(factor)

        presents_dropped = sum(map(lambda x: (x * per_elf_multiplier), factors_for_house))
        
        # print(f"House {house_num} visited by: {factors_for_house[house_num]}")
        # print(f"Presents dropped: {presents_dropped}")
        # print(f"Factors counter: {factors_counter}")
        
        yield house_num, presents_dropped
        house_num += 1


def get_factors(num: int) -> set[int]:
    """ 
    Gets the factors for a given house number.
    Here, this determines the elves that visit each house.

    Args:
        num (int): the house number we want to get factors for

    Returns:
        set[int]: The set of factors (which represent elf numbers)
    """
    factors = set()

    # E.g. factors of 8 = 1, 2, 4, 8
    # Iterate from 1 to sqrt of 8, where %=0, i.e. 1 and 2
    # E.g. for i=1, we add factors 1 and 8
    #      for i=2, we add factors 2 and 4
    # Use a set to eliminate duplicates, e.g. if i is 4, we only want one 2
    for i in range(1, (int(num**0.5) + 1)):
        if num%i == 0:
            factors.add(i)
            factors.add(num//i)
    
    return factors


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
