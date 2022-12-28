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
from enum import Enum
from pathlib import Path
from collections import deque
import re
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

class MineralType(Enum):
    """ Enumerate mineral / robot types """
    ORE = "ore"
    CLAY = "clay"
    OBSIDIAN = "obsidian"
    GEODE = "geode"

@dataclass(frozen=True)
class Blueprint():
    """ Store blueprint ID, with a dict for each robot type, that in turn contains a nested dict
    of all mineral costs for that robot. """
    id: int
    costs: dict # { "ore": {"ore": 4}, "obsidian": {"ore": 3, clay: 14}, ...}
    
    def get_max_cost(self, mineral: MineralType):
        """ Return the maximum cost of a given mineral type for all robots in this blueprint. """
        
        # If this robot does not contain a given mineral in the blueprint, return 0 for this mineral
        return max([self.costs[MineralType.ORE.value].get(mineral.value, 0), 
                    self.costs[MineralType.CLAY.value].get(mineral.value, 0), 
                    self.costs[MineralType.OBSIDIAN.value].get(mineral.value, 0), 
                    self.costs[MineralType.GEODE.value].get(mineral.value, 0)])
 
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

    max_ore_cost = blueprint.get_max_cost(MineralType.ORE)
    max_clay_cost = blueprint.get_max_cost(MineralType.CLAY)
    max_obsidian_cost = blueprint.get_max_cost(MineralType.OBSIDIAN)
    
    while frontier:
        state = frontier.popleft() # popleft for BFS; pop for DFS

        best = max(best, state.geode)
        if state.t_remaining == 0:
            continue
        
        # Optimise state space by throwing away robots we can't use
        # E.g. if the highest per minute ore cost is 4, then there's no point having more than 4 ore robots.
        ore_r = min(state.ore_r, max_ore_cost)
        clay_r = min(state.clay_r, max_clay_cost)
        obs_r = min(state.obsidian_r, max_obsidian_cost)
        
        # optimise state space by throwing away resources we can't possibly spend in the time we have left.
        # E.g. if t=10 and max ore cost is 4, then we can only spend a max of 40 ore.
        # So if we have more than 40, throw it away.
        # Of course, we can't throw away any geodes!
        ore = min(state.ore, state.t_remaining * max_ore_cost - ore_r*(state.t_remaining-1))
        clay = min(state.clay, state.t_remaining * max_clay_cost - clay_r*(state.t_remaining-1))
        obs = min(state.obsidian, state.t_remaining * max_obsidian_cost - obs_r*(state.t_remaining-1))

        # If our optimisations are applicable, amend our state to reflect the optimised state.
        # Thus, fewer overall states to explore.
        state = State(state.t_remaining, 
                 ore, clay, obs, state.geode,
                 ore_r, clay_r, obs_r, state.geode_r)

        if state in explored:
            continue
        explored.add(state)
        
        # Now add each possible next state to the frontier...
        # 1st option: Don't make any robots; just accumulate.
        # New mineral levels are simply old levels + number of each robot type
        frontier.append(State(state.t_remaining-1, 
                ore+ore_r, 
                clay+clay_r, 
                obs+obs_r, 
                state.geode+state.geode_r,
                ore_r, clay_r, obs_r, state.geode_r))
        
        # Remaining options: build one of each bot, if we can
        if ore >= blueprint.costs[MineralType.ORE.value].get(MineralType.ORE.value, 0):
            # build ore robot 
            frontier.append(State(state.t_remaining-1,
                    ore-blueprint.costs[MineralType.ORE.value][MineralType.ORE.value]+ore_r, 
                    clay+clay_r, 
                    obs+obs_r, 
                    state.geode+state.geode_r, 
                    ore_r+1, clay_r, obs_r, state.geode_r))
        if ore >= blueprint.costs[MineralType.CLAY.value][MineralType.ORE.value]: 
            # build clay robot
            frontier.append(State(state.t_remaining-1, 
                    ore-blueprint.costs[MineralType.CLAY.value][MineralType.ORE.value]+ore_r, 
                    clay+clay_r, 
                    obs+obs_r, 
                    state.geode+state.geode_r, 
                    ore_r, clay_r+1, obs_r, state.geode_r))
        if (ore >= blueprint.costs[MineralType.OBSIDIAN.value][MineralType.ORE.value] 
                and clay>=blueprint.costs[MineralType.OBSIDIAN.value][MineralType.CLAY.value]): 
            # build obsidian robot
            frontier.append(State(state.t_remaining-1,
                    ore-blueprint.costs[MineralType.OBSIDIAN.value][MineralType.ORE.value]+ore_r, 
                    clay-blueprint.costs[MineralType.OBSIDIAN.value][MineralType.CLAY.value]+clay_r, 
                    obs+obs_r, 
                    state.geode+state.geode_r, 
                    ore_r, clay_r, obs_r+1, state.geode_r))
        if (ore >= blueprint.costs[MineralType.GEODE.value][MineralType.ORE.value] 
                and obs>=blueprint.costs[MineralType.GEODE.value][MineralType.OBSIDIAN.value]): 
             # build geode robot
            frontier.append(State(state.t_remaining-1,
                    ore-blueprint.costs[MineralType.GEODE.value][MineralType.ORE.value]+ore_r, 
                    clay+clay_r, 
                    obs-blueprint.costs[MineralType.GEODE.value][MineralType.OBSIDIAN.value]+obs_r, 
                    state.geode+state.geode_r, 
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
            # costs = costs.set(robot, minerals)
        # costs = frozendict({k:v for k,v in costs.items()})
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
