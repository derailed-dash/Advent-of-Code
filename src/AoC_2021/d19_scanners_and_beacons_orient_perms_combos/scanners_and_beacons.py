"""
Author: Darren
Date: 19/12/2021

Solving https://adventofcode.com/2021/day/19

This solution takes about 40s to run for the real data.

Input data is of multiple scanners, with each reporting the locations of many beacons.
E.g.    --- scanner 0 ---
        404,-588,-901
        528,-643,409
        -838,591,734
        ...    
Scanners can detect any beacons within 1000 units.
Scanners report back these beacon positions, relative to a given scanner.
Scanners don't know their own positions; nor can they detect other scanners.
We don't know scanner orientations, but orientations are always orthogonal to other scanners.
We're guaranteed at least 12 overlapping beacons per scanner.

Part 1:
    Assemble the map of beacon locations.  How many beacons are there?
    
    Read in all scanners and their beacon locations, as dict[scanner_num, set(beacon vectors)]
    Create a set of all located beacon vectors, relative to scanner 0. We'll add to it as we go.
    Create a dict of located scanners (scanner #, vector) and a set of unlocated scanners.
    Assume scanner 0 at Point 0,0,0.
    
    Prepopulate all possible beacon vectors for each scanner, given all possible scanner orientations.
    - There are 48 different orientations, 40 scanners and ~30 beacons per scanner.
      (We're told there are 24 orientations, but it's easy to come up with 48; hard to determine the 24!)
    - Thus ~60K different vectors to compute and store.  Not so many.
    - Only takes a few ms to run this.
    - We need the orientations to always be given in a predictable order.
    
    For at least two scanners (0 known, x unknown) we should have vectors that, when subtracted,  
    will match for n>=12 overlapping beacons.  I.e. scanner 0 -> beacon <- scanner x.
    (This will only work for one scanner orientation, so we need to try them all.)
    The matching vector will be the vector to scanner x, from scanner 0.
    We can then add the vectors of scanner 0 -> scanner x -> beacons, 
    to get all scanner x's beacons relative to scanner 0.
    Union in these new beacon vectors from Scanner 0, and mark off the scanner as located.
    The beacons known from 0 is now a much bigger set.  
    Repeat the process, with a new scanner x, comparing against the bigger set of scanner 0.

Part 2:
    Another trivial addendum that uses itertools.combinations.
    Manhattan distance added as a method on the Vector class.
"""
from __future__ import annotations
import logging
from pathlib import Path
import time
import re
from collections import Counter, defaultdict
from typing import NamedTuple
from itertools import combinations, permutations
import matplotlib.pyplot as plt

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

RENDER = False
OUTPUT_DIR = Path(SCRIPT_DIR, "output/")
OUTPUT_FILE = Path(OUTPUT_DIR, "trajectory.png")

MIN_OVERLAPPING_BEACONS = 12
class Vector(NamedTuple):
    """ Tuple that represents vector and knows how to add and subtract other vectors """
    x: int
    y: int
    z: int
    
    def __sub__(self, other):
        """ Subtract other vector from this vector, returning new vector """
        return Vector(self.x - other.x,
                      self.y - other.y,
                      self.z - other.z,)
        
    def __add__(self, other):
        """ Add other vector from this vector, returning new vector """
        return Vector(self.x + other.x, 
                      self.y + other.y,
                      self.z + other.z)
        
    def manhattan_distance_to(self, other: Vector) -> int:
        """ Manhattan distance between this Vector and another Vector """
        diff = self-other
        return sum(abs(coord) for coord in diff)
    
    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

