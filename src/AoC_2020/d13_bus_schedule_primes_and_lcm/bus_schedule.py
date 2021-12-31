"""
Author: Darren
Date: 13/12/2020

Solving: https://adventofcode.com/2020/day/13

Part 1
------

Input like:
939
7,13,x,x,59,x,31,19

First line is the estimate of earliest departure timestamp.
Second line lists bus IDs, which are also the time taken by each of their loops.
What is the earliest bus we can take?
"""

import sys
import os
import time
from operator import itemgetter
from pprint import pp

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/bus_schedule.txt"
SAMPLE_INPUT_FILE = "input/sample_schedule.txt"


def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input_data = read_input(input_file)
    target, bus_sched = split_input(input_data)
    print(f"Target time: {target}")

    bus = process_schedule(target, bus_sched)
    bus_num = bus[0]
    bus_time = bus[1]
    print(f"Earliest available bus: {bus[0]} at time {bus[1]}")
    print(f"Solution answer: {(bus_time - target) * bus_num}")


def process_schedule(target, sched):
    # build dict to store the earliest time for a given bus ID, after our target time
    buses = {}

    for bus in sched:
        # e.g. 7
        if bus.isnumeric():
            bus_sched = int(bus)
            buses[bus_sched] = compute_first_available_time(target, bus_sched)

    # return the bus with minimum time (value), not minimum bus ID (key)
    return min(buses.items(), key=itemgetter(1))


def compute_first_available_time(target, bus_sched):
    next_time = 0
    while True:
        next_time += bus_sched
        if (next_time >= target):
            return next_time
    

def split_input(input_data):
    bus_sched = input_data[1].split(",")
    return int(input_data[0]), bus_sched


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

