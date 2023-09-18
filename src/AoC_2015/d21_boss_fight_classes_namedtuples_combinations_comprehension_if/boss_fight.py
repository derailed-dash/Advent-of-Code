""" 
Author: Darren
Date: 23/03/2021

Solving https://adventofcode.com/2015/day/21

Alternating turns for player vs boss.
Loser is first for hit points to reach 0.
Hit points lost = attacker damage - defender armor
(A minimum of 1 hit point lost in any attack.)

Solution:
    Shop class to store all possible items from the shop.
    Shop class determines valid combos of items.
    Build players using all valid combos, and determine the cost of each combo.
    Establish whether the player will beat another player (the boss), by following game rules.

Part 1:
    Determine cheapest winning loadout.

Part 2:
    Determine most expensive losing loadout.

"""
from __future__ import annotations
import copy
from dataclasses import dataclass
import logging
import itertools
import time
import re
from os import path
from itertools import combinations
from player import Player
import aoc_common.aoc_commons as td

locations = td.get_locations(__file__)
logger = td.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)

BOSS_FILE = "boss_stats.txt"
SHOP_FILE = "shop.txt"

@dataclass(frozen=True)
class Item:
    """ Immutable class for the properties of shop items """
    name: str
    cost: int
    damage: int
    armor: int

class Shop:
    """ Represents all the items that can be bought in the shop """

    def __init__(self, weapons: dict, armor: dict, rings: dict):
        """ Stores all_items as a dict to map the item name to the properties.
        Then computes all valid combinations of items, as 'loadouts'
        """
        self._weapons = weapons # {'Dagger': Item(name='Dagger', cost=8, damage=4, armor=0)}
        self._armor = armor     # {'Leather': Item(name='Leather', cost=13, damage=0, armor=1)}
        self._rings = rings     # {'Damage +1': }
        
        self._all_items = weapons | armor | rings # merge dictionaries
        
        self._loadouts = self._create_loadouts()

    def _create_loadouts(self):
        """ Computes all valid loadouts, given the items available in the shop. Rules:
            - All loadouts have one and only one weapon
            - Loadouts can have zero or one armor
            - Loadouts can have zero, one or two rings.  (But each ring can only be used once.)
        """
        loadouts = []        
        weapon_options = list(self._weapons) # Get a list of the 5 weapon names
        armor_options = [None] + list(self._armor) # Get a list of the 6 allowed armor options

        # build up the ring options.  Start by adding zero or one ring options.
        # E.g. [[None], [Damage +1], [Damage +2]...]
        ring_options = [[None]] + [[ring] for ring in self._rings] 
        # And now add combinations (without duplicates) if using two rings
        for combo in combinations(self._rings, 2):
            ring_options.append([combo[0], combo[1]]) # Append, e.g. ['Damage +1', 'Damage +2']

        # Now we have 5 weapons, 6 armors, and 22 different ring combos
        # smash our valid options together to get a list with three items
        # Then perform cartesian product to get all ways of combining these three lists (= 660 combos)
        all_items = [weapon_options, armor_options, ring_options]
        all_loadouts_combos: list[tuple] = list(itertools.product(*all_items))

        # Our product is a tuple with always three items, which looks like (weapon, armor, [rings])
        # Where [rings] can have [None], one or two rings.  
        # We need to flatten this list, into... [weapon, armor, ring1...]
        for weapon, armor, rings in all_loadouts_combos: 
            # e.g. 'Dagger', 'Leather', ['Damage +1', 'Damage +2']
            # Flatten to ['Dagger', 'Leather', 'Damage +1', 'Damage +2']
            loadout_item_names = [weapon] + [armor] + list(rings)
            
            # now use the item name to retrieve the actual Items for this loadout
            items = []
            for item_name in loadout_item_names:
                if item_name is not None:
                    an_item = self._all_items[item_name]
                    items.append(an_item)

            # And build a Loadout object, passing in the item names (for identification) and the items themselves
            loadout = Loadout(loadout_item_names, items)
            loadouts.append(loadout)
        
        return loadouts

    def get_loadouts(self) -> list[Loadout]:
        """ Get the valid loadouts that can be assembled from shop items """
        return self._loadouts

class Loadout:
    """ A valid combination of weapon, armor, and rings. """
    
    def __init__(self, item_names: list, items: list):
        """ Initialise a loadout.

        Args:
            item_names (list): A list of item names
            items (list): _description_
        """
        self._item_names = item_names # E.g. ['Dagger', None, 'Damage +1', 'Damage +2']
        self._items = items # The Items
        self._cost = 0 # computed
        self._damage = 0 # computed
        self._armor = 0 # computed
        self._compute_attributes()

    @property
    def cost(self) -> int:
        return self._cost

    @property
    def damage(self) -> int:
        return self._damage

    @property
    def armor(self) -> int:
        return self._armor

    def _compute_attributes(self):
        """ Compute the total cost, damage and armor of this Loadout """
        an_item:Item
        for an_item in self._items:
            self._cost += an_item.cost
            self._damage += an_item.damage
            self._armor += an_item.armor

    def __repr__(self):
        return f"Loadout: {self._item_names}, cost: {self._cost}, damage: {self._damage}, armor: {self._armor}"
    
