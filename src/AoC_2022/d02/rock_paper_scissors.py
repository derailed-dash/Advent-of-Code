"""
Author: Darren
Date: 02/12/2022

Solving https://adventofcode.com/2022/day/2

Rock, Paper, Scissors

For each hand, the score is the sum of the following:
- 0 for lose, 3 for draw, 6 for win
- 1 if we play Rock, 2 if we play Paper, 3 if we play Scissors

Input is a list of rounds, in format "A X".

Part 1:

Get our total score.
- Treat first column as what they play. A=Rock, B=Paper, C=Scissors
- Treat second column as what we play. X=Rock, Y=Paper, Z=Scissors

Part 2:

Get our total score.
- Treat first column as what they play. A=Rock, B=Paper, C=Scissors
- Treat second column as outcome required. X=Lose, Y=Draw, Z=Win

"""
from pathlib import Path
import time

HAND = {
    "ROCK": "A",
    "PAPER": "B",
    "SCISSORS": "C"
}

SCORES = {
    "X": 1,
    "Y": 2,
    "Z": 3,
    "ROCK": 1,
    "PAPER": 2,
    "SCISSORS": 3,
    "LOSE": 0,
    "DRAW": 3,
    "WIN": 6
}

REQUIRED = {
    "LOSE": "X",
    "DRAW": "Y",
    "WIN": "Z"
}

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
    
    # Part 1
    rounds = play_rounds(data)
    scores = play_part_1(rounds)
    print(f"Part 1: Your score = {sum(scores)}")
    
    scores = play_part_2(rounds)
    print(f"Part 2: Your score = {sum(scores)}")

def play_part_2(rounds: list):
    """ Here we treat X, Y, Z as whether we play Lose, Draw, or Win, respectively. 
    Determine what hand we should play to achieve that outcome.
    Then calculate our score for each hand based on what hand we chose, and whether we win, lose or draw. """
    scores = []
    for this_round in rounds:
        this_score = 0

        if this_round[1] == REQUIRED["LOSE"]:
            this_score += SCORES["LOSE"]
            
            if this_round[0] == HAND["PAPER"]:
                this_score += SCORES["ROCK"]
            elif this_round[0] == HAND["ROCK"]:
                this_score += SCORES["SCISSORS"]
            else:
                this_score += SCORES["PAPER"]
        elif this_round[1] == REQUIRED["DRAW"]:
            this_score += SCORES["DRAW"]
            
            if this_round[0] == HAND["PAPER"]:
                this_score += SCORES["PAPER"]
            elif this_round[0] == HAND["ROCK"]:
                this_score += SCORES["ROCK"]
            else:
                this_score += SCORES["SCISSORS"]
        else: # I must win
            this_score += SCORES["WIN"]
            
            if this_round[0] == HAND["PAPER"]:
                this_score += SCORES["SCISSORS"]
            elif this_round[0] == HAND["ROCK"]:
                this_score += SCORES["PAPER"]
            else:
                this_score += SCORES["ROCK"]
    
        scores.append(this_score)
        
    return scores           
    
def play_part_1(rounds: list):
    """ Here we treat X, Y, Z as whether we play Rock, Paper, Scissors, respectively. 
    Calculate our score for each hand based on what hand we play, and whether we win, lose or draw. """
    scores = []
    for this_round in rounds:
        this_score = 0
        this_score += SCORES[this_round[1]]
        
        if this_round[1] == "X": # I play rock
            if this_round[0] == HAND["ROCK"]: # they play rock
                this_score += SCORES["DRAW"]
            elif this_round[0] == HAND["SCISSORS"]: # they play scissors
                this_score += SCORES["WIN"]
        elif this_round[1] == "Y": # I play paper
            if this_round[0] == HAND["PAPER"]: # they play paper
                this_score += SCORES["DRAW"]
            elif this_round[0] == HAND["ROCK"]: # they play rock
                this_score += SCORES["WIN"]
        else: # I play scissors
            if this_round[0] == HAND["SCISSORS"]: # they play scissors
                this_score += SCORES["DRAW"]
            elif this_round[0] == HAND["PAPER"]: # they play paper
                this_score += SCORES["WIN"]
    
        scores.append(this_score)
    
    return scores              

def play_rounds(data: list[str]) -> list:
    """ Returns a list. Each element in the list is a pair as a list, e.g. ["A", "X"] """
    rounds = []
    for this_round in data:
        rounds.append(this_round.split())
    
    return rounds

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
