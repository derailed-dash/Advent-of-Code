"""
Author: Darren
Date: 20/12/2022

Solving https://adventofcode.com/2022/day/20

We have encrypted coordinates we need to decrypt.
We have a long circular list of numbers.  We need to move each number forward a back. 
But we must move all the numbers in the original order.

Part 1:

Mix your encrypted file exactly once. What is the sum of the three numbers that form the grove coordinates?
(I.e. numbers at index 1000, 2000, 3000.)

Soln:

Part 2:

"""
from collections import deque
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

DECRYPTION_KEY = 811589153

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = list(map(int, f.read().splitlines()))
    
    # Part 1
    enumerated = deque(list(enumerate(data.copy())))  # deque of tuples of (original index, value)    
    enumerated = mix(enumerated)
    
    coord_sum = 0
    for n in (1000, 2000, 3000):
        # Turn our enumerated list into a list
        coord_sum += value_at_n([val[1] for val in enumerated], n)
    print(f"Part 1: {coord_sum}")
    
    # Part 2
    new_data = [val*DECRYPTION_KEY for val in data]
    enumerated = deque(list(enumerate(new_data)))  # new deque    
    for _ in range(10): # run the mix 10 times, but always with same enumeration (starting order)
        enumerated = mix(enumerated) 
        
    coord_sum = 0
    for n in (1000, 2000, 3000):
        coord_sum += value_at_n([val[1] for val in enumerated], n)
    print(f"Part 2: {coord_sum}")

def mix(enumerated: deque):
    """ Perform the mix algorithm on our enumerated deque of numbers """
    # Move each number once, using original indexes
    # We can't iterate over actual values from enumerated, since we'll be modifying it as we go
    for original_index in range(len(enumerated)): 
        while enumerated[0][0] != original_index: # bring our required element to the front
            enumerated.rotate(-1) 
    
        current_pair = enumerated.popleft()    
        shift = current_pair[1] % len(enumerated)  # allow for wrapping over
        enumerated.rotate(-shift) # if value n, we need to shift it n positions
        enumerated.append(current_pair)
        
        # print(enumerated)
        
    return enumerated
    
def value_at_n(values: list, n: int):
    """ Determine the value at position n in our list.
    If index is beyond the end, then wrap the values as many times as required. """
    digit_posn = (values.index(0)+n) % len(values)
    return values[digit_posn]

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
