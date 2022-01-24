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
from dataclasses import dataclass
import logging
from pathlib import Path
import time
import re
from matplotlib import pyplot as plt

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

RENDER = False
OUTPUT_DIR = Path(SCRIPT_DIR, "output/")
OUTPUT_FILE = Path(OUTPUT_DIR, "trajectory.png")

@dataclass(frozen=True)
class Point():
    x: int
    y: int

class Velocity(Point):
    """ A vector represented as (x, y) values """
    
@dataclass
class Rect():
    """ Rectangle from four corner Points, and knows whether a point is enclosed """
    left_x: int
    right_x: int
    bottom_y: int
    top_y: int

    def encloses(self, point:Point) -> bool:
        return (self.left_x <= point.x <= self.right_x 
                and self.bottom_y <= point.y <= self.top_y)
        
    def as_polygon(self) -> tuple[list, list]:
        """ Convert to set of polygon points, in the order tl, tr, br, bl, 
        and returned as (list of x coords, list of y coords) """
        return ([self.left_x, self.right_x, self.right_x, self.left_x],
                [self.top_y, self.top_y, self.bottom_y, self.bottom_y])

def main():
    input_file = Path(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().strip()
    
    # Note that x and y values can be -ve
    match = re.search(r"x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", data)
    assert match, "Don't expect invalid input data"
    target = Rect(*map(int, match.groups()))
    logger.info(target)
    
    successful_peaks = {}    # init_velocity: peak
    highest_trajectory = []
    max_y = 0
    for x in range(1, target.right_x+1):   # No point having x larger than max target distance
        for y in range(target.bottom_y, abs(target.bottom_y)):   # remember we can fire up
            init_v = Velocity(x, y)
            hit, trajectory = evaluate_trajectory(target, init_v)
            if hit:     # if this was a good trajectory to hit the target
                this_max_y = max(point.y for point in trajectory) 
                successful_peaks[init_v] = this_max_y  # store the heighest point for this init_v               
                if this_max_y > max_y:  # If this trajectory has given a new highest point
                    highest_trajectory = trajectory
                    max_y = this_max_y             
    
    logger.info("Max peak=%d", max_y)
    logger.info("Count of valid shots=%d", len(successful_peaks))

    if RENDER:
        plot_trajectory(highest_trajectory, target) # show the plot    
    else:
        plot_trajectory(highest_trajectory, target, OUTPUT_FILE) # save the plot

def evaluate_trajectory(target: Rect, initial_v: Velocity) -> tuple[bool, list[Point]]:
    """ Given a target region to hit and an initial velocity, 
    determine if we will hit the target on any step.

    Args:
        target (Rect): Region we need to hit
        initial_v (Velocity): Initial x, y velocity at t=0

    Returns:
        tuple[bool, list[Point]]: Whether trajectory hit the target, and the path taken.
    """
    t = 0
    location = Point(0,0)  # Where we launch our probe from
    trajectory: list[Point] = [location]
    hit_target = False
    
    while not hit_target:
        vel = velocity_at_step(initial_v, t)
        location = Point(location.x + vel.x, location.y + vel.y)
        trajectory.append(location)
                
        if (vel.x == 0 and location.x < target.left_x):
            break   # we're just going to fall downwards from here.
                
        if location.x > target.right_x or location.y < target.bottom_y:
            break   # we've overshot the target
                
        if target.encloses(location): # If we've hit the target
            hit_target = True
            break

        # If we're here, we haven't yet reached the target
        t += 1
        
    return hit_target, trajectory
                
def velocity_at_step(init: Velocity, t: int) -> Velocity:
    """ Returns the velocity (x,y) at a given step. """
    x = abs(init.x) - t if t < init.x else 0
    y = init.y - t
    
    return Velocity(x, y)

def plot_trajectory(trajectory: list[Point], target: Rect, outputfile=None):
    """ Render this trajectory as a plot, and optionally save it """
    axes = plt.gca()
    
    # Add axis lines at x=0 and y=0
    plt.axhline(0, color='green')
    plt.axvline(0, color='green') 
    axes.grid(True) # grid lines on
    
    # Set up titles
    axes.set_title("Trajectory")
    axes.set_xlabel("Horizontal")
    axes.set_ylabel("Height")
    
    axes.fill(*target.as_polygon(), 'cyan')  # add the target area
    plt.annotate("TARGET", (target.left_x, target.top_y), 
                 xytext=(target.left_x + ((target.right_x - target.left_x)/2)-2, 
                        (target.top_y - (target.top_y-target.bottom_y)/2)-1), 
                 color="blue", weight='bold') 
    
    # Plot the trajectory points
    all_x = [point.x for point in trajectory]
    all_y = [point.y for point in trajectory]
    plt.plot(all_x, all_y, marker="o", markerfacecolor="red", markersize=4, color='black')
    
    x, y = trajectory[1].x, trajectory[1].y
    plt.annotate(f"Vel {x},{y}", (x,y), xytext=(x-3, y+2))  # label first point
    x, y = [(point.x, point.y) for point in trajectory if point.y == max(point.y for point in trajectory)][0]
    plt.annotate(f"({x},{y})", (x,y), xytext=(x+1, y-1))  # label highest point    
        
    if outputfile:
        dir_path = Path(outputfile).parent
        if not Path.exists(dir_path):
            Path.mkdir(dir_path)
        plt.savefig(outputfile)
        logger.info("Plot saved to %s", outputfile)        
    else:
        plt.show()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
