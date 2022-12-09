"""
Author: Darren
Date: 09/12/2022

Solving https://adventofcode.com/2022/day/9

Instructions describe the movement of the head.
- Each instruction can contain many steps.
- After each step, the tail may be required to move, in order to remain adjacent to the head.
- The tail should always move in the direction that puts it in the same row or column as the head.

Part 1:

How many positions does the tail of the rope visit at least once?

Part 2:

"""
from dataclasses import dataclass
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

@dataclass(frozen=True)
class Point:
    """ Class for storing a point x,y coordinate """
    x: int
    y: int
    
    # create a list of points surrounding and including this point
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
    
    move_count = 0
    for direction, mag in instructions: # read char by char
        for _ in range(mag): # move one step at a time
            # print(f"Tail: {knots[-1]}; unique positions: {len(visited_locations)}")
            knots[0] += VECTORS[direction] # move the head
            for i in range(1, len(knots)): # move the tail
                vector = knots[i-1] - knots[i]
                
                if vector in [Point(x,y) for (x,y) in Point.WITHIN_ONE]:
                    continue # don't need to move
                else:
                    move = get_move(vector)
                    move_count += 1
                    # print(f"Moving knot {i} by {move}; move count={move_count}")
                    knots[i] = knots[i] + move
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
