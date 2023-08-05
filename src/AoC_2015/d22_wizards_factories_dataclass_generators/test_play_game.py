""" Unit testing for Spell_Casting """
import unittest
import logging
from spell_casting_2 import logger, Player, Wizard, spell_key_lookup, play_game, try_combos

class TestPlayGame(unittest.TestCase):
    """ Test single game, and combos """
    
    def setUp(self):
        self.boss_hit_points = 14
        self.boss_damage = 8
        self.attack_combo = [spell_key_lookup[int(attack)] for attack in "42130"]
        self.boss = Player("Boss", hit_points=self.boss_hit_points, damage=self.boss_damage, armor=0)
        self.player = Wizard("Bob", hit_points=10, mana=250)
        
    def test_play_game(self):
        """ Test a simple game, in _normal_ diffulty """
        logger.setLevel(logging.DEBUG)
        
        player_won, mana_consumed, rounds_started = play_game(self.attack_combo, self.player, self.boss)
        self.assertEqual(player_won, True)
        self.assertEqual(mana_consumed, 641)
        self.assertEqual(rounds_started, 5)

    def test_play_game_hard_mode(self):
        """ Test a simple game, in _hard_ diffulty. I.e. player loses 1 hitpoint per turn. """        
        logger.setLevel(logging.DEBUG)
        
        player_won, mana_consumed, rounds_started = play_game(self.attack_combo, self.player, self.boss, hard_mode=True)
        self.assertEqual(player_won, False)
        self.assertEqual(mana_consumed, 229)
        self.assertEqual(rounds_started, 2)
        
    def test_try_combos(self):
        """ Try multiple games, testing combos to find the winning combo that consumes the least mana """
        logger.setLevel(logging.INFO)
                
        boss_hit_points, boss_damage, num_attacks = 40, 10, 8
        boss = Player("Boss", boss_hit_points, boss_damage, armor=0)
        player = Wizard("Bob", hit_points=50, mana=500)
                
        winning_games, least_winning_mana = try_combos(boss, player, num_attacks)
        logger.info("We found %d winning solutions. Lowest mana cost was %d.", len(winning_games), least_winning_mana)
        
        self.assertEqual(len(winning_games), 4)  # with 40, 10, 8
        self.assertEqual(least_winning_mana, 794) # with 40, 10, 8

if __name__ == '__main__':
    unittest.main()
