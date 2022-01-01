""" 
Author: Darren
Date: 14/02/2021

Solving https://adventofcode.com/2015/day/14

Various reindeer have speeds and rest times:
"Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds."

Solution:

Part 1:
    Compute distance travelled at time x.
    Determine the distance travelled by the reindeer that has gone furthest at t=2503.

Part 2:
    Each second, award a point to the reindeer currently in the lead.
    Use a defaultdict(int) to store the points.
    Determine which reindeer has the most points at t=2503.
"""
import os
import re
import time
from collections import defaultdict, namedtuple

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

# make our reindeer easier to work with
reindeer = namedtuple("reindeer", "name speed duration rest_time")

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    reindeer_list = process_reindeer_data(data)

    time = 2503

    # Part 1
    reindeer_distances = {}
    a_reindeer: reindeer
    for a_reindeer in reindeer_list:
        reindeer_distances[a_reindeer.name] = distance_travelled(a_reindeer, time)

    print("Distances: ")
    print(reindeer_distances)
    winner_on_distance = max(reindeer_distances.items(), key=lambda x: x[1])[0]
    print(f"Winning reindeer: {winner_on_distance} with distance of {reindeer_distances[winner_on_distance]}.")

    # Part 2
    reindeer_points = defaultdict(int)

    # we need to determine the winner for each second that has elapsed, 
    # and allocate a point to that reindeer
    for i in range(1, time+1):
        for a_reindeer in reindeer_list:
            reindeer_distances[a_reindeer.name] = distance_travelled(a_reindeer, i)

        current_winner = max(reindeer_distances.items(), key=lambda x: x[1])[0]
        reindeer_points[current_winner] += 1
    
    print("\nPoints:")
    for a_reindeer in reindeer_points:
        print(f"{a_reindeer}: {reindeer_points[a_reindeer]}")

    winner_on_points = max(reindeer_points.items(), key=lambda x: x[1])[0]
    print(f"Winning reindeer: {winner_on_points} who has {reindeer_points[winner_on_points]} points.")


def distance_travelled(a_reindeer: reindeer, time: int) -> int:
    """Computes the distance travelled by this reindeer in the time given

    Args:
        a_reindeer (reindeer):
        time (int): in seconds

    Returns:
        [int]
    """
    fulL_repeat = get_full_repeat(a_reindeer)
    total_repeats = time // fulL_repeat
    remainder = time % fulL_repeat
    remainder_travelling = min(remainder, a_reindeer.duration)

    return ((a_reindeer.duration*total_repeats) + remainder_travelling) * a_reindeer.speed


def get_full_repeat(a_reindeer: reindeer) -> int:
    return a_reindeer.duration + a_reindeer.rest_time


def process_reindeer_data(data) -> list:
    """Process input lines, and return a dict of reindeer

    Args:
        data : list of str, where each line is of the format:
            "Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds."

    Returns:
        [dict]: K is reindeer name, V is tuple of speed, duration, rest_time
    """    
    reindeer_pattern = re.compile(r"^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
    
    reindeer_list = []
    for line in data:
        reindeer_name, speed, duration, rest_time = reindeer_pattern.match(line).groups()
        reindeer_list.append(reindeer(reindeer_name, int(speed), int(duration), int(rest_time)))

    return reindeer_list

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
