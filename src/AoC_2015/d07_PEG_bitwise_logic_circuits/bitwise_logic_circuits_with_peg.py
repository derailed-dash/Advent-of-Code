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
import os
import time
import re
from functools import reduce
from parsimonious import Grammar, NodeVisitor, ParseError, VisitationError

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

# define the grammar rules
# EXPR matches any whole line
# Note, wires can be one or two chars in name, e.g. a, aa, xy.
grammar = Grammar(r"""
    expr = input? (op input)? feeds wire
    input = (number / wire) ws+
    op = ("AND" / "OR" / "LSHIFT" / "RSHIFT" / "NOT") ws+
    number = ~r"\d+"
    feeds = "-> "
    wire = ~r"[a-z]{1,2}"
    ws = ~"\s"
""")

class BitwiseLogicVisitor(NodeVisitor):
    """ PEG Parser for processing the Bitwise instructions """
    # override the parse method, to initialise instance variables and perform the bitwise logic
    def parse(self, *args, **kwargs):
        ''' First arg is the string to be parsed
            Second arg is expected to be a dict that maps wire names to wire values
        '''
        self._wires_dict = args[1]
        self._inputs = []
        self._op = ""
        self._target_wire = ""
        self._processing_input = True
        self._output = {}

        # call the super.  Note that it errors if you try to pass in the dict we received.
        # That's why we're only passing through the first arg, i.e. the string to be parsed.
        super().parse(args[0], **kwargs)

        # perform bitwise operation on the values in the _inputs list
        if "AND" in self._op:
            res = reduce(lambda a,b :a & b, self._inputs)
        elif "OR" in self._op:
            res = reduce(lambda a,b :a | b, self._inputs)
        elif "LSHIFT" in self._op:
            res = reduce(lambda a,b :a << b, self._inputs)
        elif "RSHIFT" in self._op:
            res = reduce(lambda a,b :a >> b, self._inputs)
        elif "NOT" in self._op:
            # The ~ operator in Python may return a signed -ve value.
            # We don't want this, so we & with 16 bit of 1s to convert to +ve representation
            res = ~self._inputs[0] & 0xFFFF
        else:
            # In reality, this is likely just passing through a list with only one value
            res = sum(self._inputs)

        self._output[self._target_wire] = res
        # print(f"Inputs were: {self._inputs}, op was: {self._op}, result: {self._output}")   

        # Wire name and wire value, as dict
        return self._output

    def visit_expr(self, node, visited_children):
        # here we can print the overall expr being parsed
        # print(f"EXPR Node: {node}; visited_children: {visited_children}")
        pass

    def visit_input(self, node, visited_children):
        pass

    def visit_feeds(self, node, visited_children):
        # change state so that the next WIRE we parse is treated as output
        self._processing_input = False

    def visit_op(self, node, visited_children):
        self._op = node.text.strip()       
        return self._op

    def visit_number(self, node, visited_children):
        number = int(node.text)
        self._inputs.append(number)
        return number

    def visit_wire(self, node, visited_children):
        # a wire is always passed as a str designation.

        wire = node.text.strip()
        if (self._processing_input):
            # if we have an input wire, then it must have a value stored in the dict
            self._inputs.append(self._wires_dict[wire])
        else:
            # otherwise, this is an output wire
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
    print(f"Part 1: Value of input a is {a_val}")

    # Part 2
    wire_b_instr = list(filter(re.compile(r"-> b$").search, data))
    wire_b_instr_index = data.index(*wire_b_instr)
    data[wire_b_instr_index] = f"{a_val} -> b"

    results = process_instructions(data.copy(), blc_visitor)
    print(f"Part 2: Value of input a is {results['a']}")

def process_instructions(data, blc_visitor):
    results = {}

    # treat all our input as a stack.  
    # Some input values will not be known yet, so park these instructions and try on the next iteration
    while data:
        not_ready_to_parse = []

        for i, line in enumerate(data):
            # print(blc_visitor.grammar.parse(line))
            try:
                results.update(blc_visitor.parse(line, results))
                # if we're here, the instruction parsed successfully, so remove it from the stack permanently
                data.pop(i)
            except (ParseError, VisitationError, KeyError):
                # if the parser tries to retrieve a wire value that is not yet known
                # a KeyError is thrown, caught, and rethrown as a VisitationError, which we catch here
                # add this instruction to the list we can't yet parse, and move on to the next instruction
                not_ready_to_parse.append(data.pop(i))
                continue

        # We're ready to process the list again.  
        # Add back in all the instructions we failed to parse last time
        data.extend(not_ready_to_parse)
    
    return results

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
