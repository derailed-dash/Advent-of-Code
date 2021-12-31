"""
Author: Darren
Date: 15/12/2021

Solving https://adventofcode.com/2021/day/15

We need to find a way from start (top left) to end (bottom right)
of an array of risk values.  We want lowest risk.

Part 1:
    Use an A* BFS, where priority is the sum of cumulative risk and 
    manhatten distance to the goal. Use heapq for the priority queue for our frontier.
    For each point, store the point we came from.
    Thus, we can rebuild the overall path, once we reach our goal.

Part 2:
    Update Grid class so it knows how to increment all its risk values.
    Update Grid class so it knows how to stich on a new grid to the right.
    Compute the 10 different grids we need to stich together in the 5x5 uber array.
    Then, build uber grid rows by horizontal stitching.
    Conver the uber grid rows into a single uber grid.
    Finally, run through the A* BFS from Part 1.
"""
from __future__ import annotations
from collections import namedtuple
from copy import deepcopy
import logging
import os
import time
import heapq

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

Point = namedtuple("Point", "x y")  # Make it easier to index point x and y

class Grid():
    """ 2D grid of point values. Knows how to:
       - Determine value at any point
       - Determine all neighbouring points of a given point
       - Stitch together an adjacent grid to create a new grid
       - Increment all values in the grid, according to cycle rules """
       
    def __init__(self, grid_array: list) -> None:
        """ Generate Grid instance from 2D array. 
        This works on a deep copy of the input data, so as not to mutate the input. """
        
        # generate list of dx,dy to get to all adjacent points, EXCLUDING diags
        delta = 1   # delta distance to use when finding neighbours
        self._adjacent_deltas = [(dx,dy) for dx in range(-delta, delta+1)
                                         for dy in range(-delta, delta+1)
                                         if abs(dy) != abs(dx)]
                                         
        self._array = deepcopy(grid_array)  # Store a deep copy of input data
        self._x_size = len(self._array[0])
        self._y_size = len(self._array)
        
    @property
    def x_size(self):
        """ Array width (cols) """
        return self._x_size
    
    @property
    def y_size(self):
        """ Array height (rows) """
        return self._y_size
    
    @property
    def array(self):
        return self._array
    
    def increment_grid(self):
        """ Increment the value of every point in the array by 1.
        However, max is 9, and values wrap around to 1, NOT 0. """
        for y in range(self.y_size):
            for x in range(self.x_size):
                value = self.value_at_point(Point(x, y))
                if value < 9:
                    self.set_value_at_point(Point(x, y), value+1)
                else:
                    self.set_value_at_point(Point(x, y), 1)
    
    def set_value_at_point(self, point: Point, value: int):
        self._array[point.y][point.x] = value
        
    def value_at_point(self, point: Point) -> int:
        """ Value at this point """
        return self._array[point.y][point.x]
    
    def _valid_location(self, point: Point) -> bool:
        """ Check if a location is within the grid """
        if (0 <= point.x < self.x_size and  0 <= point.y < self.y_size):
            return True
        
        return False
    
    def yield_neighbours(self, point:Point):
        """ Yield adjacent neighbour points """
        for dx,dy in self._adjacent_deltas:
            neighbour = Point(point.x+dx, point.y+dy)
            if self._valid_location(neighbour):
                yield neighbour
                
    def get_distance(self, point_a: Point, point_b: Point):
        """ Manhattan distance between two points in this grid """   
        return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y) 
                
    def append_grid(self, adjacent_grid: Grid) -> Grid:
        """ Append the new grid to the right of this grid.
        This creates a new grid which is horizontally bigger.
        Returns the new grid """

        this_array = self.array
        other_array = adjacent_grid.array
        
        new_rows = []
        for y in range(self.y_size):
            new_rows.append(this_array[y] + other_array[y])
            
        return Grid(new_rows)
    
    def __repr__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._array)
        

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = [[int(posn) for posn in row] for row in f.read().splitlines()]

    # Part 1
    grid = Grid(data)
    path = navigate_grid(grid)
    total_risk = sum([location[1] for location in path])
    logger.info("Part 1 total risk: %d", total_risk)
    
    # Part 2
    # Build a new grid, which is 5x5 extension of our existing grid
    uber_grid = build_uber_grid(grid, 5, 5)
    path = navigate_grid(uber_grid) # Re-run our A* BFS
    total_risk = sum([location[1] for location in path])
    logger.info("Part 2 total risk: %d", total_risk)

def build_uber_grid(start_grid: Grid, rows: int, cols:int) -> Grid:
    # First, generate 10 possible permutations of our original grid
    grids: dict[int, Grid] = {}
    grids[0] = start_grid
    for i in range(1, 10):
        uber_grid_row = Grid(grids[i-1].array)
        uber_grid_row.increment_grid()
        grids[i] = uber_grid_row
            
    uber_grid_rows: list[Grid] = []
    for row in range(rows):
        # Now stich each adjacent tile together to make an uber row
        uber_grid_row = grids[row]
        for col in range(1, cols):
            uber_grid_row = uber_grid_row.append_grid(grids[row+col])
            
        uber_grid_rows.append(uber_grid_row)
    
    # now convert our five uber_grid_rows to a single uber grid
    uber_rows = []
    for uber_grid_row in uber_grid_rows:
        for row in uber_grid_row.array:
            uber_rows.append(row)
            
    return Grid(uber_rows)      
  
def navigate_grid(grid: Grid) -> list[tuple[Point, int]]:
    """ An A* BFS to get from top right to bottom left """
    
    start = (Point(0,0))
    current = start
    end = (Point(grid.x_size-1, grid.y_size-1))
    
    frontier = []
    heapq.heappush(frontier, (0, current))   # (priority, location)
    
    came_from = {}  # So we can rebuild winning path from breadcrumbs later
    came_from[current] = None
    
    risk_so_far = {}    # Store cumulative risk from grid values
    risk_so_far[current] = 0
    
    while frontier:
        priority, current = heapq.heappop(frontier)
        if current == end:
            break   # Goal reached
        
        for neighbour in grid.yield_neighbours(current):
            new_risk = risk_so_far[current] + grid.value_at_point(neighbour)
            if neighbour not in risk_so_far or new_risk < risk_so_far[neighbour]:
                risk_so_far[neighbour] = new_risk
                priority = new_risk + grid.get_distance(neighbour, end)
                heapq.heappush(frontier, (priority, neighbour))
                came_from[neighbour] = current
    
    # Now we've reached our goal, build the winning path from breadcrumbs
    path: list[tuple[Point, int]] = []   # (location, risk)
    while current != start:
        risk_at_current = grid.value_at_point(current)
        path.append((current, risk_at_current))
        current = came_from[current]
    
    path.reverse()
    
    return path

    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
