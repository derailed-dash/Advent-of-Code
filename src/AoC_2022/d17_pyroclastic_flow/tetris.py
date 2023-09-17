"""
Author: Darren
Date: 17/12/2022

Solving https://adventofcode.com/2022/day/17

Rocks are falling.  And they resemble tetris pieces! They always fall in this order:
-, +, backwards L, |, ■.

Chamber is 7 units wide.  Rocks start to fall from:
- left edge 2 units from left wall
- bottom edge 3 units above highest rock in the room, or the floor.

Input is horizontal movement of the falling objects,
as a result of jets of gasses from the sides.  E.g.
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>

This pattern also repeats indefinitely.

Rocks are pushed 1 unit, then fall one unit. 
The rock comes to rest in the fall step AFTER it reaches its lowest point.
Then another rock starts to fall.

Part 1:

How many units tall will the tower of rocks be after 2022 rocks have stopped falling?

- Shape class:
  - Has a set of all the Points it occupies.
  - Factory methods to create each shape.
    Point coordinates are created with the appropriate starting position (offset).
  - Factory method to create a shape for a set of points (e.g. when we move a shape)
  - Is hashable, so we can store it in sets.

- Tower class:
  - Use itertools.cycle to infinitely iterate through the input jet pattern.
    We can always generate the next jet.
  - Use itertools.cycle to infinitely iterate through the shapes in order.
    We can always generate the next shape.
  - Stores all points for all at rest shapes (set).
  - Stores the current top of all the settled points.
  - Can determine origin for new shapes, using current top.
  - Simulates dropping a shape:
    - Creates the new shape at the appropriate origin.
    - Calls move with next jet.
    - Calls move with down. 
      If we can't move down, settles the shape by adding current shape to settled points.
  - To move a shape:
    - Check if we can move left, right or down based on bounds; return if we can't.
    - If bounds are okay, generate candidate points from current shape.
    - Check if candidate intersects with settled.  If so, we can't move there.
    - Otherwise, update current shape to be new shape from candidate points.

- Finally, call tower.drop_shape 2022 times.
    
Part 2:

How tall will the tower be after 1000000000000 rocks have stopped?

Part 1 achieves 1M drops / minute. So running Part 1 for this many drops would take 2 years!
We need a better solution. We need a repeating cycle. 

Look for a repeat of:
- Same dropped rock. (Enumerate the rocks.)
- Same index in the jets. (Enumerate the jet data.)
- Identical rock formation - lets build a str (which is hashable) from the last 20 rows.

We will store these three values in a cache, implemented as a dict:
  - Key = rock_index, jet_index, rock_formation.
  - Value = (current height, current shape count)
  
Implement check_cache() method:
  - Check if the current key is in the cache. 
  - If it is, return (True, height, last_height, shape count, last shape count)
  - if not, update the cache
  
- Modify drop_shape():
  - When our shape is settled, check the cache.
  - If we get a cache hit, update a property for repeats_found.
  - Store the two crucial values of our repeat cycle: height delta, and shape count delta.
  
- Add calculate_height(drops) method:
  - Determine how many drops are still required.
  - Determine how many repeat cycles we need, by dividing by the shape count delta.
    Also determine if there is a remainder, so we can manually drop the remaining shapes.
  - Determine the height increase, based on this number of repeats. Add this to current height.
  - Finally, return the calculated height, and the shape drop remainder.

- Back in main():
  - Drop shapes until we find our first repeat. Store the initial height at this point.
  - Call calculate_height to determine the calculated height after n drops.
  - Manually drop shapes for any remainder. Get the new height.
  - The final height = calculated height + new height - initial height.
"""
from dataclasses import dataclass
from enum import Enum
import itertools
from pathlib import Path
import time
from  colorama import Fore, Style

from common.aoc_commons import cls

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

VIS_ENABLED = False

class ShapeType(Enum):
    """ Enum for our five shapes """
    HLINE =       {(0, 0), (1, 0), (2, 0), (3, 0)}
    PLUS =        {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}
    BACKWARDS_L = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}
    I =           {(0, 0), (0, 1), (0, 2), (0, 3)}
    SQUARE =      {(0, 0), (1, 0), (0, 1), (1, 1)}    

MOVE = {
    "<": (-1, 0),
    ">": (1, 0),
    "V": (0, -1)
}

@dataclass(frozen=True)
class Point():
    """ Point with x,y coordinates and knows how to add a vector to create a new Point. """
    x: int
    y: int
    
    def __add__(self, other):
        """ Add other point/vector to this point, returning new point """
        return Point(self.x + other.x, self.y + other.y)     
    
    def __repr__(self) -> str:
        return f"P({self.x},{self.y})"
    
