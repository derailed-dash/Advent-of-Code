---
title: Comprehensions
main_img:
  name: That's convenient
  link: /assets/images/convenient.png
tags: 
  - name: Collection Comprehensions
    link: https://www.geeksforgeeks.org/comprehensions-in-python/
---
## Page Contents

- [Overview](#overview)
- [List Comprehension Example](#list-comprehension-example)
- [Aggregate Functions](#aggregate-functions)
- [Finding Adjacent Points Example](#finding-adjacent-points-example)

## Overview
In Python, a **comprehension** is a convenient shorthand for creating a collection, by iterating through an existing iterable.

## List Comprehension Example

This is easier to explain with an example!

Here's how we might use a `for loop` to determine the first 10 _cube_ numbers, and store them in a list:

```python
cube_numbers = []
for num in range(1, 11):
    cube_numbers.append(num**3)
    
print(cube_numbers)
```

The output looks like this:

```text
[1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]
```

But we can simplify the code, and make it look a bit more like _plain English_, by using a _list comprehension_:

```python
cube_numbers = [num**3 for num in range(1, 11)]
print(cube_numbers)
```

The output is identical! Cool, right?

So, **the general construct for a list comprehension** is:

```python
new_list = [expr(item) for item in iterable]
```

Note the use of square brackets around the comprehension. Thus, this comprehension returns a `list`.

## Aggregate Functions

Add we can apply aggregate functions, like we would with any other list. For example, if wanted to calculate the sum of the first 10 cube numbers:

```python
total = sum([num**3 for num in range(1, 11)])
print(total)
```

Output:

```text
3025
```

When we're applying an aggregate function around a comprehension, we can omit the square brackets. So, we can actually just write this:

```python
total = sum(num**3 for num in range(1, 11))
print(total)
```

## Finding Adjacent Points Example

This example starts by creating a `Point` class. It's just a dataclass. Then I create a list of `vectors`, which is made up of four `(x,y)` vectors to get from any given point to all its adjacent orthogonal points.

```python
@dataclass
class Point():
    x: int
    y: int

vectors = [
    (0, 1),  # up
    (1, 0),  # right
    (0, -1), # down
    (-1, 0)  # left
]

point = Point(3,2)
print(f"Starting point: {point}")

neighbours = [Point(point.x+dx, point.y+dy) for dx, dy in vectors]
print(f"Neighbours: {neighbours}") 
```

We then create a starting `Point` object, at location `3,2`. The cool part is where we use a `list comprehension` to iterate through the four vectors, with each returned as a `dx, dy` tuple. We then add each `dx` and `dy` to our starting point. The result is a list of four new points, as required.

The output:

```text
Starting point: Point(x=3, y=2)
Neighbours: [Point(x=3, y=3), Point(x=4, y=2), Point(x=3, y=1), Point(x=2, y=2)]
```