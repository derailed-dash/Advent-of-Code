"""
Author: Darren
Date: 18/12/2021

Solving https://adventofcode.com/2021/day/18

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

"""
from __future__ import annotations
from ast import literal_eval
import logging
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Node:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None
        self.par = None

    def __str__(self):
        if isinstance(self.val, int):
            return str(self.val)
        return f"[{str(self.left)},{str(self.right)}]"


def parse(fish_num):
    """
    Parse a big list into a tree
    """
    root = Node()
    if isinstance(fish_num, int):
        root.val = fish_num
        return root

    root.left = parse(fish_num[0])
    root.right = parse(fish_num[1])
    root.left.par = root
    root.right.par = root

    return root

def add(a, b):
    """
    Add two trees together
    """
    root = Node()
    root.left = a
    root.right = b
    root.left.par = root
    root.right.par = root
    reduce(root)
    return root


def magnitude(root):
    if isinstance(root.val, int):
        return root.val

    return 3 * magnitude(root.left) + 2 * magnitude(root.right)

def reduce(root):
    """
    Reduce a tree
    """
    done = True

    # Do a DFS through the tree
    stack = [(root, 0)]

    while len(stack) > 0:
        # A preorder traversal will have the right order
        node, depth = stack.pop()

        if node == None:
            continue

        condition = (node.left == None and node.right == None) or (
            node.left.val != None and node.right.val != None)

        if depth >= 4 and node.val == None and condition:
            # Go up the stack to find left node
            prev_node = node.left
            cur_node = node
            while cur_node != None and (cur_node.left == prev_node or cur_node.left == None):
                prev_node = cur_node
                cur_node = cur_node.par

            # Left node must exist
            if cur_node != None:

                # Now cur_idx has a left child; we go all the way down
                cur_node = cur_node.left
                while cur_node.val == None:
                    if cur_node.right != None:
                        cur_node = cur_node.right
                    else:
                        cur_node = cur_node.left

                # Update some values!
                cur_node.val += node.left.val

            # Go up the stack to find right node
            prev_node = node.right
            cur_node = node
            while cur_node != None and (cur_node.right == prev_node or cur_node.right == None):
                prev_node = cur_node
                cur_node = cur_node.par

            # Right node must exist
            if cur_node != None:

                # Now cur_idx has a left child; we go all the way down
                cur_node = cur_node.right
                while cur_node.val == None:
                    if cur_node.left != None:
                        cur_node = cur_node.left
                    else:
                        cur_node = cur_node.right

                # Update some values!
                cur_node.val += node.right.val

            # Final explode updates
            node.val = 0
            node.left = None
            node.right = None

            # Stop the DFS
            done = False
            break

        # DFS through the children
        stack.append((node.right, depth + 1))
        stack.append((node.left, depth + 1))

    # Look for splits later
    if not done:
        reduce(root)
        return

    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        if node == None:
            continue

        if node.val != None:
            # Split!
            assert node.left == None and node.right == None
            if node.val >= 10:
                node.left = Node(node.val//2)
                node.right = Node(node.val - (node.val//2))
                node.left.par = node
                node.right.par = node
                node.val = None

                done = False
                break

        stack.append(node.right)
        stack.append(node.left)

    # If not done, keep going
    if not done:
        reduce(root)
        
# Alright great
def get_mag(a, b):
    return magnitude(add(a, b))

def main():
    with open(INPUT_FILE, mode="rt") as f:
        # Each input line is a nested list. 
        # Use literal_eval to convert to Python lists.
        data = [literal_eval(line) for line in f.read().splitlines()]

    root = parse(data[0])
    i = 1
    while i < len(data):
        root = add(root, parse(data[i]))
        i += 1

    ans = magnitude(root)
    print(ans)    

    ans = 0
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j:
                continue

            a, b = parse(data[i]), parse(data[j])

            if get_mag(a, b) > ans:
                ans = get_mag(a, b)

    print(ans)
    

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
