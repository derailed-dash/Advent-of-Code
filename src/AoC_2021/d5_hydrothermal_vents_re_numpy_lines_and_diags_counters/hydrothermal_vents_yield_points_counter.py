"""
Author: Darren
Date: 05/12/2021

Solving https://adventofcode.com/2021/day/5

Hydrothermal vent lines are given in the format x1,y1 -> x2,y2.
They are lines rather than rectangles.

Part 1:
    Map out the number of hydrothermal vents at each location.
    Count how many locations have 2 or more vents.
    
    Use a NamedTuple to represent a Point (x,y).
    Use a dataclass to store p1, p2 Points of each Line.
    Line knows how to yield all the points from p1 to p2.
    For each line, yield every point.  Store a Counter for all points.
    Then use the Counter to determine how many counts are >= 2.

Part 2:
    Now add diagonal lines.
    The same as Part 1, but we no longer include the orthogonal check.
"""
from collections import Counter
import logging
import os
import time
import re
from dataclasses import dataclass
from typing import Iterator, NamedTuple

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

class Point(NamedTuple):
    x: int
    y: int

@dataclass
class Line:
    """ A vertical, horizontal or diagonal line. 
    Able to yield all points between p1 and p2, inclusive. """
    p1: Point
    p2: Point
    
    @property
    def is_orthogonal(self) -> bool:
        """ I.e. whether horizontal or vertical line.
        If both x are the same, then horizontal.
        If both y are the same, then vertical. """
        return self.p1.x == self.p2.x or self.p1.y == self.p2.y

    @property
    def diagonal_down(self) -> bool:
        """ Determine if the diagonal line increases in both x and y axes.
        If it increases in one axis but decreases in the other, then it slopes up. """
        assert not self.is_orthogonal, "Must be diagonal"
        return self.p1.x - self.p2.x == self.p1.y - self.p2.y
    
    def points(self) -> Iterator[Point]:
        """ Yield every point from the start of the line (p1) to the end of the line (p2). """
        dx = 0 if self.p2.x == self.p1.x else 1 if self.p2.x > self.p1.x else -1
        dy = 0 if self.p2.y == self.p1.y else 1 if self.p2.y > self.p1.y else -1
        
        point = self.p1
        while point != self.p2:
            yield point
            point = Point(point.x + dx, point.y + dy)
            
        assert point == self.p2
        yield point # the end point
        
def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
        
    vents = process_data(data)
    
    # Part 1: Count how many vents there are at each location
    vents_counter = Counter()
    for line in vents:
        if line.is_orthogonal:  # only include orthogonal lines
            for point in line.points():
                vents_counter[point] += 1
    
    dangerous_vents = sum(1 for point, count in vents_counter.items() if count >= 2)
    logger.info("Part 1 dangerous vents: %d", dangerous_vents)
    
    # Part 2
    vents_counter = Counter()    
    for line in vents:
        for point in line.points():
            vents_counter[point] += 1
    
    dangerous_vents = sum(1 for point, count in vents_counter.items() if count >= 2)            
    logger.info("Part 2 dangerous vents: %d", dangerous_vents)     
        
def process_data(data: list[str]) -> list[Line]:
    """ Parse data of format x1,y1 -> x2,y2 """
    lines = []
    for line in data:
        # get non-overlapping matching groups
        x1, y1, x2, y2 = map(int, re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", line)[0])
        lines.append(Line(Point(x1, y1), Point(x2, y2)))
            
    return lines

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
