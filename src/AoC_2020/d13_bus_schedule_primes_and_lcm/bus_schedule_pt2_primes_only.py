"""
Author: Darren
Date: 13/12/2020

Solving: https://adventofcode.com/2020/day/13

Solution 2 of 2:

Part 2
------
Input like: 7,13,x,x,59,x,31,19

Find first time where 7 departs at t=0, 13 departs at t=1, x departs at t=2, etc.
Bus ID also represents the duration of each bus loop.
E.g. bus 7 departs every 7 minutes.
x departure times and IDs are irrelevant.

Schedules are always prime. So easy to find schedules that align using LCM if any two schedules,
which is always the product of two schedules.
"""
import os
import time
from math import gcd
from pprint import pprint as pp

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/bus_schedule.txt"
SAMPLE_INPUT_FILE = "input/sample_schedule.txt"


def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    buses = read_input(input_file)
    # print(buses)
    
    current_bus = find_aligned_buses(buses)
    print(current_bus[2])


def lowest_common_multiple(a, b):
    # Since all the a and b values supplied are primes, 
    # we don't really need to divide by gcd (HCF), since gcd will always be 1 for two primes
    return (a*b) // gcd(a, b)


def find_aligned_buses(buses):
    buses_with_offsets = []
    for i, bus in enumerate(buses):
        # here i represents the offset from the departure time, in minutes
        if bus != "x":
            # bus_num (schedule), offset from first bus, departure timestamp
            # set the depart timestamp to 0
            # E.g. (7, 0, 0), (13, 1, 0), (59, 4, 0), etc
            buses_with_offsets.append((int(bus), i, 0))

    pp(buses_with_offsets)

    # iterate over buses
    # with each iteration, set current bus to represent schedule that aligns with the buses
    # that we've looked at before.
    # E.g. once we've evaluated buses 7 an 13, this can be represented as a single bus #91.
    period = buses_with_offsets[0]
    for i in range(1, len(buses_with_offsets)):
        period = find_two_bus_pattern(period, buses_with_offsets[i])
    
    return period


def find_two_bus_pattern(bus1, bus2):
    # Two buses will align with periodicity that matches LCM.

    # LCM is given by HCF / LCM.  But with two primes, LCM is always 1.
    # Thus, since our bus schedules are always primes, LCM is simply bus1*bus2
    # E.g. with buses 7 and 13, LCM = 91
    lcm = lowest_common_multiple(bus1[0], bus2[0])
    departure_timestamp = get_timestamp(bus1, bus2)

    # We create a new period that represents the alignment of these two buses
    # and store the first time bus1 and bus2 align with the required offset as timestamp.
    # return bus: (bus#=LCM, offset, timestamp)
    print(f"Returning {(lcm, 0, departure_timestamp)}")
    return lcm, 0, departure_timestamp


def get_timestamp(bus1, bus2):
    bus2_relative_delta = bus2[1] - bus1[1]

    departure_timestamp = bus1[2]

    # we need a bus 1 departure time where
    # bus 1 departure time + bus 2 offset is divisible by bus 2 period
    while (departure_timestamp + bus2_relative_delta) % bus2[0] != 0:
        # repeat until multiple of bus1 + offset is divisible by bus2 cycle
        # with 7 and 13, this happens at 77 and 168
        departure_timestamp += bus1[0]
    return departure_timestamp
        
        
def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines[1].split(",")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

