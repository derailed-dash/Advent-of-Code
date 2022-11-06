---
title: Permutations and Combinations

main_img:
  name: perms-and-combos
  link: /assets/images/permutations-combinations-definition.png
tags: 
  - name: Itertools
    link: https://docs.python.org/3/library/itertools.html
  - name: Itertools (GeeksForGeeks)
    link: https://www.geeksforgeeks.org/python-itertools/
  - name: Permutations and Combinations
    link: https://www.geeksforgeeks.org/permutation-and-combination-in-python/
  - name: Permutations with Examples
    link: https://www.pythonpool.com/python-permutations/
  - name: Permutations in Python
    link: https://medium.com/geekculture/permutations-in-python-431cd0c75253
---
<script id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

## Page Contents

- [Overview of Permutations and Combinations](#overview-of-permutations-and-combinations)
- [Demonstrating With Code](#demonstrating-with-code)
- [Rolling Dice Examples](#rolling-dice-examples)

## Overview of Permutations and Combinations

<table class="dazbo-table" style="width: 800px">
    <tr>
      <th style="width:200px"></th>
      <th style="width:320px">Permutations</th>
      <th style="width:280px">Combinations</th>
    </tr>
    <tr><td style="font-style: italic">What is it?</td><td>The number of ways to arrange items</td><td>The number of ways to choose items</td></tr>
    <tr><td style="font-style: italic">Ordering</td><td>Important</td><td>Irrelevant</td></tr>
    <tr><td style="font-style: italic">r items from n items</td><td>\(^nP_r = \frac{n!}{(n-r)!}\)</td><td>\(^nC_r = \frac{n!}{r!(n-r)!}\)</td></tr>
    <tr style="background: #ddffdd;"><td style="font-style: italic">All 4 items from digits 1,2,3,4</td><td>\(^{4}P_4 = \frac{4!}{(4-4)!} = 4! = 24\)</td><td>\(^{4}C_4 = \frac{4!}{4!.(4-4)!} = 1\)</td></tr>
    <tr style="background: #ddffdd;"><td style="font-style: italic">All 4 items from digits 1,2,3,4</td><td>1234, 1243, 1324, 1342, 1423, 1432, 2134, 2143, 2314, 2341, 2413, 2431, 3124, 3142, 3214, 3241, 3412, 3421, 4123, 4132, 4213, 4231, 4312, 4321</td><td>1234</td></tr>
    <tr style="background: #dddddd;"><td style="font-style: italic">3 items from digits 1,2,3,4</td><td>\(^{4}P_3 = \frac{4!}{(4-3)!} = 24\)</td><td>\(^{4}C_3 = \frac{4!}{3!.(4-3)!} = 4\)</td></tr>
    <tr style="background: #dddddd;"><td style="font-style: italic">3 items from digits 1,2,3,4</td><td>123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431, 432</td><td>123, 124, 134, 234</td></tr>
    <tr style="background: #fff2e6"><td style="font-style: italic">4 items from digits 0-9</td><td>\(^{10}P_4 = \frac{10!}{(10-4)!} = 5040\)</td><td>\(^{10}C_4 = \frac{10!}{4!.(10-4)!} = 210\)</td></tr>
</table>

- **Permutations** 
  - A unique arrangement of a group of things.
  - Returns unique permutations of items, including their sequence. So, given teh numbers `123`, `123` is a different permutation to `321`.
- **Combinations** return unique combinations of items, ignoring sequence. It is about _members_, not _order_. `123` and `321` are _the same_.

The number of permutations will be greater than the number of combinations.

## Demonstrating With Code

The `itertools` package provides both the `permutations()` and `combinations()` functions.

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

- There are 36 different outcomes from rolling two dice.  These outcomes can be determined using `itertools.product(die, repeat=n)` where `n` is the number of dice. This retuns the _cartesian product_ of our two dice.
- We can use `itertools.permutations(die, n)` to get all unique permutations of the two die rolls.
  - The results `(1,6)` and `(6,1)` are considered two different permutations.
  - Note that we only get 30 permutations.  This is because _permutations_ do not allow repeating numbers. E.g. it disallows `(1,1)`, `(2,2)`, etc. 
  - It is possible to determine _permutations with repeats_.  This is in fact equivalent to the _cartesian product_.
- If we ignore order, then `(1,2)` and `(2,1)` are the same. We use `itertools.combinations(die, n)` to determine all these combinations.
  - By default, repeating numbers are excluded. E.g. `(1,1)`, `(2,2)`, etc.
  - We can allow repeated numbers by using the method `combinations_with_replacement(die, 2)`. This this method gives more combinations.