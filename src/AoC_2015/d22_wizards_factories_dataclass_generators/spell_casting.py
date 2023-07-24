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
from __future__ import annotations
from dataclasses import dataclass
import logging
from math import ceil
import time
from os import path
from typing import Iterable
import common.type_defs as td

locations = td.get_locations(__file__)
logger = td.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.INFO)
# td.setup_file_logging(logger, folder=locations.script_dir)

BOSS_FILE = "boss_stats.txt"
NUM_ATTACKS = 7 # We need 14

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
class SpellType:
    """ The attributes and types that must be passed to a Spell factory method."""
    name: str
    mana_cost: int
    duration: int
    is_effect: bool
    heal: int = 0
    damage: int = 0
    armor: int = 0
    heal: int = 0
    mana_regen: int = 0
    delay_start: int = 0

class SpellFactory:
    """ For creating instances of Spell. Use the create_spell() method.

    Raises:
        KeyError: If an incorrect spell constant is passed.

    Returns:
        [Spell]: An instance of Spell.
    """
    class SpellConstants:
        """ Spell Constants """
        MAGIC_MISSILES = 'magic_missiles'
        DRAIN = 'drain'
        SHIELD = 'shield'
        POISON = 'poison'
        RECHARGE = 'recharge'

    spell_types = {
        SpellConstants.MAGIC_MISSILES: SpellType('MAGIC_MISSILES', mana_cost=53, duration=0, is_effect=False, damage=4),
        SpellConstants.DRAIN: SpellType('DRAIN', mana_cost=73, duration=0, is_effect=False, damage=2, heal=2),
        SpellConstants.SHIELD: SpellType('SHIELD', mana_cost=113, duration=6, is_effect=True, armor=7),
        SpellConstants.POISON: SpellType('POISON', mana_cost=173, duration=6, is_effect=True, damage=3),
        SpellConstants.RECHARGE: SpellType('RECHARGE', mana_cost=229, duration=5, is_effect=True, mana_regen=101)
    }

    @classmethod
    def check_spell_castable(cls, spell_type: str, wiz: Wizard):
        """ Determine if this Wizard can cast this spell.
        Spell can only be cast if the wizard has sufficient mana, and if the spell is not already active.

        Args:
            spell_type (str): Spell constant
            wiz (Wizard): A Wizard

        Raises:
            KeyError: If the spell_type does not exist
            ValueError: If the spell is not castable

        Returns:
            [bool]: True if castable
        """
        if spell_type not in SpellFactory.spell_types.keys():
            raise ValueError(f"{spell_type} does not exist.")
        
        spell_attribs = SpellFactory.spell_types[spell_type]

        # not enough mana
        if wiz.get_mana() < spell_attribs.mana_cost:
            raise ValueError(f"Not enough mana for {spell_type}. " \
                                f"Need {spell_attribs.mana_cost}, have {wiz.get_mana()}.")

        # spell already active
        if spell_type in wiz.get_active_effects():
            raise ValueError(f"Spell {spell_type} already active.")
    
    @classmethod
    def create_spell(cls, spell_type: str):
        """ Create a new Spell instance, by passing in the appropriate Spell Type constant.

        Args:
            spell_type (str): From SpellFactory.SpellConstants

        Raises:
            KeyError: If an incorrect spell constant is passed.

        Returns:
            [Spell]: An instance of Spell
        """
        if spell_type not in SpellFactory.spell_types.keys():
            raise KeyError

        return Spell(SpellFactory.spell_types[spell_type])

