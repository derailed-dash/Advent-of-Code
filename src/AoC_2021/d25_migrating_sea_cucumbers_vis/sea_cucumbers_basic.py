"""
Author: Darren
Date: 25/12/2021

Solving https://adventofcode.com/2021/day/25

Two herds of cucumbers.  One always moves east (>) and one always moves south (v).
Each step:
    1. Herd > attempts to move 1 step, all simultaneously
       E.g. ...>>>>.>.. becomes ...>>>.>.>.
    2. Herd v attempt to move 1 step, all simultaneously

Sea cucumbers that reach the edge wrap around to the other side!

Part 1:
    Keep iterating until the sea cucumbers stop moving.
    Use a Grid class that knows how to perform a migration cycle.
    Each cycle sets a flag if the grid has changed, 
    which can be interrogated to determine when to stop iterating.
    Because all cucumbers need to move simultaneously, 
    we'll make a copy of the grid before each migration. 

Part 2:
    No part 2 today! 
"""
import logging
import time
from pathlib import Path

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

class Grid():
    """ Store locations of sea cucumbers. """
   
    def __init__(self, data: list[str]) -> None:
        """ Take input data and convert from list-of-str to list-of-list for easier manipulation. """
        init_str = "Created Grid"
        logger.debug(init_str)
        
        self._grid = [list(row) for row in data]    # Now a nested list of list.
        self._row_len = len(self._grid[0])
        self._grid_len = len(self._grid)
        self._changed_last_cycle = True

    @property
    def changed_last_cycle(self):
        return self._changed_last_cycle

    def cycle(self):
        """ Performs a migration cycle for our east-moving and south-moving herds 
        Performs all east, and then performs all south. Then updates the grid. """
        self._changed_last_cycle = False
        
        # Make a copy of the grid.  Shallow copy won't work, as we have a nested list. Deepcopy is too slow.
        tmp_grid = [[self._grid[y][x] for x in range(self._row_len)] for y in range(self._grid_len)]
        
        # process east herd, row by row
        for y in range(self._grid_len):
            for x in range(self._row_len):
                next_x = (x+1)%self._row_len  # get right / wrap-around
                if self._grid[y][x] + self._grid[y][next_x] == ">.":
                    tmp_grid[y][x] = "."
                    tmp_grid[y][next_x] = ">"
                    self._changed_last_cycle = True
        
        self._grid = tmp_grid
        
        east_migrated = [[tmp_grid[y][x] for x in range(self._row_len)] for y in range(self._grid_len)]
                
        for y in range(self._grid_len):
            for x in range(self._row_len):
                next_y = (y+1)%self._grid_len  # get below / wrap-around
                if tmp_grid[y][x] + tmp_grid[next_y][x] == "v.":
                    east_migrated[y][x] = "."
                    east_migrated[next_y][x] = "v"
                    self._changed_last_cycle = True
        
        self._grid = east_migrated
        
    def __repr__(self) -> str:
        return "\n".join("".join(char for char in row) for row in self._grid)

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    grid = Grid(data)

    i = 0
    while grid.changed_last_cycle:
        i += 1
        grid.cycle()

    logger.info("We've stopped migrating at iteration %d", i)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds\n", t2 - t1)    
