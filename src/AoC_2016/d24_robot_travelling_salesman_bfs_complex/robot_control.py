"""
Author: Darren
Date: 20/11/2021

Solving https://adventofcode.com/2016/day/24

Find optimum path for robot to take to reach marked locations.
We need to visit every location at least once.

Key:
  . = open passage
  n = location to visit (also open)
  # = wall
  
This is a travelling salesman shortest path problem.

Part 1:
  - First, determine how many points we need to visit.
  - Then we need to create a complete undirected weighted graph, 
    i.e. the shortest path between all points.
    Get all the combinations of points we need to visit.
    Use a BFS to find the shortest path between each pair of locations.
    Use path length as the priority for heapq.
    Store a map each pair of locations to a distance.
  - Then, since n<10, we can determine all permutations of locations we need to visit; 
    there will be n! permutations.
  - Finally, we need a Travelling Salesman Problem (TSP) solution
    that sums up the distances for each pemutation of locations.
    Find the smallest sum.
    Because we want to start at location 0, this reduces the number of permutations to work through.

Part 2:
  - We need to move the robot back to the start position.
    So, we just add location 0 to the end of all the permutations.
    Then sum up all the journeys once more.
"""
import heapq
import logging
import os
import time
from itertools import combinations, permutations
from typing import NamedTuple

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class LayoutState():
    """ Represents the layout, with the current position 
    and the path taken to get this state. 
    
    The Map can be used in a priority heap queue, 
    since the distance from the current position to the goal will be the priority. """
    
    BLOCKED = "#"
    OPEN = "."
        
    VECTORS = set([0-1j, 0+1j, -1+0j, 1+0j])   # real = col, imag = row
     
    def __init__(self, layout: list[str], goal: complex, position: complex, path=None) -> None:
        """ Instantiates a LayoutState, given goal and current position. 

        Args:
            layout (list): The layout (map)
            goal (complex): The coordinate we want to reach
            position (complex): The current position
            path ([complex], optional): The path taken so far. Defaults to None.
        """
        self._layout = layout
        rows = len(self._layout)
        cols = len(self._layout[0])
        
        self._dims = (cols, rows)
        self._position = position
        self._goal = goal
        
        if path is None:
            self._path = []
        else:
            self._path = path
    
    @property
    def dims(self) -> tuple:
        """ Tuple of maze dimensions, in the format (cols, rows). """
        return self._dims
            
    @property
    def position(self) -> complex:
        """ The current position in the maze. """
        return self._position
    
    @property
    def goal(self) -> complex:
        """ The maze coordinate we need to get to. """
        return self._goal
    
    @property
    def path(self) -> list:
        """ A growing list of all the nodes traversed. """
        return self._path
    
    @property
    def priority(self):
        """ Lowest value represents highest priority. 
        Short path lengths are good, so let's prioritise on path length. """
        return len(self.path)
    
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}" +
            f"(posn={str(self.position)},path={self.path},priority={self.priority})")
    
    def __str__(self) -> str:
        return f"posn={self.position}, path={self.path}, priority={self.priority}"
    
    def __eq__(self, o) -> bool:
        """ Equality is based on current position """
        if isinstance(o, LayoutState):
            return self.position == o.position
        else:
            return NotImplemented
    
    def __hash__(self) -> int:
        """ Hash is based on tuple of the current position """
        return hash(self.position)
    
    def __lt__(self, o) -> bool:
        return self.priority < o.priority
    
    def yield_next_state(self):
        for vector in LayoutState.VECTORS:
            new_position = self.position + vector
            
            x = int(new_position.real)
            y = int(new_position.imag)
            
            # Check if adjacent node is within the grid
            if (0 <= x <= self.dims[0]
                    and 0 <= y <= self.dims[1]):
                
                # Only yield adjacent positions that are open
                if (self._layout[y][x] == LayoutState.OPEN or 
                    self._layout[y][x].isdigit()):
                    new_path = self.path + [self.position]
                    
                    yield LayoutState(layout=self._layout, goal=self.goal, position=new_position, path=new_path)

class LegToDistance(NamedTuple):
    start: int
    end: int
    distance: int

def determine_locations_to_visit(layout: list) -> dict[int, complex]:
    """ Determine all the locations to visit, in the layout.
    The layout contains ints=locations to visit, .=corridor, and #=wall.
    Looks for all integer values in the layout.
    Stores them in a dict, along with their coordinates.

    Args:
        layout (list): The layout

    Returns:
        [dict]: Dict of locations mapped to coordinates.
    """
    locations_to_visit = {}     # store in format {n: (i+j)}
    for y, row in enumerate(layout):
        for x, col in enumerate(row):
            if col.isdigit():
                locations_to_visit[int(col)] = complex(x, y)
    
    locations_to_visit = dict(sorted(locations_to_visit.items(), key=lambda x: x[0]))
    return locations_to_visit

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        layout = f.read().splitlines()
    
    # Get sorted list of locations to visit in the layout
    locations_to_visit = determine_locations_to_visit(layout)
    logger.info("We have %d locations to visit (dict):", len(locations_to_visit.keys()))
    logger.info(locations_to_visit)
    
    # Now get all the unique combinations of these locations in the layout
    # E.g. [(0, 1), (0, 2), (0, 3) ...]
    # Convert to list so we can reuse later
    combos = list(combinations(locations_to_visit.keys(), 2))
    logger.debug("Location pairs (combos):\n%s", combos)
    
    # Get the path length for each pair (combo) of locations, using BFS for each
    combo_edges = get_shortest_paths(layout, locations_to_visit, combos)
    logger.debug("Locations and distances (combo_edges):\n%s", combo_edges)
    
    # Now we need to do a travelling salesman on the path lengths
    # Let's get all the paths, a to b, in both directions, with distance
    start_location = 0
    
    # Part 1
    journey_distances = solve_tsp(combo_edges, start_location)
    min_journey = min(journey_distances.items(), key=lambda x: x[1])
    logger.info("Part 1: Shortest journey: %s", min_journey)
    
    # Part 2
    end_location = 0
    journey_distances = solve_tsp(combo_edges, start_location, end_location)
    min_journey = min(journey_distances.items(), key=lambda x: x[1])
    logger.info("Part 1: Shortest journey: %s", min_journey)

