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
from dataclasses import dataclass
import os
import re
import time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

TIME = 2503

@dataclass
class Reindeer():
    """ A reindeer flies at *speed* (km/s) for a given *duration* (s), then must *rest* (s). """
    name: str
    speed: int
    duration: int
    rest: int
    
    def cycle_time(self) -> int:
        return self.duration + self.rest
    
    def distance_at_t(self, t: int) -> int:
        """Computes the distance travelled by this reindeer in the time given """
        total_cycles = t // self.cycle_time()
        remainder = t % self.cycle_time()
        remainder_travelling = min(remainder, self.duration)

        return ((self.duration*total_cycles) + remainder_travelling) * self.speed
    
def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    reindeer_list = process_reindeer_data(data)

    print("Part 1")
    winner = max(reindeer_list, key=lambda x: x.distance_at_t(TIME))
    print(f"Winning reindeer: {winner.name} with distance of {winner.distance_at_t(TIME)}.")
    
    print("\nPart 2")
    reindeer_points = defaultdict(int)

    # we need to determine the winner for each second that has elapsed, 
    # and allocate a point to that reindeer
    for i in range(1, TIME+1):
        current_winner = max(reindeer_list, key=lambda x: x.distance_at_t(i))
        reindeer_points[current_winner.name] += 1
    
    print("Points:")
    for a_reindeer in reindeer_points:
        print(f"{a_reindeer}: {reindeer_points[a_reindeer]}")

    winner_on_points = max(reindeer_points.items(), key=lambda x: x[1])[0]
    print(f"Winning reindeer: {winner_on_points} who has {reindeer_points[winner_on_points]} points.")

def process_reindeer_data(data) -> list[Reindeer]:
    """Process input lines, and return a dict of reindeer.
    Each line is of the format:
        "Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds."

    Returns: [list]: Reindeers
    """    
    reindeer_pattern = re.compile(r"^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
    
    reindeer_list = []
    for line in data:
        reindeer_name, speed, duration, rest = reindeer_pattern.findall(line)[0]
        reindeer_list.append(Reindeer(reindeer_name, int(speed), int(duration), int(rest)))

    return reindeer_list

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"\nExecution time: {t2 - t1:0.4f} seconds")
