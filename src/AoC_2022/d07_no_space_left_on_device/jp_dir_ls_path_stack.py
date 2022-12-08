"""
Modified from Jonathan Paulson's solution here:
https://github.com/jonathanpaulson/AdventOfCode/blob/master/2022/7.py

Very fast and efficient. It works by:
- Tracking current path using a stack (implemented using a list)
- When we cd into a folder, we add it to the stack.
- When we "cd ..", we pop.
- When we "ls", we just add the sz of all the files to THIS directory,
  but also to EVERY folder above it. Use a defaultdict to make that easy.
  The dict stores folder path:sz.
"""
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

with open(INPUT_FILE, mode="rt") as f:
    lines = f.read().splitlines()

# Store every single path, and the size of that directory
# directory path -> total size of that directory (including subdirectories)
path_to_sz = defaultdict(int)

# list to store current path as a set of elements.  
# We'll add and pop from this to track current position
current_path = []
for line in lines:
    words = line.strip().split()
    if words[1] == 'cd':
        if words[2] == '..':
            current_path.pop()
        else: # cd <some_dir>
            current_path.append(words[2])
    elif words[1] == 'ls':
        continue    # move on to next line, which will be ls listing
    elif words[0] == 'dir':
        continue    # we're only interesting in adding up files
    else: # we're looking at a file in a listing
        file_sz = int(words[0])
        # Add this file's size to the current directory size *and* the size of all parents
        for i in range(1, len(current_path)+1):
            # Store path using "/" separators
            # Note, the root will appear as "//"
            path_to_sz['/'.join(current_path[:i])] += file_sz

MAX_USED = 70000000 - 30000000
total_used = path_to_sz['/']
need_to_free = total_used - MAX_USED

p1 = 0
p2 = 1e9
for directory, dir_sz in path_to_sz.items():
    # print(k,v)
    if dir_sz <= 100000:
        p1 += dir_sz
    if dir_sz >= need_to_free:
        p2 = min(p2, dir_sz)
print(p1)
print(p2)
