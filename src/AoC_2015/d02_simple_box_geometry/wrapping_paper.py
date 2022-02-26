""" 
Author: Darren
Date: 12/01/2021

Solving https://adventofcode.com/2015/day/2

Boxes given in axbxc format.

Part 1:
    Work out area of wrapping paper required, boxed on area of box + area of smallest side for contingency.

Part 2:
    Ribbon required is shortest distance around sides, i.e. smallest perimeter of any face
        + bow length b, where b = volume of box.
"""
from dataclasses import dataclass
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

@dataclass
class Box():
    """ Cuboid """
    width: int
    height: int
    length: int
    
    def __init__(self, dims: list) -> None:
        sorted_dims = sorted(dims)
        self.width = sorted_dims[0]
        self.height = sorted_dims[1]
        self.length = sorted_dims[2]
    
    @property
    def area(self):
        return 2*(self.width*self.height + self.width*self.length + self.height*self.length)
    
    @property
    def contingency(self):
        """ Contigency is the same as the area of the smallest face """
        return self.width * self.height
    

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.readlines()

    boxes = get_boxes(data)

    paper = sum(paper_required(box) for box in boxes)
    print(f"Paper required: {paper}")

    ribbon = sum(ribbon_required(box) for box in boxes)
    print(f"Ribbon required: {ribbon}")

def paper_required(box: Box):
    return box.area + box.contingency

def ribbon_required(box: Box):
    ribbon_length = 2*box.width + 2*box.height
    bow_length = box.width*box.height*box.length

    return ribbon_length + bow_length

def get_boxes(data) -> list[Box]:
    boxes = []

    p = re.compile(r"(\d+)x(\d+)x(\d+)")
    for line in data:
        if match := p.match(line):
            dims = list(map(int, match.groups())) # dims as list of int
            boxes.append(Box(dims))

    return boxes

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
