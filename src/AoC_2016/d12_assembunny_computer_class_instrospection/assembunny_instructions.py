"""
Author: Darren
Date: 27/06/2021

Solving https://adventofcode.com/2016/day/12

Create the assembunny computer.  
Then use the computer to copute the value of register a
after following a set of instructions.

Four registers that start with value 0. Limited instruction set.

Solution:
    Computer class contains methods for each instr.
    Use self.__getattribute__(f"_op_{instr}")(instr_parms) to call appropriate method
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(level=logging.DEBUG, 
                format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Assembunny")
logger.setLevel(logging.INFO)

# pylint: disable=logging-fstring-interpolation

class Computer():
    """ Stores a set of registers, which each store an int value.
    Processes instructions in a supplied program, 
    using the instruction pointer to determine which instuction is next.
    """
    def __init__(self) -> None:
        self._registers = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0
        }
        
        self._ip = 0    # instruction pointer
        self._instructions = []     # list of instructions in the format [instr, [parms]]
        
    @property
    def registers(self):
        return self._registers
     
    def set_register(self, reg, value):
        """ Sets the specified register to the specified value.

        Args:
            reg ([str]): Register value
            value ([int]): The value we want to set the register to

        Raises:
            KeyError: If no such register
        """
        if reg not in self._registers:
            raise KeyError(f"No such register '{reg}'")
        
        self._registers[reg] = value
            
    def run_program(self, instructions_input: list):
        """Process instructions in the program.
            - Converts the program input to a list of instructions and stores them in the computer.
            - Then executes the instructions one at a time, using the instruction pointer
              to determine which instruction is next.       

        Args:
            instructions (list): Each instr is in the format [instr, [parms]]
        """                
        # Create a list of instructions, 
        # where each instruction is of the format [instr, [parms]]
        for line in instructions_input:
            instr_parts = line.split()
            instr = instr_parts[0]
            instr_parms = instr_parts[1:]
        
            self._instructions.append([instr, instr_parms])
        
        while self._ip < len(self._instructions):
            logger.debug("Running instruction at %d", self._ip)
            self._execute_instruction(self._instructions[self._ip])
        
    def _execute_instruction(self, instr_and_parms:list):
        """ Takes an instruction, and calls the appropriate implementation method.
        
        After each instruction we increment in the instruction pointer,
        unless a JNZ instruction, which handles its own IP adjustment.

        Args:
            instr_and_parms (list): The instruction, in the format [instr, [parms]]
            
        Raises:
            AttributeError if instruction is not understood
        """
        logger.debug("Instruction: %s", instr_and_parms)
        instr = instr_and_parms[0]
        instr_parms = instr_and_parms[1]
        
        # call the appropriate instruction method
        try:
            self.__getattribute__(f"_op_{instr}")(instr_parms)
        except AttributeError as err:
            raise AttributeError(f"Bad instruction {instr} at {self._ip}") from err

        # increment the instruction counter, if not a jnz instruction
        if instr != "jnz":
            self._ip += 1
    
    def int_or_reg_val(self, x) -> int:
        """ Determine if the variable is an int value, or the value in a register """
        if x in self._registers:
            return self._registers[x]
        else:
            return int(x)
        
    def _op_cpy(self, instr_parms:list):
        src, dst = instr_parms
        
        # the src could be a register, or an int value
        self._registers[dst] = self.int_or_reg_val(src)
    
    def _op_inc(self, instr_params:list):
        """ Increment the specified register by 1 """
        self._registers[instr_params[0]] += 1
    
    def _op_dec(self, instr_params:list):
        """ Decrement the specified register by 1 """
        self._registers[instr_params[0]] -= 1
    
    def _op_jnz(self, instr_params:list):
        """ JNZ x y 
        Increment the instruction pointer by specified int value y,
        but only if x is not 0, or is not a register with a 0 value 

        Args:
            instr_params (list): params in a []
        """
        reg_or_val, jump_val = instr_params
        
        if str.isalpha(jump_val):
            assert jump_val in self._registers, jump_val + " must be a register."
            jump_val = self._registers[jump_val]
        
        # check if non-zero register
        if reg_or_val in self._registers and self._registers[reg_or_val] != 0:
            self._ip += int(jump_val)
        # check if non-zero number
        elif str.isnumeric(reg_or_val) and int(reg_or_val) != 0:
            self._ip += int(jump_val)
        else:
            self._ip += 1
         
    def __repr__(self):
        return f"{self.__class__.__name__}{self._registers}"
       

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    logger.debug(data)
    
    computer = Computer()
    computer.run_program(data)
    logger.info(f"Part 1: {computer}") 
    
    computer = Computer()
    computer.set_register('c', 1)
    computer.run_program(data)
    logger.info(f"Part 2: {computer}")   


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