class Shape():
    """ Stores the points that make up this shape. 
    Has a factory method to create Shape instances based on shape type. """
    
    def __init__(self, points: set[Point], at_rest=False) -> None:
        self.points: set[Point] = points   # the points that make up the shape
        self.at_rest = at_rest
    
    @classmethod
    def create_shape_by_type(cls, shape_type: str, origin: Point):
        """ Factory method to create an instance of our shape.
        The shape points are offset by the supplied origin. """
        return cls({(Point(*coords) + origin) for coords in ShapeType[shape_type].value})

    @classmethod
    def create_shape_from_points(cls, points: set[Point], at_rest=False):
        """ Factory method to create an instance of our shape.
        The shape points are offset by the supplied origin. """
        return cls(points, at_rest)
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Shape):
            if self.points == __o.points:
                return True
            else:
                return False
        else:
            return NotImplemented  
    
    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return f"Shape(at_rest={self.at_rest}, points={self.points}"

class Tower():
    """ Fixed width tower that generates new shapes to drop, and blows shapes left and right as they drop. """
    WIDTH = 7
    LEFT_WALL_X = 0  
    RIGHT_WALL_X = LEFT_WALL_X + 7 + 1  # right wall at x=8
    OFFSET_X = 2 + 1  # objects start with left edge at x=3
    OFFSET_Y = 3 + 1  # new rocks have a gap of 3 above top of highest settled rock
    FLOOR_Y = 0
        
    class PrintingChars(Enum):
        FALLING = Style.BRIGHT + Fore.BLUE + "@" + Style.RESET_ALL
        AT_REST = Fore.YELLOW+ "#" + Style.RESET_ALL
        EMPTY = Fore.GREEN + "." + Style.RESET_ALL
        CORNER = Fore.GREEN + "+" + Style.RESET_ALL
        WALL = Fore.GREEN + "|" + Style.RESET_ALL
        FLOOR = Fore.GREEN + "-" + Style.RESET_ALL
    
    def __init__(self, jet_pattern: str) -> None:
        self._jet_pattern = itertools.cycle(enumerate(jet_pattern)) # infinite cycle
        self._shape_generator = itertools.cycle(enumerate(item.name for item in ShapeType))  # infinite cycle
        self.top = Tower.FLOOR_Y  # keep track of top of blocks
        self._all_at_rest_shapes: set[Shape] = set()
        self._all_at_rest_points: set[Point] = set() # tracking this for speed
        
        self.repeat_identified = False
        self._cache: dict[tuple, tuple] = {}    # K=(rock_idx, jet_idx, rock_formation): V=(height, shape_ct)
        self._repeat: tuple = (0, 0)  # height_diff, shape_diff
    
    def _current_origin(self) -> Point:
        """ Rocks are dropped 2 from the left edge, and 3 above the current tallest settled rock. """
        return Point(Tower.LEFT_WALL_X + Tower.OFFSET_X, self.top + Tower.OFFSET_Y)
    
    def _next_shape(self):
        """ Get the next shape from the generator """
        return next(self._shape_generator)
    
    def _next_jet(self):
        """ Get the next jet blast from the generator """
        return next(self._jet_pattern)
    
    def _check_cache(self, shape_index: int, jet_index: int, formation: str) -> tuple:
        key = (shape_index, jet_index, formation)
        shape_ct = len(self._all_at_rest_shapes)
        if key in self._cache: # We've found a repeat!
            # print(key)
            last_height, last_shape_count = self._cache[key]
            return (True, self.top, last_height, shape_ct, last_shape_count)
        else: # cache miss, so add new entry to the cache
            self._cache[key] = (self.top, shape_ct)
            
        return (False, self.top, 0, shape_ct, 0)
    
    def drop_shape(self):
        shape_index, next_shape_type = self._next_shape()
        self.current_shape = Shape.create_shape_by_type(next_shape_type, self._current_origin())
            
        while True:
            jet_index, jet = self._next_jet()
            self._move_shape(jet)
            if VIS_ENABLED:
                print_and_clear(str(self))
            
            if not self._move_shape("V"): # failed to move down
                self.top = max(self.top, max(point.y for point in self.current_shape.points))
                settled_shape = Shape.create_shape_from_points(self.current_shape.points, True)
                self._settle_shape(settled_shape)
                if not self.repeat_identified:
                    cache_response = self._check_cache(shape_index, jet_index, self.get_recent_formation())
                    if cache_response[0]: # Cache hit
                        # print(cache_response)
                        self.repeat_identified = True
                        self._repeat = (cache_response[1] - cache_response[2], # current top - last top
                                        cache_response[3] - cache_response[4]) # current shape ct - last shape ct

                break
    
    def calculate_height(self, shape_drops: int) -> tuple[int, int]:
        """ Calculate the additional height given n shape drops. 
        We know that x shapes (shape repeat) create a height delta (height repeat) of y.
        x - current_shape_ct -> required_drops
        required_drops // shape_repeat -> whole repeats required 
        required_drops % shape_repeat -> remaining drops required
        required_drops * height_repeat -> height delta
        
        Returns tuple: new_height (int), remaining drops (int)
        """
        remaining_drops = shape_drops - len(self._all_at_rest_shapes)
        repeats_req = remaining_drops // self._repeat[1]    # full repeats
        remaining_drops %= self._repeat[1]      # remaining individual drops
        
        height_delta = self._repeat[0] * repeats_req  # height created by these repeats
        new_height = self.top + height_delta
        
        return new_height, remaining_drops
    
    def _settle_shape(self, shape: Shape):
        """ Add this shape to the settled sets """
        self._all_at_rest_shapes.add(shape)
        self._all_at_rest_points.update(shape.points)
    
    def _move_shape(self, direction) -> bool:
        """ Move a shape in the direction indicated. Return False if we can't move. """
        
        # Test against boundaries
        if direction == "<":
            shape_left_x = min(point.x for point in self.current_shape.points)
            if shape_left_x == Tower.LEFT_WALL_X + 1:
                return False # can't move left
            
        if direction == ">":
            shape_right_x = max(point.x for point in self.current_shape.points)
            if shape_right_x == Tower.RIGHT_WALL_X - 1:
                return False # can't move right
            
        if direction == "V":
            shape_bottom = min(point.y for point in self.current_shape.points)
            if shape_bottom == Tower.FLOOR_Y + 1:
                return False # can't move down
        
        # Move phase - test for collision
        candidate_points = {(point + Point(*MOVE[direction])) for point in self.current_shape.points}
        if self._all_at_rest_points & candidate_points: # If the candidate would intersect
            return False # Then this is not a valid posiiton
        else: # We can move there. Update our current shape position, by constructing a new shape a the new position
            self.current_shape = Shape.create_shape_from_points(candidate_points)
        return True
    
    def get_recent_formation(self) -> str:
        """ Covert last (top) 20 rows into a str representation. """
        rows = []
        min_y = max(0, self.top-20) # we want the last 20 lines
        for y in range(min_y, self.top+1):
            line = ""
            for x in range(Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X):
                if Point(x,y) in self._all_at_rest_points:
                    line += Tower.PrintingChars.AT_REST.value
                elif Point(x,y) in self.current_shape.points:
                    line += Tower.PrintingChars.FALLING.value
                else:
                    line += Tower.PrintingChars.EMPTY.value
            
            rows.append(line)
            
        return "\n".join(rows[::-1])
                   
    def __str__(self) -> str:
        rows = []
        # top_for_vis = max(self.top, max(point.y for point in self.current_shape.points))
        top_for_vis = self.top + Tower.OFFSET_Y
            
        for y in range(Tower.FLOOR_Y, top_for_vis + 1):
            line = f"{y:3d} "
            if y == Tower.FLOOR_Y:
                line += (Tower.PrintingChars.CORNER.value 
                            + (Tower.PrintingChars.FLOOR.value * Tower.WIDTH) 
                            + Tower.PrintingChars.CORNER.value)
            else:            
                for x in range(Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X + 1):
                    if x in (Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X):
                        line += Tower.PrintingChars.WALL.value
                    elif Point(x,y) in self._all_at_rest_points:
                        line += Tower.PrintingChars.AT_REST.value
                    elif Point(x,y) in self.current_shape.points:
                        line += Tower.PrintingChars.FALLING.value
                    else:
                        line += Tower.PrintingChars.EMPTY.value
                    
            rows.append(line)
        
        return f"{repr(self)}:\n" + "\n".join(rows[::-1]) 

    def __repr__(self) -> str:
        return (f"Tower(height={self.top}, rested={len(self._all_at_rest_shapes)})")

