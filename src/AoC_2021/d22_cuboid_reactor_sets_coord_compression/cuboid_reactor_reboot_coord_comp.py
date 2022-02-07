"""
Author: Darren
Date: 22/12/2021

Solving https://adventofcode.com/2021/day/22

We need to reboot the reactor. The reactor is a large 3D grid of cubes.
Each cube can be on or off. All off at the start of the reboot process.
Follow a set of instructions to turn cubes on or off. Instructions are inclusive.

Input looks like:   on x=10..12,y=10..12,z=10..12
                    on x=11..13,y=11..13,z=11..13
                    off x=9..11,y=9..11,z=9..11
                    on x=10..10,y=10..10,z=10..10

Part 1:
    Only consider cubes where x,y,z are all in the range -50 to 50.
    How many cubes are on at the end of the reboot?
    
    Store a set of all 'on' cells.
    Use set algebra to union and diff, given instructions in the instr cuboid. 
    Only need to work within the bounds, which means a total solution space of 100x100x100, so only 1m cells.
    
Part 2:
    Okay, without bounds solution space is too large to repeat Part 1.
    We don't need to keep track of every point.  We just need to track where intervals start and end.
    Process all the intervals created by all the instructions.
    Order them, and determine lengths of each interval.
    Then run through instructions again, adding intervals in order.
    We end up with about 130m intervals, and we have to work out the products for these, and sum them.
    Final solution has ~double the magnitude!
    
    This is slow: 3 mins in CPython and 2 mins in PyPy.
"""
from __future__ import annotations
import logging
import os
import time
import re
from typing import NamedTuple

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

class Instruction(NamedTuple):
    """ An instruction to turn on/off all the cubes in the region described by the Cuboid """
    on_or_off: str
    cuboid: Cuboid

class Cuboid(NamedTuple):
    """ Stores the x, y and z coordinates that make up a cuboid. """
    x_range: tuple[int, int]
    y_range: tuple[int, int]
    z_range: tuple[int, int]
    
class Reactor():
    """ 3D space that contains a number of unit cubes. Initially, all cubes are turned off.
    We process a number of instructions, which toggles cuboid regions to be on or off. """
    
    def __init__(self, bound:int=0) -> None:
        """ Initialise this cuboid set.  When adding / subtracting points (later), ignore anything out of bounds. 
        Bound is given by (0-bound, 0+bound) in any dimension. 0 means no bound. """
        self._bound = bound
        self._cuboid = set()
        
    @property
    def cells_on(self):
        return len(self._cuboid)
    
    def update(self, instr:Instruction):
        """ Turn on / off points that are supplied in the form of a Cuboid. """
        cuboid = self._cuboid_to_set(instr.cuboid.x_range, instr.cuboid.y_range, instr.cuboid.z_range)
        
        if instr.on_or_off == "on":
            self._cuboid = self._cuboid | cuboid   # union
        else:
            self._cuboid = self._cuboid - cuboid   # diff
    
    def _cuboid_to_set(self, x_range: tuple, y_range: tuple, z_range: tuple) -> set:
        """ Creates a new set of 'on' points, given a set of 3 pairs of cuboid vertices. """
        temp_cuboid = set()
        
        x_lower, x_upper = x_range[0], x_range[1]
        y_lower, y_upper = y_range[0], y_range[1]
        z_lower, z_upper = z_range[0], z_range[1]
        
        if self._bound > 0:
            x_lower = max(x_lower, -self._bound)
            y_lower = max(y_lower, -self._bound)
            z_lower = max(z_lower, -self._bound)
            
            x_upper = min(x_upper, self._bound)
            y_upper = min(y_upper, self._bound)
            z_upper = min(z_upper, self._bound)

        for x in range(x_lower, x_upper+1):
            for y in range(y_lower, y_upper+1):
                for z in range(z_lower, z_upper+1):
                    temp_cuboid.add((x, y, z))
        
        return temp_cuboid
    
    def __repr__(self) -> str:
        return f"CuboidGrid:size={len(self._cuboid)}"

