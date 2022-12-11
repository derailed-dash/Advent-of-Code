"""
Author: Darren
Date: 11/12/2022

Solving https://adventofcode.com/2022/day/11

Monkeys have my stuff! They each have a number of my items. 
The input data gives tells us how worried we are about each item.
The monkeys are throwing my items to each other. 
The input data specifies the rules for how a monkey inspects each item in order,
how our worry score is affected, and then which other monkey the item gets thrown to.
A game round = each monkey plays in order; each monkey inspects and throws each item, in order.

Part 1:

Count how many times each monkey inspects my items.
Monkey business = the product of this count from the two monkeys with the greatest count.
Determine monkey business for 20 rounds.

Solution:
- Create a Monkey class which:
  - Stores id, items (list), worry operation (str), test divisor, and inspection count.
  - Has an `inspect()` method which:
    - Increases inspect count
    - Retrieves the worry score for the first item stored
    - Performs the worry operation, which changes the worry score for this item
    - Performs the "relief" step, i.e. dividing by 3 and rounding down.
    - Performs the test by checking if the modulus of the divisor is 0, 
      and setting the target monkey accordingly.
- Read in the input data and create a list of Monkeys from this data.
- Perform 20 rounds:
  - Iterate through each monkey in order.
    - Perform the inspect and item transfer, for each item this monkey has.
- Determine the final inspect_count for each monkey. Return the product of the two largest counts.

Part 2:

Worry level is no longer reduced after inspection.
Caclulate monkey business for 10000 rounds.

The problem here is that with the Part 1 solution, the worry scores get very, very fast.
This solution is going to take too long. We need a way to make these scores smaller.
A≡B(mod C)
A is congruent to B mod C.
≡ means "is congruent to". I.e. that it belongs in the same remainder class, or bucket.
Numbers are "congruent modulo n" if they have the same remainder after division.
If a≡b(mod M) and b=d(mod m) then a≡d(mod m)
If a≡b(mod m), then a+c≡b+c(mod m)
If a≡b(mod m), then ax≡bx(mod mx)

Modulo congruence is preserved with addition and multiplication (in our worry op).
And we're not dividing any more, which would break conguence.
So we only need to maintain a number which preserves the remainder, not the actual worry score.
So, we can just store %w(mod n). And for n, we can use the LCM of all our divisors.
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
    lcm = math.lcm(*[monkey.divisor for monkey in monkeys.values()])
    # Note that here, the lcm is actually the product of these numbers, since they are all prime.
    # But in general, we would want to use LCM.
    monkey_business = play(monkeys, 10000, relief=False, lcm=lcm)
    print(f"Part 2: monkey business={monkey_business}")

def play(monkeys: dict[int, Monkey], rounds_to_play: int, relief=True, lcm=None) -> int:
    """ Play required number of rounds.
    Returns 'Monkey Business' = product of the top two inspection counts """
    for _ in tqdm(range(1, rounds_to_play+1)):
        for monkey in monkeys.values(): # Iterator through monkeys in order
            while monkey.start_items: # Monkey inspects and throws until it has no more items
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
