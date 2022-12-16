"""
Author: Darren
Date: 16/12/2022

Solving https://adventofcode.com/2022/day/16

Valves with flow rates, and tunnels between valves. Valves have flow rate in "pressure per minute".
All valves start closed. Start at valve "AA".
It takes one minute to open a valve, and one minute to travel to an adjacent tunnel.
We have 30 minutes. For every minute that passes, 
we accumulate the pressure released from all open valves in that minute.

Part 1:

Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?

Soln:

- We have an unweighted, undirected graph.  Each node has a value.
- We need to find the optimum journey path that opens the most high flow valves earlier.
- This is memoization problem, which we can do using recursion and caching with lru_cache.

Takes a minute or so to run.

Part 2:

With you and an elephant working together for 26 minutes, 
what is the most pressure you could release?

Run Part 1 twice:
- Once to represent your moves;
- And again with the same valve opened state to simulate the elephant.
  Because only one of you needs to open any given valve.
"""
from dataclasses import dataclass
from pathlib import Path
import re
import functools
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

# sys.setrecursionlimit(10000)

@dataclass(frozen=True, order=True) # state is mutable, but we hash only on other fields
class Valve():
    """ Valve has an ID, a flow rate, and valves it is connected to. """
    id: str    # E.g. "AA"
    rate: int  # E.g. 13
    leads_to: set[str]  # E.g. {"DD", "II", "BB"}
        
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    valves = parse_input(data)
    print("\n".join(str(valve) for valve in valves.values()))

    @functools.cache
    def calc_max_relief(opened, mins_remaining, curr_valve_id, elephant=False):
        """ We need to embed this function to make our valves dict available. 
        We can't pass valves to the method, because it the dict is not hashable and can't be cached. """
        
        # Base case
        if mins_remaining <= 0:
            if elephant: # Perform again, but for the elephant
                return calc_max_relief(opened, 26, "AA")
            else:
                return 0

        most_relief = 0
        current_valve = valves[curr_valve_id]
        for neighbour in current_valve.leads_to:
            # Recurse for each neighbouring position
            most_relief = max(most_relief, calc_max_relief(opened, mins_remaining - 1, neighbour, elephant))

        # We only want to open valves that are closed, and where flow rate is > 0
        if curr_valve_id not in opened and current_valve.rate > 0 and mins_remaining > 0:
            opened = set(opened)
            opened.add(curr_valve_id)
            mins_remaining -= 1
            total_released = mins_remaining * current_valve.rate

            for neighbour in current_valve.leads_to:
                # Try each neighbour and recurse in. Save the best one.
                most_relief = max(most_relief, 
                           total_released + calc_max_relief(frozenset(opened), mins_remaining - 1, neighbour, elephant))

        return most_relief

    print(f"Part 1: {calc_max_relief(frozenset(), 30, 'AA')}")
    print(f"Part 2: {calc_max_relief(frozenset(), 26, 'AA', True)}")

def parse_input(data) -> dict[str, Valve]:
    pattern = re.compile(r"Valve ([A-Z]{2}) has flow rate=(\d+);.+[valve]s? (.+)")
    valves = {}
    for line in data:
        valve, rate, leads_to = pattern.findall(line)[0]
        valves[valve] = Valve(valve, int(rate), {x.strip() for x in leads_to.split(",")})
    
    return valves

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