def print_and_clear(msg: str, delay=0.05):
    print(msg)
    time.sleep(delay)
    cls()

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()

    # Part 1        
    tower = Tower(jet_pattern=data)
    for _ in range(2022):
        tower.drop_shape()
    
    print(f"Part 1: {repr(tower)}")
    
    # Part 2
    tower = Tower(jet_pattern=data)  # Recreate the initial tower
    while not tower.repeat_identified:  # Drop until we identify the first repeat
        tower.drop_shape()
    height_at_repeat_start = tower.top  # The height achieved before first repeat
    print(f"\nPart 2: Repeat found at: {repr(tower)}")
    
    # Here we calculate the new height.  But we're NOT modifying the actual tower height.
    new_height, remaining_drops = tower.calculate_height(1000000000000)
    print(f"Part 2: Calculated new height from repeats: {new_height}")
        
    # If drops was not an exact multiple of drop repeat, 
    # then we'll need to top up with the remaining drops.
    # However, we're continuing the drops with our tower at the point where the repeat was identified.
    for _ in range(remaining_drops):
        tower.drop_shape()
    height_after_top_up = tower.top  # But this number does NOT include the calculated height delta.
    # So get the diff between the height now, and the height when we stopped dropping.
    final_height = new_height + height_after_top_up - height_at_repeat_start
    
    print(f"Part 2: Final height after top-up: {final_height}")

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
