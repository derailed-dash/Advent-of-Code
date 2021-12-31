"""
Author: Darren
Date: 23/12/2020

Solving: https://adventofcode.com/2020/day/23

Crab cups: cups, labelled with numbers, in a circle.
Three cups are picked up, clockwise of current cup.
They are placed clockwise of destination cup, which is selected based on rules.

Part 1:
Simulate 100 moves. What are the labels on all the cups after cup 1?

Part 2:
Pad out to a circle of 1000000 cups, using ascending numeric values.
Play 10000000 iterations.
What are the labels of the two cups clockwise of cup 1.

Solution:
    I've implemented a circular linked list.
    To make this scale for part 2, I implemented a dict to store value: node for every node, 
    making it fast to retrieve any node by value.  (Prevents traversing each time.)
"""
import os
import time
from circular_linked_list import Circular_Linked_List

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/data.txt"
SAMPLE_INPUT_FILE = "input/sample_data.txt"

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)
    data = read_input(input_file)

    # Part 1   
    cups = get_cups(data)
    cups = pad_cups(cups, 0)
    cups = list(play_game(cups, 100))

    cups_str_list = [str(x) for x in cups]
    posn_1 = cups_str_list.index('1')
    cups_str = ''.join(cups_str_list[posn_1+1:]) + ''.join(cups_str_list[:posn_1])
    print(f"Part 1: {cups_str}")

    # Part 2.  Takes a while...
    cups = get_cups(data)
    cups = pad_cups(cups, 1000000)
    cups = play_game(cups, 10000000)
    first_cup_after_1 = cups.get_node_after(1)
    second_cup_after_1 = cups.get_node_after(first_cup_after_1)

    print("Part 2:")
    print(f"The cups after 1 are: {first_cup_after_1} and {second_cup_after_1}")
    print(f"The product is: {first_cup_after_1*second_cup_after_1}")


def play_game(cups, iterations):
    iteration = 0
    list_size = cups.get_size()
    while iteration < iterations:
        iteration += 1
        #print(f"\nMove {iteration}")
        current_cup = cups.get_head()
        #print(f"Current cup: {current_cup}")

        # pop 3 clockwise
        pick_up = []
        for i in range(3):
            pick_up.append(cups.pop_after_value(current_cup))

        #print(f"Pick up: {pick_up}")
        #print(cups)

        # min is the lowest cup, excluding any cups in the pickup pile
        # only 3 in the pickup pile, so highest possible min value is 4
        for i in range(1, 5):
            if i not in pick_up:
                min_cup = i
                break

        # max is the highest cup, which is equivalent to the size of the list,
        # not including the 3 in the pickup pile.
        # So, lowest possible value for max is list_size-3
        for i in reversed(range(list_size-3, list_size+1)):
            if i not in pick_up:
                max_cup = i
                break

        destination_cup = current_cup-1
        if (destination_cup < min_cup):
            destination_cup = max_cup
        while (destination_cup in pick_up):
            destination_cup -= 1

        #print(f"Destination cup: {destination_cup}")

        for cup_val in reversed(pick_up):
            cups.insert_after_node(destination_cup, cup_val)

        cups.move_head_after_value(current_cup)
        #print(cups)

    return cups
    

def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read()

    return data


def get_cups(data):
    cups = Circular_Linked_List()
    for num in data:
        cups.insert_end(int(num))

    return cups


def pad_cups(cups, total_cups):
    for i in range(cups.get_size()+1, total_cups+1):
        cups.insert_end(i)

    return cups


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
