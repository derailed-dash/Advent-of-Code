"""
Author: Darren
Date: 18/12/2022

Solving https://adventofcode.com/2022/day/18

We are examining surface area of a lava droplet. The droplet is made up of many 1x1x1 cubes.
The input is a list of these cubes.

Part 1:

Count total exposed surface area.

Soln:
- Cube class knows how to find location of all six adjacent cubes.
- Each cube has a surface area of 6 - (intersection of cube adjacents with all cubes)

Part 2:

What is the exterior surface area of your scanned lava droplet?
We're told steam wont expand diagonally.

Soln:

- We now need to ignore internal pockets that are sealed to the outside.
- We need to know if a empty location is interior and if it has a path to the outside.
- Assume all cubes in our list are connected.
- Find all adjacent cubes that are not in our list:
  - These are either:
    - Part of internal pockets. If we flood fill a pocket, it will have a boundary.
    - Part of path to the outside. If we flood fill, we will reach a cube beyond all adjacents.
- To solve:
  - Subtract surface area of all internal pockets.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

@dataclass(frozen=True)
class Cube():
    """ Cube with three dimensions and knows how to return Cube locations at adjacent faces. """
    x: int
    y: int
    z: int

    # To generate deltas only for faces, we need two of three dims to 0
    ADJ_DELTAS = [(dx,dy,dz) for dx in range(-1, 1+1)
                        for dy in range(-1, 1+1) 
                        for dz in range(-1, 1+1)
                        if (dx, dy, dz).count(0) == 2]
    
    def adjacent(self):
        return {Cube(self.x+dx, self.y+dy, self.z+dz) for dx, dy, dz in Cube.ADJ_DELTAS}

@dataclass
class Droplet():
    """ Droplet is a volume of 1x1x1 cubes """
    ADJACENT_FACES = 6
    cubes: set[Cube]
    
    def __post_init__(self) -> None:
        pass
    
    def surface_area(self): 
        return sum(6 - len(self.cubes & cube.adjacent()) for cube in self.cubes)
    
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    droplet = Droplet(parse_cubes(data))
    
    # Part 1
    print(f"Part 1: surface_area={droplet.surface_area()}")

    # Part 2

        
    
def parse_cubes(data: list[str]) -> set[Cube]:
    cubes = set()
    for line in data:
        coords = tuple(map(int, line.split(",")))
        cubes.add(Cube(*coords))
    
    return cubes
    
def bfs(cubes):
    pass
    

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
