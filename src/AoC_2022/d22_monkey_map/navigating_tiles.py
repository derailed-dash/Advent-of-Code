"""
Author: Darren
Date: 22/12/2022

Solving https://adventofcode.com/2022/day/22

We're given a strange map and instructions to navigate it.
We have to follow a specific path. Start top left, facing right.

Input is two parts:
1. A map composed of locations, called tiles. Tiles are open spaces or obstacles.
   We also have positions that are not part of the navigable map.
2. A sequence of alternating numbers and letters:
   Number = move forward n tiles; stop if you hit an obstacle.
   Letter = turn L or R, at current position.
   
If we go off the map, we reappear the other side. (Assuming not blocked.)

The final password is the sum of 1000 times the row, 4 times the column, and the facing.
Note that rows and columns are 1-indexed.
Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).

Part 1:

What is the final password?

Part 2:

"""
from __future__ import annotations
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
    
    def __add__(self, other):
        """ Subtract other point from this point, returning new point vector """
        return Point(self.x + other.x, self.y + other.y)
    
    def neighbours(self) -> list[Point]:
        """ Return all adjacent orthogonal (not diagonal) Points """
        return [Point(self.x+dx, self.y+dy) for dx in range(-1, 2)
                                            for dy in range(-1, 2)
                                            if abs(dy) != abs(dx)]

DIRECTION_SYMBOLS = ['>', 'v', '<', '^']
VECTOR_COORDS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
VECTORS = {k: Point(*v) for k, v in enumerate(VECTOR_COORDS)} # so we can retrieve by index

class Map():    
    def __init__(self, grid: list[str]) -> None:
        self._grid = grid
        self._set_start()
    
    def _set_start(self):
        """ Start position is first open space on the grid, starting at (0, 0) 
        and moving right. """
        first_space = self._grid[0].find(".")
        self._posn = Point(first_space, 0)
        self._direction = 0  # index of ['>', 'v', '<', '^']
        self._path = {self._posn: self._direction}
        
    @property
    def posn(self) -> Point:
        return self._posn
    
    def move(self, instruction: str):
        """ E.g. R or 10 """
        if instruction.isdigit():
            self._move_forward(int(instruction))
        else:
            self._change_direction(instruction)
    
    def _change_direction(self, instruction):
        change = 1 if instruction == "R" else 3 # add 3 rather than -1, to avoid negative mod
        self._direction += change
        self._direction %= len(VECTORS)
        self._path[self._posn] = self._direction # update direction in path
        
    def _move_forward(self, steps: int):
        """ Move in the current direction until we hit an obstacle. """
        for _ in range(steps):
            candidate_next = self._next_posn()
            if self._is_possible(candidate_next):
                self._posn = candidate_next
                self._path[self._posn] = self._direction # update direction in path
            else: # we need to stop here
                break
            
    def _next_posn(self) -> Point:
        """ Determine next Point in this direction, including wrapping. Does not check if blocked. """
        
        # To check wrap, see if next space is a tile.
        # If not, then move in the opposite direction until we reach a non-tile.
        next_posn = self._posn + VECTORS[self._direction]
        if not self._in_grid(next_posn) or self._get_value(next_posn) == " ": # we're off the tiles
            look_back_dir = (self._direction + 2) % len(VECTORS) # set the vector to be opposite
            next_posn = self._posn + VECTORS[look_back_dir] # first move backwards
            while self._in_grid(next_posn) and self._get_value(next_posn) != " ": # keep going 
                next_posn += VECTORS[look_back_dir] # until we find the first off-tile in the opposite direction
        
            # And now step back one to get the tile we need to apear on
            next_posn += VECTORS[self._direction]
        
        return next_posn
    
    def _in_grid(self, point: Point) -> bool:
        if point.y < 0 or point.y >= len(self._grid):
            return False
                
        # check not outside the bounds of the current row
        if point.x < 0 or point.x >= len(self._grid[point.y]):
            return False
        
        return True
        
    def _get_value(self, point: Point) -> str:
        return self._grid[point.y][point.x]
        
    def _is_possible(self, locn: Point):
        """ Check if this space is open """
        return True if self._get_value(locn) == "." else False
        
    def score(self) -> int:
        return 1000*(self.posn.y+1) + 4*(self.posn.x+1)+self._direction
        
    def __str__(self) -> str:
        lines = []
        for y, row in enumerate(self._grid):
            line = ""
            for x, val in enumerate(row):
                posn = Point(x,y)
                if posn in self._path:
                    line += DIRECTION_SYMBOLS[self._path[posn]]
                else:
                    line += val
                    
            lines.append(line)
            
        return "\n".join(lines)

def main():
    with open(INPUT_FILE, mode="rt") as f:
        the_map, instructions = f.read().split("\n\n")
        
    the_map = Map(the_map.splitlines())
    
    # process the instructions
    next_transition = 0
    this_instr = "" 
    for i, char in enumerate(instructions):
        if i < next_transition:
            continue
        if char.isdigit():
            for j, later_char in enumerate(instructions[i:len(instructions)], i):
                if not later_char.isdigit():
                    next_transition = j
                    this_instr = instructions[i: next_transition]
                    break
                else:   # we've reached the end
                    this_instr = instructions[i]    
        else:   # we're processing alphabetical characters
            this_instr = instructions[i]

        # print(f"Instr: {this_instr}")
        the_map.move(this_instr)
    
    print(the_map)
    print(f"Part 1: score={the_map.score()}")
            
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
