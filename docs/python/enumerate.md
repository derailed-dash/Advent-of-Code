---
title: Enumerate and Enum
tags: 
  - name: Enumerate
    link: https://realpython.com/python-enumerate/
  - name: Enum (GeeksforGeeks)
    link: https://www.geeksforgeeks.org/enum-in-python/
  - name: Enum (Real Python)
    link: https://realpython.com/python-enum/
  - name: Enum (Python Docs)
    link: https://docs.python.org/3/library/enum.html
  - name: classes
    link: /python/classes
---
## Page Contents

- [Enumerate](#enumerate)
- [Enum](#enum)
  - [The Enum Data Type](#the-enum-data-type)
  - [Enum vs Dict](#enum-vs-dict)
  - [Example: Using Enum for Directions](#example-using-enum-for-directions)

## Enumerate

**The enumerate function is useful for obtaining a counter for any loop.**

Here is a demonstration of how we can use `enumerate()` with a `list` of input lines:

```python
input_data = """Some line of text
Another line
The last line"""

input_lines = input_data.splitlines()
print(input_lines)
print(list(enumerate(input_lines)))
```

Here's the output:

```text
['Some line of text', 'Another line', 'The last line']
[(0, 'Some line of text'), (1, 'Another line'), (2, 'The last line')]
```

We can see that the `enumerate()` function has turned each line into a numbered `tuple`.

A more common way to use `enumerate()` is in a loop.  For example:

```python
print("Iterating over names...")
names = ("Darren", "Josh", "Julie")
for name in names:
    print(name)

print("\nAnd now, with enumeration...")
for i, name in enumerate(names):
    print(f"{i}: {name}")
```

Output:

```text
Darren
Josh
Julie

And now, with enumeration...
0: Darren
1: Josh
2: Julie
```

Thus, using `enumerate` has given us a counter, which starts at 0 by default. We can change the start value by adding a second parameter to `enumerate()`, i.e. `start=some_value`. For example:

```python
names = ("Darren", "Josh", "Julie")
for i, name in enumerate(names, start=1):
    print(f"{i}: {name}")
```

Output:

```text
1: Darren
2: Josh
3: Julie
```

## Enum

### The Enum Data Type

We can also create an _Enum_ data type in Python.  This is quite different to using `enumerate()`.  Instead, an _Enum_ data type allows us to create a set of related, named constants.

Here's an example of we might use an _Enum_:

```python
from enum import Enum

class Vector(Enum):
    """ Enumeration of 8 directions, and a rotating list of direction choices. """
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)
    
print("Iterating over Vector...")
for direction in Vector:
    print(direction)
    print(f"{direction.name}: {direction.value}")

print("\nBy specific item...")
print(Vector.N.name)
print(Vector.N.value)
```

Here's the output:

```text
Iterating over Vector...
Vector.N
N: (0, -1)
Vector.E
E: (1, 0)
Vector.S
S: (0, 1)
Vector.W
W: (-1, 0)

By specific item...
N
(0, -1)
```

Some things to note:

- We define an _enum_ by **subclassing `Enum`**.
- We define a **related set of constants** which are _members_ of our _enum_. Since these are constants, by convention, they should all be defined using all-caps. In the example above, these are `N`, `E`, `S`, and `W`.
- The members are constant and **hashable**; this means we can use them anywhere we need a value to be hashable.
- Because the members must be constant, any attempt to change a member's value will result in an `AttributeError`.
- We can easily **iterate** over all members of a given _enum_.
- We can obtain an _enum's namespace_ (e.g. `Vector`), its _name_ (e.g. `N`), and its _value_ (e.g. `(0, -1)`).
- IDEs and linters support auto-completion of an _enum_.

### Enum vs Dict

We could create _similar_ behaviour by using a dictionary. E.g.

```python
VECTOR = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0)
}
    
print("Iterating over Vector...")
for direction in VECTOR:
    print(direction)
    print(f"{direction}: {VECTOR[direction]}")

print("\nBy specific item...")
print(VECTOR["N"])
```

Output:

```text
N
N: (0, -1)
E
E: (1, 0)
S
S: (0, 1)
W
W: (-1, 0)

By specific item...
(0, -1)
```

The main disadvantage of using a `dict` is that it's easy to create a typo when specifying the key.

### Example: Using Enum for Directions

Here's a more interesting example:

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Point():
    """ Point x,y which knows how to add another point, 
    and how to return all adjacent points, including diagonals. """
    x: int
    y: int

    def all_neighbours(self) -> set[Point]:
        """ Return all adjacent orthogonal (not diagonal) Points """
        return {(self + vector.value) for vector in list(Vector)}
    
    def get_neighbours(self, directions: list[Vector]) -> set[Point]:
        return {(self + vector.value) for vector in list(directions)}
        
    def __add__(self, other) -> Point:
        """ Subtract other point from this point, returning new point vector """
        return Point(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"P({self.x},{self.y})"

class Vector(Enum):
    """ Enumeration of 8 directions, and a rotating list of direction choices. """
    N = Point(0, -1)
    NE = Point(1, -1)
    E = Point(1, 0)
    SE = Point(1, 1)
    S = Point(0, 1)
    SW = Point(-1, 1)
    W = Point(-1, 0)
    NW = Point(-1, -1)
    
start = Point(10, 10)
print(f"All adjacent points to {start}:")
print(start.all_neighbours())

print(f"Get northerly neighbours to {start}:")
print(start.get_neighbours([Vector.NW, Vector.N, Vector.NE]))
```

## Examples

- [Enumerating ordinals - 2022 Day 3](/2022/3)
- [Enumerating characters in input - 2022 Day 22](/2022/22)
- [Enumerating rows and columns - 2022 Day 24](/2022/24)
- [Tetris Shape Enum and Shape factory - 2022 Day 17](/2022/17)
- [Enum of Vectors - type_defs](/python/reusable_code)