---
title: Useful Algorithms

main_img:
  name: Algorithms
  link: /assets/images/algorithms.png
tags: 
  - name: Merging intervals
    link: https://www.geeksforgeeks.org/merging-intervals/
---
## Page Contents

- [Overview](#overview)
- [Merging Overlapping Intervals](#iterating-over-two-iterables-at-once)

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