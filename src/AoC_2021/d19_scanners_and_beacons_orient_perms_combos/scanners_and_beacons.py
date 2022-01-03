"""
Author: Darren
Date: 19/12/2021

Solving https://adventofcode.com/2021/day/19

This solution takes about a minute to run for the real data.

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
    Create a set of all located beacon vectors, relative to scanner 0.
    Create a dict of located scanners (scanner #, vector) and a set of unlocated scanners.
    Assume scanner 0 at Point 0,0,0.
    Prepopulate all vectors for each scanner, given all possible scanner orientations.
    For at least two scanners, we should have vectors that when added, 
    will match for n>=12 overlapping beacons.  
    Use these addition vectors to determine location of the the new beacons, relative to scanner 0.
    Union in these new locations to Scanner 0, and mark off the set as located.
    We need a predictable arrangement of orientations for each vector.
    So precreate a fixed set of orientations, and we can then apply a given orientation to any vector.

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

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR,s "input/sample_input.txt")

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class Vector(NamedTuple):
    """ Tuple that represents vector and knows how to add and subtract other vectors """
    x: int
    y: int
    z: int
    
    def diff(self, other: Vector) -> Vector:
        """ Return the difference  """
        return Vector(self.x - other.x,
                      self.y - other.y,
                      self.z - other.z,)
    
    def add(self, other: Vector) -> Vector:
        """ Return the sum of vectors """
        return Vector(self.x + other.x, 
                      self.y + other.y,
                      self.z + other.z)
        
    def manhattan_distance_from(self, other: Vector) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
    
    def __str__(self):
        return f"({self.x},{self.y},{self.z})"
        
MIN_OVERLAPPING_BEACONS = 12

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()
    
    beacons_by_scanner = get_beacons_and_scanners(data)  # {int: set(Vector)}
    total_scanners = len(beacons_by_scanner)
    all_beacons = set(beacons_by_scanner[0]) # initialise with all beacons for scanner 0
    scanner_locations: dict[int, Vector] = {}   # scanners we have locations for
    scanners_not_located = set(int(scanner) for scanner in beacons_by_scanner)
        
    scanner_locations[0] = Vector(0, 0, 0)  # store our initial scanner locations
    scanners_not_located.remove(0)

    # Prepopulate all orientations per vector, per scanner
    # First, get the 48 possible (x,y,z) orientations, in predictable order
    orientations = get_orientations()
    
    # now apply the orientations to each set of beacons,
    # to end up with dict of {scanner:{orientation_id:[vec1, vec2...]}}
    orientations_by_scanner = defaultdict(dict)
    for scanner in range(total_scanners):
        for orientation_index, orientation in enumerate(orientations):
            orientations_by_scanner[scanner][orientation_index] = [apply_orientation(orientation, vec) 
                                                   for vec in beacons_by_scanner[scanner]]

    while scanners_not_located:
        scanner_location_found = None
        
        scanner = None
        for scanner in scanners_not_located:
            if scanner_location_found:
                break   # restart the loop, with one fewer unlocated scanner

            # We now iterate through all the possible adjustments, one at a time
            for adjustment_ind in range(len(orientations)):
                assert len(orientations) == 48, "Orientations borked"
                
                # retrieve all beacon vectors for this unknown scanner, applying current adjustment
                adjusted_vecs: list[Vector] = orientations_by_scanner[scanner][adjustment_ind]
                
                candidate_vectors = Counter()
                for adjusted_vec in adjusted_vecs:
                    for known_vec in all_beacons:
                        # Add the location of subtracting adjusted vector from known vector
                        # If we're oriented correctly and this beacon is common to more than one scanner
                        # then the candidate vector count will be incremented accordingly.
                        candidate_vectors[known_vec.diff(adjusted_vec)] += 1
            
                most_common = candidate_vectors.most_common(1)[0]   # (Vector, count)
                scanner_vector = most_common[0]
                if most_common[1] >= MIN_OVERLAPPING_BEACONS:
                    scanner_locations[scanner] = scanner_vector
                    for vec in adjusted_vecs:
                        # add in all adjusted vectors (i.e. such that they are relative to scanner 0)
                        # via the scanner we've just located.
                        all_beacons.add(vec.add(scanner_vector))
                        
                    scanner_location_found = scanner
                    logger.debug("Found scanner %d at %s; remaining=%d", 
                                 scanner, scanner_vector, len(scanners_not_located))
                    break
           
        scanners_not_located.remove(scanner_location_found)  # remove from list
      
    # Part 1
    logger.info("Part 1: Number of beacons = %d", len(all_beacons))
    
    # Part 2
    distances = []
    for combo in combinations(scanner_locations.values(), 2):
        distances.append(combo[0].manhattan_distance_from(combo[1]))
        
    logger.info("Part 2: Max Manhattan distance = %d", max(distances))

def get_orientations() -> list[tuple]:
    """ Returns a set of 48 orientation parameters that can be applied to any vector
    to deliver a consistent list of re-oriented vectors
    There are six permutations of (x,y,z), and for each, 
    there are 8 permutations of inversions of axes x,y,z. """
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
        
    return orientations # [((0, 1, 2), (0, 0, 0)), ...]
        
def apply_orientation(orientation: tuple, vector: Vector) -> Vector:
    """  Get a predictable orientation of a vector, given a permutation.

    Args:
        orientation (tuple[tuple,tuple]): Permutation (x,y,z)(a,b,c)
                                         where x,y,z is orientation, and a,b,c is axis inversion
        vector (Vector): vector

    Returns:
        Vector: new vector
    """
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
