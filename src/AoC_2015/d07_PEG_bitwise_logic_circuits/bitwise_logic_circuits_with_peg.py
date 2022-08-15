""" 
Author: Darren
Date: 26/01/2021

Solving https://adventofcode.com/2015/day/7

A value, a gate or a wire provide signals to a wire: 1-to-1.
Wires carry 16 bit (0-65535) signals.
Wires can provide a signal to multiple destinations: 1-to-many.

Instructions like:
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i

Solution 1 of 1:
    Use Parsimonious PEG to perform depth-first parsing of instructions.
    Instructions are out of order, so parse what we can, 
    and use a stack to park what we can't process until the next pass.
    For NOT gate, use ~ and then AND with all 1s, to ensure we don't return negative value.

Part 1:
    Just process the instructions, and return the value of wire a.

Part 2:
    Set wire b input signal to be the signal solution to Part 1.
    Solve for a new answer to wire a.
    Requires changing 19138 -> b to <value for a> -> b.
    Use regex to get the index of the only instruction that ends "-> b" and replace the instruction in the data.
    Then re-run the parse.
"""
import logging
import os
import time
import re
from parsimonious import Grammar, NodeVisitor, ParseError, VisitationError

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

# define the grammar rules
# EXPR matches any whole line, e.g. 'k AND m -> n'
# Note, wires can be one or two chars in name, e.g. a, aa, xy.
grammar = Grammar(r"""
    expr = input? (op input)? feeds wire
    input = (number / wire) ws+
    op = ("AND" / "OR" / "LSHIFT" / "RSHIFT" / "NOT") ws+
    number = ~r"\d+"
    feeds = "-> "
    wire = ~r"[a-z]{1,2}"
    ws = ~r"\s"
""")

class BitwiseLogicVisitor(NodeVisitor):
    """ PEG Parser for processing the Bitwise instructions """
    # override the parse method, to initialise instance variables and perform the bitwise logic
    def parse(self, *args):
        """
        Arguments
            args[0] - the str to be parsed. E.g. 'k AND m -> n'
            args[1] - a dict of known wire values 

        Returns:
            [dict] - output wire:value
            
        Raises:
            ParseError, VisitationError
        """
        
        self._wires_dict = args[1]
        
        # These instance variables are updated after we parse the input line
        self._inputs = []             # store int input values, left of the '->'. E.g. [7102, 65023]
        self._op = ""                 # E.g. AND
        self._target_wire = ""        # E.g. n
        self._processing_input = True # Set to False after we process the '->'
        self._output = {}             # Initialise empty wire:value dict

        # Parse out input line, calling our visit_xxx methods
        # This will update our instance variables
        super().parse(args[0])  

        # perform bitwise operation on the values in the _inputs list
        if "AND" in self._op:
            res = self._inputs[0] & self._inputs[1]
        elif "OR" in self._op:
            res = self._inputs[0] | self._inputs[1]
        elif "LSHIFT" in self._op:
            res = self._inputs[0] << self._inputs[1]
        elif "RSHIFT" in self._op:
            res = self._inputs[0] >> self._inputs[1]
        elif "NOT" in self._op:
            # The ~ operator in Python may return a signed -ve value.
            # We don't want this, so we & with 16 bit of 1s to convert to +ve representation
            res = ~self._inputs[0] & 0xFFFF
        else:
            # Where there is no op. E.g. '19138 -> b'
            res = sum(self._inputs)

        self._output[self._target_wire] = res
        # logger.debug("Inputs were: %s, op was: %s, result: %s", self._inputs, self._op, self._output)   

        # Wire name and wire value, as dict
        return self._output

    def visit_expr(self, node, visited_children):
        # here we can print the overall expr being parsed
        # logger.debug("EXPR Node:\n%s\nVisited_children: %s", node, visited_children)
        pass

    def visit_feeds(self, node, visited_children):
        """ Handle '-> '
        Change state so that the next wire  we parse is treated as output
        """
        self._processing_input = False

    def visit_op(self, node, visited_children):
        """ Handle "AND" / "OR" / "LSHIFT" / "RSHIFT" / "NOT"
        """
        self._op = node.text.strip()       
        return self._op

    def visit_number(self, node, visited_children):
        """ A numeric input value """
        number = int(node.text)
        self._inputs.append(number)
        return number

    def visit_wire(self, node, visited_children):
        """ Handle ~r"[a-z]{1,2}"
        A wire is always passed as a str designation. E.g. 'lf'
        Use the _wires_dict to get the numeric value for this wire.
        If we don't have a value, this will result in a KeyError, 
        which will be caught and thrown as a VisitationError. """
        wire = node.text.strip()
        if (self._processing_input):
            # if we have an input wire, then try to extract its numeric value
            self._inputs.append(self._wires_dict[wire])
        else:  # otherwise, this is an output wire
            self._target_wire = wire

        return wire

    def generic_visit(self, node, visited_children):
        return visited_children or node

def main():
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    blc_visitor = BitwiseLogicVisitor()
    blc_visitor.grammar = grammar

    # Part 1
    # Pass in a copy of the input data, as we'll need to parse it again for Part 2
    results = process_instructions(data.copy(), blc_visitor)
    a_val = results['a']
    logger.info("Part 1: Value of input a is %s", a_val)

    # Part 2
    wire_b_instr = list(filter(re.compile(r"-> b$").search, data)) # return only rows that match
    assert len(wire_b_instr) == 1, "There should only be one matching instruction"
    wire_b_instr_index = data.index(wire_b_instr[0])  # the position of this instruction in the list
    data[wire_b_instr_index] = f"{a_val} -> b"  # replace the instruction with this new one

    results = process_instructions(data.copy(), blc_visitor)
    logger.info("Part 2: Value of input a is %s", results['a'])

def process_instructions(instructions, blc_visitor):
    wire_values = {}

    # treat all our input as a stack.  
    # Some input values will not be known yet, so park these instructions and try on the next iteration
    while instructions:
        for i, line in enumerate(instructions):
            try:
                wire_values.update(blc_visitor.parse(line, wire_values))
                # if we're here, the instruction parsed successfully, so remove it from the stack permanently
                popped = instructions.pop(i)
                logger.debug("Processed: %s", popped)
            except (ParseError, VisitationError):
                # If the parser tries to retrieve a wire value that is not yet known
                # a KeyError is thrown, caught, and rethrown as a VisitationError, which we catch here.
                # This instruction can't be processed yet, as we don't have all necessary input values
                continue

        # We're ready to process the list again. 
    
    return wire_values

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
