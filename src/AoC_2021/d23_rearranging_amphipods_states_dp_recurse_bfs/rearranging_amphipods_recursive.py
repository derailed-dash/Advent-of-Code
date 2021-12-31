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

This solution uses a recursive call to work out all possible ways to get to the goal from the current state, 
and returns the lowest cost result.  
Uses a dynamic processing cache to minimise the number of states we need to recurse through.

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
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

A = 'A'
B = 'B'
C = 'C'
D = 'D'
EMPTY = '.'
ROOM_KEYS = {A: 'A', B: 'B', C: 'C', D: 'D'}
POD_COSTS = {A: 1, B: 10, C: 100, D: 1000}
ROOM_IDX = {A: 2, B: 4, C: 6, D: 8}

def is_goal(state) -> bool:
    """ Returns False if any amphipods in any room are not of the right type """
    rooms, _ = state
    for room_type, pods in rooms.items():
        if any((amphipod != room_type) for amphipod in pods):
            return False
    return True

def can_move_from(room_key: str, room: list) -> bool:
    """ If this item is an amphipod and if we can move it """
    for item in room:
        if item != room_key and item != EMPTY:
            # If there's a pod at this location, and it doesn't belong in this room
            return True
    return False

def can_move_to(room_key: str, room: list) -> bool:
    """ Check if destination room is correct type and can accept a pod """
    for item in room:
        if item != room_key and item != EMPTY:
            # If there's already a pod in this room, and it's the wrong type 
            return False
    return True

def get_room_horiz_idx(room_key: str) -> int:
    """ Get the horizontal index (relative to the hall) that matches this room """
    return ROOM_IDX[room_key]

def get_top_item_idx(room_contents: list):
    """ Return the row index of the top pod (i.e. top occupied position) in a room """
    for i, item in enumerate(room_contents):
        if item != EMPTY:
            return i
    return None

def get_room_dest_idx(room_contents):
    """ Return the position in the room we want to move to. """
    for i, char in reversed(list(enumerate(room_contents))):
        if char == EMPTY:
            return i    # return the "bottom" (highest index) that is empty
    return None

def is_between(posn: int, room_key: str, hall_idx: int) -> bool:
    """ If this posn is between the room and the hall index """
    return ((get_room_horiz_idx(room_key) < posn < hall_idx)
            or (hall_idx < posn < get_room_horiz_idx(room_key)))

def is_clear_path(room_key: str, hall_idx: int, hall: list[str]) -> bool:
    """ Is it clear between the room and the hall position? 

    Args:
        room_key (str): Which room
        hall_idx (int): Which hall horizontal position
        hall (list[str]): Contents of the hall
    """
    for posn, item in enumerate(hall):
        if is_between(posn, room_key, hall_idx) and item != EMPTY:
            return False
    return True

def render_state(state) -> str:
    """ Generate a str representation of this state """
    rooms, hall = state
    rooms_list = [room for room_type, room in rooms.items()]
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

next_state = {} # allows us to trace a path with breadcrumbs
def get_hashable_state(state: tuple[dict[str, list], list[str]]) -> tuple[tuple, tuple]:
    """ Return hashable state in the form rooms, hall 
    Where room is of format ('B', ('D', 'C')) """
    rooms, hall = state
    return (tuple((k, tuple(v)) for k,v in rooms.items()), tuple(hall))

dp_cache = {}
def solve(state: tuple[dict[str, list], list[str]]) -> int:
    """ Returns the score from getting from the supplied state to the goal. 
    Cache states. """  
    rooms, hall = state
    hashable_state = get_hashable_state(state)
    if is_goal(state):
        return 0
    
    if hashable_state in dp_cache:  # if we've solved this state before...
        return dp_cache[hashable_state]
  
    # Determine if we have any pods in the hall that can go directly to dest
    # If we have, then this is the best move
    for i, pod in enumerate(hall): # position and item (pod or empty) in hall
        
        # If a pod, and we can move it to the room
        if pod in rooms and can_move_to(pod, rooms[pod]):
            if is_clear_path(pod, i, hall):
                dest_idx = get_room_dest_idx(rooms[pod])
                assert isinstance(dest_idx, int), "We've determined we can move to this room"
                dist = dest_idx + 1 + abs(get_room_horiz_idx(pod)-i)
                cost = POD_COSTS[pod] * dist
                
                # remove pod from hall
                new_hall = list(hall) # create a copy
                new_hall[i] = EMPTY
                
                # add pod to destination room
                new_rooms = {k: [room_item for room_item in v] for k, v in rooms.items()}                
                new_rooms[pod][dest_idx] = pod
                
                next_state[hashable_state] = (new_rooms, new_hall)

                return cost + solve((new_rooms, new_hall))

    # If we're here, no pods in the hall to move to destination.
    
    ans = int(1e9) # We will look for a better next step...
    
    # Evaluate which rooms we can move pods from
    for room_key, room_contents in rooms.items():
        if not can_move_from(room_key, room_contents):
            continue
        # If we're here, we can move out of this room
        
        pod_idx = get_top_item_idx(room_contents)
        if pod_idx is None:
            continue
        # If we're here, there's a pod to move from this room
        
        pod = room_contents[pod_idx]
        
        # Now find locations in the hall our pod can move to
        for hall_posn, item in enumerate(hall):
            if hall_posn in [2, 4, 6, 8]:
                continue    # skip hall positions above rooms
            if item != EMPTY:
                continue    # skip locations that are occupied
            
            # determine if we have a path to this destination
            if is_clear_path(room_key, hall_posn, hall):
                dist = pod_idx + 1 + abs(hall_posn - get_room_horiz_idx(room_key))
                
                # make a copy of hall and rooms, and update them
                new_hall = list(hall)
                new_hall[hall_posn] = pod
                
                # This is much quicker than a deep copy
                new_rooms = {k: [room_item for room_item in v] for k, v in rooms.items()}
                new_rooms[room_key][pod_idx] = EMPTY

                # cost of this move and recurse from new state
                cost = POD_COSTS[pod]*dist + solve((new_rooms, new_hall))
                if cost < ans:
                    ans = cost
                    next_state[hashable_state] = (new_rooms, new_hall)
                
                ans = min(ans, POD_COSTS[pod]*dist + solve((new_rooms, new_hall)))
    
    dp_cache[hashable_state] = ans  # store result for this input state
    return ans

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
    rooms = {k: room for k, room in zip(ROOM_KEYS, [room_a, room_b, room_c, room_d])}
    
    # state is given by combination of rooms and hall
    init_state = (rooms, hall)
    cost = solve(init_state)
    logger.info(render_breadcrumbs(init_state))
    logger.info("Part 1: %d\n", cost)
    
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

    cost = solve(init_state)
    logger.info(render_breadcrumbs(init_state))
    logger.info("Part 2: %d", cost)

def render_breadcrumbs(init_state) -> str:
    """ Given a starting state, render the state and then 
    iterative through all successive states, rendering as we go.
    Stop when we've reached the goal state. """
    breadcrumbs = []
    current = init_state
    
    crumb_count = 0
    while not is_goal(current):
        crumb_count += 1
        breadcrumbs.append(render_state(current))
        current = next_state[get_hashable_state(current)]    
    
    breadcrumbs.append(render_state(current)) # final state
    breadcrumbs.append(f"\nCompleted in {crumb_count} steps.\n")
    return "\n".join(breadcrumbs)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
