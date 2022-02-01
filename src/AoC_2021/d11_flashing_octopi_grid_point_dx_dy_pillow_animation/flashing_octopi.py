"""
Author: Darren
Date: 11/12/2021

Solving https://adventofcode.com/2021/day/11

We have 100 octopi, represented as a 10x10 grid of numbers that are octopus energy states.
The octopi slowly gain energy and then flash brightly when full.

With each cycle:
- +1 for all
- if >9: 
    - Octopus flashes, which increases neighbours (including diag) by 1.
      Note that a given neighbour may get energy from multiple adjacent flashes.
    - if neighbours then also reach >9, they flash too.
- Finally, any octopus that flashed is reset back to 0, having used its energy.

Part 1:
    Count total flashes after 100 steps.
    
    Create a grid from a 2D list.  Grid class contains logic to:
    - find all neighbours.
    - perform an energy cycle.

Part 2:
    Keep cycling until the grid is synchronised, i.e. when all values are 0.
    Since we track the number of flashes with each cycle, 
    we can just check for when the number of flashes is equal to the total number of octopi.
"""
from copy import deepcopy
from dataclasses import dataclass
import logging
import os
import time
from PIL import Image, ImageFont, ImageDraw

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

RENDER_ANIMATION = True
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output/")
ANIM_FILE = os.path.join(OUTPUT_DIR, "octopi.gif")  # where we'll save the animation to

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

@dataclass(frozen=True)
class Point():
    """ Our immutable point data class """
    ADJACENT_DELTAS = [(dx,dy) for dx in range(-1, 2) 
                               for dy in range(-1, 2) if (dx,dy) != (0,0)]
    
    x: int
    y: int
    
    def yield_neighbours(self):
        """ Yield adjacent (orthogonal) neighbour points """
        for vector in Point.ADJACENT_DELTAS:
            yield Point(self.x + vector[0], self.y + vector[1])

