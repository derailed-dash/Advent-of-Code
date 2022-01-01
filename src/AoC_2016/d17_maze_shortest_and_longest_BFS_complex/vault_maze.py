"""
Author: Darren
Date: 01/02/2021

Solving https://adventofcode.com/2016/day/17

4x4 grid of rooms connected by doors. Start top left.
Need to get to vault in the bottom right. 
Whether the doors are open or locked depends on the hex value of an MD5 checksum,
which is computed based on the path taken so far.
Thus, a door can be closed on the first pass through a room, but be open on another pass.

Doors are closed or open based on hex MD5 hash of seed + chars representing path so far.
- Path given by U, D, L or R.
The first 4 chars of hash tell us which doors are unlocked from current position
- I.e. First 4 chars = UDLR
- 0-9, a = closed
- b-f = open

Solution:
    Define a MazeState class, which has dimensions, start, goal, current position, and path to current. 
    Position and goal are stored using complex numbers, since this is convenient for 2D coords.
    Priority is given by distance from goal.  We can use this in our heapq when implementing BFS.
    Distance from goal is abs of resulting complex number, i.e. subtracting current from goal.
    Path to current is a str of moves so far.
    
    MazeState has a generator that yields all possible valid next states, 
    based on whether the move would take us outside of the maze, and whether the door is unlocked.
    
    Note that when we do the BFS, we don't a MazeState to be unique based on current location.
    The path so far is crucial.  Thus, hash and equality are based on both position and path.

Part 1:
    Conduct a BFS using a heapq.  Store MazeState objects in the heapq.
    If the MazeState has reached the goal, store the path as a solution.
    Since we're only interested in the shortest solution, if any popped MazeState
    has a path at least as long as any existing solution, then skip it.
    Identify the solution with shortest path.
    
    Runs in about 10ms!

Part 2:
    Now we want to find the longest path to the solution.
    We no longer want to skip MazeState objects that have a longer path than existing solutions.
    Continue to store all solutions found.
    Identify the solution with the longest path, i.e. using max where ken=len.
    
    Now it takes about 1s.
"""
from __future__ import annotations
import heapq
import hashlib
import logging
import os
import time

# pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT = "pslxynzg"

class MazeState:
    """ Represents a maze, with the current maze position 
    and the path to get to the current position. 
    
    The MazeState can be used in a priority heap queue, 
    since the distance from the current location to the goal will be the priority. """
    
    # sequence is important, because it matches first four chars of hex md5: U, D, L, R
    VECTORS = {
        'U': 0-1j,
        'D': 0+1j,
        'L': -1+0j,
        'R': 1+0j
    }
     
    def __init__(self, dims: tuple, seed, goal: complex, position=0+0j, path=None) -> None:
        """ 
        Path is the journey taken so far, to get to this location, in terms of VECTORS. 

        Args:
            dims ([tuple]): x,y dimentions of this maze
            goal ([complex]): the maze position we need to reach
            seed ([str]): Prefixed to the path, when generating hexadecimal MD5 values.
            path ([str], optional): journey taken so far, to get to this location, in terms of VECTORS.
        """
        self._dims = dims
        self._position = position
        self._seed = seed
        self._goal = goal
        
        if path is None:
            self._path = ""
        else:
            self._path = path
    
    @property
    def dims(self):
        """ Tuple of maze dimensions, in the format (cols, rows). """
        return self._dims
            
    @property
    def position(self):
        """ The current position in the maze. """
        return self._position
    
    @property
    def goal(self):
        """ The maze coordinate we need to get to. """
        return self._goal    
    
    @property
    def path(self):
        """ A growing string, representing the path taken so far.  E.g. D, L, R, R, D, etc. """
        return self._path
    
    @property
    def seed(self):
        return self._seed
    
    @property
    def priority(self):
        """ Priority is given by GOAL - position. Thus, lowest value represents highest priority. """
        return round(abs(self.goal - self.position), 1)
    
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}" +
            f"(dims={self.dims},posn={str(self.position)},path={self.path},priority={self.priority})")
    
    def __str__(self) -> str:
        return f"posn={self.position}, path={self.path}, priority={self.priority}, md5={self._hex_md5_hash()}"
    
    def __eq__(self, o) -> bool:
        """ Equality is based on current position and path """
        if isinstance(o, MazeState):
            return self.position == o.position and self.path == o.path
        else:
            return NotImplemented
    
    def __hash__(self) -> int:
        """ Hash is based on tuple of the current position and path """
        return hash((self.position, self.path))
    
    def __lt__(self, o) -> bool:
        return self.priority < o.priority
    
    def yield_next_state(self):
        for index, vector in enumerate(MazeState.VECTORS):
            new_position = MazeState.VECTORS[vector] + self.position
            hex_md5_hash_char = self._hex_md5_hash()[index]
            
            # First, let's iterate through U, D, L, R and see if there are adjacent rooms
            if (0 <= new_position.real < self.dims[0]
                    and 0 <= new_position.imag < self.dims[1]):
                
                # Now let's test if the door to that room is open or locked
                # Only yield open routes
                if self.is_open(hex_md5_hash_char):
                    new_path = self.path + vector
                    yield MazeState(dims=self.dims, goal=self.goal, seed=self.seed, position=new_position, path=new_path)    
    
    def _hex_md5_hash(self) -> str:
        """ Computes the hex MD5 of the combination of the seed and path.
        
        Returns:
            str: first four chars of hex representation of md5, to represent U, D, L, R """
        md5_hash = hashlib.md5((self.seed + self.path).encode()).hexdigest()
        return md5_hash[:len(MazeState.VECTORS)]
    
    @staticmethod
    def is_open(hex_char: str) -> bool:
        """ Takes any hex value.  If 0-9 or a, then this door is closed.
        If b-f (inclusive), then this door is open """
        if str.isdigit(hex_char) or hex_char == "a":
            return False
    
        return True
    
def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
    input_data = INPUT
    
    destination = 3+3j
    shortest_solution_only = False
    
    init_maze_state = MazeState(dims=(4,4), seed=input_data, goal=destination)
    queue:list[MazeState] = []  # heap queue
    explored_states = set()
    heapq.heappush(queue, init_maze_state)
    explored_states.add(init_maze_state)
        
    solutions_found = []
    while queue:
        maze_state = heapq.heappop(queue)
        
        # If we're only interested in the shortest solution (fast)
        if shortest_solution_only and solutions_found: 
            shortest_solution_length = len(min(solutions_found, key=len))
            if len(maze_state.path) >= shortest_solution_length:
                # If we already have a solution and the current path is longer than the solution, skip it
                continue
        
        if maze_state.position == destination:
            # We've found our first solution, or a shorter solution than the one we had before
            solutions_found.append(maze_state.path)
            continue
        
        for new_maze_state in maze_state.yield_next_state():
            if new_maze_state not in explored_states:
                explored_states.add(new_maze_state)
                heapq.heappush(queue, new_maze_state)
    
    if solutions_found:
        shortest_solution = min(solutions_found, key=len)
        longest_solution = max(solutions_found, key=len)
        logging.info(f"Part 1: shortest solution found={shortest_solution} with length {len(shortest_solution)}")        
        logging.info(f"Part 2: longest solution found has length {len(longest_solution)}")
    else:
        logging.info("Part 1: No solution found!")
        
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
