---
title: Permutations and Combinations

main_img:
  name: perms-and-combos
  link: /assets/images/permutations-combinations-definition.png
tags: 
  - name: Itertools
    link: https://docs.python.org/3/library/itertools.html
  - name: Permutations and Combinations
    link: https://www.geeksforgeeks.org/permutation-and-combination-in-python/
  - name: Permutations with Examples
    link: https://www.pythonpool.com/python-permutations/
---
<script id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

## Page Contents

- [Overview of Permutations and Combinations](#overview-of-permutations-and-combinations)
- [Demonstrating With Code](#demonstrating-with-code)
- [Rolling Dice Examples](#rolling-dice-examples)

## Overview of Permutations and Combinations

||Permutations|Combinations|
|-|------------|------------|
|What is it?|The number of ways to arrange items|The number of ways to choose items|
|Ordering   |Important|Irrelevant|
|Number of sequences of length r from data of length n|\\(^nP_r = \frac{n!}{(n-r)!}\\)|\\(^nC_r = \frac{n!}{r!(n-r)!}\\)|
|Number of sequences of length 4 from digits 1,2,3,4|\\(^nP_r = \frac{4!}{(4-4)!} = 24\\)|\\(^nC_r = \frac{4!}{4!.(4-4)!} = 1\\)|
|Number of sequences of length 3 from digits 1,2,3,4|\\(^nP_r = \frac{4!}{(4-3)!} = 24\\)|\\(^nC_r = \frac{4!}{3!.(4-3)!} = 4\\)|
|Sequences of length 3 from digits 1,2,3,4|123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431, 432|123, 124, 134, 234|

- **Permutations** return unique permutations of items, including their sequence. `123` is different to `321`.
- **Combinations** return unique combinations of items, ignoring sequence. It is about _members_, not _order_. `123` and `321` are _the same_.

## Demonstrating With Code

```python
from itertools import permutations, combinations

def convert_to_num(num_seq) -> str:
    """ Take a sequence of digits, and convert to a single str """
    return "".join(num_seq)

items = list(str(val) for val in range(1,4+1)) # [1, 2, 3, 4]
SELECTION_SZ = 3
print(f"items = {items}")

print("PERMUTATIONS")

# Get all the ways of ordering all the numbers...
perms = list(permutations(items))
print(f"Count of perms with size {len(items)}: {len(perms)}")
print(",".join(convert_to_num(perm) for perm in perms))

# Get all the ways of ordering 3 numbers from these four digits...
perms = list(permutations(items, SELECTION_SZ))
print(f"Count of perms with size {SELECTION_SZ}: {len(perms)}")
print(",".join(convert_to_num(perm) for perm in perms))

print("\nCOMBINATIONS")

# Get all the ways of picking all the numbers...
combos = list(combinations(items, len(items)))
print(f"Count of combos with size {len(items)}: {len(combos)}")
print(",".join(convert_to_num(combo) for combo in combos))

# Get all the ways of picking 3 numbers from these four digits...
combos = list(combinations(items, SELECTION_SZ))
print(f"Count of combos with size {SELECTION_SZ}: {len(combos)}")
print(",".join(convert_to_num(combo) for combo in combos))
```

Output:

```text
items = ['1', '2', '3', '4']
PERMUTATIONS
Count of perms with size 4: 24
1234,1243,1324,1342,1423,1432,2134,2143,2314,2341,2413,2431,3124,3142,3214,3241,3412,3421,4123,4132,4213,4231,4312,4321
Count of perms with size 3: 24
123,124,132,134,142,143,213,214,231,234,241,243,312,314,321,324,341,342,412,413,421,423,431,432

COMBINATIONS
Count of combos with size 4: 1
1234
Count of combos with size 3: 4
123,124,134,234
```

## Rolling Dice Examples

Imagine rolling two dice. 

```python
from itertools import combinations, combinations_with_replacement, product, permutations
 
die = list(range(1, 7))
print(f"One die: {die}")
 
# Cartesian product of throwing 2 dice
cp = list(product(die, repeat=2))
print("\nCARTESIAN PRODUCT")
print("All possible ways of throwing two dice:")
print(f"{cp}\nProduct count={len(cp)}")
 
# All unique permutations (order matters)
perms = list(permutations(die, 2))
print("\nPERMUTATIONS")
print("All unique combinations from two dice. A given number will not be repeated:")
print(f"{perms}\nCount of perms={len(perms)}")
 
# All unique combinations, disallowing the same number twice.  I.e. disallowing re-placement.
combos = list(combinations(die, 2))
print("\nCOMBINATIONS")
print("All unique combinations from two dice, ignoring throwing same on both dice:")
print(f"{combos}\nCount of combos={len(combos)}")
 
# All unique combinations, allowing re-placement
cwr = list(combinations_with_replacement(die, 2))
print("\nCOMBINATIONS WITH REPLACEMENT")
print("All unique combinations from two dice, including throwing same on both dice:")
print(f"{cwr}\nCount of combos={len(cwr)}")
```

Output:

```text
One die: [1, 2, 3, 4, 5, 6]

CARTESIAN PRODUCT
All possible ways of throwing two dice:
[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]    
Product count=36

PERMUTATIONS
All unique combinations from two dice. A given number will not be repeated:
[(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), (2, 3), (2, 4), (2, 5), (2, 6), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5)]
Count of perms=30

COMBINATIONS
All unique combinations from two dice, ignoring throwing same on both dice:
[(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)]
Count of combos=15

COMBINATIONS WITH REPLACEMENT
All unique combinations from two dice, including throwing same on both dice:
[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4), (3, 5), (3, 6), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (6, 6)]
Count of combos=21
```

  - The results `(1,6)` and `(6,1)` are considered two different permutations.
  - With two dice, there are 30 unique permutations. I.e. every unique (ordered) pair, except (1,1), (2,2), (3,3), etc.