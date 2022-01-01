"""
Author: Darren
Date: 12/11/2021

Solving https://adventofcode.com/2016/day/23

We need to tweak the Day 12 Monorail Assembunny computer.
Uses same instruction set as Assembunny, but now adds a new instruction: tgl x
This means: toggle the instruction that is x instructions away.

Part 1:
    Extend the original Assembunny.
    Implement the tgl method to toggle instructions as required.
    Tweak the original class to store the instructions as an instance attribute, 
    so we can modify the instructions.
    Tweak original JNZ so that second parameter can also be value in a register.

Part 2:
    The challenge here is that we have instruction combos that result in very long inefficient loops.
    It runs without any optimisation but takes an hour!
    We create a new subclass, the MultiplyingAssembunny.
    This uses regex to substitute inefficient instructions for more efficient instructions.
    Gets us down to under a second.
"""
import logging
import os
import time
import re
from AoC_2016.d12_assembunny_computer_class_instrospection.assembunny_instructions import Computer

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Assembunny2")
logger.setLevel(level=logging.INFO)

class Assembunny2(Computer):
    """ Extension of origional Assembunny computer.
    This adds the ability to 'toggle' a given instruction in the program, using tgl instruction. """
    
    def _op_tgl(self, instr_params:list):
        """ Toggle the instruction x away, where x is the value held at the specified register.
        Toggle means:
            - For 1 arg instructions:
                - Inc becomes dec
                - All others become inc, including tgl of a tgl
                - With a=0, tgl a becomes inc a
            - For 2 arg instructions:
                - jnz becomes cpy
                - All others become jnz
                - Any instructions that are invalid after a tgl are skipped
                  e.g. cpy 1 2 (since the second arg must always be a register)
         """
        tgl_param = instr_params[0]
        offset = tgl_param if isinstance(tgl_param, int) else self.registers[tgl_param]
        
        if self._ip + offset >= len(self._instructions):
            # Offset is beyond the end of the program
            return
        
        old_instr, params = self._instructions[self._ip + offset]
        if len(params) == 1:
            if old_instr == "inc":
                self._instructions[self._ip + offset][0] = "dec"
            else:
                self._instructions[self._ip + offset][0] = "inc"
        elif len(params) == 2:
            if old_instr == "jnz":
                self._instructions[self._ip + offset][0] = "cpy"
            else:
                self._instructions[self._ip + offset][0] = "jnz"

class MultiplyingAssembunny(Assembunny2):
    def run_program(self, instructions_input: list):
        new_instructions = self.optimise(instructions_input)
        super().run_program(new_instructions)
    
    def optimise(self, instructions_input: list) -> list[str]:
        """ Convert inefficient instructions to more efficient instructions.
        Resulting code needs to occupy the same number of instruction lines.
        That's why we have nop instruction to take up space and o nothing.
        """
        
        # convert instructions to a str
        code = '\n'.join(line for line in instructions_input)

        # use regex to replace patterns of instructions with more efficient instructions
        replacements = [
            (   # Multiplication (inc X, dec Y, jnz Y -2, dec Z, jnz Z -5)
                # Becomes (mul Y Z X)
                r'inc ([a-d])\ndec ([a-d])\njnz \2 -2\ndec ([a-d])\njnz \3 -5',
                r'mul \2 \3 \1\ncpy 0 \2\ncpy 0 \3\nnop\nnop',
            ), 
            (   # Addition (inc X, dec Y, jnz Y -2)
                # Becomes (add X Y X)
                r'inc ([a-d])\ndec ([a-d])\njnz \2 -2',
                r'add \1 \2 \1\ncpy 0 \2\nnop',
            ),
            (   # Addition (dec X, inc Y, jnz X -2)
                # Becomes (add X Y Y)
                r'dec ([a-d])\ninc ([a-d])\njnz \1 -2',
                r'add \1 \2 \2\ncpy 0 \1\nnop',
            )
        ]

        for pattern, replacement in replacements:
            code = re.sub(pattern, replacement, code)

        # convert str back to instructions list
        new_instructions = code.split('\n')
        return new_instructions
        
    def _op_nop(self, instr_params:list):
        """ Do nothing """
        pass
    
    def _op_add(self, instr_params:list):
        """ add a b c 
        Adds a to b and stores in register c """
        parm_a, parm_b, parm_c = instr_params
        self._registers[parm_c] = self.int_or_reg_val(parm_a) + self.int_or_reg_val(parm_b)
    
    def _op_mul(self, instr_params:list):
        """ mul a b c 
        Product of a and b is stored in register c """
        parm_a, parm_b, parm_c = instr_params
        self._registers[parm_c] = self.int_or_reg_val(parm_a) * self.int_or_reg_val(parm_b)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
        
    logger.debug(data)
    
    try:
        computer = Assembunny2()
        computer.set_register('a', 7)
        computer.run_program(data)
        logger.info("Part 1: %s", computer)
    except AttributeError as err:
        logger.error(err)
        #logger.error(err.__cause__)   # show implementation
        
    try:
        computer = MultiplyingAssembunny()
        computer.set_register('a', 12)
        computer.run_program(data)
        logger.info("Part 2: %s", computer)
    except AttributeError as err:
        logger.error(err)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
