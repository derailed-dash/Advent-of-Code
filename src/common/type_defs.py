""" A set of reusable classes and attributes used by my AoC solutions """
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    """ Class for storing a point x,y coordinate """
    x: int
    y: int
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

class Vector(Point):
    """ Same as a Point class. But more intuitive to treat deltas as vectors than points. """

ARROW_VECTORS = {
    '^': Vector(0, 1),
    '>': Vector(1, 0),
    'v': Vector(0, -1),
    '<': Vector(-1, 0)
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
