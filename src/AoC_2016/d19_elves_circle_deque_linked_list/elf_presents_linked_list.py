"""
Author: Darren
Date: 12/09/2021

Solving https://adventofcode.com/2016/day/19

Solution #5. Uses a home-made LinkedList.  Takes a few seconds.  Not bad.

Part 1:
    Performance = O(n).
    Use a linked list.  Wrap each elf with a linked list node, that knows prev and next.
    Join up the two ends to make circular.
    Now, we can simply keep moving to 'next' without ever worrying about what happens
    when we reach the 'end' of the circle.
    Unlink every other elf, until only one remains.

Part 2:
    Hurrah!  Performance = O(n).
    Under 6s for final solution.
    
    The trick here is to initially establish the opposite elf, and then to realise
    that the opposite elf jumps alternately by one and two, as we remove elves from the circle.
    With each move, we unlink the opposite elf, 
    then move the opposite elf 1 or 2, alternating.    
"""
import logging
import os
import time
from linked_lists import LinkedListNode

SCRIPT_DIR = os.path.dirname(__file__) 
# NUMBER_OF_ELVES = 30000
NUMBER_OF_ELVES = 3012210

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")

    # Part 1
    elves = range(1, NUMBER_OF_ELVES+1)
    linked_elves = list(map(LinkedListNode, elves))
    
    # Establish a linked list
    for i, _ in enumerate(linked_elves):
        if i < (len(linked_elves) - 1):
            linked_elves[i].next = linked_elves[i+1]
            linked_elves[i+1].prev = linked_elves[i]
        else:   # join up the ends to make circular linked list
            linked_elves[i].next = linked_elves[0]
            linked_elves[0].prev = linked_elves[i]
    
    counter = 0
    elves_counter = NUMBER_OF_ELVES
    current_linked_elf = linked_elves[counter]      # start
    while elves_counter > 1:
        if counter % 2 == 1:    # we want to remove (unlink) every other elf
            current_linked_elf.unlink()
            elves_counter -= 1
        
        current_linked_elf = current_linked_elf.next
        counter += 1

    logging.info(f"Part 1: Winning elf is {current_linked_elf.value}")
    
    # Part 2
    linked_elves = list(map(LinkedListNode, elves))
    
    # One again, establish circular linked list
    for i, _ in enumerate(linked_elves):
        if i < (len(linked_elves) - 1):
            linked_elves[i].next = linked_elves[i+1]
            linked_elves[i+1].prev = linked_elves[i]
        else:
            linked_elves[i].next = linked_elves[0]
            linked_elves[0].prev = linked_elves[i]
    
    counter = 0
    elves_counter = NUMBER_OF_ELVES
    current_linked_elf = linked_elves[counter]
    opposite_linked_elf = linked_elves[NUMBER_OF_ELVES // 2]    # Identify opposite elf
    while elves_counter > 1:
        opposite_linked_elf.unlink()        # unlink this elf
        elves_counter -= 1
        
        # the opposite index increases alternately by 1 and 2, 
        # as we proceed around the circle. 
        # This is due to how //2 works as the circle decreases. 
        opposite_linked_elf = opposite_linked_elf.next
        if counter % 2 != 0:
            opposite_linked_elf = opposite_linked_elf.next
        
        current_linked_elf = current_linked_elf.next
        counter += 1
        
    logging.info(f"Part 2: Winning elf is {current_linked_elf.value}")    
       

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
