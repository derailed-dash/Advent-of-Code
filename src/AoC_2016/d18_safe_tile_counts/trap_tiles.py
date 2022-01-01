"""
Author: Darren
Date: 09/09/2021

Solving https://adventofcode.com/2016/day/18

Safe tiles = .
Traps = ^
Arranged in fixed length rows.
Whether trap n in current row is safe depends 
on tile n (C), n-1 (L) and n+1 (R) in previous row.
Non-existent tiles count as safe.

Trap if:
    - L and C are traps AND R is safe.
    - C and R are traps AND L is safe.
    - L is trap; C and R are safe.
    - R is trap; C and L are safe.

Solution:
    Trivial.  Implement a function to execute the rule against tile n in row above.
    Use comprehension to get SAFE counts for each row.
    Then sum them.

Part 1:
    - Determine how many safe tiles for 40 rows
    
Part 2:
    - Determine how many safe tiles for 400000 rows
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

ROWS = 400000
TRAP = '^'
SAFE = '.'

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()
        
    logging.debug(f"Input: {data}")
    row_width = len(data)
    rows: list[str] = []
    rows.append(data)   # add first row
    
    for row_num in range(1, ROWS):
        last_row = rows[row_num-1]
        row_data = []
        for tile_posn in range(row_width):
            row_data.append(TRAP) if is_trap(tile_posn, last_row) else row_data.append(SAFE)
            
        rows.append("".join(row_data))
        
    safe_count = sum(row.count(SAFE) for row in rows)
    logging.info(f"Safe tiles count: {safe_count}")
            

def is_trap(position: int, last_row):
    """
    Position is TRAP if:
        - L and C are traps AND R is safe.
        - C and R are traps AND L is safe.
        - L is trap; C and R are safe.
        - R is trap; C and L are safe.ption]
    """
    tile_l = SAFE if position == 0 else last_row[position-1]
    tile_r = SAFE if position == len(last_row) - 1 else last_row[position+1]
    tile_c = last_row[position]
    
    if tile_l == TRAP and tile_c == TRAP and tile_r == SAFE:
        return True
    
    if tile_r == TRAP and tile_c == TRAP and tile_l == SAFE:
        return True
    
    if tile_l == TRAP and tile_c == SAFE and tile_r == SAFE:
        return True
    
    if tile_r == TRAP and tile_c == SAFE and tile_l == SAFE:
        return True
    
    return False        
    

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