class Spell:
    """Spells should be created using Spellfactory.create_spell()

    Spells have a number of attributes.  Of note:
    - effects last for multiple turns, and apply on both player and opponent turns.
    - duration is the number of turns an effect lasts for
    - mana is the cost of the spell
    """

    def __init__(self, spell_type: SpellType):
        self._name = spell_type.name
        self._mana_cost = spell_type.mana_cost
        self._duration = spell_type.duration
        self._is_effect = spell_type.is_effect
        self._heal = spell_type.heal
        self._damage = spell_type.damage
        self._armor = spell_type.armor
        self._mana_regen = spell_type.mana_regen
        self._effect_applied_count = 0

    def __repr__(self) -> str:
        return f"Spell: {self._name}, cost: {self._mana_cost}, " \
                    f"is effect: {self._is_effect}, remaining duration: {self._duration}"

    def is_effect(self):
        return self._is_effect

    def get_mana_cost(self):
        return self._mana_cost

    def get_heal(self):
        return self._heal

    def get_damage(self):
        return self._damage

    def get_armor(self):
        return self._armor
    
    def get_duration(self):
        return self._duration

    def get_mana_regen(self):
        return self._mana_regen 
    
    def get_effect_applied_count(self):
        return self._effect_applied_count

    def increment_effect_applied_count(self):
        self._effect_applied_count += 1


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

    def get_mana(self):
        return self._mana

    def use_mana(self, mana_used: int):
        if mana_used > self._mana:
            raise ValueError("Not enough mana!")
        
        self._mana -= mana_used

    def get_active_effects(self):
        return self._active_effects

    def take_turn(self, spell_key: str, other_player: Player) -> int:
        """ This player takes a turn.
        This means: casting a spell, applying any effects, and fading any expired effects

        Args:
            spell_key (str): The spell key, from SpellFactory.SpellConstants
            other_player (Player): The opponent

        Returns:
            int: The mana consumed by this turn
        """
        self.apply_effects(other_player)
        self.fade_effects()
        mana_consumed = self.cast_spell(spell_key, other_player)

        return mana_consumed

    def opponent_takes_turn(self, other_player: Player):
        """ An opponent takes their turn.  (Not the wizard.)
        We must apply any Wizard effects on their turn (and fade), before their attack.
        This method does not include their attack.

        Args:
            other_player (Player): [description]
        """
        self.apply_effects(other_player)
        self.fade_effects()        

    def cast_spell(self, spell_key: str, other_player: Player) -> int:
        """ Casts a spell.
        If spell is not an effect, it applies once.
        Otherwise, it applies for the spell's duration, on both player and opponent turns.

        Args:
            spell_key (str): a SpellType constant.
            other_player (Player): The other player

        Returns:
            [int]: Mana consumed
        """
        SpellFactory.check_spell_castable(spell_key, self)

        spell = SpellFactory.create_spell(spell_key)
        try:
            self.use_mana(spell.get_mana_cost())
        except ValueError as err:
            raise ValueError(f"Unable to cast {spell_key}: Not enough mana! " \
                             f"Needed {spell.get_mana_cost()}; have {self._mana}.") from err

        logger.debug("%s casted %s", self._name, spell)

        if spell.is_effect():
            # add to active effects, apply later
            # this might replace a fading effect
            self._active_effects[spell_key] = spell
        else:
            # apply now.
            # opponent's armor counts for nothing against a magical attack
            attack_damage = spell.get_damage()
            if attack_damage:
                logger.debug("%s attack. Inflicting damage: %s.", self._name, attack_damage)
                other_player.take_hit(attack_damage)

            heal = spell.get_heal()
            if heal:
                logger.debug("%s: healing by %s.", self._name, heal) 
                self._hit_points += heal

        return spell.get_mana_cost()                        
            
    def fade_effects(self):
        effects_to_remove = []
        for effect_name, effect in self._active_effects.items():
            if effect.get_effect_applied_count() >= effect.get_duration():
                logger.debug("%s: fading effect %s", self._name, effect_name)
                if effect.get_armor():
                    # restore armor to pre-effect levels
                    self._armor -= effect.get_armor()

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
            if effect.get_effect_applied_count() < effect.get_duration():
                effect.increment_effect_applied_count()
                logger.debug("%s: applying effect %s, leaving %d turns.", 
                        self._name, effect_name, effect.get_duration() - effect.get_effect_applied_count())

                if effect.get_armor():
                    if effect.get_effect_applied_count() == 1:
                        # increment armor on first use, and persist this level until the effect fades
                        self._armor += effect.get_armor()

                if effect.get_damage():
                    other_player.take_hit(effect.get_damage())
                
                if effect.get_mana_regen():
                    self._mana += effect.get_mana_regen()
        
    def attack(self, other_player: Player):
        """ A Wizard cannot perform a mundane attack.
        Use cast_spell() instead.
        """
        raise NotImplementedError("Wizards cast spells")


    def __repr__(self):
        return f"{self._name} (Wizard): hit points={self._hit_points}, " \
                        f"damage={self._damage}, armor={self._armor}, mana={self._mana}"
    
