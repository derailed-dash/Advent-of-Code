"""
Author: Darren
Date: 13/12/2022

Solving https://adventofcode.com/2022/day/13

Input contains blocks, where each block is a pair.
Each 'packet' in the pair is a list or an int. Lists can contain other lists.
So clearly, recursion is going to be involved.

Part 1:

How many pairs are in the right order?

Soln:
- Read in each 'packet' using ast.literal_eval. This will automatically store as list or int.
- Create a Packet class that stores this item, and which implements __lt__ so that we can compare,
  according to the rules.
  - The __lt__() method compares self with other.
  - It is recursive: the base case is when we're comparing int values.
    Otherwise, we're either converting an int on one side to list and comparing, 
    or iterating over a list and comparing.
- Finally, for each pair, compare and count how many times L < R.

Part 2:

Ignore pairs.  Get ALL the packets. Add two special 'divider' packets.
Then put ALL the packets in the right order, find the 1-indexed index locations 
of the two divider packets, and return the product of these two indexes.

Soln:
- Our Item class is already sortable since we implemented __lt__().
- So, read in all items, sort, and find the dividers.
"""
from __future__ import annotations
from pathlib import Path
import time
from ast import literal_eval

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

class Packet():
    """ Sortable. Packet is made up of a value which is either a list or an int.
    Lists can contain other lists. """
    
    def __init__(self, value) -> None:
        self.value = value
        
    def __lt__(self, other: Packet) -> bool:
        # Base case - both are ints
        if isinstance(self.value, int) and isinstance(other.value, int):
            if self.value < other.value:
                return True 

            if other.value < self.value:
                return False

        # if one int and one list
        if isinstance(self.value, int) and isinstance(other.value, list):
            new_item = Packet([self.value]) # convert this int to list
            return new_item < other
        if isinstance(self.value, list) and isinstance(other.value, int):
            new_item = Packet([other.value]) # convert other int to list
            return self < new_item
        
        # both are lists
        if isinstance(self.value, list) and isinstance(other.value, list):
            # take each item and compare it. Zip will stop when it reaches the end of either list
            compare_count = 0
            for val in zip(self.value, other.value): 
                compare_count += 1
                if val[0] == val[1]:
                    continue # if the same, continue to next item
                
                return Packet(val[0]) < Packet(val[1])
            
            # If we're here, then the iterator terminated before finding a difference
            return len(self.value) < len(other.value)
        
    def __repr__(self) -> str:
        return str(self.value)
        
class Pair():
    """ Contains two items: left and right """
    def __init__(self, left: Packet, right: Packet) -> None:
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Pair(l={self.left}, r={self.right})"

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()

    # Part 1        
    pairs = get_pairs(data)
    right_order = []    
    for i, pair in enumerate(pairs, start=1):
        if pair.left < pair.right:
            right_order.append(i)
            
    print(f"Part 1 = {sum(right_order)}")
    
    # Part 2
    all_packets = get_all_packets(data)
    
    # Add divider packets, as required:
    div_two, div_six = Packet([[2]]), Packet([[6]])
    
    all_packets.append(div_two)
    all_packets.append(div_six)
    sorted_items = sorted(all_packets)
    loc_div_two = sorted_items.index(div_two) + 1
    loc_div_six = sorted_items.index(div_six) + 1
    print(f"Part 2 = {loc_div_two*loc_div_six}")

def get_pairs(data: str) -> list[Pair]:
    pairs: list[Pair] = []
    blocks = data.split("\n\n") # split into blocks
    
    for block in blocks:
        lines = block.splitlines()
        left = Packet(literal_eval(lines[0]))
        right = Packet(literal_eval(lines[1]))
        pair = Pair(left, right)
        pairs.append(pair)
        
    return pairs

def get_all_packets(data: str) -> list[Packet]:
    lines = data.splitlines()
    return [Packet(literal_eval(line)) for line in lines if line]

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
