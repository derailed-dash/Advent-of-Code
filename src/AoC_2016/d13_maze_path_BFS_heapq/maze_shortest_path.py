"""
Author: Darren
Date: 09/07/2021

Solving https://adventofcode.com/2016/day/13

Solution 1 of 2:
    This solution is purely BFS.
    It builds a dict that maps points to the path to that point.
    It assembles the path one point at a time, and uses preceding path + [current point] as the path to all neighbours.
    Solves both parts in under 40ms.

Part 1:
    Point2D class knows how to find its own neighbours, and check for equality.
    Then, implement standard BFS algorithm:
        Use set to store points explored.
        Use dict to map points to paths (where a path is a set of points to this point)
        Create a queue of points to dive into.
        Mark START as explored
        Add START to queue
        while we have points in the queue and we haven't reached the destination
            cp = pop the queue
            get all valid unexplored neighbours not already explored
            set new path (p: list) as path to cp, plus [cp] itself
            for neighbour (n) in neighbours
                if n is in the paths dict and new path is longer: ignore it
                Add {n: new path} to the paths dict
                Mark n as explored
                Add n to the queue
                
Part 2:
    We need all points we can reach in 50 moves or less.
    We know from Part 1 that we've already achieved all paths that can be reached in 50 moves, 
    since answer to Part 1 was > 50.
    Simply use a filter, i.e. using this construct:
        filtered_locations = dict(filter(lambda item: len(item[1]) <= max_steps, my_dict.items()))   

"""
from __future__ import annotations
import logging
import os
import time
import heapq    # we could simply use a list or a deque, but wouldn't scale to huge problems

# pylint: disable=logging-fstring-interpolation
class Point2D():
    """ Point2D class, which stores x and y, and can generate adjacent Point2D objects """
    
    # If diagonal is not allowed, then these are the only adjacent moves
    VALID_MOVES = {
        'U': (0, 1),
        'R': (1, 0),
        'D': (0, -1),
        'L': (-1, 0)
    }
    
    def __init__(self, x:int, y:int) -> None:
        self._x = x
        self._y = y
        
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def yield_neighbours(self):
        for vector in Point2D.VALID_MOVES.values():
            x = self.x + vector[0]
            y = self.y + vector[1]
            
            yield Point2D(x, y)
    
    def __lt__(self, o: Point2D) -> bool:
        return (self.x + self.y) < (o.x + o.y)
    
    def __gt__(self, o: Point2D) -> bool:
        return (self.x + self.y) > (o.x + o.y)
                
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, o: Point2D) -> bool:
        return self.x == o.x and self.y == o.y
        
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"({self._x}, {self._y})"
            
SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

WALL = "#"
SPACE = "."
START = Point2D(1, 1) 

RENDER_MAZE_PATH = True

# Test problem
# MAZE_CONST = 10
# dest = Point2D(7,4)

# Actual problem
MAZE_CONST = 1352
dest = Point2D(31,39)

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
    
    # Part 1
    points_explored = set()
    paths_to_points: dict[Point2D, list[Point2D]] = {START: []}  # map each point to the path that gets to this point
    
    points_explored.add(START)      # Mark our START as explored
    points_queue: list = [START]
        
    while dest not in points_explored and points_queue:
        current_point = heapq.heappop(points_queue)
        
        # determine all valid neighbours that are not yet explored
        valid_neighbours = [neighbour for neighbour in current_point.yield_neighbours() 
                                if is_open(neighbour) 
                                and neighbour not in points_explored 
                                and is_valid_coord(neighbour)]
        
        # Set the path for each valid neighbour.  This will path to the current point, plus the current point.
        path_with_current = paths_to_points[current_point] + [current_point]        
        for neighbour in valid_neighbours:
            if neighbour in paths_to_points and len(paths_to_points[current_point]) <= len(path_with_current):
                continue    # Don't set the path if we already have a shorter path defined for this neighbour
            
            paths_to_points[neighbour] = path_with_current
            points_explored.add(neighbour)
            heapq.heappush(points_queue, neighbour)
    
    if dest not in paths_to_points:
        raise ValueError(f"No path found for {dest}", paths_to_points.keys())
        
    solution_path = paths_to_points[dest] + [dest]
    # logging.debug(f"Path to {dest}: {solution_path}")
    
    # Path length is the length of the path, minus one, since we don't count the point we started on
    logging.info(f"Steps required: {len(solution_path)-1}")
    
    # We don't actually need to build the maze, because the algorithm can determine if a valid space on the fly
    if RENDER_MAZE_PATH:
        maze = build_maze(solution_path)
        logging.info(f"Solution path:\n{visualise_path(maze, solution_path=solution_path)}\n")
    
    # Part 2
    max_steps = 50
    filtered_locations = dict(filter(lambda item: len(item[1]) <= max_steps, paths_to_points.items()))
    logging.info(f"Points we can reach in no more than {max_steps} = {len(filtered_locations)}")
    
def build_maze(solution_path: list[Point2D]) -> list[str]:
    """ Create a maze in the form of a list 
    We need to render a map that is at least as big as the solution path itself """
    max_x = max(point.x for point in solution_path)
    max_y = max(point.y for point in solution_path)
    
    maze = []
    for y in range(max_y+1):
        row = ""
        for x in range(max_x+1):
            if is_open(Point2D(x, y)):
                row += SPACE
            else:
                row += WALL
        
        maze.append(row)
    return maze
    
def is_open(point: Point2D) -> bool:
    """ Determines if point is open or blocked.
    Does this by: Find x*x + 3*x + 2*x*y + y + y*y + c
    Find binary representation. Count number of 1s in the binary repr.
    If even, it's open space.  If odd, it's a wall.
    """
    x = point.x
    y = point.y
        
    val = x**2 + 3*x + 2*(x*y) + y + y**2 + MAZE_CONST
    bin_repr = bin(val)[2:]
    true_bits = bin_repr.count("1")
    return true_bits % 2 == 0

def is_valid_coord(coord: Point2D) -> bool:
    """ Exclude coords outside the maze """
    if coord.x < 0 or coord.y < 0:
        return False
    
    return True

def visualise_path(map_list: list[str], solution_path: list) -> str:
    """ Create a visual representation of the path, line by line.
    Inserts path char "O" into the map str. """
    for point in solution_path:
        map_list[point.y] = map_list[point.y][:point.x] + "O" + map_list[point.y][point.x + 1:]
    return "\n".join(map_list)

if __name__ == "__main__":
    t1 = time.perf_counter()
    try:
        main()
    except ValueError as err: 
        print(err.args[0])
        for item in err.args[1]:
            print(item)
    
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
