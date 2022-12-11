"""
Author: Darren
Date: 10/12/2022

Solving https://adventofcode.com/2022/day/10

Part 1:

We have a CRT computer that processes instructions. It has a single register, x.
Instructions start on a given clock cycle. The addx instruction takes 2 cycles; noop takes 1.
Signal strength is given by: cycle value * x.

What is the sum of signals strengths from cycles 20, 60, 100, 140, 180 and 220?

- Solution:
  - Create a CrtComputer class that takes instructions as a parameter.
    - Track current instruction. Track which instruction was last started, 
      and whether it has completed yet, by decremeting a "doing" cycle counter.
    - Externalise a tick method, which increments the cycle, and start/finishes instructions.
      - Starting the instruction means adding the instruction, and its cycle requirement,
        to the self._doing property.
      - Ending an instruction means actually performing the job the instruction was meant to do,
        e.g. modifying the register value.
    - Provide a method to calculate and return the signal strength at any time.
    - Externalise a property to inform the caller when the program is finished.
  - From the calling application, continue to tick the computer until the program
    has finished. If the current cycle is one of our required cycles, 
    retrieve the signal strength.
  - Finally, add up our signal strengths.

Part 2:

"""
from pathlib import Path
import time
from matplotlib import pyplot as plt

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

class CrtComputer():
    """ Performs instructions. Add instructions take 2 ticks. Noop takes 1 tick. """
    DISPLAY_WIDTH = 40
    DISPLAY_HEIGHT = 6
    
    LIT = "#"
    
    def __init__(self, instructions: list[str]) -> None:
        self._x = 1 # represents middle of horizontal sprite position
        self._instructions = self._convert_to_instructions(instructions)
        self._ip = 0    # instruction pointer
        self.cycle = 0
        self._doing = []  # [[instruction], duration]
        self.running_program = True # Set to false when instructions are complete
        
        self._display_posn = [0,0]
        self._display = [[" " for _ in range(CrtComputer.DISPLAY_WIDTH)] 
                            for _ in range(CrtComputer.DISPLAY_HEIGHT)]
        
    @property
    def x(self):
        return self._x
    
    @property
    def signal_strength(self) -> int:
        return self.cycle * self.x
    
    def _convert_to_instructions(self, data: list[str]):
        """ Create a list of instructions in [[instr, val],[],...] format. """
        instructions = []
        for line in data:
            line_words = line.split()
            instr = line_words[0]
            val = None
            if len(line_words) > 1:
                val = int(line_words[1])
            instructions.append((instr, val))
                
        return instructions
        
    def tick(self):
        """ Perform one CPU cycle """
        # print(self)

        if len(self._doing) > 0: # we're processing an instruction
            self._doing[1] -= 1
            
            if self._doing[1] == 0:
                # Complete the running instruction
                instruction = self._doing[0]
                self.__getattribute__(f"_op_{instruction[0]}")(instruction)
                # print(f"Completed instruction: {instruction}")
                
                self._start_next_instruction() # and start the next one
        else: # our first instruction
            self._start_next_instruction()
        
        self._update_display()
            
        self.cycle += 1
    
    def _update_display(self):
        # Current horizontal pixel position being drawn
        x_posn = self._display_posn[0]
        
        # Check if horizontal position is *within* to current sprite position
        # The sprite is 3 pixels wide, and the x register gives us the middle position
        if x_posn in range(self.x-1, self.x+2):
            self._display[self._display_posn[1]][x_posn] = CrtComputer.LIT

        # display position moves across the row, then down, 
        # one pixel at a time with each tick        
        if x_posn < CrtComputer.DISPLAY_WIDTH-1:
            self._display_posn[0] += 1
        else:
            self._display_posn[0] = 0
            self._display_posn[1] += 1        
        
    def _start_next_instruction(self):
        """ Takes an instruction, and calls the appropriate implementation method. """
        instruction = self._instructions[self._ip]
        # print(f"Starting instruction: {instruction}")
        
        if instruction[0] == "addx":
            self._doing = [instruction, 2]
        elif instruction[0] == "noop":
            self._doing = [instruction, 1]

        self._ip += 1  # increment the instruction pointer
        if self._ip == len(self._instructions): # we've finished
            self.running_program = False
    
    def _op_addx(self, instruction: tuple):
        """ Takes 2 cycles. Adds val to register x """
        self._x += instruction[-1]

    def _op_noop(self, _: tuple):
        """ Takes 1 cycle. Does nothing. Instruction parameter will be empty. """
    
    def __repr__(self):
        return f"{self.__class__.__name__}(Cycle={self.cycle};x={self._x},pixel={self._display_posn})"

    def render_display(self):
        return "\n".join("".join(row) for row in self._display)

    def render_as_plt(self):
        """ Render the display as a scatter plot """
        
        all_points = [(x,y) for x in range(CrtComputer.DISPLAY_WIDTH)
                            for y in range(CrtComputer.DISPLAY_HEIGHT)
                            if self._display[y][x] == CrtComputer.LIT]
        
        x_vals, y_vals = zip(*all_points)
        
        axes = plt.gca()
        axes.set_aspect('equal')
        plt.axis("off") # hide the border around the plot axes
        axes.set_xlim(min(x_vals)-1, max(x_vals)+1)
        axes.set_ylim(min(y_vals)-1, max(y_vals)+1)
        axes.invert_yaxis()
        
        axes.scatter(x_vals, y_vals, marker="o", s=50)
        plt.show()
        
def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    # Part 1
    interesting_cycles = [20, 60, 100, 140, 180, 220]
    signal_strength_sum = 0
    crt_computer = CrtComputer(data)
    while crt_computer.running_program:
        crt_computer.tick()
        if crt_computer.cycle in interesting_cycles:
            signal_strength_sum += crt_computer.signal_strength
    
    print(f"Part 1: {signal_strength_sum}")
    print(f"Part 2:\n{crt_computer.render_display()}")
    crt_computer.render_as_plt()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
