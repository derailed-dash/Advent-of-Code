""" 
Author: Darren
Date: 16/02/2021

Solving https://adventofcode.com/2015/day/15

Cookie recipes contain exactly 100 spoonfulls of ingredients.
Each ingredient is made up of 5 properties: capacity, durability, flavour, texture, calories.
Each ingredient has a score for each of these properties.
Score of each property = qty1 * ingr1 + qt2 * ingr2... (or 0 if score is -ve)

Overall cookie score = product of all properties

Solution 1 of 3:
    Determine possible permutations by finding all combinations first (with replacement),
    and then expanding to permutations of those combinations.

Part 1:
    Goal: Determine score of best cookie.
    
    Get all permutations of quantities that sum to 100, 
    where the number of quantities is the number of ingredients.
    Note that Python permutations function is not suitable, as it doesn't allow for repeating quantities in our 100.
    So, we can either use catesian product (slow @13s, because there are many results), 
    or we can use combinations_with_replacement, 
    and then expand these to the possible permutations of those combinations. (Much faster: ~1s.)
    For each permutation of ingredients, compute sum of quantities * prop.


Part 2:
    Goal: Determine score of best cookie where calories == 500.
    As before, but filter on calories == 500.
"""
from dataclasses import dataclass
from pathlib import Path
import time
from itertools import permutations, combinations_with_replacement
from math import prod
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

CAL_TARGET = 500
INGREDIENT_QTY = 100

@dataclass(frozen=True)
class Cookie:
    """ A cookie is made up of 4 ingredients with quantities (a, b, c, d)
    and it has a score and calorie value """
    ingredients: tuple  # Ingredient amounts, e.g. (28, 35, 18, 19)
    score: int   
    calories: int

    def __str__(self) -> str:
        return f"{str(self.ingredients)}, cals={self.calories}, score={self.score}"

@dataclass
class Ingredient:
    """ Every ingredient has a name, and a set of five properties:
        capacity, durability, flavour, texture, calories. """
    CALORIES = "calories"
    
    name: str
    properties: dict

    def __post_init__(self) -> None:
        """ We pop 'calories' and store as a separate property.
        Note that the dataclass automatically calls __post_init__() after __init__(), 
        if the method is defined. """
        self.calories = self.properties.pop(Ingredient.CALORIES)

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()

    ingr_list = process_ingredients(data)

    cookies: list[Cookie] = []
    perms = find_permutations(INGREDIENT_QTY, len(ingr_list))

    print(f"A total of {len(perms)} cookie recipes to process...")
    for perm in perms:   # e.g. with 2 ingredients, a perm might be (44, 56)
        prop_scores = defaultdict(int)
        calories = 0
        for qty, ingr in zip(perm, ingr_list):
            for prop, value in ingr.properties.items():
                prop_scores[prop] += qty * value

            calories += qty * ingr.calories

        # If any properties have negative value, set it to 0.
        for prop, value in prop_scores.items():
            if value < 0:
                prop_scores[prop] = 0
    
        total_score = prod(list(prop_scores.values()))
        cookies.append(Cookie(perm, total_score, calories))

    # Part 1
    best_cookie = max(cookies, key=lambda x: x.score)
    print(f"Best cookie: {best_cookie}")

    # Part 2
    fixed_cal_cookies = list(filter(lambda x: x.calories == CAL_TARGET, cookies))
    best_fixed_cal_cookie = max(fixed_cal_cookies, key=lambda x: x.score)
    print(f"Best {CAL_TARGET} calorie cookie: {best_fixed_cal_cookie}")

def find_permutations(target: int, terms: int) -> set[tuple]: 
    """ Return all permutations of terms that sum to the target number.
    We need to include repeats. E.g. (10, 10, 40, 40) would be valid.
    Use combinations_with_replacement. E.g. if target = 6 and terms = 2, the results would be:
    (0, 6), (1, 5), (2, 4), (3, 3).
    However, order is important since (0, 6) is different properties to (6, 0).
    So we need to determine the permutations for each combo.

    Returns: Set containing tuples of valid term permutations """
    
    combos = [combo for combo in combinations_with_replacement(range(target), terms) if sum(combo) == target]
    perms_of_combos = set() # use a set to filter out duplicates
    for combo in combos:
        for perm in permutations(combo):
            perms_of_combos.add(perm) 
    
    return perms_of_combos

def process_ingredients(data: list) -> list[Ingredient]:
    ingr_list = []
    for line in data:
        name, properties = line.split(":")
        properties = [x.strip().split(" ") for x in properties.split(",")]
        props_dict = {prop[0]:int(prop[1]) for prop in properties}
        ingr_list.append(Ingredient(name, props_dict))

    return ingr_list

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
