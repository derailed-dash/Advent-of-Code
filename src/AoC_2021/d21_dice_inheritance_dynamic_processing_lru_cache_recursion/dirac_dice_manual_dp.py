"""
Author: Darren
Date: 21/12/2021

Solving https://adventofcode.com/2021/day/21

Dirac dice. Circular board wtih spaces marked 1-10.
Starting space chosen randomly (input). Player 1 goes first.
Player rolls die 3 times, adds up the score, and moves around the circle
that many spaces.  Score is increased by the space the player lands on.
Game ends when either player reaches 1000.

Part 1:
    - We're using deterministic die.
      The value of each rolling increases by 1.  Wraps back around to 1 after 100. 
    - Player class to store player position and cumulative score.
    - Die class to store total rolls and return a die roll.
    - Game class that stores players and die, and knows how to play a game.
    - Game execution is through calling the _turn() method once per player, until target is reached.
    
Part 2:
    - 3-sided die. Each roll of the die splits the universe.
    - Solve with dynamic processing, i.e. brute force + caching of game states.
    - Create a recursive function that returns the number of ways a player can win,
      with given position and score for both players.
      If score >= 21, that player has won.  For any other state, roll all possible roll triplets,
      update the player's position and score accordingly, then recurse next state with other player.
    - Cache using a dict, which stores the arguments as key. 
"""
from __future__ import annotations
import logging
import os
import time
from typing import Iterator, NamedTuple
from copy import deepcopy
from itertools import product

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dp_cache = {} # Cache game states for our recursion

class Player(NamedTuple):
    """ A player has a current position on the board, and a cumulative score """
    posn: int
    score: int

class AbstractDie():
    """ Abstract die """
    def __init__(self, faces: int) -> None:
        self._faces = faces
        self._total_rolls = 0   # How many times have we rolled this die
        self._roll_gen = self._roll()   # A generator that performs the roll.
            
    @property
    def total_rolls(self):
        return self._total_rolls
    
    @property
    def roll(self):
        """ This is how we roll the die. Calls next() on the roll generator. """
        return next(self._roll_gen)
    
    def _roll(self) -> Iterator[int]:
        """ We need to override this method. """
        return NotImplemented
                
class DeterministicDie(AbstractDie):
    """ Subclass of AbstractDie. Persists state between rolls.
    Always yields an incrementing int from the number of available faces, starting at 1.
    E.g. from 1-100. When we get to the number of faces, we wrap back around to 1. """
    
    def _roll(self) -> Iterator[int]:
        """ Yield the next available number. """
        while True:
            for i in range(1, self._faces+1):
                self._total_rolls += 1
                yield i

class Game():
    """ We're on a circular track, with grid numbers 1 to 10. The player moves around the circle with each go.
    If the player lands on number x, the player gains x points.
    The player starts on an arbitrary grid number, and with a score of 0. """
    SPACES = 10
    ROLLS_PER_TURN = 3    
    
    def __init__(self, players: list[Player], die: AbstractDie, target: int) -> None:
        self._players = players  # OUr two players.
        self._die = die          # Our die may be deterministic, so we need to store die state
        self._target = target    # The score a player needs to reach, to win the game    
    
    @property
    def players(self):
        return self._players
    
    @property
    def die(self):
        return self._die
    
    def play(self) -> int:
        """ Play a game. Each player takes a turn, until the target score is reached by a player. """
        while True:
            for player_num in range(len(self.players)):
                score = self._take_turn(player_num)
                if score >= self._target:   # This player has won!
                    return player_num
        
        assert False, "Game should end!"
        
    def _take_turn(self, player_num: int) -> int:
        """ Takes a turn for this player.  Roll the die n (e.g. 3) times, to give score x.
        Then move around the circle x places.  Whatever we land on, that's the score returned.
        Add this to existing score. Update the player.  Returns the cumulative score of the player """

        old_posn, old_total = self.players[player_num] # unpack the player
        
        die_score = sum(self._die.roll for i in range(Game.ROLLS_PER_TURN)) # Roll n times
        new_posn = (((old_posn + die_score)-1) % Game.SPACES) + 1 # Move forward n spaces
        new_total = old_total + new_posn  # Add new board position to existing player score
        self.players[player_num] = Player(new_posn, new_total)  # Update the player
        
        return new_total     


def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()

    init_players: list[Player] = []
    for line in data:
        tokens = line.split() # Into 5 tokens, e.g. "Player" "1" "starting" "position:" "4"
        init_players.append(Player(posn=int(tokens[-1]), score=0))

    # Part 1
    players = deepcopy(init_players)
    die = DeterministicDie(faces=100)
    game = Game(players, die, target=1000)
    won = game.play()
    
    total_rolls = game.die.total_rolls
    logger.debug("Die has been rolled %d times", total_rolls)
    logger.info("Player %d won with score of: %d", won+1, players[won].score)
    logger.info("Part 1 result = %d\n", total_rolls * min(player.score for player in game.players))
    
    # Part 2
    # With a given game state, player_1 starts at posn_1 with score_1and player_2 at posn_2 with score_2.
    # How many ways can they win from this state?
    players = deepcopy(init_players)
    
    wins = count_wins(players[0].posn, players[1].posn, players[0].score, players[1].score)
    for i, win in enumerate(wins):
        logger.info("Player %d wins: %d", i+1, win)
        
    logger.info("Part 2: universes in which the player wins the most = %d", max(wins))
     
def count_wins(posn_a: int, posn_b: int, score_a: int, score_b: int) -> tuple[int, int]:
    """ Return number of universes in which each player can win from this state.
    With a given game state, player a starts at posn_a with score_a and player b at posn_b with score_b.
    Player a's turn.

    Args:
        posn_a (int): Current position of player a
        posn_b (int): Current position of player b
        score_a (int): Current score of player a
        score_b (int): Current score of player b

    Returns:
        tuple[int, int]: Ways to win for player a, player a
    """
    if score_a >= 21:
        return (1, 0)   # Player A has won; player B has lost. No other options are possible.
    
    if score_b >= 21:
        return (0, 1)   # Player B has won; player A has lost. No other options are possible.
    
    if (posn_a, posn_b, score_a, score_b) in dp_cache:
        return dp_cache[posn_a, posn_b, score_a, score_b]
    
    result = (0, 0)     # Initiliase; no wins yet
    
    # Sums of possible die rolls, i.e. 3x3x3 = 27 different ways of rolling.
    triple_roll_sums = [sum(prod) for prod in product(range(1, 4), repeat=3)] 
    for score in triple_roll_sums:  # 1x3, 3x4, 6x5, etc.
        new_posn_a = (posn_a + score - 1) % Game.SPACES + 1
        new_score_a = score_a + new_posn_a
        
        # Now recurse to find the number of ways each player can win from this new game state.
        # Next move is from player b. So, next call will return (ways b, ways a)
        ways_b, ways_a = count_wins(posn_b, new_posn_a, score_b, new_score_a)
        result = (result[0]+ways_a, result[1]+ways_b)   # add to current
    
    dp_cache[posn_a, posn_b, score_a, score_b] = result # cache this result for this game state  
    return result

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
