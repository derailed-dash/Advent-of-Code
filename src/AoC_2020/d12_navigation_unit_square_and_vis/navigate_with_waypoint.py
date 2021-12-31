"""
Author: Darren
Date: 12/12/2020

Solving: https://adventofcode.com/2020/day/12

Modelling ship navigation.

Solution 1 of 2:

Part 2
------
N, S, E, W means translate the waypoint by given magnitude.
L, R means rotate waypoint about the ferry, maintaining the distance between ship and waypoint
F means move the ferry (translate) towards waypoint, n times the magnitude of the vector to the waypoint
"""
import sys
import os
import time

INPUT_FILE = "input/nav.txt"
SAMPLE_INPUT_FILE = "input/sample_nav.txt"

X = "X"
Y = "Y"
HDG = "HDG"

START_X = 10
START_Y = 1

waypoint = {
    X: START_X,
    Y: START_Y
}

location = {
    X: 0,
    Y: 0
}

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    nav_instructions = read_input(input_file)
    # pp(nav_instructions)

    navigate(nav_instructions)
    new_x = location[X]
    new_y = location[Y]
    manhattan_distance = abs(new_x) + abs(new_y)
    print(f"New location is E {new_x}, N {new_y} with Manhattan distance of {manhattan_distance}")
 

def navigate(instructions):
    for instr in instructions:
        process_instruction(instr)


def process_instruction(instr):
    global waypoint

    instr_type = instr[0]
    instr_mag = int(instr[1:])

    # print(f"Instr is {instr_type} with magnitude: {instr_mag}")

    if (instr_type == 'N'):
        waypoint[Y] = waypoint[Y] + instr_mag
    elif (instr_type == 'S'):
        waypoint[Y] = waypoint[Y] - instr_mag
    elif (instr_type == 'E'):
        waypoint[X] = waypoint[X] + instr_mag
    elif (instr_type == 'W'):
        waypoint[X] = waypoint[X] - instr_mag 
    elif (instr_type == 'R'):
        rotations = instr_mag // 90
        for _ in range(rotations):
            waypoint[Y], waypoint[X] = -waypoint[X], waypoint[Y]
    elif (instr_type == 'L'):
        rotations = instr_mag // 90
        for _ in range(rotations):
            waypoint[X], waypoint[Y] = -waypoint[Y], waypoint[X]

    elif (instr_type == 'F'):
        location[X] = location[X] + instr_mag * waypoint[X]
        location[Y] = location[Y] + instr_mag * waypoint[Y]

    return location
        

def read_input(a_file):
    with open(a_file, mode="rt") as f:
        codelines = f.read().splitlines()
        
    return codelines


def convert_angle(angle):
    if (angle < 0):
        angle += 360
    
    return angle % 360


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

