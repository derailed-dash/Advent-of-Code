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
from io import BytesIO
from pathlib import Path
import time
import imageio as iio
from tqdm import tqdm
from matplotlib import pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.ticker import MaxNLocator

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

# MAKE SURE YOU DISABLE IF RUNNING WITH THE REAL DATA. IT TAKES TOO LONG!!!
ENABLE_ANIMATIONS = True
OUTPUT_FOLDER = Path(SCRIPT_DIR, "output/")

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

class Animator():
    """ Creates an animation file of specified target size. 
    Designed to be used as Context Manager. E.g. 
    with Animator(file=Path("path/to/file""), fps=num) as animator:
        # code
    """
   
    def __enter__(self):
        """ Required for ContextManager implementation. """
        if self._enabled:
            self._create_path()
        
        return self # so the as <name> returns an object
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Required for ContextManager implementation. """
        if self._enabled:
            self._save_anim()
        
    def __init__(self, file: Path, fps: int, loop=1, enabled=True) -> None:
        """ Create an Animator. Suggest the file should be a .gif.
        Set frames per second (fps). 
        Set loop to 0, to loop indefinitely. Default is 1. """
        self._enabled = enabled
        self._outputfile = file
        self._frames = []  # can be in-memory BytesIO objects, or files
        self._fps = fps
        self._loop = loop
        
    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
    
    def _create_path(self):
        if self._enabled:
            dir_path = Path(self._outputfile).parent
            if not Path.exists(dir_path):
                Path.mkdir(dir_path)
    
    def _save_anim(self):
        """ Takes animation frames, and converts to a single animated file. """
        with iio.get_writer(self._outputfile, mode='I', fps=self._fps, loop=self._loop) as writer:
            for frame in tqdm(self._frames):
                image = iio.imread(frame)
                writer.append_data(image)
                
        print(f"Animation saved to {self._outputfile}")
    
    def add_frame(self, frame):
        """ Add a frame to the animation.
        The frame can be in the form of a BytesIO object, or a file Path
        """
        self._frames.append(frame)

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
        
    with Animator(file=Path(OUTPUT_FOLDER, "rope_bridge_pt1.gif"), fps=10, enabled=ENABLE_ANIMATIONS) as animator:
        rope_sim = RopeSim(data, 2, animator=animator)
        visited_locations = rope_sim.pull_rope()
        answers.append(len(visited_locations))
        
    with Animator(file=Path(OUTPUT_FOLDER, "rope_bridge_pt2.gif"), fps=20, enabled=ENABLE_ANIMATIONS) as animator:
        rope_sim = RopeSim(data, 10, animator=animator)
        visited_locations = rope_sim.pull_rope()
        answers.append(len(visited_locations))

    print(answers)

class RopeSim():
    """ Simulates a rope with a number of knots. We move the head according to a set of instructions. 
    Here we model the movement of the knots behind the head, according to the rules specified. """
    
    def __init__(self, motions: list[tuple[str, int]], num_knots: int, animator=None) -> None:
        """ Expects a list of instructions in the format:
        [['R', 5], ['U', 8], ...]
        
        Models rope with num_knots. The first is the head, and the last is the tail. """
        self._instructions = motions
        self._num_knots = num_knots
        self._knots = [Point(0,0) for _ in range(self._num_knots)] 
        self._all_head_locations: set[Point] = set()  # for rendering the vis
        
        self._animator: Animator = animator
        self._plt_info = self._init_plt()  # contains (figure, axes)
    
    @staticmethod
    def _get_next_move(vector: Point) -> Point:
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
    
    def pull_rope(self) -> set[Point]:
        """ Simulate the rope knot movemens, according to the rules given. """
        
        visited_locations: set[Point] = set()
        visited_locations.add(self._knots[-1]) # track the tail
        
        step = 0
        for direction, mag in self._instructions: # read char by char
            for _ in range(mag): # move one step at a time
                # print(f"Tail: {knots[-1]}; unique positions: {len(visited_locations)}")
                self._knots[0] += VECTORS[direction] # move the head
                self._all_head_locations.add(self._knots[0])
                
                for i in range(1, len(self._knots)): # move the tail
                    step += 1
                    vector = self._knots[i-1] - self._knots[i]
                    
                    if vector in [Point(x,y) for (x,y) in Point.WITHIN_ONE]:
                        continue # don't need to move
                    else:
                        self._knots[i] = self._knots[i] + RopeSim._get_next_move(vector)
                        visited_locations.add(self._knots[-1])

                        if self._animator and self._animator.enabled:
                            self._render_frame(visited_locations, step)
    
        return visited_locations
    
    def _init_plt(self):
        """ Generate a Figure and Axes objects which are reused. """
        my_dpi = 120
        figure, axes = plt.subplots(figsize=(1024/my_dpi, 768/my_dpi), dpi=my_dpi, facecolor="white") # set size in pixels
        axes.set_aspect('equal') # set x and y to equal aspect
        axes.set_facecolor('xkcd:black')
        
        return figure, axes
    
    def _render_frame(self, visited: set[Point], iteration: int=0):
        """ Only renders an animation frame if we've attached an enabled Animator """
        
        fig, axes = self._plt_info
        axes.clear()
        
        # The grid will grow as the rope heads moves around
        max_x = max(self._all_head_locations, key=lambda point: point.x).x
        min_x = min(self._all_head_locations, key=lambda point: point.x).x
        max_y = max(self._all_head_locations, key=lambda point: point.y).y
        min_y = min(self._all_head_locations, key=lambda point: point.y).y
        axes.set_xlim(min_x - 2, max_x + 2)
        axes.set_ylim(min_y - 2, max_y + 2)

        # dynamically compute the marker size
        fig.canvas.draw()
        factor = 40  # Smaller factor means smaller markers
        mkr_size = int((axes.get_window_extent().width / (max_x-min_x+1) * (factor/fig.dpi)) ** 2)

        # make sure the ticks have integer values
        axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        head = self._knots[0]
        tail = self._knots[-1]
        others_knots = self._knots[1:-1]
        
        visited_x = [point.x for point in visited if point != tail]
        visited_y = [point.y for point in visited if point != tail]

        for knot in others_knots:
            axes.scatter(knot.x, knot.y, marker=MarkerStyle("."), s=mkr_size/2, color="white")
            
        axes.scatter(head.x, head.y, marker=MarkerStyle("."), s=mkr_size, color="red")
        axes.scatter(visited_x, visited_y, marker=MarkerStyle("x"), s=mkr_size/3, color="grey")
        axes.scatter(tail.x, tail.y, marker=MarkerStyle("*"), s=mkr_size/2, color="yellow")
                
        axes.set_title(f"Iteration: {iteration}; tail has visited {len(visited)} locations")
        
        # save the plot as a frame; store the frame in-memory, using a BytesIO buffer
        frame = BytesIO()
        plt.savefig(frame, format='png') # save to memory, rather than file
        self._animator.add_frame(frame)
        
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
