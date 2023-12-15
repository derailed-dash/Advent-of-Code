""" 
Author: Darren
Date: March 2023

A set of helper functions, reusable classes and attributes used by my AoC solutions 
Test with tests/test_aoc_commons.py

You can import as follows:
import aoc_common.aoc_commons as ac                           
"""
# py -m pip install requests python-dotenv
from __future__ import annotations
import contextlib
import copy
from dataclasses import asdict, dataclass
from enum import Enum
from functools import cache
import operator
import logging
import os
from pathlib import Path
import time
from dotenv import load_dotenv # python-dotenv
import requests
from colorama import Fore

##########################################################################
# SETUP LOGGING
#
# Create a new instance of "logger" in the client application
# Set to your preferred logging level
# And add the stream_handler from this module, if you want coloured output
##########################################################################

# logger for aoc_commons only
logger = logging.getLogger(__name__) # aoc_common.aoc_commons
logger.setLevel(logging.INFO)

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

if not logger.handlers:
    # Write to console with threshold of INFO
    stream_handler = logging.StreamHandler()
    stream_fmt = ColouredFormatter(fmt='%(asctime)s.%(msecs)03d:%(name)s - %(levelname)s: %(message)s', 
                                datefmt='%H:%M:%S')
    stream_handler.setFormatter(stream_fmt)
    logger.addHandler(stream_handler)

def retrieve_console_logger(script_name):
    """ Create and return a new logger, named after the script 
    So, in your calling code, add a line like this: 
    logger = ac.retrieve_console_logger(locations.script_name) 
    """
    a_logger = logging.getLogger(script_name)
    a_logger.addHandler(stream_handler)
    a_logger.propagate = False
    return a_logger
    