def plot(scanner_locations: dict[int, Vector], beacon_locations: set[Vector], outputfile=None):
    _ = plt.figure(111)
    axes = plt.axes(projection="3d")
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.set_zlabel("z")

    axes.grid(True) # grid lines on
    
    x,y,z = zip(*scanner_locations.values())    # scanner locations
    axes.scatter3D(x, y, z, marker="o", color='r', s=40, label="Sensor")
    offset=50
    for x, y, z, scanner in zip(x, y, z, scanner_locations.keys()): # add scanner numbers
        axes.text3D(x+offset, y+offset, z+offset, s=scanner, color="red", fontweight="bold")
    
    x,y,z = zip(*beacon_locations)
    axes.scatter3D(x, y, z, marker=".", c='blue', label="Probe", s=10)
    
    x_line = [min(x), max(x)]
    y_line = [0, 0]
    z_line = [0, 0]
    plt.plot(x_line, y_line, z_line, color="black", linewidth=1)
    
    x_line = [0, 0]
    y_line = [min(y), max(y)]
    z_line = [0, 0]
    plt.plot(x_line, y_line, z_line, color="black", linewidth=1)
    
    x_line = [0, 0]
    y_line = [0, 0]
    z_line = [min(z), max(z)]
    plt.plot(x_line, y_line, z_line, color="black", linewidth=1)
    
    axes.legend()
    plt.title("Scanner and Beacon Locations", fontweight="bold")

    if outputfile:
        dir_path = Path(outputfile).parent
        if not Path.exists(dir_path):
            Path.mkdir(dir_path)
        plt.savefig(outputfile)
        logger.info("Plot saved to %s", outputfile)        
    else:
        plt.show()
    
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()
    
    beacons_by_scanner = get_beacons_and_scanners(data)  # {int: set(Vector)}
    
    total_scanners = len(beacons_by_scanner)
    all_located_beacons = set(beacons_by_scanner[0]) # initialise with all beacons for scanner 0
    scanner_locations: dict[int, Vector] = {}   # scanners we have locations for
    scanners_not_located = set(int(scanner) for scanner in beacons_by_scanner)  # Scanner numbers
        
    scanner_locations[0] = Vector(0, 0, 0)  # store our known scanner location
    scanners_not_located.remove(0)

    # Prepopulate all orientations that can be applied to any vector.
    # First, get the 48 possible (x,y,z) orientations, in predictable order
    orientations = get_orientations()   # ( ((0,1,2), (inv,inv,inv)), ... )
    
    # Now apply all the orientations to each set of beacons,
    # to end up with dict of {scanner:{orientation_id:[vec1, vec2...]}}
    orientations_by_scanner = defaultdict(dict) # {scanner 0: {orientation 0: [vec1, vec2, ...]}}
    for scanner in range(total_scanners):
        for orientation_index, orientation in enumerate(orientations):
            orientations_by_scanner[scanner][orientation_index] = [apply_orientation(orientation, vec) 
                                                   for vec in beacons_by_scanner[scanner]]

    while scanners_not_located:     # scanners we still need to locate
        scanner_location_found = None
        for scanner in scanners_not_located:
            if scanner_location_found:
                break   # restart the loop, with one fewer unlocated scanner
            
            # We now iterate through all the possible orientations, one at a time
            for adjustment_ind in range(len(orientations)):
                assert len(orientations) == 48, "Orientations borked"
                
                # retrieve all beacon vectors for this unknown scanner, applying current adjustment
                adjusted_vecs: list[Vector] = orientations_by_scanner[scanner][adjustment_ind]
                
                candidate_vectors = Counter()
                # Iterate through all beacon vectors, relative to the unlocated scanner
                for adjusted_vec in adjusted_vecs:  
                    for known_vec in all_located_beacons:
                        # Subtract adjusted vector from known vector, 
                        # in order to get a potential vector to the unknown scanner.
                        # We subtract because we want to get the vector TO the sensor, not FROM it.
                        # If we're oriented correctly and this beacon is common to more than one scanner
                        # then the candidate vector will be common to multiple beaacons.
                        candidate_vectors[known_vec - adjusted_vec] += 1
            
                candidate_scanner_vector, beacon_count = candidate_vectors.most_common(1)[0]
                if beacon_count >= MIN_OVERLAPPING_BEACONS: # we need at least this many overlapping beacons
                    scanner_locations[scanner] = candidate_scanner_vector
                    for vec in adjusted_vecs:
                        # add together adjusted vectors with vector of this scanner, relative to scanner 0.
                        # This gives us the new scanner's beacon vectors, relative to scanner 0.
                        all_located_beacons.add(candidate_scanner_vector + vec)
                        
                    scanner_location_found = scanner    # Exit the "for scanner in" loop
                    logger.debug("Found scanner %d at %s; remaining=%d", 
                                 scanner, candidate_scanner_vector, len(scanners_not_located))
                    break   # Don't need to try any more vector orientations
        
        assert scanner_location_found, "We must have found a scanner location"   
        scanners_not_located.remove(scanner_location_found)  # remove from list
      
    # Part 1
    logger.info("Part 1: Number of beacons = %d", len(all_located_beacons))
    
    # Part 2
    distances = []
    for combo in combinations(scanner_locations.values(), 2):
        distances.append(combo[0].manhattan_distance_to(combo[1]))
        
    logger.info("Part 2: Max Manhattan distance = %d", max(distances))

    if RENDER:
        plot(scanner_locations, all_located_beacons) # show the plot    
    else:
        plot(scanner_locations, all_located_beacons, OUTPUT_FILE) # save the plot

