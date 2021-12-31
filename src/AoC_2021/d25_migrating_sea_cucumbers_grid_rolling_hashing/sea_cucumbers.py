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
    Use the hash of grid (which hashes tuples of the internal list of str)
    to compare each grid to the cycle before.

Part 2:
    No part 2 today! 
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class Grid():
    """ Store locations of sea cucumbers. """
   
    def __init__(self, data: list[str]) -> None:
        """ Take input data and convert from list-of-str to list-of-list for easier manipulation. """
        self._grid = [list(row) for row in data]    # Now a nested list of list.
        self._row_len = len(self._grid[0])
        self._grid_len = len(self._grid)
        self._changed_last_cycle = False
    
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
    
    def __hash__(self) -> int:
        """ To help us to uniquely identify grids. 
        Convert strings to tuples, so we can hash them. """
        grid_as_tuple = tuple(tuple(row) for row in self._grid)
        hash_val = hash(grid_as_tuple)
        return hash_val
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Grid):
            return self._grid == __o._grid
        else:
            return NotImplemented

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    logger.info("Updating using 'changed_last_cycle' in the grid class...")
    grid = Grid(data)
    i = 0
    t1 = time.perf_counter()
    while True:
        i += 1
        grid.cycle()
        if not grid.changed_last_cycle:
            logger.info("We've stopped changing at iteration %d", i)
            break

    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds\n", t2 - t1)    

    logger.info("Comparing hash values of each grid instance...")
    t1 = time.perf_counter()
    grid = Grid(data)
    i = 0
    last_hash = hash(grid)        
    while True:
        i += 1
        grid.cycle()
        new_hash = hash(grid)
        # print(f"Iteration {i}:\n{grid}\n")
        if last_hash == new_hash:
            logger.info("We've stopped changing at iteration %d", i)
            break  

        last_hash = new_hash
        
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)          

if __name__ == "__main__":
    main()
