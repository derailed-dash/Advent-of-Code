"""
Author: Darren
Date: 23/12/2021

Solving https://adventofcode.com/2021/day/23

Need to rearrange amphipods from:
 
############# to #############
#...........#    #...........#
###A#D#B#C###    ###A#B#C#D###
  #B#C#D#A#        #A#B#C#D# 
  #########        #########  

Different movement costs for different types of amphipod.

This solution uses a Dijkstra BFS, where the cumulative energy cost is used as the priority for the priority queue.

Part 1:
    States are represented by (hall, rooms).
    Target state is where hall is empty and rooms only contain one char that matches their key.
    Our solve method:
    - Takes a starting state.
    - Looks for any pods in the hall that can move directly to destination.
      If so, return the cost and store the nex state.
    - Otherwise, look for any pods in rooms that can move to hall.
      Recursively determine the cost of going to hall, and subsequent states.
    - Note: this approach treats Room -> Hall -> Room as 2 steps, even if Room -> Room is possible.
    
Part 2:
    - Just add the required rows to the input data and re-run.
"""
from __future__ import annotations
import logging
import os
import time
import heapq
from typing import Iterable

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

class BurrowState():
    """ Store the state of a Burrow, i.e. the configuration of the hall and rooms. 
    Knows how to yield next possible states (e.g. for use in a BFS). """
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    EMPTY = '.'
    ROOM_KEYS = [A, B, C, D]
    POD_COSTS = {A: 1, B: 10, C: 100, D: 1000}
    ROOM_IDX = {A: 2, B: 4, C: 6, D: 8}

    def __init__(self, state: tuple[dict[str, list[str]], list[str]], cost:int=0) -> None:
        """ Creates a new BurrowState.

        Args:
            state (tuple[dict[str, list[str]], list[str]]): (rooms, hall)
            energy (int, optional): Energy required to get to this state. Defaults to 0.
        """
        self._state = state # (rooms, hall)
        self._last_cost = cost # energy required to get to this state from last state
    
    @property
    def last_cost(self):
        """ The energy cost taken to generate this state from the previous state.
        (This is not a cumulative energy.) """
        return self._last_cost
    
    def is_goal(self) -> bool:
        """ Returns False if any amphipods in any room are not of the right type """
        rooms, _ = self._state
        for room_type, pods in rooms.items():
            if any((amphipod != room_type) for amphipod in pods):
                return False
        return True

    def _can_move_from(self, room_key: str, room: list) -> bool:
        """ If this item is an amphipod and if we can move it """
        for item in room:
            if item != room_key and item != BurrowState.EMPTY:
                # If there's a pod at this location, and it doesn't belong in this room
                return True
        return False

    def _can_move_to(self, room_key: str, room: list) -> bool:
        """ Check if destination room is correct type and can accept a pod """
        for item in room:
            if item != room_key and item != BurrowState.EMPTY:
                # If there's already a pod in this room, and it's the wrong type 
                return False
        return True

    def _get_top_item_idx(self, room_contents: list):
        """ Return the row index of the top pod (i.e. top occupied position) in a room """
        for i, item in enumerate(room_contents):
            if item != BurrowState.EMPTY:
                return i
        return None

    def _get_room_dest_idx(self, room_contents: list):
        """ Return the position in the room we want to move to. """
        for i, char in reversed(list(enumerate(room_contents))):
            if char == BurrowState.EMPTY:
                return i    # return the "bottom" (highest index) that is empty
        return None

    def _is_between(self, posn: int, room_key: str, hall_idx: int) -> bool:
        """ If this posn is between the room and the hall index """
        return ((BurrowState.ROOM_IDX[room_key] < posn < hall_idx)
                or (hall_idx < posn < BurrowState.ROOM_IDX[room_key]))

    def _is_clear_path(self, room_key: str, hall_idx: int) -> bool:
        """ Is it clear between the room and the hall position? 

        Args:
            room_key (str): Which room
            hall_idx (int): Which hall horizontal position
            hall (list[str]): Contents of the hall
        """
        _, hall = self._state
        
        for posn, item in enumerate(hall):
            if self._is_between(posn, room_key, hall_idx) and item != BurrowState.EMPTY:
                return False
        return True

    def __repr__(self) -> str:
        """ Generate a str representation of this state """
        rooms, hall = self._state
        rooms_list = [room_items for room_type, room_items in rooms.items()]
        render = []
        render.append('')  # Blank line
        render.append("#" + "#"*len(hall) + "#") # top row
        render.append("#" + "".join(hall) + "#") # hall row
        for i in range(len(rooms_list[0])): # room rows
            if i == 0:
                prefix = suffix = "###" # top room row
            else:
                prefix = "  #"
                suffix = "#"
                
            render.append(prefix + "#".join(rooms[k][i] for k in rooms) + suffix)
        render.append("  " + "#"*(len(hall)-2)) # bottom row
        return "\n".join(render)

    def __hash__(self) -> int:
        rooms, hall = self._state
        rooms_tuple = tuple((k, tuple(v)) for k,v in rooms.items())
        hall_tuple = tuple(hall)
        return hash(tuple((rooms_tuple, hall_tuple)))
    
    def __eq__(self, __o: object) -> bool:
        """ Test for equivalence by comparing hall and rooms """
        if isinstance(__o, BurrowState):
            this_rooms, this_hall = self._state
            other_rooms, other_hall = __o._state
            
            return this_rooms == other_rooms and this_hall == other_hall
        else:
            return NotImplemented
        
    def __lt__(self, __o: object) -> bool:
        """ Performs comparision based on last energy cost. """
        if isinstance(__o, BurrowState):
            return self.last_cost < __o.last_cost
        else:
            return NotImplemented
    
    def next_state(self) -> Iterable[BurrowState]:
        """ Yields next possible states from here.
        If we can put a amphipod into its destination room, then only return that state. """  
        rooms, hall = self._state
    
        # Determine if we have any pods in the hall that can go directly to dest
        # If we have, then this is the best move
        for i, pod in enumerate(hall): # position and item (pod or empty) in hall
            # If a pod, and we can move it to the room
            if pod in rooms and self._can_move_to(pod, rooms[pod]):
                if self._is_clear_path(pod, i):
                    dest_idx = self._get_room_dest_idx(rooms[pod])
                    assert isinstance(dest_idx, int), "We've determined we can move to this room"
                    dist = dest_idx + 1 + abs(BurrowState.ROOM_IDX[pod]-i)
                    cost = BurrowState.POD_COSTS[pod] * dist
                    
                    # remove pod from hall
                    new_hall = list(hall) # create a copy
                    new_hall[i] = BurrowState.EMPTY
                    
                    # add pod to destination room
                    new_rooms = {k: [room_item for room_item in v] for k, v in rooms.items()}                
                    new_rooms[pod][dest_idx] = pod

                    yield BurrowState((new_rooms, new_hall), cost=cost)

        # If we're here, no pods in the hall to move to destination.
        # Evaluate which rooms we can move pods from
        for room_key, room_contents in rooms.items():
            if not self._can_move_from(room_key, room_contents):
                continue
            # If we're here, we can move out of this room
            
            pod_idx = self._get_top_item_idx(room_contents)
            if pod_idx is None:
                continue
            
            # If we're here, there's a pod to move from this room
            pod = room_contents[pod_idx]
            
            # Now find locations in the hall our pod can move to
            for hall_posn, item in enumerate(hall):
                if hall_posn in [2, 4, 6, 8]:
                    continue    # skip hall positions above rooms
                if item != BurrowState.EMPTY:
                    continue    # skip locations that are occupied
                
                # determine if we have a path to this destination
                if self._is_clear_path(room_key, hall_posn):
                    dist = pod_idx + 1 + abs(hall_posn - BurrowState.ROOM_IDX[room_key])
                    cost = BurrowState.POD_COSTS[pod] * dist  # cost of this move
                    
                    # make a copy of hall and rooms, and update them
                    new_hall = list(hall)
                    new_hall[hall_posn] = pod
                    
                    # This is much quicker than a deep copy
                    new_rooms = {k: [room_item for room_item in v] for k, v in rooms.items()}
                    new_rooms[room_key][pod_idx] = BurrowState.EMPTY
                    
                    yield BurrowState((new_rooms, new_hall), cost=cost)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    # Part 1
    # Process data with initial state of our four rooms
    room_a: list[str] = []
    room_b: list[str] = []
    room_c: list[str] = []
    room_d: list[str] = []
    hall: list[str] = []
    
    for line in data:   # we only care about chars in "ABCD."
        for x, char in enumerate(line):
            if char == ".":     # hall
                hall.append(char)
            if char in "ABCD":  # rooms
                if x == 3:
                    room_a.append(char)
                if x == 5:
                    room_b.append(char)
                if x == 7:
                    room_c.append(char)
                if x == 9:
                    room_d.append(char) 
    
    # Convert to {room: list[elements]}
    # E.g. {'A': ['A', 'B'], 'B': ['D', 'C'], 'C': ['B', 'D'], 'D': ['C', 'A']}
    rooms = {k: room for k, room in zip(BurrowState.ROOM_KEYS, [room_a, room_b, room_c, room_d])}
    
    # state is given by combination of rooms and hall
    start = BurrowState((rooms, hall))
    current, came_from = solve_with_dijkstra(start)
    logger.info("Part 1:\n%s", render_breadcrumbs(current, came_from, start))
    
    # Part 2 - We need to insert D C B A
    #                            D B A C
    room_a.insert(1, 'D')
    room_a.insert(2, 'D')
    room_b.insert(1, 'C')
    room_b.insert(2, 'B')
    room_c.insert(1, 'B')
    room_c.insert(2, 'A')
    room_d.insert(1, 'A')
    room_d.insert(2, 'C')

    start = BurrowState((rooms, hall))
    current, came_from = solve_with_dijkstra(start)
    logger.info("Part 2:\n%s", render_breadcrumbs(current, came_from, start))

