---
title: Parsing with Parsimonious
tags: 
  - name: Recursion (Wikipedia)
    link: https://en.wikipedia.org/wiki/Recursion_(computer_science)
---
## Page Contents

- [Introduction](#introduction)
- [When Do You Use It?](#when-do-you-use-it)
- [The Rules](#the-rules)
- [Examples](#examples)
  - [Countdown](#countdown)
  - [Factorial](#factorial)
  - [Counting Leaf Items in a Nested List](#counting-leaf-items-in-a-nested-list)
  - [Fibonacci](#fibonacci)
  - [Calculating the Next Term in an Nth-Degree Arithmetic Progression](#calculating-the-next-term-in-an-nth-degree-arithmetic-progression)
- [AoC Examples](#aoc-examples)

## Introduction

I have to admit, I used to struggle with recursion.  A lot of people do.  It can be a bit mind-bending. But it's a pretty simple concept and can be very useful.

In short: **a recursive function is a function that calls itself.**  Thus, the code that defines the function will include a call to the same function.

As an anology, take a look at examples of recursive acronyms.  See how the acronym definition includes the acronym itself!

|Acronym|Definition|
|-------|----------|
|GNU| = GNU's not Linux|
|LAME| = LAME Ain't an MP3 Encoder|
|YAML|  YAML Ain't Markup Lanugage|

## When Do You Use It? 

Typical use cases include:

- Any time you need to calculate the _next_ value of something, based on the _current_ value of something.
- To traverse some sort of tree or nested structure.

We'll look at example of these in a bit.

## The Rules

When creating a recursive function, there are only two rules you need to know:

1. The function must have an _exit condition_, called the _base case_. You need this, otherwise your recursive function will never end!
1. Each recursive call should move us closer to the base case.

## Examples

### Countdown

We want to create recursive function that counts down from an arbitary number `n` to 0.  We can do it like this:

```python
def countdown(n):
    print(n)
    if n == 0:
        return             # Terminate recursion
    else:
        countdown(n - 1)   # Recursive call, one closer to the base case
```

As per the rules:

- We've defined a base condition.  I.e. when we get to 0, we exit.
- We've defined a condition that always moves us closer to the base condition. In this case, by decrementing the value of `n` each time by 1.

We can simplify this code:

```python
def countdown(n):
    print(n)
    if n > 0:
        countdown(n - 1)   # Recursive call, one closer to the base case
```

Let's try it.  I've added the above code to a file called scratch.py, in my snippets folder. I'll now execute it from the Python REPL:

```python
>>> from snippets.scratch import *
>>> countdown(5)
5
4
3
2
1
0
```

### Factorial

Recall the defition of factorial:

\\(k! = k * (k-1)\\)

This is slightly tricker than the previous example, since we're not just printing a value with each iteration.  Instead, we're always multiplying the current iteration by the result of the previous iteration.

So we can code it like this:

```python
def factorial(n):
     return 1 if n <= 1 else n * factorial(n - 1)
```

- The base condition is when `n == 1`.  In this situation, `factorial` should always return 1.
- If not the base condition, we always multiply by a recursive call where `n` is decremented by 1.

Note that it's common for any recusive function that calculates a _product_ to have an exit condition that returns 1.

We can see how function works by adding some debugging statements:

```python
def factorial(n):
    print(f"factorial() called with n = {n}")
    return_value = 1 if n <= 1 else n * factorial(n -1)
    print(f"-> factorial({n}) returns {return_value}")
    return return_value
```

Let's run it from the REPL:

```python
>>> from snippets.scratch import *
>>> factorial(4)
factorial() called with n = 4
factorial() called with n = 3
factorial() called with n = 2
factorial() called with n = 1
-> factorial(1) returns 1
-> factorial(2) returns 2
-> factorial(3) returns 6
-> factorial(4) returns 24
24
```

Note how each `return` is the product of `n` and the previous return value.

### Counting Leaf Items in a Nested List

Here we create a recursive function that counts all the individual elements in a list.  If the list is nested, the function recurses into each _sub_ list, adding the elements of that list to the overall count.

```python
def count_leaf_items(item_list):
    """Recursively counts and returns the number of leaf items
       in a (potentially nested) list. """
    count = 0
    for item in item_list:
        if isinstance(item, list): # if the element is itself a list, recurse...
            count += count_leaf_items(item)
        else: # count the item
            # this is the exit condition, i.e. when we've reached a leaf (element) rather than a nested list
            count += 1  

    return count
```

Let's try this...

```python
nested_list = [2, [3,5], [[10,20],30]]
print(nested_list)

res = count_leaf_items(nested_list)
print(res)
```

Output:

```text
[2, [3, 5], [[10, 20], 30]]
6
```

### Fibonacci

The Fibonacci sequence is an infinite sequence that generates the next number by adding the two preceding numbers.

`1, 1, 2, 3, 5, 8, 13, 21...`

I.e. to determine the `nth` value in the sequence:

\\(f(n) = f(n-2) + f(n-1)\\)

The base case is where `n` is `1`, which returns a value of `1`.

```python
def fib(num: int) -> int:
    """ Recursive function to determine nth value of Fibonacci sequence.
    I.e. 1, 1, 2, 3, 5, 8, 13, 21...
    fib(n) = fib(n-2) + fib(n-1)

    Args:
        num (int): value of n, i.e. to determine nth value

    Returns:
        int: The nth value of the Fibonacci sequence
    """
    if num > 2:
        return fib(num-2) + fib(num-1)
    else:
        return 1

while True:
    try:
        input_val = input("Enter the value of n, or q to quit: ")
        if input_val.upper() == "Q":
            break
        
        print(fib(int(input_val)))
    except ValueError as err:
        print("Invalid input")
```

Note: this isn't a particularly efficient function. It doesn't scale well!

## Calculating the Next Term in an Nth-Degree Arithmetic Progression

An arithmetic progression (AP) is a sequence of numbers in which the difference of any two successive members is a constant. This difference is commonly referred to as the _"common difference"_. For example:

```text
Progression: 0   3   6   9  12  15  18
Common diff:   3   3   3   3   3   3
```

A second-degree arithmetic progression is one in which the differences between terms is growing, but growing by a constant amount. Thus, _differences of differences_ are common:

Triangle numbers are a common example:

```text
       Progression: 1   3   6  10  15  21
          First diff: 2   3   4   5   6
Second (common) diff:   1   1   1   1
```

We can extrapolate this to the Nth Degree. I.e. the number of times you have to determine differences, before the differences are common. If you determine the number of degrees after which the differences are common, you can bubble the results back up to the top, in order to determine the next term in the sequence.

So this is a good candidate for a recursive function:

```python
def recurse_diffs(sequence: np.ndarray, forwards=True) -> int:
    """
    Calculate the next value in a numeric sequence based on the pattern of differences.

    Recursively analyses the differences between consecutive elements of the sequence. Recurses until the differences remain constant. It then calculates the next value in the sequence based on this constant difference.

    Parameters:
        sequence (np.ndarray): A NumPy array representing the sequence.
        forwards (bool, optional): A flag to determine the direction of progression.
                                   If True (default), the function calculates the next value. 
                                   If False, it calculates the previous value in the sequence.

    Returns:
        int: The next (or previous) value in the sequence
    """
    diffs = np.diff(sequence)
    
    op = operator.add if forwards else operator.sub
    term = sequence[-1] if forwards else sequence[0]
    
    # Check if all the diffs are constant
    # If they are, we've reached the deepest point in our recursion, and we know the constant diff
    if np.all(diffs == diffs[0]):
        next_val = op(term, diffs[0])
    else: # if the diffs are not constant, then we need to recurse
        diff = recurse_diffs(diffs, forwards)
        next_val = op(term, diff)
        
    return int(next_val)
```

## AoC Examples

- [Recursively process json - 2015 day 12](/2015/12)
- [Recursive string replacement - 2021 day 14](/2021/14)
- [Various recursinos as methods of a class - 2021 day 16](/2021/16)
- [Recursive snail mail - 2021 day 18](/2021/18)
- [Recursive game states using dynamic programming and lru cache - 2021 day 21](/2021/21)
- [Recursive directory listing by extending the list - 2022 day 7](/2022/7)
- [Recursive `__lt__` compare - 2022 day 13](/2022/13)
- [Recursive arithmetic progressions - 2023 day 9](https://colab.research.google.com/github/derailed-dash/Advent-of-Code/blob/master/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb){:target="_blank"}
- [Creating a pretty print with recursion and max depth - 2024 day 24](https://colab.research.google.com/github/derailed-dash/Advent-of-Code/blob/master/src/AoC_2024/Dazbo's_Advent_of_Code_2024.ipynb){:target="_blank"}