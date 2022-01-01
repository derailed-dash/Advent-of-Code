""" 
Author: Darren
Date: 08/03/2021

Solving https://adventofcode.com/2015/day/18

We have a grid of lights.  They can be on or off.
With each iteration, we update whether lights are on or off, according to these rules:
    - A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    - A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.

Part 1:
    Use a set to store all lights as x, y tuples.
    Use another set to store only lights that are on.
    Iterate through all lights.  For each, obtain coords of all neighbours.
    Determine 'on' neighbours using intersection with the on_lights.
    Apply rules, now we know whether a light is on or off, and how many 'on' neighbours it has.

Part 2:
    As before, but treat corner lights as always on.
    Create a set that contains just the corners.  
    Union with this set at the beginning of every iteration.
    When processing each iteration, ignore rules for corners.
"""
from typing import Dict, List, Set, Tuple
import os
import time
from itertools import product

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

ITERATIONS = 100

class Cell:

    # static variables
    vectors: Dict[str, Tuple[int, int]] = {
        # x, y vector for adjacent locations
        'tr': (1, 1),
        'mr': (1, 0),
        'br': (1, -1),
        'bm': (0, -1),
        'bl': (-1, -1),
        'ml': (-1, 0),
        'tl': (-1, 1),
        'tm': (0, 1)
    }

    def __init__(self, on: bool = True):
        # white is default for a tile
        self._on = on

    def is_on(self):
        return self._on
    
    def __str__(self):
        return self._on

    def __repr__(self):
        return f"{self.__class__.__name__}: " + str(self._on)

    @staticmethod
    def get_vector(compass_direction: str) -> tuple:
        """ Returns a vector for a given compass direction.  E.g. tr (top right) returns (1, 1)

        Args:
            compass_direction (str): I.e. tr, mr, br, bm, bl, ml, tl, tm

        Returns:
            tuple: the (x, y) coordinates for a given adjacent direction
        """
        return Cell.vectors[compass_direction]

    @staticmethod
    def get_neighbours(coord: Tuple[int, int]) -> List[Tuple[int, int]]:
        """ Get list of neighbour coords

        Args:
            coord (tuple): the coord of the cell whose neighbours we want to identify, passed as (x, y)

        Returns:
            list: A list of coordinates for for neighbours. Each coord pay is a tuple in the list.
        """
        neighbours = []

        x = coord[0]
        y = coord[1]

        for vector in Cell.vectors.values():
            new_x = x + vector[0]
            new_y = y + vector[1]
            neighbours.append(tuple([new_x, new_y]))

        return neighbours


def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    # Get all light coordinates by obtaining cartesian product of all x coords with all y coords
    lights_length = len(data[0])
    lights_height = len(data)
    
    all_lights = set(product(range(lights_length), range(lights_height)))
    on_lights = init_state(data)
    corner_lights = get_corners(lights_length, lights_height)

    # Part 1
    final_on_lights = process_iterations(all_lights, on_lights.copy(), ITERATIONS)
    print(f"Part 1, after {ITERATIONS} iterations, there are {len(final_on_lights)} turned on.")

    # Part 2
    final_on_lights = process_iterations(all_lights, on_lights.copy(), ITERATIONS, corner_lights)
    print(f"Part 2, after {ITERATIONS} iterations, there are {len(final_on_lights)} turned on.")


def get_corners(lights_length: int, lights_height: int) -> Set[Tuple[int, int]]:
    """ 
    Gets the coordinates of the four corners, given an x size and y size

    Args:
        lights_length (int): x size
        lights_height (int): y size

    Returns:
        Set[Tuple[int, int]]: A set of four (x, y) coords
    """

    on_lights_to_add = set()

    on_lights_to_add.add((0, 0))
    on_lights_to_add.add((lights_length-1, 0))
    on_lights_to_add.add((0, lights_height-1))
    on_lights_to_add.add((lights_length-1, lights_height-1))

    return on_lights_to_add


def process_iterations(all_lights: Set[Tuple[int, int]], 
                       on_lights: Set[Tuple[int, int]], 
                       iterations: int,
                       fixed_lights: Set[Tuple[int, int]] = set()) -> Set[Tuple[int, int]]:
    """ 
    Carry out Conway-like rules for all lights in the all_lights set.

    Args:
        all_lights (Set[Tuple[int, int]]): A set of all coords, in an array of width x and height y
        on_lights (Set[Tuple[int, int]]): A set containing only coords of lights that are on
        iterations (int): The number of iterations to process the Conway-like rules
        fixed_lights (Set[Tuple[int, int]], optional): Coords of lights that will always be on. Defaults to empty set().

    Returns:
        Set[Tuple[int, int]]: The coords of lights that are 'on', following specified iterations
    """

    for _ in range(iterations):
        on_lights_to_remove = set()
        on_lights_to_add = set()

        on_lights.update(fixed_lights)
        
        for light in all_lights:
            neighbours = set(Cell.get_neighbours(light))
            on_neighbours = neighbours.intersection(on_lights)
            
            if (light in fixed_lights):
                # do nothing
                pass
            elif (light in on_lights):
                if len(on_neighbours) < 2 or len(on_neighbours) > 3:
                    on_lights_to_remove.add(light)
            else:
                if (len(on_neighbours) == 3):
                    on_lights_to_add.add(light)
        
        on_lights.update(on_lights_to_add)
        on_lights.difference_update(on_lights_to_remove)

        # print(f"Iteration {_+1}: {len(on_lights)}")

    return on_lights
    

def init_state(data: List[str]) -> Set:
    on_lights = set()

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if (char == '#'):
                on_lights.add((x, y))

    return on_lights


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
