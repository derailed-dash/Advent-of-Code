import os
import time
import re
from collections import defaultdict

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
    # print(data)

    combos = init_combos(data)

    refined_candidates, not_candidates = process_combos(combos)
    not_candidate_occurences = 0
    for ingredient in not_candidates:
        for combo in combos:
            ingredients_list = combo[0]
            if ingredient in ingredients_list:
                not_candidate_occurences += 1

    print(f"Occurrences of non-candidates: {not_candidate_occurences}")

    assigned_allergens = assign_allergens(refined_candidates)
    canonical_dangerous_ingredients = []
    for allergen in sorted(assigned_allergens.keys()):
        ingredient = assigned_allergens[allergen]
        canonical_dangerous_ingredients.append(ingredient)

    print("Canonical dangerous ingredients: " + ",".join(canonical_dangerous_ingredients))


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read()

    return data.splitlines()


def process_combos(combos):
    unique_ingredients = set()
    ingredient_candidates = defaultdict(list)

    for item in combos:
        ingredients = item[0]
        allergens = item[1]
        unique_ingredients.update(ingredients) 

        # build a dict containing potential ingredients for each allergen
        for allergen in allergens:
            ingredient_candidates[allergen].append(set(ingredients))

    refined_candidates = {}
    # process each set of ingredient candidates for each allergen
    # refine by only taking the intersection 
    for allergen, ingredient_list in ingredient_candidates.items():
        # Here, * is iterable unpacking, to expand the list of sets
        refined_candidates[allergen] = set.intersection(*ingredient_list)    

    all_refined_candidates = set()
    # unpack all the refined_candidates sets, and make superset.
    all_refined_candidates.update(*refined_candidates.values())
    not_candidates = unique_ingredients.difference(all_refined_candidates)

    return refined_candidates, not_candidates


def assign_allergens(candidates):
    # Candidates look like...
    # 'fish': {'sqjhc', 'mxmxvkd'}

    # create dict of { allergen: ingredient }
    assigned_allergens = {}

    while len(assigned_allergens) < len(candidates):
        for candidate in candidates:
            ingredients = set(candidates[candidate])

            # take the list of ingredients for this allergen,
            # and then remove any ingredients we've already allocated
            ingredients.difference_update(assigned_allergens.values())
            
            # When we're down to one ingredient, we can assign it to the allergen
            if len(ingredients) == 1: 
                assigned_allergens[candidate] = ingredients.pop()

    return assigned_allergens


def init_combos(data):
    word_matcher = re.compile(r"[a-z]+")
    CONTAINS = "contains"

    combos = []

    for row in data:
        matches = word_matcher.findall(row)
        if CONTAINS in matches:
            contains_index = matches.index(CONTAINS)
            ingr = set(matches[0:contains_index])
            allergens = set(matches[contains_index+1:])
        else:
            ingr = set(matches)
            allergens = set()

        combos.append([ingr, allergens])
    
    return combos


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")

