""" 
Author: Darren
Date: 18/02/2021

Solving https://adventofcode.com/2015/day/15

Cookie recipes contain exactly 100 spoonfulls of ingredients.
Each ingredient is made up of 5 properties: capacity, durability, flavour, texture, calories.
Each ingredient has a score for each of these properties.
Score of each property = qty1 * ingr1 + qt2 * ingr2... (or 0 if score is -ve)

Overall cookie score = product of all properties

Solution 3 of 3:
    Uses the "subset with sum" pattern, expanded to find all permutations of a given number of terms.
    E.g. using this base pattern: https://www.geeksforgeeks.org/count-of-subsets-with-sum-equal-to-x-using-recursion/
    Here, the number of terms is given by the length of the ingredients list.

    This approach is much faster (but more complicated) than using itertools product / combinations / permutations.
    Overall solution time is ~0.1s.
"""
import re
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

CAL_TARGET = 500
INGREDIENT_QTY = 100

NAME = "Name"
CAPACITY = "capacity"
DURABILITY = "durability"
FLAVOR = "flavor"
TEXTURE = "texture"
CALORIES = "calories"

def main():
    ingredients = []
    with open(INPUT_FILE, mode="rt") as f:
        p = re.compile(r'^([A-Za-z]+): capacity (-?[0-9]+), durability (-?[0-9]+), flavor (-?[0-9]+), texture (-?[0-9]+), calories (-?[0-9]+)$')
        for line in f:
            name, cap, dur, flav, text, cal = p.findall(line.strip())[0]
            cap, dur, flav, text, cal = map(int, [cap, dur, flav, text, cal])
            ingredients.append({NAME: name, CAPACITY: cap, DURABILITY: dur, FLAVOR: flav, TEXTURE: text, CALORIES: cal})

    for ingredient in ingredients:
        print(ingredient)
        
    print(find_max_score(ingredients, 0, [0]*len(ingredients), INGREDIENT_QTY))

def ingredient_prop_score(ingredients: list, quantities: list, prop) -> int: 
    """Get score for this property, by calculating the sum of the prop*mass for each ingredient used

    Args:
        ingredients ([list]): ingredients list
        masses ([list]): masses, indexed to the ingredients
        prop ([type]): the property we want to calculate score for

    Returns:
        [int]: Score for this property, or 0 if the score is negative
    """
    return max(sum([ingredient[prop] * mass for ingredient, mass in zip(ingredients, quantities)]), 0)

def score(ingredients, quantities): 
    return (ingredient_prop_score(ingredients, quantities, CAPACITY)
            * ingredient_prop_score(ingredients, quantities, DURABILITY) 
            * ingredient_prop_score(ingredients, quantities, FLAVOR) 
            * ingredient_prop_score(ingredients, quantities, TEXTURE))

def find_max_score(ingredients: list, current_ingr: int, ingr_quantities: list, remaining_qty: int) -> int:
    """Determine max score for these ingredients

    Args:
        ingredients ([list]): list of ingredients
        current_ingr ([int]): current ingr index
        ingr_quantities ([list]): list of quantities, for each ingredient
        remaining_qty ([int]): ingredients qty left to add

    Returns:
        [int]: Best cookie score
    """
    # we're on the last ingredient
    if current_ingr == len(ingredients)-1:
        ingr_quantities[current_ingr] = remaining_qty
        if ingredient_prop_score(ingredients, ingr_quantities, CALORIES) != CAL_TARGET: return 0
        return score(ingredients, ingr_quantities)

    best_score = 0
    for m in range(1, remaining_qty):
        ingr_quantities[current_ingr] = m

        # recurse into this method, incrementing current ingr (if we're not on the last ingr)
        # and decrementing the remainder
        best_score = max(best_score, find_max_score(ingredients, current_ingr+1, ingr_quantities, remaining_qty-m))

    return best_score

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
