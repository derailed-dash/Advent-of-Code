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
    
    It works, but it requires a combo with 12 attacks for the lowest mana win.
    With 5 different attacks, this means 5**12 attack sequences, i.e. 244m different attack combos.
    
    Caching the sorted attack_combo_lookup str reduces the overall time by about half.
    
    This approach currently takes a few minutes.

Part 2:
    Simply deduct one hit point for every player turn in a game.  This reduces the number of winning games.
    Fortunately, still solved with attack sequences with 12 attacks.
"""
from __future__ import annotations
from enum import Enum
from functools import cache
import logging
import time
from math import ceil
from dataclasses import dataclass
from os import path
from typing import Iterable
from tqdm import tqdm

import common.type_defs as td

locations = td.get_locations(__file__)
logger = td.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, folder=locations.output_dir)

BOSS_FILE = "boss_stats.txt"

class Player:
    """A player has three key attributes:
      hit_points (life) - When this reaches 0, the player has been defeated
      damage - Attack strength
      armor - Attack defence

    Damage done per attack = this player's damage - opponent's armor.  (With a min of 1.)
    Hit_points are decremented by an enemy attack.
    """
    def __init__(self, name: str, hit_points: int, damage: int, armor: int):
        self._name = name
        self._hit_points = hit_points
        self._damage = damage
        self._armor = armor

    @property
    def name(self) -> str:
        return self._name

    @property
    def hit_points(self) -> int:
        return self._hit_points

    @property
    def armor(self) -> int:
        return self._armor

    @property
    def damage(self) -> int:
        return self._damage
    
    def take_hit(self, loss: int):
        """ Remove this hit from the current hit points """
        self._hit_points -= loss

    def is_alive(self) -> bool:
        return self._hit_points > 0

    def _damage_inflicted_on_opponent(self, other_player: Player) -> int:
        """Damage inflicted in an attack.  Given by this player's damage minus other player's armor.
        Returns: damage inflicted per attack """
        return max(self._damage - other_player.armor, 1)

    def get_attacks_needed(self, other_player: Player) -> int:
        """ The number of attacks needed for this player to defeat the other player. """
        return ceil(other_player.hit_points / self._damage_inflicted_on_opponent(other_player))

    def will_defeat(self, other_player: Player) -> bool:
        """ Determine if this player will win a fight with an opponent.
        I.e. if this player needs fewer (or same) attacks than the opponent.
        Assumes this player always goes first. """
        return (self.get_attacks_needed(other_player) 
                <= other_player.get_attacks_needed(self))

    def attack(self, other_player: Player):
        """ Perform an attack on another player, inflicting damage """
        attack_damage = self._damage_inflicted_on_opponent(other_player)
        other_player.take_hit(attack_damage)
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f"Player: {self._name}, hit points={self._hit_points}, damage={self._damage}, armor={self._armor}"

@dataclass
class SpellAttributes:
    """ Define the attributes of a Spell """
    name: str
    mana_cost: int
    effect_duration: int
    is_effect: bool
    heal: int
    damage: int
    armor: int
    mana_regen: int
    delay_start: int
    
class SpellType(Enum):
    """ Possible spell types. 
    Any given spell_type.value will return an instance of SpellAttributes. """
    
    MAGIC_MISSILES = SpellAttributes('MAGIC_MISSILES', 53, 0, False, 0, 4, 0, 0, 0)
    DRAIN = SpellAttributes('DRAIN', 73, 0, False, 2, 2, 0, 0, 0)
    SHIELD = SpellAttributes('SHIELD', 113, 6, True, 0, 0, 7, 0, 0)
    POISON = SpellAttributes('POISON', 173, 6, True, 0, 3, 0, 0, 0)
    RECHARGE = SpellAttributes('RECHARGE', 229, 5, True, 0, 0, 0, 101, 0)

spell_key_lookup = {
    0: SpellType.MAGIC_MISSILES, # 53
    1: SpellType.DRAIN, # 73
    2: SpellType.SHIELD, # 113
    3: SpellType.POISON, # 173
    4: SpellType.RECHARGE # 229
}

spell_costs = {spell_key: spell_key_lookup[spell_key].value.mana_cost 
               for spell_key, spell_type in spell_key_lookup.items()}

@dataclass
class Spell:
    """ Spells should be created using create_spell_by_type() factory method.

    Spells have a number of attributes.  Of note:
    - effects last for multiple turns, and apply on both player and opponent turns.
    - duration is the number of turns an effect lasts for
    - mana is the cost of the spell
    """
    name: str
    mana_cost: int
    effect_duration: int
    is_effect: bool
    heal: int = 0
    damage: int = 0
    armor: int = 0
    mana_regen: int = 0
    delay_start: int = 0
    effect_applied_count = 0 # track how long an effect has been running

    @classmethod
    def check_spell_castable(cls, spell_type: SpellType, wiz: Wizard):
        """ Determine if this Wizard can cast this spell.
        Spell can only be cast if the wizard has sufficient mana, and if the spell is not already active.

        Raises:
            ValueError: If the spell is not castable

        Returns:
            [bool]: True if castable
        """

        # not enough mana
        if wiz.mana < spell_type.value.mana_cost:
            raise ValueError(f"Not enough mana for {spell_type}. " \
                                f"Need {spell_type.value.mana_cost}, have {wiz.mana}.")

        # spell already active
        if spell_type in wiz.get_active_effects():
            raise ValueError(f"Spell {spell_type} already active.")
        
        return True
        
    @classmethod
    def create_spell_by_type(cls, spell_type: SpellType):
        # Unpack the spell_type.value, which will be a SpellAttributes class
        # Get all the values, and unpack them, to pass into the factory method.
        attrs_dict = vars(spell_type.value)
        return cls(*attrs_dict.values())
    
    def __repr__(self) -> str:
        return f"Spell: {self.name}, cost: {self.mana_cost}, " \
                    f"is effect: {self.is_effect}, remaining duration: {self.effect_duration}"

    def increment_effect_applied_count(self):
        self.effect_applied_count += 1

class Wizard(Player):
    """ Extends Player.
    Also has attribute 'mana', which powers spells.
    Wizard has no armor (except when provided by spells) and no inherent damage (except from spells).

    For each wizard turn, we must cast_spell() and apply_effects().
    On each opponent's turn, we must apply_effects().
    """
    def __init__(self, name: str, hit_points: int, mana: int, damage: int = 0, armor: int = 0):
        """ Wizards have 0 mundane armor or damage.

        Args:
            name (str): Wizard name
            hit_points (int): Total life.
            mana (int): Used to power spells.
            damage (int, optional): mundane damage. Defaults to 0.
            armor (int, optional): mundane armor. Defaults to 0.
        """
        super().__init__(name, hit_points, damage, armor)
        self._mana = mana

        # store currently active effects, where key = spell constant, and value = spell
        self._active_effects: dict[str, Spell] = {}

    @property
    def mana(self):
        return self._mana

    def use_mana(self, mana_used: int):
        if mana_used > self._mana:
            raise ValueError("Not enough mana!")
        
        self._mana -= mana_used

    def get_active_effects(self):
        return self._active_effects

    def take_turn(self, spell_key, other_player: Player) -> int:
        """ This player takes a turn.
        This means: casting a spell, applying any effects, and fading any expired effects

        Args:
            spell_key (str): The spell key, from SpellFactory.SpellConstants
            other_player (Player): The opponent

        Returns:
            int: The mana consumed by this turn
        """
        self._turn(other_player)
        mana_consumed = self.cast_spell(spell_key, other_player)

        return mana_consumed

    def _turn(self, other_player: Player):
        self.apply_effects(other_player)
        self.fade_effects()        
        
    def opponent_takes_turn(self, other_player: Player):
        """ An opponent takes their turn.  (Not the wizard.)
        We must apply any Wizard effects on their turn (and fade), before their attack.
        This method does not include their attack.

        Args:
            other_player (Player): [description]
        """
        self._turn(other_player)

    def cast_spell(self, spell_type: SpellType, other_player: Player) -> int:
        """ Casts a spell.
        - If spell is not an effect, it applies once.
        - Otherwise, it applies for the spell's duration, on both player and opponent turns.

        Args:
            spell_type (SpellType): a SpellType constant.
            other_player (Player): The player to cast against

        Returns:
            [int]: Mana consumed
        """
        Spell.check_spell_castable(spell_type, self) # can this wizard cast this spell?
        spell = Spell.create_spell_by_type(spell_type)
        try:
            self.use_mana(spell.mana_cost)
        except ValueError as err:
            raise ValueError(f"Unable to cast {spell_type}: Not enough mana! " \
                             f"Needed {spell.mana_cost}; have {self._mana}.") from err

        logger.debug("%s casted %s", self._name, spell)

        if spell.is_effect:
            # add to active effects, apply later
            # this might replace a fading effect
            self._active_effects[spell_type.name] = spell
        else:
            # apply now.
            # opponent's armor counts for nothing against a magical attack
            attack_damage = spell.damage
            if attack_damage:
                logger.debug("%s attack. Inflicting damage: %s.", self._name, attack_damage)
                other_player.take_hit(attack_damage)

            heal = spell.heal
            if heal:
                logger.debug("%s: healing by %s.", self._name, heal) 
                self._hit_points += heal

        return spell.mana_cost                        
            
    def fade_effects(self):
        effects_to_remove = []
        for effect_name, effect in self._active_effects.items():
            if effect.effect_applied_count >= effect.effect_duration:
                logger.debug("%s: fading effect %s", self._name, effect_name)
                if effect.armor:
                    # restore armor to pre-effect levels
                    self._armor -= effect.armor

                # Now we've faded the effect, flag it for removal
                effects_to_remove.append(effect_name)
        
        # now remove any effects flagged for removal
        for effect_name in effects_to_remove:
            self._active_effects.pop(effect_name)        

    def apply_effects(self, other_player: Player):
        """ Apply effects in the active_effects dict.

        Args:
            other_player (Player): The opponent
        """
        for effect_name, effect in self._active_effects.items():
            # if effect should be active if we've used it fewer times than the duration
            if effect.effect_applied_count < effect.effect_duration:
                effect.increment_effect_applied_count()
                if logger.getEffectiveLevel() == logging.DEBUG:
                    logger.debug("%s: applying effect %s, leaving %d turns.", 
                            self._name, effect_name, effect.effect_duration - effect.effect_applied_count)

                if effect.armor:
                    if effect.effect_applied_count == 1:
                        # increment armor on first use, and persist this level until the effect fades
                        self._armor += effect.armor

                if effect.damage:
                    other_player.take_hit(effect.damage)
                
                if effect.mana_regen:
                    self._mana += effect.mana_regen
        
    def attack(self, other_player: Player):
        """ A Wizard cannot perform a mundane attack.
        Use cast_spell() instead.
        """
        raise NotImplementedError("Wizards cast spells")

    def __repr__(self):
        return f"{self._name} (Wizard): hit points={self._hit_points}, " \
                        f"damage={self._damage}, armor={self._armor}, mana={self._mana}"

@cache # I think there are only about 3000 different sorted attacks
def get_combo_mana_cost(attack_combo_lookup: str) -> int:
    """ Pass in attack combo lookup str, and return the cost of this attack combo.
    Ideally, the attack combo lookup should be sorted, because cost doesn't care about attack order;
    and providing a sorted value, we can use a cache. """
    return sum(spell_costs[int(attack)] for attack in attack_combo_lookup)
    
def main():
    # boss stats are determined by an input file
    with open(path.join(locations.input_dir, BOSS_FILE), mode="rt") as f:
        boss_hit_points, boss_damage = process_boss_input(f.read().splitlines())
        actual_boss = Player("Actual Boss", hit_points=boss_hit_points, damage=boss_damage, armor=0)

    test_boss = Player("Test Boss", hit_points=40, damage=10, armor=0) # test boss, which only requires 7 attacks
    player = Wizard("Bob", hit_points=50, mana=500)

    # winning_games, least_winning_mana = try_combos(test_boss, player, 11)
    winning_games, least_winning_mana = try_combos(actual_boss, player, 12)

    message = "Winning solutions:\n" + "\n".join(f"Mana: {k}, Attack: {v}" for k, v in winning_games.items())
    logger.info(message)
    logger.info("We found %d winning solutions. Lowest mana cost was %d.", len(winning_games), least_winning_mana)

def try_combos(boss_stats: Player, plyr_stats: Wizard, num_attacks):
    # the generator - without list - is faster, but we lose the tqdm progress bar
    logger.info("Boss stats: name=%s, hit_points=%d, damage=%d", boss_stats.name, boss_stats.hit_points, boss_stats.damage)
    logger.info("Player stats: name=%s, hit_points=%d, mana=%d", plyr_stats.name, plyr_stats.hit_points, plyr_stats.mana)    
    attack_combos_lookups = attack_combos_generator(num_attacks, len(spell_key_lookup))

    winning_games = {}
    least_winning_mana = 2500 # ball-park of what will likely be larger than winning solution
    ignore_combo = "9999999"
    player_has_won = False
    
    for attack_combo_lookup in tqdm(list(attack_combos_lookups)): # play the game with this attack combo
        # since attack combos are returned sequentially, 
        # we can ignore any that start with the same attacks as the last failed combo.
        if attack_combo_lookup.startswith(ignore_combo):
            continue
        
        # determine if the cost of the current attack is going to be more than an existing
        # winning solution. (Sort it, so we can cache the attack cost.)
        sorted_attack = ''.join(sorted(attack_combo_lookup))
        if get_combo_mana_cost(sorted_attack) >= least_winning_mana:
            continue
        
        # Much faster than a deep copy
        boss = Player(boss_stats.name, boss_stats.hit_points, boss_stats.damage, boss_stats.armor)
        player = Wizard(plyr_stats.name, plyr_stats.hit_points, plyr_stats.mana)
    
        if player_has_won and logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug("Best winning attack: %s. Total mana: %s. Current attack: %s", 
                        winning_games[least_winning_mana], least_winning_mana, attack_combo_lookup)
        else:
            logger.debug("Current attack: %s", attack_combo_lookup)

        # Convert the attack combo to a list of spells. E.g. convert '00002320'
        # to [<SpellType.MAGIC_MISSILES: ..., <SpellType.MAGIC_MISSILES: ..., 
        #    ... <SpellType.SHIELD: ..., <SpellType.MAGIC_MISSILES: ... >]
        attack_combo = [spell_key_lookup[int(attack)] for attack in attack_combo_lookup]
        player_won, mana_consumed, rounds_started = play_game(
                attack_combo, player, boss, hard_mode=True, mana_target=least_winning_mana)
        
        if player_won:
            player_has_won = True
            winning_games[mana_consumed] = attack_combo_lookup
            least_winning_mana = min(mana_consumed, least_winning_mana)      
        
        # we can ingore any attacks that start with the same attacks as what we tried last time
        ignore_combo = attack_combo_lookup[0:rounds_started]
        
    return winning_games, least_winning_mana

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
    curr_num = number
    while curr_num:
        ret_str = str(curr_num % base) + ret_str
        curr_num //= base

    return ret_str if number > 0 else "0"

def attack_combos_generator(max_attacks: int, count_different_attacks: int, reverse=False) -> Iterable[str]:
    """ Generator that returns the next attack combo.
    E.g. with a max of 3 attacks, and 5 different attacks, 
    the generator will return a max of 5**3 = 125 different attack combos

    Args:
        max_attacks (int): Maximum number of attacks to return before exiting
        count_different_attacks (int): How many different attacks we can make

    Yields: next attack sequence
    """
    num_attack_combos = count_different_attacks**max_attacks
    for i in range(num_attack_combos):
        # convert i to base-n (where n is the number of attacks we can choose from) 

        if reverse:
            # Pad with zeroes such that str length is the same as total number of attacks.
            # E.g. 000, 001, 002, 003, 004, 010, 011, 012, 013, 014, 020, 021, 022, 023, 024, etc
            yield to_base_n(i, count_different_attacks).zfill(max_attacks)
        else:
            # E.g. 0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, etc
            yield to_base_n(i, count_different_attacks)

def play_game(attacks: list, player: Wizard, boss: Player, hard_mode=False, **kwargs) -> tuple[bool, int, int]:
    """ Play a game, given a player (Wizard) and an opponent (boss)

    Args:
        attacks (list[str]): List of spells to cast, from SpellFactory.SpellConstants
        player (Wizard): A Wizard
        boss (Player): A mundane opponent
        hard_mode (Bool): Whether each player turn automatically loses 1 hit point
        mana_target (int): optional arg, that specifies a max mana consumed value which triggers a return

    Returns:
        tuple[bool, int, int]: player won, mana consumed, number of rounds
    """
    game_round = 1
    current_player = player
    other_player = boss    

    mana_consumed: int = 0
    mana_target = kwargs.get('mana_target', None)

    while (player.hit_points > 0 and boss.hit_points > 0):
        if current_player == player:
            # player (wizard) attack
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.debug("")
                logger.debug("Round %s...", game_round)
                logger.debug("%s's turn:", current_player.name)
    
            if hard_mode:
                logger.debug("Hard mode hit. Player hit points reduced by 1.")
                player.take_hit(1)
                if player.hit_points <= 0:
                    logger.debug("Hard mode killed %s", boss.name)
                    continue
            try:
                mana_consumed += player.take_turn(attacks[game_round-1], boss)
                if mana_target and mana_consumed > mana_target:
                    logger.debug('Mana target %s exceeded; mana consumed=%s.', mana_target, mana_consumed)
                    return False, mana_consumed, game_round
            except ValueError as err:
                logger.debug(err)
                return False, mana_consumed, game_round
            except IndexError:
                logger.debug("No more attacks left.")
                return False, mana_consumed, game_round

        else:
            logger.debug("%s's turn:", current_player.name)
            # effects apply before opponent attacks
            player.opponent_takes_turn(boss)
            if boss.hit_points <= 0:
                logger.debug("Effects killed %s!", boss.name)
                continue

            boss.attack(other_player)
            game_round += 1
        
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug("End of turn: %s", player)
            logger.debug("End of turn: %s", boss)

        # swap players
        current_player, other_player = other_player, current_player

    player_won = player.hit_points > 0
    return player_won, mana_consumed, game_round

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
    logger.info("Final cache size: %d", get_combo_mana_cost.cache_info().currsize)
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
