"""
Author: Darren
Date: 14/12/2021

Solving https://adventofcode.com/2021/day/14

We read in a polymer template (e.g. NNCB) and a list of pair insertion rules, e.g.
CH -> B
HH -> N
CB -> H
NH -> C

E.g. CH becomes CBH, and CB becomes CHB.
Inserted elements are not considered to be part of a pair until the next cycle.
E.g. template   N       N       C       B
     step 1     N   C   N   B   C   H   B
     step 2     N B C C N B B B C B H C B  

Part 1:
    Apply 10 steps of polymerisation, and then find most and least common elements.
    
    We can recursively replace each pair with the new triplet.
    We need to be careful to keep track of how many chars have been inserted,
    in order to index either side properly.

Part 2:
    Takes too long to build the strings with this many iterations.
    Instead, we can just count how many pairs are generated.
    E.g. AB->Z --> AZ + ZB. Store both pairs in a counter.
    Proceed to next iteration and repeat the pair counter.
    Finally, we need to extract unique char counts from the pairs counter.
    Each char will be present as both [pair j][0] and some other pair[k][1].
    So we only need to count the first char of each pair, except for the char at the end.
"""
import logging
import os
import time
from collections import Counter

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read()
        
    template, rules = process_data(data)

    # Part 1
    steps = 10
    res = recursive_replace(steps, template, rules)
    logger.debug("Length of chain: %d", len(res))
    char_counts = Counter(res).most_common()    # [(char1, count1), (char2, count2)...]
    logger.info("Part 1 with recursive replace: Most common count - least common count = %d", 
                char_counts[0][1] - char_counts[-1][1])

    element_counts = count_by_pairs(template, rules, steps).most_common()
    logger.info("Part 1 using pair counting: Most common count - least common count = %d", 
                element_counts[0][1] - element_counts[-1][1])

    # Part 2
    # We just need to count each pair
    steps = 40
    element_counts = count_by_pairs(template, rules, steps).most_common()
    logger.info("Part 2: Most common count - least common count = %d", 
                element_counts[0][1] - element_counts[-1][1])

def count_by_pairs(template, rules, steps) -> Counter:
    """ Expand the pairs according to the supplied rules, for the given number of steps.
    Simply counts how many of each type of pair we have after each step.

    Args:
        input (str): The initial template, e.g. 'NNCB'
        steps (int): How many iterations.
        rules (dict): Dict of {'XY': 'Z', ...}, such that XY becomes XZY """
    pairs_counter = Counter()  # Initialise the counts
    
    # Find each overlapping pair in the template
    for i in range(len(template)-1):  # E.g. NNCB
        pair = template[i:i+2]  # E.g. NN, NC, CB
        pairs_counter[pair] += 1     # increment count for pair, e.g. {'NN': 1, 'NC': 1, ...}

    # With each step, increment counts of all daughter pairs by the count of source pairs
    for _ in range(steps):
        counts_this_step = Counter()
        for pair in pairs_counter:  # E.g. NN, NC..
            # Rule NN -> C converts NN -> NC + CN
            
            # Increment count of new left and right pairs by the count of source pair
            # E.g. count of NC and CN both increment by count of NN
            counts_this_step[pair[0] + rules[pair]] += pairs_counter[pair]  # NB
            counts_this_step[rules[pair] + pair[1]] += pairs_counter[pair]  # BC
        
        pairs_counter = counts_this_step
    
    # We've got counts of pairs, but we need counts of the individual elements
    element_counts = Counter()  # i.e. a counter for each char
    for pair in pairs_counter:  # e.g. NB
        # Apart from the char at the end, 
        # each letter will be both the last char of a pair, and the first letter of another pair.
        # We don't want to double-count, so we only need to count first chars
        element_counts[pair[0]] += pairs_counter[pair]  # N from NC, C from CN, etc

    # The only exception is the last char from the original str, 
    # since it always remains after insertions
    element_counts[template[-1]] += 1
    
    return element_counts

def recursive_replace(steps: int, to_expand: str, rules: dict) -> str:
    """ Replace the given string with a new replacement string, according to the rules.

    Args:
        steps (int): How many iterations. Decremented with each recursion. Recursion ends when step=0.
        input (str): Input str. The str to be replaced at this recursion depth
        rules (dict): Map of XY: Z, such that XY becomes XZY """
    res = to_expand     # E.g. NNCB first iteration, NCN on second iteration, NBC on third...
    chars_inserted = 0  # This grows as we insert horizontally, to allow indexing
    for i in range(len(to_expand)-1):  # sliding window of 2 chars; stop at len-1
        pair = to_expand[i:i+2] # E.g. CB
        if pair in rules:   # if this pair has a valid replacement str
            replacement = pair[0] + rules[pair] + pair[1]   # E.g. CH -> CBH
            insertion_point = i + chars_inserted
            if steps > 1:   # Deeper recursions to go
                # Now recurse into the pair we've just expanded
                replacement = recursive_replace(steps-1, replacement, rules)  
            
            res = res[:insertion_point] + replacement + res[insertion_point+2:]
            
            # Because replacement is recursive, XY could be replaced by a long str
            chars_inserted += len(replacement)-len(pair)
            
    return res
       
def process_data(data: str) -> tuple[str, dict[str, str]]:
    """ Process one row of template, then an empty line, then rows of rules

    Returns:
        tuple[str, dict[str, str]]: (template, rules-dict)
            where rules-dict looks like {'CH':'B', 'HH':'N', ...}
    """
    template, _, rules_lines = data.partition('\n\n')
    rules = {}
    for line in rules_lines.splitlines():
        if len(line) > 0:
            pair, element = line.split(" -> ")
            rules[pair] = element
        
    return template, rules

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