class Grid():
    """ 2D grid of point values. Knows how to:
       - Determine value at any point
       - Determine all neighbouring points of a given point
       - Perform an 'energy cycle' """
       
    FLASH_THRESHOLD = 9
    ENERGY_RESET = 0
       
    def __init__(self, grid_array: list, render_animation=False) -> None:
        """ Generate Grid instance from 2D array. 
        This works on a deep copy of the input data, so as not to mutate the input. """
        
        self._array = deepcopy(grid_array)  # Store a deep copy of input data
        self._x_size = len(self._array[0])
        self._y_size = len(self._array)
        self._generation = 0
        self._cumulative_flashes = 0
        
        self._render_animation = render_animation
        self._frames: list[Image.Image] = [] # for animating
    
    def save_frames(self, file: str, duration=50) -> None:
        """ Save the animation frames to the specified file.

        Args:
            file (str): File path to save to
            duration (int, optional): Frame length in ms. Defaults to 50.
            scale (int, optional): Size of each pixel. Defaults to 20.
        """
        if not self._frames:
            logger.info("Nothing to save")
            return
        
        dir_path = os.path.dirname(file)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        try:
            self._frames[0].save(file, save_all=True, loop=True, blend=1, duration=duration, append_images=self._frames[1:])
            logger.info("Animation saved to %s", file)
        except (KeyError, IOError):
            logger.error("Unable to save to %s", file)
        
    @property
    def x_size(self):
        """ Array width (cols) """
        return self._x_size
    
    @property
    def y_size(self):
        """ Array height (rows) """
        return self._y_size
    
    @property 
    def cumulative_flashes(self) -> int:
        """ Total flashes in the life of this grid """
        return self._cumulative_flashes
    
    @property
    def generation(self) -> int:
        """ Return the current generation cycle of this grid """
        return self._generation
    
    def set_value_at_point(self, point: Point, value: int):
        self._array[point.y][point.x] = value
        
    def value_at_point(self, point: Point) -> int:
        """ Value at this point """
        return self._array[point.y][point.x]
    
    def _valid_location(self, point: Point) -> bool:
        """ Check if a location is within the grid """
        if (0 <= point.x < self.x_size and  0 <= point.y < self.y_size):
            return True
        
        return False
    
    def all_points(self) -> list[Point]:
        points = [Point(x, y) for x in range(self.x_size) for y in range(self.y_size)]
        return points
              
    def cycle(self) -> int:
        """ Perform a grid cycle:
          - Octopus flashes when its energy is GREATER than 9.
          - When it flashes, it increments the energy of all adjacent octopi.
            (Which may cause more flashing.)
          - Once flashing is complete, any octopi that have flashed are reset to 0.
        
        Returns [int]: flashes in this cycle """

        # Step 1: increment all by 1     
        for point in self.all_points():
            self.set_value_at_point(point, self.value_at_point(point)+1)
        
        # Step 2: flash cascade
        flashed_octopi = set()     # Track which octopi have already flashed
        still_flashing = True
        while still_flashing:     # repeat this loop until no more flashing
            still_flashing = False
            for point in self.all_points():
                if point not in flashed_octopi and self.value_at_point(point) > Grid.FLASH_THRESHOLD:
                    flashed_octopi.add(point) # This octopus now flashes
                    still_flashing = True
                    for neighbour in point.yield_neighbours():  # increment any unflashed neighbours
                        if self._valid_location(neighbour):
                            if neighbour not in flashed_octopi:
                                self.set_value_at_point(neighbour, self.value_at_point(neighbour)+1)
            
        # Step 3: reset all flashed octopi back to 0
        for point in flashed_octopi:
            self.set_value_at_point(point, Grid.ENERGY_RESET)
            
        self._cumulative_flashes += len(flashed_octopi)    # update grid cumulative flash count
        self._generation += 1
        
        if self._render_animation:
            self.generate_frame()
            
        return len(flashed_octopi)
    
    def generate_frame(self):
        """ Render an image frame showing the current cycle state.
        Saves the frame to the self._frames list.
        Superimposes the cycle number text to the frame. """
        scale = 50
        all_values = [self.value_at_point(point) for point in self.all_points()] # flattened values
        max_energy = Grid.FLASH_THRESHOLD
        
        # create a new list of pixels, where each is given by an (R,G,B) tuple.
        pixel_colour_map = list(map(lambda x: (x*255//max_energy, 0, 0), all_values)) 
        
        # Create an image from the flattened list of pixels, and scale up the size
        small_image = Image.new(mode='RGB', size=(self.x_size, self.y_size))
        small_image.putdata(pixel_colour_map)  # load our original data into the image
        scaled_image = small_image.resize((self.x_size * scale, self.y_size * scale))

        # Add our cycle count text to the bottom right of the image
        image_draw = ImageDraw.Draw(scaled_image)        
        font = ImageFont.truetype('arial.ttf', 24)
        text = str(self._generation)
        rgba = (140, 200, 250, 255) # light blue
        textwidth, textheight = image_draw.textsize(text, font)
        im_width, im_height = scaled_image.size
        margin = 10     # margin we want round the text to the edge
        x_locn = im_width - textwidth - margin
        y_locn = im_height - textheight - margin
        image_draw.text((x_locn, y_locn), text, font=font, fill=rgba)
        
        if (0, 0, 0) in pixel_colour_map:  # if 0 in colour_map, we need to flash  
            flash_image = small_image.copy()
            new_image_data = []
            for pixel in pixel_colour_map:
                if pixel == (0, 0, 0):  # replace black with white
                    new_image_data.append((255, 255, 255))
                else:
                    new_image_data.append(pixel)
            
            # Add the new image data, and then resize as before
            flash_image.putdata(new_image_data)
            flash_image = flash_image.resize((self.x_size * scale, self.y_size * scale))
            
            flash_image_draw = ImageDraw.Draw(flash_image)
            flash_image_draw.text((x_locn, y_locn), text, font=font, fill=rgba)
            
            # Flash frame needs to get appended before the 'black' frame
            self._frames.append(flash_image)

        self._frames.append(scaled_image)
    
    def __repr__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._array)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = [[int(posn) for posn in row] for row in f.read().splitlines()]
        
    # Part 1 - How many flashes after 100 steps?
    grid = Grid(data, render_animation=RENDER_ANIMATION)
    for _ in range(100):
        grid.cycle()
    
    logger.info("Part 1: total flashes=%d", grid.cumulative_flashes)

    # Part 2
    while True:
        flash_count = grid.cycle()
        if flash_count == grid.x_size * grid.y_size:    # all octopi have flashed
            break
    
    logger.info("Part 2: synchronised at step: %d", grid.generation)  
    
    # let's add a few more cycles, to demonstrate the synchronisation
    for _ in range(60):
        flash_count = grid.cycle()
    
    grid.save_frames(ANIM_FILE, duration=100) # save to file

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
