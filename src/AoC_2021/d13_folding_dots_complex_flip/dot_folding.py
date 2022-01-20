"""
Author: Darren
Date: 13/12/2021

Solving https://adventofcode.com/2021/day/13

We have a set of x,y coords that represent dots on a piece of paper. E.g.
6,10
0,14
9,10
0,3

We have a set of fold instructions, along a given x or y axis. E.g.
fold along y=7

Solution:
    Complex numbers FTW!

Part 1:
    Follow first fold instruction.  Overlay the resulting dots.
    Count how many dots there are.
    Store the data as complex numbers in a set.  And then:
    - Flip vertically by negating the real component (relative to the axis)
    - Flip horizontally by negating the imag component (relative to the axis)
    - Simply union the unfolded half with the folded half.

Part 2:
    Complete the fold instructions.
    Render as a str.
    Work out size of the printable area from max real and imag components.
    Then print a grid of this size, but printing # if the coord exists in the complex set.
"""
import logging
import os
import time
from matplotlib import pyplot as plt

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

class Paper():
    """ Represents transparent paper with dots at specified x,y locations.
    The paper knows how to fold itself, given an instruction with an x or y value to fold along. """
    def __init__(self, dots: set[complex]) -> None:
        self._dots: set[complex] = dots
    
    @property
    def dot_count(self) -> int:
        """ Total number of dots showing on the paper """
        return len(self._dots)
    
    def __str__(self) -> str:
        """ Convert the dots to a printable string """
        height = int(max(self._dots, key=lambda y: y.imag).imag)
        width = int(max(self._dots, key=lambda x: x.real).real)
        
        rows = []
        for row in range(height+1):
            row_str = ""
            for col in range(width+1):
                coord = complex(col, row)
                row_str += "#" if coord in self._dots else " "

            rows.append(row_str)
        
        return "\n".join(rows)

    def render_as_plt(self):
        """ Render this paper and its dots as a scatter plot """
        all_x = [point.real for point in self._dots]
        all_y = [point.imag for point in self._dots]
        
        axes = plt.gca()
        axes.set_aspect('equal')
        plt.axis("off") # hide the border around the plot axes
        axes.set_xlim(min(all_x)-1, max(all_x)+1)
        axes.set_ylim(min(all_y)-1, max(all_y)+1)
        axes.invert_yaxis()
        
        axes.scatter(all_x, all_y, marker="o", s=50)
        plt.show()
    
    def fold(self, instruction: list[str]):
        """ Fold along a given axis.  Returns the union set of 
        numbers before the fold line, and the flip of the numbers after the fold line.

        Args:
            instruction (list[str]): x (vertical) or y (horizontal), value of fold axis
        """
        instr, axis = instruction[0], int(instruction[1])
        assert instr in ('x', 'y'), "Instruction must be 'x' or 'y'"
        
        before_fold = set()
        after_fold = set()
        
        if instr == 'x':    # fold vertical
            before_fold = set(dot for dot in self._dots if dot.real < axis)
            after_fold = set(num for num in self._dots if num.real > axis)
            folded = set(complex(axis-(num.real-axis), num.imag) for num in after_fold)
        else:   # fold horizontal
            before_fold = set(num for num in self._dots if num.imag < axis)
            after_fold = set(num for num in self._dots if num.imag > axis)
            folded = set(complex(num.real, axis-(num.imag-axis)) for num in after_fold)
        
        self._dots = before_fold | folded   

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        dots, instructions = process_data(f.read())

    paper = Paper(dots)
    
    # Part 1 - First instruction only
    paper.fold(instructions[0])
    logger.info("Part 1: %d dots are visible", paper.dot_count)

    # Part 2 - All remaining instructions
    for instruction in instructions[1:]:
        paper.fold(instruction)
        
    logger.info("Part 2: %d dots are visible", paper.dot_count)
    logger.info("Part 2 decoded:\n%s", paper)
    paper.render_as_plt()

def process_data(data: str) -> tuple[set[complex], list]:
    """ Input has n rows of x,y coords, then an empty line, then rows of instructions """
    
    coords, _, instructions = data.partition('\n\n')
    dots = set()
    for coord in coords.splitlines():    # e.g. [6, 10]
        x,y = map(int, coord.split(","))
        dots.add(complex(x, y))
        
    # convert "fold along y=7" to "[y,7]"
    instructions = [instruction.replace("fold along ", "").split("=")
                    for instruction in instructions.splitlines()]
    return dots, instructions
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
