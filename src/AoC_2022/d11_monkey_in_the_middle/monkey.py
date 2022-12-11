"""
Author: Darren
Date: 11/12/2022

Solving https://adventofcode.com/2022/day/11

Part 1:

Part 2:

"""
from __future__ import annotations
from collections import Counter
import copy
import math
import operator
from pathlib import Path
import time
import re
from tqdm import tqdm

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

class Monkey:
    """ The monkey has a bunch of my things. 
    start_items = worry level for each item, in the order they will be inspectd
    worry_op = how worry level changes as the monkey inspects the item
    """
    def __init__(self, monkey_id: int, items: list, worry_op: str, div: int, throw_to: list) -> None:
        self.monkey_id = monkey_id # E.g. 0
        self.start_items = items # E.g. [79, 98]
        self._worry_op = worry_op  # E.g. old * 19
        self.divisor = div  # E.g. 13
        self._throw_to = throw_to # E.g. [2, 3]
        self.inspect_count = 0
    
    def add_item(self, item:int):
        self.start_items.append(item)
        
    def inspect(self, relief=True, lcm=None) -> int:
        """ Inspects the next item in the list. 
        Inspecting causes our worry level to go up, as given by worry_op. 
        If relief enabled, we then reduce our worry level by //3.
        Then we work out who to throw to, by dividing by a divisor.
        
        In part 2:
          - relief is disabled and worry level can get VERY LARGE!!
          - We can significantly reduce this number by using LCM trick.
         """
        
        self.inspect_count += 1
        
        # turn "old * 19" into "79 * 19"
        worry_op = self._worry_op.replace("old", str(self.start_items[0]))
        
        first, the_op, second = re.findall(r"(\w+) (.) (\w+)", worry_op)[0]
        ops_dict = {
            "+": operator.add,
            "*": operator.mul
        }
        
        self.start_items[0] = ops_dict[the_op](int(first), int(second))
    
        # Relief. Rule = divide by three and round down
        if relief:
            self.start_items[0] //= 3
        
        if lcm:
            self.start_items[0] %= lcm
        
        return self._throw_to[0] if self.start_items[0] % self.divisor == 0 \
                                 else self._throw_to[1]
    
    def throw_to(self, other: Monkey):
        other.add_item(self.start_items.pop(0))
        
    def __repr__(self) -> str:
        return f"Monkey:(id={self.monkey_id}, items={self.start_items}, " \
                + f"inspect_count={self.inspect_count})"

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read()
        
    monkeys = parse_input(data)
    print("\n".join(str(monkey) for id, monkey in monkeys.items()))

    # Part 1
    monkey_business = play(copy.deepcopy(monkeys), 20)
    print(f"Part 1: monkey business={monkey_business}")
    
    # Part 2
    lcm = math.prod(monkey.divisor for monkey in monkeys.values())
    monkey_business = play(monkeys, 10000, relief=False, lcm=lcm)
    print(f"Part 2: monkey business={monkey_business}")

def play(monkeys, rounds_to_play: int, relief=True, lcm=None) -> int:
    """ Play required number of rounds.
    Returns 'Monkey Business' = product of the top two inspection counts """
    for _ in tqdm(range(1, rounds_to_play+1)):
        for monkey in monkeys.values(): # Iterator through monkeys in order
            while monkey.start_items: # Monkey inspects and thorws until it has no more items
                to_monkey = monkeys[monkey.inspect(relief=relief, lcm=lcm)]
                monkey.throw_to(to_monkey)
    
    # Get the two monkeys that have inspected the most
    monkey_inspect = Counter({monkey.monkey_id: monkey.inspect_count for monkey in monkeys.values()})
    two_most_common = monkey_inspect.most_common(2)
    return two_most_common[0][1] * two_most_common[1][1]

def parse_input(data: str) -> dict[int, Monkey]:
    blocks = data.split("\n\n")
    
    monkeys = {}
    for block in blocks:
        for line in block.splitlines():
            if line.startswith("Monkey"):
                monkey_id = int(re.findall(r"(\d+)", line)[0])
                
            if "items:" in line:
                items = list(map(int, re.findall(r"(\d+)", line)))

            if "Operation:" in line:
                worry_op = line.split("=")[-1].strip()
            
            if "Test:" in line:
                divisor = int(re.findall(r"\d+", line)[0])
            
            if "true:" in line:
                to_monkey_true = int(re.findall(r"\d+", line)[0])
            
            if "false:" in line:
                to_monkey_false = int(re.findall(r"\d+", line)[0])
                
        monkey = Monkey(monkey_id=monkey_id, items=items,
                        worry_op=worry_op, div=divisor, 
                        throw_to=[to_monkey_true, to_monkey_false])
        
        monkeys[monkey_id] = monkey
        
    return monkeys
        
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
