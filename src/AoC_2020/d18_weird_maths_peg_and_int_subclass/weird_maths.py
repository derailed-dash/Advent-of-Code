"""
Author: Darren
Date: 18/12/2020

Solving: https://adventofcode.com/2020/day/18

Solution 1 of 3:
    Regex to process each line as digits and operators (tokens)
    Recursively eliminate brackets, each time evaluating inside the brackets, until it evaluates to a value.
    Then, perform addition over multiplication using a simple state machine that performs the addition loop first.
    The addition loop strips out all x+y and replaces with the evaluated results.
    Finally, the multiplication loop does what's left.

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
import re
from pprint import pprint as pp

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/math_puzzle.txt"
SAMPLE_INPUT_FILE = "input/test_math_puzzle.txt"


def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input = read_input(input_file)
    
    results = process_input(input)
    pp(results)
    print(f"Sum of results: {sum(results)}")


def process_input(input):
    tokenizer = re.compile(r'\s*([()+*/-]|\d+)')

    results = []

    for line in input:
        # first, let's get all our tokens.  I.e. operators and digits.
        # Match 0 or more spaces, followed by capture group 1, which is:
        # any character set of 1 or more ()+*/- as operator tokens OR any digit
        expr_tokens = []
   
        current_pos = 0
        while current_pos < len(line):
            match = tokenizer.match(line, current_pos)
            # we match group 1, thus eliminating any whitespace matches
            expr_tokens.append(match.group(1))
            current_pos = match.end()
        
        # print(f"Processing {''.join(expr_tokens)}")
        results.append(process_weird_expr(expr_tokens))

    return results


def process_weird_expr(expr_tokens):
    # Rules: evaluate left to right; addition BEFORE multiplication; brackets take precedence

    # first let's eliminate the brackets
    expr_tokens = convert_inner_expressions(expr_tokens)

    # we've stripped the brackets.  So evaluate left to right
    result = process_inner_expression_add_over_prod(expr_tokens)

    # print(f"Intermediate result: {left_num}")
    return result


def process_inner_expression_add_over_prod(expr_tokens):
    # do addition first
    # iterate until we've done all the additions
    # replace x+y tokens with the evaluation as we go
    while "+" in expr_tokens:
        left_num = None
        right_num = None
        op = ""
        the_sum = 0
        for i, token in enumerate(expr_tokens):
            if token.isdigit():
                if left_num is None:
                    left_num = int(token)
                    left_posn = i
                else:
                    right_num = int(token)
                    right_posn = i

                    if op == "add":
                        the_sum = left_num + right_num

                        # substite sum for the previous terms
                        expr_tokens[left_posn:right_posn+1] = [str(the_sum)]

                        # break out of this loop and start next iteration
                        # otherwise we're continuing to process a list we've modified!
                        break
                    elif op == "prod":
                        left_num = right_num
                        left_posn = i

            elif token == "+":
                op = "add"
            elif token == "*":
                op = "prod"

        # print(f"Intermediate: {''.join(expr_tokens)}")
    
    # now multiplication; there should be no + left at this point
    left_num = None
    right_num = None
    for token in expr_tokens:
        if token.isdigit():
            if left_num is None:
                left_num = int(token)
            else:
                right_num = int(token)
                left_num = left_num * right_num

    return left_num


def process_inner_expression(expr_tokens):
    left_num = None
    right_num = None
    op = ""
    for token in expr_tokens:
        if token.isdigit():
            if left_num is None:
                left_num = int(token)
            else:
                right_num = int(token)
                if op == "add":
                    left_num = left_num + right_num
                elif op == "prod":
                    left_num = left_num * right_num

        elif token == "+":
            op = "add"
        elif token == "*":
            op = "prod"
    return left_num


def convert_inner_expressions(expr_tokens):
    # keep going recursively, from outside in, until there are no more brackets
    while "(" in expr_tokens:
        bracket_count = 0
        outside_left_bracket = None

        for i, token in enumerate(expr_tokens):
            if token == "(":
                # see if this is the first bracket
                if outside_left_bracket is None:
                    outside_left_bracket = i

                # increment out bracket counter
                bracket_count += 1
            elif token == ")":
                # decrement our bracket counter
                bracket_count -= 1

                # if we get to 0, then we've reached the matching outer bracket
                if (bracket_count) == 0:
                    outside_right_bracket = i

                    # get the expression within the outer brackets
                    outer_bracket_expr = expr_tokens[outside_left_bracket+1:outside_right_bracket]

                    # recurse until we reach the innermost expression
                    result = str(process_weird_expr(outer_bracket_expr))

                    # replace the brackets with the recursive evaluation
                    expr_tokens[outside_left_bracket:outside_right_bracket+1] = [result]
                    # print("".join(expr_tokens))
                    break
    
    return expr_tokens


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines   


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
