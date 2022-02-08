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
    Okay, without bounds the solution space is too large to repeat Part 1.
    We don't need to keep track of every point.  We just need to track where intervals start and end.
    We use "coordinate compression" to remove all 'regions' where nothing happens, 
    leaving only coordinates where something interesting happens, i.e. where an instruction turns cubes on or off.
    So
      - Get sorted lists for all x, y, and z values in all the instructions.  This is where changes happen.
      - The values and their associated edges represent cuboid 'segments' which could be turned on or off.
      - Process instructions in order, determining which segments ultimately need to be turned on.
      - Work out the volume of all the on segments, and add them together.
    
    This is slow: 3 mins in CPython and 2 mins in PyPy.
"""
from __future__ import annotations
import logging
import os
import time
import re
from typing import NamedTuple
from bisect import bisect_left
from tqdm import tqdm

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
    def cubes_on(self):
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
    """ Represents number of points that are turned on in a 3D space. This class works using coordinate compression.
    Instructions are pre-processed to collapse to coordinates where something changes, i.e. the beginning or end of a cuboid.
    We obtain a sorted list of coordinates in each dimension, representing any interval boundaries in that dimension.
    For each boundary, we have an associated length of the corresponding cuboid 'segment'.
    Finally, we work out how many cubes there are in all the 'on' cuboid segments, and return the total. """
    
    def __init__(self, instructions: list[Instruction]) -> None:
        self._instructions = instructions

    def perform_reset(self) -> int:
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
        
        # Store the intervals (ranges) between each successive value in a given dimension        
        x_intervals = [x_vals[i+1]-x_vals[i] for i in range(len(x_vals)-1)]
        y_intervals = [y_vals[i+1]-y_vals[i] for i in range(len(y_vals)-1)]
        z_intervals = [z_vals[i+1]-z_vals[i] for i in range(len(z_vals)-1)]
        
        on_indexes = set()
        
        # Now apply on and off instructions, i.e. add or remove cuboids in the right order
        for instruction in tqdm(self._instructions):
            # unpack the vertices of this cuboid
            x1, x2 = instruction.cuboid.x_range[0], instruction.cuboid.x_range[1]
            y1, y2 = instruction.cuboid.y_range[0], instruction.cuboid.y_range[1]
            z1, z2 = instruction.cuboid.z_range[0], instruction.cuboid.z_range[1]
            
            # Determine all the cuboid 'segments' we need to turn on.
            # A given cuboid in an instruction could contain many smaller cuboid 'segments'.
            # Get the indexes for the values given by each instruction, in a given dimension.
            # E.g. the first cuboid might give us x1 of 0 and x2 of 2. 
            # (Because x=1 might be the start of a different cuboid.)
            x1_index, x2_index = bisect_left(x_vals, x1), bisect_left(x_vals, (x2+1))
            y1_index, y2_index = bisect_left(y_vals, y1), bisect_left(y_vals, (y2+1))
            z1_index, z2_index = bisect_left(z_vals, z1), bisect_left(z_vals, (z2+1))
            
            for x_intv_index in range(x1_index, x2_index):
                for y_intv_index in range(y1_index, y2_index):
                    for z_intv_index in range(z1_index, z2_index):
                        # add starting coords corresponding to cuboid segments to turn on / off
                        if instruction.on_or_off == "on":
                            on_indexes.add((x_intv_index, y_intv_index, z_intv_index))
                        else:
                            # use discard, to remove cuboid segments that we have previously 'turned on'
                            # I.e. because an off instruction might overlap.  
                            # If it doesn't overlap, there will be nothing to discard.
                            on_indexes.discard((x_intv_index, y_intv_index, z_intv_index))
        
        logger.info("%d 'on' segments identified.", len(on_indexes))
        logger.info("Computing interval volumes. This might take a while...")
        
        total_cubes_on:int = 0

        # Each 'on' coord will align to a triplet of interval lengths, i.e. to give the volume of that cuboid 'segment'.
        # This gives us the size of the 'on cuboid', i.e. how many cubes are 'on' in the cuboid
        # Wrap our set with tqdm to provide a progress bar
        for x_intv_index, y_intv_index, z_intv_index in tqdm(on_indexes):
            len_x = x_intervals[x_intv_index]
            len_y = y_intervals[y_intv_index]
            len_z = z_intervals[z_intv_index]
            total_cubes_on += len_x * len_y * len_z
        
        return total_cubes_on

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
    logger.info("Part 1:")
    reactor = Reactor(bound=50)
    for instr in tqdm(instructions):
        reactor.update(instr)

    logger.info("Using CuboidSet - cubes on: %d\n", reactor.cubes_on)

    # Part 2 - Count how many cubes are on, with no bounds
    logger.info("Part 2:")
    reactor = CuboidDeterminator(instructions)
    logger.info("Using CuboidDeterminator - cubes on: %d", reactor.perform_reset())

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
