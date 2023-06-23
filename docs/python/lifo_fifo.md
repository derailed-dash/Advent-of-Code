---
title: LIFO, FIFO, and deques

main_img:
  name: "LIFO and FIFO"
  link: /assets/images/lifo_fifo.png
tags: 
  - name: Python's Deque (RealPython)
    link: https://realpython.com/python-deque/
---
## Page Contents

- [Overview](#overview)
- [Simple Use of the Deque as a Stack or Queue](#simple-use-of-the-deque-as-a-stack-or-queue)
- [Max Length Deques](#max-length-deques)
- [Circular Lists and Rotation](#circular-lists-and-rotation)
- [Examples](#examples)

## Overview

**LIFO means "Last-In, First-Out".** We typically to a data structure that stores elements in this way as a **stack**. For example, imagine a stack of plates, where put clean plates on the top, and when you want to use a plate, you also retrieve it from the top.

**FIFO means "First-In, First-Out".** We typically to a data structure that stores elements in this way as a **queue**.

In Python, we can use a `list` for both. The Python `list` is very efficient where we want to retrieve an element by some arbitrary index. They're also good if we want to append or pop (retrieve and remove) data from the _right hand end_.  Thus, they can be used for stacks.

However, if we predominantly only want LIFO (stack) or FIFO (queue) behaviour, then the Python `deque` (which means _"double-ended queue"_) is more efficient. This is because the `list` is not very efficient when we need to add any data that requires modifying the `list` data; adding any data at the front of a `list` would cause this to happen.

## Simple Use of the Deque as a Stack or Queue

Note that we create an empty `deque` and add items to it.  Or, we can create a deque from an existing iterable, such as a `list`, `tuple`, or `range`.

```python
from collections import deque

my_deque = deque([1, 2, 3, 4]) # populate the deque from a list
print(my_deque)

print("\nImplementing right-end stack behaviour...")
my_deque.append(10)
print(my_deque)

retrieved = my_deque.pop()
print(f"Retrieved: {retrieved}")
print(my_deque)

print("\nImplementing left-end stack behaviour...")
my_deque.appendleft(0)
print(my_deque)

retrieved = my_deque.popleft()
print(f"Retrieved: {retrieved}")
print(my_deque)

print("\nImplementing queue behaviour...")
my_deque.append(20)
print(my_deque)

retrieved = my_deque.popleft()
print(f"Retrieved: {retrieved}")
print(my_deque)
```

Note how we've used `append()` and `appendleft()`, as well as `pop()` and `popleft()`.

Output:

```text
deque([1, 2, 3, 4])

Implementing right-end stack behaviour...
deque([1, 2, 3, 4, 10])
Retrieved: 10
deque([1, 2, 3, 4])

Implementing left-end stack behaviour...
deque([0, 1, 2, 3, 4])
Retrieved: 0
deque([1, 2, 3, 4])

Implementing queue behaviour...
deque([1, 2, 3, 4, 20])
Retrieved: 1
deque([2, 3, 4, 20])
```

## Max Length Deques

This is really useful if we only want to keep the last `n` items of something. You can imagine implementing a _head_ or _tail_ function like this.

```python
from collections import deque

my_deque = deque(maxlen=3)

my_list = [1, 2, 3, 4]
my_deque.extend(my_list) # initialise with items from my_list
print(my_deque)
my_deque.append(10)
print(my_deque)
```

Note how we can use `extend()` (or `extendleft()`) to add multiple items from an interable.

Output:

```text
deque([2, 3, 4], maxlen=3)
deque([3, 4, 10], maxlen=3)
```

## Circular Lists and Rotation

Another useful feature of deque is the ability to call the `rotate(n)` method.  This takes `n` items from the right end and moves them to the left end, in a circular fashion.  (Known as rotating right.)   

- With no value specified, one item is rotated right. 
- With negative values, items are rotated left.

```python
from collections import deque
 
my_list = deque(range(1, 11))
print(f"Original:   {my_list}")
 
my_list.rotate()    # pops off the right and adds to the left
print(f"Right:      {my_list}")
 
my_list.rotate(3)
print(f"Right by 3: {my_list}")
 
my_list.rotate(-4)  # pops from the left and adds to the right
print(f"Left by 4:  {my_list}")
```

Output:

```text
Original:   deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Right:      deque([10, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Right by 3: deque([7, 8, 9, 10, 1, 2, 3, 4, 5, 6])
Left by 4:  deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
```

## Examples

- [Deque with sliding window - 2021 day 3](/2021/3)
- [Lantern fish timers and circular deque - 2021 day 6](/2021/6)
- [Flood fill lava basins with deque - 2021 day 9](/2021/9)
- [Stack popping using deque - 2021 day 10](/2021/10)
- [DFS exploding of nested tree with deque - 2021 day 18](/2021/18)
- [BFS best path with deque - 2022 day 12](/2022/12)
- [BFS flood fill with deque - 2022 day 18](/2022/18)
- [Circular numbers - 2022 day 20](/2022/20)
- [A deque to rotate through vectors - 2022 Day 23](/2022/23)