def solve_tsp(locations_and_distances, start_location=None, end_location=None) -> dict:
    """ Determine the shortest path through all locations.
    
    Args:
        locations_and_distances (dict[tuple, int]): dict of (start, end), distance
        start_location (int, optional): Location to start from.  Constraints permutations.
        end_location (int, optional): Location to end on. Gets added to all permutations.

    Returns:
        dict: journeys mapped to journey distance
    """
    leg_to_distance: list[LegToDistance] = []      # list of tuple(start, end, distance)
    unique_locations = set()
    
    # Get distance for every a to b and b to a
    # This will be our leg-to-distance lookup
    for combo, edge in locations_and_distances.items():
        path_a_to_b = LegToDistance(combo[0], combo[1], edge)
        path_b_to_a = LegToDistance(combo[1], combo[0], edge)
        unique_locations.add(combo[0])
        unique_locations.add(combo[1])
        leg_to_distance.append(path_a_to_b)
        leg_to_distance.append(path_b_to_a)
        
    logger.info("Unique locations:%s", unique_locations)
    logger.debug("All legs:\n%s", "\n".join(str(path) for path in leg_to_distance))
    
    # Now get all permuations through these locations
    # E.g. [(0, 1, 2, 3, 4), (0, 1, 2, 4, 3), (0, 1, 3, 2, 4)... ]
    journey_perms = list(permutations(unique_locations))
    logger.info("A total of %d journey permutations", len(journey_perms))
    
    # add the end location to each permutation, if we have an end location
    if end_location is not None:
        logger.info("Adding %s to permutations", end_location)
        journey_perms = [tuple(list(journey) + [end_location]) for journey in journey_perms]
    
    if start_location is not None:
        journey_perms = [journey for journey in journey_perms if journey[0] == start_location]
        logger.info("Starting from location 0, a total of %d journey permutations", len(journey_perms))
        
    logger.debug("Journey permutations:\n%s", journey_perms)
 
    journey_distances = {}
    
    for journey in journey_perms:
        # where a journey might be, say, (2, 3, 4, 1, 0)
        journey_distance = 0
        for i in range(len(journey)-1):
            leg_start = journey[i]
            leg_end = journey[i+1]
            
            # This filter should only return the single leg with matching start and end locations
            leg = list(filter(lambda l: l.start == leg_start and l.end == leg_end, leg_to_distance))[0]
            journey_distance += leg.distance
        
        journey_distances[journey] = journey_distance
    
    logger.debug("Journey distances:\n%s", journey_distances)
    return journey_distances


def get_shortest_paths(layout:list[str], 
                       locations_to_visit:dict[int,complex], 
                       combos:list[tuple[int, int]]) -> dict[tuple, int]:
    """ Use BFS to find the shortest path between each pair of locations.

    Args:
        layout ([str]): The layout (maze)
        locations_to_visit (dict[int, complex]): The locations we need to visit, with coords
        combos (list[tuple[int, int]]): List of all combinations of locations

    Returns:
        dict[tuple, int]: distance between this pair of points
    """
    distances:dict[tuple, int] = {}    # store the shortest path between nodes
    
    # for each pair of locations...
    for location_pair in combos:
        goal = locations_to_visit[location_pair[1]]
        start = locations_to_visit[location_pair[0]]
        layout_state = LayoutState(layout=layout, goal=goal, position=start)
        
        queue:list[LayoutState] = []            # for our heapq
        explored_states = set()
        heapq.heappush(queue, layout_state)     # initial state
        explored_states.add(layout_state)       # label initial state as explored
        
        while queue:
            layout_state = heapq.heappop(queue) # pop highest priority
            
            if layout_state.position == goal:   # shortest path found
                distances[location_pair] = len(layout_state.path)
                break
            
            for new_layout_state in layout_state.yield_next_state():
                if new_layout_state not in explored_states:
                    explored_states.add(new_layout_state)
                    heapq.heappush(queue, new_layout_state)
                    
    return distances


if __name__ == "__main__":
    t_1 = time.perf_counter()
    main()
    t_2 = time.perf_counter()  
    logger.info("Execution time: %0.4f seconds", t_2 - t_1)  
