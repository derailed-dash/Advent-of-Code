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

- Shape class:
  - Has a set of all the Points it occupies.
  - Factory methods to create each shape.
    Point coordinates are created with the appropriate starting position (offset).
  - Factory method to create a shape for a set of points (e.g. when we move a shape)
  - Is hashable, so we can store it in sets.

- Tower class:
  - Use itertools.cycle to infinitely iterate through the input jet pattern.
    We can always generate the next jet.
  - Use itertools.cycle to infinitely iterate through the shapes in order.
    We can always generate the next shape.
  - Stores all points for all at rest shapes (set).
  - Stores the current top of all the settled points.
  - Can determine origin for new shapes, using current top.
  - Simulates dropping a shape:
    - Creates the new shape at the appropriate origin.
    - Calls move with next jet.
    - Calls move with down. 
      If we can't move down, settles the shape by adding current shape to settled points.
  - To move a shape:
    - Check if we can move left, right or down based on bounds; return if we can't.
    - If bounds are okay, generate candidate points from current shape.
    - Check if candidate intersects with settled.  If so, we can't move there.
    - Otherwise, update current shape to be new shape from candidate points.

- Finally, call tower.drop_shape 2022 times.
    
Part 2:

How tall will the tower be after 1000000000000 rocks have stopped?

Part 1 achieves 1M drops / minute. So running Part 1 for this many drops would take 2 years!
We need a better solution. We need a repeating cycle. 

Look for a repeat of:
- Identical rock formation - try over 100 rows.
- Same dropped rock. (Enumerate the rocks.)
- Same index in the jets. (Enumerate the jet data.)

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
    """ Point with x,y coordinates and knows how to add a vector to create a new Point. """
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
        self.points: set[Point] = points   # the points that make up the shape
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
    LEFT_WALL_X = 0  
    RIGHT_WALL_X = LEFT_WALL_X + 7 + 1  # right wall at x=8
    OFFSET_X = 2 + 1  # objects start with left edge at x=3
    OFFSET_Y = 3 + 1  # new rocks have a gap of 3 above top of highest settled rock
    FLOOR_Y = 0
    
    # Printing characters
    FALLING = "@"
    AT_REST = "#"
    EMPTY = "."
    WALL = "|"
    FLOOR = "-"
    
    def __init__(self, jet_pattern: str) -> None:
        self._jet_pattern = itertools.cycle(enumerate(jet_pattern)) # infinite cycle
        self._shape_generator = itertools.cycle(enumerate(SHAPES))  # infinite cycle
        self.top = Tower.FLOOR_Y  # keep track of top of blocks
        self._all_at_rest_shapes: set[Shape] = set()
        self._all_at_rest_points: set[Point] = set() # tracking this for speed
    
    def _current_origin(self) -> Point:
        """ Rocks are dropped 2 from the left edge, and 3 above the current tallest settled rock. """
        return Point(Tower.LEFT_WALL_X + Tower.OFFSET_X, self.top + Tower.OFFSET_Y)
    
    def _next_shape(self):
        """ Get the next shape from the generator """
        return next(self._shape_generator)
    
    def _next_jet(self):
        """ Get the next jet blast from the generator """
        return next(self._jet_pattern)
    
    def drop_shape(self):
        shape_index, next_shape_type = self._next_shape()
        self.current_shape = Shape.create_shape_by_type(next_shape_type, self._current_origin())
            
        while True:
            jet_index, jet = self._next_jet()
            self._move_shape(jet)
            # print(self)
            if not self._move_shape("V"): # failed to move down
                self.top = max(self.top, max(point.y for point in self.current_shape.points))
                settled_shape = Shape.create_shape_from_points(self.current_shape.points, True)
                self._settle_shape(settled_shape)
                break
        
        # print(self)
    
    def _settle_shape(self, shape: Shape):
        """ Add this shape to the settled sets """
        self._all_at_rest_shapes.add(shape)
        self._all_at_rest_points.update(shape.points)
    
    def _move_shape(self, direction) -> bool:
        """ Move a shape in the direction indicated. Return False if we can't move. """
        
        # Test against boundaries
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
        
        # Move phase - test for collision
        candidate_points = {(point + Point(*MOVE[direction])) for point in self.current_shape.points}
        if self._all_at_rest_points & candidate_points: # If the candidate would intersect
            return False # Then this is not a valid posiiton
        else: # We can move there. Update our current shape position, by constructing a new shape a the new position
            self.current_shape = Shape.create_shape_from_points(candidate_points)
        return True
                    
    def __str__(self) -> str:
        rows = []
        top_for_vis = max(self.top, max(point.y for point in self.current_shape.points))
            
        for y in range(Tower.FLOOR_Y, top_for_vis + 1):
            line = f"{y:3d} "
            if y == Tower.FLOOR_Y:
                line += "+" + (Tower.FLOOR * Tower.WIDTH) + "+"
            else:            
                for x in range(Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X + 1):
                    if x in (Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X):
                        line += Tower.WALL
                    elif Point(x,y) in self._all_at_rest_points:
                        line += Tower.AT_REST
                    elif Point(x,y) in self.current_shape.points:
                        line += Tower.FALLING
                    else:
                        line += Tower.EMPTY
                    
            rows.append(line)
        
        return f"{repr(self)}:\n" + "\n".join(rows[::-1]) 

    def __repr__(self) -> str:
        return (f"Tower(height={self.top}, rested={len(self._all_at_rest_shapes)})")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()

    # Part 1        
    tower = Tower(jet_pattern=data)
    for _ in range(2022):
        tower.drop_shape()
    
    print(f"Part 1: {repr(tower)}")

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
