""" Unit testing for Spell_Casting 
    0: SpellType.MAGIC_MISSILES, # 53
    1: SpellType.DRAIN, # 73
    2: SpellType.SHIELD, # 113
    3: SpellType.POISON, # 173
    4: SpellType.RECHARGE # 229
"""
import unittest
import logging
from spell_casting import (
        logger, 
        Player, Wizard, 
        spell_key_lookup, 
        play_game, try_combos, get_combo_mana_cost)

class TestPlayGame(unittest.TestCase):
    """ Test single game, and combos """
    
    def setUp(self):
        pass
    
    def run(self, result=None):
        """ Override run method so we can include method name in output """
        method_name = self._testMethodName
        logger.info("Running test: %s", method_name)
        super().run(result)
        
    def test_play_game_42130(self):
        """ Test a simple game, in _normal_ diffulty.
        As supplied in the game instructions. """  
        logger.setLevel(logging.DEBUG) # So we can look at each turn and compare to the instructions
        player = Wizard("Bob", hit_points=10, mana=250)
        boss = Player("Boss", hit_points=14, damage=8, armor=0)
        attack_combo = [spell_key_lookup[int(attack)] for attack in "42130"]
        
        player_won, mana_consumed, rounds_started = play_game(attack_combo, player, boss)
        self.assertEqual(player_won, True)
        self.assertEqual(mana_consumed, 641)
        self.assertEqual(rounds_started, 5)

    def test_play_game_42130_hard_mode(self):
        """ Test a simple game, in _hard_ diffulty. I.e. player loses 1 hitpoint per turn. """        
        logger.setLevel(logging.DEBUG)
        player = Wizard("Bob", hit_points=10, mana=250)
        boss = Player("Boss", hit_points=14, damage=8, armor=0)
        attack_combo = [spell_key_lookup[int(attack)] for attack in "42130"]
        
        player_won, mana_consumed, rounds_started = play_game(attack_combo, player, boss, hard_mode=True)
        self.assertEqual(player_won, False)
        self.assertEqual(mana_consumed, 229)
        self.assertEqual(rounds_started, 2)
    
    def test_play_game_304320_hard_mode(self):
        logger.setLevel(logging.INFO)
        player = Wizard("Bob", hit_points=50, mana=500)
        boss = Player("Boss", hit_points=40, damage=10, armor=0)
        attack_combo = [spell_key_lookup[int(attack)] for attack in "304320"]
        
        player_won, mana_consumed, rounds_started = play_game(attack_combo, player, boss, hard_mode=True)
        self.assertEqual(player_won, True)
        self.assertEqual(mana_consumed, 794)
        self.assertEqual(rounds_started, 6)
        
    def test_play_game_34230000_hard_mode(self):
        logger.setLevel(logging.DEBUG)
        player = Wizard("Bob", hit_points=50, mana=500)
        boss = Player("Boss", hit_points=40, damage=10, armor=0)
        attack_combo = [spell_key_lookup[int(attack)] for attack in "34230000"]
        
        player_won, mana_consumed, rounds_started = play_game(attack_combo, player, boss, hard_mode=True)
        self.assertEqual(player_won, True)
        self.assertEqual(mana_consumed, 794) # only uses 6 of the 8 attacks, otherwise would be 900
        self.assertEqual(rounds_started, 6)
        
    def test_play_game_224304300300_hard_mode(self):
        logger.setLevel(logging.INFO)
        player = Wizard("Bob", hit_points=50, mana=500)
        boss = Player("Boss", hit_points=71, damage=10, armor=0)
        attack_combo = [spell_key_lookup[int(attack)] for attack in "224304300300"]
        
        player_won, mana_consumed, rounds_started = play_game(attack_combo, player, boss, hard_mode=True)
        self.assertEqual(player_won, True)
        self.assertEqual(mana_consumed, 1468)
        self.assertEqual(rounds_started, 12)        
    
    def test_calculate_mana_cost(self):
        self.assertEqual(get_combo_mana_cost("42130"), 641)
        self.assertEqual(get_combo_mana_cost("34230000"), 900)
        
    def test_try_combos(self):
        """ Try multiple games, testing combos to find the winning combo that consumes the least mana """
        logger.setLevel(logging.INFO)
        num_attacks = 9
        logger.info("Using %d attacks", num_attacks)
        
        boss = Player("Boss", hit_points=40, damage=10, armor=0)
        player = Wizard("Bob", hit_points=50, mana=500)
                
        winning_games, least_winning_mana = try_combos(boss, player, num_attacks)
        logger.info("We found %d winning solutions. Lowest mana cost was %d.", len(winning_games), least_winning_mana)
        message = "Winning solutions:\n" + "\n".join(f"Mana: {k}, Attack: {v}" for k, v in winning_games.items())
        logger.info(message)
        self.assertEqual(least_winning_mana, 794) # with 40, 10, 8

if __name__ == '__main__':
    unittest.main()
