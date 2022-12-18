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
    filled_cubes: set[Cube]
    
    def __post_init__(self) -> None:
        self._all_adjacent_positions: set[Cube] = set()  # filled or empty adjacent
        self._adjacent_empty: set[Cube] = set()  # only empty adjacent
        self.all_surface_area: int = 0  # surface area, internal+external
        
        # Store max bounds, so we can tell if we've followed a path beyond the perimeter
        self._min_x = self._min_y = self._min_z = 0
        self._max_x = self._max_y = self._max_z = 0
        
        self._calculate_values()
    
    def __repr__(self) -> str:
        return (f"Droplet(filled_cubes={len(self.filled_cubes)}, " +
                f"all_adjacent={len(self._all_adjacent_positions)}, " +
                f"empty adjacent={len(self._adjacent_empty)}")
        
    def _calculate_values(self): 
        """ Determine:
            - All filled adjacent positions
            - All empty adjacent positions
            - Total surface area of all filled positions
        """
        for filled_cube in self.filled_cubes:
            self._all_adjacent_positions |= filled_cube.adjacent()
            self._adjacent_empty.update(cube for cube in filled_cube.adjacent() if cube not in self.filled_cubes)
            self.all_surface_area += Droplet.ADJACENT_FACES - len(self.filled_cubes & filled_cube.adjacent())
            
            self._min_x = min(filled_cube.x, self._min_x)
            self._min_y = min(filled_cube.y, self._min_y)
            self._min_z = min(filled_cube.z, self._min_z)
            self._max_x = max(filled_cube.x, self._max_x)
            self._max_y = max(filled_cube.y, self._max_y)
            self._max_z = max(filled_cube.z, self._max_z)
    
    def get_external_surface_area(self) -> int:
        """ Determine surface area of all cubes that can reach the outside. """
        cubes_to_outside = set()   # cache cubes we have already identified a path to outside for
        no_path_to_outside = set()  # store all internal empty
        surfaces_to_outside = 0

        # Loop through the cubes and find any that can reach outside
        for cube in self.filled_cubes:
            for adjacent in cube.adjacent(): # for each adjacent...
                if self._has_path_to_outside(adjacent, cubes_to_outside, no_path_to_outside): 
                    cubes_to_outside.add(adjacent)
                    surfaces_to_outside += 1
                else:
                    no_path_to_outside.add(adjacent)
            
        return surfaces_to_outside
    
    def _has_path_to_outside(self, cube: Cube, 
                              cubes_to_outside: set[Cube], 
                              no_path_to_outside: set[Cube]) -> bool:
        """ Perform BFS to flood fill from this empty cube.
        Param cubes_to_outside is to cache cubes we've seen before, that we know have a path. 
        Param internal_cubues is to cache cubes we've seen before, that are internal. """
        frontier = deque([cube])
        explored = {cube}
        
        while frontier:
            current_cube = frontier.popleft() # FIFO for BFS
            
            # Check caches
            if current_cube in cubes_to_outside:
                return True # We've got out from here before
            
            if current_cube in no_path_to_outside or current_cube in self.filled_cubes:
                continue # This cube doesn't have a path, so no point checking its neighbours
            
            # Check if we've followed a path outside of the bounds
            if current_cube.x > self._max_x or current_cube.y > self._max_y or current_cube.z > self._max_z:
                return True

            if current_cube.x < self._min_x or current_cube.y < self._min_y or current_cube.z < self._min_z:
                return True
            
            # We want to look at all neighbours of this empty space
            for neighbour in current_cube.adjacent():
                if neighbour not in explored:
                    frontier.append(neighbour)
                    explored.add(neighbour)
                    
        return False
    
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    droplet = Droplet(parse_cubes(data))
    print(droplet)
    
    # Part 1
    print(f"Part 1: all surface area={droplet.all_surface_area}")

    # Part 2
    external_faces = droplet.get_external_surface_area()
    print(f"Part 2: external surface area={external_faces}")

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
