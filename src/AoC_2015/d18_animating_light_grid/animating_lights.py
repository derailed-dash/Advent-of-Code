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
import os
import time
from itertools import product
from aoc_common.aoc_commons import Vectors

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

ITERATIONS = 100

def get_neighbours(coord: tuple[int, int]) -> list[tuple[int, int]]:
    """ Get list of neighbour coords

    Args:
        coord (tuple): the coord of the cell whose neighbours we want to identify, passed as (x, y)

    Returns:
        list: A list of coordinates for for neighbours. Each coord pay is a tuple in the list.
    """
    neighbours = []

    x = coord[0]
    y = coord[1]

    for vector in Vectors:
        new_x = x + vector.value[0]
        new_y = y + vector.value[1]
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

def get_corners(lights_length: int, lights_height: int) -> set[tuple[int, int]]:
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

def process_iterations(all_lights: set[tuple[int, int]], 
                       on_lights: set[tuple[int, int]], 
                       iterations: int,
                       fixed_lights: set[tuple[int, int]] = set()) -> set[tuple[int, int]]:
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
            neighbours = set(get_neighbours(light))
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
    
def init_state(data: list[str]) -> set:
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
