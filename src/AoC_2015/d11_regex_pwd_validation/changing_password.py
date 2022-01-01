""" 
Author: Darren
Date: 01/02/2021

Solving https://adventofcode.com/2015/day/11

Increment 8 lowercase char password, from right to left, but following rules:
    - One straight of at least three letters (e.g. bcd)
    - No i, o, l
    - At least two different, non-overlapping pairs of chars, e.g. aa, bb, zz

Solution:
    For the password incrementor, use a recursive function that increments the rightmost column,
    and which recursively processes the [password-last column], when we wrap the last column.

    Regex to match char straights, two pairs of chars, and to exclude certain chars.
    For the two pairs, return them and check they're not the same.  E.g. bb and bb is no good.
"""
import time
import re

# validate straight
STRAIGHT_MATCH = re.compile(r"abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz")
# Two non-overlapping pairs of any character
PAIRS_CHARS_MATCH = re.compile(r"(.)\1.*(.)\2")
# match any of i, o, u
BAD_CHARS_MATCH = re.compile(r"[iol]")

def main():
    old_pwd = 'cqjxjnds'

    new_pwd = find_next_password(old_pwd)
    print(new_pwd)

    new_pwd = find_next_password(new_pwd)
    print(new_pwd)


def find_next_password(new_pwd: str):
    new_pwd_valid = False
    while not new_pwd_valid:
        try:
            new_pwd = increment_pwd(new_pwd)
            new_pwd_valid = check_rules(new_pwd)
        except IndexError:
            # thrown if we reach all z
            print("Max value reached")
            break
    return new_pwd


def increment_pwd(pwd):
    # increment password char from the rightmost column
    last_col = len(pwd) - 1
    char = pwd[last_col]
    left_pwd = pwd[:last_col]
    new_char = next_char(char)

    if (new_char) == 'a':
        # We've rolled over from z to a, so we need to increment one column left
        # So pass in all left pwd chars, exluding rightmost column, and call this method recursively
        left_pwd = increment_pwd(left_pwd)
    
    new_pwd = left_pwd + new_char
    return new_pwd


def next_char(a_char: str):
    if (a_char != 'z'):
        # get ascii code, add 1, then convert back to a char
        return chr(ord(a_char)+1)
    else:
        # if we're incrementing 'z', then we need to wrap around to 'a'
        return 'a'


def check_rules(input):
    if not STRAIGHT_MATCH.search(input):
        return False

    if BAD_CHARS_MATCH.search(input):
        return False
        
    two_pairs_match = PAIRS_CHARS_MATCH.search(input)
    if not two_pairs_match:
        return False
    else:
        pair_one, pair_two = two_pairs_match.groups()
        if pair_one == pair_two:
            # the two pairs must be different, e.g. aa and bb, but not aa and aa
            return False

    return True


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
