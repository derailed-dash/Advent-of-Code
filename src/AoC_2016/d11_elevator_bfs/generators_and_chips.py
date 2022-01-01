"""
Author: Darren
Date: 20/06/2021

Solving https://adventofcode.com/2016/day/11

    Elevator can carry 2 RTGs (generators, "G") or microchips ("M") in any combination.
    Elevator will only run with at least 1 RTG or chip onboard.
    Elevator must stop on each floor to recharge.
    When RTGs are paired with their corresponding chip, they generate a shield: the chip is shielded.
    Pairing happens automatically if RTG and its chip are on the same floor.
    Unpaired chips get fried by nearby RTGs. That includes chips on the same floor as the elevator.
    The elevator stops on each floor it passes, to recharge.
    Elevator requirs at least one RTG or chip to move.
    Chips do not affect each other.
    Chips in the elevator are shielded, because the elevator is in the shielded region.

    We start on the 1st floor. 
    Need to get all the RTGs and microchips to the 4th floor. How many steps does this take?
    Each elevator stop counts as one step.

Solution:
    We want to use a BFS.
    Use heapq to prioritise the BFS, using a priority stored in the AreaState object.
    Priority is calculated based on how close we are to the goal.
    Goal is having all items in the top floor.  
    Each AreaState has a score, based on the number of items in each floor * floor number.
    Thus, the goal is the highest possible score.
    Priority is given by the GOAL score - current AreaState score.  Thus, the closer to the goal, the lower the priority.
    (Recall that heapq pops the lowest priority FIRST.)
    
Part 1:
    Floor class stores items on a given floor, including elevator.
    Can return its items, chips and generators, and unpaired chips.
    Can determine if it can accept a new chip or generator.
    Has a score attribute, where score is dependent on number of items and floor number.
    
    AreaState class has class attributes to store number of floors,
    all available items, and the the goal (i.e. score with all items in top floor).
    AreaState instances reflect a given state of all floors, 
    and stores a list of all parent states.
    AreaState can generate all valid next states, based on valid combinatons
    of items that can move from the current elevator-holding floor.
    AreaState has a score, which is the sum of scores of its floors.
    AreaState has a priority, which is the difference between score and goal.
    (Lower priority is processed first in the BFS implementation.)
    
    Solution takes 192 iterations and 62ms to solve with a priority heapq BFS.
    If we swap heapq with an unprioritised list implementation, and simply always pop the first item, 
    it takes 615438 iterations and over 2 minutes!!
    
Part 2:
    Barely an inconvenience!  Just add the new items to the first floor and repeat.

    Output:
    2021-07-26 07:29:38,720:INFO:   Goal is: 56
    2021-07-26 07:29:38,720:INFO:   Initial state:
    F4:   | .   .   .   .   .   .   .   .   .   .   .   .   .   .   |  0 |
    F3:   | .   .   .   .   .   .   .   .   .   .   .   .   .   ThM |  3 | {'ThM'}
    F2:   | CuG CuM .   .   .   .   .   .   RuG RuM .   .   ThG .   | 10 |
    F1: E | .   .   DiG DiM ElG ElM PlG PlM .   .   StG StM .   .   |  8 |
    Score: 21, Priority: 35, Parent count: 0
    2021-07-26 07:29:38,859:INFO:   Part 1 solved with 407 iterations.
    2021-07-26 07:29:38,859:INFO:   Final state:
    F4: E | CuG CuM DiG DiM ElG ElM PlG PlM RuG RuM StG StM ThG ThM | 56 |
    F3:   | .   .   .   .   .   .   .   .   .   .   .   .   .   .   |  0 |
    F2:   | .   .   .   .   .   .   .   .   .   .   .   .   .   .   |  0 |
    F1:   | .   .   .   .   .   .   .   .   .   .   .   .   .   .   |  0 |
    Score: 56, Priority: 0, Parent count: 61
    Execution time: 0.1418 seconds
"""
from __future__ import annotations, generator_stop, generators
import heapq
import logging
import os
import time
import re
from copy import deepcopy
from itertools import combinations
from dataclasses import dataclass
from typing import Sequence

