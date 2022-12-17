"""
Author: Darren
Date: 17/12/2022

Solving https://adventofcode.com/2022/day/17

Rocks are falling.  And they resemble tetris pieces! They always fall in this order:
-, +, backwards Lâ, |, ■.

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
    "HLINE":       {(0, 0), (1, 0), (2, 0), (3, 0)},
    "PLUS":        {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    "BACKWARDS_L": {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    "I":           {(0, 0), (0, 1), (0, 2), (0, 3)},
    "SQUARE":      {(0, 0), (1, 0), (0, 1), (1, 1)}
}

MOVE = {
    "<": (-1, 0),
    ">": (1, 0),
    "V": (0, -1)
}

@dataclass(frozen=True)
class Point():
    x: int
    y: int
    
    def __add__(self, other):
        """ Add other point/vector to this point, returning new point """
        return Point(self.x + other.x, self.y + other.y)     
    
    def __repr__(self) -> str:
        return f"P({self.x},{self.y})"
    
class Shape():
    """ Stores the points that make up this shape. 
    Has a factory method to create Shape instances based on shape type. """
    
    def __init__(self, points: set[Point], at_rest=False) -> None:
        self.points = points   # the points that make up the shape
        self.at_rest = at_rest
    
    @classmethod
    def create_shape_by_type(cls, shape_type: str, origin: Point):
        """ Factory method to create an instance of our shape.
        The shape points are offset by the supplied origin. """
        return cls({(Point(*coords) + origin) for coords in SHAPES[shape_type]})

    @classmethod
    def create_shape_from_points(cls, points: set[Point], at_rest=False):
        """ Factory method to create an instance of our shape.
        The shape points are offset by the supplied origin. """
        return cls(points, at_rest)
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Shape):
            if self.points == __o.points:
                return True
        else:
            return NotImplemented  
    
    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return f"Shape(at_rest={self.at_rest}, points={self.points}"
    
class Tower():
    WIDTH = 7
    LEFT_WALL_X = 0  # left wall at x=0
    RIGHT_WALL_X = LEFT_WALL_X + 7 + 1  # right wall at x=8
    OFFSET_X = 2 + 1  # objects start with left edge at x=3
    OFFSET_Y = 3 + 1
    FLOOR_Y = 0
    
    FALLING = "@"
    AT_REST = "#"
    EMPTY = "."
    WALL = "|"
    FLOOR = "-"
    
    def __init__(self, jet_pattern: str) -> None:
        self._jet_pattern = itertools.cycle(jet_pattern)
        self._shape_generator = itertools.cycle(SHAPES)
        self._highest_floor = Tower.FLOOR_Y
        self._all_at_rest_shapes: set[Shape] = set()
    
    def _x_origin(self):
        return Tower.LEFT_WALL_X + Tower.OFFSET_X
    
    def _y_origin(self):
        return self._highest_floor + Tower.OFFSET_Y
    
    def _next_shape(self):
        """ Get the next shape from the generator """
        return next(self._shape_generator)
    
    def _next_jet(self):
        """ Get the next jet blast from the generator """
        return next(self._jet_pattern)
    
    def drop_shape(self):
        self.current_shape = Shape.create_shape_by_type(
                self._next_shape(), Point(self._x_origin(), self._y_origin()))
        print(self)
            
        self.shape_falling = True
        while True:
            self._move_shape(self._next_jet())
            print(self)
            if not self._move_shape("V"):
                self._highest_floor = max(point.y for point in self.current_shape.points)
                settled_shape = Shape.create_shape_from_points(self.current_shape.points, True)
                self._all_at_rest_shapes.add(settled_shape)
                break
    
    def _move_shape(self, direction) -> bool:
        """ Move a shape in the direction indicated. 
        Return False if we can't move. """
        if direction == "<":
            shape_left_x = min(point.x for point in self.current_shape.points)
            if shape_left_x == Tower.LEFT_WALL_X + 1:
                return False # can't move left
            
        if direction == ">":
            shape_right_x = max(point.x for point in self.current_shape.points)
            if shape_right_x == Tower.RIGHT_WALL_X - 1:
                return False # can't move right
            
        if direction == "V":
            shape_bottom = min(point.y for point in self.current_shape.points)
            if shape_bottom == Tower.FLOOR_Y + 1:
                return False # can't move down
        
        # Move the shape; construct a new shape from the new Points
        candidate_points = {(point + Point(*MOVE[direction])) for point in self.current_shape.points}
        if self._get_at_rest_points() & candidate_points: # If the candidate would intersect
            return False # Then this is not a valid posiiton
        else: # We can move there. Update our current shape position.
            self.current_shape = Shape.create_shape_from_points(candidate_points)
        return True
                    
    def _get_at_rest_points(self) -> set[Point]:
        """ Get all the points from all the at_rest shapes """
        points = set()
        for shape in self._all_at_rest_shapes:
            points |= shape.points
        return points 
    
    def __str__(self) -> str:
        rows = []
        all_at_rest_shapes_points = self._get_at_rest_points()
            
        for y in range(Tower.FLOOR_Y, self.height() + 1):
            line = ""
            if y == Tower.FLOOR_Y:
                line += "+" + (Tower.FLOOR * Tower.WIDTH) + "+"
            else:            
                for x in range(Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X + 1):
                    if x in (Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X):
                        line += Tower.WALL
                    elif Point(x,y) in all_at_rest_shapes_points:
                        line += Tower.AT_REST
                    elif Point(x,y) in self.current_shape.points:
                        line += Tower.FALLING
                    else:
                        line += Tower.EMPTY
                    
            rows.append(line)
        
        return f"{repr(self)}\n" + "\n".join(rows[::-1]) 

    def height(self) -> int:
        points = self._get_at_rest_points() | self.current_shape.points
        return max(point.y for point in points)
    
    def __repr__(self) -> str:
        return (f"Tower(height={self.height()}, rested={len(self._all_at_rest_shapes)})")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()
        
    print(data)
    
    tower = Tower(jet_pattern=data)
    for _ in range(15):
        tower.drop_shape()
    
    print(f"Part 1: {repr(tower)}")

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
