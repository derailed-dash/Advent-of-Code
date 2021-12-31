"""
Author: Darren
Date: 14/12/2020

Solving: https://adventofcode.com/2020/day/14

Part 1
------
Apply 36-bit mask to values, and then write values to memory.
E.g.
mask = 000000000000000000000000000000X1001X
mem[42] = 100

X values do not not modify the value, whilst 0 or 1 in the mask overwrite corresponding bit.
Mask:   00X1001X
Val:    01100100 (100)

Apply:  00110010 (50)

Sum the written memory addresses.

Part 2
------
Mask doesn't update values before writing to memory. 
Instead, mask updates the memory address to be written.
    If the bitmask bit is 0, the corresponding memory address bit is unchanged.
    If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
    If the bitmask bit is X, the corresponding memory address bit is floating.
        Floating bits can be both 1 and 0.
"""
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__)
INPUT_FILE = "input/docking_program.txt"
SAMPLE_INPUT_FILE = "input/sample_docking_program.txt"

ADDR_SIZE = 36
INSTR_PATTERN = re.compile(r"mem\[(\d+)")


def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input = read_input(input_file)
    
    v1_mem_values, updated_addresses = process_input(input)
    # pp(v1_mem_values)
    sum_of_values = sum(v1_mem_values.values())
    print(f"Sum of v1 mem values = {sum_of_values}")

    sum_of_updated_addresses = sum(updated_addresses.values())
    print(f"Sum of v2 updated address values = {sum_of_updated_addresses}")


def process_input(data):
    INSTR_MASK = "mask"

    v1_mem_values = {}
    updated_addresses = {}
    current_mask = None

    for line in data:
        instr, value = [x.strip() for x in line.split("=")]
        if (instr == INSTR_MASK):
            current_mask = value
            #pp(current_mask)
        else:
            addr, new_val = process_mem_update_v1(instr, value, current_mask)
            v1_mem_values[addr] = new_val

            updated_addresses.update(process_mem_update_v2(instr, value, current_mask))

    return v1_mem_values, updated_addresses


def convert_to_bin_rep(addr):
    int_addr = int(addr)

    # get a str binary representation that's 36 chars long
    return format(int_addr, "036b")


def process_mem_update_v2(instr, value, mask):
    # Modify the address being written to, using a mask
    # Multiple addresses can be defined by a single mask

    # Regex to extract the supplied memory address
    addr = int(INSTR_PATTERN.findall(instr)[0])

    # First, get binary equivalent of address supplied.
    # bin converts to binary STR equivalent, prefixed with 0b. Strip off 0b
    bin_addr = bin(addr)[2:]
    bin_addr_list = list(bin_addr.zfill(36))
    # print(f"Addr: {addr}, {bin_addr}")

    # placeholder for masked address
    intermediate_addr = ADDR_SIZE * ["0"]

    # This is the easy bit.
    # zip creates tuples from mask and addr. 
    # (Doesn't matter that mask is a str and bin_addr_list is a list.)
    # E.g. if mask[0] is X and bin_addr_list[0] is 0, then the zip is ('X', '0')
    # These are then unpacked into mark_char and addr_char
    for i, (mask_char, addr_char) in enumerate(zip(mask, bin_addr_list)):
        if (mask_char == 'X'):
            # intermediate address includes our floating X
            intermediate_addr[i] = 'X'
        elif (mask_char == '1'):
            # intermediate address set to 1
            intermediate_addr[i] = '1'
        elif (mask_char == '0'):
            # addr bit unchanged
            intermediate_addr[i] = addr_char

    num_X = intermediate_addr.count("X")
    num_perms = (2**num_X)
    perms = []

    # build up a list of perms. E.g. if 3 Xs in mask ending 000X0XX:
    # [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], etc
    for i in range(num_perms):
        # convert i to bin, and then pad to num_x
        perms.append(list(bin(i)[2:].zfill(num_X)))

    addresses_to_update = {}

    # iterate through permutations
    # E.g. perm = [0, 0, 0]
    # E.g. replace three Xs with three 0s
    # Then replace three Xs with 0, 0, 1
    # Etc
    for perm in perms:
        i = 0
        new_addr = ""
        for addr_char in intermediate_addr:
            if addr_char == "X":
                # substitute our permutation for X
                new_addr += str(perm[i])

                # increment the permutation
                i += 1
            else:
                new_addr += addr_char

        new_addr_dec = int(new_addr, 2)
        addresses_to_update[new_addr_dec] = int(value)
        
    return addresses_to_update


def process_mem_update_v1(instr, value, mask: str):
    # Modify the data being written to the address using a mask
    # The mask changes the bit in the address being written.

    # Regex to extract the memory address
    addr = INSTR_PATTERN.findall(instr)[0]
    new_val = int(value)

    # If mask=1, 1 is written at this bit.  Do nothing with X.
    # Achieve using OR as a SET mask, and zero all X.
    set_mask = int(mask.replace("X", "0"), 2)

    # If mask=0, 0 is written at this bit.  Do nothing with X.
    # Achieve using AND as a CLEAR mask, and set all X to 1.
    clear_mask = int(mask.replace("X", "1"), 2)

    new_val = new_val | set_mask
    new_val = new_val & clear_mask

    return addr, new_val


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

