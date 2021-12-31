""" Count_Trees.py
Author: Darren
Date 27/12/2020

Solving https://adventofcode.com/2020/day/3

Count how many trees on the toboggan journey from top left to bottom, 
where # denotes a tree, and . denotes empty space.

The toboggan moves x right and y down for each iteration.

Solution 2 of 2:
    Don't need to do vertical repeats. Just wrap around with modulus.
    
"""

import sys
import os
import math
import time

INPUT_TREEMAP_FILE = "input/treemap.txt"
SAMPLE_FILE = "input/sample_treemap.txt"
TREE = '#'

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_TREEMAP_FILE)
    #input_file = os.path.join(script_dir, SAMPLE_FILE)
    print("Input file is: " + input_file)
    treemap = get_treemap(input_file)

    # x, y movement
    vectors = ([3, 1], [1, 1], [5, 1], [7, 1], [1, 2])

    trees_hit = []
    for vector in vectors:
        stops = "".join(navigate_treemap(treemap, vector))
        trees_hit.append(stops.count(TREE))
        print(f"Vector {vector}, trees hit: {stops.count(TREE)}")

    print(f"Product of trees hit: " + str(math.prod(trees_hit)))


def get_treemap(a_file):
    """
        Read a tree map file, and represent ast a list.
    """
    with open(a_file, mode="rt") as f:
        treemap = Treemap(f.read().splitlines())

    return treemap


class Treemap:
    def __init__(self, treemap: list):
        self._treemap = treemap
        self._length = len(treemap)
        self._width = len(treemap[0])

    def get_row(self, y):
        """
            Helper method to allow us to use 1-indexing
        """
        return self._treemap[y-1]

    def get_char_at(self, x, y):
        """
            Helper method to allow us to use 1-indexing.
            If width is exceeded, we just loop back around to the left side.
        """
        return self._treemap[y-1][(x-1)%self._width]

    def get_width(self):
        return self._width

    def get_length(self):
        return self._length

    def __str__(self):
        return "\n".join(self._treemap)

    def __repr__(self):
        return "\n".join(self._treemap)


def navigate_treemap(treemap, vector):
    """Processes a treemap list.
    Determines how many trees would be hit, based on specified x/y movement pattern
    """
    stops = []
    
    # x, y coordinates; 1-indexed, not 0
    current_posn = [1, 1]

    # whilst we have rows left
    while (current_posn[1] <= treemap.get_length()):
        stops.append(treemap.get_char_at(*current_posn))

        current_posn[0] += vector[0]
        current_posn[1] += vector[1]

    return stops


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")




