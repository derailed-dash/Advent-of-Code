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
from collections import deque
from dataclasses import dataclass
import functools
import heapq
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

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
    def __init__(self, grid: list, me_locn: Point, t=0) -> None:
        self.grid: list[list] = grid # { point: { blizzards } }  Can contain a blizzard or a wall
        
        self._height = len(grid)
        self._width = len(grid[0])
        self._me = me_locn
        self._time = t
        self.goal = Point(self._width-2, self._height-1)

    def __hash__(self) -> int:
        row = self.grid[1]
        row_str = ""
        for item in row:
            if isinstance(item, set):
                val = len(item)
            else:
                val = item
                
            row_str += str(val)
        
        return hash((self._me, "\n".join(row_str)))  
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, MapState):
            if self.grid == other.grid and self.me == other.me:
                return True
            
            return False
        else:
            return NotImplemented

    @property
    def me(self) -> Point:
        return self._me
    
    @property
    def time(self) -> int:
        return self._time
    
    def _distance_to_goal(self) -> int:
        """ Use to determine how close we are to succeeding. """
        return self.goal.distance_to(self.me)
    
    def __lt__(self, other):
        """ Use distance heuristic. Lower is better. """
        if isinstance(other, MapState):
            return self._distance_to_goal() < other._distance_to_goal()
        else:
            return NotImplemented
        
    def next_blizzard_state(self) -> MapState:
        """ Move blizzards to achieve next blizzard state.  There is only one possible next blizzard state """

        row_width = self._width - 2 # ignore walls
        col_height = self._height - 2 # ignore walls
        
        # Create new grid, with edges and all inner tiles containing an empty set
        tmp_grid = []
        for y, current_row in enumerate(self.grid):
            new_row = []
            if y in (0, self._height-1):
                new_row = current_row
            else:        
                for x, current_val in enumerate(current_row):
                    if x in (0, self._width-1): # add the edges
                        new_row.append(current_val)
                    else:
                        new_row.append(set()) # create an empty set to store blizzards
                        
            tmp_grid.append(new_row)
        
        for y in range(1, self._height-1):
            for x in range(1, self._width-1):
                current = self.grid[y][x]
                if isinstance(current, set):
                    for bliz in current:
                        # For blizzard, find next position by adding blizzard vector. Handle the wrap around.
                        move_to_x = (x-1 + VECTORS[bliz].x + row_width) % row_width
                        move_to_y = (y-1 + VECTORS[bliz].y + col_height) % col_height
                        tmp_grid[move_to_y+1][move_to_x+1].add(bliz)
        
        return MapState(tmp_grid, self._me, self._time+1)
    
    def next_me_state(self):
        # now yield MapStates with with all valid positions for me
        proposals = self._me.adjacent_points()
        proposals.add(self._me)
        
        for proposed in proposals:
            if self._is_valid(proposed):
                yield MapState(self.grid, proposed, self._time)
        
    def _is_valid(self, point: Point) -> bool:
        if not (0 <= point.x < self._width):   # out of bounds
            return False
        
        if not (0 <= point.y < self._height):   # out of bounds
            return False
        
        if self.grid[point.y][point.x] == '#':
            return False
        
        if self.grid[point.y][point.x] == '.':
            return True
        
        if isinstance(self.grid[point.y][point.x], set):
            if len(self.grid[point.y][point.x]) == 0:
                return True
        
        return False
    
    @classmethod
    def create_from_grid(cls, grid: list[str]):
        """ New grid from input data. Blizzards stored in sets. """
        rows = []
        for row in grid:
            new_row = []
            for val in row:
                if val in VECTORS:
                    new_row.append({val})
                else:
                    new_row.append(val)
            
            rows.append(new_row)
        
        me = Point(1,0)
        return cls(rows, me)
        
    def __str__(self) -> str:
        lines = []
        for y in range(0, self._height):
            line = ""
            for x in range (0, self._width):
                val = self.grid[y][x]
                if Point(x,y) == self._me:
                    line += "M" 
                elif isinstance(val, set):
                    if len(val) == 1: # one blizzard here
                        line += next(bliz for bliz in val)
                    elif len(val) > 1: # more than one blizzard here
                        line += str(len(val))
                    else:
                        line += '.'
                else: # must be a str
                    line += val
                    
            lines.append(line)
            
        return ("\n".join(lines) + 
                f"\nTime={self.time}, Me={self._me}, Distance={self._distance_to_goal()}, Hash={hash(self)}")

    def __repr__(self) -> str:
        return f"Time={self.time}, Me={self._me}, Distance={self._distance_to_goal()}, Hash={hash(self)}"
    
VECTORS = {
    '^': Point(0, -1),
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0)
}

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    @functools.cache
    def a_star(state: MapState, goal: Point):
        current_state: MapState = state
        # frontier = []
        # heapq.heappush(frontier, current_state)
        frontier = deque([current_state])
        explored = {current_state}
        
        while frontier:
            # current_state = heapq.heappop(frontier)
            current_state = frontier.popleft()
            print(repr(current_state))
            
            if current_state.me == goal:
                break
            
            next_blizzard_state = current_state.next_blizzard_state()
            
            for next_state in next_blizzard_state.next_me_state():
                if next_state not in explored:
                    # heapq.heappush(frontier, next_state)
                    frontier.append(next_state)
                    explored.add(next_state)
            
        return current_state

    state = MapState.create_from_grid(data)
    last_state = a_star(state, state.goal)
    print(f"Time={last_state.time}")
            
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
