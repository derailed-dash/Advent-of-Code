"""
Author: Darren
Date: 02/10/2021

Solving https://adventofcode.com/2016/day/21

We need to take an input value and then scramble it by following a series of instructions.

Part 1:
    Create a Scrambler class that processes each instruction.

Part 2:
    Now we need to reverse the scrambling process.
    Fortunately, most of the scramble instructions do not need to be reversed.
    We only need to explicitly reverse instructions that rely on positions.
    For rotate based, let's just shift left one at a time, and see whether the original shift right
        would have produced the current scramble.
    For move position, just swap the x and y around.
    
    Of course, we need to process the instructions in reverse.
"""
import logging
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

SCRAMBLE_INPUT = "abcdefgh"
# SCRAMBLE_INPUT= "abcde"

UNSCRAMBLE_INPUT = "fbgdceah"
# UNSCRAMBLE_INPUT = "decab"

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Scrambler")    
class Scrambler:
    """ Knows how to scramble and unscramble input, based on a set of supplied instructions. """
    
    SWAP_POSITION = "swap position"
    SWAP_LETTER = "swap letter"
    ROTATE_BASED = "rotate based"
    REVERSE = "reverse"
    MOVE = "move"
    ROTATE_LEFT_OR_RIGHT = "rotate"
    
    def __init__(self, scramble_input: str) -> None:
        self._scramble_input = scramble_input
        self._scramble_value = self._scramble_input     # stores scrambled value as we process
        
    @property
    def scramble_value(self):
        return self._scramble_value
    
    @scramble_value.setter
    def scramble_value(self, value: str):
        self._scramble_value = value
    
    def scramble(self, instructions: list):
        """ Scramble using instructions """
        for instruction in instructions:
            self._execute_instruction(instruction)
    
    def unscramble(self, instructions: list):
        """ Unscramble using instructions. Here, the instructions are processed in reverse. """
        for instruction in reversed(instructions):
            self._execute_instruction(instruction, reverse=True)
    
    def _execute_instruction(self, instruction:str, reverse=False):
        """ Takes an instruction, and calls the appropriate implementation method. 
        Note that some instructions take a 'reverse' parameter """
        
        logger.debug("Instruction: %s", instruction)
        if instruction.startswith(Scrambler.SWAP_POSITION):
            self.scramble_value = self._swap_position(instruction, self.scramble_value)
        elif instruction.startswith(Scrambler.SWAP_LETTER):
            self.scramble_value = self._swap_letters(instruction, self.scramble_value)
        elif instruction.startswith(Scrambler.ROTATE_BASED):
            self.scramble_value = self._rotate_based(instruction, self.scramble_value, reverse)
        elif instruction.startswith(Scrambler.REVERSE):
            self.scramble_value = self._reverse(instruction, self.scramble_value)
        elif instruction.startswith(Scrambler.MOVE):
            self.scramble_value = self._move_position(instruction, self.scramble_value, reverse)
        elif instruction.startswith(Scrambler.ROTATE_LEFT_OR_RIGHT):
            self.scramble_value = self._rotate(instruction, self.scramble_value, reverse)
        else:
            assert False, "No instructions fall through."
            
        logger.debug("Current scramble: %s", self.scramble_value)

    def _swap_position(self, instruction: str, src: str) -> str:
        pattern = re.compile(r"(swap position) (\d+) with position (\d+)")
        index_x, index_y = map(int, pattern.match(instruction).groups()[-2:])
        
        char_at_x, char_at_y = src[index_x], src[index_y]
        
        new_val = src
        new_val = new_val[:index_x] + char_at_y + new_val[index_x+1:]
        new_val = new_val[:index_y] + char_at_x + new_val[index_y+1:]
        
        return new_val

    def _swap_letters(self, instruction: str, src: str) -> str:
        pattern = re.compile(r"(swap letter) ([a-z]) with letter ([a-z])")
        letter_x, letter_y = pattern.match(instruction).groups()[-2:]
        
        new_val = src
        new_val = new_val.replace(letter_x, "*")
        new_val = new_val.replace(letter_y, letter_x)
        new_val = new_val.replace("*", letter_y)
        
        return new_val

    def _reverse(self, instruction: str, src: str) -> str:
        pattern = re.compile(r"(reverse) positions (\d+) through (\d+)")
        index_x, index_y = map(int, pattern.match(instruction).groups()[-2:])
        
        return src[:index_x] + src[index_x:index_y+1][::-1] + src[index_y+1:]
        
    def _rotate(self, instruction: str, src: str, reverse=False) -> str:
        pattern = re.compile(r"(rotate) (left|right) (\d+) step")
        rotate = int(pattern.match(instruction).groups()[-1])
        
        left_or_right = pattern.match(instruction).groups()[-2]
        
        if left_or_right == "right":
            rotate_method = self._rotate_left_n if reverse else self._rotate_right_n
        else:
            rotate_method = self._rotate_right_n if reverse else self._rotate_left_n
        
        return rotate_method(rotate, src)
        
    def _rotate_left_n(self, rotations:int, src: str) -> str:
        return src[rotations:] + src[:rotations]
    
    def _rotate_right_n(self, rotations:int, src: str) -> str:
        rotate = len(src) - rotations
        return self._rotate_left_n(rotate, src)
    
    def _rotate_based(self, instruction: str, src: str, reverse=False) -> str:
        """ The whole string should be rotated to the right based on the index of letter X (counting from 0)
        as determined before this instruction does any rotations. 
        Once the index is determined, rotate the string to the right one time, 
        plus a number of times equal to that index, plus one additional time if the index was at least 4. """
        
        pattern = re.compile(r"(rotate based) on position of letter ([a-z])")
        char = pattern.match(instruction).groups()[-1]
        index_of_char = src.index(char)
        
        new_val = src
        
        # for scrambling
        if not reverse:
            # Rotate to the right once, plus a number of times equal to the index
            for _ in range(index_of_char+1):
                new_val = self._rotate_right_n(1, new_val)
                
            # If original index is at least 4, rotate one extra time
            if index_of_char >= 4:
                new_val = self._rotate_right_n(1, new_val)
        else:
            assert reverse, "We should be reversing the rotate"
            # just keep rotating left and then test if the original instruction
            # would have resulted in the current scramble
            target = src
            for _ in range(len(src)):
                new_val = self._rotate_left_n(1, new_val)
                if target == self._rotate_based(instruction, new_val):
                    break   # at least one of these will always work
                
        return new_val
        
    def _move_position(self, instruction: str, src: str,  reverse=False) -> str:
        pattern = re.compile(r"(move) position (\d+) to position (\d+)")
        
        index_x, index_y = map(int, pattern.match(instruction).groups()[-2:])
        if reverse:
            index_x, index_y = index_y, index_x    
                
        char_at_x = src[index_x]
        
        new_val = src
        new_val = new_val[:index_x] + new_val[index_x+1:]
        new_val = new_val[:index_y] + char_at_x + new_val[index_y:]
        return new_val
            
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(input={self._scramble_input}, value={self.scramble_value})"
    
def main():        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        instructions = f.read().splitlines()

    # Part 1
    logger.info("Part 1 input: %s", SCRAMBLE_INPUT)
    scrambler = Scrambler(SCRAMBLE_INPUT)
    scrambler.scramble(instructions)
    logger.info("Scramble=%s\n", scrambler.scramble_value)
    
    # Part 2
    logger.info("Part 2 input: %s", UNSCRAMBLE_INPUT)
    scrambler = Scrambler(UNSCRAMBLE_INPUT)
    scrambler.unscramble(instructions)
    logger.info("Unscramble=%s", scrambler.scramble_value)   

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
