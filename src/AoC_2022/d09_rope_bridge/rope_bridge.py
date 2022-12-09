"""
Author: Darren
Date: 09/12/2022

Solving https://adventofcode.com/2022/day/9

Instructions describe the movement of the head.
- Each instruction can contain many steps.
- After each step, the tail may be required to move, in order to remain adjacent to the head.
- The tail should always move in the direction that puts it in the same row or column as the head.

Part 1:

We have a rope with two knots: head + tail.
How many positions does the tail of the rope visit at least once?

- Solution:
  - Point dataclass to store locations.
    - Knows how to add and subtract to return a new Point.
    - Contains a list of (x,y) vectors that immediately surround and include this point.  I.e.
      [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
  - VECTORS to map input instruction to a vector.
  - Create head Point and tail Point. They both start at (0,0).
  - Store tail in in visited set.  We use a set, because we only one to count location visited at least once.
  - Process each instruction.
    - For each step in the instruction:
      - Add the instruction vector to head, to create new head location.
      - Get the vector between head and tail.
      - If tail needs to move to catch up, determine the movement required.
      - Add the movement to the tail to create the new tail location, and store this in visisted.
   - Return the length of visisted.

Part 2:

The rope now has 10 knots. How many positions does the tail of the rope visit at least once?

Solution:

- Same as before.  But now, instead of just head and tail, we keep a list of knots.
- Process the instruction for head.
  - Make each subsequent knot move in turn, as it it were a tail.
  - Store the locations where the actual tail moves.
"""
from dataclasses import dataclass
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

@dataclass(frozen=True)
class Point:
    """ Class for storing a point x,y coordinate """
    x: int
    y: int
    
    # create a list of (x,y) vectors that sorround and include this point
    WITHIN_ONE = [(dx,dy) for dx in range(-1, 2) for dy in range(-1, 2)]
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
VECTORS = {
    'U': Point(0, 1),
    'R': Point(1, 0),
    'D': Point(0, -1),
    'L': Point(-1, 0)
}

def main():
    with open(INPUT_FILE, mode="rt") as f:
        # convert to list of (direction, magnitude)
        data = [(d, int(v)) for d, v in [instruction.split() for instruction in f.read().splitlines()]]
    
    answers = []
    for num_knots in (2, 10):
        visited_locations = pull_rope(data, num_knots)
        answers.append(len(visited_locations))

    print(answers)    

def pull_rope(instructions, num_knots: int) -> set[Point]:
    knots = [Point(0,0) for _ in range(num_knots)] 
    visited_locations: set[Point] = set()
    visited_locations.add(knots[-1]) # track the tail
    
    for direction, mag in instructions: # read char by char
        for _ in range(mag): # move one step at a time
            # print(f"Tail: {knots[-1]}; unique positions: {len(visited_locations)}")
            knots[0] += VECTORS[direction] # move the head
            for i in range(1, len(knots)): # move the tail
                vector = knots[i-1] - knots[i]
                
                if vector in [Point(x,y) for (x,y) in Point.WITHIN_ONE]:
                    continue # don't need to move
                else:
                    knots[i] = knots[i] + get_move(vector)
                    visited_locations.add(knots[-1])
    
    return visited_locations
               
def get_move(vector: Point) -> Point:
    x_move = y_move = 0
    move_x = move_y = False
    
    if vector.y == 0:   # we only need to move left or right
        move_x = True
    elif vector.x == 0: # we only need to move up or down
        move_y = True
    else: # we need to move diagonally
        assert vector.x != 0 and vector.y != 0, "We must move diagonally"
        move_x = move_y = True
    
    if move_x:
        x_move = 1 if vector.x > 0 else -1
    
    if move_y:
        y_move = 1 if vector.y > 0 else -1

    return Point(x_move, y_move)

def print_grid(knots, visited: set[Point]):
    pass  

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
