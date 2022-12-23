from __future__ import annotations
from collections import defaultdict
import re
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

with open(INPUT_FILE, mode="rt") as fh:
    s = fh.read()

mp, cmds = s.split('\n\n')
mp = mp.splitlines()
B = int((sum(c in '#.' for c in s ) / 6) ** .5)

imnj, jmni, imxj, jmxi = defaultdict(lambda: 10000), defaultdict(lambda: 10000), defaultdict(lambda: -1), defaultdict(lambda: -1)

for i, row in enumerate(mp):
    for j, c in enumerate(row):
        if c != ' ':
            imnj[i] = min(imnj[i], j)
            imxj[i] = max(imxj[i], j)
            jmni[j] = min(jmni[j], i)
            jmxi[j] = max(jmxi[j], i)

@dataclass(frozen=True)
class Point3D:
    x: int
    y: int
    z: int
    def __add__(self, other: Point3D):
        return Point3D(self.x+other.x, self.y+other.y, self.z+other.z)
    def __sub__(self, other: Point3D):
        return Point3D(self.x-other.x, self.y-other.y, self.z-other.z)
    def __matmul__(self, other: Point3D): # cross product
        return Point3D(self.y*other.z-self.z*other.y, self.z*other.x-self.x*other.z, self.x*other.y-self.y*other.x)
    def __mul__(self, k: int):
        return Point3D(self.x * k, self.y * k, self.z * k)
    def dot(self, other: Point3D):
        return self.x*other.x+self.y*other.y+self.z*other.z

faces = {}
edges = {}
def inb(i, j):
    return i >= 0 and i < len(mp) and j >= 0 and j < len(mp[i]) and mp[i][j] != ' '
def f(i: int, j: int, xyz: Point3D, di: Point3D, dj: Point3D):
    if not inb(i, j) or (i, j) in faces:
        return
    faces[(i, j)] = (xyz, di, dj)
    for r in range(B):
        edges[(xyz+di*r, di@dj)] = i+r, j
        edges[(xyz+di*r+dj*(B-1), di@dj)] = i+r, j+B-1
        edges[(xyz+dj*r, di@dj)] = i,j+r
        edges[(xyz+dj*r+di*(B-1), di@dj)] = i+B-1, j+r
    f(i+B, j, xyz+di*(B-1), di@dj, dj)
    f(i-B, j, xyz+di@dj*(B-1), dj@di, dj)
    f(i, j+B, xyz+dj*(B-1), di, di@dj)
    f(i, j-B, xyz+di@dj*(B-1), di, dj@di)

i0, j0 = 0, min(j for j, c in enumerate(mp[0]) if c == '.')
f(i0, j0, Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(0, 1, 0))

def step(part, x, i, j, di, dj):
    for _ in range(x):
        ii, jj, ddi, ddj = i + di, j + dj, di, dj
        if not inb(ii, jj):
            if part == 1:
                ii = ii if di == 0 else jmxi[j] if ii < jmni[j] else jmni[jj] if ii > jmxi[jj] else ii
                jj = jj if dj == 0 else imxj[i] if jj < imnj[i] else imnj[ii] if jj > imxj[ii] else jj
            else:
                xyz, di3, dj3 = faces[(i//B*B, j//B*B)]
                here = xyz + di3*(i%B) + dj3*(j%B)
                n = di3@dj3
                ii, jj = edges[(here, di3*-di+dj3*-dj)]
                _, di3, dj3 = faces[(ii//B*B, jj//B*B)]
                ddi, ddj = di3.dot(n), dj3.dot(n)
        if mp[ii][jj] == '#':
            break
        else:
            i, j, di, dj = ii, jj, ddi, ddj
    return i, j, di, dj

def run(part):
    i, j = i0, j0
    di, dj = 0, 1
    for cmd in re.finditer('[0-9]+|L|R', cmds):
        match cmd.group(0):
            case 'L':
                di, dj = -dj, di
            case 'R':
                di, dj = dj, -di
            case x:
                i, j, di, dj = step(part, int(x), i, j, di, dj)
    return 1000*(i+1)+4*(j+1)+[(0, 1), (1, 0), (0, -1), (-1, 0)].index((di, dj))

print(run(1))
print(run(2))
