""" Test cases for Spell Casting """
import logging
from d22_wizards_factories_constants.players_and_wizards import Player, Wizard, SpellFactory
from d22_wizards_factories_constants.spell_casting import play_game as pg

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:\t%(message)s")

# pylint: disable=logging-fstring-interpolation

def test_attacks():
    player = Wizard("Bob", hit_points=10, mana=250)
    boss = Player("Boss Socks", hit_points=14, damage=8, armor=0)
    
    # run some tests
    attacks = [
        SpellFactory.SpellConstants.RECHARGE,
        SpellFactory.SpellConstants.SHIELD,
        SpellFactory.SpellConstants.DRAIN,
        SpellFactory.SpellConstants.POISON, 
        SpellFactory.SpellConstants.MAGIC_MISSILES,
    ]
    do_test_game("TEST: TEST GAME", attacks, player, boss)    

def not_enough_mana():
    player = Wizard("Bob", hit_points=10, mana=250)
    boss = Player("Boss Socks", hit_points=14, damage=8, armor=0)
    
    attacks = [
        SpellFactory.SpellConstants.RECHARGE,
        SpellFactory.SpellConstants.POISON, 
        SpellFactory.SpellConstants.SHIELD,
        SpellFactory.SpellConstants.DRAIN,
        SpellFactory.SpellConstants.MAGIC_MISSILES,
    ]    
    do_test_game("TEST: NOT ENOUGH MANA", attacks, player, boss)
    
def spell_already_active():
    player = Wizard("Bob", hit_points=10, mana=250)
    boss = Player("Boss Socks", hit_points=14, damage=8, armor=0)
        
    attacks = [
        SpellFactory.SpellConstants.RECHARGE,
        SpellFactory.SpellConstants.SHIELD,
        SpellFactory.SpellConstants.DRAIN,
        SpellFactory.SpellConstants.SHIELD,
        SpellFactory.SpellConstants.RECHARGE,
        SpellFactory.SpellConstants.MAGIC_MISSILES,
    ]    
    do_test_game("TEST: SPELL ALREADY ACTIVE", attacks, player, boss)

def do_test_game(game_label: str, attacks: list[str], player: Wizard, boss: Player, hard_mode = False):
    logging.debug(f"*** {game_label} ***")
    
    logging.debug(f"{player}")
    logging.debug(boss)
  
    player_won, mana_consumed, rounds_started = pg(attacks, player, boss, hard_mode=hard_mode)
    logging.debug(f"Player won? {player_won}. Mana consumed: {mana_consumed}. Rounds started: {rounds_started}.")  
    logging.debug("")

def specific_attack(attack_str: str, hard_mode = False):
    player = Wizard("Bob", hit_points=50, mana=500)
    boss = Player("Boss Socks", hit_points=71, damage=10, armor=0)
        
    spell_key_lookup = {
        0: SpellFactory.SpellConstants.MAGIC_MISSILES,
        1: SpellFactory.SpellConstants.DRAIN,
        2: SpellFactory.SpellConstants.SHIELD,
        3: SpellFactory.SpellConstants.POISON,
        4: SpellFactory.SpellConstants.RECHARGE
    }
    attacks = [spell_key_lookup[int(key)] for key in attack_str]
    do_test_game("TEST: ATTACK " + attack_str, attacks, player, boss, hard_mode)
    
def do_tests():
    # test_attacks()
    # not_enough_mana()
    # spell_already_active()
    specific_attack('43243243203000', hard_mode=True)


do_tests()
