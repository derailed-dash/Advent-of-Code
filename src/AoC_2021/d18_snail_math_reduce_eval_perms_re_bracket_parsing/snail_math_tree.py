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
        """ Create a new FishNumber """
        self.val = val  # leaf node value
        self.left: FishNumber = None
        self.right: FishNumber = None
        self.parent = None
    
    def __repr__(self):
        if isinstance(self.val, int):
            return str(self.val)
        
        assert isinstance(self.left, FishNumber) and isinstance(self.right, FishNumber)
        return f"[{str(self.left)},{str(self.right)}]" # print recursively
    
    def magnitude(self):
        """ Magnitude is given by 3*LHS + 2*RHS for any pair of values. 
        If the values are themselves lists, we must recurse.
        If the values are themselves ints, we return the int value. 
        If the value is not part of a pair, simply return the value. """
        if isinstance(self.val, int):
            return self.val

        return 3 * self.left.magnitude() + 2 * self.right.magnitude()
    
    def fish_reduce(self):
        """ Reduce a FishNumber """
        
        done = False
        while not done:
            done = True
            
            # DFS through the tree
            stack: deque[tuple[FishNumber, int]] = deque()
            stack.append((self, 0))    # (tree, depth)

            while len(stack) > 0:
                # A preorder traversal will have the right order
                node, depth = stack.pop()

                if node is None:
                    continue

                condition = ((node.left is None and node.right is None) or 
                            (node.left.val is not None and node.right.val is not None))

                if depth >= FishNumber.EXPLODE_BRACKETS and node.val is None and condition:
                    self._explode(node)
                    done = False
                    break

                # DFS through the children
                stack.append((node.right, depth + 1))
                stack.append((node.left, depth + 1))

            if not done:   # We've just exploded
                continue
            
            # No explosions, so now try splitting
            assert done, "Done exploding"

            stack: deque[tuple[FishNumber]] = deque()
            stack.append(self)    # We don't care about depth now
            while len(stack) > 0:
                node = stack.pop()
                if node is None:
                    continue

                if node.val is not None:
                    assert node.left is None and node.right is None
                    if node.val >= FishNumber.SPLIT_MIN:
                        self._split(node)
                        done = False
                        break

                stack.append(node.right)
                stack.append(node.left)

    def _split(self, node):
        node.left = FishNumber(node.val//2)
        node.right = FishNumber(node.val - (node.val//2))
        node.left.parent = node
        node.right.parent = node
        node.val = None

    def _explode(self, node):
        # Go up the stack to find left node
        prev_node = node.left
        current_node = node
        while (current_node is not None and 
               (current_node.left == prev_node or current_node.left is None)):
            prev_node = current_node
            current_node = current_node.parent

        if current_node is not None:   # Left node must exist
            # Now cur_idx has a left child; we go all the way down
            current_node = current_node.left
            while current_node.val is None:
                if current_node.right is not None:
                    current_node = current_node.right
                else:
                    current_node = current_node.left

            current_node.val += node.left.val

        # Go up the stack to find right node
        prev_node = node.right
        current_node = node
        while current_node is not None and (current_node.right == prev_node or current_node.right is None):
            prev_node = current_node
            current_node = current_node.parent

        if current_node is not None: # Right node must exist
            # Now cur_idx has a left child; we go all the way down
            current_node = current_node.right
            while current_node.val is None:
                if current_node.left is not None:
                    current_node = current_node.left
                else:
                    current_node = current_node.right

            current_node.val += node.right.val

        # Final explode updates
        node.val = 0
        node.left = None
        node.right = None

    @staticmethod
    def parse(fish_num: list|int) -> FishNumber:
        """ Parse a list into a FishNumber. Recurses any nested lists, including leaf values. """
        root = FishNumber()
        if isinstance(fish_num, int):   # if a leaf node with no children
            root.val = fish_num
            return root

        root.left = FishNumber.parse(fish_num[0])
        root.right = FishNumber.parse(fish_num[1])
        root.left.parent = root
        root.right.parent = root

        return root

def add(left_tree: FishNumber, right_tree: FishNumber) -> FishNumber:
    """ Add two FishNumbers together """
    new_root = FishNumber()
    
    # These deep copies slow it down a lot
    new_root.left = left_tree
    new_root.right = right_tree
    new_root.left.parent = new_root
    new_root.right.parent = new_root
    
    new_root.fish_reduce()
    return new_root

def main():
    with open(INPUT_FILE, mode="rt") as f:
        # Each input line is a nested list. 
        # Use literal_eval to convert each to a Python list.
        data = [literal_eval(line) for line in f.read().splitlines()]
        
    # Part 1 - Sum all numbers and report magnitude
    result = reduce(add, map(FishNumber.parse, data))  # Reduce to add n to n+1, then the sum to n+2, etc
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
