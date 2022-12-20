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
- We need to store 3 things: 
  - the original index -> number, so we can move the next number, wherever it is
  - the current index -> number, to keep track of where the number is now
- We need to track original position and current position for every number.
- Store the numbers in a circular_linked_list, because using a list or going to be slow for large datasets.

Part 2:

"""
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = list(map(int, f.read().splitlines()))
        
    print(data)
    
    # Store "pairs" as (val, original_index)
    curr_idx_to_pair = {i:(v,i) for i,v in enumerate(data)} # to find pair by index
    pair_to_curr_idx = {v:k for k,v in curr_idx_to_pair.items()} # to find the current index for a pair
    
    for i, val in enumerate(data): # process numbers in original order
        # E.g. 1, 3, 2, 5, 7, 9, with i=1 and val=3
        if val == 0:
            continue
        curr_idx = pair_to_curr_idx[(val, i)]
        if curr_idx + val <= 0:
            fudge = -1
        elif curr_idx + val > len(data):
            fudge = 1
        else:
            fudge = 0
        modulo_fudge = 1 if curr_idx + val <= 0 else 0
        displacement_idx = (curr_idx+val+fudge) % len(data) # idx=4, i.e. where 7 is. It can rollover
        print(f"Moving {val} from {curr_idx} to {displacement_idx}")
        
        displaced_pair = curr_idx_to_pair[displacement_idx] # grab the (4, 7)
        curr_idx_to_pair[displacement_idx] = curr_idx_to_pair[curr_idx] # move our value from idx 1 to idx 4
        
        # Now move everything in between down one
        for j in range(curr_idx+1, displacement_idx+1):
            pair_to_curr_idx[curr_idx_to_pair[j]] = j-1
            curr_idx_to_pair[j-1] = curr_idx_to_pair[j]
            
        # And finally, put the displaced pair back in the gap
        curr_idx_to_pair[displacement_idx-1] = displaced_pair
        pair_to_curr_idx[displaced_pair] = displacement_idx-1        
        
        print(f"{i+1}: {[val[0] for val in curr_idx_to_pair.values()]}")

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
