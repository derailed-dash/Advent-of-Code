"""Player Class"""
from __future__ import annotations
from math import ceil

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