#pylint: disable=logging-fstring-interpolation,invalid-name

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

@dataclass(frozen=True)
class Floor:
    """ Immutable Floor object
    
    By using a dataclass, the __init__ and __repr__ are craeated automatically/implicitly.
    This object is 'frozen' (immutable). 
    """
    
    GEN_TYPE = "G"
    CHIP_TYPE = "M"
    
    floor_num: int
    items: set      # made up of generators "XxG" and chips "XxM"
    has_elevator: bool = False
   
    def get_chips(self, other_items=None) -> set:
        items = self.items.copy()
        if other_items:
            items = items.union(other_items)
            
        return set(filter(lambda i: i[-1] == Floor.CHIP_TYPE, items))
    
    def get_generators(self, other_items=None) -> set:
        items = self.items.copy()
        if other_items:
            items = items.union(other_items)
        
        return set(filter(lambda i: i[-1] == Floor.GEN_TYPE, items))
    
    def get_unpaired_chips(self, other_items=None) -> set:
        gen_strs = set(gen[:-1] for gen in self.get_generators(other_items))
        chip_strs = set(chip[:-1] for chip in self.get_chips(other_items))
        
        unpaired_chips = chip_strs - gen_strs
        return set(chip + Floor.CHIP_TYPE for chip in unpaired_chips)
    
    def can_accept(self, item, other_items=None) -> bool:
        """ This item can only be placed on this floor if:
            - It is a generator, and the floor has no unpaired non-matching chips
            - It is a chip, and the floor has no non-matching generators

        Args:
            item (str): a chip or generator
            other_item(str): another chip or generator carried in the elevator

        Returns:
            [bool]: If the item can be accepted without causing chip frying.
        """
        if item[-1] == Floor.GEN_TYPE:
            # The item we want to place on this floor is a generator...
            if self.get_unpaired_chips(other_items):
                if len(self.get_unpaired_chips(other_items)) > 1:
                    # if more than one unpaired chip, adding a gen will definitely fry at least one chip
                    return False
                else:
                    # Must be only one unpaired chip on this floor. 
                    # Check if it is the matching chip for this generator...
                    if (item[:-1] + Floor.CHIP_TYPE) in self.get_unpaired_chips(other_items):
                        return True
                    
                    # The unpaired chip does not match this generator.  Adding this gen will fry the chip.
                    return False
            
            # No unpaired chips, so safe to put a generator here
            return True
        
        # If we're here, the item is a CHIP
        if self.get_generators(other_items):
            # If this chip has a matching generator, it's safe
            if (item[:-1] + Floor.GEN_TYPE) in self.get_generators(other_items):
                return True
            
            # Otherwise, no matching generator, and this chip will get fried    
            return False 
        
        # No generators, so safe to put chip here
        return True
    
    @property
    def score(self) -> int:
        """ The score is given by the floor number multiplied by the count of any generators and chips on this floor """
        return self.floor_num * (len(self.items))
    
    def __eq__(self, o: Floor) -> bool:
        return (self.floor_num == o.floor_num
                and self.has_elevator == o.has_elevator
                and self.items == o.items)
        
    def __hash__(self):
        return hash((self.floor_num, 
                     self.has_elevator, 
                     tuple(sorted(self.items))))
        
    def get_floor_plan(self, all_items: set) -> str:
        """Renders a floor str, formatted with fixed columns, 
        and replacing any absent generators or chips with a "." character.

        Args:
            all_items (set): All the items in the area

        Returns:
            str: The floor contents.
        """
        floor = "F" + str(self.floor_num)
        elevator = "E" if self.has_elevator else " "
        unpaired_chips = str(self.get_unpaired_chips()) if self.get_unpaired_chips() else ""
        
        # convert to 3-char width strs, left aligned
        item_strs = map("{0:<3}".format, [item if item in self.items else "." for item in sorted(all_items)])
        
        return (floor + ": " + elevator + " | " 
                + " ".join(item_strs) + " | " 
                + f"{self.score:>2}" + " | "
                + str(unpaired_chips))
        
    def __str__(self):
        floor = "F" + str(self.floor_num)
        elevator = "E" if self.has_elevator else " "
        items = str(sorted(self.items)) if self.items else "."
        
        return floor + ": " + elevator + " " + items + " (Score=" + str(self.score) + ")"

