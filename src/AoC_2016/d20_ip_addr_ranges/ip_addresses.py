"""
Author: Darren
Date: 25/09/2021

Solving https://adventofcode.com/2016/day/20

Solution:

Part 1:
    Take a set of "IP addresses" from 0 to 4294967295 (inclusive),
    and then remove blacklist ranges, provided in min-max (inclusive) format.
    Sets based on ranges are no good. There are too many items.
    
    So create an object to store allowed ranges as a list of hi, low lists.
    Add deny_ranges from the blacklist, one at a time. 
    With each addition, merge any overlaps or adjacent ranges and keep sorted.
    
    Compute allowed ranges by taking the gaps between all the deny ranges.
    Compute the min value of the lowest allowed range.

Part 2:
    Sum the allowed ranges.
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

MIN_IP = 0
MAX_IP = 4294967295
# MAX_IP = 35

class Allowed_IPs():
    def __init__(self, min_ip, max_ip) -> None:
        self._min_ip = min_ip
        self._max_ip = max_ip
        self._deny_ranges = []
        self._allowed_ranges = []
    
    @property
    def min_ip(self):
        return min(self.allowed_ranges, key=lambda x: x[0])
    
    @property
    def deny_ranges(self):
        return self._deny_ranges
    
    @property
    def allowed_ranges(self):
        """ Computes allowed ranges, if not already computed

        Returns:
            [tuple]: low, high, inclusive count
        """
        if not self._allowed_ranges:
            self._compute_allow_ranges()
            
        return self._allowed_ranges
        
    @property
    def available_ips(self):
        """ Sum of all allowed IPs """
        return sum(rng[2] for rng in self.allowed_ranges)
    
    def add_deny(self, new_min, new_max):
        # logging.debug(f"Adding {new_min}-{new_max}")
        new_range = True
        for deny_range in self.deny_ranges:
            
            if new_max < deny_range[0]-1:
                break   # no point in progressing through further ranges
            
            if deny_range[0]-1 <= new_max <= deny_range[1] and new_min < deny_range[0]:
                deny_range[0] = new_min    # extend existing deny range to the left
                new_range = False
                continue
            
            if deny_range[0] <= new_min <= deny_range[1]+1 and new_max > deny_range[1]:
                deny_range[1] = new_max   # extend existing deny range to the right
                new_range = False
                continue
            
            if deny_range[0] <= new_min and deny_range[1] >= new_max:
                new_range = False
                continue  # new range sits within existing range; nothing to do
            
        if new_range:
            self._deny_ranges.append([new_min, new_max])  # add new range
        
        self.deny_ranges.sort(key=lambda x: x[0])   # sort based on min of range

        # Now look for adjacent ranges with no gaps or overlaps,
        # and extend the lowest range to include the higher range
        remove_ranges = []
        for i in range(len(self.deny_ranges)-1):
            if self.deny_ranges[i+1][0] <= self.deny_ranges[i][1] + 1:  # adjacent or overlap
                self.deny_ranges[i][1] = self.deny_ranges[i+1][1]
                remove_ranges.append(i+1)   # no longer need this adjacent or overlapping range
                
        for rng in remove_ranges:
            self.deny_ranges.pop(rng)
        
    def _compute_allow_ranges(self):
        current_ip = self._min_ip
        
        for deny_rng in self.deny_ranges:
            if current_ip < deny_rng[0]:
                self._allowed_ranges.append([current_ip, deny_rng[0]-1, deny_rng[0]-current_ip])
            
            current_ip = deny_rng[1] + 1
                
        if current_ip <= self._max_ip:
            self._allowed_ranges.append([current_ip, self._max_ip, self._max_ip+1 - current_ip])

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
    
    allowed = Allowed_IPs(MIN_IP, MAX_IP)
    for line in data:
        blacklist_min, blacklist_max = map(int, line.split("-"))
        allowed.add_deny(blacklist_min, blacklist_max)
        
    logging.info(f"Part 1: Min IP = {allowed.min_ip}")
    logging.info(f"Available IPs: {allowed.available_ips}")


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
