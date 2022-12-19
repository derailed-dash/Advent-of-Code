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

@dataclass
class Blueprint():
    id: int
    costs: dict # { "ore": {"ore": 4}, "obsidian": {"ore": 3, clay: 14}, ...}    

@dataclass(frozen=True)
class State():
    blueprint: Blueprint
    time_remaining: int
    
    geode_robots: int = 0
    obsidian_robots: int = 0
    clay_robots: int = 0
    ore_robots: int = 1
    
    geode: int = 0
    obsidian: int = 0
    clay: int = 0
    ore: int = 0
    
    def next_state(self) -> State:
        """ Generator that returns next state. There are only five next states:
        1: Build nothing (accumulate) 
        2-5: Build a robot, if you can """
        time_remaining = self.time_remaining-1
        
        # each robot collects one of its resources per minute
        geode = self.geode + self.geode_robots
        obsidian = self.obsidian + self.obsidian_robots
        clay = self.clay + self.clay_robots
        ore = self.ore + self.ore_robots
        
        # do nothing        
        yield State(self.blueprint, time_remaining, 
                    self.geode_robots, self.obsidian_robots, self.clay_robots, self.ore_robots,
                    geode, obsidian, clay, ore)
        
        # build a geode robot
        if (self.obsidian >= self.blueprint.costs["geode"]["obsidian"] 
                and  self.ore >= self.blueprint.costs["geode"]["ore"]):
            yield State(self.blueprint, time_remaining, 
                        self.geode_robots+1, self.obsidian_robots, self.clay_robots, self.ore_robots,
                        geode, 
                        obsidian - self.blueprint.costs["geode"]["obsidian"],
                        clay,
                        ore - self.blueprint.costs["geode"]["ore"])
        
        # build obsidian robot
        if (self.ore >= self.blueprint.costs["obsidian"]["ore"] 
                and  self.clay >= self.blueprint.costs["obsidian"]["clay"]):
            yield State(self.blueprint, time_remaining, 
                        self.geode_robots, self.obsidian_robots+1, self.clay_robots, self.ore_robots,
                        geode, 
                        obsidian,
                        clay - self.blueprint.costs["obsidian"]["clay"],
                        ore - self.blueprint.costs["obsidian"]["ore"])
    
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    blueprints = parse_data(data)
    
    for blueprint in blueprints:
        state = State(blueprint, time_remaining=24)
        best = bfs(state)
        print(state)
        print(f"Best={best}\n")
    
def bfs(state: State) -> int:
    return 0
    
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
