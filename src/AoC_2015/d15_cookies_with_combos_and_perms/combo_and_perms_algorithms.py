"""
Find all combinations of two digits that sum to TARGET
Vary the RANGE_SIZE and TERMS to see impact on efficiency
"""
from itertools import combinations_with_replacement, permutations, combinations, product
import time

RANGE = 500
TERMS = 3
TARGET = 10

# Get all permutations, but note that (5, 5) is not a valid permutation
# since 5 only appears in the range once
def use_perms():
    name = "use_perms"
    result = [perm for perm in permutations(range(RANGE+1), TERMS) if sum(perm) == TARGET]
    return name, result

# Get all combinations, filtering out duplicates with different order
# Again (5, 5) is not a valid permutation
def use_combos():
    name = "use_combos"
    result = [combo for combo in combinations(range(RANGE+1), TERMS) if sum(combo) == TARGET]
    return name, result   

# Get all permutations using a cartesian product.
# Effectively, a cartesian product of range(10) with range(10)
# Thus, (5, 5) is possible
def use_product():
    name = "use_product"
    result = [perm for perm in product(range(RANGE+1), repeat=TERMS) if sum(perm) == TARGET]
    return name, result

# Get all combinations, filtering out duplicates with different order, 
# but allowing duplicates of any digit.  Thus (5, 5) is a valid result
def use_combos_with_replacement():
    name = "use_combos_with_replacement"
    result = [combo for combo in combinations_with_replacement(range(RANGE+1), TERMS) if sum(combo) == TARGET]
    return name, result    

# Take our valid combinations, and then find all permutations of just those combos
# E.g. the perms for (1, 9) will be (1, 9) and (9, 1)
# Use a set to eliminate duplicates such as (5, 5) and (5, 5)
def use_perms_of_combos(combos_with_replacement):
    name = "use_perms_of_combos"
    perms_of_combos = set()
    for combo in combos_with_replacement:
        for perm in permutations(combo):
            perms_of_combos.add(perm)
    
    return name, perms_of_combos

# recursively return each valid permutation, using a generator
def recursive_sub_sum(terms, target):
    if terms <= 1:
        yield [target]
    else:
        for i in range(target + 1):
            for value in recursive_sub_sum(terms - 1, target - i):
                yield [i] + value


def main():
    functions_list = []
    functions_list.append(tuple([use_combos]))
    functions_list.append(tuple([use_product]))
    functions_list.append(tuple([use_perms]))
    functions_list.append(tuple([use_combos_with_replacement]))
    functions_list.append(tuple([use_perms_of_combos, use_combos_with_replacement]))

    for func in functions_list:
        t1 = time.perf_counter()
        if len(func) == 2:
            # the 2nd item is a function.  The functions all return data in element [1]
            result = func[0](func[1]()[1])
        else:
            result = func[0]()
        # print(f"{result[0]}: {result[1]}")
        t2 = time.perf_counter()
        print(f"Execution time for {result[0]}: {t2 - t1:0.4f} seconds, with {len(result[1])} items")

    t1 = time.perf_counter()
    recursive_perms = list(recursive_sub_sum(TERMS, TARGET))
    # print(recursive_perms)
    t2 = time.perf_counter()
    print(f"Execution time for recusive_perms: {t2 - t1:0.4f} seconds, with {len(recursive_perms)} items")


if __name__ == "__main__":
    main()
