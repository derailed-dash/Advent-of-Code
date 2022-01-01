"""
Author: Darren
Date: 17/12/2021

Solving https://adventofcode.com/2021/day/17

We need to fire a probe into a large ocean trench. 
Firing from 0,0 with velocity x,y.  +ve y means up.
x and y are distance travelled by per unit t.
x velocity decreases by 1 towards 0 with each step, due to drag.
y velocity always decreases by 1, due to gravity. So if -ve, will get more -ve.

To enter the trench, the probe must be on a trajectory that causes it to 
pass through a target area. It must be WITHIN the target area at any given value of t.

Target area looks like: x=20..30, y=-10..-5       20,-5 xxxxxxxxxxx 30,-5
                                                        xxxxxxxxxxx
                                                        xxxxxxxxxxx
                                                        xxxxxxxxxxx
                                                        xxxxxxxxxxx
                                                 20,-10 xxxxxxxxxxx 30,-10

I.e. a rectangular range that is inclusive of the x and y values provided.

Part 1:
    What is the highest y position we can achieve on any successful trajectory?

    First, use a formula to calculate velocity at step t, given an initial velocity.
    Then, loop through range of initial velocities, with:
    - x from 0 to x_right, since we can only fire right, towards the target.
    - y from bottom_y to abs(bottom_y), since we can fire both down towards the target, 
      but also up.
    Then, loop infinitely through steps, and determine x,y locations at each step.
    Store max y achieved in this loop so far.
    Build a dict of {init vel: max y} for any init velocities that hit the target.
    
    Finally, return the max y overall.

Part 2:
    Find every initial velocity that causes the probe to be within the target area
    at any time t.
"""
import logging
import os
import time
import re
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int
    
class Velocity(Point):
    """ A vector represented as (x, y) values """
    
class Rect(NamedTuple):
    """ Rectangle from four corner Points, and knows whether a point is enclosed """
    left_x: int
    right_x: int
    bottom_y: int
    top_y: int

    def encloses(self, point:Point) -> bool:
        return (self.left_x <= point.x <= self.right_x 
                and self.bottom_y <= point.y <= self.top_y)

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
    
    # Note that x and y values can be -ve
    match = re.search(r"x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", data)
    target = Rect(*map(int, match.groups()))
    logger.info(target)
    
    successful_peaks = {}    # init_velocity: peak
    for x in range(1, target.right_x+1):   # No point having x larger than max target distance
        for y in range(target.bottom_y, abs(target.bottom_y)):   # remember we can fire up
            init_v = Velocity(x, y)
            hit, res = evaluate_trajectory(target, init_v)
            if hit:
                successful_peaks[init_v] = res
    
    logger.info("Max peak=%d", max(successful_peaks.values()))
    logger.info("Count of valid shots=%d", sum(1 for peak in successful_peaks))

def evaluate_trajectory(target: Rect, initial_v: Velocity) -> tuple[bool, int]:
    t = 0
    location = Point(0,0)  # Where we launch our probe from
    max_y_so_far_this_trajectory = target.bottom_y
    hit_target = False
    
    while not hit_target:
        vel = velocity_at_step(initial_v, t)
        location = Point(location.x + vel.x, location.y + vel.y)             
        max_y_so_far_this_trajectory = max(location.y, max_y_so_far_this_trajectory)
                
        if (vel.x == 0 and location.x < target.left_x):
            break   # we're just going to fall downwards from here.
                
        if location.x > target.right_x or location.y < target.bottom_y:
            break   # we've overshot the target
                
        if target.encloses(location): # If we've hit the target
            hit_target = True
            break

        # If we're here, we haven't yet reached the target
        t += 1
        
    return hit_target, max_y_so_far_this_trajectory
                
def velocity_at_step(init: Velocity, t: int) -> Velocity:
    """ Returns the velocity (x,y) at a given step. """
    x = abs(init.x) - t if t < init.x else 0
    y = init.y - t
    
    return Velocity(x, y)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
