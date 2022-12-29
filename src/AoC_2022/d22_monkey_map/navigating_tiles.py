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

The final password is the sum of 1000 times the row, 4 times the column, and the last facing.
Note that rows and columns are 1-indexed.
Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).

Part 1:

What is the final password?

Soln:
- Store a map of vectors to >, v, < and ^, which can be indexed by 0, 1, 2, 3.
- Map class instantiated from the input grid.
- Stores current position, current direction, and the path taken, made up of (Point, direction).
- Processes two types of instruction:
  - change_direction: if R, select the (n+1)%4 vector. If left, select (n+3)%4 vector.
  - move_forward:
    - Determine what the next position would be by adding the appropriate vector.
    - If the candidate is in the grid and not a space, then this is a valid candidate.
      If not blocked, move there.
    - If the candidate is not in the grid or is a space, then we need to re-enter from the other side.
      We do this by reversing direction and moving all the way to the opposite edge. 
      Then reverse direction again, so we're still facing the right way.

Part 2:

- We need to map all the edges.

"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

class Colours(Enum):
    """ ANSI escape sequences for coloured console output """
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
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
        
    def __str__(self):
        return f"P({self.x}, {self.y})"

DIRECTION_SYMBOLS = ['>', 'v', '<', '^']  # Orientation vector key
VECTOR_COORDS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
VECTORS = {k: Point(*v) for k, v in enumerate(VECTOR_COORDS)} # so we can retrieve by index
         
class Map(): 
        
    def __init__(self, grid: list[str]) -> None:
        self._grid = grid
        self._width = max(len(line) for line in self._grid) # the widest line
        self._pad_grid() # make all rows same length
        self._cols = self._generate_cols()
        self._set_start() # Initialise top-left, pointing right
        self._last_instruction = "" # just to help with debugging
    
    def _generate_cols(self):
        """ Create a list of str, where each str is a column.
        E.g. first col could be '    ....    '
        """
        cols_list = list(zip(*self._grid))
        return ["".join(str(char) for char in col) for col in cols_list]
        
    def _set_start(self):
        """ Start position is first open space on the grid, 
        starting at (0, 0) - which could be in 'emtpy' space, and moving right. """
        first_space = self._grid[0].find(".")
        self._posn = Point(first_space, 0)
        self._direction = 0  # index of ['>', 'v', '<', '^']
        self._path = {self._posn: self._direction} # Everywhere we've been, including direction

    def _pad_grid(self):
        """ Make all rows are the same length. """
        lines = []
        for line in self._grid:
            if len(line) < self._width:
                line += " " * (self._width - len(line))
            lines.append(line)
            
        self._grid = lines
        
    @property
    def posn(self) -> Point:
        """ Point coordinate of the current position. """
        return self._posn
    
    def move(self, instruction: str):
        """ Can be direction instruction, i.e. L or R, or a move forward instruction, e.g. 10 """
        self._last_instruction = instruction
        if instruction.isdigit():
            self._move_forward(int(instruction))
        else:
            self._change_direction(instruction)
    
    def _change_direction(self, instruction):
        """ Rotate to the left or the right, relative to current orientation. """
        change = 1 if instruction == "R" else 3 # add 3 rather than -1, to avoid negative mod
        self._direction = (self._direction+change) % len(VECTORS)
        self._path[self._posn] = self._direction # update direction in the path
        
    def _move_forward(self, steps: int):
        """ Move in the current direction until we hit an obstacle. """
        for _ in range(steps):
            candidate_next = self._next_posn()
            if self._is_possible(candidate_next):
                self._posn = candidate_next
                self._path[self._posn] = self._direction # update direction in path
            else: # we need to stop here
                break
    
    def _get_row_length(self, row_num: int):
        return len(self._grid[row_num]) - self._grid[row_num].count(" ")
    
    def _get_col_length(self, col_num: int):
        return len(self._cols[col_num]) - self._cols[col_num].count(" ")

    def _next_posn(self) -> Point:
        """ Determine next Point in this direction, including wrapping. Does not check if blocked. """
        
        next_posn = self._posn + VECTORS[self._direction]
        if not self._is_tile(next_posn): # we're off the tiles, so we need to wrap
            # Subtract vector in the opposite direction equal to the length of the row / col
            new_x = next_posn.x - VECTORS[self._direction].x * self._get_row_length(self._posn.y)
            new_y = next_posn.y - VECTORS[self._direction].y * self._get_col_length(self._posn.x)
            next_posn = Point(new_x, new_y)
        
        return next_posn
    
    def _is_tile(self, point: Point) -> bool:
        """ Check if the specified point is a tile. I.e. within the bounds and not empty. """
        if point.y < 0 or point.y >= len(self._grid):
            return False
                
        # check not outside the bounds of the current row. (Allow for variable length row)
        if point.x < 0 or point.x >= len(self._grid[point.y]):
            return False
        
        # If we've got this far, we're within the bounds of the input data, but it could still be empty
        if self._get_value(point) == " ":
            return False
        
        return True
        
    def _get_value(self, point: Point) -> str:
        """ The value of the grid at the specified point. """
        return self._grid[point.y][point.x]
        
    def _is_possible(self, locn: Point):
        """ Check if this space is open. Only '.' counts as open. """
        return True if self._get_value(locn) == "." else False
        
    def score(self) -> int:
        """ Score is given by sum of: (1000*y), (4*x), facing. 
        For this calculation, x and y are 1-indexed. Facing = direction index. """
        return 1000*(self.posn.y+1) + 4*(self.posn.x+1) + self._direction
        
    def __str__(self) -> str:
        lines = []
        for y, row in enumerate(self._grid):
            line = ""
            for x, val in enumerate(row):
                posn = Point(x,y)
                if posn in self._path:
                    line += Colours.CYAN.value + DIRECTION_SYMBOLS[self._path[posn]] + Colours.RESET.value
                else:
                    line += val
                    
            lines.append(line)
            
        return "\n".join(lines)

    def __repr__(self):
        return f"Map(posn={self.posn}, last_instr={self._last_instruction}, score={self.score()})"

class CubeMap(Map):
    def __init__(self, grid: list[str]) -> None:
        super().__init__(grid)
        
    def _create_faces(self):
        pass

def main():
    with open(INPUT_FILE, mode="rt") as f:
        map_data, instructions = f.read().split("\n\n")
        
    map_data = map_data.splitlines()
    the_map = Map(map_data)
    
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

        the_map.move(this_instr)
        # print(repr(the_map))
    
    print(the_map)
    print(f"Part 1: score={the_map.score()}")
            
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
