---
day: 3
title: Day 3
problem: Binary Diagnostic
main_img:
  name: squiddie
  link: /assets/images/squiddy.jpg
tags: 
  - name: Complex Numbers
    link: https://realpython.com/python-complex-numbers/
  - name: List Comprehension
    link: https://www.geeksforgeeks.org/python-list-comprehension/
  - name: vectors
---

## Solution Intro

We need to...

Input looks like...

```
```

I wrote two different solutions to this problem.

- [Solution #1](#solution-1) - Nothing clever
- [Solution #2](#solution-2) - Making use of Numpy

## Solution #1

### Setup

### Part 1

The goal for part 1 is to parse a list of depth figures, and count how many times the depth increases.

```python
```

<img src="{{ site.url }}{{ site.baseurl }}/assets/images/input_folder_location.png" alt="drawing" style="width:250px;"/>


### Solving the Problem

The input data looks something like this:

```
199
200
208
210
200
```

This is a simple problem.  We want to look at each number, and see if it's bigger than the previous number.

### Part 2

Now the challenge is a tiny bit harder.  Rather than comparing each number to the last,
we now need to compare a sliding window of 3 numbers to the previous 3 numbers.

```python
```

## Solution #2

Here I'm using Numpy, a data science package that is awesome for manipulating arrays of data.
It makes for much shorter code in a problem like this.

### Setup

If you don't have Numpy installed, the easiest way to install it is with pip:

```
py -m pip install numpy
```
The rest of the setup is the same as before.

### Solving the Problem

```python
```

And that's it!