"""
Author: Darren
Date: 15/12/2022

Solving https://adventofcode.com/2022/day/15

Sensors deploy to specific locations and detect the single nearest beacon at a specific location.
The nearest beacon is measured as Manhattan distance. 

Part 1:

In the row where y=2000000, how many positions CANNOT contain a beacon?

Soln:

- Create Point class which knows how to determine Manhattan distance to another point.
- Read in input data, to create a dict of Sensor -> Nearest beacon.
- Create SensorGrid class:
  - Store Sensor -> Beacon dict.
  - coverage_for_row() returns the x values covered by existing sensors.
    - Get all the sensors that are within range of this row
    - For each sensor, determine the max horizontal vector that is possible in this row,
      but calculating the Manhattan distance and subtracting the vertical distance to this row.
      Thus, each sensor gives gives us an interval in the form (start, end), representing a range on the row.
    - Take all the intervals, and merge them into the smallest number of non-overlapping intervals.
    - Add up ((end+1)-start) for each interval, 
      to find the total number of x locations where a beacon cannot be.

Part 2:

The distress beacon has not been detected by any of sensors.
It must have x and y coordinates each no lower than 0 and no larger than 4000000.
There is only one valid position.

Determine its position. Then, it's "tuning frequency" is given by 
multiplying its x coordinate by 4000000 and then adding its y coordinate.

Soln:

- The distress beacon must be distance=1 outside an existing beacon.
- Find all locations that sit outside the perimeter of all sensor coverage areas.
  - I.e. determine all points at d+1 relative to a sensor.
  - For each of these points, check whether the point outside all coverage intervals for this row y.
  - We use this using the same row coverage approach as Part 1.
  - If there are any gaps between coverage intervals, then this is where our x must be.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import time

SCRIPT_DIR = Path(__file__).parent
TUNING_FREQ_MULTIPLIER = 4000000

# Test data
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# TARGET_ROW = 10
# DISTRESS_X_BOUNDS = (0, 20)
# DISTRESS_Y_BOUNDS = (0, 20)

# Real data
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
TARGET_ROW = 2000000
DISTRESS_X_BOUNDS = (0, 4000000)
DISTRESS_Y_BOUNDS = (0, 4000000)

@dataclass(frozen=True)
class Point():
    """ Point with x, y coords. Knows how to add a vector, remove a vector, 
    and calculate Manhattan distance to to another point. """
    x: int
    y: int
    
    def __sub__(self, other):
        """ Subtract other point from this point, returning new point vector """
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """ Subtract other point from this point, returning new point vector """
        return Point(self.x + other.x, self.y + other.y)        
    
    def manhattan_distance_to(self, other: Point) -> int:
        """ Manhattan distance between this Vector and another Vector """
        diff = self - other
        return sum((abs(diff.x), abs(diff.y)))

class SensorGrid():
    """ Stores a grid of Sensors, and each sensor's nearest beacon. """
    
    def __init__(self, sensor_to_beacon: dict[Point, Point]) -> None:
        """ Takes a dictionary of Sensors and their beacons """
        self.sensor_to_beacon = sensor_to_beacon
        self.beacons = set(sensor_to_beacon.values())
        self.sensor_range = {s: b.manhattan_distance_to(s) 
                             for s, b in self.sensor_to_beacon.items()}
            
        self._init_bounds()

    def _init_bounds(self):
        """ Get the bounds by finding min and max values of any scanner or beacon,
        then adding to each edge the maximum distance we've found for any Scanner->Beacon """
        max_distance = max(self.sensor_range.items(), key=lambda x: x[1])[1]    
        self.min_x = self.min_y = self.max_x = self.max_y = 0
        for s, b in self.sensor_to_beacon.items():
            self.min_x = min([self.min_x, s.x, b.x])
            self.max_x = max([self.max_x, s.x, b.x])
            self.min_y = min([self.min_y, s.y, b.y])
            self.max_y = max([self.max_y, s.y, b.y])

        self.min_x -= max_distance
        self.min_y -= max_distance
        self.max_y += max_distance
        self.max_x += max_distance

    def test_points_outside_perimeter(self) -> Point:
        """ The signal beacon must be one outside of the perimeter of existing sensor boundaries. """
        for sensor_point, dist_to_nearest in self.sensor_range.items():
            for dx in range(dist_to_nearest+2): # max dx is dist_to_nearest + 1
                dy = (dist_to_nearest+1) - dx   # To always be on perimeter, dx+dy must be dist_to_nearest + 1
                
                for sign_x, sign_y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]: # Add our dx and dy in all directions
                    x = sensor_point.x + (dx * sign_x)
                    y = sensor_point.y + (dy * sign_y)
                    
                    # Check within the bounds defined; if not, try next dx and dy
                    if not (DISTRESS_X_BOUNDS[0] <= x <= DISTRESS_X_BOUNDS[1]
                            and DISTRESS_Y_BOUNDS[0] <= y <= DISTRESS_Y_BOUNDS[1]):
                        continue

                    coverage = self.coverage_for_row(y) # get all disallowed intervals
                    # look for a gap between any intervals
                    if len(coverage) > 1:
                        for i in range(1, len(coverage)+1):
                            if coverage[i][0] > coverage[0][1] + 1:
                                x = coverage[i][0] - 1
                                print(f"x must be {x}")
                                return Point(x,y)
        
        return None
    
    def tuning_frequency(self, point: Point) -> int:
        return point.x * TUNING_FREQ_MULTIPLIER + point.y
                                                       
    def _get_row_coverage_intervals(self, row: int) -> list[list]:
        """ For each nearby sensor, get all x interval for this row.
        Each sensor will return a range of coverage, like [a, b].
        So all sensors will return a list of ranges, like [[a, b][c, d][d, e]...] """
        
        # Get only the sensors that are within range of this row
        close_sensors = {s:r for s, r in self.sensor_range.items() if abs(s.y - row) <= r}
        
        intervals: list[list] = [] # store start and end y for each sensor
        for sensor, max_rng in close_sensors.items():
            vert_dist_to_row = abs(sensor.y - row)
            max_x_vector = (max_rng - vert_dist_to_row)
            start_x = sensor.x - max_x_vector
            end_x = sensor.x + max_x_vector
            intervals.append([start_x, end_x])

        return intervals
    
    def _merge_intervals(self, row: int) -> list[list]:
        """ Takes intervals in the form [[a, b][c, d][d, e]...]
        Intervals can overlap.  Compresses to minimum number of non-overlapping intervals. """
        intervals = self._get_row_coverage_intervals(row)
        intervals.sort()
        stack = []
        stack.append(intervals[0])
        
        for interval in intervals[1:]:
            # Check for overlapping interval
            if stack[-1][0] <= interval[0] <= stack[-1][-1]:
                stack[-1][-1] = max(stack[-1][-1], interval[-1])
            else:
                stack.append(interval)
         
        return stack
    
    def coverage_for_row(self, row: int) -> list:
        return self._merge_intervals(row)

    def __str__(self) -> str:
        rows = []
        for y in range(self.min_y, self.max_y + 1):
            row = ""
            for x in range(self.min_x, self.max_x + 1):
                point = Point(x,y)
                if point in self.sensor_to_beacon.keys():
                    row += "S"
                elif point in self.beacons:
                    row += "B"
                else:
                    row += "."
            
            rows.append(row)
        
        return "\n".join(rows)   
    
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    grid = SensorGrid(process_sensors(data))

    # Part 1
    total_coverage = grid.coverage_for_row(TARGET_ROW)
    coverage_count = sum(interval[1]-interval[0]+1 for interval in total_coverage)
    beacons_to_exclude = sum(1 for beacon in grid.beacons if beacon.y == TARGET_ROW)
    print(f"Part 1 - row {TARGET_ROW}: {coverage_count - beacons_to_exclude}")  
    
    # # Part 2: we need to find the only non-coverage point in the given area
    beacon_location = grid.test_points_outside_perimeter()
    print(f"Part 2: point={beacon_location}, tuning freq={grid.tuning_frequency(beacon_location)}")

def process_sensors(data) -> dict[Point, Point]:
    # Find four digits, preceeded by "not digit"
    pattern = re.compile(r"[\D]+x=(-?\d+)[\D]+y=(-?\d+)[\D]+x=(-?\d+)[\D]+y=(-?\d+)")
    sensor_to_beacon: dict[Point,Point] = {}
    for line in data:
        sx, sy, bx, by = map(int, pattern.findall(line)[0])
        sensor_to_beacon[Point(sx, sy)] = Point(bx, by)
    
    return sensor_to_beacon

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
