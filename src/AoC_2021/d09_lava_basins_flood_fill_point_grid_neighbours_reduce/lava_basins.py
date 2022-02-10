"""
Author: Darren
Date: 09/12/2021

Solving https://adventofcode.com/2021/day/9

We want to avoid lava smoke. Smoke flows to the lowest point.
We have a heightmap as a 2D grid.  9 is heighest point and 0 is lowest.
Risk score is given by height+1, at any given point.

Part 1:
    Find all the lowest points, i.e. points that are lower than adjacent orthagonal.
    Point2D class knows how to yield its neighbours.
    Grid class knows height at a given point. Easy.
    
Part 2:
    We need the product of sizes of the three largest basins.  
    A basin has a low point, and any surrounding points that are greater or equal, excluding 9.
    All basins have a perimeter of 9s (which are not part of the basin).

    Determine a basin for each low point we already have.
    We can do this with a flood-fill BFS. 
    Use the same yield_neighbours() to return all neighbours, 
    and add all points < 9.  Mark any points already seen.  Don't look at neighbours of 9.
"""
from __future__ import annotations
import logging
import os
import time
from collections import deque
from dataclasses import dataclass
from functools import reduce
from typing import Iterator
from PIL import Image

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

RENDER = True
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "output/heatmap.png")

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

@dataclass(frozen=True)
class Point():
    """ Our immutable point data class """
    ADJACENT_DELTAS = [(dx,dy) for dx in range(-1, 2) 
                               for dy in range(-1, 2) if abs(dy) != abs(dx)]
    
    x: int
    y: int
    
    def yield_neighbours(self) -> Iterator[Point]:
        """ Yield adjacent (orthogonal) neighbour points """
        for vector in Point.ADJACENT_DELTAS:
            yield Point(self.x + vector[0], self.y + vector[1])        
    
class Grid():
    """ 2D grid of point values. Knows how to:
       - Determine value at any point
       - Whether the point is lower than adjancent
       - Determine the entire basin, given a low point """
    def __init__(self, grid_array: list) -> None:
        self._array = grid_array
        self._width = len(self._array[0])
        self._height = len(self._array)
        
    def height_at_point(self, point: Point) -> int:
        """ Height is given by the value at this point """
        return self._array[point.y][point.x]
    
    def risk_at_point(self, point: Point) -> int:
        """ Risk is given by height at point + 1 """
        return self.height_at_point(point) + 1
    
    def low_points(self) -> set:
        """ Returns all low points in the grid """
        low_points = set()
        
        for y in range(self._height):
            for x in range(self._width):
                point = Point(x, y)
                if self.is_low_point(point):
                    low_points.add(point)
                    
        return low_points
    
    def is_low_point(self, point: Point) -> bool:
        """ Determines if this point is a low point, i.e. surrounded by higher values. """
        value = self.height_at_point(point)
        
        for neighbour in point.yield_neighbours():
            if self.valid_location(neighbour):
                if self.height_at_point(neighbour) <= value:
                    return False
                
        return True
                   
    def valid_location(self, point: Point) -> bool:
        """ Check if a location is within the grid """
        if (0 <= point.x < self._width and  0 <= point.y < self._height):
            return True
        
        return False
    
    def get_basin(self, low_point: Point) -> set:
        """ Given a low point, determine all the surrounding points that make up a basin.
        Any points with height 9 mark the boundary of the basin and are NOT part of the basin. """
        
        assert self.is_low_point(low_point), "We should never start with a point that isn't a low point"
        
        basin_points = set()            # The points we'll return
        points_to_assess: deque[Point] = deque()  # Points we want to get value of, and get neighbours for
        assessed = set()                # Points we don't want to assess again
        points_to_assess.append(low_point)  # where we start
        
        while points_to_assess:     # They should only ever be valid points
            point_to_assess = points_to_assess.popleft()
            if point_to_assess in assessed:     
                continue    # We've seen this before, so skip it
            
            assessed.add(point_to_assess)   # So we don't look at this again
            
            if self.height_at_point(point_to_assess) < 9:   # Points lower than 9 count as basin
                basin_points.add(point_to_assess)         
            
                for neighbour in point_to_assess.yield_neighbours():
                    if self.valid_location(neighbour):
                        if neighbour not in assessed:   # We will need to assess this point
                            points_to_assess.append(neighbour)
        
        return basin_points
    
    def render_image(self, target_width:int=600) -> Image.Image:
        """ Render grid as a heatmap image

        Args:
            width (int, optional): Target width, in pxiels. Defaults to 600.
        """
        scale = target_width // self._width  # our original image is only a few pixels across. We need to scale up.
        
        # Flatten our x,y array into a single list of height values
        height_values = [self.height_at_point(Point(x,y)) for y in range(self._height) 
                                                          for x in range(self._width)]
        max_height = max(height_values)

        # create a new list of RGB values, where each is given by an (R,G,B) tuple.
        # To achieve a yellow->amber->red effect, we want R to always be 255, B to always be 0, and G to vary based on height
        pixel_colour_map = list(map(lambda x: (255, int(255*((max_height-x)/max_height)), 0), height_values)) 

        image = Image.new(mode='RGB', size=(self._width, self._height))
        image.putdata(pixel_colour_map)  # load our colour map into the image

        # scale the image and return it
        return image.resize((self._width*scale, self._height*scale), Image.NEAREST)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = [[int(posn) for posn in row] for row in f.read().splitlines()]
        
    grid = Grid(data)
    low_points = grid.low_points()
    risk_by_point = {point: grid.risk_at_point(point) for point in low_points}
    logger.info("Part 1: low_point_risks = %d", sum(risk_by_point.values()))
    
    basin_sizes = []
    for point in low_points:    # basins are generated from low points
        basin = grid.get_basin(point)
        basin_sizes.append(len(basin))

    qty_required = 3
    basin_sizes.sort(reverse=True)  # descending size order
    biggest_basins = basin_sizes[0:qty_required]  # top n basins
    logger.info("Part 2: product = %d", reduce((lambda x, y: x * y), biggest_basins))
    
    if RENDER:
        dir_path = os.path.dirname(OUTPUT_FILE)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        image = grid.render_image(400)
        image.save(OUTPUT_FILE)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
