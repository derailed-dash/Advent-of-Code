""" 
Author: Darren
Date: 26/02/2021

Solving https://adventofcode.com/2015/day/16

500 Sues. Each with different known attributes, and potentially other forgetten attributes.
Examine list of k:v pairs determined from item received from Sue,
using the My First Crime Scene Analysis Machine (MFCSAM).

The MFCSAM produces properties, which we store as a dict.
We also have a list of k:v attributes that we can remember from 500 Sues. 
But where we don't know a value, the key is absent.

Solution:

Part 1:
    Iterate through our k:V from the MFCSAM. 
    For each Sue:
        If the k is not present, this Sue is a candidate.
        If k is present and the value matches, this Sue is a candidate.

Part 2: 
    Cats and trees readings indicates that there are greater than that many
    Pomeranians and goldfish readings indicate that there are fewer than that many
"""
from dataclasses import dataclass
import os
import time

SCRIPT_DIR = os.path.dirname(__file__)
INPUT_FILE = "input/input.txt"

known_attribs = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}

@dataclass
class Sue:
    """ A Sue has a unique number and a set of properties that look like...
    {'pomeranians': 3, 'perfumes': 1, 'vizslas': 0}
    """
    num: int
    properties: dict

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    sue_list = process_input(data)

    # Part 1
    sue_candidates = sue_list.copy()

    # we need to find any Sue where k:v is an exact match
    # but also consider any Sue where the k is not present as we don't know the v
    for known_attrib, known_attrib_value in known_attribs.items():
        sues_matching_attrib = [sue for sue in sue_candidates if known_attrib in sue.properties
                                and known_attrib_value == sue.properties[known_attrib]]
        sues_missing_attrib = [sue for sue in sue_candidates if known_attrib not in sue.properties]

        sue_candidates = sues_matching_attrib + sues_missing_attrib

    print(f"Part 1: Aunt Sue candidates matching MFCSAM attributes: {sue_candidates[0].num}")

    # Part 2
    sue_candidates = sue_list.copy()
    for known_attrib, known_attrib_value in known_attribs.items():
        sues_missing_attrib = [sue for sue in sue_candidates if known_attrib not in sue.properties]
        sues_matching_attrib = []

        if known_attrib in ['cats', 'trees']:
            sues_matching_attrib = [sue for sue in sue_candidates if known_attrib in sue.properties
                                and known_attrib_value < sue.properties[known_attrib]]
        elif known_attrib in ['pomeranians', 'goldfish']:
            sues_matching_attrib = [sue for sue in sue_candidates if known_attrib in sue.properties
                                and known_attrib_value > sue.properties[known_attrib]]
        else:
            sues_matching_attrib = [sue for sue in sue_candidates if known_attrib in sue.properties
                                and known_attrib_value == sue.properties[known_attrib]]

        sue_candidates = sues_matching_attrib + sues_missing_attrib

    print(f"Part 2: Aunt Sue candidates matching MFCSAM attributes: {sue_candidates[0].num}")

def process_input(data) -> list[Sue]:
    # Input looks like:
    # Sue 1: cars: 9, akitas: 3, goldfish: 0
    # Return list of Sue objects.
    sue_list = []

    for line in data:
        sue_num, attribs = line[4:].split(":", 1)
        properties = [x.strip().split(":") for x in attribs.split(",")]
        props_dict = {prop[0]: int(prop[1]) for prop in properties}
        sue_list.append(Sue(int(sue_num), props_dict))

    return sue_list

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
