"""
Modified from Jonathan Paulson's solution here:
https://github.com/jonathanpaulson/AdventOfCode/blob/master/2022/10.py

Very fast and efficient. It works by:
Only about 1/5 as many lines of code as my solution!
"""
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

with open(INPUT_FILE, mode="rt") as f:
    lines = f.read().splitlines()

G = [['?' for _ in range(40)] for _ in range(6)]
p1 = 0
reg_x = 1
tick = 0

def handle_tick(t, x):
    global p1
    global G
    t1 = t-1
    G[t1//40][t1%40] = ('#' if abs(x-(t1%40))<=1 else ' ')
    if t in [20, 60, 100, 140, 180, 220]:
        p1 += x*t

for line in lines:
    words = line.split()
    if words[0] == 'noop':
        tick += 1
        handle_tick(tick,reg_x)
    elif words[0] == 'addx':
        tick += 1
        handle_tick(tick,reg_x)
        tick += 1
        handle_tick(tick,reg_x)
        reg_x += int(words[1])

print(p1)

for r in range(6):
    print(''.join(G[r]))
