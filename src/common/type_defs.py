""" A set of reusable classes and attributes used by my AoC solutions """
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Point:
    """ Class for storing a point x,y coordinate """
    x: int
    y: int
        
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def neighbours(self, include_diagonals=True, include_self=False) -> set[Point]:
        """ Return neighbouring Points """

        if not include_diagonals:
            neighbours = {(self + Point(*vector.value)) for vector in Vectors
                                                        if abs(vector.value[0]) != abs(vector.value[1])}
        else:
            neighbours = {(self + Point(*vector.value)) for vector in Vectors}
        
        if include_self:
            neighbours.add(self)
            
        if not include_diagonals:
            neighbours.difference_update({point for point in neighbours if abs(point.x) == abs(point.y)})
        
        return neighbours
    
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
