"""
Author: Darren
Date: 19/12/2022

Solving https://adventofcode.com/2022/day/19

We need to make robots:
- geode-cracking
- obsidian-collecting
- clay-collecting
- ore-collecting; we have 1 already

Our input contains blueprints for robot types.

Robots can collect one of its resources per minute. 
Robot factory takes one minute to construct a robot; resources are consumed at the beginning of the minute.

Part 1:

Determine the quality level of each blueprint by multiplying that blueprint's ID number with 
the largest number of geodes that can be opened in 24 minutes using that blueprint.
What do you get if you add up the quality level of all of the blueprints in your list?

Soln:

- Use regex to read the input and assemble Blueprint objects. Each has id a a dict of {robot: {mineral: cost}}
- We can take 24 actions.
- Create a State object: qty of each robot, qty of each mineral, minutes remaining
- Our next state is: build nothing (accumulate resources), or build one of the robots we can build
- Then just BFS through all possible states. Return the one with the most geodes.

Part 2:

"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
OUTPUT_FILE = Path(SCRIPT_DIR, "output/output.png")

# robots
MINERALS = {
    "ORE": "ore",
    "CLAY": "clay",
    "OBSIDIAN": "obsidian",
    "GEODE": "geode"
}

@dataclass
class Blueprint():
    id: int
    costs: dict # { "ore": {"ore": 4}, "obsidian": {"ore": 3, clay: 14}, ...}    

@dataclass(frozen=True)
class State():
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int
    
    ore: int
    clay: int
    obsidian_robots: int
    geode: int
    
    time_remaining: int
    
    def next_state(self) -> State:
        # TODO implement all possible next states from here
        pass
    
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    blueprints = parse_data(data)
    print(blueprints)
    
def parse_data(data: list[str]) -> list[Blueprint]:
    """ Read the input and return a list of Blueprint """
    pattern = re.compile(r"Each (\w+) robot costs (\d+) (\w+)(?: and (\d+) (\w+))*.")
    blueprints = []
    for line in data:
        blueprint_id = int(line.split(":")[0].split()[-1])
        costs = {}
        for matches in pattern.findall(line):
            robot = matches[0]
            minerals = {}
            for i in range(2, len(matches) + 1, 2):
                if matches[i]: # if not empty
                    minerals[matches[i]] = int(matches[i-1])
            
            costs[robot] = minerals
    
        blueprints.append(Blueprint(blueprint_id, costs))
    
    return blueprints            
         
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
