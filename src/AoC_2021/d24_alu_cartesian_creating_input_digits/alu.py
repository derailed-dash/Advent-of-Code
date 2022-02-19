"""
Author: Darren
Date: 24/12/2021

Solving https://adventofcode.com/2021/day/24

Created an ALU computer, but turned out not to need it.
Using the computer class to compute the result of 9**14 input values won't do!
So instead, we need to work out what the input program is doing, 
determine a function z = f(w,z), and then determine values that lead to z=0.

Part 1:
    - Take a 14 digit input number, and process digit by digit (start most significant).
    - Stop when our z value is 0.
    - The input program has 14 repeating blocks of 18 lines, i.e. one block per input digit.
        inp w                               add y 25
        mul x 0                             mul y x
        add x z                             add y 1
        mod x 26                            mul z y
        div z 1  * 1 (shrink) or 26 (exp)   mul y 0
        add x 12 * -ve when div z is 26     add y w
        eql x w                             add y 7 * Varies
        eql x 0                             mul y x
        mul y 0                             add z y

      (Specific instructions will obviously be unique per input.)
    - Three lines (marked *) are variable.
    - z persists between blocks. Whereas x and y are both reset during the block.
    - Thus, z will be a function of w and previous z.
    - There are two types of instruction block:
        - Those where z expands, where next z = 26z+w+b
        - Those where z can shrink.
    - For the shrinkage type, next z can be given by:
        - z = z//26 (when x=0), where z shrinks.
        - z = z+w+b, where z stays of similar magnitude.
    - There are 7 instruction blocks of each type.
        - For expansions, input value makes little difference.
        - For shrinkage, we always want to make sure the shrink formula is satisfied, 
          which is true when w = (z % 26) + a
          for -ve values of a as the parameter to the "add x" step.
    - We can compute the values of z for shrinkage types.
    - For expansion types, we just need to try all possible permutations of 
      these 7 instructions.  Thus, of the 14 input digits, we only need to brute force 7 of them, 
      leading to 9**7 = 4.8m permutations.

Part 2:
    Same as Part 1, but now we just want the minimum valid value.
"""
import logging
import os
import time
from itertools import product
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

class ALU():
    """ Simulate processor with four registers and six instructions """
    def __init__(self) -> None:
        self._vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        
        self._input = None
        self._input_posn = 0    # which digit of the input value we're currently on
        
        self._instructions: list[tuple[str, list[str]]] = []     # list of instructions in the format [instr, [parms]]
        self._ip = 0
        
    @property
    def vars(self):
        return self._vars
    
    def _set_input(self, value: str):
        """ Take a number and store as a str representation """
        assert value.isdigit, "Must be number"
        assert len(value) == 14, "Must be 14 digit input"
        self._input = value
        self._input_posn = 0        
     
    def _set_var(self, var, value):
        """ Sets the specified var to the specified value. """
        if var not in self._vars:
            raise KeyError(f"No such var '{var}'")
        
        self._vars[var] = value
    
    def _reset(self):
        for var in self._vars:
            self._vars[var] = 0

        self._input = None
        self._input_posn = 0
        self._ip = 0
        
    def run_program(self, input_str: str):
        """ Process instructions in the program. """
        self._reset()      
        self._set_input(input_str)
        
        for instruction in self._instructions:
            self._execute_instruction(instruction)
            self._ip += 1

    def set_program(self, instructions_input: list[str]):
        """ Create a list of instructions, 
        where each instruction is of the format: (str, list[str]) """
        self._instructions = []
        
        for line in instructions_input:
            instr_parts = line.split()
            instr = instr_parts[0]
            instr_parms = instr_parts[1:]
        
            self._instructions.append((instr, instr_parms))
        
    def _execute_instruction(self, instruction:tuple[str, list[str]]):
        """ Takes an instruction, and calls the appropriate implementation method.

        Args:
            instr_and_parms (list): The instruction, in the format (instr, [parms])
            
        Raises:
            AttributeError if instruction is not understood
        """
        # logger.debug("Instruction: %s", instruction)
        instr = instruction[0]
        instr_parms = instruction[1]
        
        # call the appropriate instruction method
        try:
            self.__getattribute__(f"_op_{instr}")(instr_parms)         
        except AttributeError as err:
            raise AttributeError(f"Bad instruction {instr} at {self._ip}") from err

    def int_or_reg_val(self, x) -> int:
        """ Determine if the variable is an int value, or the value is a register """
        if x in self._vars:
            return self._vars[x]
        else:
            return int(x)
        
    def _op_inp(self, parms:list[str]):
        var = parms[0]
        assert self._input, "Input value not set"
        assert self._input_posn < len(self._input), "Too many input digits!"
        input_digit = int(self._input[self._input_posn])
        self._vars[var] = input_digit
        self._input_posn += 1
    
    def _op_add(self, parms:list[str]):
        """ Add a to b and store in a. Param b could be a var or a number. """
        self._vars[parms[0]] += self.int_or_reg_val(parms[1])
    
    def _op_mul(self, parms:list[str]):
        """ Multiply a by b and store in a. Param b could be a var or a number. """
        self._vars[parms[0]] *= self.int_or_reg_val(parms[1])
    
    def _op_div(self, parms:list[str]):
        """ Divide a by b and store in a. Param b could be a var or a number. """
        parm_b = self.int_or_reg_val(parms[1])
        assert parm_b != 0, "Integer division by 0 is bad."
        self._vars[parms[0]] //= parm_b
        
    def _op_mod(self, parms:list[str]):
        """ Modulo a by b and store in a. Param b could be a var or a number. """
        parm_a = self._vars[parms[0]]
        parm_b = self.int_or_reg_val(parms[1])
        try:
            assert parm_a >= 0 and parm_b != 0, "Integer division by 0 is bad." 
            self._vars[parms[0]] %= parm_b     
        except AssertionError as err:
            raise AttributeError(f"Bad instruction: {parm_a} mod {parm_b}") from err

    def _op_eql(self, parms:list[str]):
        """ Chec if a and b are equal. Store 1 if equal. Param b could be a var or a number. """
        self._vars[parms[0]] = 1 if self._vars[parms[0]] == self.int_or_reg_val(parms[1]) else 0
                 
    def __repr__(self):
        return f"{self.__class__.__name__}{self._vars}"    

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    COUNT_INSTRUCTION_BLOCKS = 14
    EXPECTED_INSTRUCTIONS_PER_BLOCK = 18
    
    instruction_block_size = len(data) // COUNT_INSTRUCTION_BLOCKS
    assert instruction_block_size == EXPECTED_INSTRUCTIONS_PER_BLOCK
    
    # Split all instructions into repeating blocks of instructions
    instruction_blocks: list[list[str]] = []
    for i in range(COUNT_INSTRUCTION_BLOCKS):
        instruction_blocks.append(data[i*instruction_block_size:(i+1)*instruction_block_size])
    
    alu = ALU()
    alu.set_program(data)
    valid_vals = compute_valid_inputs(instruction_blocks)
    if valid_vals:
        max_input_val = max(valid_vals)
        min_input_val = min(valid_vals)
        
        # check them by running them through the ALU
        for val in (min_input_val, max_input_val):
            alu.run_program(str(val))
            if alu.vars['z'] == 0:
                logger.info("%s verified.", val) 
            else:
                logger.info("%s does not work??")
    else:
        logger.info("Fail bus, all aboard.")

