"""
Author: Darren
Date: 04/12/2021

Solving https://adventofcode.com/2021/day/4

We're playing bingo with a squid!
We're supplied with a list of numbers to read, and some 5x5 bingo cards, e.g.
    22 13 17 11  0
     8    23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

Part 1:
    Objective: 
    - Find the card that wins. 
    - Get the sum of all unmarked numbers on that card
      and multiply by the number just drawn.
    
    Store the card numbers in a 3D numpy array, of dimensions (n, 5, 5).
    Create a boolean array with the same shape, initialised to False.
    Draw each number.  Finding all matching positions in the bool ndarray and update to True.
    Iterate through each card.  
    Look for any row or col where all positions are True, using all(axis=n).
    When we find such a card, we've won.

Part 2:
    Now we want the squid to win.  So we want to find out which card would win last and select it.
    Same as part 1, but now repeat for each card that hasn't yet won, until no more cards left.
"""
import logging
import os
import time
from collections import deque
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()
    
    draw_numbers, bingo_cards = process_data(data)
    
    # Create a boolean np array of the same shape as bingo_cards, all False
    # E.g. with 100 bingo cards, the shape would be (100, 5, 5)
    card_completion: np.ndarray = np.full(bingo_cards.shape, False)
    
    cards_winning = set()   # store each card that has won so far (just store the position ints)
    
    # draw numbers until all cards have won
    while draw_numbers and len(cards_winning) < len(bingo_cards):
        num_drawn = draw_numbers.popleft()
        
        # find all locations on the card where we've matched THIS number
        # create a new np (bool) array accordingly
        where_true: np.ndarray = (bingo_cards == num_drawn) # where_true has same shape as cards
        card_completion |= where_true   # update card completion array
        
        # Now determine which cards have won at this point
        # Iterate through our boolean versions of each bingo card
        for i, card in enumerate(card_completion):
            if i in cards_winning:
                continue    # this card has already won; skip it
            
            cols_complete = np.all(card, axis=0) # array of AND(cols), e.g. [True, False, False, True, True]
            rows_complete = np.all(card, axis=1) # array of AND(rows)
            
            if any(cols_complete) or any(rows_complete):  # We got one!!
                cards_winning.add(i)
                
                # We're only interested in the first and last card that win...
                if len(cards_winning) == 1 or len(cards_winning) == len(bingo_cards):
                    part_num = 1 if len(cards_winning) == 1 else 2
                    logger.info("Part %d:", part_num)
                    logger.info("Last number drawn: %d", num_drawn)
                    
                    # Find all nums in this card where the card completion state is False
                    card_unmarked_nums = bingo_cards[i][~card]
                    sum_unmarked_nums = sum(card_unmarked_nums)
                    logger.info("Sum of remaining: %d", sum(card_unmarked_nums))
                    logger.info("Product=%d\n", num_drawn*sum_unmarked_nums)

def process_data(data: str) -> tuple[deque, np.ndarray]:
    """ Takes raw str data. Converts first line to a list of int.
    Converts remaining blocks into a 3D Numpy array. """
    # get the first line
    draw_numbers = deque(map(int, data.partition('\n')[0].split(",")))
    
    # Get list of cards, where each card is a list of 5 rows, 
    # which each row being a list of 5 ints
    # E.g. one card = [[66, 78, 7, 45, 92], [39, 38, 62, 81, 77], [...], [...], [...]]
    bingo_cards = [[list(map(int, row.split())) for row in card.splitlines()] 
                    for card in data.split('\n\n')[1:]]
    
    return draw_numbers, np.array(bingo_cards)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
