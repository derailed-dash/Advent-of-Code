"""
Author: Darren
Date: 25/12/2022

Solving https://adventofcode.com/2022/day/25

Determine the sum of the fuel requirements of all of the hot air balloons.
Numbers in the snafu system; it's base-5.
'2' = 2, '1' = 1, '0' = 0, '-' = -1, '=' = -2
So, 1=-0-2

Part 1:

Part 2:

"""
from pathlib import Path
import time
import string

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

convert = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    print(data)
    
    # convert rows from snafu to decimal
    totals = []
    for row in data:
        row_total = 0
        for posn, digit in enumerate(row, 1):
            row_total += 5**(len(row) - posn) * convert[digit]
        
        totals.append(row_total)
    
    total = sum(totals)
    print(f"Decimal total: {total}") # represent total as snafu
    
    base_5 = int_to_base(total, 5) # convert to base 5
    print(base_5)
    
    convert_num = total
    index = 0
    divisible = True
    while divisible:
        index += 1
        if (convert_num*2-1) // 5**index == 0:
            divisible = False
            
    print(index)
    
def int_to_base(int_num, base):
    """ Return base N representation for int n. """
    base_n_digits = string.digits + string.ascii_lowercase + string.ascii_uppercase
    result = ""
    while int_num > 0:
        q, r = divmod(int_num, base)
        result += base_n_digits[r]
        int_num = q
    if result == "":
        result = "0"
    return "".join(reversed(result))

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
