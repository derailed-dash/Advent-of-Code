"""
Author: Darren
Date: 24/12/2022

Solving https://adventofcode.com/2022/day/24

We have a map of ground, with walls and blizzards.
Blizzards move simultaneously, and wrap around.
We move simultaneously with blizzards. We can move or wait.

Part 1:

What is the fewest number of minutes required to avoid the blizzards and reach the goal?

Soln:
- Create a MapState.
- There are no v or ^ blizzards in the cols with openings, so we can ignore this case.
- Stores all blizzards at a given location. Because there can be more than one blizzard.  Thus dict of {Point: {blizzards}}
- MapState able to yield next MapState by moving all blizzards.
- Now A* through the map. Use Manhattan distance for the heuristic.

Part 2:

"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

@dataclass(frozen=True)
class Point():
    """ Point x,y which knows how to add another point, 
    and how to return all adjacent points, including diagonals. """
    x: int
    y: int

    def __add__(self, other) -> Point:
        """ Subtract other point from this point, returning new point vector """
        return Point(self.x + other.x, self.y + other.y)
    
    def adjacent_points(self) -> set[Point]:
        return set(self+vector for vector in VECTORS.values())
    
    def distance_to(self, other: Point) -> int:
        """ Manhattan distance between points """
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def __repr__(self):
        return f"P({self.x},{self.y})"

class MapState():    
    def __init__(self, grid_dims: tuple, locations: dict, me_locn: Point) -> None:
        self._map_locs: dict[Point, set] = locations # { point: { blizzards } }  Can contain a blizzard or a wall
        self._width, self._height = grid_dims
        self._me = me_locn
        self._goal = Point(self._width-2, self._height-1)

    def next_blizzard_state(self) -> MapState:
        """ Move blizzards to achieve next blizzard state.  There is only one possible next blizzard state """
        new_blizzard_locs = defaultdict(set)
        row_width = self._width - 2 # ignore walls
        col_height = self._height - 2 # ignore walls
        
        for y in range(1, self._height):
            for x in range(1, self._width):
                curr_locn = Point(x,y)
                if curr_locn in self._map_locs: # go through all locations that contain something
                    for map_locn, contained in self._map_locs.items():
                        for item in contained: # it could be a '#', or one-or-many blizzards
                            # Because our grid area excludes row 0 and col 0, subtract 1 from these coords
                            x = (map_locn.x-1)
                            y = (map_locn.y-1)
                            if item is not '#':
                                # For blizzard, find next position by adding blizzard vector. Handle the wrap around.
                                x = (x + VECTORS[item].x + row_width) % row_width
                                y = (y + VECTORS[item].y + col_height) % col_height
                            
                            # And now add the +1 back to both coords
                            new_blizzard_locs[Point(x+1, y+1)].add(item)        
        
        return MapState((self._width, self._height), new_blizzard_locs, self._me)
    
    def next_me_state(self):
        # now yield MapStates with with all valid positions for me
        for proposed in self._me.adjacent_points():
            if self._is_valid(proposed):
                yield MapState((self._width, self._height), self._map_locs, proposed)
        
    def _is_valid(self, point: Point) -> bool:
        if not (0 <= point.x < self._height):   # out of bounds
            return False
        
        if point in self._map_locs: # it's a blizzard or a wall
            return False
        
        return True
    
    @classmethod
    def create_from_grid(cls, grid: list[str]):
        """ Normal route to create an initial MapState from a grid """
        locations = defaultdict(set)
        for y, row in enumerate(grid):
            for x, val in enumerate(row):
                if val is not ".": 
                    locations[Point(x,y)].add(val)
        
        grid_dims = (len(grid[0]), len(grid))
        me = Point(1,0)
        return cls(grid_dims, locations, me)
        
    def __str__(self) -> str:
        lines = []
        for y in range(0, self._height):
            line = ""
            for x in range (0, self._width):
                curr_locn = Point(x,y)
                count = len(self._map_locs[curr_locn])
                if count == 1: # one blizzard here
                    line += next(val for val in self._map_locs[curr_locn])
                elif count == 0: # Nothing here
                    line += "."
                else: # more than one blizzard here
                    line += str(len(self._map_locs[curr_locn]))
                    
            lines.append(line)
            
        return "\n".join(lines) + f"\nCurrent={self._me}, Goal={self._goal}"

VECTORS = {
    '^': Point(0, -1),
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0)
}

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    state = MapState.create_from_grid(data)
    print(state)
    
    for i in range(1, 6):
        print(f"\nRound {i}")
        state = state.next_blizzard_state()
        print(state)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
