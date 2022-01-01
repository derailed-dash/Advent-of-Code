"""
Author: Not me
Date: 25/09/2021

Solving https://adventofcode.com/2016/day/20

Solution:
    Found this solution when mine wasn't working for part 2

"""
import logging
import os
import time
import bisect

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

MIN_IP = 0
MAX_IP = 4294967295
# MAX_IP = 35

class IntRange(object):
    '''
    Represents a list of integers.

    Specific values can be allowed (included) / denied (excluded) from the range.
    '''

    def __init__(self, min_ip, max_ip):
        '''Create a new int range with the given values initially allowed.'''

        self._ranges = [(min_ip, max_ip)]

    def __repr__(self):
        '''Pretty print a range (this can get long).'''

        return 'IntRange<{}>'.format(self._ranges)

    def __in__(self, value):
        '''Test if a value is in this int range.'''

        # Slower version
        # return any(lo <= value <= hi for (lo, hi) in self._ranges)

        index = bisect.bisect(self._ranges, (value, value))
        lo, hi = self._ranges[index]
        return lo <= value <= hi

    def __iter__(self):
        '''Return all values in this int range.'''

        for (lo, hi) in self._ranges:
            yield from range(lo, hi + 1)

    def __len__(self):
        '''Return how many values are in this IP range.'''

        return sum(hi - lo + 1 for (lo, hi) in self._ranges)

    def _simplify(self):
        '''Go through current ranges and remove/collapse overlapping ranges.'''

        i = 0
        while i + 1 < len(self._ranges):
            range1_lo, range1_hi = self._ranges[i]
            range2_lo, range2_hi = self._ranges[i + 1]

            # Only guarantee: lo1 is <= lo2

            # There is an overlap, combine and remove range2
            # Continue without incrementing since another range might be collapsed
            if range2_lo <= range1_hi:
                self._ranges[i] = (range1_lo, max(range1_hi, range2_hi))
                del self._ranges[i + 1]
                continue

            i += 1

    def allow(self, allow_min, allow_max):
        '''Add a new range of allowed values.'''

        # Insert sorted (using bisect) then simplify
        bisect.insort(self._ranges, (allow_min, allow_max))
        self._simplify()

    def deny(self, deny_min, deny_max):
        '''Remove a range of (possibly) previously allowed values.'''

        i = 0
        while i < len(self._ranges):
            lo, hi = self._ranges[i]

            # Range is completely denied
            if deny_min <= lo <= hi <= deny_max:
                del self._ranges[i]
                continue

            # Denial is completely within the range, split it
            elif lo <= deny_min <= deny_max <= hi:
                del self._ranges[i]
                self._ranges.insert(i, (lo, deny_min - 1))
                self._ranges.insert(i + 1, (deny_max + 1, hi))

            # Partial overlap, adjust the range
            elif lo <= deny_min <= hi:
                self._ranges[i] = (lo, deny_min - 1)

            elif lo <= deny_max <= hi:
                self._ranges[i] = (deny_max + 1, hi)

            i += 1

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    ips = IntRange(MIN_IP, MAX_IP)

    for line in data:
        blacklist_min, blacklist_max = map(int, line.split("-"))
        ips.deny(blacklist_min, blacklist_max)
    
    for ip in ips:
        logging.info(f"First IP: {ip}")
        break

    logging.info(f"Number of allowed IPs: {len(ips)}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
