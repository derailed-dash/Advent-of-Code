"""
Author: Darren
Date: 09/12/2020

Solving: https://adventofcode.com/2020/day/8

Read instructions like:
nop +0
acc +1
jmp +4
"""
import os
import time

BOOT_CODE_INPUT_FILE = "input/bootcode.txt"
SAMPLE_BOOT_CODE_INPUT_FILE = "input/sample_code.txt"

ACC = "acc"
JMP = "jmp"
NOP = "nop"

accumulator = 0

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, BOOT_CODE_INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_BOOT_CODE_INPUT_FILE)
    print("Input file is: " + input_file)

    code = read_input(input_file)

    success = run_code(code)
    if (success):
        print(f"Execution completed. Accumulator: {accumulator}")
    else:
        print(f"Execution could not complete. Accumulator: {accumulator}")

    success = try_substitutions(code)


def try_substitutions(code):
    substitutions_tried = 0
    
    for index, line in enumerate(code):
        substituted_code = code.copy()

        substituted = False
        if (JMP in line):
            substituted_code[index] = [NOP, substituted_code[index][1]]
            substituted = True
        
        if (NOP in line):
            substituted_code[index] = [JMP, substituted_code[index][1]]
            substituted = True

        if (substituted):
            substitutions_tried += 1
            # print(f"Substituting at line {index+1}, instruction: {line} -> {substituted_code[index]}")
            success = run_code(substituted_code)
            if (success):
                print(f"Program terminates successfully on iteration {substitutions_tried}. Accumulator value is: {accumulator}.")
                return True

    return False


def get_line(a_ptr):
    return a_ptr + 1
    

def run_code(code: list):
    global accumulator

    accumulator = 0

    # store current instruction
    instruction_ptr = 0

    # store instructions already processed
    instructions_processed = []

    while True:
        if (instruction_ptr in instructions_processed):
            # print(f"[Step {len(instructions_processed) + 1}]: We've done instruction {instruction_ptr + 1} before!")
            return False

        if (instruction_ptr >= len(code)):
            print(f"[Step {len(instructions_processed) + 1}]: EOF!")
            return True

        instructions_processed.append(instruction_ptr)
        instruction_ptr = process_instruction(code, instruction_ptr)


def process_instruction(code: list, ptr: int) -> int:
    global accumulator

    instruction, value = code[ptr]
    # print(f"[Step {len(instructions_processed)}, line {instruction_ptr + 1}]: Executing {instruction} {value}")

    if (instruction == ACC):
        accumulator += value
        ptr += 1
    elif (instruction == NOP):
        ptr += 1
    elif (instruction == JMP):
        ptr += value

    return ptr


def read_input(a_file) -> list:
    with open(a_file, mode="rt") as f:
        codelines = f.read().splitlines()
        
    return [[instr, int(val)] for instr, val in [line.split() for line in codelines]]


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

