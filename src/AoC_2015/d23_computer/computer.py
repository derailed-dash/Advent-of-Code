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
import logging
import time
import aoc_common.aoc_commons as td

locations = td.get_locations(__file__)
logger = td.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)

class Instructions():
    """ Define an instruction set, made up of instruction constants """
    JMP = "jmp"
    JIO = "jio"
    JIE = "jie"
    HLF = "hlf"
    TPL = "tpl"
    INC = "inc"

    @staticmethod
    def _hlf(x):
        return x // 2

    @staticmethod
    def _tpl(x):
        return x * 3
    
    @staticmethod
    def _inc(x):
        return x + 1

    @classmethod
    def execute(cls, instr, x):
        """ Dispatch to the specified instruction, with the specified value """
        method = getattr(cls, f'_{instr}', None)
        if method:
            return method(x)
        raise ValueError(f"Invalid instruction: {instr}") 
  
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
    
    def get_register_value(self, register: str):
        return self._registers[register]
    
    def set_register_value(self, register: str, val: int):
        self._registers[register] = val

    def run_program(self, program):
        """ Execute the specified program """

        # exit the loop when we reach an instruction that does not exist
        while self._instruction_ptr < len(program):
            program_line = program[self._instruction_ptr]
            parts = program_line.split(" ", 1) # split at the first space only
            instr = parts[0]
            instr_args = [arg.strip() for arg in parts[1].split(',')]
            
            if instr == Instructions.JMP: # e.g. jmp +19
                self._instruction_ptr += int(instr_args[0])
                continue
            
            # all other instructions have a register argument
            reg = instr_args[0]
            if instr == Instructions.JIE: # jie a, +4
                # jump if reg is even
                if self.get_register_value(reg) % 2 == 0:
                    self._instruction_ptr += int(instr_args[1])
                    continue
            elif instr == Instructions.JIO: # jio a, +8
                # jump if reg is ONE
                if self.get_register_value(reg) == 1:
                    self._instruction_ptr += int(instr_args[1])
                    continue
            else:
                try:
                    self.set_register_value(reg, Instructions.execute(instr, self.get_register_value(reg)))
                except ValueError as e:
                    e_val = e.args[0] if e.args else str(e)
                    raise ValueError(f"{e_val} at instruction {self._instruction_ptr}") from e

            self._instruction_ptr += 1
    
def main():
    # with open(locations.sample_input_file, mode="rt") as f:
    with open(locations.input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    run_part(1, data)
    run_part(2, data)
    
def run_part(part_num, program):
    computer = Computer()
    if part_num == 2:
        computer.set_register_value('a', 1)
        
    computer.run_program(program)
    
    logger.info("PART %d:", part_num)
    for reg_key, reg_val in computer.registers.items():
        logger.info(f"Register {reg_key}: {reg_val}")
    
    logger.info(".")

if __name__ == "__main__":
    t1 = time.perf_counter()
    try:
        main()   
    except ValueError as ex:
        logger.error(ex)
             
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
