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
import sys
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"


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


def paper_required(box):
    w = box[0]
    h = box[1]
    l = box[2]

    box_area = 2*(w*h+w*l+h*l)
    contingency_area = w*h

    return box_area + contingency_area


def ribbon_required(box):
    w = box[0]
    h = box[1]
    l = box[2]

    ribbon_length = 2*w + 2*h
    bow_length = w*h*l

    return ribbon_length + bow_length


def get_boxes(data):
    boxes = []

    p = re.compile(r"(\d+)x(\d+)x(\d+)")
    for line in data:
        # get list of dimensions
        dims = p.match(line).groups()
        # convert dims to int
        dims = list(map(int, dims))
        # sort and add to our boxes list
        boxes.append(sorted(dims))

    return boxes


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")