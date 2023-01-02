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
- VECTORS dict to represent one unit movement in any of the four directions.
- Point class to store current location, and which allows us to add vectors to return four adjacent Points.
- Create a MapState:
  - Create a factory method that initialises a MapState from the input grid.
  - Defines the grid bounds, but trims out the four edges.
  - Stores the current time.
  - Stores all current blizzard locations as a dict:
    Key is location, and value is a list of blizzards, since we can have more than one blizzard at a loc.
  - Stores start and goal points, and provides getter / setters for them.
  - Provide a method to generate t+1 MapState, where all blizzards have moved to their new locations.
  - Provide a method to check if a given point is 'allowed', i.e. within bounds, 
    and not meeting a blizzard. (And add in the start and goal locations.)

- Implement a BFS that:
  - Add the start location to the frontier. Make the frontier a set to eliminate duplicate locations.
  - Then...
    - Get next MapState.
    - Finds all valid next locations for locations in the frontier. This includes checking current location.
      These locations become a new frontier.
    - Rinse and repeat until we identify a location that is the goal.
      Then return the latest state.

- Get the time from the latest state.

Part 2:

Now complete a return journey to the start, and then back to the finish. Whas it the total time?

- Easy... Just swap goal and start, and repeat BFS using our last state.
- Then swap goal and start one more time, and repeat again. We now have the final time.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

@dataclass(frozen=True)
class Point():
    """ Point x,y which knows how to add another point, and how to return all adjacent (non-diag) points """
    x: int
    y: int

    def __add__(self, other) -> Point:
        """ Add other point to this point, returning new point vector """
        return Point(self.x + other.x, self.y + other.y)
    
    def adjacent_points(self) -> set[Point]:
        return set(self+vector for vector in VECTORS.values())
    
    def __repr__(self):
        return f"P({self.x},{self.y})"

VECTORS = {
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0),
    '^': Point(0, -1)
}

class MapState():
    """ Store location of blizzards, grid bounds, start, goal, and time. """
    def __init__(self, blizzards: dict, grid_dims: tuple, start: Point, goal: Point, t: int) -> None:
        self._blizzards: dict[Point, list] = blizzards
        self._width = grid_dims[0]
        self._height = grid_dims[1]
        self._start = start
        self._goal = goal
        self._time = t
    
    @classmethod
    def init_from_grid(cls, grid_input: list[str]):
        """ Create a new MapState using an input grid """
        grid: list[str] = grid_input
        blizzards = defaultdict(list)
        for y, row in enumerate(grid[1:-1]): # ignore top and bottom
            for x, col in enumerate(row[1:-1]): # ignore left and right
                point = Point(x,y)
                if col in VECTORS:
                    blizzards[point].append(col)
                    
        height = len(grid) - 2
        width = len(grid[0]) - 2
        
        start = Point(0, -1) # 1 above top grid row
        goal = Point(width-1, height) # 1 below bottom grid row
        
        return MapState(blizzards, (width, height), start=start, goal=goal, t=0)
    
    @property
    def start(self) -> Point:
        return self._start
    
    @start.setter
    def start(self, point: Point):
        self._start = point
    
    @property
    def time(self) -> int:
        return self._time
    
    @property
    def goal(self) -> Point:
        return self._goal
    
    @goal.setter
    def goal(self, point):
        self._goal = point
    
    def next_blizzard_state(self) -> MapState:
        """ Move blizzards to achieve next blizzard state.  There is only one possible next blizzard state """
        next_blizzards = defaultdict(list)
        for loc, blizzards_here in self._blizzards.items():
            for current_bliz in blizzards_here:
                next_bliz_x = (loc + VECTORS[current_bliz]).x % self._width
                next_bliz_y = (loc + VECTORS[current_bliz]).y % self._height
                next_blizzards[Point(next_bliz_x, next_bliz_y)].append(current_bliz)
        
        return MapState(next_blizzards, (self._width, self._height), self._start, self._goal, self.time+1)

    def is_valid(self, point: Point) -> bool:
        """ Check if the specified point is an allowed position in the current blizzard state. """
        if point in (self._start, self._goal): # out of bounds, but allowed
            return True
        
        # out of bounds
        if not (0 <= point.x < self._width):
            return False
        if not (0 <= point.y < self._height):
            return False
        
        if point in (self._blizzards):
            return False
        
        return True

    def __str__(self) -> str:
        lines = []
        for y in range(0, self._height):
            line = ""
            for x in range (0, self._width):
                loc = Point(x,y)
                if loc in self._blizzards:
                    blizzards_here = self._blizzards[loc]
                    how_many_blizzards = len(blizzards_here)
                    if how_many_blizzards == 1: # one blizzard here
                        line += next(bliz for bliz in blizzards_here)
                    elif how_many_blizzards > 1: # more than one blizzard here
                        line += str(how_many_blizzards)
                else:
                    line += '.'
                    
            lines.append(line)
            
        return ("\n".join(lines) + 
                f"\nTime={self.time}, Hash={hash(self)}")

    def __repr__(self) -> str:
        return f"Time={self.time}, Hash={hash(self)}"
    
VECTORS = {
    '^': Point(0, -1),
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0)
}

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
    
    leg_times = []
    
    # Part 1
    state = MapState.init_from_grid(data)
    state = bfs(state)
    leg_times.append(state.time)
    print(f"Part 1: Leg time={leg_times[0]}")
    
    # Part 2
    # First, swap goal and start, since we need to go back to the start
    state.start, state.goal = state.goal, state.start
    state = bfs(state)
    leg_times.append(state.time - sum(leg_times))
    print(f"Part 2: Return leg time={leg_times[-1]}")
    
    state.start, state.goal = state.goal, state.start
    state = bfs(state)
    leg_times.append(state.time - sum(leg_times))
    print(f"Part 2: Last leg time={leg_times[-1]}")
    print(f"Part 2: Total time={sum(leg_times)}")
        
def bfs(state: MapState) -> MapState:
    """ BFS, but we're allowed to backtrack. 
    Our frontier should only contain the current set of allowed next locations. """
    start = state.start
    goal = state.goal
    
    # Use a set because the many neighbours of the points in our frontier may be the same position
    # We don't want to explore the same location twice IN THE SAME ITERATION
    frontier = {start} 
    
    while goal not in frontier:
        state = state.next_blizzard_state()
        # reset frontier because we can revisit locations we've been to before
        frontier = set(explore_frontier(state, frontier))
       
    return state
            
def explore_frontier(current_state, frontier):
    """ Generator that returns all valid next locations with current blizzard state
    from all locations in the frontier. """
    for loc in frontier:
        for neighbour in loc.adjacent_points():
            if current_state.is_valid(neighbour):
                yield neighbour
        if current_state.is_valid(loc): # staying still may be a valid move
            yield loc

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
