"""
Author: Darren
Date: 12/12/2022

Solving https://adventofcode.com/2022/day/12

Input is a grid of elevations, where a is lowest, and z is tallest.
We need to navigate the grid, from Start to End.
We can move to any adjacent L, R, U, D location, 
if that location's elevation is no greater than current elevation + 1.

Part 1:

What is the fewest steps required to move from your current position to the goal?

Find shortest path from S to E.
Solution: use a BFS.

Part 2:

What is the shortest number of steps (path), given all starting locations `a` to the goal?

Rather than doing a BFS from each start position `a`, we should just do a single BFS
from `E` to every point in the grid.  Then find all paths that with `a` as a goal, 
and assemble the path with breadcrumbs. Abort if we can't find a key,
as this means there is no path from `E` to this `a`.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

@dataclass(frozen=True)
class Point():
    """ Point class, which knows how to return a list of all adjacent coordinates """    
    x: int
    y: int
    
    def neighbours(self) -> list[Point]:
        """ Return all adjacent orthogonal (not diagonal) Points """
        return [Point(self.x+dx, self.y+dy) for dx in range(-1, 2)
                                            for dy in range(-1, 2)
                                            if abs(dy) != abs(dx)]

class Grid():
    """ 2D grid of point values. """
       
    def __init__(self, grid_array: list[str]) -> None:
        """ Generate Grid instance from 2D array. 
        This works on a deep copy of the input data, so as not to mutate the input. """                                         
        self.array = grid_array  # Store a deep copy of input data
        self.x_size = len(self.array[0])
        self.y_size = len(self.array)
        self.start = self._get_point_for_elevation("S")
        self.goal = self._get_point_for_elevation("E")
        
    def _all_points(self) -> list[Point]:
        points = [Point(x, y) for x in range(self.x_size) for y in range(self.y_size)]
        return points
    
    def all_lowest_elevation_points(self) -> set[Point]:
        low_points = {point for point in self._all_points() 
                        if self.array[point.y][point.x] == "a"
                        or self.array[point.y][point.x] == "S"}
        return low_points
    
    def _get_point_for_elevation(self, x: str) -> Point:
        """ Use this to find the point where "S" or "E" are located. """
        assert x in ("S", "E"), "Specified point must be Start or End!"
        for row_num, row in enumerate(self.array):
            if x in row:
                return Point(row.index(x), row_num)
    
    def elevation_at_point(self, point: Point) -> int:
        """ Elevation value at this point """
        if point not in (self.start, self.goal):
            return ord(self.array[point.y][point.x])
        
        if point == self.start:
            return ord("a") # we're told start location is elevation a

        if point == self.goal:
            return ord("z") # we're told start location is elevation z
    
    def _point_in_grid(self, point: Point) -> bool:
        """ Check if a location is within the grid """
        if (0 <= point.x < self.x_size and 0 <= point.y < self.y_size):
            return True
        
        return False
    
    def _valid_neighbours(self, location:Point):
        """ Yield adjacent neighbour points.
        We can move L, R, U, D by one unit. But we can only move to locations that
        are no more than one higher than current elevation. """
        current_elevation = self.elevation_at_point(location)
        
        for neighbour in location.neighbours():
            if self._point_in_grid(neighbour):
                if self.elevation_at_point(neighbour) <= current_elevation + 1:
                    yield neighbour

    def get_path(self, end: Point) -> dict:
        """ Given the start point, find all paths to destination. """
        points_to_assess: deque[Point] = deque() # Points we want to get value of, and get neighbours for
        points_to_assess.append(end)   # where we start

        came_from = {}
        came_from[end] = None
        
        # BFS with no goal
        while points_to_assess:     # They should only ever be valid points
            current = points_to_assess.popleft()
            
            for neighbour in self._valid_neighbours(current):
                if neighbour not in came_from:   # We will need to assess this point
                    points_to_assess.append(neighbour)
                    came_from[neighbour] = current
        
        return came_from

    def __repr__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self.array)     

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    grid = Grid(data)
    came_from = grid.get_path(grid.start)
    
    # Part 1
    goal = grid.start   # Going to 'S'
    path = []
    current = grid.goal  # Starting with 'E'
    while current != goal: 
        path.append(current)
        current = came_from[current]
    p1_length = len(path)
    
    print(f"Part 1: {p1_length}")
    
    # Part 2  
    p2_length = p1_length
    for goal in grid.all_lowest_elevation_points():  # Going to all 'a'
        if goal in came_from:
            path = []
            current = grid.goal # Starting with 'E'
            while current != goal: 
                path.append(current)
                if current in came_from:
                    current = came_from[current]
                else:
                    break
            p2_length = min(p2_length, len(path))

    print(f"Part 2: {p2_length}")
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