def get_orientations() -> tuple:
    """ Creates a set of 48 orientation parameters that can be applied to any vector
    to deliver a consistent list of re-oriented vectors.
    
    There are six permutations of (x,y,z), and for each, there are 8 permutations of inversions of axes x,y,z.

    Returns:
        tuple[tuple]: ( ((x,y,z permutation), (x,y,z axis inversion)), ...)
    """
    orientations = []
    # The perms are the [x, y, z] index positions, i.e.
    # [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
    for perm in list(permutations([0, 1, 2])):
        orientations.append((perm, (0,0,0))) # e.g. ((0, 1, 2), (0, 0, 0))
        orientations.append((perm, (1,0,0)))
        orientations.append((perm, (0,1,0)))
        orientations.append((perm, (0,0,1)))
        orientations.append((perm, (1,1,0)))
        orientations.append((perm, (0,1,1)))
        orientations.append((perm, (1,0,1)))
        orientations.append((perm, (1,1,1)))  # This one IS needed!    
    
    return tuple(orientations) # (((0, 1, 2), (0, 0, 0)), ...)
        
def apply_orientation(orientation: tuple, vector: Vector) -> Vector:
    """  Apply a reorientation of a vector, given an orientation.
    Orientation looks like ((x,y,z)(a,b,c)), where orientation[0] is x,y,z
    and orientation[1] is a,b,c, i.e. the axis inversion.
    Returns: a new vector """
    coord_list = [vector.x, vector.y, vector.z]
    x = coord_list[orientation[0][0]]
    y = coord_list[orientation[0][1]]
    z = coord_list[orientation[0][2]]
    
    x = x if orientation[1][0] == 0 else -x
    y = y if orientation[1][1] == 0 else -y
    z = z if orientation[1][2] == 0 else -z
    
    return Vector(x, y, z)

def get_beacons_and_scanners(data: str) -> dict[int, set[Vector]]:
    """ Return dict containing {scanner_num, set(Vector) """
    scanner_pattern = re.compile(r"--- scanner (\d+) ---")
    
    beacons_by_scanner = defaultdict(set)
    scanner_num = 0
    for line in [line.strip() for line in data.splitlines() if line != ""]:
        if "scanner" in line:
            if match := scanner_pattern.match(line):
                scanner_num = int(match.group(1))
        else:
            x, y, z = map(int, line.split(","))
            vec = Vector(x,y,z)
            beacons_by_scanner[scanner_num].add(vec)
    
    return beacons_by_scanner

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
