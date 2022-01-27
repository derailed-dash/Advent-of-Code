"""
Author: Darren
Date: 18/12/2021

Solving https://adventofcode.com/2021/day/18

Solution 2 of 2:
    This solution creates a binary tree from the input data.
    Much quicker than the str manipulation of solution 1.
    
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
    We parse the snailfish numbers and store as a binary tree.
    Top node is the root.  Every other node is associated with one parent.
    Each node can have only two children: left and right.
    
Part 2:
    We want the maximum magnitude from adding of any two input fish numbers.
    Simply add all permutations.
"""
from __future__ import annotations
from ast import literal_eval
from functools import reduce
from itertools import permutations
from collections import deque
import logging
from pathlib import Path
import time
from typing import Optional

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class FishNumber:
    """ A FishNumber is either a leaf node or a pair of FishNumbers """
    
    EXPLODE_BRACKETS = 4
    SPLIT_MIN = 10
    
    def __init__(self, val=None):
        """ Create a new FishNumber. 
        If val is an int, then this is a leaf, and left/right will be None. """
        self.val: Optional[int] = val  # leaf node value
        self.left: Optional[FishNumber] = None
        self.right: Optional[FishNumber] = None
        self.parent: Optional[FishNumber] = None
    
    def __str__(self):
        if isinstance(self.val, int):
            return str(self.val)
        
        assert isinstance(self.left, FishNumber) and isinstance(self.right, FishNumber)
        return f"[{str(self.left)},{str(self.right)}]" # print recursively
    
    def __repr__(self):
        msg = str(self.val) if isinstance(self.val, int) else f"[{str(self.left)},{str(self.right)}]"           
        return msg if self.parent else "FishNumber(" + msg + ")"

    def magnitude(self):
        """ Magnitude is given by 3*LHS + 2*RHS for any pair of values. 
        If the values are themselves lists, we must recurse.
        If the values are themselves ints, we return the int value. """
        if isinstance(self.val, int):
            return self.val

        assert self.left and self.right, "Must have children"
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()
    
    def fish_reduce(self):
        """ Reduce a FishNumber 
        - Explode any pairs that are more than four deep.
          Repeat explode until no more explosions possible.
        - Split any numbers that are > 10.
          Repeat split until no more splits are possible. """
        
        still_reducing = True
        while still_reducing:
            still_reducing = False  # assume nothing more to do
            
            # DFS through the tree, starting at the root, to see if we have pairs to explode
            stack = deque()
            stack.append((self, 0))    # (tree, depth)
            while len(stack) > 0:
                node, depth = stack.pop()

                # If we're at sufficient depth and this we're dealing with a pair
                if depth >= FishNumber.EXPLODE_BRACKETS and node.val is None:
                    self._explode(node)
                    still_reducing = True
                    break   # we've just exploded, so start loop again

                # otherwise, add children to the DFS frontier, ensuring left is always popped first
                if node.right and node.left: 
                    stack.append((node.right, depth + 1))
                    stack.append((node.left, depth + 1))

            if still_reducing:   # We've just exploded
                continue  # So loop
            
            # No explosions, so now try splitting
            assert not still_reducing, "Done exploding"
            assert len(stack) == 0, "Stack should be empty"
            stack.append(self)    # Add root node. We don't care about depth now.
            while len(stack) > 0:
                node = stack.pop()
                if node.val is not None:    # we've found our leaf
                    assert node.left is None and node.right is None
                    if node.val >= FishNumber.SPLIT_MIN:
                        self._split(node)
                        still_reducing = True
                        break   # back to the top
                else:   # not a leaf node, so must have children
                    stack.append(node.right)
                    stack.append(node.left)

    def _split(self, node):
        """ Split a single value into a pair of two halves.
        (Rounding down on the left, and rounding up on the right.)
        The current node becomes the parent of new left/right nodes. """
        assert node.val >= 10, "We can only split numbers >= 10"
        
        node.left = FishNumber(node.val//2) # new left val
        node.right = FishNumber(node.val - (node.val//2)) # new right val
        node.left.parent = node   # left node parent is current node
        node.right.parent = node  # right node parent is current node
        node.val = None  # current node value is cleared

    def _explode(self, node: FishNumber):
        """ Split a pair. The node passed to this method itself contains a pair of leaf values.
        Left node value is added to first value on the left, if there is one.
        Right node value is added to first value on the right, if there is one.
        Current node value is then set to 0. 

        Args: node ([FishNumber]): The node containing a pair we need to explode
        """
        
        # First explode the left side
        prev_node = node.left
        current_node = node  # the parent of our pair of leaf values
        
        # Move UP the tree until we identify a node with a left (different) child
        # or until we can go no further
        while (current_node is not None and 
               (current_node.left == prev_node or current_node.left is None)):
            prev_node = current_node  # prev node moves up one
            current_node = current_node.parent  # current node now points to parent

        # Current node will be None if we previously reached the root from the left.
        # Otherwise, we must have identified a left node, so come back DOWN the left
        if current_node is not None:
            assert current_node.left is not None, "There must be a left node"
            current_node = current_node.left
            while current_node.val is None: # must have two children; keep going down until we reach a leaf
                if current_node.right is not None:
                    current_node = current_node.right   # if there's a number on the right of this node, it's nearest
                else:
                    current_node = current_node.left

            assert current_node.val is not None, "We've reached the value on the left"
            current_node.val += node.left.val   # add to the left

        # Now explode the right side
        prev_node = node.right
        current_node = node
        
        # traverse up the tree until we identify a node with a right (different) child
        # or until we can go no further
        while (current_node is not None and 
                (current_node.right == prev_node or current_node.right is None)):
            prev_node = current_node
            current_node = current_node.parent

        # current node will be null if we previously reached the root (so no right value)
        # otherwise, we must have identified a right node, so come back down the right
        if current_node is not None: 
            current_node = current_node.right
            while current_node.val is None:
                if current_node.left is not None:
                    current_node = current_node.left
                else:
                    current_node = current_node.right

            current_node.val += node.right.val  # add to the right

        # Final explode updates - set original node value to 0 and clear the children
        node.val = 0 
        node.left = None
        node.right = None

    @staticmethod
    def parse(parse_input: list|int) -> FishNumber:
        """ Parse a list and convert to a FishNumber. 
        Recurses any nested lists, including leaf values. """
        node = FishNumber()
        if isinstance(parse_input, int):   # If a leaf node with no children
            node.val = parse_input
            return node

        assert len(parse_input) == 2, "Must be a pair in a list"
        node.left = FishNumber.parse(parse_input[0])
        node.right = FishNumber.parse(parse_input[1])
        node.left.parent = node
        node.right.parent = node

        return node

def add(left_tree: FishNumber, right_tree: FishNumber) -> FishNumber:
    """ Add two FishNumbers together.
    Creates a new parent node, with the supplied left and right set to its children. """
    new_root = FishNumber()
    
    new_root.left = left_tree
    new_root.right = right_tree
    new_root.left.parent = new_root
    new_root.right.parent = new_root
    
    new_root.fish_reduce()  # Note that this modifies the original supplied FishNumbers
    return new_root

def main():
    with open(INPUT_FILE, mode="rt") as f:
        # Each input line is a nested list. 
        # Use literal_eval to convert each to a Python list.
        data = [literal_eval(line) for line in f.read().splitlines()]
        
    # Part 1 - Sum all numbers and report magnitude
    result = reduce(add, map(FishNumber.parse, data))  # Reduce to add n to n+1, then to n+2, etc
    logger.info("Result = %s", result)
    logger.info("Part 1 magnitude = %d", result.magnitude())
    
    # Part 2
    mags = []
    for perm in permutations(data, 2): # All permutations of 2 fish numbers
        # Quicker to parse the input data each time than deepcopy a FishNumber
        result = add(FishNumber.parse(perm[0]), FishNumber.parse(perm[1]))
        mags.append(result.magnitude())
        
    logger.info("Part 2: max magnitude = %d", max(mags))

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
