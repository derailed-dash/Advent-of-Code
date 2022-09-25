---
title: Recursion
main_img:
  name: Argand Plot
  link: /assets/images/recursion.gif
tags: 
  - name: Recursion (Wikipedia)
    link: https://en.wikipedia.org/wiki/Recursion_(computer_science)
  - name: Recursion Introduction (@ RealPython)
    link: https://realpython.com/python-recursion/
---
<script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>
## Page Contents

- [Introduction](#introduction)
- [When Do You Use It?](#when-do-you-use-it)
- [The Rules](#the-rules)
- [Examples](#examples)
  - [Countdown](#countdown)
  - [Factorial](#factorial)
  - [Counting Leaf Items in a Nested List](#counting-leaf-items-in-a-nested-list)

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