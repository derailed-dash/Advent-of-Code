"""
Author: Darren
Date: 16/12/2022

Solving https://adventofcode.com/2022/day/16

Valves with flow rates, and tunnels between valves. Valves have flow rate in "pressure per minute".
All valves start closed. Start at valve AA.
It takes one minute to open a valve, and one minute to travel to an adjacent tunnel.
We have 30 minutes. 
For every minute that passes, we accumulate the pressure released from all open valves in that minute.

Part 1:

Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?

Soln:

- We have an unweighted, undirected graph.  Each node has a value.
- We need to find the optimum journey path that opens the most high flow valves earlier.
  I think we need an Dijkstra's Algorithm - i.e. favouring lower cost (highest score) paths!

Part 2:

"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import re
import time
import heapq

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

@dataclass(order=True,unsafe_hash=True) # state is mutable, but we hash only on other fields
class Valve():
    id: str    # E.g. "AA"
    rate: int  # E.g. 13
    leads_to: set[str] = field(compare=False, hash=None, repr=False)  # E.g. {"DD", "II", "BB"}
    open: bool = field(compare=False, hash=None, default=False)
    
    def set_open(self):
        self.open = True
    
class VolcanoState():
    def __init__(self, valves: dict[str, Valve], current_valve_id: str="AA", t=0, released=0, path=None) -> None:
        self.valves = valves
        self.time = t
        self.current_valve_id = current_valve_id
        self.flow_rate = self._calculate_flow_rate()
        self.total_released = released
        self.path = path if path is not None else [current_valve_id]

    def _calculate_flow_rate(self):
        """ Add up the flow rate of all open valves """
        return sum(valve.rate for valve in self.valves.values() if valve.open)
    
    def next_state(self):
        """ Generator for next possible states """
        current_valve = self.valves[self.current_valve_id]
        
        released = self.total_released + self.flow_rate
        if not current_valve.open: # We've just arrived here so we need to open the valve
            current_valve.set_open()
            yield VolcanoState(valves=self.valves, 
                               current_valve_id=current_valve.id, 
                               t=self.time+1, 
                               released=released,
                               path=self.path)            
        
        else: # we need to move to one of the adjacent tunnels
            for next_id in current_valve.leads_to:
                yield VolcanoState(valves=self.valves, 
                               current_valve_id=next_id, 
                               t=self.time+1, 
                               released=released,
                               path=self.path + [self.current_valve_id])
    
    def priority(self) -> int:
        """ Priority is given by highest total released. """
        return self.total_released
    
    def __lt__(self, other: VolcanoState):
        """ Heapq pops by lowest priority, so we want to reverse the output """
        if self.time != other.time:  # primary comparison
            return self.time < other.time
        else:  # secondary comparison
            return -self.priority() < -other.priority()

    def __eq__(self, o) -> bool:
        """ Equality is based on current position """
        if isinstance(o, VolcanoState):
            return self.time == o.time and self.flow_rate == o.flow_rate and self.current_valve_id == o.current_valve_id
        else:
            return NotImplemented
    
    def __hash__(self) -> int:
        """ Hash is based on tuple time, flow rate and current valve """
        return hash((self.time, self.flow_rate, self.current_valve_id))
    
    def __repr__(self) -> str:
        return (f"VolcanoState:(t={self.time}, " +
                f"current_valve={self.current_valve_id}, flow_rate={self.flow_rate}, released={self.total_released}, " +
                f"path={self.path}")
      
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    valves = parse_input(data)
    print("\n".join(str(valve) for valve in valves.values()))
    state = VolcanoState(valves)
    print(state)
    
    final_state = dijkstra(state)
    print(final_state)

def dijkstra(state: VolcanoState) -> VolcanoState:
    """ We want to search the graph using the highest pressure released as the heuristic. 
    Our initial priority comparison has to be distance, which is given by time.
    Our next priority comparison has to be total released. """
    
    current_state = state
    frontier: list[VolcanoState] = [current_state]  
    explored = set()
    explored.add(current_state)
    
    while frontier:
        current_state = heapq.heappop(frontier)
        if current_state.time == 30:
            break
        
        for next_state in current_state.next_state():
            if next_state not in explored:
                heapq.heappush(frontier, next_state)
                explored.add(next_state)

    return current_state

def show_path(came_from: dict, start: str, end: str) -> list[str]:
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
   
    path.reverse()
    return path 

def parse_input(data) -> dict[str, Valve]:
    pattern = re.compile(r"Valve ([A-Z]{2}) has flow rate=(\d)+;.+[valve]s? (.+)")
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
