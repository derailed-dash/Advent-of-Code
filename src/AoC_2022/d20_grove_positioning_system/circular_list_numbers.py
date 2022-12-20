"""
Author: Darren
Date: 20/12/2022

Solving https://adventofcode.com/2022/day/20

We have encrypted coordinates we need to decrypt.
We have a long list of numbers.  We need to move each number forward a back. 
But we must move all the numbers in the original order.

Part 1:

Mix your encrypted file exactly once. What is the sum of the three numbers that form the grove coordinates?
(I.e. numbers at index 1000, 2000, 3000.)

Soln:
- We need to track original position and current position for every number.
- Store the numbers in a circular_linked_list, because using a list or going to be slow for large datasets.

Part 2:

"""
from pathlib import Path
import time
from circular_linked_list import CircularLinkedList

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = list(map(int, f.read().splitlines()))
        
    print(data)
    o_to_c_idx = [(i, val) for i, val in enumerate(data)] # we need unique objects that we can retrieve by original index
    print(o_to_c_idx)
    
    mixing = CircularLinkedList()
    for node in o_to_c_idx:
        mixing.insert_end(node)
        
    for node in o_to_c_idx: # now process in order
        retrieved = mixing.index(node)
        print(retrieved)
        # todo: pop

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
