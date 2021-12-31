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

Solution 1 of 2:
    Use a recursive method that recurses lists of rules.
    At the bottom of the recursion, it replaces a rule number with a rule letter.
    Each rule is processed by popping the next rule off the stack, and comparing with the current char.
    If we're at the bottom of the recursion and matching a letter successfully, 
    we move on to the next character in the string, and match against the remainder of the stack.
"""
import os
import time
from pprint import pprint as pp

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/data.txt"
SAMPLE_INPUT_FILE = "input/sample_data.txt"

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)

    input = read_input(input_file)
    # pp(input)

    rules, messages = process_input(input)
    pp(rules)

    # reverse the rule stack, because we want to pop and process from the right
    # rules[0] will look like [[11, 8]], so index again with 0 to extract the inner list.
    first_rule = list(reversed(rules[0][0]))
    valid_rules_count = 0
    for message in messages:
        # Use a copy of the first_rule, since we create and modify a stack from this
        if validate(message, first_rule.copy(), rules):
            valid_rules_count += 1

    print(f"Sum of valid rules: {valid_rules_count}")


def process_input(input):
    # Creates rules using this structure:
    # 0: [[4, 1, 5]]
    # 1: [[2, 3], [3, 2]]
    # 2: 'a'
    # 3: 'b'
    rules = {}
    messages = []

    processing_rules = True
    for line in input:
        if line == "":
            processing_rules = False
            continue

        if (processing_rules):
            # get the simple rules first
            k, v = line.split(":")
            
            # if a calling-rule
            if '"' not in v:
                tokens = v.split()
                found_or = False
                rule_list_1 = []
                rule_list_2 = []
                for token in tokens:
                    if token == "|":
                        found_or = True
                    else:
                        if found_or:
                            rule_list_2.append(int(token))
                        else:
                            rule_list_1.append(int(token))

                if len(rule_list_2) == 0:
                    rules[int(k)] = [rule_list_1]
                else:
                    rules[int(k)] = [rule_list_1, rule_list_2]
            
            else:
                rules[int(k)] = v.replace('"', '').strip()

        else:
            messages.append(line)
    
    return rules, messages


def validate(msg, rule_stack, rules):
    """ 
    Consider these rules
    0: 2 1 3
    1: 2 3 | 3 2
    2: "a"
    3: "b"

    And data: abab

    The only valid matches would be aabb and abab.
    
    Logic is:
        2 -> a, leaving a, 1, 3.  The a (of 'abab') validates, leaving 1, 3. Remove the a.
        1 -> 2, 3 as first sub rule of 1. Substituting for 1 gives us 2, 3, 3.
             The 2 -> a, giving us a, 3, 3.  This will fail the test against b of 'bab'.
          -> 3, 2 as the second sub rule of 1.  Subtituting for 1 gives us 3, 2, 3.
            This ultimately substittues for bab, which validates.
    """

    # Incoming rule is reversed, so rule stack might be [3, 1, 2]
    # if there are more rules than the length of the message, then validation has failed
    if len(rule_stack) > len(msg):
        return False
    elif len(rule_stack) == 0:
        # we've run out of rules
        # So far so good.  We should have no more rules and no more characters to check.
        return len(rule_stack) == 0 and len(msg) == 0

    # pop the current rule off the stack
    # E.g. if we pop 3, 1, 2, we'll get 2.
    current_rule = rule_stack.pop()

    # If the rule is a string (e.g. 'a' or 'b'), we've reached the 'bottom'
    # Otherwise, we need to recurse to the matching rule
    if isinstance(current_rule, str):
        # check whether first char of msg matches the rule str
        if msg[0] == current_rule:
            # if this validated, we move on to the second char, with the shorter rule stack
            return validate(msg[1:], rule_stack, rules)
    else:
        # not a str, so we need to recurse
        # E.g. if we recurse 2, 1, 3
        # when {2: 'a'}
        for sub_rule in rules[current_rule]:
            # use list concatenation to add the current rule to the rule stack
            # E.g. this might replace [3, 1] with ['a']
            # if a sub_rule fails to validate, then the recursed function will return False, 
            # but this for loop will not return.
            # For this calling function to return False, NONE of the recursed calls in this loop must be valid.
            if validate(msg, rule_stack + list(reversed(sub_rule)), rules):
                return True
    
    # Fall through and return False if we fail to match at 'top' level
    return False


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        lines = f.read().splitlines()
        
    return lines   


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