class AreaState:
    """ Represents the state of all floors in the area. 
    Knows how to generate all possible next states.
    """
    # we must set these before we initialise any instances of the class
    CLASS_INITIALISED = False
    FLOOR_COUNT = 0
    ALL_ITEMS = set()
    GOAL = 0
    
    @classmethod
    def class_init(cls, floor_count: int, all_items: set):
        """ Initialise class attributes

        Args:
            floor_count (int): The number of floors
            all_items (set): All the generators
        """
        AreaState.FLOOR_COUNT = floor_count
        AreaState.ALL_ITEMS = all_items
        
        # Objective is to have all the items in the top floor
        # E.g. with 4 floors, goal will be 4 * items
        AreaState.GOAL = AreaState.FLOOR_COUNT * (len(AreaState.ALL_ITEMS))
        AreaState.CLASS_INITIALISED = True
    
    def __init__(self, floors: Sequence[Floor], parents=None) -> None:
        """ Create a new instance of an AreaState.
        If this is created as a possible state from a previous state, 
        then parents (a list of previous states) wil be supplied.

        Args:
            floors (Collection[Floor]): The ordered list/tuple of Floor objects.
            parents ([type], optional): [description]. Defaults to None.

        Raises:
            ValueError: If we try to create an instance without first calling class_init() on the class itself.
        """
        if not AreaState.CLASS_INITIALISED:
            raise ValueError("Class attributes not set.")
        
        self._floors = tuple(floors)    # we want this to be immutable
        if parents is None:
            self._parents = []
        else:
            self._parents = parents

    @property
    def floors(self) -> Sequence[Floor]:
        """ Ordered sequence of Floors 
        Note: floors are zero-indexed, and floor nums are 1-indexed """
        return self._floors
    
    @property
    def parents(self) -> list:
        return self._parents
    
    def next_state(self):
        """ Valid states:
        - Select any 1 or 2 items on the floor with elevator.
        - Move item(s) one floor above or below.
        - If any item is a G, target floor must have no unpaired C, except matching C.
        - If any item is a C, target floor must:
            - have no G, except matching G
        """
        floors = list(self.floors)  # make a copy of the floors, as a list
        src_floor:Floor = list(filter(lambda x: x.has_elevator, floors))[0]
        src_floor_num = src_floor.floor_num
        
        # Determine next possible floors for elevator to move to (one up, or one down)
        target_floor_nums = []
        if src_floor.floor_num-1 > 0:
            target_floor_nums.append(src_floor.floor_num-1)
        if src_floor.floor_num+1 <= AreaState.FLOOR_COUNT:
            target_floor_nums.append(src_floor.floor_num+1)
            
        # Get item combos for the src floor
        items_to_move = [tuple([item]) for item in src_floor.items]    # list of tuples
        pairs_to_move = list(combinations(src_floor.items, 2))
        items_to_move.extend(pairs_to_move)
        
        # Establish which item combos are safe to move to target floor
        for target_floor_num in target_floor_nums:
            target_floor = floors[target_floor_num-1]
            for item_group in items_to_move:
                # item_group could have one or two items to move
                can_accept_item_group = True
                for item in item_group:
                    other_items = list(item_group).copy()
                    other_items.remove(item)
                    if not target_floor.can_accept(item, other_items=other_items):
                        can_accept_item_group = False
                        break
                    
                if can_accept_item_group:    
                    new_floors = deepcopy(floors)
                    
                    new_src_floor = Floor(floor_num=src_floor_num, items=src_floor.items.difference(item_group), has_elevator=False)
                    new_floors[src_floor_num-1] = new_src_floor
                    new_target_floor = Floor(floor_num=target_floor_num, items=target_floor.items.union(item_group), has_elevator=True)
                    new_floors[target_floor_num-1] = new_target_floor
                    
                    yield AreaState(new_floors, parents=self.parents + [self])
    
    @property
    def score(self) -> int:
        """The sum of scores of all floors in the AreaState """
        return sum(floor.score for floor in self.floors)
        
    @property
    def priority(self) -> int:
        """ Priority is given by GOAL - score. Thus, lowest value represents highest priority. """
        return AreaState.GOAL - self.score
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}:{hash(self)},Score={self.score},Parents={len(self.parents)}"
    
    def __str__(self) -> str:
        floor_lines = [floor.get_floor_plan(AreaState.ALL_ITEMS) 
                       for floor in reversed(self.floors)]
        
        return ("\n".join(floor_lines) 
                + "\nScore: " + str(self.score) + ", Priority: " + str(self.priority) 
                + ", Parent count: " + str(len(self.parents)))
    
    def __eq__(self, o: AreaState) -> bool:
        return (self.floors == o.floors)
    
    def __hash__(self) -> int:
        return hash(self.floors)
    
    def __lt__(self, o: AreaState) -> bool:
        """ Compares AreaState instances by priority. 
        We want lower priority to be popped earlier from the heap queue when performing a BFS search """
        return self.priority < o.priority
        
