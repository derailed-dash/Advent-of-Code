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
    - Part of path to the outside. If we flood fill, we will reach a cube beyond all adjacents. No close boundary.
- To solve:
  - Subtract surface area of all internal pockets.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from functools import cache
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

@dataclass(frozen=True)
class Cube():
    """ Cube with three dimensions and knows how to return Cube locations at adjacent faces. """
    x: int
    y: int
    z: int

    # To generate deltas only for faces, we need two of three dims to be 0
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
        self._all_adjacent_positions: set[Cube] = set()  # filled or empty adjacent
        self._adjacent_empty: set[Cube] = set()  # only empty adjacent
        self.all_surface_area: int = 0  # surface area, internal+external
        
        self._calculate_values()
    
    def _calculate_values(self): 
        for cube in self.cubes:
            self._all_adjacent_positions |= cube.adjacent()
            self._adjacent_empty.update(cube for cube in cube.adjacent() if cube not in self.cubes)
            self.all_surface_area += Droplet.ADJACENT_FACES - len(self.cubes & cube.adjacent())
    
    def get_internal_surface_area(self):
        internal_empty_cubes = self._get_internal_space()
        internal_surface_area = 0
        for internal_empty in internal_empty_cubes:
            internal_surface_area += Droplet.ADJACENT_FACES - len(internal_empty_cubes & internal_empty.adjacent())
        
        return internal_surface_area
    
    def _get_internal_space(self):
        """ Process all adjacent empty locations. 
        Find those that don't connect outside and therefore must be internally bound. """
        
        cube_internal = set()  # store all internal empty
        for cube in self._adjacent_empty:   # loop through all adjacent empty
            if not self._external_connect(cube):  # if this empty doesn't connect to outside, it's internal
                cube_internal.add(cube)

        print(f"Internal empty: {cube_internal}")                
        return cube_internal
    
    def _external_connect(self, cube: Cube) -> bool:
        frontier = deque([cube])
        explored = {cube}
        
        while frontier:
            current_cube = frontier.popleft() # FIFO for BFS
            
            # our goal is when this point seems to have no bound
            if len(explored) > 5000:
                return True
            
            # We want to look at all neighbours of this empty space, but only if they are also empty
            for neighbour in current_cube.adjacent():
                if neighbour not in self.cubes:
                    if neighbour not in explored:
                        explored.add(neighbour)
                        frontier.append(neighbour)
                    
        return False
    
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    droplet = Droplet(parse_cubes(data))
    
    # Part 1
    print(f"Part 1: all surface area={droplet.all_surface_area}")

    # Part 2
    internal = droplet.get_internal_surface_area()
    print(f"Part 2: external surface area={droplet.all_surface_area - internal}")
    
def parse_cubes(data: list[str]) -> set[Cube]:
    cubes = set()
    for line in data:
        coords = tuple(map(int, line.split(",")))
        cubes.add(Cube(*coords))
    
    return cubes
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