def compute_valid_inputs(instruction_blocks: list[list[str]]) -> list[int]:
    """ Our goal is determine valid values of w, 
    where w is each successive digit of the 14-digit input value.
    The 14 input values are used in the 14 blocks of instructions.
    
    The 14 instruction types are across 2 types:
        - expansion, where div z 1.
          Brute-force all possible w values
        - shrinkage, where div z 26
          Determine specific values of w that will lead to shrinkage. """

    # instruction types, based on "div z" instruction parameter
    SHRINKAGE = 26
    
    div_z_instructions = []
    add_x_instructions = []
    add_y_instructions = []
    
    for block in instruction_blocks:
        # Retrieve the param value from each instruction
        # The instructions we care about are at specific locations in the block
        div_z_instructions.append(int(block[4].split()[-1]))
        add_x_instructions.append(int(block[5].split()[-1]))
        add_y_instructions.append(int(block[15].split()[-1]))
    
    # Values of these variables in our input data
    # z [1,   1,  1,  1, 26,  1,  1,  26,  1, 26,  26, 26, 26,  26]
    # x [12, 12, 13, 12, -3, 10, 14, -16, 12, -8, -12, -7, -6, -11]
    # y [7,   8,  2, 11,  6, 12, 14,  13, 15, 10,   6, 10,  8,   5]
    
    # E.g. [False, False, False, False, True...]
    shrink_instructions = [z == SHRINKAGE for z in div_z_instructions]
    shrink_count = sum(x for x in shrink_instructions)
    assert shrink_count == 7, "We expect 7 shrink types for our input"
    
    # list of tuples by index, e.g. (False, 12, 7)
    instruction_vars = list(zip(shrink_instructions, add_x_instructions, add_y_instructions))

    # Get the cartesian product of all digits where any digit is possible
    # E.g. 9999999, 9999998, 9999997, etc
    any_digits = list(product(range(9, 0, -1), repeat=shrink_count))
    assert len(any_digits) == 9**shrink_count, "Cartesian product messed up"
        
    valid: list[int] = []    # Store valid 14-digit input values
    for digits_candidate in tqdm(any_digits):
        num_blocks = len(instruction_blocks)
        z = 0
        digit = [0] * num_blocks
    
        early_exit = False
        digits_idx = 0
    
        for block_idx in range(num_blocks):
            is_shrink, add_x, add_y = instruction_vars[block_idx]
                  
            if is_shrink:
                # We want to compute a value w, where w = (z % 26) + a 
                digit[block_idx] = ((z % 26) + add_x)   # digit[block_idx] = w
                z //= 26    # New z is given by z = z//26
                if not (1 <= digit[block_idx] <= 9):
                    early_exit = True
                    break
            
            else:   # expansion type, so just use the candidate digit
                z = (26 * z) + digits_candidate[digits_idx] + add_y
                digit[block_idx] = digits_candidate[digits_idx]  
                digits_idx += 1
        
        if not early_exit:
            valid.append(int("".join(str(i) for i in digit)))
     
    return valid

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
