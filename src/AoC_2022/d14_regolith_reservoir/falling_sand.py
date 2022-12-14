"""
Author: Darren
Date: 14/12/2022

Solving https://adventofcode.com/2022/day/14

Grains of sand falling from point (500,0). 
Input is in the form of points that make vert and horizontal lines of rock.

Part 1:

How many units of sand come to rest before sand starts flowing into the abyss below?

Soln:
- Read the input to construct lines. Line class with start and end.
- Create instance of Grid class.
  - Get points that make up the lines, and store them in a set for rock.
  - Create empty set for where sand falls and comes to rest.
  - Union these two sets for "filled".
  - drop_sand() method:
    - Drops sand grain from the top.
    - Sand grain falls according to rules, specified as three vectors: down, down-left, down-right.
    - Iterate through vectors. Candidate point is current sand grain point, plus vector.
    - If candidate point is empty, the sand can fall to it.  If not, sand has stopped falling.
    - Keep iterating until sand stops falling.
    - If sand has come to rest, return the grain point. If not, then return None.
- Back in main(), call drop_sand() until no more grains returned. Then count grid.sand.

Part 2:

We now have a floor, at location y+2 relative to lowest rock. 
Sand will keep falling until we've blocked the origin at (500,0).

How many units of sand come to rest?

Soln:

- __init__() now accepts a parameter to set whether we have a floor or not.
  If we do, set the floor_y accordingly, and update other limits.
- Update is_empty() to now return False if the point.y location is the floor.
- Update drop_sand() method:
  - If we have a floor and sand has come to rest there, update x and y limits if required.
  - After adding sand to our internal sets, if the grain added was the same as the ORIGIN,
    then this is the last grain we can drop, so return None.
"""
from dataclasses import dataclass
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
OUTPUT_FILE = Path(SCRIPT_DIR, "output/output.png")

@dataclass(frozen=True)
class Point():
    x: int
    y: int
    
@dataclass(frozen=True)
class Line():
    start: Point
    end: Point
    
class Grid():
    SAND_ORIGIN = Point(500,0)
    SAND_VECTORS = [Point(0,1), Point(-1, 1), Point(1, 1)] # down, diagonal left, diagonal right
    
    def __init__(self, lines: set[Line], floor=False) -> None:
        self.rock: set[Point] = self._get_rock(lines)
        self.sand = set()
        self.filled = self.rock | self.sand  # union of two sets
        self.min_x = min(point.x for point in self.filled)
        self.max_x = max(point.x for point in self.filled)
        self.min_y = min(point.y for point in self.filled)
        self.max_y = max(point.y for point in self.filled)
        self._set_floor(floor)

    def _set_floor(self, floor: bool):
        self._floor = floor
        self._floor_y = self.max_y + 2
        self.max_y = self._floor_y        
        
    def _get_rock(self, lines: set[Line]):
        """ Process lines of rock. For each point in those lines, add a rock point to the set. """
        rock = set()
        for line in lines:
            x_start = min(line.start.x, line.end.x)
            x_end = max(line.start.x, line.end.x)
            y_start = min(line.start.y, line.end.y)
            y_end = max(line.start.y, line.end.y)
            rock.update({Point(x,y) for x in range(x_start, x_end+1)
                                    for y in range(y_start, y_end+1)})
        
        return rock
    
    def _is_empty(self, point: Point) -> bool:
        """ If this point is not rock or sand, return True. """
        if point not in self.filled:
            if self._floor:
                if point.y == self._floor_y:
                    return False
            return True
        
        return False
    
    def drop_sand(self) -> Point:
        """ Sand falls down until it reaches an obstacle.
        If it reaches an obstacle, it will they try to fall diagonally left, then diagonally right. """
        grain = Grid.SAND_ORIGIN
        falling = True
        while falling:
            for v in Grid.SAND_VECTORS:
                candidate = Point(grain.x + v.x, grain.y + v.y)
                if self._is_empty(candidate):
                    if not self._floor and candidate.y == self._floor_y: # we've reached fall-through
                        return None
                    else: # there is a floor; expand the grid
                        self.min_x = min(self.min_x, grain.x - 1)
                        self.max_x = max(self.max_x, grain.x + 1)
                        self.min_y = min(self.min_y, grain.y)
                    
                    grain = candidate
                    self.min_y = min(self.min_y, grain.y)

                    break  # move out of the vectors loop
            else: # Get here if all our fall positions are full
                falling = False

        self._add_sand(grain)
        if grain == Grid.SAND_ORIGIN:
            return None                  
        
        return grain

    def _add_sand(self, grain):
        self.sand.add(grain)
        self.filled.add(grain)
    
    def __str__(self) -> str:
        rows = []
        for y in range(self.min_y, self.max_y+1):
            row = f"{y:3d} "
            
            # print 1 col to either side
            for x in range(self.min_x-1, self.max_x+2):
                point = Point(x,y)
                if point in self.rock:
                    row += "#"
                    continue
                if self._floor and y == self._floor_y:
                    row += "#"
                    continue
                if point in self.sand:
                    row += "o"
                    continue
                row += "."
            
            rows.append(row)
            
        return "\n".join(rows)

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    lines = process_lines(data)
    
    # Part 1
    grid = Grid(lines)
    
    adding_sand = True
    while adding_sand:
        adding_sand = grid.drop_sand()
        # print(f"\n{grid}")
    
    print(f"Part 1: resting grains={len(grid.sand)}")
    
    # Part 2
    grid = Grid(lines, floor=True)
    adding_sand = True    
    while adding_sand:
        adding_sand = grid.drop_sand()
        # print(f"\n{grid}")
        
    print(f"Part 2: resting grains={len(grid.sand)}")        
        
def process_lines(data):
    lines = set()
    for input_line in data:
        point_coords = input_line.split(" -> ")
        points = [Point(*map(int, coord.split(","))) for coord in point_coords]
        for i in range(1, len(points)):
            lines.add(Line(points[i-1], points[i]))
    
    return lines

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
