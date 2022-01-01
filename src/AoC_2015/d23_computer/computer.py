""" 
Author: Darren
Date: 26/04/2021

Solving https://adventofcode.com/2015/day/23

Simulator a simple computer with 2 registers and 6 instructions.

Part 1:
    Register class stores register state and provides convenience methods.
    The program loops through all instructions, processing the instruction
    pointed to at the instruction pointer. 
    The program exits when the instruction pointer points to a non-existent instruction.

Part 2:
    Same as before, but reg b initalised to 1, rather than 0.

"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

# pylint: disable=logging-fstring-interpolation

class Instructions:
    """Store instruction constants"""
    JMP = "jmp"
    JIO = "jio"
    JIE = "jie"
    HLF = "hlf"
    TPL = "tpl"
    INC = "inc"
  
class Register:
    """Store register state"""
    
    def __init__(self, init_val: int = 0) -> None:
        self._value = init_val
        
    def hlf(self):
        self._value //= 2
    
    def tpl(self):
        self._value *= 3
        
    def inc(self, amount: int = 1):
        self._value += amount
        
    def get_value(self):
        return self._value
        

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
        
    program = process_input(data)
    logging.debug(program) 
    
    reg_a = Register()
    reg_b = Register()
    registers = {'a': reg_a, 'b': reg_b}
    
    run_program(program, registers)
    logging.info("PART 1:")
    for register in registers:
        logging.info(f"Register {register}: {registers[register].get_value()}")
    
    reg_a = Register(1)
    reg_b = Register()
    registers = {'a': reg_a, 'b': reg_b}
    
    run_program(program, registers)
    logging.info("PART 2:")
    for register in registers:
        logging.info(f"Register {register}: {registers[register].get_value()}")


def run_program(program, registers):
    instr_pointer = 0
    
    # exit the loop when we reach an instruction that does not exist
    while instr_pointer < len(program):
        instr = program[instr_pointer]
        
        if instr[0] == Instructions.JMP:
            instr_pointer += instr[2]
            continue
        
        # all other instructions have a register argument
        current_reg = registers[instr[1]]
        if instr[0] == Instructions.JIE:
            # jump if reg is even
            if current_reg.get_value() % 2 == 0:
                instr_pointer += instr[2]
                continue
        elif instr[0] == Instructions.JIO:
            # jump if reg is ONE
            if current_reg.get_value() == 1:
                instr_pointer += instr[2]
                continue
        elif instr[0] == Instructions.HLF:
            current_reg.hlf()
        elif instr[0] == Instructions.TPL:
            current_reg.tpl()
        elif instr[0] == Instructions.INC:
            current_reg.inc()
        else:
            raise ValueError(f"Invalid instruction: {instr[0]}") 

        instr_pointer += 1


def process_input(data: list[str]) -> list:
    """Input is a list of instructions.  Convert to a list of instructions.
    Each instruction takes the format [instr, register, offset]
    Note: Register is None for JMP instructions.
          Offset is None for all non-jump instructions.

    Args:
        data (List[str]): Input list

    Returns:
        List: List of lists
    """
    program = []
    
    for line in data:
        reg = None
        offset = None
        
        instruction_parts = line.split()
        instr = instruction_parts[0]
        if instr != Instructions.JMP:
            reg = instruction_parts[1][0]
            
        if instr == Instructions.JMP or instr == Instructions.JIE or instr == Instructions.JIO:
            offset = int(instruction_parts[-1])
            
        program.append([instr, reg, offset])
        
    return program    
            

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
