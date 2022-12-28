---
title: Useful Algorithms

main_img:
  name: Algorithms
  link: /assets/images/algorithms.png
tags: 
  - name: Merging intervals
    link: https://www.geeksforgeeks.org/merging-intervals/
  - name: Binary Search (RealPython)
    link: https://realpython.com/binary-search-python/
---
## Page Contents

- [Overview](#overview)
- [Merging Overlapping Intervals](#merging-overlapping-intervals)
- [Binary Search](#binary-search)

## Overview

Just a set of useful reusable algorithms...

## Merging Overlapping Intervals

```python
def merge_intervals(intervals: list[List]) -> list[list]:
    """ Takes intervals in the form [[a, b][c, d][d, e]...]
    Intervals can overlap.  Compresses to minimum number of non-overlapping intervals. """
    intervals.sort()
    stack = []
    stack.append(intervals[0])
    
    for interval in intervals[1:]:
        # Check for overlapping interval
        if stack[-1][0] <= interval[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], interval[-1])
        else:
            stack.append(interval)
      
    return stack

intervals = [[6, 8], [1, 9], [2, 4], [4, 7]]
merged = merge_intervals(intervals)
print(merged)
```

Output:

```text
[[1, 9]]
```

## Binary Search

Here I've created a generic binary search algorithm that can be used to pass a candidate number to an arbitrary function, and to finish when the function returns our _goal_.

```python
def binary_search(target, low:int, high:int, func, *func_args, reverse_search=False) -> int:
    """ Generic binary search function that takes a target to find,
    low and high values to start with, and a function to run, plus its args. 
    Implicitly returns None if the search is exceeded. """
    
    res = None  # just set it to something that isn't the target
    candidate = 0  # initialise; we'll set it to the mid point in a second
    
    while low < high:  # search exceeded        
        candidate = int((low+high) // 2)  # pick mid-point of our low and high        
        # print(f"{candidate}->{res}")
        res = func(candidate, *func_args) # run our function, whatever it is
        if res == target:
            return candidate  # solution found
        
        comp = operator.gt if not reverse_search else operator.lt
        if comp(res, target):
            low = candidate
        else:
            high = candidate
```