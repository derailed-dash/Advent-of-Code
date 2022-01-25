"""
Author: Darren
Date: 18/12/2021

Solving https://adventofcode.com/2021/day/18

Solution 1 of 2:
    This solution works, but is a bit slow due to all the string manipulation.

We need to help the snailfish with their homework.
Snailfish numbers are always pairs, where each element is either an int or a nested pair.
E.g. [1,2] - the simplest snailfish number
E.g. [9,[8,7]] - a pair, where left is a number, and right is a nested pair.

We must 'add' a bunch of snailfish numbers, where each number is a line in the input.
To add snailfish numbers, first concatenate the two lists, and then perform 'reduction'.

Reduction:
    1 If any pair nested in 4 pairs, leftmost pair explodes.
    2 If any regular number is >=10, leftmost regular number splits.
    
    - Repeat first action that applies, until no action applies.
    - Only perform one explode/split per iteration.
    - Assume we never start with a pair more than 5 deep.

Exploding removes an inner bracket and adds the inner numbers to either side:
    - Add x to first avail number on the left (if there is one)
    - Add y to first avail number on the right (if there is one)
    - Then, replace the original pair (and its brackets) with 0.
    - This has the result of reducing the overall list depth by 1.

Splitting creates a bracketed pair (x,y) from a regular number:
    - Essentially, it splits an int into a pair (x,y) of two halves:
      x = math.floor(n/2), y = math.ceil(n/2)
    - This adds a new pair with a depth of n+1.

Part 1:
    Here we need to add up all the numbers in the input data, 
    and return the resulting magnitude.
    
    Magnitude of any pair |x,y| = 3*|x| + 2|y|
    Magnitude of any int x is simply x.
    
    Add line 1 to line 2, evaluate, then reduce with line 3, etc.
    
    Create a FishNumber class to store the fish number as a list.
    Use literal_eval to read in the list and store as Python list.
    Use functools.reduce() to add all the lines in the input data, one pair at a time.
    Explode logic works by counting brackets, and some regex.
    Split logic works by regex to look for numbers with > 1 char.
    
Part 2:
    Here we need to add up all permutations of pairs of the input data,
    and return the largest magnitude.
    
    Just use itertools.permutations (since not commutative so we can't use combinations).
    Then add each pair, work out the magnitude, and return the largest. Easy!
"""
from __future__ import annotations
import logging
from pathlib import Path
import time
import re
from functools import reduce
from math import ceil, floor
from itertools import permutations
from ast import literal_eval

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class FishNumber():
    """ FishNumber stores a snailfish number internally.
    This class knows how to:
    - Add two FishNumbers to create a new FishNumber. 
    - Reduce snailfish numbers according to rules. """
    
    EXPLODE_BRACKETS = 4
    SPLIT_MIN = 10
    
    def __init__(self, fish_list: list) -> None:
        self._number = fish_list # internal representation as a list
         
    @property
    def number(self):
        return self._number

    @staticmethod
    def magnitude(fish_num) -> int:
        """ Magnitude is given by 3*LHS + 2*RHS for any pair of values. 
        If the values are themselves lists, we must recurse.
        If the values are themselves ints, we return the int value. 
        If the value is not part of a pair, simply return the value. """
        mag = 0
        
        # First check if this is a pair (list)
        if isinstance(fish_num, list):
            mag = 3*FishNumber.magnitude(fish_num[0]) + 2*FishNumber.magnitude(fish_num[1])
        elif isinstance(fish_num, int): # must be a single value
            mag = fish_num
    
        return mag  
   
    def add(self, other: FishNumber) -> FishNumber:
        """ Creates a new FishNumber by concatenating two FishNumbers.
        Effectively, this is list extension. """
        return FishNumber([self.number] + [other.number])
        
    def reduce(self):
        """ Performs 'reduction' logic. I.e. explode and split, as required. """
        while True:
            if self._can_explode():
                self._number = self._explode()
            elif self._can_split():
                self._number = self._split()
            else:
                break        
    
    def _can_explode(self) -> bool:
        """ Checks if we can explode by counting brackets. """
        str_repr = str(self._number)
        depth_count = 0
        for char in str_repr:
            if char == "[":
                depth_count += 1
                
            if char == "]":
                depth_count -= 1
                
            if depth_count > FishNumber.EXPLODE_BRACKETS:
                return True
        
        return False

    def _explode(self) -> list:
        """ Explodes the current list.
        Looks for first opening bracket that is sufficiently nested. Takes the pair of digits within.  
        Adds LH to first digit on the left. (If there is one.)
        Adds RH to the first digit on the right. (If there is one.)
        Then replaces the entire bracket with 0. """
        
        str_repr = str(self._number)    # convert list to str
        
        depth_count = 0
        for i, char in enumerate(str_repr):
            if char == "[":
                depth_count += 1
                
            if char == "]":
                depth_count -= 1
                
            if depth_count > FishNumber.EXPLODE_BRACKETS:
                assert str_repr[i+1].isdigit(), "Should have been a digit here"
                left_bracket_posn = i
                comma_posn = i+1 + str_repr[i+1:].find(",")
                right_bracket_posn = comma_posn + str_repr[comma_posn:].find("]")
                
                left_num = int(str_repr[i+1: comma_posn])
                right_num = int(str_repr[comma_posn+1:right_bracket_posn])
                
                # process left of pair
                # This regex looks for the first matching digits at the end
                if match := re.match(r".*\D+(\d+).*$", str_repr[:left_bracket_posn]):
                    # match first group, i.e. (\d+)
                    num_start, num_end = match.span(1)[0], match.span(1)[1]
                    new_num = int(str_repr[num_start:num_end]) + left_num
                    
                    # We might be inserting a bigger number
                    l_increase = len(str(new_num)) - (num_end-num_start)            
                    str_repr = str_repr[:num_start] + str(new_num) + str_repr[num_end:]
                    
                    left_bracket_posn += l_increase
                    comma_posn += l_increase
                    right_bracket_posn += l_increase
                    
                # process right of pair
                if match := re.search(r"\d+", str_repr[right_bracket_posn:]):
                    # match whole group
                    num_start = right_bracket_posn + match.span(0)[0]
                    num_end = right_bracket_posn + match.span(0)[1]
                    new_num = int(str_repr[num_start:num_end]) + right_num
                    str_repr = str_repr[:num_start] + str(new_num) + str_repr[num_end:]
                
                # replace the original pair with 0
                str_repr = str_repr[:left_bracket_posn] + "0" + str_repr[right_bracket_posn+1:]
                
                break
        
        new_num = literal_eval(str_repr)    # convert back to list
        return new_num
    
    def _can_split(self) -> bool:
        """ We can split if there is a number >= 10 """
        str_repr = str(self._number)
        if re.search(r"(\d{2,})", str_repr):
            return True
        
        return False
        
    def _split(self) -> list:
        """ Split our fish number by taking the first n >= 10,
        and replacing with [floor(n/2), ceil(n/2)] """
        str_repr = str(self._number)
        if match := re.search(r"(\d{2,})", str_repr):
            num = int(match.groups()[0])
        
            if (num >= FishNumber.SPLIT_MIN):
                new_left_num = floor(num/2)
                new_right_num = ceil(num/2)
                new_str = "[" + str(new_left_num) + ", " + str(new_right_num) + "]"
                str_repr = re.sub(r"(\d{2,})", new_str, str_repr, count=1)

            new_num = literal_eval(str_repr)     # convert back to list
            return new_num
        
        assert False, "We should never get here since we're checking if we can split"
        return []
    
    def __repr__(self) -> str:
        return str(self.number)

def main():
    with open(INPUT_FILE, mode="rt") as f:
        # Each input line is a nested list. 
        # Use literal_eval to convert to Python lists.
        data = [FishNumber(literal_eval(line)) for line in f.read().splitlines()]
    
    # Part 1
    result = reduce(fish_add, data)  # Reduce to add n to n+1, then the sum to n+2, etc
    logger.info("Result = %s", result)
    mag = FishNumber.magnitude(result.number)
    logger.info("Part 1 magnitude = %d", mag)
    
    # Part 2
    mags = []
    for perm in permutations(data, 2): # All permutations of 2 fish numbers
        result = fish_add(perm[0], perm[1])
        mags.append(FishNumber.magnitude(result.number))
        
    logger.info("Part 2: max magnitude = %d", max(mags))    
    
def fish_add(left: FishNumber, right: FishNumber) -> FishNumber:
    """ Create new FishNumber by concatenating left and right
    Then reduce the resulting number and return it """
    
    new_fish_num = left.add(right)
    new_fish_num.reduce()
    return new_fish_num        

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
