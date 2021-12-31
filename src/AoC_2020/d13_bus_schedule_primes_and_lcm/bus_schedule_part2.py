"""
Author: Darren
Date: 13/12/2020

Solving: https://adventofcode.com/2020/day/13

Solution 1 of 2: doing it the hard way

Part 2
------
Input like: 7,13,x,x,59,x,31,19

Find first time where 7 departs at t=0, 13 departs at t=1, x departs at t=2, etc.
Bus ID also represents the duration of each bus loop.
E.g. bus 7 departs every 7 minutes.
x departure times and IDs are irrelevant.
"""

import sys
import os
import time
from operator import itemgetter
from pprint import pprint as pp

INPUT_FILE = "input/bus_schedule.txt"
SAMPLE_INPUT_FILE = "input/sample_schedule.txt"


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    # input_file = os.path.join(script_dir, INPUT_FILE)
    input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    buses = split_input(read_input(input_file))
    print(buses)
    
    current_bus = find_aligned_buses(buses)
    
    # offset of uber bus -> the first time that all buses are aligned & first bus departs
    print(current_bus[0])


def find_aligned_buses(buses):
    buses_with_offsets = []
    for i, bus in enumerate(buses):
        # here i represents the offset from the departure time, in minutes
        if bus != "x":
            # start offset (initially 0), bus_num (schedule), offset from first bus
            buses_with_offsets.append((0, int(bus), i))

    pp(buses_with_offsets)

    # iterate over buses
    # with each iteration, set current bus to represent schedule that aligns with the buses
    # that we've looked at before.
    # E.g. once we've evaluated buses 7 an 13, this can be reprsented as a single bus #91.
    current_bus = buses_with_offsets[0]
    for i in range(1, len(buses_with_offsets)):
        current_bus = find_aligned_bus_from_pair(current_bus, buses_with_offsets[i])
    return current_bus


def find_aligned_bus_from_pair(bus1, bus2):
    # We want to create a 'new bus' that represents two buses
    # Determine the first and second times that these two buses align
    # we save it as 'offset' and 'cycle_length'
    # delta of new bus is 0! (you can imagine that uber-buses depart longer than 1min)

    # bus -> (offset, bus ID (cycle_length), bus 'delta')
    cycle, cycle_start = False, None
    bus2_relative_delta = bus2[2] - bus1[2]

    # index stores incrementing multiple of bus cycle (e.g. 7)
    bus1_multiple = bus1[0]
    while not cycle:
        # repeat until multiple of bus1 + offset is divisible by bus2 cycle
        # with 7 and 13, this happens at 77 and 168
        if (bus1_multiple + bus2_relative_delta) % bus2[1] == 0:
            if cycle_start is None:
                # start the cycle
                cycle_start = bus1_multiple
            else:
                # cycle found - we've got all we need
                return cycle_start, bus1_multiple - cycle_start, 0
        bus1_multiple += bus1[1]

        
def split_input(input_data):
    return input_data[1].split(",")


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

