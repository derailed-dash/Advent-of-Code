""" 
Author: Darren
Date: 09/04/2021

Solving https://adventofcode.com/2015/day/22

Solution:
    Wizard class overrides Player class.
    We have a SpellFactory, which creates instances of Spell, passing in SpellType dataclasss instances.

Part 1:
    We need to find the combination of attacks that uses the least mana.
    We use a generator to yield successive attack combos.
    For each combo, we play the game and store the mana used.
    Games are considered lost if the opponent wins, or a given spell combo is invalid (e.g. not enough mana).
    As we yield the next combo, we skip any combos that have the same starting sequence as a previous game.
    
    It works, but it requires a combo with 14 attacks for the lowest mana win.
    With 5 different atttacks, this means 5**14 attack sequences, i.e. >6 billion sequences!
    So, it takes a while.

Part 2:
    Simply deduct one hit point for every player turn in a game.  This reduces the number of winning games.
    Fortunately, still solved with attack sequences with 14 attacks.
"""
from __future__ import absolute_import
import logging
import os
import time
from typing import Iterable
from AoC_2015.d22_wizards_factories_dataclass_generators.players_and_wizards import Player, Wizard, SpellFactory

# pylint: disable=multiple-statements

SCRIPT_DIR = os.path.dirname(__file__) 
BOSS_FILE = "input/boss_stats.txt"

# pylint
def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")
    boss_file = os.path.join(SCRIPT_DIR, BOSS_FILE)
    
    # boss stats are determined by an input file
    with open(boss_file, mode="rt") as f:
        data = f.read().splitlines()
    
    boss_hit_points, boss_damage = process_boss_input(data)

    spell_key_lookup = {
        0: SpellFactory.SpellConstants.MAGIC_MISSILES,
        1: SpellFactory.SpellConstants.DRAIN,
        2: SpellFactory.SpellConstants.SHIELD,
        3: SpellFactory.SpellConstants.POISON,
        4: SpellFactory.SpellConstants.RECHARGE
    }

    attack_combos_lookups = attack_combos_generator(14, len(spell_key_lookup))

    winning_games = {}
    least_winning_mana = 10000
    ignore_combo = "9999999"
    player_has_won = False
    
    for attack_combo_lookup in attack_combos_lookups:
        # since attack combos are returned sequentially, 
        # we can ignore any that start with the same attacks as the last failed combo.
        if attack_combo_lookup.startswith(ignore_combo):
            continue  
        
        boss = Player("Boss", hit_points=boss_hit_points, damage=boss_damage, armor=0)
        player = Wizard("Bob", hit_points=50, mana=500)
    
        if player_has_won:
            logging.info("Best winning attack: %s. Total mana: %s. Current attack: %s", 
                        winning_games[least_winning_mana], least_winning_mana, attack_combo_lookup)
        else:
            logging.info("Current attack: %s", attack_combo_lookup)

        # Convert the attack combo to a list of spells.
        attack_combo = [spell_key_lookup[int(key)] for key in attack_combo_lookup]
        player_won, mana_consumed, rounds_started = play_game(attack_combo, player, boss, hard_mode=True, mana_target=least_winning_mana)
        if player_won:
            player_has_won = True
            winning_games[mana_consumed] = attack_combo_lookup
            least_winning_mana = min(mana_consumed, least_winning_mana)      
        
        # we can ingore any attacks that start with the same attacks as what we tried last time
        ignore_combo = attack_combo_lookup[0:rounds_started]
        
    print(f"We found {len(winning_games)} winning solutions. Lowest mana cost was {least_winning_mana}.")
            
                
def to_base_n(number: int, base: int):
    """ Convert any integer number into a base-n string representation of that number.
    E.g. to_base_n(38, 5) = 123

    Args:
        number (int): The number to convert
        base (int): The base to apply

    Returns:
        [str]: The string representation of the number
    """
    ret_str = ""
    while number:
        ret_str = str(number % base) + ret_str
        number //= base

    return ret_str


def attack_combos_generator(max_attacks: int, count_different_attacks: int) -> Iterable[str]:
    """ Generator that returns the next attack combo.
    E.g. with a max of 3 attacks, and 5 different attacks, 
    the generator will return a max of 5**3 = 125 different attack combos

    Args:
        max_attacks (int): Maximum number of attacks to return before exiting
        count_different_attacks (int): How many different attacks we can make

    Yields:
        Iterator[Iterable[str]]: Next attack sequence
    """
    num_attack_combos = count_different_attacks**max_attacks
    
    # yield the next attack combo, i.e. from 
    # 000, 001, 002, 003, 004, 010, 011, 012, 013, 014, 020, 021, 022, 023, 024, etc
    # Let's return them in reverse, to give us a nice countdown
    for i in range(num_attack_combos):
        # convert i to base-n (where n is the number of attacks we can choose from), 
        # and then pad with zeroes such that str length is the same as total number of attacks
        yield to_base_n(i, count_different_attacks).zfill(max_attacks)


def play_game(attacks: list, player: Wizard, boss: Player, hard_mode=False, **kwargs) -> tuple[bool, int, int]:
    """ Play a game, given a player (Wizard) and an opponent (boss)

    Args:
        attacks (list[str]): List of spells to cast, from SpellFactory.SpellConstants
        player (Wizard): A Wizard
        boss (Player): A mundane opponent
        hard_mode (Bool): Whether each player turn automatically loses 1 hit point
        mana_target (int): optional arg, that specifies a max mana consumed value which triggers a return

    Returns:
        tuple[bool, int, int]: Whether the player won, the amount of mana consumed, and the number of rounds started
    """
    i = 1
    current_player = player
    other_player = boss    

    mana_consumed: int = 0
    mana_target = kwargs.get('mana_target', None)

    while (player.get_hit_points() > 0 and boss.get_hit_points() > 0):
        if current_player == player:
            # player (wizard) attack
            logging.debug("")
            logging.debug("Round %s...", i)

            logging.debug("%s's turn:", current_player.get_name())
            if hard_mode:
                logging.debug("Hard mode hit. Player hit points reduced by 1.")
                player.take_hit(1)
                if player.get_hit_points() <= 0:
                    logging.debug("Hard mode killed %s", boss.get_name())
                    continue
            try:
                mana_consumed += player.take_turn(attacks[i-1], boss)
                if mana_target and mana_consumed > mana_target:
                    logging.debug('Mana target %s exceeded; mana consumed=%s.', mana_target, mana_consumed)
                    return False, mana_consumed, i
            except ValueError as err:
                logging.debug(err)
                return False, mana_consumed, i
            except IndexError:
                logging.debug("No more attacks left.")
                return False, mana_consumed, i

        else:
            logging.debug("%s's turn:", current_player.get_name())
            # effects apply before opponent attacks
            player.opponent_takes_turn(boss)
            if boss.get_hit_points() <= 0:
                logging.debug("Effects killed %s!", boss.get_name())
                continue

            boss.attack(other_player)
            i += 1

        logging.debug("End of turn: %s", player)
        logging.debug("End of turn: %s", boss)

        # swap players
        current_player, other_player = other_player, current_player

    player_won = player.get_hit_points() > 0
    return player_won, mana_consumed, i


def process_boss_input(data:list[str]) -> tuple:
    """ Process boss file input and return tuple of hit_points, damage

    Args:
        data (List[str]): input file lines

    Returns:
        tuple: hit_points, damage
    """
    boss = {}
    for line in data:
        key, val = line.strip().split(":")
        boss[key] = int(val)

    return boss['Hit Points'], boss['Damage']


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
