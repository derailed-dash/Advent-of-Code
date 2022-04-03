"""
Author: Darren
Date: 19/12/2020

Solving: https://adventofcode.com/2020/day/19

Input is a block of rules followed by a block of messages.  E.g.
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb

Solution 2 of 2:
    Use PEG to perform depth-first recursion of rules.
    The PEG grammar contains all the rules necessary for recursive parsing.  No validation code required.

Part 2:
    Replace rules 8 and 11, resulting in self-referential loops in the rules, 
    which could result in infinite recursion.
    8: 42 | 42 8    - i.e. 42 can repeat
    11: 42 31 | 42 11 31  - i.e. can result in repeating (42 31), or (42 (42 31)+ 31)
"""
import os
import time
import re
from parsimonious.grammar import Grammar
from parsimonious import ParseError

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/data.txt"
SAMPLE_INPUT_FILE = "input/sample_data.txt"

def create_grammar_rule(rule_line: str):
    """ We want to get to:
        RULE0 = RULE4 RULE1 RULE5
        RULE1 = ((RULE2 RULE3) / (RULE3 RULE2))
        RULE2 = ((RULE4 RULE4) / (RULE5 RULE5))
        RULE3 = ((RULE4 RULE5) / (RULE5 RULE4))
        RULE4 = "a"
        RULE5 = "b"

    Convert line:
        Replace any n with RULEn
        Replace all ":" with " =" (There's already a space after the ":")
        Replace any "x yz | ab c" with "((RULEx RULEyz) / (RULEab RULEc))"
        Replace any "|" with "/"
    """
    line = rule_line.strip().replace(":", " =")
    line = re.sub(r"(\d+)", r"RULE\1", line)
    line = re.sub(r"= (.*) \| (.*)$", r"= ((\1) / (\2))", line)

    return line

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    with open(input_file, mode="rt") as f:
        input = f.read()

    rules, messages = process_input(input)

    print("PART 1")
    grammar_rules = "\n".join(map(create_grammar_rule, rules))
    grammar = Grammar(grammar_rules)

    # we don't need to do anything special when we validate each rule.
    # we just need to know many messages can be parsed by rule 0.
    # So we don't need to override NodeVisitor.
    valid_messages = 0
    for message in messages:
        if is_valid_message(grammar, message, valid_messages):
            valid_messages += 1

    print(f"Count of messages that match RULE0: {valid_messages}")

    print("\nPart 2")

    # replace rules 8 and 11
    rules = ["8: 42 | 42 8" if item.startswith("8:") else item for item in rules]
    rules = ["11: 42 31 | 42 11 31" if item.startswith("11:") else item for item in rules]

    grammar_rules = "\n".join(map(create_grammar_rule, rules))
    grammar = Grammar(grammar_rules)

    valid_messages = 0
    for message in messages:
        if is_valid_message(grammar, message, valid_messages):
            valid_messages += 1

    print(f"Count of messages that match RULE0: {valid_messages}")

def is_valid_message(grammar, message, valid_messages):
    try:
        grammar.parse(message)
    except ParseError as err:
        # RULE31 is recursive and tries to consume the whole message
        # we can ignore 31 where it's matching nothing
        if "RULE31" in repr(err) and "match at ''" in repr(err):
            # print(f"*** {message}: {err}")
            return True
        
        return False
    
    return True

def process_input(input):
    """ Returns rules and messages, as lists
        Rules = ['0: 4 1 5', '1: 2 3 | 3 2', etc]
        Messages = ['ababbb', 'bababa', etc]
    """
    # first split the rules block from the messages block
    rules_line, messages_line = input.split("\n\n")

    # then split each blow into a list of sorted rules / messages
    rules = rules_line.splitlines()

    # we want to sort, since we want RULE0 at the top.
    # PEG will start by applying the first rule in the PEG grammar.
    rules.sort(key = lambda x: int(x.split(":")[0]))
    messages = messages_line.splitlines()
    return rules, messages

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
