"""
Author: Darren
Date: 20/12/2021

Solving https://adventofcode.com/2021/day/20

Part 1:
    Store lit pixels in a set, usings coords from input str.
    Determine the bounds of the set.
    ImageArray class creates a set of deltas in order to generate a 3x3 grid of any given point.
    The hard work is done in the enhance() method.
    For each cycle, we use the 3x3 grid about each px to generate a integer value lookup.
    This lookup is used agains the enhancement map, to determine the new value of the px in the new 
    ImageArray.  The infinite canvas is typically made up of '.'  
    But with certain enhancement maps, the infinite canvas alternates between lit and dark.
    So, our ImageArray determines which char should be used in the next cycle,
    and passes it to the initiaser for the new ImageArray.

Part 2:
    Same, but 50 cycles instead of 2.  Runs pretty quick, so no need to do anything clever.
"""
from __future__ import annotations
import logging
import os
import time
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

class ImageArray():
    """ Stores array of pixels (points) in a set. 
    Knows how many pixels are lit.  Is able to create a new ImageArray based on rules. """
    LIGHT = "#" # 1
    DARK = "."  # 0
    BIN_MAP = { DARK: '0', LIGHT: '1'}
    
    def __init__(self, image_data, img_enhancement_map: str, canvas_char='.') -> None:
        """ Create a new ImageArray, containing a set of lit pixels.

        Args:
            image_data ([type]): Str representation or set.
            img_enhancement_map (str): Map used for enhancing the image.
            expansion_char (str, optional): Typically DARK, but can be lit depending on enhancement map.
        """
        
        delta = 1   # delta distance to use when finding neighbours
        self._adjacent_deltas = [(dx,dy) for dy in range(-delta, delta+1) for dx in range(-delta, delta+1)]

        self._img_enhancement_map = img_enhancement_map
        
        if isinstance(image_data, str):
            self._pixels = self._process_img_str(image_data)
        else:
            assert isinstance(image_data, set)
            self._pixels = image_data
        
        # bounds of set
        self._min_x = min(pixel.x for pixel in self._pixels)
        self._max_x = max(pixel.x for pixel in self._pixels)
        self._min_y = min(pixel.y for pixel in self._pixels)
        self._max_y = max(pixel.y for pixel in self._pixels)
        
        self._canvas_char = canvas_char
        
    def _process_img_str(self, image_data: str) -> set[Point]:
        """ Take a str of image data and convert to a set.
        Only stores points that are lit. """
        pixels = set()
        
        for y, line in enumerate(image_data.splitlines()):
            for x, char in enumerate(line):
                if char == ImageArray.LIGHT:
                    pixels.add(Point(x, y))
        
        return pixels
    
    def render(self) -> str:
        """ Generate str representation """
        lines = []    
        for y in range(self._min_y, self._max_y+1):
            line = ""
            for x in range(self._min_x, self._max_x+1):                 
                char = ImageArray.LIGHT if Point(x,y) in self._pixels else ImageArray.DARK
                line += char

            lines.append(line)
            
        return "\n".join(lines)
                            
    @property
    def lit(self) -> int:
        """ Return count of lit pixels """
        return len(self._pixels)

    def enhance(self) -> ImageArray:
        """ Process all squares simultaneously, i.e. based on current state of all pixels.
        Returns: ImageArray: New ImageArray, which will 1px bigger in all directions. """
        new_pixels = set()
        # Process using rules, with a 1px border around existing bounds
        for y in range(self._min_y-1, self._max_y+2):
            for x in range(self._min_x-1, self._max_x+2): 
                pnt = Point(x,y)       
                enhancement_i = self._image_enhancement_index(pnt) # get enhancement index for this point
                char = self._img_enhancement_map[enhancement_i] # determine type of pixel
                if char == ImageArray.LIGHT:
                    new_pixels.add(pnt)
        
        # Update the char that should be used for the infinite canvas next time.          
        next_canvas_char = self._img_enhancement_map[ImageArray._surrounded_by_index(self._canvas_char)]   
        return ImageArray(new_pixels, self._img_enhancement_map, canvas_char=next_canvas_char)
    
    @classmethod
    def _surrounded_by_index(cls, char: str) -> int:
        """ Get the mapping index for any char surrounded by . or # 
        I.e. where the 3x3 grid is all '.' (so int=0) or all '#' (so int=511). """
        assert char in (ImageArray.DARK, ImageArray.LIGHT), "Can only be surrounded by . or #"
        return ImageArray.convert_to_dec(9*ImageArray.BIN_MAP[char])
    
    def _image_enhancement_index(self, point: Point) -> int:
        """ Determine the decimal value of the 9-bit representation of this point.
        The 9-bit representation of the point is based on the 3x3 grid of pixels 
        with this point at the centre. Where any px is lit, the repr is 1, else 0.
        E.g. if only BR it lit, then the binary repr is 000000001.  If TL is lit, then 100000000.
        If the infinite canvas should be lit, then treat any pixels outside of 
        the current boundary as a lit pixel. """
        
        nine_box_bin = ""
        for nine_box_point in self._yield_neighbours(point):
            if nine_box_point in self._pixels:  # If this is lit
                nine_box_bin += ImageArray.BIN_MAP[ImageArray.LIGHT]
            elif (nine_box_point.x < self._min_x or nine_box_point.x > self._max_x or
                        nine_box_point.y < self._min_y or nine_box_point.y > self._max_y):
                # Outside the bounds, i.e. in the infinite canvas area
                if self._canvas_char == ImageArray.LIGHT:
                    nine_box_bin += ImageArray.BIN_MAP[ImageArray.LIGHT]
                else:
                    nine_box_bin += ImageArray.BIN_MAP[ImageArray.DARK]
            else:
                nine_box_bin += ImageArray.BIN_MAP[ImageArray.DARK]
        
        res = int(nine_box_bin, 2)
        return res
    
    @staticmethod
    def convert_to_dec(input_str: str) -> int:
        """ Convert bin str (e.g. '111110101') to int value """
        assert len(input_str) == 9, "Valid input should be a nine-box str representation"
        return int(input_str, 2)
        
    def _yield_neighbours(self, point:Point):
        """ Yield 9x9 grid of points, surrounding and including self, starting TL and ending BR. """
        for dx,dy in self._adjacent_deltas:
            neighbour = Point(point.x+dx, point.y+dy)
            yield neighbour
                
    def __repr__(self) -> str:
        return self.render()

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().split("\n\n")
        
    image_enhance_map = data[0] # 512 byte str
    input_img = data[1]
    
    image = ImageArray(input_img, image_enhance_map)
    
    for i in range(50):
        logger.debug("Image iteration %d", i)
        image = image.enhance()
        
    logger.debug("%s\nLit=%d\n", image, image.lit)    
  
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