def setup_file_logging(a_logger: logging.Logger, folder: str|Path=""):
    """ Add a FileHandler to the specified logger. File name is based on the logger name.
    In calling code, we can add a line like this:
    td.setup_file_logging(logger, locations.output_dir)

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
    
def top_and_tail(data, block_size=5, include_line_numbers=True, zero_indexed=False):
    """ Print a summary of a large amount of data 

    Args:
        data (_type_): The data to present in summary form.
        block_size (int, optional): How many rows to include in the top, and in the tail.
        include_line_numbers (bool, optional): Prefix with line number. Defaults to True.
        zero_indexed (bool, optional): Lines start at 0? Defaults to False.
    """
    if isinstance(data, list):
        # Get the number of digits of the last item for proper alignment
        num_digits_last_item = len(str(len(data)))

        # Format the string with line number
        def format_with_line_number(idx, line):
            start = 0 if zero_indexed else 1
            if include_line_numbers:
                return f"{idx + start:>{num_digits_last_item}}: {line}"
            else:
                return line

        start = 0 if zero_indexed else 1
        if len(data) < 11:
            return "\n".join(format_with_line_number(i, line) for i, line in enumerate(data))
        else:
            top = [format_with_line_number(i, line) for i, line in enumerate(data[:block_size])]
            tail = [format_with_line_number(i, line) for i, line in enumerate(data[-block_size:], start=len(data)-block_size)]
            return "\n".join(top + ["..."] + tail)
    else:
        return data
    
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
    
def get_locations(script_file) -> Locations:
    """ Set various paths, based on the location of the calling script. """
    script_name = Path(script_file).stem   # this script file, without .py
    script_dir = Path(script_file).parent  # the folder where this script lives
    input_dir = Path(script_dir, "input")
    output_dir = Path(script_dir, "output")
    input_file = Path(input_dir, "input.txt")
    sample_input_file = Path(script_dir, "input/sample_input.txt")
    
    return Locations(script_name, script_dir, 
                     input_dir, 
                     output_dir, 
                     sample_input_file, input_file)

##################################################################
# Retrieving input data
##################################################################

def get_envs_from_file() -> bool:
    """ Look for .env files, read variables from it, and store as environment variables """
    potential_path = ".env"
    for _ in range(3):
        logger.debug("Trying .env at %s", os.path.realpath(potential_path))
        if os.path.exists(potential_path):
            logger.info("Using .env at %s", os.path.realpath(potential_path))
            load_dotenv(potential_path, override=True, verbose=True)
            return True
        
        potential_path = os.path.join('..', potential_path)
   
    logger.warning("No .env file found.")
    return False

get_envs_from_file() # read env variables from a .env file, if we can find one
    
def write_puzzle_input_file(year: int, day: int, locations: Locations) -> str:
    """ Use session key to obtain user's unique data for this year and day.
    Only retrieve if the input file does not already exist. 
    Raises a ValueError if unable to perform request.
    Requires env: AOC_SESSION_COOKIE, which can be set from the .env.
    Returns str:
      - input_file, if the file already exists
      - otherwise, the data retrieved from the request
    """
    if os.path.exists(locations.input_file):
        logger.debug("%s already exists", os.path.basename(locations.input_file))
        return os.path.basename(locations.input_file)

    session_cookie = os.getenv('AOC_SESSION_COOKIE')
    if not session_cookie:
        raise ValueError("Could not retrieve session cookie.")        
    
    logger.info('Session cookie retrieved: %s...%s', session_cookie[0:6], session_cookie[-6:])
    
    # Create input folder, if it doesn't exist
    if not locations.input_dir.exists():
        locations.input_dir.mkdir(parents=True, exist_ok=True)
    
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": session_cookie}
    response = requests.get(url, cookies=cookies, timeout=5)
    
    data = ""
    if response.status_code == 200:
        data = response.text
    
        with open(locations.input_file, 'w') as file:
            logger.debug("Writing input file %s", os.path.basename(locations.input_file))
            file.write(data)
            return data
    else:
        raise ValueError(f"Unable to retrieve input data.\n" +
                         f"HTTP response: {response.status_code}\n" +
                         f"{response.reason}: {response.content.decode('utf-8').strip()}")
       
#################################################################
# TESTING
#################################################################

def validate(test, answer):
    """
    Args:
        test: the answer given by our solution
        answer: the expected answer, e.g. from instructions
    """
    if test != answer:
        raise AssertionError(f"{test} != {answer}")

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
        self.array = grid_array
        self._width = len(self.array[0])
        self._height = len(self.array)
        
    def value_at_point(self, point: Point):
        """ The value at this point """
        return self.array[point.y][point.x]

    def set_value_at_point(self, point: Point, value):
        self.array[point.y][point.x] = value
        
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
        return ["".join(str(char) for char in row) for row in self.array]
        
    def cols_as_str(self):
        """ Render columns as str. Returns: list of str """
        cols_list = list(zip(*self.array))
        return ["".join(str(char) for char in col) for col in cols_list]

    def transpose(self) -> Grid:
        return Grid(list(zip(*self.array)))
    
    def flip_vertical(self) -> Grid:
        """ Flip the array about the vertical axis of symmetry """
        return Grid([row[::-1] for row in self.array])
    
    def flip_horizontal(self) -> Grid:
        """ Flip the array about the horizontal axis of symmetry """
        return Grid(self.array[::-1])
    
    def rotate_90(self, ccw=False) -> Grid:
        """ Rotates 90 degrees CW. It works by transposing, then flipping. """
        if ccw:
            flipped = self.flip_vertical()
        else:
            flipped = self.flip_horizontal()
    
        return flipped.transpose()
        
    def __repr__(self) -> str:
        return f"Grid(size={self.width}*{self.height})"
    
    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self.array)

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

def to_base_n(number: int, base: int):
    """ Convert any integer number into a base-n string representation of that number.
    E.g. to_base_n(38, 5) = 123

    Args:
        number (int): The number to convert
        base (int): The base to apply

    Returns:
        [str]: The string representation of the number
    """
    ret_str = ""
    curr_num = number
    while curr_num:
        ret_str = str(curr_num % base) + ret_str
        curr_num //= base

    return ret_str if number > 0 else "0"

@contextlib.contextmanager
def timer(description="Execution time"):
    """A context manager to measure the time taken by a block of code or function.
    
    Args:
    - description (str): A description for the timing output. 
      Default is "Execution time".
    """
    t1 = time.perf_counter()
    yield
    t2 = time.perf_counter()
    logger.info(f"{description}: {t2 - t1:.3f} seconds")
