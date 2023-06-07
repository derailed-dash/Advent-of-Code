""" 
Author: Darren
Date: 08/03/2021

Solving https://adventofcode.com/2015/day/18

We have a grid of lights.  They can be on or off.
With each iteration, we update whether lights are on or off, according to these rules:
    - A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    - A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.

Solution 3 of 3:
  - Solving with numpy.  This is faster than my previous solutions
"""
import os
import time
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

ITERATIONS = 100

def count_neighbors(grid, x, y):
    """ Count the _on_ neighbours around the light at coords (x, y). """
    min_x, max_x = max(0, x-1), min(grid.shape[0], x+2)
    min_y, max_y = max(0, y-1), min(grid.shape[1], y+2)
    return np.sum(grid[min_x:max_x, min_y:max_y]) - grid[x, y]

def update_grid(grid, ignore_corners=False):
    new_grid = grid.copy()
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if ignore_corners:
                if (x, y) in [(0, 0),
                              (0, grid.shape[1]-1),
                              (grid.shape[0]-1, 0), 
                              (grid.shape[0]-1, grid.shape[1]-1)]:
                    continue
            count = count_neighbors(grid, x, y)
            if grid[x, y] == 1 and count not in [2, 3]:
                new_grid[x, y] = 0
            elif grid[x, y] == 0 and count == 3:
                new_grid[x, y] = 1
                
    return new_grid

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # inport text as a numpy grid, setting each field to 1 char wide
    grid = np.genfromtxt(input_file, dtype='U1', comments=None, delimiter=1)
    grid[grid == '#'] = 1
    grid[grid == '.'] = 0
    grid = grid.astype(int)

    # Part 1
    p1_grid = grid.copy()
    for _ in range(100):
        p1_grid = update_grid(p1_grid)

    print(f"Part 1: {np.sum(p1_grid)}")
    
    # Part 2
    # Turn on corners
    for x, y in [(0, 0), 
                 (0, grid.shape[1]-1), 
                 (grid.shape[0]-1, 0), 
                 (grid.shape[0]-1, grid.shape[1]-1)]:
        grid[x, y] = 1
        
    for _ in range(100):
        grid = update_grid(grid, ignore_corners=True)
    
    print(f"Part 2: {np.sum(grid)}")
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