def main():    
    boss_file = path.join(locations.input_dir, BOSS_FILE)
    shop_file = path.join(locations.input_dir, SHOP_FILE)
    
    # boss stats are determined by an input file
    with open(boss_file, mode="rt") as f:
        data = f.read().splitlines()
    
    hit_points, damage, armor = process_boss_input(data)
    boss = Player("Boss", hit_points=hit_points, damage=damage, armor=armor)
    
    # Uncomment, to actually play a game
    # test_game(Player("Player", hit_points=100, damage=7, armor=1), boss)
    
    # shop items come from an input file
    with open(shop_file, mode="rt") as f:
        data = f.read().splitlines()

    # Shop contructor takes multiple params.  Splat the tuple to pass these in.
    shop = Shop(*process_shop_items(data))

    # Get the valid loadouts
    loadouts = shop.get_loadouts()

    # Create a player using each loadout
    loadouts_tried = []
    for loadout in loadouts:
        player = Player("Player", hit_points=100, damage=loadout.damage, armor=loadout.armor)
        player_wins = player.will_defeat(boss)

        # Store the loadout we've tried, in a list with item that look like [loadout, success]
        loadouts_tried.append([loadout, player_wins])
    
    # Part 1
    winning_loadouts = [loadout for loadout, player_wins in loadouts_tried if player_wins]
    cheapest_winning_loadout = min(winning_loadouts, key=lambda loadout: loadout.cost)
    logger.info("Cheapest win = %s", cheapest_winning_loadout)
    
    # Part 2
    losing_loadouts = [loadout for loadout, player_wins in loadouts_tried if not player_wins]
    priciest_losing_loadout = max(losing_loadouts, key=lambda loadout: loadout.cost)
    logger.info("Priciest loss = %s", priciest_losing_loadout)

def test_game(player, boss):
    player_wins = play_game(player, boss)
    if player_wins:
        logger.info("We won!")
    else:
        logger.info("We lost")

def process_shop_items(data) -> tuple[dict, dict, dict]:
    """ Process shop items and return tuple of weapons, armor and rings.
    Each tuple member is a dict, mapping a shop item to its properties (name, cost, damage, armor).

    Args:
        data (List[str]): Lines from the shop file

    Returns:
        Tuple[dict, dict, dict]: Dictionaries of weapons, armor and rings. 
                                 Each dict is a mapping of item name to an Item object.
    """
    # e.g. "Damage +1    25     1       0"
    item_match = re.compile(r"^(.*)\s{2,}(\d+).+(\d+).+(\d+)")

    weapons = {}
    armor = {}
    rings = {}

    block = ""
    for line in data:
        if "Weapons:" in line:
            block = "weapons"
        elif "Armor:" in line:
            block = "armor"
        elif "Rings:" in line:
            block = "rings"
        else: # we're processing items listed in the current block type
            match = item_match.match(line)
            if match:
                item_name, cost, damage_score, armor_score = match.groups()
                item_name = item_name.strip()
                cost, damage_score, armor_score = int(cost), int(damage_score), int(armor_score)
                if block == "weapons":
                    weapons[item_name] = Item(item_name, cost, damage_score, armor_score)
                elif block == "armor":
                    armor[item_name] = Item(item_name, cost, damage_score, armor_score)
                elif block == "rings":
                    rings[item_name] = Item(item_name, cost, damage_score, armor_score)

    return weapons, armor, rings

def process_boss_input(data:list[str]):
    """ Process boss file input and return tuple of hit_points, damage and armor """
    boss = {}
    for line in data:
        key, val = line.strip().split(":")
        boss[key] = int(val)

    return boss['Hit Points'], boss['Damage'], boss['Armor']

def play_game(player: Player, opponent: Player) -> bool:
    """Performs a game, given two players. Determines if player1 wins, vs boss.

    Args:
        player (Player): The player
        enemy (Player): The opponent

    Returns:
        bool: Whether player wins
    """
    boss = copy.deepcopy(opponent)
    logger.debug("Playing...")
    i = 1
    current_player = player
    other_player = boss
    while (player.hit_points > 0 and boss.hit_points > 0):
        current_player.attack(other_player)
        logger.debug("%s round %d", current_player.name, i)
        logger.debug(other_player)
        if current_player == boss:
            i += 1

        current_player, other_player = other_player, current_player
    
    return player.is_alive()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
