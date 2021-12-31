import os
import time

INPUT_FILE = "input/data.txt"
SAMPLE_INPUT_FILE = "input/sample_data.txt"

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)
    data = read_input(input_file)

    player_1_deck, player_2_deck = process_data(data)
    play_simple_game(player_1_deck.copy(), player_2_deck.copy())

    recursive_game(player_1_deck.copy(), player_2_deck.copy(), 0)


def recursive_game(deck_1, deck_2, depth):
    # return False if player_1 wins, or True for player_2

    previous_hands = set()
    
    while deck_1 and deck_2:
        # if the same hand has been played before, p1 wins
        # this is to avoid infinitely playing the same hand
        current_hand = str(deck_1) + str(deck_2)
        if current_hand in previous_hands:
            # p1 win
            return False
        previous_hands.add(current_hand)

        # draw cards from each deck
        p1_card = deck_1.pop()
        p2_card = deck_2.pop()

        # if we've got enough cards to play the recursive game, do so
        # i.e. based on there being at least as many cards as the value of the card drawn
        if len(deck_1) >= p1_card and len(deck_2) >= p2_card:
            sub_deck_1 = deck_1[-p1_card:].copy()
            sub_deck_2 = deck_2[-p2_card:].copy()

            p2_win = recursive_game(sub_deck_1, sub_deck_2, depth+1)
        else:
            # otherwise, basic game rules apply
            # i.e. highest drawn card wins
            p2_win = (p2_card > p1_card)

        # put drawn cards at the bottom of the round winner's deck
        if (p2_win):
            deck_2.insert(0, p2_card)
            deck_2.insert(0, p1_card)
        else:
            deck_1.insert(0, p1_card)
            deck_1.insert(0, p2_card)
    
    if deck_2:
        p2_win = True
        winning_deck = deck_2
        winning_player = 2
    else:
        p2_win = False
        winning_deck = deck_1
        winning_player = 1
    
    if (depth == 0):
        score = evaluate_score(winning_deck)
        print(f"Recursive game, winning player {winning_player} score: {score}")

    return p2_win  


def evaluate_score(deck):
    score = 0
    score = sum((i+1)*card for i, card in enumerate(deck))
    
    return score


def play_simple_game(deck_1, deck_2):
    while deck_1 and deck_2:
        player_1_card = deck_1.pop()
        player_2_card = deck_2.pop()

        if player_1_card > player_2_card:
            deck_1.insert(0, player_1_card)
            deck_1.insert(0, player_2_card)
        else:
            deck_2.insert(0, player_2_card)
            deck_2.insert(0, player_1_card)

    if deck_1:
        winning_deck = deck_1
        winning_player = 1
    else:
        winning_deck = deck_2
        winning_player = 2

    score = evaluate_score(winning_deck)
    print(f"Basic game, winning player {winning_player} score: {score}")


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read()

    return data


def process_data(data):
    player_1_deck = []
    player_2_deck = []

    players = data.split("\n\n")
    for player_deck, player_data in zip([player_1_deck, player_2_deck], players):
        for i, card in enumerate(player_data.splitlines()):
            if (i == 0):
                continue
            player_deck.append(int(card))
        
    return player_1_deck[::-1], player_2_deck[::-1]


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
