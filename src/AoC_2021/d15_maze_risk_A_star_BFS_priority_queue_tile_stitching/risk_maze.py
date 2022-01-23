"""
Author: Darren
Date: 15/12/2021

Solving https://adventofcode.com/2021/day/15

We're in a cavern with a low ceiling just above us, 
so we can only navigate in two dimensions.
The cavern makes up a graph of connected locations.
Each location has a risk level to enter, based on hazards on the walls. 
  
We need to find a way from start (top left) to end (bottom right),
picking the route with lowest risk.

Part 1:
    Use an Dijkstra/A* BFS, where priority is the sum of cumulative risk and 
    manhatten distance to the goal. Use heapq for the priority queue for our frontier.
    For each point, store the point we came from.
    Thus, we can rebuild the overall path, once we reach our goal.

Part 2:
    The cave is 5x larger than Part 1 in both x and y dimensions.
    Thus Part 1 is a single tile at the top left of a 5x5 grid of tiles.
    With each repeating tile, the location risk is 1 higher than the corresponding risk above or left.
    As before, find the path from top left to bottom right.
    
    Update Grid class so it knows how to increment all its risk values.
    Update Grid class so it knows how to stich on a new grid to the right.
    Compute the 10 different grids we need to stich together in the 5x5 uber array.
    Then, build uber grid rows by horizontal stitching.
    Conver the uber grid rows into a single uber grid.
    Finally, run through the A* BFS from Part 1.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
import logging
import os
import time
import heapq
from matplotlib import pyplot as plt

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

@dataclass(frozen=True, order=True)
class Point():
    """ Point class, which knows how to return a list of all adjacent coordinates """
    
    # Return all adjacent orthogonal (not diagonal) coordinates
    DELTAS = [(dx,dy) for dx in range(-1, 2) for dy in range(-1, 2) if abs(dy) != abs(dx)]
    
    x: int
    y: int
    
    def neighbours(self) -> list[Point]:
        """ Return all adjacent orthogonal (not diagonal) Points """
        return [Point(self.x+dx, self.y+dy) for dx,dy in Point.DELTAS]

class Grid():
    """ 2D grid of point values. Knows how to:
       - Determine value at any point
       - Determine all neighbouring points of a given point
       - Stitch together an adjacent grid to create a new grid
       - Increment all values in the grid, according to the increment rules """
       
    def __init__(self, grid_array: list[list[int]]) -> None:
        """ Generate Grid instance from 2D array. 
        This works on a deep copy of the input data, so as not to mutate the input. """                                         
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

    def all_points(self) -> list[Point]:
        points = [Point(x, y) for x in range(self.x_size) for y in range(self.y_size)]
        return points
    
    def increment_grid(self):
        """ Increment the value of every point in the array by 1.
        However, max is 9, and values wrap around to 1, NOT 0. """
        for point in self.all_points():
            value = self.value_at_point(point)
            if value < 9:
                self.set_value_at_point(point, value+1)
            else:
                self.set_value_at_point(point, 1)
    
    def set_value_at_point(self, point: Point, value: int):
        self._array[point.y][point.x] = value
        
    def value_at_point(self, point: Point) -> int:
        """ Value at this point """
        return self._array[point.y][point.x]
    
    def _valid_location(self, point: Point) -> bool:
        """ Check if a location is within the grid """
        if (0 <= point.x < self.x_size and 0 <= point.y < self.y_size):
            return True
        
        return False
    
    def valid_neighbours(self, point:Point):
        """ Yield adjacent neighbour points """
        for neighbour in point.neighbours():
            if self._valid_location(neighbour):
                yield neighbour
                
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
    # visualise_path(grid, path)
    
    # Part 2
    # Build a new grid, which is 5x5 extension of our existing grid
    uber_grid = build_uber_grid(grid, 5, 5)
    path = navigate_grid(uber_grid) # Re-run our A* BFS
    total_risk = sum([location[1] for location in path])
    logger.info("Part 2 total risk: %d", total_risk)

def visualise_path(grid: Grid, path: list[tuple[Point, int]]):
    """ Render this paper and its dots as a scatter plot """
    all_x = [point.x for point in grid.all_points()]
    all_y = [point.y for point in grid.all_points()]
    labels = [grid.value_at_point(point) for point in grid.all_points()]
    path_points = [Point(0,0)] + [path_item[0] for path_item in path]
    
    axes = plt.gca()
    axes.set_aspect('equal')
    plt.axis("off") # hide the border around the plot axes
    axes.set_xlim(min(all_x)-1, max(all_x)+1)
    axes.set_ylim(min(all_y)-1, max(all_y)+1)
    axes.invert_yaxis()
    
    for point, label in zip(grid.all_points(), labels):
        if point in path_points:
            plt.text(point.x, point.y, s=str(label), color="r")
        else:
            plt.text(point.x, point.y, s=str(label), color="b")
        
    plt.show()

def build_uber_grid(start_grid: Grid, rows: int, cols:int) -> Grid:
    """ Build an uber grid, made up of y*x tiles, where each tile is the size of the start grid.
    With each tile to the right or down, all values increase by 1, according to increment rules. 
    """
    
    # Create the nine permutations of the starting tile 
    # (since each digit in the tile can only be from 1-9 inclusive)
    tile_permutations: dict[int, Grid] = {}
    tile_permutations[0] = start_grid
    for i in range(1, 9):
        tile = Grid(tile_permutations[i-1].array)
        tile.increment_grid()
        tile_permutations[i] = tile  # each tile is an increment of the grid before

    # Now stich each adjacent tile together to make an uber row            
    tile_rows: list[Grid] = []  # to hold y rows of very wide arrays
    for row in range(rows):
        tile_row = tile_permutations[row] # set the first tile in the row
        for col in range(1, cols):   # now add additional tiles to make the complete row
            tile_row = tile_row.append_grid(tile_permutations[row+col])
            
        tile_rows.append(tile_row)
    
    # now convert our five long grids into a single list of rows
    uber_rows = []
    for tile_row in tile_rows:
        for row in tile_row.array:
            uber_rows.append(row)
            
    return Grid(uber_rows)      
  
def navigate_grid(grid: Grid) -> list[tuple[Point, int]]:
    """  A Dijkstra BFS to get from top left to bottom right 

    Args:
        grid (Grid): 2d grid of risk values

    Returns:
        list[tuple[Point, int]]: A path, from beginning to end, as a list of (Point, risk)
    """
    
    start: Point = (Point(0,0))
    current: Point = start
    end: Point = (Point(grid.x_size-1, grid.y_size-1))
    
    frontier = []
    heapq.heappush(frontier, (0, current))   # (priority, location)
    
    came_from = {}  # So we can rebuild winning path from breadcrumbs later
    came_from[current] = None
    
    risk_so_far: dict[Point, int] = {}    # Store cumulative risk from grid values
    risk_so_far[current] = 0
    
    while frontier:
        _, current = heapq.heappop(frontier)
        if current == end:
            break   # Goal reached
        
        for neighbour in grid.valid_neighbours(current):
            new_risk = risk_so_far[current] + grid.value_at_point(neighbour)
            if neighbour not in risk_so_far or new_risk < risk_so_far[neighbour]:
                risk_so_far[neighbour] = new_risk
                heapq.heappush(frontier, (new_risk, neighbour))
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
