""" 
Author: Darren
Date: 06/12/2020

Solving https://adventofcode.com/2020/day/2

Solution 1 of 3:
    Rows look like "5-7 z: qhcgzzz"
    Basic splitting of strings, based on : and - chars 
"""

import sys
import os
import time

pwd_file = "input/pwd_file.txt"
sample_input = "input/sample_input.txt"


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

    count_pwds_valid = 0
    for pwd_row in pwd_list:
        if password_okay_by_char_count(pwd_row):
            count_pwds_valid = count_pwds_valid + 1

    print("\nTotal passwords valid: " + str(count_pwds_valid))
    print("Total passwords invalid: " + str(total_pwds - count_pwds_valid))

    count_pwds_valid = 0
    for pwd_row in pwd_list:
        if password_okay_by_position(pwd_row):
            count_pwds_valid = count_pwds_valid + 1

    print("\nTotal passwords valid: " + str(count_pwds_valid))
    print("Total passwords invalid: " + str(total_pwds - count_pwds_valid))


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        global pwd_list
        pwd_list = f.read().splitlines()

    return pwd_list


def password_okay_by_char_count(pwd_row):
    """ 
    Process list of rows from a file, where each row contains pwd policy and pwd.
    Pwd is only valid if the indicated character is found between x and y times (inclusive) in the pwd.

    E.g. 5-7 z: qhcgzzz
    This pwd is invalid, since z is only found 3 times, but minimum is 5.
    """
    
    # Each input row looks like "5-7 z: qhcgzzz"
    # Convert each row to a list that looks like ['5-7 z', 'qhcgzzz']
    pwd_policy_and_pwd = [item.strip() for item in pwd_row.split(":")]
    #print(pwd_policy_and_pwd)

    pwd = pwd_policy_and_pwd[1]
    char_counts, _, char_match = pwd_policy_and_pwd[0].partition(" ")
    min_chars, _, max_chars = char_counts.partition("-")
    
    actual_char_count = pwd.count(char_match)
    if (actual_char_count < int(min_chars)) or (actual_char_count > int(max_chars)):
        return False

    return True


def password_okay_by_position(pwd_row):
    """
    Pwd is only valid if the indicated character is found in either the first numbered
    OR second numbered position.  It is not valid if the character is found in both positions.
    The password policy is 1-indexed.

    E.g. 5-7 z: qhcgzzz
    This pwd is invalid, since z is found in BOTH position 5 and position 7.
    """
    pwd_policy_and_pwd = [item.strip() for item in pwd_row.split(":")]
    #print(pwd_policy_and_pwd)

    pwd = pwd_policy_and_pwd[1]
    char_counts, _, char_match = pwd_policy_and_pwd[0].partition(" ")
    first_posn, _, last_posn = char_counts.partition("-")

    if(int(last_posn) > len(pwd)):
        # Password too short
        return False

    first_posn_match = False
    second_posn_match = False

    if (pwd[int(first_posn)-1] == char_match):
        first_posn_match = True
        
    if (pwd[int(last_posn)-1] == char_match):
        second_posn_match = True

    # Only valid if first OR second match, i.e. XOR
    if (first_posn_match ^ second_posn_match):
        return True

    return False


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")



