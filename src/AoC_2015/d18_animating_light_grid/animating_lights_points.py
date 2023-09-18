""" 
Author: Darren
Date: 08/03/2021

Solving https://adventofcode.com/2015/day/18

We have a grid of lights.  They can be on or off.
With each iteration, we update whether lights are on or off, according to these rules:
    - A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    - A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.

Solution 2 of 2:
  - Same as solution 1, but this time using Points instead of tuples.
  - It works, but it's about 2x slower.
"""
import os
import time
from itertools import product
from aoc_common.aoc_commons import Point

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

ITERATIONS = 100

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    # Get all light coordinates by obtaining cartesian product of all x coords with all y coords
    lights_length = len(data[0])
    lights_height = len(data)
    
    all_lights = {Point(*point) 
                  for point in set(product(range(lights_length), range(lights_height)))}

    on_lights = init_state(data)

    # Part 1
    final_on_lights = process_iterations(all_lights, on_lights.copy(), ITERATIONS)
    print(f"Part 1, after {ITERATIONS} iterations, there are {len(final_on_lights)} turned on.")

    # Part 2
    corner_lights = set()
    corner_lights.add(Point(0, 0))
    corner_lights.add(Point(lights_length-1, 0))
    corner_lights.add(Point(0, lights_height-1))
    corner_lights.add(Point(lights_length-1, lights_height-1))
    
    final_on_lights = process_iterations(all_lights, on_lights.copy(), ITERATIONS, corner_lights)
    print(f"Part 2, after {ITERATIONS} iterations, there are {len(final_on_lights)} turned on.")

def process_iterations(all_lights: set[Point], 
                       on_lights: set[Point], 
                       iterations: int,
                       fixed_lights: set[Point] = None) -> set[Point]:
    """ 
    Carry out Conway-like rules for all lights in the all_lights set.

    Args:
        all_lights (Set[Point]): A set of all coords, in an array of width x and height y
        on_lights (Set[Point]): A set containing only coords of lights that are on
        iterations (int): The number of iterations to process the Conway-like rules
        fixed_lights (Set[Point], optional): Coords of lights that will always be on. Defaults to empty set().

    Returns:
        Set[Point]: The coords of lights that are 'on', following specified iterations
    """

    if not fixed_lights:
        fixed_lights = set()
        
    for _ in range(iterations):
        on_lights_to_remove = set()
        on_lights_to_add = set()

        on_lights.update(fixed_lights)
        
        for light in all_lights:
            neighbours = set(light.neighbours())
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
    
def init_state(data: list[str]) -> set[Point]:
    on_lights = set()

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if (char == '#'):
                on_lights.add(Point(x, y))

    return on_lights

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
