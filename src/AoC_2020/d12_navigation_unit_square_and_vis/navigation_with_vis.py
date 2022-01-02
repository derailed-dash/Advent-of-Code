"""
Author: Darren
Date: 31/12/2020

Solving: https://adventofcode.com/2020/day/12

Modelling ship navigation.

Solution 2 of 2:
    Simplified translation using vector.
    Added visualisation using matplotlib.

Part 1
------
N, S, E, W means move (translate) the ferry in that direction by given magnitude.
L, R means rotate ferry in that direction, given degrees.
F means forward (translate) in the direction we're currently heading.
    Interpret F instructions by using unit-circle trig. 
    See https://www.mathsisfun.com/geometry/unit-circle.html

We start pointing E (90 degrees).

Part 2
------
N, S, E, W means translate the waypoint by given magnitude.
L, R means rotate waypoint about the ferry, maintaining the distance between ship and waypoint
F means move the ferry (translate) towards waypoint, n times the magnitude of the vector to the waypoint
"""
import os
import time
from math import sin, cos, radians
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/nav.txt"
SAMPLE_INPUT_FILE = "input/sample_nav.txt"
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output/")

X = "X"
Y = "Y"
HDG = "HDG"

VECTORS = {
    "N": [0, 1],
    "S": [0, -1],
    "E": [1, 0],
    "W": [-1, 0]
}

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    nav_instructions = read_input(input_file)
    # pp(nav_instructions)

    # part 1
    location_and_bearing = {
        X: 0,
        Y: 0,
        HDG: 90
    }
    coords_visited = navigate_via_translation(nav_instructions, location_and_bearing)
    draw_graph(coords_visited, "ferry_movement_plot.jpg")

    last_x, last_y = coords_visited[-1]
    manhattan_distance = abs(last_x) + abs(last_y)
    print(f"New location is E {last_x}, N {last_y} with Manhattan distance of {manhattan_distance}")

    # part 2
    location = {
        X: 0,
        Y: 0
    }

    waypoint = {
        X: 10,
        Y: 1
    }

    coords_visited = navigate_via_waypoint(nav_instructions, waypoint, location)
    draw_graph(coords_visited, "ferry_movement_by_waypoint_plot.jpg")
    
    last_x, last_y = coords_visited[-1]
    manhattan_distance = abs(last_x) + abs(last_y)
    print(f"New location is E {last_x}, N {last_y} with Manhattan distance of {manhattan_distance}")
 

def draw_graph(coords_visited, output_file):
    # take list of [x, y], and extract x into one list, and y into another list
    x_coords = [x for x, y in coords_visited]
    y_coords = [y for x, y in coords_visited]

    # set x and y to use same scale
    axes = plt.gca()
    axes.set_aspect('equal', adjustable='box')
    axes.grid(True)
    plt.plot(x_coords, y_coords, color="green", marker="o", markerfacecolor="red", markersize=5)
    plt.title("Ferry Movement")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    output_plot_file = os.path.join(OUTPUT_DIR, output_file)
    print("Output plot file is: " + output_plot_file)
    # if we want to show interactive view...
    # plt.show()
    plt.savefig(output_plot_file, transparent=True)


def navigate_via_translation(instructions, location_and_bearing):
    coords_visited = [[location_and_bearing[X], location_and_bearing[Y]]]

    for instr in instructions:
        location_and_bearing = process_translation_instruction(instr, location_and_bearing)
        coords_visited.append([location_and_bearing[X], location_and_bearing[Y]])

    return coords_visited


def process_translation_instruction(instr, location_and_bearing):
    instr_type = instr[0]
    instr_mag = int(instr[1:])

    # print(f"Instr is {instr_type} with magnitude: {instr_mag}")
    if (instr_type in VECTORS):
        # translate
        location_and_bearing[X] += instr_mag * VECTORS[instr_type][0]
        location_and_bearing[Y] += instr_mag * VECTORS[instr_type][1]
    elif (instr_type == 'R'):
        # rotate right
        location_and_bearing[HDG] = convert_angle(location_and_bearing[HDG] + instr_mag)
    elif (instr_type == 'L'):
        # rotate left
        location_and_bearing[HDG] =  convert_angle(location_and_bearing[HDG] - instr_mag)
    elif (instr_type == 'F'):
        # translate based on current heading.  Note, sin and cos require HDG in radians
        location_and_bearing[X] += instr_mag * round(sin(radians(location_and_bearing[HDG])), 1)
        location_and_bearing[Y] += instr_mag * round(cos(radians(location_and_bearing[HDG])), 1)

    return location_and_bearing


def convert_angle(angle):
    if (angle < 0):
        angle += 360
    
    return angle % 360


def navigate_via_waypoint(instructions, waypoint, location):
    coords_visited = [[location[X], location[Y]]]
    
    for instr in instructions:
        location = process_waypoint_instruction(instr, waypoint, location)
        coords_visited.append([location[X], location[Y]])

    return coords_visited


def process_waypoint_instruction(instr, waypoint, location):
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


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
