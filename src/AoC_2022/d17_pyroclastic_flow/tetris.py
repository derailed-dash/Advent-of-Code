"""
Author: Darren
Date: 17/12/2022

Solving https://adventofcode.com/2022/day/17

Rocks are falling.  And they resemble tetris pieces! They always fall in this order:
-, +, backwards Lâ, |, ■.
Probably a mod problem!

Chamber is 7 units wide.  Rocks start to fall from:
- left edge 2 units from left wall
- bottom edge 3 units above highest rock in the room, or the floor.

Input is horizontal movement of the falling objects,
as a result of jets of gasses from the sides.  E.g.
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>

This pattern also repeats indefinitely.

Rocks are pushed 1 unit, then fall one unit. 
The rock comes to rest in the fall step AFTER it reaches its lowest point.
Then another rock starts to fall.

Part 1:

How many units tall will the tower of rocks be after 2022 rocks have stopped falling?

Part 2:

"""
from dataclasses import dataclass
import itertools
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
OUTPUT_FILE = Path(SCRIPT_DIR, "output/output.png")

SHAPES = {
    "HLINE":  {(0, 0), (1, 0), (2, 0), (3, 0)},
    "PLUS": {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    "BACKWARDS_L": {(0, 0),(1, 0),(2, 0),(2, 1),(2, 2)},
    "I": {(0, 0), (0, 1), (0, 2), (0, 3)},
    "SQUARE": {(0, 0), (1, 0), (0, 1), (1, 1)}
}

@dataclass(frozen=True)
class Point():
    x: int
    y: int
    
    def __repr__(self) -> str:
        return f"P({self.x},{self.y})"
    
class Shape():
    """ Stores the points that make up this shape. 
    Has a factory method to create Shape instances based on shape type. """
    
    def __init__(self, shape_type: str, points: set[Point]) -> None:
        self.type = shape_type
        self.points = points   # the points that make up the shape
        
    def bottom_left(self) -> Point:
        """ Return the logical bottom left of this shape. The BL could be empty """
        left_x = min(point.x for point in self.points)
        bottom_y = max(point.y for point in self.points) # remember, y will decrease going up
        return Point(left_x, bottom_y)
    
    def top(self) -> int:
        return min(point.y for point in self.points)
    
    @classmethod
    def create_shape(cls, shape_type: str):
        """ Factory method to create an instance of our shape """
        return cls(shape_type, {Point(*coord) for coord in SHAPES[shape_type]})
    
    def __repr__(self) -> str:
        return f"Shape(type={self.type}, points={self.points}"

class Tower():
    WIDTH = 7
    FALLING = "@"
    AT_REST = "#"
    EMPTY = "."
    
    def __init__(self, jet_pattern: str) -> None:
        self._jet_pattern = itertools.cycle(jet_pattern)
        self._shape_generator = itertools.cycle(SHAPES)
        self.shape_count = 0
        self.shape_falling = False
        self.current_shape = None
    
    def _next_shape(self):
        """ Get the next shape from the generator """
        return next(self._shape_generator)
    
    def _next_jet(self):
        """ Get the next jet blast from the generator """
        return next(self._jet_pattern)
    
    def drop_shape(self):
        if not self.shape_falling:
            self.current_shape = Shape.create_shape(self._next_shape())
            print(f"Added {self.current_shape}")
            
            self.shape_falling = True
    
    def __str__(self) -> str:
        pass

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()
        
    print(data)
    
    tower = Tower(jet_pattern=data)
    for _ in range(3):
        tower.drop_shape()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
