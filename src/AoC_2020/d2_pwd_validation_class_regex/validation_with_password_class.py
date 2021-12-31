""" 
Author: Darren
Date: 06/12/2020

Solving https://adventofcode.com/2020/day/2

Solution 3 of 3:
    Rows look like "5-7 z: qhcgzzz"
    Refactored using a password class
"""

import sys
import os
import time
import re

pwd_file = "input/pwd_file.txt"
sample_input = "input/sample_input.txt"


class Password():
    # static variables
    pwd_matcher = re.compile(r"^(?P<first>\d+)-(?P<last>\d+) (?P<char_match>[a-z]): (?P<pwd>[a-z]+)")
    
    def __init__(self, pwd_line: str):
        self._fields = Password.pwd_matcher.match(pwd_line).groupdict()
        self._first = int(self._fields['first'])
        self._last = int(self._fields['last'])
        self._policy_char = self._fields['char_match']
        self._pwd = self._fields['pwd']

    def is_valid_for_count(self):
        char_count = self._pwd.count(self._policy_char)
        return (self._first <= char_count <= self._last)

    def is_valid_for_posn(self):
        if (self._first > len(self._pwd)):
            # Password too short
            return False

        first_posn_match = False
        second_posn_match = False

        if (self._pwd[self._first-1] == self._policy_char):
            first_posn_match = True
            
        if (self._pwd[self._last-1] == self._policy_char):
            second_posn_match = True

        # Only valid if first OR second match, i.e. XOR
        if (first_posn_match ^ second_posn_match):
            return True

        return False

    def __str__(self):
        return ",".join(self._fields.values())

    def __repr__(self):
        return ",".join(self._fields.values())


def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, pwd_file)
    # input_file = os.path.join(script_dir, sample_input)
    print("Input file is: " + input_file)
    
    pwd_list = read_input(input_file)
    print("File read.")

    total_pwds = len(pwd_list)
    print("Total passwords to process: " + str(total_pwds))

    passwords = [Password(pwd_row) for pwd_row in pwd_list]
    valid_for_count = sum(password.is_valid_for_count() for password in passwords)    
    valid_for_posn = sum(password.is_valid_for_posn() for password in passwords)
   
    print("\nTotal passwords valid for count: " + str(valid_for_count))
    print("\nTotal passwords valid for posn: " + str(valid_for_posn))    


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        global pwd_list
        pwd_list = f.read().splitlines()

    return pwd_list


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



