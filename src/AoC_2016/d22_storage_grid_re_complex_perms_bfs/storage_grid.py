"""
Author: Darren
Date: 12/10/2021

Solving https://adventofcode.com/2016/day/22

Rectangular storage grid where each node is surrounded by four others, i.e. L, R, U, D.
We can only access data in top left (x=0, y=0).
But we can also MOVE data between any adjacent nodes,
if there is available capacity for such a move.
(Sending node is left empty.)

Part 1:
    Find viable node pairs, where a pair is any two nodes A, B where:
        A is not empty ("Used")
        A and B are not the same node
        A data will fit onto B ("Avail")
    
    Extract all coords, as well as size, used and avail, from the input using regex.
    Save all storage nodes in a dict.
    Convert each storage node x, y coord to a complex number, to use as keys.
    Save the [size, used, avail] as the value.
    
    Then use itertools.permutations to find all pairs of nodes.
    Then apply logic above.

Part 2:
    Find the shortest path to get the goal data to the accessible node.
    
    We want to gain access to data in top right, i.e. (max x, 0).
    We'll call this the Goal (G).
    Thus, we need to move the data in this node through the array,
    until it reaches top left (0,0).
    
    There's a strong hint that we have an empty node,
    and that most nodes will fit data on to the empty node.
    We also know that we've got some large immovable nodes.
    
    Printing the grid makes the solution much more obvious.
    
    So we need to move the empty node until it is adjacent to G.
    We can do this with a BFS.
    
    From there, we can keep moving G towards 0,0.
    With each move of G towards 0,0:
        We leave an empty node behind.
        We need to move that empty node so that it on the other side of G.
        Thus, each move requires 5 steps.
    
    Then one final step to place the G data in the accessible node.
"""
from collections import defaultdict
from itertools import permutations
import heapq
import logging
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

