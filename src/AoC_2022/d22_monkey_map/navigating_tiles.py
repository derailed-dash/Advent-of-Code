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

- Instead of wrapping left-to-right, or top-to-bottom, we now need to wrap around cube faces.
- Extend our Map class with a new CubeMap class. Most of the work is done by overriding _next_posn().
- Externalise the cube geometry into a separate file, which contains cube 'face coordinates'
  and edge mappings. I.e. for all edges where folding would be required in more than one plane. 
- I.e. if we're leaving face n in direction x, what face do we arrive at, 
  and what new direction are we facing?  This is visualised in the associated diagram, 
  and represented in the externalised file which can be read in using literal_eval().
- Map the face coordinate to the arrival coordinate in the new face.
- Then convert this 'face coordinate' back to an overall grid coordinate.
"""
from __future__ import annotations
from ast import literal_eval
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_CUBE = Path(SCRIPT_DIR, "input/sample_cube_in.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
INPUT_CUBE = Path(SCRIPT_DIR, "input/cube_in.txt")

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
VECTORS = [Point(*v) for v in VECTOR_COORDS] # so we can retrieve by index
         
class Map(): 
    """ 2D grid map. Follows 'move' instructions, which can either be a L/R rotation,
    or n steps forward in the current orientation. If we step off a tile into the abyss, 
    we wrap around to the opposite edge. Stores the path taken, and uses it to evaluate a total 'score'. """
    def __init__(self, grid: list[str]) -> None:
        self._grid = grid # store original input grid
        
        self._height = len(self._grid) 
        self._width = max(len(line) for line in self._grid) # the widest line
        self._grid = self._pad_grid() # make all rows same length
        self._cols = self._generate_cols()
        
        self._staert = Point(0,0)
        self._posn = Point(0,0)
        self._direction = 0
        self._path = {} # key=point, value=direction
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
        self._start = self._posn
        self._direction = 0  # index of ['>', 'v', '<', '^']
        self._path = {self._posn: self._direction} # Everywhere we've been, including direction

    def _pad_grid(self):
        """ Make all rows are the same length. """
        return [line + " " * (self._width - len(line)) if len(line) < self._width else line for line in self._grid]
        
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
            candidate, new_dir = self._next_posn()
            if self._is_possible(candidate):
                self._posn = candidate
                self._direction = new_dir
                self._path[self._posn] = self._direction # update direction in path
            else: # we need to stop here
                break
    
    def _get_row_length(self, row_num: int):
        return len(self._grid[row_num]) - self._grid[row_num].count(" ")
    
    def _get_col_length(self, col_num: int):
        return len(self._cols[col_num]) - self._cols[col_num].count(" ")

    def _next_posn(self) -> tuple[Point, int]:
        """ Determine next Point in this direction, including wrapping. Does not check if blocked. """
        
        next_posn = self._posn + VECTORS[self._direction]
        if not self._is_tile(next_posn): # we're off the tiles, so we need to wrap
            # Subtract vector in the opposite direction equal to the length of the row / col
            new_x = next_posn.x - VECTORS[self._direction].x * self._get_row_length(self._posn.y)
            new_y = next_posn.y - VECTORS[self._direction].y * self._get_col_length(self._posn.x)
            next_posn = Point(new_x, new_y)
        
        return next_posn, self._direction
    
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
                if posn == self._posn:
                    line += (Colours.RED.value + Colours.BOLD.value 
                            + DIRECTION_SYMBOLS[self._path[posn]] + Colours.RESET.value)
                elif posn == self._start:
                    line += (Colours.YELLOW.value + Colours.BOLD.value 
                            + DIRECTION_SYMBOLS[self._path[posn]] + Colours.RESET.value)
                elif posn in self._path:
                    line += Colours.CYAN.value + DIRECTION_SYMBOLS[self._path[posn]] + Colours.RESET.value
                else:
                    line += val
                    
            lines.append(line)
            
        return "\n".join(lines)

    def __repr__(self):
        return f"Map(posn={self.posn}, last_instr={self._last_instruction}, score={self.score()})"

class CubeMap(Map):
    """ Take a 2D grid that is made up of 6 regions, and convert to a cube.
    The face coordinates of the Cube, and its edge mappings, must be supplied. """
    
    def __init__(self, grid: list[str], face_coords: list[tuple], face_edge_map: dict[tuple, tuple]) -> None:
        super().__init__(grid)
        
        self._face_coords = face_coords # the coordinates of the top-left vertices of this cube
        self._face_edge_map = face_edge_map

        self._h_faces_width = max(x for x,y in self._face_coords) + 1 # e.g. 4 faces wide
        self._v_faces_height = max(y for x,y in self._face_coords) + 1 # e.g. 3 faces tall
        self._face_width = self._width // self._h_faces_width # E.g. 4, or 50 with real
        self._face_height = self._height // self._v_faces_height # E.g. 4 or 50 with real"
        assert self._face_width == self._face_height, "Faces should be squares!"
        
    def _origin_face(self) -> int:
        """ Get the face number (index) that this point lives in """
        face_x = self._posn.x // self._face_width
        face_y = self._posn.y // self._face_width
        
        return self._face_coords.index((face_x, face_y))
        
    def _next_posn(self) -> tuple[Point, int]:
        """ Determine next Point in this direction, including wrapping. Does not check if blocked. """
        
        next_posn = self._posn + VECTORS[self._direction]
        next_dir = self._direction
        
        if not self._is_tile(next_posn): 
            # we're off the tiles, so we need to wrap around the cube
            next_posn, next_dir = self._next_face_point()
        
        return next_posn, next_dir

    def _next_face_point(self) -> tuple[Point, int]:
        """ A face point is an x,y point within the current face only. 
        We return the new face point, and the new direction we're pointing in, 
        having changed face. """
        dest_face, dest_direction = self._face_edge_map[(self._origin_face(), self._direction)]
        # print(f"Moving to face {dest_face}, with direction={DIRECTION_SYMBOLS[dest_direction]}")
        
        current_face_x = self.posn.x % self._face_width
        current_face_y = self.posn.y % self._face_height
        other = 0
        dest_face_point = Point(0,0)
        
        match self._direction: # which way are we currently going?
            case 0: # >
                assert current_face_x == self._face_width - 1, "We must be on a right edge"
                other = current_face_y
            case 1: # v
                assert current_face_y == self._face_height - 1, "We must be on a bottom edge"
                other = self._face_width - 1 - current_face_x
            case 2: # <
                assert current_face_x == 0, "We must be on a left edge"
                other = self._face_height - 1 - current_face_y
            case 3: # ^
                assert current_face_y == 0, "We must be on a top edge"
                other = current_face_x
                
        match dest_direction: # which way will we be going? 
            case 0: # >
                dest_face_point = Point(0, other)
            case 1: # v
                dest_face_point = Point(self._face_height - 1 - other, 0)
            case 2: # <
                dest_face_point = Point(self._face_height - 1, self._face_width - 1 - other)
            case 3: # ^
                dest_face_point = Point(other, self._face_width - 1)
        
        # convert face point to grid point
        return (self._face_point_to_grid_point(dest_face_point, dest_face), dest_direction)

    def _face_point_to_grid_point(self, face_point: Point, face: int) -> Point:
        """ Converts a point relative to a face back to an overall grid point. """
        return Point(face_point.x + self._face_coords[face][0]*self._face_width, 
                     face_point.y + self._face_coords[face][1]*self._face_height)
    
def main():
    with open(INPUT_FILE, mode="rt") as f:
        map_data, instructions = f.read().split("\n\n") # input is two blocks, separated by a line
        
    with open(INPUT_CUBE, mode="rt") as f:  # read in Cube input, in Python list format
        cube_data = literal_eval(f.read())
                
    map_data = map_data.splitlines()
    
    # Part 1 - 2D map
    the_map = Map(map_data)
    process_instructions(instructions, the_map)
    # print(the_map)
    print(f"Part 1: score={the_map.score()}")
    
    # Part 2 - Cube
    cube = CubeMap(map_data, face_coords=cube_data[0], face_edge_map=cube_data[1])
    process_instructions(instructions, cube)
    print(f"Part 2: score={cube.score()}")

def process_instructions(instructions, the_map):
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
            
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
