"""
Author: Darren
Date: 12/12/2020

Solving: https://adventofcode.com/2020/day/11

Modelling people sitting on seats.
If current seat is empty and no adjacent (or visible) seats are filled, the seat is filled.
If the seat is filled and n or more adjacent (or visible) seats are filled, the seat becomes empty.

Part 1
------
Looking for steady state using adjacent seats.

Part 2
------
Looking for steady state using 'visible' seats.

"""
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/seating.txt"
SAMPLE_INPUT_FILE = "input/sample_seating.txt"

EMPTY = 'L'
OCCUPIED = '#'
FLOOR = '.'

# each adjacent seat position, expressed as relative [row][seat]
SEATS_TO_TEST = {
    'UL': [-1, -1],
    'UM': [-1, 0],
    'UR': [-1, 1],
    'ML': [0, -1],
    'MR': [0, 1],
    'LL': [1, -1],
    'LM': [1, 0],
    'LR': [1, 1],
}

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)
    seating = read_input(input_file)
    # pp (seating)

    # part 1
    max_occupied = 4
    last_seating = seating
    count = 0
    while True:
        count += 1
        new_seating = process_seating_rules_adjacent(last_seating, max_occupied)

        if (new_seating == last_seating):
            print(f"Iteration {count}: Seating layout has not changed.")
            print(f"Seats occuped = {count_occupied(new_seating)}")
            break

        last_seating = new_seating        

    # part 2
    max_occupied = 5
    last_seating = seating
    count = 0
    while True:
        count += 1
        new_seating = process_seating_rules_line_of_sight(last_seating, max_occupied)

        if (new_seating == last_seating):
            print(f"Iteration {count}: Seating layout has not changed.")
            print(f"Seats occuped = {count_occupied(new_seating)}")
            break

        last_seating = new_seating    
    

def process_seating_rules_line_of_sight(seating, max_occupied):
    # if seat is empty and no adjacent seats are occupied, this becomes occupied
    # note: everyone sits at the same time, so we only need to consider seating plan at the start of the iteration
    # I.e. if the seat to the left is filled on *this* iteration, we ignore it.

    new_seating = seating.copy()

    for row_num, row in enumerate(seating):
        for seat_num, seat in enumerate(row):

            visible_occupied = 0

            if seat != FLOOR:

                # check each of the eight dimensions
                # iterate through UL, UM, UR, LL, etc
                for visible_seat in SEATS_TO_TEST.keys():
                    # set seat location to current seat
                    # then we'll move away from it, one x,y vector at a time
                    adjacent_seat_row_num = row_num
                    adjacent_seat_col_num = seat_num

                    counter = 0
                    while True:
                        counter += 1
                        adjacent_seat_row_num += SEATS_TO_TEST[visible_seat][0]
                        adjacent_seat_col_num += SEATS_TO_TEST[visible_seat][1]

                        if (adjacent_seat_row_num < 0 or adjacent_seat_row_num >= len(seating)):
                            break

                        if (adjacent_seat_col_num < 0 or adjacent_seat_col_num >= len(row)):
                            break

                        nearest_visible_seat = seating[adjacent_seat_row_num][adjacent_seat_col_num]
                        if (nearest_visible_seat) != FLOOR:
                            if (nearest_visible_seat == OCCUPIED):
                                visible_occupied += 1
                            
                            # we don't need to go any further in this dimension
                            break
                
                if seat == EMPTY:
                    if (visible_occupied == 0):
                        new_seating[row_num] = new_seating[row_num][:seat_num] + OCCUPIED + new_seating[row_num][seat_num+1:]
                elif seat == OCCUPIED:
                    if (visible_occupied >= max_occupied):
                        new_seating[row_num] = new_seating[row_num][:seat_num] + EMPTY + new_seating[row_num][seat_num+1:]

    # pp(new_seating)
    return new_seating


def count_occupied(seating):
    occupied_count = 0

    for row in seating:
        occupied_count += row.count(OCCUPIED)

    return occupied_count


def process_seating_rules_adjacent(seating, max_occupied):
    # if seat is empty and no adjacent seats are occupied, this becomes occupied
    # note: everyone sits at the same time, so we only need to consider seating plan at the start of the iteration
    # I.e. if the seat to the left is filled on *this* iteration, we ignore it.

    new_seating = seating.copy()

    for row_num, row in enumerate(seating):
        for seat_num, seat in enumerate(row):

            visible_occupied = 0

            if seat != FLOOR:
                # check each of the eight dimensions
                for visible_seat in SEATS_TO_TEST.keys():
                    # iterate through UL, UM, UR, LL, etc
                    adjacent_seat_row_num = row_num + SEATS_TO_TEST[visible_seat][0]
                    adjacent_seat_col_num = seat_num + SEATS_TO_TEST[visible_seat][1]

                    # check the seat we want to check is not out of bounds
                    if (adjacent_seat_row_num >= 0 and adjacent_seat_row_num < len(seating)):
                        if (adjacent_seat_col_num >= 0 and adjacent_seat_col_num < len(row)):
                            if (seating[adjacent_seat_row_num][adjacent_seat_col_num]) == OCCUPIED:
                                visible_occupied += 1
                
                if seat == EMPTY:
                    if (visible_occupied == 0):
                        new_seating[row_num] = new_seating[row_num][:seat_num] + OCCUPIED + new_seating[row_num][seat_num+1:]
                elif seat == OCCUPIED:
                    if (visible_occupied >= max_occupied):
                        new_seating[row_num] = new_seating[row_num][:seat_num] + EMPTY + new_seating[row_num][seat_num+1:]

    #pp(new_seating)
    return new_seating


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