def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().title().splitlines()    # convert file to list of str; convert to title caps
    
    # Get all the gens and chips referenced in the input file.
    # We want to extract first two chars from the element only.
    generators_pattern = re.compile(r"[A|An] (..)\w* Generator")
    chips_pattern = re.compile(r"[A|An] (..)\w*-Compatible")
    
    # Create sets of all generators (XxG) and chips (XxM)
    all_items = set(gen + Floor.GEN_TYPE for gen in generators_pattern.findall("".join(data)))
    all_items.update(set(chip + Floor.CHIP_TYPE for chip in chips_pattern.findall("".join(data))))
    
    # One-off initialisation of class attributes
    AreaState.class_init(len(data), all_items)
    
    logging.info(f"Goal is: {AreaState.GOAL}")
    
    # get initial state
    floors: list[Floor] = []
    for i, line in enumerate(data, 1):      
        floor = i
        
        items_found = set(gen + Floor.GEN_TYPE for gen in generators_pattern.findall("".join(line)))
        items_found.update(set(chip + Floor.CHIP_TYPE for chip in chips_pattern.findall("".join(line))))
        
        floor = Floor(floor_num=i, 
                  items=items_found,
                  has_elevator=(i==1))
       
        floors.append(floor)
        
    init_state = AreaState(floors)
    logging.info(f"Initial state:\n{init_state}")
    logging.debug(f"Hash of state = {hash(init_state)}")
    
    states_explored = set()
    states_explored.add(init_state)

    current_state = init_state    
    states_queue:list[AreaState] = []
    states_queue.append(current_state)
    
    iterations = 0
    
    while states_queue:
        iterations += 1
        current_state = heapq.heappop(states_queue)
        
        if (current_state.score == AreaState.GOAL):
            logging.debug("Solution found!")
            break
        
        for new_state in current_state.next_state():
            if new_state not in states_explored:
                states_explored.add(new_state)
                heapq.heappush(states_queue, new_state)
    
    logging.info(f"Part 1 solved with {iterations} iterations.")            
    logging.info(f"Final state:\n{current_state}")
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
