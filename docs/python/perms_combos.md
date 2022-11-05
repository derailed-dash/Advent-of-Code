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
---
<script id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

## Overview of Permutations and Combinations

||Permutations|Combinations|
|-|------------|------------|
|What is it?|The number of ways to arrange items|The number of ways to choose items|
|Ordering   |Important|Irrelevant|
|Number of sequences of length r from data of length n|\\(^nP_r = \frac{n!}{(n-r)!}\\)|\\(^nC_r = \frac{n!}{r!(n-r)!}\\)|
|Number of sequences of length 4 from digits 1,2,3,4|\\(^nP_r = \frac{4!}{(4-4)!} = 24\\)|\\(^nC_r = \frac{4!}{4!.(4-4)!} = 1\\)|
|Number of sequences of length 3 from digits 1,2,3,4|\\(^nP_r = \frac{4!}{(4-3)!} = 24\\)|\\(^nC_r = \frac{4!}{3!.(4-3)!} = 4\\)|
|Sequences of length 3 from digits 1,2,3,4|123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431, 432|123, 124, 134, 234|

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