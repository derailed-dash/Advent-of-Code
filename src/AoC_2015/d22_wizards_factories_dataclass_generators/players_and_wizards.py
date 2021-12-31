"""Player Class"""
from __future__ import absolute_import, annotations
import logging
from math import ceil
from dataclasses import dataclass

# pylint: disable=too-few-public-methods, inherit-non-class
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

    def get_name(self) -> str:
        return self._name

    def get_hit_points(self) -> int:
        return self._hit_points

    def get_armor(self) -> int:
        return self._armor

    def take_hit(self, loss: int):
        self._hit_points -= loss

    def is_alive(self) -> bool:
        return self._hit_points > 0

    def get_attack_damage(self, other_player: Player) -> int:
        """Damage inflicted in an attack.  Given by this player's damage minus other player's armor.

        Args:
            other_player (Player): The defender

        Returns:
            int: The damage inflicted per attack
        """
        return max(self._damage - other_player.get_armor(), 1)

    def get_attacks_needed(self, other_player: Player) -> int:
        """The number of conventional attacks needed for this player to defeat the other player.

        Args:
            other_player (Player): The other player

        Returns:
            int: The number of rounds needed.
        """
        return ceil(other_player.get_hit_points() / self.get_attack_damage(other_player))

    def will_defeat(self, other_player: Player) -> bool:
        """ Determine if this player will win a fight with an opponent.
        I.e. if this player needs fewer (or same) attacks than the opponent.
        Assumes this player always goes first.
        """
        return (self.get_attacks_needed(other_player) 
                <= other_player.get_attacks_needed(self))

    def attack(self, other_player: Player):
        attack_damage = self.get_attack_damage(other_player)
        logging.debug("%s attack. Inflicting damage: %d.", self._name, attack_damage)
        other_player.take_hit(attack_damage)
    
    def __repr__(self):
        return f"{self._name} (Mundane): hit points={self._hit_points}, damage={self._damage}, armor={self._armor}"


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

        logging.debug("%s casted %s", self._name, spell)

        if spell.is_effect():
            # add to active effects, apply later
            # this might replace a fading effect
            self._active_effects[spell_key] = spell
        else:
            # apply now.
            # opponent's armor counts for nothing against a magical attack
            attack_damage = spell.get_damage()
            if attack_damage:
                logging.debug("%s attack. Inflicting damage: %s.", self._name, attack_damage)
                other_player.take_hit(attack_damage)

            heal = spell.get_heal()
            if heal:
                logging.debug("%s: healing by %s.", self._name, heal) 
                self._hit_points += heal

        return spell.get_mana_cost()                        
            
    def fade_effects(self):
        effects_to_remove = []
        for effect_name, effect in self._active_effects.items():
            if effect.get_effect_applied_count() >= effect.get_duration():
                logging.debug("%s: fading effect %s", self._name, effect_name)
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
                logging.debug("%s: applying effect %s, leaving %d turns.", 
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
    