def main():
    boss_file = path.join(locations.input_dir, BOSS_FILE)
    
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

    attack_combos_lookups = attack_combos_generator(NUM_ATTACKS, len(spell_key_lookup))

    winning_games = {}
    least_winning_mana = 10000
    ignore_combo = "9999999"
    player_has_won = False
    
    for attack_combo_lookup in attack_combos_lookups:
        # since attack combos are returned sequentially, 
        # we can ignore any that start with the same attacks as the last failed combo.
        if attack_combo_lookup.startswith(ignore_combo):
            continue  
        
        # boss = Player("Boss", hit_points=boss_hit_points, damage=boss_damage, armor=0)
        boss = Player("Boss Socks", hit_points=40, damage=10, armor=0)
        player = Wizard("Bob", hit_points=50, mana=500)
    
        if player_has_won:
            logger.info("Best winning attack: %s. Total mana: %s. Current attack: %s", 
                        winning_games[least_winning_mana], least_winning_mana, attack_combo_lookup)
        else:
            logger.debug("Current attack: %s", attack_combo_lookup)

        # Convert the attack combo to a list of spells.
        # E.g. convert 4111000 to 
        # ['recharge', 'drain', 'drain', 'drain', 'magic_missiles', 'magic_missiles', 'magic_missiles']
        attack_combo = [spell_key_lookup[int(attack)] for attack in attack_combo_lookup]
        player_won, mana_consumed, rounds_started = play_game(attack_combo, player, boss, hard_mode=True, mana_target=least_winning_mana)
        if player_won:
            player_has_won = True
            winning_games[mana_consumed] = attack_combo_lookup
            least_winning_mana = min(mana_consumed, least_winning_mana)      
        
        # we can ingore any attacks that start with the same attacks as what we tried last time
        ignore_combo = attack_combo_lookup[0:rounds_started]
        
    logger.info("We found %d winning solutions. Lowest mana cost was %d.", len(winning_games), least_winning_mana)
    logger.info("Winning solutions: %s", winning_games)

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

    while (player.hit_points > 0 and boss.hit_points > 0):
        if current_player == player:
            # player (wizard) attack
            logger.debug("")
            logger.debug("Round %s...", i)

            logger.debug("%s's turn:", current_player.name)
            if hard_mode:
                logger.debug("Hard mode hit. Player hit points reduced by 1.")
                player.take_hit(1)
                if player.hit_points <= 0:
                    logger.debug("Hard mode killed %s", boss.name)
                    continue
            try:
                mana_consumed += player.take_turn(attacks[i-1], boss)
                if mana_target and mana_consumed > mana_target:
                    logger.debug('Mana target %s exceeded; mana consumed=%s.', mana_target, mana_consumed)
                    return False, mana_consumed, i
            except ValueError as err:
                logger.debug(err)
                return False, mana_consumed, i
            except IndexError:
                logger.debug("No more attacks left.")
                return False, mana_consumed, i

        else:
            logger.debug("%s's turn:", current_player.name)
            # effects apply before opponent attacks
            player.opponent_takes_turn(boss)
            if boss.hit_points <= 0:
                logger.debug("Effects killed %s!", boss.name)
                continue

            boss.attack(other_player)
            i += 1

        logger.debug("End of turn: %s", player)
        logger.debug("End of turn: %s", boss)

        # swap players
        current_player, other_player = other_player, current_player

    player_won = player.hit_points > 0
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
    logger.info("Execution time: %.3f seconds", t2 - t1)
