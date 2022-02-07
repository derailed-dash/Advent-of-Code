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
    We use "coordinate compression" to remove all cubes where nothing happens, 
    leaving only coordinates where something interesting happens, i.e. where an instruction turns cubes on or off.
    So
      - Get all the intervals created by all the instructions.
      - Order them, and then aggregate them into blocks based on the intervals lengths along each axis.
      - Then run through instructions again, adding intervals in order.
      - We end up with about 130m intervals, and we have to work out the products for these, and sum them.
    
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
# INPUT_FILE = "input/input.txt"
INPUT_FILE = "input/sample_input.txt"

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
    """ Represents number of points that are turned on in a 3D space. This class works by tracking intervals.
    Instructions are pre-processed to determine all intervals, i.e. vertices and intersections. 
    Then we sort them in each dimension, and have a map of each to an interval length. 
    Finally, intervals and their corresponding lengths can be used to determine the size of 'on' cuboids. """
    
    def __init__(self, instructions: list[Instruction]) -> None:
        self._instructions = instructions
        self._cells_on = self._process_instructions()

    @property
    def cells_on(self):
        return self._cells_on
    
    def _process_instructions(self) -> int:
        """ Process all the instructions, e.g. 
        on x=10..12,y=10..12,z=10..12, on x=11..13,y=11..13,z=11..13.
        Instruction order is not important.  We'll convert to an ordered list.
        
        Returns int: Total cubes turned on. """
        
        # Here we will store all cube positions where something interesting happens, i.e. a cuboid begins or ends
        x_vals = []
        y_vals = []
        z_vals = []
                
        # Get all the intervals, i.e. where an instruction changes something
        for instruction in self._instructions:
            cuboid = instruction.cuboid
            
            # Add the intervals (vertices) in this instruction
            x_vals.append(cuboid.x_range[0])
            x_vals.append(cuboid.x_range[1]+1)
            y_vals.append(cuboid.y_range[0])
            y_vals.append(cuboid.y_range[1]+1)
            z_vals.append(cuboid.z_range[0])
            z_vals.append(cuboid.z_range[1]+1)
    
        # All dimensions in numeric order
        x_vals.sort()
        y_vals.sort()
        z_vals.sort()
        
        # Store the intervals between each successive value in a given dimension        
        x_intervals = [x_vals[i+1]-x_vals[i] for i in range(len(x_vals)-1)]
        y_intervals = [y_vals[i+1]-y_vals[i] for i in range(len(y_vals)-1)]
        z_intervals = [z_vals[i+1]-z_vals[i] for i in range(len(z_vals)-1)]
        
        on_indexes = set()
        
        # Now apply on and off instructions
        # I.e. add or remove cuboids in the right order
        for i, instruction in enumerate(self._instructions):
            cuboid = instruction.cuboid
            logger.debug("Instruction %d (of %d)=%s: %s", i+1, len(self._instructions), instruction.on_or_off, cuboid)
            
            # unpack the vertices of this cuboid
            x1, x2 = cuboid.x_range[0], cuboid.x_range[1]
            y1, y2 = cuboid.y_range[0], cuboid.y_range[1]
            z1, z2 = cuboid.z_range[0], cuboid.z_range[1]
            
            # Get the appropriate intervals given by these coordinates
            # E.g. for cuboid (10,12),(10,12),(10,12), we turn on a 3x3x3 cuboid of cells.
            # E.g. x_intv_index in range(1, 4) = 3 interval indexes
            for x_intv_index in range(x_vals.index(x1), x_vals.index(x2+1)):
                for y_intv_index in range(y_vals.index(y1), y_vals.index(y2+1)):
                    for z_intv_index in range (z_vals.index(z1), z_vals.index(z2+1)):
                        if instruction.on_or_off == "on":
                            # add intervals corresponding to cuboids turned on
                            on_indexes.add((x_intv_index, y_intv_index, z_intv_index)) # E.g. (1, 1, 1)
                        else:
                            # remove intervals corresponding to cuboids turned off
                            on_indexes.discard((x_intv_index, y_intv_index, z_intv_index)) # E.g. (0, 0, 0)
           
        logger.debug("Computing interval volumes for %d on indexes. This might take a while...", len(on_indexes))
        total_cells_on = 0
        # on_indexes contains, e.g. 39 different non-overlapping 'on' intervals
        # For each triplet of on intervals, get the corresponding lengths.
        # This gives us the size of the 'on cuboid', i.e. how many cells are on in the cuboid
        for x_intv_index, y_intv_index, z_intv_index in on_indexes:
            len_x = x_intervals[x_intv_index]
            len_y = y_intervals[y_intv_index]
            len_z = z_intervals[z_intv_index]
            total_cells_on += len_x * len_y * len_z
            
        return total_cells_on

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
