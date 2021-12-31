"""
Author: Darren
Date: 13/06/2021

Solving https://adventofcode.com/2016/day/10
    Bots take chips from input bins.
    Bots give chips to other bots, or output bins.
    Bots only proceed when they carry two chips.
    
Sample input:
    value 5 goes to bot 2
    bot 2 gives low to bot 1 and high to bot 0
    value 3 goes to bot 1
    bot 1 gives low to output 1 and high to bot 0
    bot 0 gives low to output 2 and high to output 0
    value 2 goes to bot 2

Part 1:
    Create a Bot class that knows how to add values, and how to pop low and high values.
    The Bot also knows how to check if two values are currently compared by it.  
    It does this by converting its own values, and the values to check, into sets.
    
    Parse all instructions by regex.
    
    Loop through all instructions until no instructions left
    We'll remove processed instructions by adding them to a list on each loop, 
    and then removing from outer instr set using a filter.
    
    for instr in current_instrs
        If BOT_GIVES
            If bot is full, execute and add to remove_list, else ignore
            While we're here, check if the two specified values are compared by this bot.
        
        If VALUE
            If bot is not full, execute and add to remove list, else ignore

Part 2:
    We just need to determine product of Outputs 0, 1 and 2.  Really easy, since we stored these as we went along, in a dict.
"""
from __future__ import absolute_import
import logging
import os
import time
import re

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

value_pattern = re.compile(r"value (\d+) goes to bot (\d+)")
bot_gives_pattern = re.compile(r"bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)")

CHECK_VALS = [61, 17]

class Bot:
    """ A bot picks up microchips from inputs, or from other bots.
    When a bot has two microchips, it is able to give those microchips to other bots, or to outputs. 
    External rules tell Bots what to do. """
    
    MAX_VALUES = 2
    
    def __init__(self, num:int) -> None:
        self._num = num
        self._values = []
    
    def add_value(self, value:int) -> None:
        if self.is_full():
            raise ValueError("This bot is full.")
        
        self._values.append(value)
        
    def is_full(self) -> bool:
        if len(self._values) == Bot.MAX_VALUES:
            return True
        
        return False

    def _pop_val(self, min_or_max) -> int:
        ret_val = min_or_max(self._values)
        self._values.remove(ret_val)
            
        return ret_val
        
    def pop_low(self) -> int:
        return self._pop_val(min)
    
    def pop_high(self) -> int:
        return self._pop_val(max)
            
    @property
    def low(self) -> int:
        return min(self._values)
    
    @property
    def high(self) -> int:
        return max(self._values)
    
    @property
    def num(self) -> int:
        return self._num
    
    def compares(self, values:list) -> bool:
        """ Determine if this bot currently compares the values supplied.
        It does this by converting the supplied values and the internal values to sets, and then comparing those sets.

        Args:
            values (list): Check if these supplied values are currently compared by this bot.

        Returns:
            bool: Whether these values are currently compared or not.
        """
        if set(self._values) == set(values):
            return True

        return False   
    
    def __eq__(self, other):
        return self.num == other.num
    
    def __hash__(self):
        return hash(self.num)
        
    def __str__(self):
        return f"Bot {self.num}"
    
    def __repr__(self):
        return f"Bot {self.num}: Values={sorted(self._values)}"


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        all_instructions = f.read().splitlines()
    
    # Part 1   
    logging.debug(all_instructions)
    filtered_list = all_instructions
    
    bots = {}       # store bot_num: bot
    outputs = {}    # store output: value
    
    while filtered_list:
        remove_list = []
        for instr in filtered_list:
            logging.debug("Processing: %s", instr)

            # value (\d+) goes to bot (\d+)
            # but only if the bot isn't full      
            if (match := value_pattern.match(instr)):
                value, bot_num = [int(x) for x in match.groups()]
                
                bot = make_or_get_bot(bots, bot_num)
                
                if not bot.is_full():
                    bot.add_value(value)
                    logging.debug("Added %d to %s", value, bot)
                    remove_list.append(instr)    
                
                continue
            
            # bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)  
            # But only if the src bot is full and the target bots are not full
            if (match := bot_gives_pattern.match(instr)):
                bot_num, low_type, low_num, high_type, high_num = match.groups()
                bot_num, low_num, high_num = map(int, [bot_num, low_num, high_num])

                src_bot = make_or_get_bot(bots, bot_num)

                if src_bot.is_full():
                    if src_bot.compares(CHECK_VALS):
                        logging.info("Part 1: %s compares %s", src_bot, CHECK_VALS)
                    
                    try:
                        # check if either target is a bot, and if so, that all target bots are not full
                        for tgt_type, tgt_num in zip([low_type, high_type], [low_num, high_num]):
                            if tgt_type == "bot":
                                tgt_bot = make_or_get_bot(bots, tgt_num)
                                if tgt_bot.is_full():
                                    raise TypeError("Target bots have no space")
                    except TypeError as err:
                        logging.debug(err)
                        
                        # can't process this instruction, so move on
                        continue
                    
                    if low_type == "bot":
                        low_tgt = make_or_get_bot(bots, low_num)
                        low_tgt.add_value(popped_val := src_bot.pop_low())
                        logging.debug("Added %d to %s", popped_val, low_tgt)
                    else:
                        outputs[low_num] = (popped_val := src_bot.pop_low())
                        logging.debug("Added %d to output %s", popped_val, low_num)
                    
                    if high_type == "bot":
                        high_tgt = make_or_get_bot(bots, high_num)
                        high_tgt.add_value(popped_val := src_bot.pop_high())
                        logging.debug("Added %d to %s", popped_val, high_tgt)                        
                    else:
                        outputs[high_num] = (popped_val := src_bot.pop_high())
                        logging.debug("Added %d to output %s", popped_val, high_num)                        
                            
                    remove_list.append(instr)
                else:
                    logging.debug("Source bot not ready to give.")
                
                continue
               
        # remove any instructions we've just processed
        filtered_list = list(filter(lambda element: element not in remove_list, filtered_list))
        
    # Part 2
    prod = outputs[0] * outputs[1] * outputs [2]
    logging.info("Part 2: Product of outputs 0, 1, and 2 = %d", prod)


def make_or_get_bot(bots: dict[int, Bot], bot_num: int):
    """ If this bot already exists in bots, then return that bot.
    If not, make it.

    Args:
        bots (dict[int, Bot]): dict of bots
        bot_num (int): bot number

    Returns:
        [Bot]: New or existing bot
    """
    if bot_num in bots:
        bot = bots[bot_num]
    else:
        bot = Bot(bot_num)
        bots[bot_num] = bot
        
    return bot   
    

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
