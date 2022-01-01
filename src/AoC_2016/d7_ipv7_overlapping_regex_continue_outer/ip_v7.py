"""
Author: Darren
Date: 01/06/2021

Solving https://adventofcode.com/2016/day/7

Part 1:
    Find 'IPs' that support TLS.  Here, TLS means ABBA in a supernet, but not in a hypernet.
    ABBA seq = any four chars where second pair is first pair reversed. ABBA is good.  AAAA is not. 
    
    Obtain strings outside of brackets - called supernet sequences,
        and within brackets - called hypernet sequences.
    Check if any hypernet contains an ABBA sequence.  If so, this line is NOT valid; move on.
    Check if any supernet contains an ABBA sequence.  If so, this line is valid. Add and move on.

Part 2:
    Find 'IPs' that support SSL.  Here, SSL means supernets contain ABA, 
        along with hypernets containing corresponding BAB.
        
    ABA = aba, dad, xyx, zaz, etc.
    BAB = ABA reversed. E.g. bab, ada, yxy, aza, etc.
    
    Crucially, we need to do overlapping matches on the aba regex, 
        which requires using the regex module, rather than re. I.e. so that we can do:
        aba_pattern.findall(supernet, overlapped=True)

"""
import logging
import os
import time
import regex    # enhanced regex lib that supports finding overlapping matches

# pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

# Only match text outside the square bracekts.
# Use (?:xyz) construct to turn this into a non-matching group
non_brackets_pattern = regex.compile(r"(\w+)(?:\[\w*\])*")

# Only match the text within the square brackets
brackets_pattern = regex.compile(r"\[(\w+)\]+")

# ABA match
aba_pattern = regex.compile(r"((.).\2)")

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    # Part 1
    valid_ips = []
    for line in data:
        supernets = non_brackets_pattern.findall(line)
        hypernets = brackets_pattern.findall(line)
        
        # first check we don't have an ABBA in a hypernet seq, i.e. within [...]
        try:
            for hypernet in hypernets:
                # if we find a match, this line is NOT a valid IP. Move on to next line.
                logging.debug("Checking [%s] does not contain an ABBA.", hypernet)
                if contains_abba(hypernet, 4):
                    raise StopIteration()
        except StopIteration:
            continue
        
        try:
            for supernet in supernets:
                # if we find a match, this line is a valid IP. Move on to next line.
                logging.debug("Testing to see if %s contains an ABBA.", supernet)
                if contains_abba(supernet, 4):
                    valid_ips.append(line)
                    raise StopIteration()
        except StopIteration:
            continue
                
    logging.info(f"Part 1: Found {len(valid_ips)} valid TLS IPs.")
    
    # Part 2
    valid_ips = []
    for line in data:
        supernets = non_brackets_pattern.findall(line)
        hypernets = brackets_pattern.findall(line)
        
        # first check for ABAs in the supernet
        try:
            babs = []
            for supernet in supernets:
                # look for ABAs
                # For all ABAs found, create corresponding BABs and store in a list
                # Each match is a list of tuples.  We only want group 0 from each tuple
                aba_matches = aba_pattern.findall(supernet, overlapped=True)
                for aba_match in aba_matches:
                    match_str = str(aba_match[0])
                    # check middle char is different, to avoid matches like "aaa"
                    if match_str[0] != match_str[1]:
                        bab = match_str[1] + match_str[0] + match_str[1]
                        babs.append(bab)             
                
                # Then check if any of those BABs are present in any of the hypernets
                # if so, we've got a valid IP
                for bab in babs:
                    for hypernet in hypernets:
                        if bab in hypernet:
                            valid_ips.append(line)
                            raise StopIteration()
        except StopIteration:
            continue
    
    logging.info(f"Part 2: Found {len(valid_ips)} valid SSL IPs.")
    


def contains_abba(potential: str, abba_size: int) -> bool:
    """ Check whether this string contains an ABBA sequence.
    E.g. abba is valid.  deed is valid.  xyyx is valid. 
    aaaa is not.  aabb is not.  abcd is not.

    Args:
        potential (str): Any str
        abba_size (int): The number of chars in a valid ABBA sequence

    Returns:
        bool: Whether valid ABBA.
    """
    for i in range(len(potential) - abba_size + 1):
        block = potential[i:i+4]
        logging.debug("Block %s", block)
        
        if block[0] != block[1] and block[0:2] == (block[3:1:-1]):
            logging.debug("ABBA found")
            return True
    
    return False    


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
