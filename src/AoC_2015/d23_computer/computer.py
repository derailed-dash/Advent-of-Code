""" 
Author: Darren
Date: 26/04/2021

Solving https://adventofcode.com/2015/day/23

Simulate a simple computer with 2 registers and 6 instructions.

Part 1:
    Register class stores register state and provides convenience methods.
    The program loops through all instructions, processing the instruction
    pointed to at the instruction pointer. 
    The program exits when the instruction pointer points to a non-existent instruction.

Part 2:
    Same as before, but reg b initalised to 1, rather than 0.
"""
from enum import Enum
import logging
import time
import common.type_defs as td

locations = td.get_locations(__file__)
logger = td.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)

class Instructions(Enum):
    """ Define an instruction set, made up of instruction constants """
    JMP = "jmp"
    JIO = "jio"
    JIE = "jie"
    HLF = "hlf"
    TPL = "tpl"
    INC = "inc"
  
class Computer:
    """ Simulate a computer with 2 registers """
    
    def __init__(self, init_val: int = 0) -> None:
        self._registers = {
            'a': init_val,
            'b': init_val
        }
        self._instruction_ptr = 0
    
    @property
    def registers(self):
        """ Return the registers """
        return self._registers
    
    def hlf(self, register: str):
        self._registers[register] //= 2
    
    def tpl(self, register: str):
        self._registers[register] *= 3
        
    def inc(self, register: str, amount: int = 1):
        self._registers[register] += amount
    
    def get_register_value(self, register: str):
        return self._registers[register]
    
    def set_register_value(self, register: str, val: int):
        self._registers[register] = val

    def run_program(self, program):

        # exit the loop when we reach an instruction that does not exist
        while self._instruction_ptr < len(program):
            instr = program[self._instruction_ptr]
            
            if instr[0] == Instructions.JMP.value:
                self._instruction_ptr += instr[2]
                continue
            
            # all other instructions have a register argument
            if instr[0] == Instructions.JIE.value:
                # jump if reg is even
                if self.get_register_value(instr[1]) % 2 == 0:
                    self._instruction_ptr += instr[2]
                    continue
            elif instr[0] == Instructions.JIO.value:
                # jump if reg is ONE
                if self.get_register_value(instr[1]) == 1:
                    self._instruction_ptr += instr[2]
                    continue
            elif instr[0] == Instructions.HLF.value:
                self.hlf(instr[1])
            elif instr[0] == Instructions.TPL.value:
                self.tpl(instr[1])
            elif instr[0] == Instructions.INC.value:
                self.inc(instr[1])
            else:
                raise ValueError(f"Invalid instruction: {instr[0]}") 

            self._instruction_ptr += 1

def main():
    # with open(locations.sample_input_file, mode="rt") as f:
    with open(locations.input_file, mode="rt") as f:
        data = f.read().splitlines()
        
    program = process_input(data)
    for item in program:
        logger.debug(item)
    
    run_part(1, program)
    run_part(2, program)
    
def run_part(part_num, program):
    computer = Computer()
    if part_num == 2:
        computer.set_register_value('a', 1)
    computer.run_program(program)
    
    logger.info("PART %d:", part_num)
    for reg_key, reg_val in computer.registers.items():
        logger.info(f"Register {reg_key}: {reg_val}")
    
    logger.info(".")

def process_input(data: list[str]) -> list:
    """ Input is a list of instructions.  Convert to a list of instructions.
    Note: Register is None for JMP instructions.
          Offset is None for all non-jump instructions.

    Returns:
        List: Where each item is itself a list of [instr, register, offset]
        
    E.g. turns: jio a, +22 
          into: ['jio', 'a', 22]
    """
    program = []
    
    for line in data:
        reg = None
        offset = None
        
        instruction_parts = line.split()
        instr = instruction_parts[0]
        if instr != Instructions.JMP:
            reg = instruction_parts[1][0]
            
        if (instr in (Instructions.JMP.value, Instructions.JIE.value, Instructions.JIO.value)):
            offset = int(instruction_parts[-1])
            
        program.append([instr, reg, offset])
        
    return program    
            
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
