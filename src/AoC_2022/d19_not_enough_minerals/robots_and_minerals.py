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
- As above, but with more minutes.
"""
from dataclasses import dataclass
from pathlib import Path
from collections import deque
import re
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

@dataclass
class Blueprint():
    id: int
    costs: dict # { "ore": {"ore": 4}, "obsidian": {"ore": 3, clay: 14}, ...}
    
    def get_max_ore_cost(self):
        return max([self.costs["ore"]["ore"], 
                    self.costs["clay"]["ore"], 
                    self.costs["obsidian"]["ore"], 
                    self.costs["geode"]["ore"]])
 
@dataclass(frozen=True)
class State():
    t_remaining: int
    
    ore: int = 0   
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    ore_r: int = 1
    clay_r: int = 0
    obsidian_r: int = 0
    geode_r: int = 0
    
def bfs(blueprint: Blueprint, state: State):
    best = 0
    frontier = deque([state])
    explored = set()
    
    while frontier:
        state = frontier.popleft()

        best = max(best, state.geode)
        if state.t_remaining == 0:
            continue

        max_ore_cost = blueprint.get_max_ore_cost()
        
        ore_r = min(state.ore_r, max_ore_cost)
        clay_r = min(state.clay_r, blueprint.costs["obsidian"]["clay"])
        obs_r = min(state.obsidian_r, blueprint.costs["geode"]["obsidian"])
            
        ore = min(state.ore, state.t_remaining * max_ore_cost - ore_r*(state.t_remaining-1))
        clay = min(state.clay, state.t_remaining * blueprint.costs["obsidian"]["clay"] - clay_r*(state.t_remaining-1))
        obs = min(state.obsidian, state.t_remaining * blueprint.costs["geode"]["obsidian"] - obs_r*(state.t_remaining-1))

        state = State(state.t_remaining, 
                 ore, clay, obs, state.geode,
                 ore_r, clay_r, obs_r, state.geode_r)

        if state in explored:
            continue
        explored.add(state)
        
        # Don't make any robots; just accumulate
        frontier.append(State(state.t_remaining-1, 
                ore+ore_r, clay+clay_r, obs+obs_r, state.geode+state.geode_r,
                ore_r, clay_r, obs_r, state.geode_r))
        
        if ore >= blueprint.costs["ore"]["ore"]: # build ore robot
            frontier.append(State(state.t_remaining-1,
                    ore-blueprint.costs["ore"]["ore"]+ore_r, clay+clay_r, obs+obs_r, state.geode+state.geode_r, 
                    ore_r+1, clay_r, obs_r, state.geode_r))
        if ore >= blueprint.costs["clay"]["ore"]: # build clay robot
            frontier.append(State(state.t_remaining-1, 
                    ore-blueprint.costs["clay"]["ore"]+ore_r, clay+clay_r, obs+obs_r, state.geode+state.geode_r, 
                    ore_r, clay_r+1, obs_r, state.geode_r))
        if ore >= blueprint.costs["obsidian"]["ore"] and clay>=blueprint.costs["obsidian"]["clay"]: # build obsidian robot
            frontier.append(State(state.t_remaining-1,
                    ore-blueprint.costs["obsidian"]["ore"]+ore_r, 
                    clay-blueprint.costs["obsidian"]["clay"]+clay_r, 
                    obs+obs_r, state.geode+state.geode_r, 
                    ore_r, clay_r, obs_r+1, state.geode_r))
        if ore >= blueprint.costs["geode"]["ore"] and obs>=blueprint.costs["geode"]["obsidian"]: # build geode robot
            frontier.append(State(state.t_remaining-1,
                    ore-blueprint.costs["geode"]["ore"]+ore_r, clay+clay_r, 
                    obs-blueprint.costs["geode"]["obsidian"]+obs_r, state.geode+state.geode_r, 
                    ore_r, clay_r, obs_r, state.geode_r+1))
            
    return best

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

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    blueprints = parse_data(data)
    quality_level = 0
    geode_product = 1
    for blueprint in blueprints:
        print(blueprint)
        geodes = bfs(blueprint, State(24))
        quality_level += geodes * blueprint.id
        
        if blueprint.id <= 3:  # First three blueprints; they start at 1
            geodes = bfs(blueprint, State(32)) # These take a while!
            geode_product *= geodes
    
    print(f"Part 1={quality_level}")
    print(f"Part 2={geode_product}")                
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
