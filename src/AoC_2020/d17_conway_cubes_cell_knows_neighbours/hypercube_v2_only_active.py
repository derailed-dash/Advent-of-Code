"""
Author: Darren
Date: 17/12/2020

Solving: https://adventofcode.com/2020/day/17

Solution 2 of 2:
    Only stores active cells in the grid.  Much more efficient.
    Reduces execution time from 3 minutes down to ~30s using CPython, and about 5s using PyPy.
    Added some visualisation to part 1.

Part 1
------
3D space of cubes which are active or inactive.  
With each iteration, cells change state simultaneously, according to rules:
    - If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
      Otherwise, the cube becomes inactive.
    - If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. 
      Otherwise, the cube remains inactive.

Each cube will have 26 neighbours (8 in the same plane; 9 in upper and lower planes)

Part 2
------
As before, but now extends to 4D.
"""
import os
import time
from pprint import pprint as pp
import numpy as np
import matplotlib.pyplot as plt
from AoC_2020.d17_conway_cubes_cell_knows_neighbours.cell import Cell, Cell4d

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/init_state.txt"
SAMPLE_INPUT_FILE = "input/sample_init_state.txt"

ACTIVE = '#'
CYCLES = 6

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input_state = read_input(input_file)
    pp(input_state)

    grid = set()
    process_init(input_state, grid)
    for i in range(CYCLES):
        print(f"Cycle {i}:")
        # show_grid(grid)
        grid = execute_cycle(grid)

    print(f"Sum active: {len(grid)}")

    grid = set()
    process_init_4d(input_state, grid)

    for i in range(CYCLES):
        print(f"Cycle {i}:")
        grid = execute_cycle(grid)

    print(f"Sum active: {len(grid)}")


def show_grid(grid):
    x_vals = [cell.get_x() for cell in grid]
    y_vals = [cell.get_y() for cell in grid]
    z_vals = [cell.get_z() for cell in grid]

    min_x_add = 0
    min_y_add = 0
    min_z_add = 0

    min_x = min(x_vals)
    min_y = min(y_vals)
    min_z = min(z_vals)

    # we need to get rid of negative coords, since numpy doesn't support -ve values for indexes
    if min_x < 0:
        min_x_add = 0 - min_x
    if min_y < 0:
        min_y_add = 0 - min_y
    if min_z < 0:
        min_z_add = 0 - min_z        

    x_size = (max(x_vals) + 1) - min(x_vals)
    y_size = (max(y_vals) + 1) - min(y_vals)
    z_size = (max(z_vals) + 1) - min(z_vals)
    xyz = np.zeros((x_size, y_size, z_size))
    for cell in grid:
        x = cell.get_x() + min_x_add
        y = cell.get_y() + min_y_add
        z = cell.get_z() + min_z_add

        xyz[x, y, z] = 1

    axes = plt.axes(projection='3d')
    for index, active in np.ndenumerate(xyz):
        if active == 1:
            axes.scatter3D(*index, c='blue', marker='s', s=200, alpha=0.7)
        else:
            axes.scatter3D(*index, c='yellow', marker='s', s=200, alpha=0.7)

    axes.set_xlabel('x')
    axes.set_ylabel('y')
    axes.set_zlabel('z')
    axes.set_title('Cells')

    plt.show()
    

def execute_cycle(grid):
    cells_to_add = set()
    cells_to_remove = set()

    for existing_cell in grid:
        neighbours_of_existing_cell = existing_cell.get_neighbours()
        existing_cell_active_neighbours_count = 0
        for neighbour in neighbours_of_existing_cell:
            # neighbour not yet in grid
            # we need to add it, so we need to determine its own neighbours
            if neighbour not in grid:        
                new_cell_neighbours = neighbour.get_neighbours()
                # the intersection will give us all the active neighbours for this cell
                new_cell_active_neighbours_count = len(grid.intersection(set(new_cell_neighbours)))
                if (new_cell_active_neighbours_count == 3):
                    cells_to_add.add(neighbour)

            # neighbour already in grid
            else:
                existing_cell_active_neighbours_count += 1
   
        if (existing_cell_active_neighbours_count < 2
                or existing_cell_active_neighbours_count > 3):
            cells_to_remove.add(existing_cell)

    # do our grid updates at the end, since the cell changes are supposed to be simultaneous
    grid.update(cells_to_add)
    grid.difference_update(cells_to_remove)

    return grid       


def process_init(input_data, grid: set):
    # initialisation grid is 2D, so z coordinate is 0
    # only store active cells in the grid
    for y in range(len(input_data)):
        for x in range(len(input_data[y])):
            if (input_data[y][x] == ACTIVE):
                grid.add(Cell([x, y, 0]))


def process_init_4d(input_data, grid):
    # initialisation grid is 2D, so z and w coordinates are 0
    # only store active cells in the grid
    for y in range(len(input_data)):
        for x in range(len(input_data[y])):
            if (input_data[y][x] == ACTIVE):
                grid.add(Cell4d([x, y, 0, 0]))


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