def solve_with_dijkstra(start: BurrowState) -> tuple[BurrowState, dict[BurrowState, BurrowState]]:
    current: BurrowState = start
    frontier: list = []
    heapq.heappush(frontier, (0, current))   # init state will have energy cost of 0
    
    came_from = {}  # so we can rebuild path from breadcrumbs
    came_from[current] = None
    
    energy_so_far = {}  # store cumulative energy required to get to this state. Use as priority for heapq.
    energy_so_far[current] = 0
    
    while frontier:
        _, current = heapq.heappop(frontier)
        if current.is_goal():
            break
        
        next_state: BurrowState
        for next_state in current.next_state():
            new_energy = energy_so_far[current] + next_state.last_cost
            
            # If we haven't seen this state before, or we've found a more efficient way to get to this state...
            if next_state not in energy_so_far or new_energy < energy_so_far[next_state]:
                energy_so_far[next_state] = new_energy
                heapq.heappush(frontier, (new_energy, next_state))
                came_from[next_state] = current
                
    return (current, came_from)

def render_breadcrumbs(last_state: BurrowState, came_from: dict, start: BurrowState) -> str:
    """ Given a final state and a map of state-to-previous state, 
    render the entire path to the initial state. """
    breadcrumbs = []    # BurrowStates
    current: BurrowState = last_state  
    cumulative_energy = 0
    while current != start:
        breadcrumbs.append(str(current))
        cumulative_energy += current.last_cost
        current = came_from[current]
    
    breadcrumbs.append(str(start))
    breadcrumbs.reverse()
    breadcrumbs.append(f"\nCompleted in {len(breadcrumbs)-1} steps with total energy of {cumulative_energy}.\n")
    return "\n".join(breadcrumbs)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
