"""
Author: Darren
Date: 04/01/2021

Solving: https://adventofcode.com/2020/day/18

E.g. ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2

Solution 3 of 3:
    Using PEG.
    Establish rules.
    Right event handler for each node matched.
    Part 2 just uses a subclass that overrides the visit_EXPR method.

Part 1
------
Rather than evaluating multiplication before addition, 
the operators have the same precedence, and are evaluated left-to-right 
regardless of the order in which they appear.

Part 2
------
Addition is evaluated before multiplication.
"""
import os
import time
import math
from parsimonious import Grammar, NodeVisitor

class WeirdMathVisitor(NodeVisitor):
    """ PEG Parser for handling mathematical operators left to right """
    
    def visit_expr(self, node, visited_children):
        # NUMBER_OR_BRACKETS (OP NUMBER_OR_BRACKETS)+
        # print(f"EXPR: {node.text} => {visited_children}")
        
        left = visited_children[0][0]
        for op_and_right in visited_children[1]:
            op = op_and_right[0]
            right = op_and_right[1][0]
            if op == "+":
                left += right
            if op == "*":
                left *= right

        return left

    def visit_number_or_bracket(self, node, visited_children):
        # (NUMBER / BRACKETS)
        # print(f"NUMBER_OR_BRACKET: {node.text} => {visited_children[0]}")
        return visited_children[0]

    def visit_op(self, node, visited_children):
        # r"\s*([+-/*])\s*"
        # print(f"OP: {node.text.strip()}")
        return node.text.strip()

    def visit_brackets(self, node, visited_children):
        # "(" EXPR ")"
        # print(f"BRACKET: {node.text} => {visited_children[1]}")
        return visited_children[1]

    def visit_number(self, node, visited_children):
        # print(f"NUMBER: {node.text}")
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node

class WeirdMathAdditionOverMultiplicationVisitor(WeirdMathVisitor):
    """ PEG Parser. Addition over multiplication """
    
    def visit_expr(self, node, visited_children):
        # NUMBER_OR_BRACKETS (OP NUMBER_OR_BRACKETS)+
        # print(f"EXPR: {node.text} => {visited_children}")
        
        # store our left value here
        prod_terms = []
        prod_terms.append(visited_children[0][0])

        # we'll end with something like a + b * c + d
        for op_and_right in visited_children[1]:
            op = op_and_right[0]
            right = op_and_right[1][0]
            if op == "+":
                # replace left value with the new l+r value
                prod_terms[-1] += right
            if op == "*":
                # append the right hand value to the list to be multiplied after
                prod_terms.append(right)

        # At this point, all a+b terms have been evaluated, leaving only terms to be multiplied.
        return math.prod(prod_terms)    

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/math_puzzle.txt"
SAMPLE_INPUT_FILE = "input/test_math_puzzle.txt"

grammar = Grammar(r"""
    expr = number_or_brackets (op number_or_brackets)+ "\n"?
    number_or_brackets = (number / brackets)
    brackets = "(" expr ")"
    op = ~r"\s*([+*])\s*"
    number = ~r"\d+"
""")

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)
    input = read_input(input_file)
    # pp(input)
    
    wmv = WeirdMathVisitor()
    sum_results = sum(wmv.visit(grammar.parse(line)) for line in input)
    print(f"Results for left-to-right: {sum_results}")

    wmv = WeirdMathAdditionOverMultiplicationVisitor()
    sum_results = sum(wmv.visit(grammar.parse(line)) for line in input)
    print(f"Result for addition-over-multiplication: {sum_results}")

def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines   

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