class CuboidDeterminator():
    """ Represents number of points that are turned on in a 3D space. 
    This class works by tracking intervals.
    Instructions are pre-processed to deterine all intervals, i.e. vertices and intersections. 
    Then we sort them in each dimension, and have a map of each to an interval length. 
    Finally, intervals and their corresponding lengths can be used to determine 
    the size of 'on' cuboids. """
    
    def __init__(self, instructions: list[Instruction], bound:int=0) -> None:
        self._instructions = instructions   # e.g. ("on", ((x1, x2), (y1, y2), (z1, z2)))
        self._bound = bound
        
        # Maintain current bounds
        self._min_x = self._min_y = self._min_z = 0
        self._max_x = self._max_y = self._max_z = 0
               
        self._cells_on = self._process_instructions()

    @property
    def cells_on(self):
        return self._cells_on
    
    def _process_instructions(self) -> int:
        """ Process all the instructions, e.g. 
        on x=10..12,y=10..12,z=10..12, on x=11..13,y=11..13,z=11..13.
        Instruction order is not important.  We'll convert to an ordered list.
        
        Returns int: Total cubes turned on. """
        
        # Store intervals defined by each cuboid, i.e. where cuboids can begin, end or intersect
        # Within an interval, all cells are the same.  I.e. either all on or all off.
        x_intervals = set()   # E.g. Will become {9, 10, 11, 12, 13, 14}
        y_intervals = set()
        z_intervals = set()
        
        # Sorted intervals, and their corresponding lengths
        x_intv_to_index = {} # E.g. will become {9: 0, 10:1, 11:2, etc}
        y_intv_to_index = {}
        z_intv_to_index = {}
        x_index_to_len = {} # E.g. will become {0: 1, 1: 1, 2: 1, etc}
        y_index_to_len = {}
        z_index_to_len = {}   
        
        # Populate all the intervals, and the lengths between intervals
        for instruction in self._instructions:
            cuboid = instruction.cuboid     # e.g. ((10, 12), (10, 12), (10, 12))
            
            # Add the intervals (vertices) in this instruction
            x_intervals.add(cuboid.x_range[0])  # E.g. adding 10
            x_intervals.add(cuboid.x_range[1]+1) # E.g. adding 13
            y_intervals.add(cuboid.y_range[0])
            y_intervals.add(cuboid.y_range[1]+1)
            z_intervals.add(cuboid.z_range[0])
            z_intervals.add(cuboid.z_range[1]+1)      
            self._update_bounds(cuboid)
            
        x_intv_to_index, x_index_to_len = self._create_intv_maps(x_intervals)
        y_intv_to_index, y_index_to_len = self._create_intv_maps(y_intervals)
        z_intv_to_index, z_index_to_len = self._create_intv_maps(z_intervals)                        
        
        on_indexes = set()
        
        # Now apply on and off instructions
        # I.e. add or remove cuboids in the right order
        for i, instruction in enumerate(self._instructions):
            cuboid = instruction.cuboid
            logger.debug("Instruction %d (of %d)=%s: %s", i+1, len(self._instructions), instruction.on_or_off, cuboid)
            
            # unpack the vertices of this cuboid
            # E.g. (10, 12), (10, 12), (10, 12)
            x1, x2 = cuboid.x_range[0], cuboid.x_range[1]
            y1, y2 = cuboid.y_range[0], cuboid.y_range[1]
            z1, z2 = cuboid.z_range[0], cuboid.z_range[1]
            
            # i.e. get the appropriate intervals given by these coordinates
            # E.g. for cuboid (10,12),(10,12),(10,12), 
            # we turn on a 3x3x3 cuboid of cells.
            # E.g. x_intv_index in range(1, 4) = 3 interval indexes
            for x_intv_index in range(x_intv_to_index[x1], x_intv_to_index[x2+1]):
                for y_intv_index in range(y_intv_to_index[y1], y_intv_to_index[y2+1]):
                    for z_intv_index in range (z_intv_to_index[z1], z_intv_to_index[z2+1]):
                        if instruction.on_or_off == "on":
                            # add intervals corresponding to cuboids turned on
                            on_indexes.add((x_intv_index, y_intv_index, z_intv_index)) # E.g. (1, 1, 1)
                        else:
                            # remove intervals corresponding to cuboids turned off
                            on_indexes.discard((x_intv_index, y_intv_index, z_intv_index)) # E.g. (0, 0, 0)
           
        logger.debug("Computing interval volumes for %d on indexes...", len(on_indexes))
        total_cells_on = 0
        # on_indexes contains, e.g. 39 different non-overlapping 'on' intervals
        # For each triplet of on intervals, get the corresponding lengths.
        # This gives us the size of the 'on cuboid', i.e. how many cells are on in the cuboid
        for x_intv_index, y_intv_index, z_intv_index in on_indexes:
            len_x = x_index_to_len[x_intv_index]
            len_y = y_index_to_len[y_intv_index]
            len_z = z_index_to_len[z_intv_index]
            total_cells_on += len_x * len_y * len_z
            
        return total_cells_on
                             
    def _create_intv_maps(self, intvals: set[int]) -> tuple[dict, dict]:
        """ For this dimension:
            - Create a map of interval value to interval index 
            - Create a map of interval lengths (i.e. from one interval to the next) by position
        
        E.g. passing in {9, 10, 11, 12, 13, 14}, we'll get {9: 1} and {0: 1} """
        intvals_list = sorted(intvals)   # create ordered list from set, i.e. [9, 10, 11, 12, 13, 14]

        intv_to_ind = {}    # map of intervals to their position
        ind_to_len = {}     # map of position to interval length
        
        for i, intv in enumerate(intvals_list):
            intv_to_ind[intv] = i   # {9: 0}, i.e. interval starting at 9 is index 0
            
            # Now work out the length of this interval, i.e. diff between this intv and the next
            if i+1 < len(intvals_list): # when i+1 = len(intvals_list), there is no next interval
                intv_length = intvals_list[i+1] - intvals_list[i]
                ind_to_len[i] = intv_length
            
        return (intv_to_ind, ind_to_len)
        
    def _update_bounds(self, cuboid: Cuboid):
        self._min_x = min(self._min_x, cuboid.x_range[0])   # E.g. 0
        self._min_y = min(self._min_y, cuboid.y_range[0])
        self._min_z = min(self._min_z, cuboid.z_range[0])
        self._max_x = max(self._max_x, cuboid.x_range[1])   # E.g. 0 -> 12 -> 13
        self._max_y = max(self._max_y, cuboid.y_range[1])
        self._max_z = max(self._max_z, cuboid.z_range[1])

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    instructions: list[Instruction] = []
    pattern = re.compile(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")
    for line in data:
        if (match := pattern.match(line)):
            instr, x_min, x_max, y_min, y_max, z_min, z_max = match.groups()
            reactor = Cuboid((int(x_min), int(x_max)), (int(y_min), int(y_max)), (int(z_min), int(z_max)))
            instructions.append(Instruction(instr, reactor))
    
    # Part 1 - Count how many cubes are on, with small bounds
    reactor = Reactor(bound=50)
    for i, instr in enumerate(instructions):
        logger.debug("Processing instruction %d; there are %d left", i+1, len(instructions)-(i+1))
        reactor.update(instr)

    logger.info("Part 1 using CuboidSet - cubes on: %s\n", reactor.cells_on)

    # Part 2 - Count how many cubes are on, with no bounds
    reactor = CuboidDeterminator(instructions)
    logger.info("Part 2 cubes on: %d", reactor.cells_on)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
