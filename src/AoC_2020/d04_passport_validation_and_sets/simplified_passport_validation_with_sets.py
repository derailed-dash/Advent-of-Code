""" Passport_Validation.py
Author: Darren
Date: 06/12/2020

Solving: https://adventofcode.com/2020/day/4

Each passport is represented as a sequence of key:value pairs 
separated by spaces or newlines. Passports are separated by blank lines.
E.g.

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

Solution 2 of 2:
    Read in all K:V pairs and store in a list of dicts, using comprehension.
    Use set issuperset() to check if passports contain all required fields.
    Process all K:V pairs to determine if passport is valid.
"""

import sys
import os
import time
import re
from pprint import pprint as pp

PASSPORT_INPUT_FILE = "input/passports.txt"
SAMPLE_INPUT_FILE = "input/sample_data.txt"

# passport fields
BIRTH_YEAR = "byr"
ISSUE_YEAR = "iyr"
EXP_YEAR = "eyr"
HEIGHT = "hgt"
HAIR_COLOR = "hcl"
EYE_COLOR = "ecl"
PASSPORD_ID = "pid"

# North Pole Credentials don't need cid 
COUNTRY_ID = "cid"

dict_keys = [
    BIRTH_YEAR,
    ISSUE_YEAR,
    EXP_YEAR,
    HEIGHT,
    HAIR_COLOR,
    EYE_COLOR,
    PASSPORD_ID,
    COUNTRY_ID
]

count_passports_processed = 0
count_passports_valid = 0
count_passports_invalid = 0

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, PASSPORT_INPUT_FILE)
    print("Input file is: " + input_file)
    
    passports = read_input(input_file)

    # don't need cid to be valid
    required_fields = {BIRTH_YEAR, ISSUE_YEAR, EXP_YEAR, HEIGHT, HAIR_COLOR, EYE_COLOR, PASSPORD_ID}
    
    # count all the passports that contain required_fields
    count_valid_ignoring_cid = sum(set(passport.keys()).issuperset(required_fields) for passport in passports)
    print(f"Part 1: Valid, ignoring CID: {count_valid_ignoring_cid}")

    validate_passports(passports, dict_keys)

    print("Total passwords processed: " + str(count_passports_processed))
    print("Total passwords valid: " + str(count_passports_valid))
    print("Total passwords invalid: " + str(count_passports_invalid))


def passport_is_valid(passport, keys):
    # recall each passport is a dict of K:V pairs
    for k in keys:
        if k not in passport:
            if (k == COUNTRY_ID):
                # we don't care, sow we're going to ignore this
                continue
            else:
                # key is missing, so this passport is invalid
                return False
        else:
            # this key is included in the passport, so let's validate the value
            if (k == BIRTH_YEAR):
                try:
                    value = int(passport[k])
                    if ((value < 1920) or (value > 2002)):
                        #print(f"Issue with {k} and {value}")
                        return False

                except ValueError:
                    #print(f"Issue with {k} and {value}")
                    return False

            elif (k == ISSUE_YEAR):
                try:
                    value = int(passport[k])
                    if ((value < 2010) or (value > 2020)):
                        #print(f"Issue with {k} and {value}")
                        return False

                except ValueError:
                    #print(f"Issue with {k} and {value}")
                    return False

            elif (k == EXP_YEAR):
                try:
                    value = int(passport[k])
                    if ((value < 2020) or (value > 2030)):
                        #print(f"Issue with {k} and {value}")
                        return False

                except ValueError:
                    #print(f"Issue with {k} and {value}")
                    return False

            elif (k == HEIGHT):
                value = str(passport[k])
                if (len(value) < 4):
                    #print(f"Issue with {k} and {value}")
                    return False

                units = value[-2:].lower()
                if (units == "cm"):
                    try:
                        height = int(value[:-2])
                        if ((height < 150) or (height > 193)):
                            #print(f"Issue with {k} and {value}")
                            return False

                    except ValueError:
                        #print(f"Issue with {k} and {value}")
                        return False
                elif (units == "in"):
                    try:
                        height = int(value[:-2])
                        if ((height < 59) or (height > 76)):
                            #print(f"Issue with {k} and {value}")
                            return False

                    except ValueError:
                        #print(f"Issue with {k} and {value}")
                        return False
                else:
                    print(f"Issue with {k} and {value}")
                    return False

            elif (k == HAIR_COLOR):
                # validate the value uses #hhhhhh colour convention
                value = str(passport[k])
                if (len(value) != 7):
                    #print(f"Issue with {k} and {value}")
                    return False
                else:
                    match = re.search(r'^#(?:[0-9a-f]{3}){1,2}$', value)
                    if (not match):
                        #print(f"Issue with {k} and {value}")
                        return False
                
            elif (k == EYE_COLOR):
                value = str(passport[k])
                VALID_EYE_COLOURS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
                if (value not in VALID_EYE_COLOURS):
                    #print(f"Issue with {k} and {value}")
                    return False

            elif (k == PASSPORD_ID):
                # 9 digit number including zeroes
                value = str(passport[k])
                match = re.search(r'^\d{9}$', value)
                if (not match):
                    #print(f"Issue with {k} and {value}")
                    return False
            elif (k == COUNTRY_ID):
                # don't bother validating
                pass
            else:
                print(f"Something unexpected. Key was {k}.")

    return True        


def validate_passports(passports, keys):
    global count_passports_invalid, count_passports_valid, count_passports_processed
    
    for passport in passports:
        count_passports_processed += 1
                 
        if (passport_is_valid(passport, keys)):
            count_passports_valid += 1
        else:
            count_passports_invalid += 1


def read_input(a_file):
    """
    Input file is composed of multiple password blocks.
    Each block is separated by an empty line.
    Each block is composed of multiple K:V pairs, which may be separated by space or newline
    I.e. each entry looks like this:
    hgt:189cm byr:1987 pid:572028668 iyr:2014 hcl:#623a2f
    eyr:2028 ecl:amb
    """
    # Build a list of dicts, where each element is a single passport
    passports = []
    with open(a_file, mode="rt") as f:
        list_of_passports = f.read().split("\n\n")
        passports = [dict(kv.split(":") for kv in entry.split()) for entry in list_of_passports]

    return passports


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
