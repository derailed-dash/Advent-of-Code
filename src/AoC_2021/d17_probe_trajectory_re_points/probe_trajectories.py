"""
Author: Darren
Date: 17/12/2021

Solving https://adventofcode.com/2021/day/17

Firing a probe with velocity x,y.  +ve y means up.
x velocity decreases by 1 towards 0 with each step.
y velocity always decreases by 1 (i.e. if -ve, will get more -ve)

Here we've gone with a brute force solution.  Takes a few seconds.
Suspect some optimisation could be done.

Part 1:
    First, use a formula to calculate velocity at step s.
    Then, loop through range of initial velocitise, with x from 0 to max x+1.
    and y from lowest target y to abs(lowest target y).
    Then, loop infinitely through steps, and determine x,y locations at each step.
    Store max y achieved in this loop so far.
    Build a dict of {init vel: max y} for any init velocities that hit the target.
    
    Finally, return the max y overall.

Part 2:
    Already solved in part 1.
"""
import logging
import os
import time
import re
from collections import namedtuple

Point = namedtuple("Pnt", "x y")  # Make it easier to index point x and y
Velocity = namedtuple("Vel", "x y")

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().strip()
    
    match = re.search(r"x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", data)
    # Note: x_min < x_max and y_min < y_max, but but abs(y_min) > abs(y_max)
    # I.e. y_min is the BOTTOM of the target
    t_x_min, t_x_max, t_y_min, t_y_max = map(int, match.groups())
    logger.info("x_min=%d, x_max=%d, y_min=%d, y_max=%d", t_x_min, t_x_max, t_y_min, t_y_max)
    
    start = Point(0,0)  # Where we launch our probe from
    
    successful_peaks = {}    # init_velocity: peak
    for x in range(1, t_x_max+1):   # No point having x larger than max target distance
        for y in range(t_y_min, abs(t_y_min)):   # remember we can fire up
            initial_v = Velocity(x,y)
            step = 0
            location = start
            max_y_so_far_this_route = t_y_min
            while True:
                vel = velocity_at_step(initial_v, step)
                location = Point(location.x + vel.x, location.y + vel.y)             
                max_y_so_far_this_route = max(location.y, max_y_so_far_this_route)
                
                if (vel.x == 0 and location.x < t_x_min):
                    break   # we're just going to fall downwards from here.
                
                # If we've missed the target
                if location.x > t_x_max or location.y < t_y_min:
                    break   # we've missed the target
                
                # If we've hit the target
                if t_x_min <= location.x <= t_x_max and t_y_min <= location.y <= t_y_max:
                    successful_peaks[initial_v] = max_y_so_far_this_route # store our successful peak
                    # logger.debug("Initial vel=%s, peak=%d", initial_v, max_y_so_far_this_route)
                    break
                
                step += 1
    
    logger.info("Max peak=%d", max(successful_peaks.values()))
    logger.info("Count of valid shots=%d", sum(1 for peak in successful_peaks))
                
def velocity_at_step(init: Velocity, n: int) -> Velocity:
    """ Returns the velocity (x,y) at a given step. """
    x = abs(init.x) - n if n < init.x else 0
    y = init.y - n
    
    return Velocity(x, y)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
