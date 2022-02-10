""" Count_Trees.py
Author: Darren
Date: 05/12/2020

Solving https://adventofcode.com/2020/day/3

Count how many trees on the toboggan journey from top left to bottom, 
where # denotes a tree, and . denotes empty space.

The toboggan moves x right and y down for each iteration.

Solution 1 of 2:
    Build a list to hold the coordinates of every tree, i.e. as a 2D array
    Replicate the array in the x direction, as many times as necessary, depending on x/y numbers.
    Create a copy of the array to hold the hits and misses.
    Step down and across the array.  Mark all hits and misses.
"""

import sys
import os
import math
import time

INPUT_TREEMAP_FILE = "input/treemap.txt"
OUTPUT_TREEMAP_FILE = "output/treemap.txt"
NAVIGATED_TREEMAP_FILE = "output/navigated_treemap.txt"

x_movement = 1
y_movement = 1


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_TREEMAP_FILE)
    print("Input file is: " + input_file)

    output_file = os.path.join(script_dir, OUTPUT_TREEMAP_FILE)
    print("Output file is: " + output_file)

    treemap = get_treemap(input_file)

    # if we want to write visual representation to file...
    # write_treemap(output_file, treemap)
   
    output_file = os.path.join(script_dir, NAVIGATED_TREEMAP_FILE)
    navigated_treemap = navigate_treemap(treemap)   
    print(f"We have hit {''.join(navigated_treemap).count('X')} trees")
    
    # write_treemap(output_file, navigated_treemap)


def write_treemap(a_file, treemap):
    """Write a treemap (in memory list) to a file.
 
    Args:
        a_file - the file to be written
        treemap - the list that represents the tree locations
    """

    with open(a_file, 'w') as f:
        for row in treemap:
            f.write(row + "\n")


def get_treemap(a_file):
    """Read a tree map file, and represent ast a list.
 
    Args:
        a_file - the tree map file to be read

    Returns:
        treemap - a list that represents the tree locations
    """
    with open(a_file, mode="rt") as f:
        
        # get the width of the map
        # strip off the newline character
        treemap_cols = len(f.readline()) - 1

        # get the number of rows in the map
        # add 1, since we've already read one row
        treemap_rows = len(f.readlines()) + 1

        print("Treemap rows: " + str(treemap_rows))
        print("Treemap cols: " + str(treemap_cols))
        
        # decide how many horizontal repeats we need, based on tobogan movement
        # i.e. for every (y), we need (x) horizontal characters
        min_width = math.ceil(treemap_rows/y_movement) * x_movement
        print("Min width: " + str(min_width))
        horizontal_repeats = math.ceil(min_width / treemap_cols)
        print("Horizontal repeats needed: " + str(horizontal_repeats))

        # Go back to the beginning of the file
        f.seek(0)
        treemap = [horizontal_repeats * line.rstrip('\n') for line in f.readlines()]

    return treemap


def navigate_treemap(treemap):
    """Processes a treemap list.
    Determines how many trees would be hit, 
    based on specified x/y movement pattern.
 
    Args:
        treemap - treemap locations as a list

    Returns:
        navigated_treemap - a new list that shows tree collisions and misses
    """
    TREE = '#'
    TREE_HIT = 'X'
    TREE_MISS = 'O'
 
    # x, y coordinates; 1-indexed, not 0
    posn = [1, 1]

    # let's create a copy of the treemap, and update it with the hit/miss markers
    navigated_treemap = treemap[:]    
    
    # whilst we have rows left
    while (posn[1] <= len(treemap)):
        # Now obtain the treemap row [y-1], and the treemap index [x-1], and see what it is.
        if ((posn[1]-1) <= len(navigated_treemap)):
            try:
                at_location = navigated_treemap[posn[1]-1][posn[0]-1]
                # print(f"Current position {posn}:" + navigated_treemap[posn[1]-1][posn[0]-1])

                # Get this row.  Convert from str to list
                newrow = list(navigated_treemap[posn[1]-1])

                # replace the current char
                if (at_location == TREE):
                    newrow[posn[0]-1] = TREE_HIT
                else:
                    newrow[posn[0]-1] = TREE_MISS
                
                # replace the row
                navigated_treemap[posn[1]-1] = "".join(newrow)
            except IndexError:
                print("Error")
                print(posn)

        posn[0] = posn[0] + x_movement
        posn[1] = posn[1] + y_movement

    return navigated_treemap


if __name__ == "__main__":
    try:
        x_movement = int(input("Enter x movement: "))
        y_movement = int(input("Enter y movement: "))

        t1 = time.perf_counter()
        main()
        t2 = time.perf_counter()
        print(f"Execution time: {t2 - t1:0.4f} seconds")
    except ValueError:
        print("Movement must be an integer value")




