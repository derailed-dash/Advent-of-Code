"""
Author: Darren
Date: 01/12/2022

Solving https://adventofcode.com/2022/day/1

Part 1:

Part 2:

"""
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
# OUTPUT_FILE = Path(SCRIPT_DIR, "output/output.png")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().split("\n\n")
    
    print(data)
    elf_calories = []
    for elf in data:
        calories = sum(map(int, elf.splitlines()))
        elf_calories.append(calories)
        
    print(max(elf_calories))
    
    elf_calories = sorted(elf_calories)
    print(sum(elf_calories[-3:]))
    

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