# Storage array constants
SIZE = 0
USED = 1 
AVAIL = 2

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class StorageGrid():
    """ Represents the storage grid, with the current empty node position 
    and the path taken to get this state. 
    
    The StorageGrid can be used in a priority heap queue, 
    since the distance from the current empty node to the goal will be the priority. """
    
    IMMOVABLE = "#"
    MOVABLE = "."
    ACCESSIBLE = "A"
    GOAL = "G"
    EMPTY = "_"
    TRAVERSED = "X"
        
    VECTORS = [
        0-1j,
        0+1j,
        -1+0j,
        1+0j
    ]
     
    def __init__(self, nodes, goal: complex, position=0+0j, path=None) -> None:
        """ 
        Path is the journey taken so far, to get to this location, in terms of VECTORS. 

        Args:
            goal (complex): the maze position we need to reach
            position(complex): the current position
            path ([complex]): journey taken so far, to get to this location, as list of VECTORS.
        """
        self._nodes = nodes
        rows = int(max(node.imag for node in nodes))
        cols = int(max(node.real for node in nodes if node.imag == 0))
        
        self._dims = (cols, rows)
        self._position = position
        self._goal = goal
        
        if path is None:
            self._path = []
        else:
            self._path = path
    
    @property
    def nodes(self) -> dict:
        return self._nodes
    
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
        """ Priority is given by GOAL - position. Thus, lowest value represents highest priority. """
        return (abs(self.goal.real - self.position.real) + 
                abs(self.goal.imag - self.position.imag))
    
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}" +
            f"(posn={str(self.position)},path={self.path},priority={self.priority})")
    
    def __str__(self) -> str:
        return f"posn={self.position}, path={self.path}, priority={self.priority}"
    
    def __eq__(self, o) -> bool:
        """ Equality is based on current position """
        if isinstance(o, StorageGrid):
            return self.position == o.position
        else:
            return NotImplemented
    
    def __hash__(self) -> int:
        """ Hash is based on tuple of the current position """
        return hash(self.position)
    
    def __lt__(self, o) -> bool:
        return self.priority < o.priority
    
    def render_grid_as_str(self) -> str:
        """ Print the storage grid.
        A is the accessible storage in 0,0.
        G is the data we need to access, i.e. the goal.
        _ is the empty node that can accommodate data from other nodes.
        . is a node small enough that its data will fit onto the empty node.
        # is a node with too much data to fit on the empty node. 
        X is the path the empty node has traversed. """        
        rows = []
        for y in range(self.dims[1]+1):    # for each row
            row = ""
            for x in range(self.dims[0]+1):   # for each col
                posn = complex(x, y)
                
                if posn in self.path:
                    row += StorageGrid.TRAVERSED
                else:
                    row += self.nodes[posn]
            
            rows.append(row)
        
        return "\n".join(rows)        
    
    def yield_next_state(self):
        for vector in StorageGrid.VECTORS:
            new_position = vector + self.position
            
            # Check if adjcaent node is within the grid
            if (0 <= new_position.real <= self.dims[0]
                    and 0 <= new_position.imag <= self.dims[1]):
                
                # Only yield adjacent positions that are movable
                if self.nodes[new_position] == StorageGrid.MOVABLE:
                    new_path = self.path + [self.position]
                    new_grid = self.nodes.copy()
                    new_grid[self.position] = StorageGrid.MOVABLE
                    new_grid[new_position] = StorageGrid.EMPTY
                    
                    yield StorageGrid(nodes=new_grid, goal=self.goal, position=new_position, path=new_path)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    # /dev/grid/node-x0-y0     90T   69T    21T   76%
    node_pattern = re.compile(r"-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T")    
    storage_nodes = {}
    
    # Part 1
    for line in data:
        if match := node_pattern.search(line):
            x, y, size, used, avail = map(int, match.groups())
            # store x, y coords as a complex number to make dict indexing easy
            storage_nodes[complex(x, y)] = [size, used, avail]
    
    viable_pairs = defaultdict(list)
    
    # get all permutations of storage pairs
    perms = permutations(storage_nodes, 2)  # each perm is a tuple: (key_a, key_b) 
    for perm in perms:
        node_a = storage_nodes[perm[0]]
        node_b = storage_nodes[perm[1]]
        
        # for each storage node pair A and B,
        # find where A used > 0, and A used <= B available
        if node_a[USED] > 0 and node_a[USED] <= node_b[AVAIL]:
            # each node could have multiple other nodes it could be viable with
            viable_pairs[perm[0]].append(perm[1])
    
    viable_pairs_count = sum(len(viable_pairs[node]) for node in viable_pairs)
    logger.info("Viable pairs count = %d", viable_pairs_count)

    # Part 2
    # Where is top right?  I.e. (max, 0)
    max_y = max(node.imag for node in storage_nodes)
    max_x = max(node.real for node in storage_nodes if node.imag == 0)
    top_right_key = complex(max_x, 0) 
    top_right_node = storage_nodes[top_right_key]
    logger.debug("Top right: %s=%s", top_right_key, top_right_node)
    
    # We're told there's going to be an empty one...
    empty_key = [node_key for node_key in storage_nodes if storage_nodes[node_key][USED] == 0][0]
    empty_node= storage_nodes[empty_key]
    logger.debug("Empty node: %s=%s", empty_key, empty_node)
    
    simplified_grid = simplify_grid(storage_nodes, goal=top_right_key, empty=empty_key)
    
    # Now implement the BFS pattern
    # initial state
    grid = StorageGrid(simplified_grid, goal=top_right_key, position=empty_key)
    logger.debug("\n%s", grid.render_grid_as_str())

    queue:list[StorageGrid] = []  # heap queue
    explored_states = set()
    heapq.heappush(queue, grid)     # put the first vertex on the queue
    explored_states.add(grid)       # label as explored
    
    solution_found = False
    while queue:
        grid = heapq.heappop(queue)     # pop the highest priority item
        
        # we've achieved our goal when the empty node is placed next to the goal node
        # on the horizontal
        if (abs(grid.goal.real - grid.position.real) == 1
            and abs(grid.goal.imag - grid.position.imag) == 0):

            solution_found = True
            break
        
        for new_grid in grid.yield_next_state():
            if new_grid not in explored_states:
                explored_states.add(new_grid)
                heapq.heappush(queue, new_grid)
    
    if solution_found:        
        logger.debug("Path to goal:\n%s", grid.render_grid_as_str())
        steps_to_postion_adjacent_to_goal = len(grid.path)
        logger.info("Steps required to move empty node adjacent to goal: %d", 
                    steps_to_postion_adjacent_to_goal)
        
        logger.info("Current position %s", grid.position)
            
        # Now we have the missing node adjacent to the goal (top right),
        # we want to move to the top right data left until it reaches the accessible node.
        # Each move of the goal data requires one goal move,
        # plus 4 additional moves to place the empty node left of the goal
        MOVES_PER_GOAL_SHIFT = 5
        steps_to_shift_goal_data = MOVES_PER_GOAL_SHIFT * grid.position.real
        total_moves_required = (steps_to_postion_adjacent_to_goal
                                + steps_to_shift_goal_data
                                + 1)        

        logger.info("Total steps required: %d", total_moves_required)
    else:
        logger.info("No solution found.")


def simplify_grid(grid: dict, goal: complex, empty: complex) -> dict:
    """ Convert the dict of storage nodes into a simpler representation. 
    Here, we remove all the list data, and replace with simple char representations
    for each storage node in the array. """
    rows = int(max(node.imag for node in grid))
    cols = int(max(node.real for node in grid if node.imag == 0))
    
    new_storage_grid = {}
    
    for y in range(rows+1):    # for each row
        for x in range(cols+1):   # for each col
            posn = complex(x, y)
            storage_type = None
            
            if x==0 and y==0:
                storage_type = StorageGrid.ACCESSIBLE
            elif x==goal.real and y==goal.imag:
                storage_type = StorageGrid.GOAL
            elif x==empty.real and y==empty.imag:
                storage_type = StorageGrid.EMPTY
            elif grid[posn][USED] > grid[empty][SIZE]:
                storage_type = StorageGrid.IMMOVABLE
            else:
                storage_type = StorageGrid.MOVABLE
            
            assert storage_type is not None, "Storage type should not be None"
            new_storage_grid[posn] = storage_type
    
    return new_storage_grid

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
