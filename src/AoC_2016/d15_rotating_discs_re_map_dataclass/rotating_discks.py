"""
Author: Darren
Date: 06/08/2021

Solving https://adventofcode.com/2016/day/15

Overview:
    A stack of rotating disks, where each disc has a slot big enough to allow a capsule to fall through.
    Disks rotate and pause each second.  
    Each disc has a fixed number of positions they will pause at. E.g. a disk with 5 positions has positions 0-4.
    Position 0 is the position with the slot aligned to the falling capsule.
    The discs in the stack are spaced out so that the time taken for the capsule to pass from one disk to the next is 1s.
    E.g. if we push the button at t=100, the capsule reaches top disk (n) at 101, reaches n+1 at 102, etc.

Solution:
    Use a Disc dataclass.  Each disc is able to determine its position at any given time.
    Create Discs with regex.
    At each incrementing time t, determine the position of each disc, 
    bearing in mind that successive discs are reached at t = t+1.
    
Part 1:
    What is the first time we can press the button and the capsule will fall through all discs?
    Use a disc object, where we increment the disc position based on the time when the capsule arrives.
    Takes 0.1s.

Part 2:
    We've added another disc.
    Now takes 1s.    
"""
import logging
import os
import time
import re
from dataclasses import dataclass

#pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

disc_params_match = re.compile(r"Disc #(\d+) has (\d+) positions; at time=(\d+), it is at position (\d+).")

@dataclass
class Disc:
    """ Disc Dataclass 
    Knows how to return its own position at any given time in seconds. """
    disc_num: int
    positions_count: int
    start_time: int
    position: int
        
    def get_position_at_time(self, t) -> int:
        return (self.position + t) % self.positions_count
        
    def __str__(self):
        return f"{self.__class__.__name__}: num={self.disc_num}, position={self.position}"

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
        
    discs: list[Disc] = []
    for line in data:
        if match := disc_params_match.search(line):
            disc_num, disc_positions, disc_time, disc_position = map(int, match.groups())
            discs.append(Disc(disc_num, disc_positions, disc_time, disc_position))

    t = 0
    # loop until we find a drop time t, where all discs are aligned
    while True:
        all_discs_aligned = True
        for i, disc in enumerate(discs, 1): # we reach the 1st disc at time t=t+1, 2nd at t=t+2, etc
            time_at_this_disc = t+i
            
            # We need all discs to be at position 0
            if disc.get_position_at_time(time_at_this_disc) != 0:
                all_discs_aligned = False
                break
            
        if all_discs_aligned:
            logging.info(f"All discs aligned at t={t}")
            break
        
        t += 1


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
