""" 
Author: Darren
Date: 13/03/2021

Solving https://adventofcode.com/2015/day/19

Start with input molecule and then replace components, one per step, 
until it has the right molecule.

E.g. input of:
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO

Part 1:
    Calibration: how many molecules can be generated in one step?

    Read input and build defaultdict of source groups to target groups (1 to many).
    At the same time, let's build a dict of target groups to src groups (1 to 1).

    For each src group:
        Match each position in the medicine molecule.
        For each match, and for each target group, 
            concatenate prefix + target group + suffix.

Part 2:
    Number of iterations to go from e to target molecule.

    E.g. HOHOHO -> (3) HHH -> (1) OH -> (1) H -> (1) e

    Start with the target medicine molecule.
    Go through all target groups, and substitute with src molecule.
    Ingore e substitutions for now.
    Count how many substitions are possible with this target, and store in a list.
    Update the current molecule.  Repeat until the molecule is no longer updated.

    Once no more updates are possible, perform substition to get back to e.
"""
import os
import time
import re
from collections import defaultdict
from typing import Tuple

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    src_groups, target_groups, medicine_molecule = process_input(data)

    new_molecules = substitute_groups(src_groups, medicine_molecule)

    unique_new_molecules = set(new_molecules)
    # print(unique_new_molecules)
    print(f"Part 1: Identified {len(unique_new_molecules)} unique molecules.")

    synthesis_stack = retrosynthesis(target_groups, medicine_molecule)
    synthesis_steps = sum(step[0] for step in synthesis_stack)
    print(f"Part 2: Synthesis stack requires {synthesis_steps} steps.")
    # print(synthesis_stack)


def retrosynthesis(target_groups: dict, target_molecule: str) -> list:
    synthesis_stack = []
    current_molecule = target_molecule

    # start by doing all the substitions, without e
    # repeat until the molecule is not modified
    molecule_modified = True
    while molecule_modified:
        molecule_modified = False

        for tgt_grp, src_grp in target_groups.items():
            if src_grp == 'e':
                continue

            # count how many matches of target first
            substitutions = current_molecule.count(tgt_grp)

            # then replace them all
            if substitutions > 0:
                current_molecule = current_molecule.replace(tgt_grp, src_grp)
                molecule_modified = True
                synthesis_stack.append([substitutions, current_molecule])

    # now replace target with e
    for tgt_grp, src_grp in target_groups.items():
        if src_grp != 'e':
            continue

        # count how many matches of target first
        substitutions = current_molecule.count(tgt_grp)

        # then replace them all
        if substitutions > 0:
            current_molecule = current_molecule.replace(tgt_grp, src_grp)
            synthesis_stack.append([substitutions, current_molecule])

    return synthesis_stack


def substitute_groups(groups: dict, molecule: str) -> list:
    new_molecules = []

    # go through all the groups we have substitutions for
    for group, targets in groups.items():
        # get all matching positions for this group
        group_matches = re.finditer(group, molecule)

        # move left to right, matching group one at a time
        for group_match in group_matches:
            start, end = group_match.span()
            prefix = molecule[:start]
            suffix = molecule[end:]

            # replace the current group occurrence with each target
            for target in targets:
                new_molecules.append(prefix + target + suffix)
    
    return new_molecules


def process_input(data: list) -> Tuple[dict, dict, str]:
    subst_match = re.compile(r"^(\w+) => (\w+)")
    
    # each src group can make many target groups
    src_groups = defaultdict(list)

    # each target group can be made from only one src group
    target_groups = {}

    for line in data:
        if "=>" in line:
            group, target_group = subst_match.match(line).groups()
            src_groups[group] += [target_group]
            target_groups[target_group] = group

    return src_groups, target_groups, data[-1]


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
