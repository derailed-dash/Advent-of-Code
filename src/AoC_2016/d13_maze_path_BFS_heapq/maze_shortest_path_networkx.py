"""
Author: Darren
Date: 11/07/2021

Solving https://adventofcode.com/2016/day/13

Solution 2 of 2:
    Use a NetworkX graph and BFS.
    You can turn the nx graph rendering off.  (Set NX_RENDERING.)
    Marginally slower than my dict-based solution.  But takes away all the hard work!  Still under 60ms.

Part 1:
    Point2D class knows how to find its own neighbours, and check for equality.
    Then, implement standard BFS algorithm:
        Create nx graph, g.
        Use set to store points explored.
        Create a queue of points to dive into.
        Mark START as explored
        Add START to queue
        Add START to g.
        while we have points in the queue and we haven't reached the destination
            cp = pop the queue
            get all valid unexplored neighbours not already explored
            for neighbour (n) in neighbours
                if n not explored
                    Add n as node to graph
                    Add cp, n as edge to graph 
                    Mark n as explored
                    Add n to the queue
                    
    Solve using nx.shortest_path(g, START, dest)
                
Part 2:
    We need all destinations that can be reached in no more than 50 steps.
    Solve using nx.single_source_shortest_path(g, START, cutoff=50) 
"""
from __future__ import annotations
import logging
import os
import time
import heapq    # we could simply use a list or a deque, but wouldn't scale to huge problems
import matplotlib.pyplot as plt
import networkx as nx

# pylint: disable=logging-fstring-interpolation,no-value-for-parameter,unexpected-keyword-arg
class Point2D():
    """ Point2D class, which stores x and y, and can generate adjacent Point2D objects """
    
    # If diagnonal is not allowed, then these are the only adjacent moves
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

# Test problem
MAZE_CONST = 10
dest = Point2D(7,4)

# Actual problem
MAZE_CONST = 1352
dest = Point2D(31,39)

NX_RENDERING = False

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
    
    # Part 1
    graph = nx.Graph()
    
    points_explored = set()
    points_explored.add(START)      # Mark our START as explored
    points_queue: list = [START]
    
    graph.add_node(START)
      
    while dest not in points_explored and points_queue:
        current_point = heapq.heappop(points_queue)
        
        # determine all valid neighbours that are not yet explored
        valid_neighbours = [neighbour for neighbour in current_point.yield_neighbours() 
                                if is_open(neighbour) 
                                and neighbour not in points_explored 
                                and is_valid_coord(neighbour)]
        
        # Add each neighbour to the graph, and the edge from current point to neighbour
        for neighbour in valid_neighbours:
            if neighbour not in points_explored:
                points_explored.add(neighbour)
                graph.add_node(neighbour)
                graph.add_edge(current_point, neighbour)
                heapq.heappush(points_queue, neighbour)
                
    solution_path = nx.shortest_path(graph, source=START, target=dest)
    logging.debug(f"Shortest path from graph: {solution_path}")
    logging.info(f"Steps required: {len(solution_path)-1}")
    
    if NX_RENDERING:
        pos= nx.planar_layout(graph)
        nx.draw(graph, pos, with_labels=True, edge_color="r")
        plt.show()
       
    # Part 2
    max_steps = 50
    
    # return dict of {dest: path} for all destinations that can be reached from this START
    # and stopping which we reach the maximum length of path, i.e. the cutoff
    paths = nx.single_source_shortest_path(graph, START, cutoff=max_steps)
    print(f"Destinations with no more than {max_steps} = {len(paths)}")
    
def build_maze(solution_path: list[Point2D]) -> list[str]:
    """ Create a maze in the form a list 
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
