"""
Author: Darren
Date: 15/12/2022

Solving https://adventofcode.com/2022/day/15

Sensors deploy to specific locations and detect the single nearest beacon at a specific location.
The nearest beacon is measured as Manhattan distance. 

Part 1:

In the row where y=2000000, how many positions CANNOT contain a beacon?

Soln:

- Nearest beacon to a sensor gives Manhattan distance. 
- Thus, we can establish overlapping coverage for each row.
- We need to establish the superset of all coverage on a row. 

Part 2:

To isolate the distress beacon's signal, you need to determine its tuning frequency,
which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.


"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import time

SCRIPT_DIR = Path(__file__).parent
TUNING_FREQ_MULTIPLIER = 4000000

# Test data
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
TARGET_ROW = 10
DISTRESS_X_BOUNDS = (0, 20)
DISTRESS_Y_BOUNDS = (0, 20)

# Real data
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# TARGET_ROW = 2000000
# DISTRESS_X_BOUNDS = (0, 4000000)
# DISTRESS_Y_BOUNDS = (0, 4000000)

@dataclass(frozen=True)
class Point():
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
    def __init__(self, sensor_to_beacon: dict[Point, Point]) -> None:
        self.sensor_to_beacon = sensor_to_beacon
        self.beacons = set(sensor_to_beacon.values())
        self.sensor_range = {s: b.manhattan_distance_to(s) 
                             for s, b in self.sensor_to_beacon.items()}
        
        max_distance = max(self.sensor_range.items(), key=lambda x: x[1])[1]

        # Get the bounds by finding min and max values of any scanner or beacon
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
        
    def valid_for_beacon(self, candidate: Point):
        """ Determine if the specified location can contain a beacon. 
        If this candidate location is less than or equal to the distance between a sensor and its nearest beacon,
        then this location is invalid. """
        for sensor_point, dist_to_nearest in self.sensor_range.items():
            dist = sensor_point.manhattan_distance_to(candidate)
            if dist <= dist_to_nearest:
                return False
        
        return True
    
    def _get_row_coverage_intervals(self, row: int) -> set[tuple]:
        """ For each nearby sensor, get all the possible x covered for this row """
        
        close_sensors = {s:r for s, r in self.sensor_range.items() if abs(s.y - row) <= r}
        row_coverage: set[tuple] = set() # store start and end y for each sensor
        for s, r in close_sensors.items():
            vert_dist_to_row = abs(s.y - row)
            max_x_vector = (r - vert_dist_to_row)
            start_x = s.x - max_x_vector
            end_x = s.x + max_x_vector
            row_coverage.add((start_x, end_x))
    
        return row_coverage
    
    def compress_coords(self, row: int):
        y_intervals_inclusive = []
        for interval in self._get_row_coverage_intervals(row):
            y_intervals_inclusive.append(interval[0])
            y_intervals_inclusive.append(interval[1] + 1)
        
        # All y vertices
        y_intervals_inclusive.sort()
        
        # Store the sizes of each successive interval. They will be overlapping.
        y_boundaries = [y_intervals_inclusive[i+1]-y_intervals_inclusive[i] for i in range(len(y_intervals_inclusive)-1)]
        
        return y_boundaries

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
    # print(grid)

    # Part 1
    invalid_locations = 0
    for x in range(grid.min_x, grid.max_x+1):
        candidate = Point(x, TARGET_ROW)
        if not grid.valid_for_beacon(candidate) and candidate not in grid.beacons:
            invalid_locations += 1    
    print(f"JP row {TARGET_ROW}: {invalid_locations}")
    

    for y in range(grid.min_y, grid.max_y+1):
        invalid_locations = 0
        for x in range(grid.min_x, grid.max_x+1):
            candidate = Point(x, y)
            if not grid.valid_for_beacon(candidate) and candidate not in grid.beacons:
                invalid_locations += 1    
        print(f"JP row {y}: {invalid_locations}")    
    
    compressed_ints = grid.compress_coords(TARGET_ROW)
    total_coverage = sum(compressed_ints)    
    beacons_to_exclude = sum(1 for beacon in grid.beacons if beacon.y == TARGET_ROW)
    print(f"Part 1 - row {TARGET_ROW}: {total_coverage - beacons_to_exclude}")
    
    for y in range(grid.min_y, grid.max_y+1):
        compressed_ints = grid.compress_coords(y)
        total_coverage = sum(compressed_ints)    
        beacons_to_exclude = sum(1 for beacon in grid.beacons if beacon.y == y)
        print(f"Part 1 - row {y}: {total_coverage - beacons_to_exclude}")    
    
    # # Part 2: we need to find the only non-coverage point in the given area
    for row in range(DISTRESS_Y_BOUNDS[0], DISTRESS_Y_BOUNDS[1] + 1):
        # all_row_points = set(x for x in range(DISTRESS_X_BOUNDS[0], DISTRESS_X_BOUNDS[1]))
        close_sensors = get_close_sensors_for_row(sensor_coverage, row)
        row_coverage_intervals = get_row_coverage_intervals(close_sensors, row)
        compressed_ints = compress_coords(row_coverage_intervals)
        total_coverage = sum(compressed_ints)
    #     print(f"Row: {row} - {sum(compressed_ints)}")
    #     # diff = all_row_points - row_coverage_points
    #     # if len(diff) > 0:
    #     #     x = diff.pop()
    #     #     print(f"{x, row}")
    #     #     print(f"{x*TUNING_FREQ_MULTIPLIER + row}")
    #     #     break


    
def get_row_coverage_points(row_coverage_intervals):
    row_coverage_points = set()
    for interval in row_coverage_intervals:
        points = set(range(interval[0], interval[1]+1))
        row_coverage_points.update(points)
    return row_coverage_points

def get_close_sensors_for_row(sensor_coverage, row: int):
    return {s:r for s, r in sensor_coverage.items() if abs(s.y - row) <= r}

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
