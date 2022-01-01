"""
Author: Darren
Date: 10/09/2021

Solving https://adventofcode.com/2016/day/19

Solution 1. After tweaking, this is now the best solution (but is basically the same as #6).
Uses a deque since deques are effectively linked lists with efficient popping.

Part 1:
    Elves sat in a circle.  Each elf brings 1 present.
    Start at elf 1, each elf steals all the presents from the elf to their left (CW).
    Remove elves that have no presents.
    Stop when one elf has all the presents.
    
    Implement using a deque, since this allows us to efficiently pop "empty" elves
    and supports a rotate method in order to replicate the circular group of elves.
    This way, we don't have to mess about with what happens when we reach the ends.
    Simply start with elf 1, take from elf 2, pop elf 2, 
    then rotate left such that elf 2 is now at the beginning.
    Rinse and repeat until only 1 elf left.
    
    Takes < 2s.
    t(n) = O(n), i.e. linear performance.

Part 2:
    Now elves steal from elves that are opposite, rather than right.
    If two elves are opposite, steal from the nearest of the two.
    Use integer division to determine who is opposite.
    We now need to pop the elf that is opposite.
    Inefficient to use remove() since this is a search of the whole deque.
    Instead, rotate to the position opposite, popleft().
    
    My original implementation rotated to opposite, popped opposite, 
    then rotated back to 'current' taker, but one fewer, i.e. to end up on the elf to the right.
    Then recalculate where opposite is (based on smaller circle) and repeat.
    
    This was pretty slow:  t(n) = O(n**2), i.e. exponential.
    Ended up taking 2 hours for the final solution!
    
    I changed it so that there's no rotate back.  
    We continue to calculate the shrinking circle, 
    and use the new 'half' circle size to determine how many additional rotations are required.
    It turns out that after popping 'opposite', the new opposite is either at the same position, 
    or we need to rotate one extra move.
    
    Rinse and repeat until only 1 elf left.

    This performs really well!  t(n) = O(n).  Whole program in <2s.
"""
import logging
import os
import time
from collections import deque

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

# NUMBER_OF_ELVES = 10000
NUMBER_OF_ELVES = 3012210

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")

    # Part 1    
    
    # deques are really efficient for popping at either end.
    # And we can easily rotate the deck so our 'current' taker is at position 0.
    # Very useful for replicating behaviour in a circle.
    elves = deque()     
    for elf_num in range(1, NUMBER_OF_ELVES+1):
        elves.append([elf_num, 1])  # Initialise all our elves to 1 present
        
    while len(elves) > 1:           # Loop until only one elf left
        elves[0][1] = elves[0][1] + elves[1][1]     # Elf takes all presents from elf on the right
        elves[1][1] = 0     # Set elf on right to 0 presents.
        elves.rotate(-1)    # Rotate left.  So the elf that was on the right is now first elf
        elves.popleft()     # Pop the elf on the left, since they have 0 presents
        
    logging.info(f"Part 1: Winning elf is {elves[0][0]}")
    
    # Part 2
    
    # I now know that we don't care how many presents are taken by each elf.
    # We only care whether elves are retained or kicked from the circle.
    # Thus, no need to go moving these quantities about.
    elves = deque(range(1, NUMBER_OF_ELVES+1))

    elf_opposite = len(elves) // 2    # determine which elf is opposite the current taker   
    elves.rotate(-elf_opposite)    # Rotate until we reach the elf that will be stolen from
    while len(elves) > 1:           # Loop until only one elf left
        elves.popleft()     # Pop this 'opposite' elf, since they have 0 presents
        old_elf_opposite = elf_opposite
        elf_opposite = len(elves) // 2    
        rotate_amount = old_elf_opposite - elf_opposite     
        
        # Replicate rotating back to (where we were-1), then rotating forward the new half size of circle
        elves.rotate(rotate_amount-1)

    logging.info(f"Part 2: Winning elf is {elves[0]}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
