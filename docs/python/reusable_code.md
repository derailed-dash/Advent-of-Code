---
title: Reusable Code 
---

## Page Contents

- [Motivation](#motivation)
- [type_defs.py](#type_defspy)
- [Unit Tests](#unit-tests)

## Motivation

In Advent of Code, it's common to need to do similar things over and over.  
In particular, many problems require working with coordinates, or with many points in a grid.
Rather than repeating the same code in each solution that requires these things, let's create a shared `type_defs.py` module for storing this reusable code.

## type_defs.py

In the module below, I've included a few useful things:

- A `Point` class
- A `Vectors` enumeration class
- A `VectorDicts` class, so that we can look up Vectors using keys like "`U`" or "`^`".
- A `Grid` class
- Useful functions that we [discussed previously](/python/useful_algorithms).

```python
""" 
Author: Darren
Date: March 2023

A set of reusable classes and attributes used by my AoC solutions 
Test with tests/test_type_defs.py

You could import as follows:
import common.type_defs as td                               
"""
from __future__ import annotations
import copy
from dataclasses import asdict, dataclass
from enum import Enum
from functools import cache
import operator
import logging
import os
from pathlib import Path
from colorama import Fore

#################################################################
# SETUP LOGGING
#################################################################

# Create a new instance of "logger" in the client application
# Set to your preferred logging level
# And add the stream_handler from this module, if you want coloured output
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ColouredFormatter(logging.Formatter):
    """ Custom Formater which adds colour to output, based on logging level """

    level_mapping = {"DEBUG": (Fore.BLUE, "DBG"),
                     "INFO": (Fore.GREEN, "INF"),
                     "WARNING": (Fore.YELLOW, "WRN"),
                     "ERROR": (Fore.RED, "ERR"),
                     "CRITICAL": (Fore.MAGENTA, "CRT")
    }
    
    def __init__(self, *args, apply_colour=True, shorten_lvl=True, **kwargs) -> None:
        """ Args:
            apply_colour (bool, optional): Apply colouring to messages. Defaults to True.
            shorten_lvl (bool, optional): Shorten level names to 3 chars. Defaults to True.
        """
        super().__init__(*args, **kwargs)
        self._apply_colour = apply_colour
        self._shorten_lvl = shorten_lvl 

    def format(self, record):
        if record.levelname in ColouredFormatter.level_mapping:
            new_rec = copy.copy(record)
            colour, new_level = ColouredFormatter.level_mapping[record.levelname]
            
            if self._shorten_lvl:
                new_rec.levelname = new_level
            
            if self._apply_colour:
                msg = colour + super().format(new_rec) + Fore.RESET
            else:
                msg = super().format(new_rec)
            
            return msg
        
        # If our logging message is not using one of these levels...
        return super().format(record)

# Write to console with threshold of INFO
stream_handler = logging.StreamHandler()
stream_fmt = ColouredFormatter(fmt='%(asctime)s.%(msecs)03d:%(name)s - %(levelname)s: %(message)s', 
                               datefmt='%H:%M:%S')
stream_handler.setFormatter(stream_fmt)
logger.addHandler(stream_handler)

def retrieve_console_logger(script_name):
    """ Create and return a new logger, named after the script """
    a_logger = logging.getLogger(script_name)
    a_logger.addHandler(stream_handler)
    a_logger.propagate = False
    return a_logger
    
def setup_file_logging(a_logger: logging.Logger, folder: str|Path=""):
    """ Add a FileHandler to the specified logger. File name is based on the logger name.

    Args:
        a_logger (Logger): The existing logger
        folder (str): Where the log file will be created. Will be created if it doesn't exist
    """
    Path(folder).mkdir(parents=True, exist_ok=True)     # Create directory if it does not exist
    file_handler = logging.FileHandler(Path(folder, a_logger.name + ".log"), mode='w')
    file_fmt = logging.Formatter(fmt="%(asctime)s.%(msecs)03d:%(name)s:%(levelname)8s: %(message)s", 
                                datefmt='%H:%M:%S')
    file_handler.setFormatter(file_fmt)
    a_logger.addHandler(file_handler)

#################################################################
# Paths and Locations
#################################################################

@dataclass
class Locations:
    """ Dataclass for storing various location properties """
    script_name: str
    script_dir: Path
    input_dir: Path
    output_dir: Path
    sample_input_file: Path
    input_file: Path
    
def get_locations(script_file):
    script_name = Path(script_file).stem   # this script file, without .py
    script_dir = Path(script_file).parent  # the folder where this script lives
    input_dir = Path(script_dir, "input")
    output_dir = Path(script_dir, "output")
    input_file = Path(input_dir, "input.txt")
    sample_input_file = Path(script_dir, "input/sample_input.txt")
    
    return Locations(script_name, script_dir, input_dir, output_dir, sample_input_file, input_file)

#################################################################
# POINTS, VECTORS AND GRIDS
#################################################################

@dataclass(frozen=True)
class Point:
    """ Class for storing a point x,y coordinate """
    x: int
    y: int
        
    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other: Point):
        """ (x, y) * (a, b) = (xa, yb) """
        return Point(self.x * other.x, self.y * other.y)
    
    def __sub__(self, other: Point):
        return self + Point(-other.x, -other.y)

    def yield_neighbours(self, include_diagonals=True, include_self=False):
        """ Generator to yield neighbouring Points """
        
        deltas: list
        if not include_diagonals:
            deltas = [vector.value for vector in Vectors if abs(vector.value[0]) != abs(vector.value[1])]
        else:
            deltas = [vector.value for vector in Vectors]
        
        if include_self:
            deltas.append((0, 0))
        
        for delta in deltas:
            yield Point(self.x + delta[0], self.y + delta[1])

    def neighbours(self, include_diagonals=True, include_self=False) -> list[Point]:
        """ Return all the neighbours, with specified constraints.
        It wraps the generator with a list. """
        return list(self.yield_neighbours(include_diagonals, include_self))
    
    def get_specific_neighbours(self, directions: list[Vectors]) -> list[Point]:
        """ Get neighbours, given a specific list of allowed locations """
        return [(self + Point(*vector.value)) for vector in list(directions)]
    
    @staticmethod
    def manhattan_distance(a_point: Point) -> int:
        """ Return the Manhattan distance value of this vector """
        return sum(abs(coord) for coord in asdict(a_point).values())     
        
    def manhattan_distance_from(self, other: Point) -> int:
        """ Manhattan distance between this Vector and another Vector """
        diff = self-other
        return Point.manhattan_distance(diff)  
        
    def __repr__(self):
        return f"P({self.x},{self.y})"

class Vectors(Enum):
    """ Enumeration of 8 directions.
    Note: y axis increments in the North direction, i.e. N = (0, 1) """
    N = (0, 1)
    NE = (1, 1)
    E = (1, 0)
    SE = (1, -1)
    S = (0, -1)
    SW = (-1, -1)
    W = (-1, 0)
    NW = (-1, 1)
    
    @property
    def y_inverted(self):
        """ Return vector, but with y-axis inverted. I.e. N = (0, -1) """
        x, y = self.value
        return (x, -y)

class VectorDicts():
    """ Contains constants for Vectors """
    ARROWS = {
        '^': Vectors.N.value,
        '>': Vectors.E.value,
        'v': Vectors.S.value,
        '<': Vectors.W.value
    }

    DIRS = {
        'U': Vectors.N.value,
        'R': Vectors.E.value,
        'D': Vectors.S.value,
        'L': Vectors.W.value
    }

    NINE_BOX: dict[str, tuple[int, int]] = {
        # x, y vector for adjacent locations
        'tr': (1, 1),
        'mr': (1, 0),
        'br': (1, -1),
        'bm': (0, -1),
        'bl': (-1, -1),
        'ml': (-1, 0),
        'tl': (-1, 1),
        'tm': (0, 1)
    }

class Grid():
    """ 2D grid of point values. """
    def __init__(self, grid_array: list) -> None:
        self._array = grid_array
        self._width = len(self._array[0])
        self._height = len(self._array)
        
    def value_at_point(self, point: Point) -> int:
        """ The value at this point """
        return self._array[point.y][point.x]

    def set_value_at_point(self, point: Point, value: int):
        self._array[point.y][point.x] = value
        
    def valid_location(self, point: Point) -> bool:
        """ Check if a location is within the grid """
        if (0 <= point.x < self._width and  0 <= point.y < self._height):
            return True
        
        return False

    @property
    def width(self):
        """ Array width (cols) """
        return self._width
    
    @property
    def height(self):
        """ Array height (rows) """
        return self._height
    
    def all_points(self) -> list[Point]:
        points = [Point(x, y) for x in range(self.width) for y in range(self.height)]
        return points

    def rows_as_str(self):
        """ Return the grid """
        return ["".join(str(char) for char in row) for row in self._array]
        
    def cols_as_str(self):
        """ Render columns as str. Returns: list of str """
        cols_list = list(zip(*self._array))
        return ["".join(str(char) for char in col) for col in cols_list]

    def __repr__(self) -> str:
        return f"Grid(size={self.width}*{self.height})"
    
    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._array)

#################################################################
# CONSOLE STUFF
#################################################################

def cls():
    """ Clear console """
    os.system('cls' if os.name=='nt' else 'clear')

#################################################################
# USEFUL FUNCTIONS
#################################################################

def binary_search(target, low:int, high:int, func, *func_args, reverse_search=False):
    """ Generic binary search function that takes a target to find,
    low and high values to start with, and a function to run, plus its args. 
    Implicitly returns None if the search is exceeded. """
    
    res = None  # just set it to something that isn't the target
    candidate = 0  # initialise; we'll set it to the mid point in a second
    
    while low < high:  # search exceeded        
        candidate = int((low+high) // 2)  # pick mid-point of our low and high        
        res = func(candidate, *func_args) # run our function, whatever it is
        logger.debug("%d -> %d", candidate, res)
        if res == target:
            return candidate  # solution found
        
        comp = operator.lt if not reverse_search else operator.gt
        if comp(res, target):
            low = candidate
        else:
            high = candidate
            
def merge_intervals(intervals: list[list]) -> list[list]:
    """ Takes intervals in the form [[a, b][c, d][d, e]...]
    Intervals can overlap.  Compresses to minimum number of non-overlapping intervals. """
    intervals.sort()
    stack = []
    stack.append(intervals[0])
    
    for interval in intervals[1:]:
        # Check for overlapping interval
        if stack[-1][0] <= interval[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], interval[-1])
        else:
            stack.append(interval)
      
    return stack

@cache
def get_factors(num: int) -> set[int]:
    """ Gets the factors for a given number. Returns a set[int] of factors. 
        # E.g. when num=8, factors will be 1, 2, 4, 8 """
    factors = set()

    # Iterate from 1 to sqrt of 8,  
    # since a larger factor of num must be a multiple of a smaller factor already checked
    for i in range(1, int(num**0.5) + 1):  # e.g. with num=8, this is range(1, 3)
        if num % i == 0: # if it is a factor, then dividing num by it will yield no remainder
            factors.add(i)  # e.g. 1, 2
            factors.add(num//i)  # i.e. 8//1 = 8, 8//2 = 4
    
    return factors
```

I've placed the module into a folder called `common`. So we can use it by importing like this:

```python
from common.type_defs import Point
```

Or, to import everything:

```python
import common.type_defs as td
```

Then we can do stuff like this:

```python
locations = td.get_locations(__file__)
logger = td.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
```

## Unit Tests

We talked about [unit testing](/python/unit_test) before.

Here I've created a test module, for testing the `type_defs.py` module:

```python
""" Testing the type_defs module """
import unittest
from os import path
from common.type_defs import (
    Point, 
    Grid, 
    Vectors, 
    VectorDicts, 
    binary_search, 
    merge_intervals,
    get_factors,
    get_locations
)

class TestTypes(unittest.TestCase):
    """ Unit tests of various classes in type_defs """
    
    def setUp(self):
        self.points = set()
        self.a_point = Point(5, 5)
        self.b_point = Point(1, 2)
        self.c_point = Point(6, 7)
        self.d_point = Point(4, 3)
        self.e_point = Point(3, 6)
        self.y_invert_point = Point(0, -1)
        
        self.points.add(self.a_point)
        self.points.add(self.b_point)  
        self.points.add(self.c_point)  
        self.points.add(self.d_point)  
        self.points.add(self.e_point)
        
        self.a_point_neighbours = self.a_point.neighbours()   
    
    def test_locations(self):
        locations = get_locations(__file__)
        
        # use normcase to un-escape and ignore case differences in the paths
        script_directory = path.normcase(path.dirname(path.realpath(__file__)))
        self.assertEqual(path.normcase(locations.script_dir), script_directory)
        
        this_script = path.splitext(path.basename(__file__))[0]
        self.assertEqual(locations.script_name, this_script)        

    def test_vectors(self):
        self.assertEqual(Vectors.N.value, (0, 1))
        self.assertEqual(Vectors.NW.value, (-1, 1))
        self.assertEqual(Vectors.S.value, (0, -1))
        self.assertEqual(Vectors.E.value, (1, 0))
        self.assertEqual(Vectors.N.y_inverted, (0, -1))
        self.assertEqual(Vectors.SW.value, (-1, -1))
        
    def test_vector_dicts(self):
        self.assertEqual(VectorDicts.ARROWS[">"], (1, 0))
        self.assertEqual(VectorDicts.ARROWS["v"], (0, -1))
        self.assertEqual(VectorDicts.DIRS["L"], (-1, 0))
        self.assertEqual(VectorDicts.DIRS["U"], (0, 1))
        self.assertEqual(VectorDicts.NINE_BOX["tr"], (1, 1))
        self.assertEqual(VectorDicts.NINE_BOX["bl"], (-1, -1))
        
    def test_point_arithmetic(self):
        self.assertEqual(self.a_point + self.b_point, self.c_point, "Asserting Point addition")
        self.assertEqual(self.a_point - self.b_point, self.d_point, "Asserting Point subtraction")
        self.assertEqual(self.b_point * Point(3, 3), self.e_point, "Asserting multiplication")
    
    def test_manhattan_distance(self):
        self.assertEqual(Point.manhattan_distance(self.e_point), 3+6)
        self.assertEqual(self.c_point.manhattan_distance_from(self.b_point), abs(self.a_point.x)+abs(self.a_point.y))
        
    def test_point_containers(self):
        all_neighbours_count = 8 # point has 8 neighbours
        diag_neighbours_count = 4 # point has 4 orthogonal neighbours

        self.assertEqual(len(self.a_point_neighbours), all_neighbours_count, 
                         f"Expect {all_neighbours_count} from all neighbours")
        
        a_point_diag_neighbours = self.a_point.neighbours(include_diagonals=False)
        self.assertEqual(len(a_point_diag_neighbours), diag_neighbours_count, 
                         f"Expect {diag_neighbours_count} orthogonal neighbours")
        self.assertNotIn(self.a_point, self.a_point.neighbours(), 
                         "Check neighbours does not include self")
        self.assertIn(self.a_point, self.a_point.neighbours(include_self=True), 
                         "Check neighbours includes self")
        self.assertEqual(len(self.a_point.neighbours(include_self=True)), all_neighbours_count+1, 
                         f"All neighbours with self should be {all_neighbours_count+1}")
        
    def test_point_neighbour_generator(self):
        gen = self.a_point.yield_neighbours()
        
        for _ in range(len(self.a_point_neighbours)):
            self.assertIn(next(gen), self.a_point_neighbours, "Generated item is a valid neighbour")
            
        with self.assertRaises(StopIteration): # no more items to generate
            next(gen)
            
    def test_grid(self):
        input_grid = ["5483143223",
                      "2745854711",
                      "5264556173",
                      "6141336146",
                      "6357385478",
                      "4167524645",
                      "2176841721"]
    
        input_array_data = [[int(posn) for posn in row] for row in input_grid]      
        grid = Grid(input_array_data)
        self.assertEqual(grid.height, len(input_grid))
        self.assertEqual(grid.width, len(input_grid[0]))
        self.assertTrue(grid.valid_location(Point(1, 1)))
        self.assertFalse(grid.valid_location(Point(11,8)))
        self.assertEqual(grid.value_at_point(Point(1, 1)), 7)
        self.assertEqual(grid.rows_as_str()[0], "5483143223")
        self.assertEqual(grid.cols_as_str()[0], "5256642")
      
    def test_binary_search(self):
        self.assertEqual(binary_search(225, 0, 20, lambda x: x**2, reverse_search=True), None)
        self.assertEqual(binary_search(225, 0, 20, lambda x: x**2), 15)
    
    def test_merge_intervals(self):
        pairs = [
            [1, 5],    # Non-overlapping pair
            [3, 7],    # Overlapping pair
            [8, 12],   # Non-overlapping pair
            [10, 15],  # Overlapping pair
            [18, 20]   # Non-overlapping pair
        ]
        
        expected = [[1, 7], [8, 15], [18, 20]]
        
        self.assertEqual(merge_intervals(pairs), expected)
        
    def test_get_factors(self):
        expected = {1, 2, 4, 8}
        self.assertEqual(get_factors(8), expected)
          
if __name__ == "__main__":
    unittest.main(verbosity=2)
```
