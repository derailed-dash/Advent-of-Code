"""
Author: Darren
Date: 05/12/2021

Solving https://adventofcode.com/2021/day/5

Hydrothermal vent lines are given in the format x1,y1 -> x2,y2.
They are lines rather than rectangles.

This solution uses numpy to represent the 2D grid, with each point set to 0.
We then use numpy slicing to pass in lines, 
incrementing the values of each grid point that matches a line.

Part 1:
    Map out the number of hydrothermal vents at each location.
    Count how many locations have 2 or more vents.
    
    Use a dataclass to store x1, y1, x2, y2 coords of each line,
    with helper methods for things like max_x, for checking if horiz/vert/diag.
    Initialise a numpy array to 0s.
    Determine the overall grid size by finding the max x and y for all lines.
    Then iterate through the lines and increment the array at matching points.
    Only include vert/horiz lines.

Part 2:
    Now add diagonal lines.
    The trick here is know whether a line slopes down or up at 45 degrees, 
    which we can do by checking if x2-x2 == y2-y2.  If it slopes up, the sign will be inverted.
"""
import logging
import os
import time
import re
from dataclasses import dataclass
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

@dataclass
class Line:
    """ A vertical, horizontal or diagonal line. """
    x1: int
    y1: int
    x2: int
    y2: int
    
    @property
    def is_orthogonal(self) -> bool:
        """ I.e. whether horizontal or vertical line.
        If both x are the same, then horizontal.
        If both y are the same, then vertical. """
        return self.x1 == self.x2 or self.y1 == self.y2

    @property
    def diagonal_down(self) -> bool:
        """ Determine if the diagonal line increases in both x and y axes.
        If it increases in one axis but decreases in the other, then it slopes up. """
        assert not self.is_orthogonal, "Must be diagonal"
        return self.x1 - self.x2 == self.y1 - self.y2

    @property    
    def min_x(self) -> int:
        return min(self.x1, self.x2) 
    
    @property
    def min_y(self) -> int:
        return min(self.y1, self.y2)

    @property
    def max_x(self) -> int:
        return max(self.x1, self.x2)

    @property
    def max_y(self) -> int:
        return max(self.y1, self.y2)
    
def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
        
    vents = process_data(data)
    logger.debug("\n%s", "\n".join(str(vent) for vent in vents))
    
    # Get the bottom right coordinate of our x,y field
    max_x = max(vents, key=lambda line: line.max_x).max_x
    max_y = max(vents, key=lambda line: line.max_y).max_y

    field = np.zeros(shape=(max_y+1, max_x+1), dtype=np.int8)   # Initialise field(y, x)
    
    # Part 1: Count how many vents there are at each location, 
    # counting only horizontal and vertical vent lines
    for line in vents:
        if line.is_orthogonal:
            field[line.min_y:line.max_y+1, line.min_x:line.max_x+1] += 1
    
    logger.debug("\n%s", field)
    
    dangerous_vents = np.count_nonzero(field >= 2)
    logger.info("Part 1 dangerous vents: %d", dangerous_vents)
    
    # Part 2: Now add diagonal vent lines
    for line in vents:
        if not line.is_orthogonal: # diagonal
            for i in range(line.max_y-line.min_y+1):    # length of the line (x len = y len)
                if line.diagonal_down:
                    field[line.min_y+i, line.min_x+i] += 1
                else:   # diagonal up
                    field[line.max_y-i, line.min_x+i] += 1
    
    dangerous_vents = (field >= 2).sum()    # alternative to count_nonzero
    logger.info("Part 2 dangerous vents: %d", dangerous_vents)     
        
def process_data(data: list[str]) -> list[Line]:
    """ Parse data of format x1,y1 -> x2,y2 """
    lines = []
    for line in data:
        # get non-overlapping matching groups
        x1, y1, x2, y2 = map(int, re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", line)[0])
        lines.append(Line(x1, y1, x2, y2))
            
    return lines

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
