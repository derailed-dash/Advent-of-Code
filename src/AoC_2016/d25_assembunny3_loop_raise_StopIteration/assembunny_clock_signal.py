"""
Author: Darren
Date: 21/11/2021

Solving https://adventofcode.com/2016/day/25

Part 1:
    Extend Assembunny Computer from Day 12.
    Add the "out" instruction. It emits a value each time it runs.
    Goal is for the out instruction to emit alternating 0 and 1, forever.
    Let's store the emitted result from out in an instance attribute.
    It can only emit 0 or 1.  
    If we get two repeating digits, we've failed to terminate this computer.
    Throw an exception to terminate the out method, whenever we fail,
    or when we're confident we've got a good clock signal

Part 2:
    Nothing to do!

"""
from __future__ import absolute_import
import logging
import os
import time
from AoC_2016.d12_assembunny_computer_class_instrospection.assembunny_instructions import Computer

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"

logging.basicConfig(level=logging.DEBUG, 
                format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Assembunny3")
logger.setLevel(level=logging.INFO)

class Assembunny3(Computer):
    """ Extension of origional Assembunny computer.
    This adds the "out" instruction

    Raises:
        StopIteration
    """
    
    def __init__(self) -> None:
        self._clock_signal = ""
        super().__init__()
    
    @property
    def clock_signal(self) -> str:
        return self._clock_signal
    
    def _op_out(self, instr_params:list):
        """ Outputs the int value or value of the register

        Args:
            instr_params (list): params in a []

        Raises:
            StopIteration: To terminate the method, otherwise could loop forever
        """
        self._clock_signal += str(self.int_or_reg_val(instr_params[0]))
        
        if (len(self.clock_signal) >= 2 and 
            self.clock_signal[-1] == self.clock_signal[-2]):
            # We've got a repeating digit, so not what we're after
            raise StopIteration("Bad clock")
        elif len(self.clock_signal) > 100:
            raise StopIteration("Good clock!")

def main():    
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
        
    logger.debug(data)
    
    try:
        reg_input = 0
        while True:
            computer = Assembunny3()
            computer.set_register('a', reg_input)
            try:
                computer.run_program(data)
            except StopIteration as err:
                if err.value == "Bad clock":
                    logger.debug("Bad clock with %d: %s", reg_input, computer.clock_signal)
                else: 
                    logger.info("Good clock with %d: %s", reg_input, computer.clock_signal)
                    break
                
            reg_input += 1
    except AttributeError as err:
        logger.error(err)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
