"""
Author: Darren
Date: 25/12/2021

Solving https://adventofcode.com/2021/day/25

Two herds of cucumbers.  One always moves east (>) and one always moves south (v).
Each step:
    1. Herd > attempts to move 1 step, all simultaneously
       E.g. ...>>>>.>.. becomes ...>>>.>.>.
    2. Herd v attempt to move 1 step, all simultaneously

Sea cucumbers that reach the edge wrap around to the other side!

Part 1:
    Keep iterating until the sea cucumbers stop moving.
    Use a Grid class that knows how to perform a migration cycle.
    Each cycle sets a flag if the grid has changed, 
    which can be interrogated to determine when to stop iterating.
    Because all cucumbers need to move simultaneously, 
    we'll make a copy of the grid before each migration. 

Part 2:
    No part 2 today! 
"""
import logging
import time
from io import BytesIO
from pathlib import Path
import imageio
from matplotlib import pyplot as plt

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

RENDER = True
OUTPUT_FILE = Path(SCRIPT_DIR, "output/migrating_cucumbers.gif")

class Animator():
    """ Creates an animation file of specified target size. """
    
    def __init__(self, file: Path, fps: int, loop=1) -> None:
        """ Create an Animator. Suggest the file should be a .gif.
        Set frames per second (fps). 
        Set loop to 0, to loop indefinitely. Default is 1. """
        self._outputfile = file
        self._frames: list[BytesIO] = []  # in-memory store of frames
        self._fps = fps
        self._loop = loop
        
        dir_path = Path(self._outputfile).parent
        if not Path.exists(dir_path):
            Path.mkdir(dir_path)
    
    def save_anim(self):
        """ Takes animation frames, and converts to a single animated file. """
        with imageio.get_writer(self._outputfile, mode='I', fps=self._fps, loop=self._loop) as writer:
            for buffer in self._frames:
                buffer.seek(0)
                image = imageio.imread(buffer)
                writer.append_data(image)
                
        logger.info("Animation saved to %s", self._outputfile)
    
    def add_frame(self, buffer: BytesIO):
        """ Add a frame, using in memory buffer """
        self._frames.append(buffer)

class Grid():
    """ Store locations of sea cucumbers. """
   
    def __init__(self, data: list[str], animator: Animator=None) -> None:
        """ Take input data and convert from list-of-str to list-of-list for easier manipulation. """
        self._grid = [list(row) for row in data]    # Now a nested list of list.
        self._row_len = len(self._grid[0])
        self._grid_len = len(self._grid)
        self._changed_last_cycle = True
        
        self._plot_info = self.setup_fig()
        self._animator = animator
        self._render_frame()
    
    @property
    def changed_last_cycle(self):
        return self._changed_last_cycle

    def cycle(self):
        """ Performs a migration cycle for our east-moving and south-moving herds 
        Performs all east, and then performs all south. Then updates the grid. """
        self._changed_last_cycle = False
        
        # Make a copy of the grid.  Shallow copy won't work, as we have a nested list. Deepcopy is too slow.
        tmp_grid = [[self._grid[y][x] for x in range(self._row_len)] for y in range(self._grid_len)]
        
        # process east herd, row by row
        for y in range(self._grid_len):
            for x in range(self._row_len):
                next_x = (x+1)%self._row_len  # get right / wrap-around
                if self._grid[y][x] + self._grid[y][next_x] == ">.":
                    tmp_grid[y][x] = "."
                    tmp_grid[y][next_x] = ">"
                    self._changed_last_cycle = True
        
        self._grid = tmp_grid
        self._render_frame()
        
        east_migrated = [[tmp_grid[y][x] for x in range(self._row_len)] for y in range(self._grid_len)]
                
        for y in range(self._grid_len):
            for x in range(self._row_len):
                next_y = (y+1)%self._grid_len  # get below / wrap-around
                if tmp_grid[y][x] + tmp_grid[next_y][x] == "v.":
                    east_migrated[y][x] = "."
                    east_migrated[next_y][x] = "v"
                    self._changed_last_cycle = True
        
        self._grid = east_migrated
        self._render_frame()
        
    def __repr__(self) -> str:
        return "\n".join("".join(char for char in row) for row in self._grid)
    
    def _render_frame(self):
        """ Only renders an animation frame if we've attached an Animator """
        if not self._animator:
            return
        
        east = set()
        south = set()
        
        for y in range(self._grid_len):
            for x in range(self._row_len):
                if self._grid[y][x] == ">":
                    east.add((x,y))
                elif self._grid[y][x] == "v":
                    south.add((x,y))
        
        east_x, east_y = zip(*east)
        south_x, south_y = zip(*south)
        
        axes, mkr_size = self._plot_info
        
        axes.clear()
        min_x, max_x = -0.5, self._row_len - 0.5
        min_y, max_y = -0.5, self._grid_len - 0.5
        axes.set_xlim(min_x, max_x)
        axes.set_ylim(max_y, min_y)
        
        axes.scatter(east_x, east_y, marker=">", s=mkr_size, color="black")
        axes.scatter(south_x, south_y, marker="v", s=mkr_size, color="white")
        
        # save the plot as a frame; store the frame in-memory, using a BytesIO buffer
        buf = BytesIO()
        plt.savefig(buf, format='png') # save to memory, rather than file
        self._animator.add_frame(buf)

    def setup_fig(self):
        fig, axes = plt.subplots(dpi=110)
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        axes.set_aspect('equal') # set x and y to equal aspect
        axes.set_facecolor('xkcd:orange')
        
        min_x, max_x = -0.5, self._row_len - 0.5
        min_y, max_y = -0.5, self._grid_len - 0.5
        axes.set_xlim(min_x, max_x)
        axes.set_ylim(max_y, min_y)

        # dynamically compute the marker size
        fig.canvas.draw()
        mkr_size = ((axes.get_window_extent().width / (max_x-min_x) * (45/fig.dpi)) ** 2)
        return axes, mkr_size

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    animator = None
    if RENDER:
        animator = Animator(file=OUTPUT_FILE, fps=6)
        grid = Grid(data, animator=animator)
    else:
        grid = Grid(data)

    i = 0
    while grid.changed_last_cycle:
        i += 1
        grid.cycle()

    logger.info("We've stopped changing at iteration %d", i)
    if animator:
        animator.save_anim()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds\n", t2 - t1)    
