""" A set of reusable classes and attributes used by my AoC solutions """
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Point:
    """ Class for storing a point x,y coordinate """
    x: int
    y: int
        
    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)
    
    def __mul__(self, val):
        return Point(self.x * val, self.y * val)
    
    def __sub__(self, other: Point):
        return self + (other*-1)

    def yield_neighbours(self, include_diagonals=True, include_self=False):
        """ Generator to yield neighbouring Points """
        
        deltas: set
        if not include_diagonals:
            deltas = {vector.value for vector in Vectors if abs(vector.value[0]) != abs(vector.value[1])}
        else:
            deltas = {vector.value for vector in Vectors}
        
        if include_self:
            deltas.add((0, 0))
        
        for delta in deltas:
            yield Point(self.x + delta[0], self.y + delta[1])

    def neighbours(self, include_diagonals=True, include_self=False):
        """ Return all the neighbours, with specified constraints """
        return set(self.yield_neighbours(include_diagonals, include_self))
    
    def get_specific_neighbours(self, directions: list[Vectors]) -> set[Point]:
        """ Get neighbours, given a specific list of allowed locations """
        return {(self + Point(*vector.value)) for vector in list(directions)}
    
    def __repr__(self):
        return f"P({self.x},{self.y})"

class Vectors(Enum):
    """ Enumeration of 8 directions, and a rotating list of direction choices.
    Note: y axis increments in the South direction. """
    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    SE = (1, 1)
    S = (0, 1)
    SW = (-1, 1)
    W = (-1, 0)
    NW = (-1, -1)
    
ARROW_VECTORS = {
    '^': Vectors.N.value,
    '>': Vectors.E.value,
    'v': Vectors.S.value,
    '<': Vectors.W.value
}

DIRECTION_VECTORS = {
    'U': Vectors.N.value,
    'R': Vectors.E.value,
    'D': Vectors.S.value,
    'L': Vectors.W.value
}

NINE_BOX_VECTORS: dict[str, tuple[int, int]] = {
    # x, y vector for adjacent locations
    'tr': (1, 1),
    'mr': (1, 0),
    'br': (1, -1),
    'bm': (0, -1),
    'bl': (-1, -1),
    'ml': (-1, 0),
    'tl': (-1, 1),
    'tm': (0, 1)
}

class Grid():
    """ 2D grid of point values. """
    def __init__(self, grid_array: list) -> None:
        self._array = grid_array
        self._width = len(self._array[0])
        self._height = len(self._array)
        
    def value_at_point(self, point: Point) -> int:
        """ The value at this point """
        return self._array[point.y][point.x]

    def set_value_at_point(self, point: Point, value: int):
        self._array[point.y][point.x] = value
        
    def valid_location(self, point: Point) -> bool:
        """ Check if a location is within the grid """
        if (0 <= point.x < self._width and  0 <= point.y < self._height):
            return True
        
        return False

    @property
    def width(self):
        """ Array width (cols) """
        return self._width
    
    @property
    def height(self):
        """ Array height (rows) """
        return self._height
    
    def all_points(self) -> list[Point]:
        points = [Point(x, y) for x in range(self.width) for y in range(self.height)]
        return points

    def __repr__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._array)
