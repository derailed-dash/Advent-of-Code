"""
Author: Darren
Date: 12/05/2021

Solving https://adventofcode.com/2016/day/1

Part 1:
    Determine x and y movement using unit circle geometry.
    https://www.mathsisfun.com/geometry/unit-circle.html
    
Part 2:
    Find the first location visited twice.
    This is any intersection of any path taken.
    So, we store every visited coordinate.

"""
import logging
import os
import time
from math import sin, cos, radians

# pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

X = 'x'
Y = 'y'

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().split(", ")
    
    logging.debug(data)
    
    location = {
        X: 0,
        Y: 0
    }
    
    visited_locations = []
    visited_locations.append(location.copy())
    
    heading = 0
    
    for instr in data:
        location, heading = process_direction(location, visited_locations, heading, instr)

    taxicab_distance = abs(location[X]) + abs(location[Y])
    logging.info(f"Taxicab distance for entire journey: {taxicab_distance}")
    
    for visited in visited_locations:
        # we want the first location that was visited twice
        # i.e. where this particular location has a count > 1
        if visited_locations.count(visited) > 1:
            taxicab_distance = abs(visited[X]) + abs(visited[Y])
            logging.info(f"First location visited twice was {visited}")
            logging.info(f"Distance to this location: {taxicab_distance}")
            break
    

def process_direction(location: dict, visited_locations: list, heading: int, instr: str):
    turn = instr[0]
    magnitude = int(instr[1:])
    rotation = 90 if turn == 'R' else -90
    heading = convert_angle(heading + rotation)
    
    # We need to process the instruction one unit at a time, 
    # so that we store the path taken, not just the final landing location of each instruction
    for _ in range(magnitude):
        # unit circle geometry
        location[X] += round(sin(radians(heading)))
        location[Y] += round(cos(radians(heading)))
        
        # store all coords visited whilst following this direction
        visited_locations.append(location.copy())
    
    return location, heading

        
def convert_angle(angle: int):
    """ Convert any angle to %360

    Args:
        angle (int): An angle

    Returns:
        [int]: The angle
    """
    if (angle < 0):
        angle += 360
    
    return angle % 360


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
