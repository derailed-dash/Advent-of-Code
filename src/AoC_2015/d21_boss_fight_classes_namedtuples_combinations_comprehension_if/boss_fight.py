""" 
Author: Darren
Date: 23/03/2021

Solving https://adventofcode.com/2015/day/21

Alternating turns for player vs boss.
Loser is first for hit points to reach 0.
Hit points lost = attacker damange - defender armor
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
import itertools
import os
import time
import re
from collections import namedtuple
from itertools import combinations
from AoC_2015.d21_boss_fight_classes_namedtuples_combinations_comprehension_if.player import Player

SCRIPT_DIR = os.path.dirname(__file__) 
BOSS_FILE = "input/boss_stats.txt"
SHOP_FILE = "input/shop.txt"

Item = namedtuple("Item", "name cost damage armor")

class Shop:
    """Represents all the items that can be bought in the shop """

    def __init__(self, weapons: dict, armor: dict, rings: dict):
        """ Constructor for the shop.

        Stores all_items as a dict to map the item name to the properties
        The computes all valid combinations of items, as 'outfits'

        Args:
            weapons (dict): Weapons, as namedtuple
            armor (dict): Armor, as namedtuple
            rings (dict): Rings, as namedtuple
        """
        self._all_items = weapons | armor | rings
        
        self._weapons = weapons
        self._armor = armor
        self._rings = rings
        
        self._outfits = []
        self.create_outfits()

    def create_outfits(self):
        """Computes all valid outfits, given the items available in the shop.

        Rules:
            - All outfits have one and only one weapon
            - Outfits can have zero or one armor
            - Outfits can have zero, one or two rings.  (But each ring can only be used once.)
        """
        weapon_options = [weapon for weapon in self._weapons]
        armor_options = [None] + [armor for armor in self._armor]

        # build up the ring options.  Start by adding zero or one ring options.
        ring_options = [[None]] + [[ring] for ring in self._rings]
        # And now add combinations (without duplicates) if using two rings
        for combo in combinations(self._rings, 2):
            ring_options.append([combo[0], combo[1]])

        # smash our valid options together, and then perform cartesian product
        all_items = [weapon_options, armor_options, ring_options]
        all_outfits_combos: list[tuple] = list(itertools.product(*all_items))

        # Our product is a tuple with always three items, which looks like (weapon, armor, [rings])
        # Where [rings] can have [None], one or two rings.  
        # We need to expand this list, by turning each item into a list and then adding the lists, 
        # so that we end up with... [weapon, armor, ring1...]
        for outfit_combo in all_outfits_combos:
            outfit_item_names = []
            outfit_item_names = [outfit_combo[0]] + [outfit_combo[1]] + [rings for rings in outfit_combo[2]]

            # now use the item name to retrieve the actual items for this outfit
            items = []
            for item_name in outfit_item_names:
                if item_name is not None:
                    an_item = self._all_items[item_name]
                    items.append(an_item)

            # And build an Outfit object, passing in the item names (for identification) and the items themselves
            outfit = Outfit(outfit_item_names, items)
            self._outfits.append(outfit)

    def get_outfits(self) -> list[Outfit]:
        """ Get the valid outfits (loadouts) that can be assembled from shop items

        Returns:
            list[Outfit]: List of valid Outfits
        """
        return self._outfits

class Outfit:
    """ A valid combination of weapon, armor, and rings.
    I.e. a valid loadout for a player.
    """
    def __init__(self, item_names: list, items: list):
        self._item_names = item_names
        self._items = items
        self._cost = 0
        self._damage = 0
        self._armor = 0
        self.compute_attributes()

    def get_cost(self) -> int:
        return self._cost

    def get_damage(self) -> int:
        return self._damage

    def get_armor(self) -> int:
        return self._armor

    def compute_attributes(self):
        an_item:Item
        for an_item in self._items:
            self._cost += an_item.cost
            self._damage += an_item.damage
            self._armor += an_item.armor

    def __repr__(self):
        return f"Outfit: {self._item_names}, cost: {self._cost}, damage: {self._damage}, armor: {self._armor}"
    

def main():
    boss_file = os.path.join(SCRIPT_DIR, BOSS_FILE)
    shop_file = os.path.join(SCRIPT_DIR, SHOP_FILE)
    
    # boss stats are determined by an input file
    with open(boss_file, mode="rt") as f:
        data = f.read().splitlines()
    
    hit_points, damage, armor = process_boss_input(data)
    boss = Player("Boss", hit_points=hit_points, damage=damage, armor=armor)
    
    # shop items come from an input file
    with open(shop_file, mode="rt") as f:
        data = f.read().splitlines()

    # Shop contructor takes multiple params.  Splat the tuple to pass these in.
    shop = Shop(*process_shop_items(data))

    # Get the valid loadouts
    loadouts = shop.get_outfits()

    # Create a player using each loadout
    loadouts_tried = []
    for loadout in loadouts:
        player = Player("Player", hit_points=100, damage=loadout.get_damage(), armor=loadout.get_armor())
        player_wins = player.will_defeat(boss)

        # Store the loadout we've tried, in a list that looks like [loadout cost, player, success]
        loadouts_tried.append([loadout.get_cost(), player, player_wins])
    
    # Part 1
    winning_loadouts = [loadout for loadout in loadouts_tried if loadout[2]]
    cheapest_winning_loadout = min(winning_loadouts, key=lambda x: x[0])
    print(f"Cheapest winning loadout = {cheapest_winning_loadout}")
    
    # Part 2
    losing_loadouts = [loadout for loadout in loadouts_tried if not loadout[2]]
    priciest_losing_loadout = max(losing_loadouts, key=lambda x: x[0])
    print(f"Priciest losing loadout = {priciest_losing_loadout}")

    # If we want to play a game and see each attack...  
    # player_wins = play_game(player, boss)
    # if player_wins:
    #     print("We won!")
    # else:
    #     print("We lost")


def process_shop_items(data) -> tuple[dict, dict, dict]:
    """Process shop items and return tuple of weapons, armor and rings.
    The returned dicts are keyed by the item name, mapped to a value of NamedTuple for item, cost, damage and armor

    Args:
        data (List[str]): Lines from the shop file

    Returns:
        Tuple[dict, dict, dict]: Dictionaries of weapons, armor and rings
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
            continue
        elif "Armor:" in line:
            block = "armor"
            continue
        elif "Rings:" in line:
            block = "rings"
        else:
            match = item_match.match(line)
            if match:
                item_name, cost, damage_score, armor_score = match.groups()
                item_name = item_name.strip()
                cost = int(cost)
                damage_score = int(damage_score)
                armor_score = int (armor_score)
                if block == "weapons":
                    weapons[item_name] = Item(item_name, cost, damage_score, armor_score)
                elif block == "armor":
                    armor[item_name] = Item(item_name, cost, damage_score, armor_score)
                elif block == "rings":
                    rings[item_name] = Item(item_name, cost, damage_score, armor_score)

    return weapons, armor, rings


def process_boss_input(data:list[str]):
    """ Process boss file input and return tuple of hit_points, damage and armor

    Args:
        data (List[str]): input file lines

    Returns:
        tuple: hit_points, damage, armor
    """
    boss = {}
    for line in data:
        key, val = line.strip().split(":")
        boss[key] = int(val)

    return boss['Hit Points'], boss['Damage'], boss['Armor']


def play_game(player: Player, boss: Player) -> bool:
    """Performs a game, given two players. Determines if player1 wins, vs bloss.

    Args:
        player (Player): The player
        boss (Player): The boss

    Returns:
        bool: Whether player wins
    """
    print("Playing...")
    i = 1
    current_player = player
    other_player = boss
    while (player.get_hit_points() > 0 and boss.get_hit_points() > 0):
        current_player.attack(other_player)
        print(f"{current_player.get_name()} round {i}")
        print(other_player)
        if current_player == boss:
            i += 1

        current_player, other_player = other_player, current_player
    
    return player.is_alive()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
