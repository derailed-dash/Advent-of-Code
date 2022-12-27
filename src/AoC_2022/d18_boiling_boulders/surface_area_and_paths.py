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
- Droplet class stores cubes.
- Each cube has a surface area of 6 - (intersection of cube adjacents with all cubes)

Part 2:

What is the exterior surface area of your scanned lava droplet?
We're told steam wont expand diagonally.

Soln:

- We now need to ignore internal pockets that are sealed to the outside.
- We need to know if a empty location is interior and if it has a path to the outside.
- Assume all cubes in our list are connected.
- Find all adjacent cubes. These are either:
  - Part of internal pockets. If we flood fill a pocket, it will have a boundary.
  - Part of path to the outside. If we flood fill, we will reach a cube beyond all the droplet bounds.
- To solve:
  - For each filled cube, get its adjacents
  - BFS for each adacent, if adjacent is empty space.
  - If the BFS only leads to filled cubes, then all paths are blocked, so cube is internal.
  - If the BFS leads to cubes that our outside our bounds, then this cube has a path out.
  - Store all cubes that have a path out or are internal, and use these to cache the BFS.
  - Only increment the surface area count every time we find an adjacent location that has a path out.
  
Takes about 5s.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from pathlib import Path
import time
import matplotlib.pyplot as plt
import numpy as np

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
        # Store max bounds, so we can tell if we've followed a path beyond the perimeter
        self._min_x = self._min_y = self._min_z = 0
        self._max_x = self._max_y = self._max_z = 0
        self._all_surface_area: int = 0  # surface area, internal+external
        self._internal = set()
        self._external = set()
        
        self._calculate_values()
    
    @property
    def all_surface_area(self):
        return self._all_surface_area
    
    def __repr__(self) -> str:
        return (f"Droplet(filled_cubes={len(self.filled_cubes)})")
        
    def _calculate_values(self): 
        """ Determine:
            - Total surface area of all filled positions
            - Outer boundaries (min/max x/y/z values) for the droplet.
        """
        for filled_cube in self.filled_cubes:
            self._all_surface_area += Droplet.ADJACENT_FACES - len(self.filled_cubes & filled_cube.adjacent())
            
            self._min_x = min(filled_cube.x, self._min_x)
            self._min_y = min(filled_cube.y, self._min_y)
            self._min_z = min(filled_cube.z, self._min_z)
            self._max_x = max(filled_cube.x, self._max_x)
            self._max_y = max(filled_cube.y, self._max_y)
            self._max_z = max(filled_cube.z, self._max_z)
    
    def get_external_surface_area(self) -> int:
        """ Determine surface area of all cubes that can reach the outside. """
        surfaces_to_outside = 0

        # Loop through the cubes and find any that can reach outside
        for cube in self.filled_cubes:
            for adjacent in cube.adjacent(): # for each adjacent...
                if self._has_path_to_outside(adjacent): 
                    self._external.add(adjacent)
                    surfaces_to_outside += 1
                else:
                    self._internal.add(adjacent)
            
        return surfaces_to_outside
    
    def _has_path_to_outside(self, cube: Cube) -> bool:
        """ Perform BFS to flood fill from this empty cube.
        Param cubes_to_outside is to cache cubes we've seen before, that we know have a path. 
        Param internal_cubues is to cache cubes we've seen before, that are internal. """
        frontier = deque([cube])
        explored = {cube}
        
        while frontier:
            current_cube = frontier.popleft() # FIFO for BFS
            
            # Check caches
            if current_cube in self._external:
                return True # We've got out from here before
            if current_cube in self._internal:
                continue # This cube doesn't have a path, so no point checking its neighbours
            
            if current_cube in self.filled_cubes:
                continue # This path is blocked
            
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
    
    def vis(self):
        """ Render a visualisation of our droplet """

        axes = [self._max_x+1, self._max_y+1, self._max_z+1]  # set bounds

        grid = np.zeros(axes, dtype=np.int8)   # Initialise 3d grid to empty
        for point in self.filled_cubes:  # set our array to filled for all filled cubes
            grid[point.x, point.y, point.z] = 1
        
        facecolors = np.where(grid==1, 'red', 'black')
        
        # Plot figure
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(grid, facecolors=facecolors, edgecolors="grey", alpha=0.3)
        ax.set_aspect('equal')
        plt.axis("off")
        plt.show()
        
        
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
    
    droplet.vis()

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
